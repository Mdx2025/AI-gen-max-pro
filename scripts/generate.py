#!/usr/bin/env python3
"""
AI GEN MAX — generate.py
Multi-provider media generation executor.

Usage:
  python3 generate.py '<json_config>'

JSON config fields:
  provider        : piapi | fal | together | runware
  model           : provider-specific model ID or key
  task_type       : piapi task_type (required for piapi)
  params          : dict of model parameters
  media_type      : image | video | audio | music | 3d | tool
  routing         : optional route signals (`route_id`, `operation`, `goal`, etc.)
  estimated_cost  : human-readable cost string
  output_dir      : output directory path (default: ~/.openclaw/media)
"""

import base64
import json
import mimetypes
import os
import sys
import time
import uuid
import requests
from pathlib import Path
from datetime import datetime

try:
    from PIL import Image
except Exception:  # pragma: no cover - optional runtime guard
    Image = None

from model_manifest import (
    FAL_EDIT_MAP,
    FAL_EXT_MAP,
    FAL_I2V_MAP,
    FAL_MODEL_MAP,
    PIAPI_MODEL_MAP,
    resolve_route_selection,
    TASK_EXT_MAP,
    validate_route_constraints,
)
from prompt_compiler import compile_prompt


# ─────────────────────────────────────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────────────────────────────────────

CONFIG_PATH = Path.home() / ".openclaw" / "ai-gen-max.env"
DEFAULT_OUTPUT_DIR = Path.home() / ".openclaw" / "media"

POLL_INTERVAL = 5    # seconds between polls
MAX_POLLS = 360      # 30 minutes max
MIN_IMAGE_LONG_SIDE = 1280
MIN_IMAGE_SHORT_SIDE = 720


def load_env() -> dict:
    env = {}
    if CONFIG_PATH.exists():
        for line in CONFIG_PATH.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, _, v = line.partition("=")
                env[k.strip()] = v.strip()
    for key in ("FAL_API_KEY", "PIAPI_API_KEY", "TOGETHER_API_KEY",
                "RUNWARE_API_KEY", "KIE_API_KEY", "OPENAI_API_KEY"):
        if os.environ.get(key):
            env[key] = os.environ[key]
    return env


def get_key(env: dict, key: str, provider_name: str) -> str:
    val = env.get(key, "")
    if not val:
        raise ValueError(
            f"{key} not configured.\n"
            f"Add it to {CONFIG_PATH}:\n  {key}=your_key_here"
        )
    return val


# ─────────────────────────────────────────────────────────────────────────────
# UTILITIES
# ─────────────────────────────────────────────────────────────────────────────

def make_output_path(output_dir: Path, media_type: str, ext: str) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    return output_dir / f"aigen_{media_type}_{ts}.{ext}"


def download(url: str, timeout: int = 300) -> bytes:
    resp = requests.get(url, timeout=timeout, stream=True)
    resp.raise_for_status()
    chunks = []
    for chunk in resp.iter_content(chunk_size=65536):
        if chunk:
            chunks.append(chunk)
    return b"".join(chunks)


def upload_to_fal(local_path: str, api_key: str) -> str:
    path = Path(local_path)
    if not path.exists():
        raise FileNotFoundError(f"Image not found: {local_path}")
    mime_type = mimetypes.guess_type(str(path))[0] or "image/png"
    log(f"  Uploading {path.name} to fal.ai storage...")
    data = path.read_bytes()

    # Step 1: initiate upload → get presigned GCS URL + final file_url
    init_resp = requests.post(
        "https://rest.fal.ai/storage/upload/initiate?storage_type=gcs",
        headers={
            "Authorization": f"Key {api_key}",
            "Accept": "application/json",
            "Content-Type": "application/json",
        },
        json={"file_name": path.name, "content_type": mime_type},
        timeout=30,
    )
    if not init_resp.ok:
        # Fallback: CDN direct upload
        cdn_resp = requests.post(
            "https://fal.media/files/upload",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": mime_type,
                "X-Fal-File-Name": path.name,
            },
            data=data,
            timeout=60,
        )
        if not cdn_resp.ok:
            raise RuntimeError(f"fal.ai upload failed [{cdn_resp.status_code}]: {cdn_resp.text[:200]}")
        url = cdn_resp.json().get("access_url")
        if not url:
            raise RuntimeError(f"fal.ai CDN upload: no access_url: {cdn_resp.text[:200]}")
        log(f"  Uploaded (CDN): {url}")
        return url

    init_result = init_resp.json()
    upload_url = init_result.get("upload_url")
    file_url = init_result.get("file_url")
    if not upload_url or not file_url:
        raise RuntimeError(f"fal.ai initiate: missing fields: {init_resp.text[:200]}")

    # Step 2: PUT binary to presigned URL
    put_resp = requests.put(
        upload_url,
        data=data,
        headers={"Content-Type": mime_type},
        timeout=120,
    )
    if not put_resp.ok:
        raise RuntimeError(f"fal.ai GCS PUT failed [{put_resp.status_code}]: {put_resp.text[:200]}")

    log(f"  Uploaded (GCS): {file_url}")
    return file_url


def resolve_image_url(image_ref: str, api_key: str = "", provider: str = "fal") -> str:
    if image_ref.startswith("https://") or image_ref.startswith("http://"):
        return image_ref
    if not api_key:
        raise ValueError(
            "FAL_API_KEY is required to upload local images. "
            "Add it to ~/.openclaw/ai-gen-max.env"
        )
    return upload_to_fal(image_ref, api_key)


def resolve_media_ref(media_ref: str, api_key: str = "") -> str:
    if media_ref.startswith("https://") or media_ref.startswith("http://"):
        return media_ref
    if not api_key:
        raise ValueError(
            "FAL_API_KEY is required to upload local media references. "
            "Add it to ~/.openclaw/ai-gen-max.env"
        )
    return upload_to_fal(media_ref, api_key)


def ext_for(media_type: str) -> str:
    return {
        "video": "mp4", "audio": "wav", "music": "mp3", "3d": "glb",
    }.get(media_type, "png")


def _image_needs_hd_guard(image_path: str) -> tuple[bool, int, int]:
    if Image is None:
        return False, 0, 0

    with Image.open(image_path) as image:
        width, height = image.size

    long_side = max(width, height)
    short_side = min(width, height)
    needs_guard = long_side < MIN_IMAGE_LONG_SIDE or short_side < MIN_IMAGE_SHORT_SIDE
    return needs_guard, width, height


def _pick_upscale_factor(width: int, height: int) -> int:
    long_side = max(width, height)
    short_side = min(width, height)
    required = max(
        MIN_IMAGE_LONG_SIDE / max(long_side, 1),
        MIN_IMAGE_SHORT_SIDE / max(short_side, 1),
    )
    if required <= 1:
        return 1
    if required <= 2:
        return 2
    return 4


def ensure_preservation_contract(
    result: dict,
    source_local_path: str | None,
) -> dict:
    """Assert the output canvas matches the source canvas.

    Called when the selected route has `preservation_mode == "strict"`.
    Converts "lane promised preservation, provider reframed anyway" from a
    silent quality bug into a hard failure the caller can see.
    """
    saved_path = result.get("saved_path")
    if not saved_path or not source_local_path or Image is None:
        return result

    source_path = Path(source_local_path)
    if not source_path.exists():
        return result

    try:
        with Image.open(saved_path) as out_img:
            out_size = out_img.size
        with Image.open(source_path) as src_img:
            src_size = src_img.size
    except Exception as e:  # pragma: no cover - defensive
        result["preservation_check"] = {"status": "skipped", "reason": str(e)}
        return result

    if out_size != src_size:
        raise RuntimeError(
            "Preservation contract violated: strict-preservation lane returned a reframed canvas. "
            f"Source {src_size[0]}x{src_size[1]} != output {out_size[0]}x{out_size[1]}. "
            "Provider reframe is a known limitation of generative edit lanes. "
            "For true canvas preservation, use a mask-based inpaint lane (e.g. image-strict-inpaint with bria-eraser)."
        )

    result["preservation_check"] = {
        "status": "ok",
        "source_size": list(src_size),
        "output_size": list(out_size),
    }
    return result


def ensure_min_hd_image(result: dict, api_key: str, output_dir: Path) -> dict:
    saved_path = result.get("saved_path")
    if not saved_path or result.get("model") == FAL_MODEL_MAP.get("image-upscale"):
        return result

    needs_guard, width, height = _image_needs_hd_guard(saved_path)
    if not needs_guard:
        return result

    upscale_factor = _pick_upscale_factor(width, height)
    log(
        "  Output below HD-equivalent "
        f"({width}x{height}); upscaling x{upscale_factor} before delivery..."
    )

    # fal expects image_url to be a public URL. saved_path is a local
    # filesystem path; POSTing it directly returns 422. Upload it first.
    try:
        image_url = upload_to_fal(saved_path, api_key)
    except Exception as e:
        log(f"  Upscale skipped: upload failed ({e})")
        return result

    upscaled = generate_fal(
        "image-upscale",
        {"image_url": image_url, "upscale_factor": upscale_factor},
        api_key,
        "image",
        output_dir,
    )
    upscaled["upscaled_from"] = saved_path
    upscaled["original_dimensions"] = {"width": width, "height": height}
    return upscaled


def log(msg: str, end: str = "\n"):
    print(msg, end=end, flush=True)


# Routing constants live in model_manifest.py.


def _remap_fal_params(fal_model: str, params: dict) -> dict:
    """Translate PiAPI-style params into fal.ai equivalents."""
    p = dict(params)

    # Strip PiAPI-only fields
    for key in ("version", "mode", "prefer_multi_shots", "resolution"):
        p.pop(key, None)

    # enable_audio → generate_audio (Kling)
    if "enable_audio" in p:
        p["generate_audio"] = p.pop("enable_audio")

    # Kling I2V: image_url → start_image_url
    if "image-to-video" in fal_model and "kling" in fal_model:
        if "image_url" in p and "start_image_url" not in p:
            p["start_image_url"] = p.pop("image_url")

    # Kling / Seedance duration must be string ("5", "10", etc.)
    if ("kling-video" in fal_model or "seedance" in fal_model) and "duration" in p:
        p["duration"] = str(p["duration"])

    # Sora 2: generate_audio/enable_audio → audio (bool)
    # Note: enable_audio was already converted to generate_audio above (line ~402)
    if "sora-2" in fal_model:
        if "generate_audio" in p:
            p["audio"] = p.pop("generate_audio")
        elif "enable_audio" in p:
            p["audio"] = p.pop("enable_audio")

    # Veo 3.1 family prefers generate_audio and string durations (e.g. "8s")
    if "veo3.1" in fal_model:
        if "enable_audio" in p and "generate_audio" not in p:
            p["generate_audio"] = p.pop("enable_audio")
        elif "enable_audio" in p:
            p.pop("enable_audio", None)
        if "audio" in p and "generate_audio" not in p:
            p["generate_audio"] = p.pop("audio")
        if isinstance(p.get("duration"), int):
            p["duration"] = f"{p['duration']}s"
        elif isinstance(p.get("duration"), str) and p["duration"].isdigit():
            p["duration"] = f"{p['duration']}s"

    # Ace-Step: style_prompt → tags
    if "ace-step" in fal_model:
        if "style_prompt" in p and "tags" not in p:
            p["tags"] = p.pop("style_prompt")
        # audio-to-audio mode
        if p.get("task_type") == "audio2audio":
            p.pop("task_type", None)

    # DiffRhythm: task_type → music_duration
    if "diffrhythm" in fal_model:
        task = p.pop("task_type", "")
        if "music_duration" not in p:
            p["music_duration"] = "285s" if "full" in task else "95s"

    # F5-TTS: ref_audio → ref_audio_url; add model_type
    if "f5-tts" in fal_model:
        if "ref_audio" in p and "ref_audio_url" not in p:
            p["ref_audio_url"] = p.pop("ref_audio")
        p.setdefault("model_type", "F5-TTS")

    # MMAudio: video → video_url
    if "mmaudio" in fal_model:
        if "video" in p and "video_url" not in p:
            p["video_url"] = p.pop("video")

    # Remove BG (birefnet): image → image_url
    if "birefnet" in fal_model:
        if "image" in p and "image_url" not in p:
            p["image_url"] = p.pop("image")

    # Image upscale: image → image_url, scale → upscale_factor
    if "clarity-upscaler" in fal_model:
        if "image" in p and "image_url" not in p:
            p["image_url"] = p.pop("image")
        if "scale" in p and "upscale_factor" not in p:
            p["upscale_factor"] = p.pop("scale")

    # Bria Eraser: strict subtractive inpaint. Requires image_url + mask_url.
    # Preserves canvas by construction — only modifies the mask region.
    if "bria/eraser" in fal_model:
        if "image" in p and "image_url" not in p:
            p["image_url"] = p.pop("image")
        if "mask" in p and "mask_url" not in p:
            p["mask_url"] = p.pop("mask")
        p.pop("task_type", None)
        p.pop("prompt", None)  # eraser takes no prompt
        p.pop("aspect_ratio", None)  # inherited from source

    # Flux inpaint (general): image_url + mask_url + prompt.
    if "flux-general/inpainting" in fal_model:
        if "image" in p and "image_url" not in p:
            p["image_url"] = p.pop("image")
        if "mask" in p and "mask_url" not in p:
            p["mask_url"] = p.pop("mask")
        p.pop("task_type", None)
        p.pop("aspect_ratio", None)

    # Flux Fill Pro: image_url + mask_url + prompt (inpaint/outpaint).
    if "flux-pro/v1/fill" in fal_model:
        if "image" in p and "image_url" not in p:
            p["image_url"] = p.pop("image")
        if "mask" in p and "mask_url" not in p:
            p["mask_url"] = p.pop("mask")
        p.pop("task_type", None)
        p.pop("aspect_ratio", None)

    # IC-Light v2: relight lane. Takes image_url + prompt. Canvas-preserving by design.
    # IMPORTANT: IC-Light defaults `hr_downscale` to 0.5 which returns a half-size
    # output. That violates `ensure_preservation_contract` (strict pixel match).
    # Force `hr_downscale=1.0` unless the caller overrode it.
    if "iclight-v2" in fal_model:
        if "image" in p and "image_url" not in p:
            p["image_url"] = p.pop("image")
        p.pop("task_type", None)
        p.pop("aspect_ratio", None)
        p.pop("mask_url", None)  # iclight is global relight, not masked
        p.pop("mask", None)
        p.setdefault("hr_downscale", 1.0)
        p.setdefault("output_format", "png")

    # Trellis: images array → image_url (fal takes single)
    # Exclude trellis/multi and trellis-2 — they have their own handling below
    if "trellis" in fal_model and "/multi" not in fal_model and "trellis-2" not in fal_model:
        if "images" in p and "image_url" not in p:
            imgs = p.pop("images")
            if isinstance(imgs, list) and imgs:
                p["image_url"] = imgs[0]
        p.pop("task_type", None)

    # Hunyuan: map to fal params (no duration, no audio)
    if "hunyuan-video" in fal_model:
        p.pop("task_type", None)
        p.pop("audio", None)
        p.pop("duration", None)
        p.pop("generate_audio", None)
        p.pop("enable_audio", None)

    # Luma Ray 2: strip unsupported fields
    if "luma-dream-machine" in fal_model:
        p.pop("enable_audio", None)
        p.pop("generate_audio", None)
        p.pop("task_type", None)

    # PixVerse: strip unsupported fields
    if "pixverse" in fal_model:
        p.pop("enable_audio", None)
        p.pop("generate_audio", None)
        p.pop("task_type", None)
        if "video" in p and "video_url" not in p:
            p["video_url"] = p.pop("video")

    # Hailuo 02: no aspect_ratio param, use resolution
    if "hailuo-02" in fal_model or "hailuo-2.3" in fal_model:
        ar = p.pop("aspect_ratio", None)
        p.pop("enable_audio", None)
        p.pop("generate_audio", None)
        p.pop("task_type", None)
        if ar and "resolution" not in p:
            p["resolution"] = "720p" if ar in ("16:9", "4:3") else "720p"

    # CogVideoX: fixed 10s, no duration/aspect_ratio
    if "cogvideox" in fal_model:
        p.pop("duration", None)
        p.pop("aspect_ratio", None)
        p.pop("task_type", None)

    # MiniMax Music: style_prompt → prompt
    if "minimax-music" in fal_model:
        if "style_prompt" in p and "prompt" not in p:
            p["prompt"] = p.pop("style_prompt")
        p.pop("task_type", None)

    # CassetteAI: style_prompt → text
    if "cassetteai" in fal_model:
        if "style_prompt" in p and "text" not in p:
            p["text"] = p.pop("style_prompt")
        elif "prompt" in p and "text" not in p:
            p["text"] = p.pop("prompt")
        p.pop("task_type", None)

    # Beatoven: style_prompt → prompt; duration → duration_in_seconds
    if "beatoven" in fal_model:
        if "style_prompt" in p and "prompt" not in p:
            p["prompt"] = p.pop("style_prompt")
        if "duration" in p and "duration_in_seconds" not in p:
            p["duration_in_seconds"] = p.pop("duration")
        p.pop("task_type", None)

    # Recraft: strip unsupported fields
    if "recraft" in fal_model:
        p.pop("negative_prompt", None)
        p.pop("task_type", None)

    # Ideogram: strip unsupported fields
    if "ideogram" in fal_model:
        p.pop("negative_prompt", None)
        p.pop("task_type", None)
        # aspect_ratio maps directly (16:9 → ASPECT_16_9 format on some versions)

    # Seedream: strip unsupported fields
    if "seedream" in fal_model:
        p.pop("task_type", None)
        if "/edit" in fal_model:
            if "image_urls" not in p and "image_url" in p:
                p["image_urls"] = [p.pop("image_url")]
            elif "image_urls" in p:
                p.pop("image_url", None)

    # GPT Image 2 / 1.5: default to benchmarked high quality and use image_urls[] for edit.
    if "gpt-image-2" in fal_model or "gpt-image-1.5" in fal_model:
        p.pop("task_type", None)
        p.setdefault("quality", "high")
        if "aspect_ratio" in p and "image_size" not in p:
            aspect_map = {
                "1:1": "square",
                "16:9": "landscape_16_9",
                "9:16": "portrait_16_9",
                "4:3": "landscape_4_3",
                "3:4": "portrait_4_3",
                "3:2": "landscape_3_2",
                "2:3": "portrait_3_2",
            }
            p["image_size"] = aspect_map.get(str(p.pop("aspect_ratio")), "landscape_4_3")
        if "/edit" in fal_model:
            if "image_urls" not in p and "image_url" in p:
                p["image_urls"] = [p.pop("image_url")]
            elif "image_urls" in p:
                p.pop("image_url", None)

    # FLUX.2 edit endpoints accept image_urls[] for image editing calls.
    if "flux-2-" in fal_model and "/edit" in fal_model:
        if "image_urls" not in p and "image_url" in p:
            p["image_urls"] = [p.pop("image_url")]
        elif "image_urls" in p:
            p.pop("image_url", None)
        p.pop("task_type", None)

    # FLUX Kontext: keeps image_url as reference (not I2V)
    if "kontext" in fal_model:
        p.pop("task_type", None)

    # Nano Banana edit endpoints require image_urls[]
    if "nano-banana" in fal_model and "/edit" in fal_model:
        if "image_urls" not in p and "image_url" in p:
            p["image_urls"] = [p.pop("image_url")]
        elif "image_urls" in p and "image_url" in p:
            p.pop("image_url", None)
        p.pop("task_type", None)

    # Grok Imagine image edit also expects image_urls[]
    if "xai/grok-imagine-image/edit" in fal_model:
        if "image_urls" not in p and "image_url" in p:
            p["image_urls"] = [p.pop("image_url")]
        elif "image_urls" in p and "image_url" in p:
            p.pop("image_url", None)
        p.pop("task_type", None)

    # Grok Imagine video reference lane expects reference_image_urls
    if "xai/grok-imagine-video/reference-to-video" in fal_model:
        if "reference_image_urls" not in p and "image_urls" in p:
            p["reference_image_urls"] = p.pop("image_urls")
        elif "reference_image_urls" not in p and "image_url" in p:
            p["reference_image_urls"] = [p.pop("image_url")]
        p.pop("task_type", None)

    # Seedance reference-to-video accepts plural media refs
    if "seedance-2.0/reference-to-video" in fal_model:
        if "image_urls" not in p and "image_url" in p:
            p["image_urls"] = [p.pop("image_url")]
        if "video_urls" not in p and "video_url" in p:
            p["video_urls"] = [p.pop("video_url")]
        if "audio_urls" not in p and "audio_url" in p:
            p["audio_urls"] = [p.pop("audio_url")]
        p.pop("task_type", None)

    # First/last frame lanes require explicit frame fields
    if "first-last-frame-to-video" in fal_model:
        if "first_frame_url" not in p and "image_url" in p:
            p["first_frame_url"] = p.pop("image_url")
        if "last_frame_url" not in p and "end_image_url" in p:
            p["last_frame_url"] = p.pop("end_image_url")
        p.pop("task_type", None)

    # Video extension / lipsync lanes use explicit video/audio refs
    if "extend" in fal_model or "lipsync" in fal_model or "video-to-video" in fal_model:
        if "video" in p and "video_url" not in p:
            p["video_url"] = p.pop("video")
        if "audio" in p and "audio_url" not in p:
            p["audio_url"] = p.pop("audio")
        p.pop("task_type", None)

    # Trellis Multi: images array passthrough
    if "trellis/multi" in fal_model:
        if "images" in p and "image_url" not in p:
            pass  # keep images array as-is
        elif "image_url" in p and "images" not in p:
            p["images"] = [p.pop("image_url")]
        p.pop("task_type", None)

    return p


# ─────────────────────────────────────────────────────────────────────────────
# PIAPI — GPT-Image-1 (LLM completions endpoint)
# ─────────────────────────────────────────────────────────────────────────────

def generate_piapi_gpt_image(params: dict, api_key: str,
                              media_type: str, output_dir: Path) -> dict:
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    payload = {
        "model": "gpt-image-1",
        "prompt": params.get("prompt", ""),
        "n": 1,
        "size": params.get("size", "1024x1024"),
        "quality": params.get("quality", "standard"),
    }
    log("  Submitting to PiAPI: gpt-image-1")
    resp = requests.post("https://api.piapi.ai/v1/images/generations",
                         headers=headers, json=payload, timeout=120)
    if not resp.ok:
        raise RuntimeError(f"PiAPI GPT-Image-1 [{resp.status_code}]: {resp.text[:300]}")
    result = resp.json()
    data_list = result.get("data", [])
    if not data_list:
        raise RuntimeError(f"GPT-Image-1 no data: {str(result)[:300]}")
    item = data_list[0]
    image_url = item.get("url")
    b64 = item.get("b64_json")
    if image_url:
        data = download(image_url)
    elif b64:
        data = base64.b64decode(b64)
        image_url = "(base64)"
    else:
        raise RuntimeError(f"GPT-Image-1: no url/b64: {str(item)[:200]}")
    saved = make_output_path(output_dir, "image", "png")
    saved.write_bytes(data)
    log(f"  Saved: {saved}")
    return {"success": True, "provider": "piapi", "model": "gpt-image-1",
            "output_url": image_url, "saved_path": str(saved), "file_size_bytes": len(data)}


# ─────────────────────────────────────────────────────────────────────────────
# PIAPI — Main handler
# ─────────────────────────────────────────────────────────────────────────────

def generate_piapi(model_key: str, params: dict, api_key: str,
                   media_type: str, output_dir: Path,
                   task_type_override: str = "") -> dict:

    if model_key == "gpt-image-1":
        return generate_piapi_gpt_image(params, api_key, media_type, output_dir)

    headers = {"x-api-key": api_key, "Content-Type": "application/json"}

    # Resolve model config
    cfg = PIAPI_MODEL_MAP.get(model_key)
    if cfg:
        model_id = cfg["model"]
        task_type = task_type_override or cfg["task_type"]
    else:
        # model_key is the raw model ID, task_type_override required
        model_id = model_key
        task_type = task_type_override or "txt2img"

    # Build payload input — pass params through, handle special cases
    input_data = dict(params)

    # Framepack uses start_image instead of image_url
    if task_type == "img2video" and model_id == "Qubico/framepack":
        if "image_url" in input_data and "start_image" not in input_data:
            input_data["start_image"] = input_data.pop("image_url")

    # Skyreels uses image instead of image_url
    if task_type == "img2video" and model_id == "Qubico/skyreels":
        if "image_url" in input_data and "image" not in input_data:
            input_data["image"] = input_data.pop("image_url")

    # Trellis image-to-3d uses images array
    if task_type == "image-to-3d" and model_id in ("Qubico/trellis",):
        if "image_url" in input_data and "images" not in input_data:
            input_data["images"] = [input_data.pop("image_url")]

    # Trellis2 uses image (singular)
    if task_type == "image-to-3d" and model_id == "Qubico/trellis2":
        if "image_url" in input_data and "image" not in input_data:
            input_data["image"] = input_data.pop("image_url")

    # MMAudio uses video field
    if task_type == "video2audio":
        if "video_url" in input_data and "video" not in input_data:
            input_data["video"] = input_data.pop("video_url")

    # PiAPI video toolkit uses video input; image upscalers use image_url.
    if task_type == "upscale" and model_id == "Qubico/video-toolkit":
        if "video_url" in input_data and "video" not in input_data:
            input_data["video"] = input_data.pop("video_url")

    # OmniHuman uses image_url and audio_url directly
    # F5-TTS uses gen_text + ref_audio
    # Udio uses prompt as the music description

    payload = {"model": model_id, "task_type": task_type, "input": input_data}

    log(f"  Submitting to PiAPI: {model_id} / {task_type}")
    resp = requests.post("https://api.piapi.ai/api/v1/task",
                         headers=headers, json=payload, timeout=30)
    if not resp.ok:
        raise RuntimeError(f"PiAPI submit [{resp.status_code}]: {resp.text[:300]}")

    data = resp.json()
    if data.get("code") != 200:
        raise RuntimeError(f"PiAPI error: {data.get('message', resp.text[:200])}")

    task_id = data["data"]["task_id"]
    log(f"  Task ID: {task_id}")
    log("  Waiting", end="")

    output = {}
    for _ in range(MAX_POLLS):
        time.sleep(POLL_INTERVAL)
        s = requests.get(f"https://api.piapi.ai/api/v1/task/{task_id}",
                         headers=headers, timeout=15)
        if not s.ok:
            print("?", end="", flush=True)
            continue
        task_data = s.json().get("data", {})
        status = task_data.get("status", "")
        if status == "completed":
            print(" done!", flush=True)
            output = task_data.get("output", {})
            break
        elif status in ("failed", "error"):
            print(" FAILED", flush=True)
            raise RuntimeError(f"PiAPI task failed: {task_data.get('error', status)}")
        else:
            print(".", end="", flush=True)
    else:
        raise TimeoutError("PiAPI timed out after 10 minutes")

    output_url = _extract_piapi_url(output, task_type)
    if not output_url:
        # JoyCaption returns text
        if task_type == "joycaption-beta-one":
            caption = output.get("caption") or output.get("text") or str(output)
            saved = make_output_path(output_dir, "caption", "txt")
            saved.write_text(caption)
            log(f"  Caption: {caption[:100]}")
            return {"success": True, "provider": "piapi", "model": model_id,
                    "caption": caption, "saved_path": str(saved)}
        return {"success": True, "provider": "piapi", "model": model_id, "raw_result": output}

    log("  Downloading output...")
    ext = "mp4" if media_type == "video" and task_type == "upscale" else TASK_EXT_MAP.get(task_type, ext_for(media_type))
    data_bytes = download(output_url)
    saved = make_output_path(output_dir, media_type, ext)
    saved.write_bytes(data_bytes)
    log(f"  Saved: {saved}")

    return {"success": True, "provider": "piapi", "model": model_id,
            "output_url": output_url, "saved_path": str(saved),
            "file_size_bytes": len(data_bytes)}


def _extract_piapi_url(output: dict, task_type: str) -> str | None:
    for key in ("video_url", "audio_url", "image_url", "url", "video_urls",
                "image_urls", "image", "video", "audio", "model_url", "glb_url"):
        val = output.get(key)
        if not val:
            continue
        if isinstance(val, str) and val.startswith("http"):
            return val
        if isinstance(val, list) and val:
            item = val[0]
            if isinstance(item, str):
                return item
            if isinstance(item, dict):
                return item.get("url") or item.get("image_url")
    return None


# ─────────────────────────────────────────────────────────────────────────────
# FAL.AI
# ─────────────────────────────────────────────────────────────────────────────

def generate_fal(model: str, params: dict, api_key: str,
                 media_type: str, output_dir: Path) -> dict:
    # Resolve shorthand key → fal model ID
    fal_model = FAL_MODEL_MAP.get(model, model)

    # Nano Banana image refs must hit the edit endpoint, not text-to-image.
    if (params.get("image_url") or params.get("image_urls")) and fal_model in FAL_EDIT_MAP:
        fal_model = FAL_EDIT_MAP[fal_model]

    # Auto-switch to I2V endpoint when image_url is present
    if params.get("image_url") and fal_model in FAL_I2V_MAP:
        fal_model = FAL_I2V_MAP[fal_model]

    # Translate PiAPI-style params to fal.ai equivalents
    fal_params = _remap_fal_params(fal_model, params)

    if "gpt-image-2" in fal_model or "gpt-image-1.5" in fal_model:
        fal_params.setdefault("quality", "high")
        fal_params["openai_api_key"] = get_key(load_env(), "OPENAI_API_KEY", "OpenAI")

    headers = {"Authorization": f"Key {api_key}", "Content-Type": "application/json"}
    submit_url = f"https://queue.fal.run/{fal_model}"
    log(f"  Submitting to fal.ai: {fal_model}")
    resp = requests.post(submit_url, headers=headers, json=fal_params, timeout=30)
    if not resp.ok:
        raise RuntimeError(f"fal.ai submit [{resp.status_code}]: {resp.text[:300]}")
    request_id = resp.json().get("request_id")
    if not request_id:
        raise RuntimeError(f"fal.ai no request_id: {resp.text[:300]}")
    log(f"  Request ID: {request_id}")
    # Prefer URLs returned by fal.ai in the submit response (most reliable)
    submit_data = resp.json()
    status_url = submit_data.get("status_url") or f"https://queue.fal.run/{fal_model}/requests/{request_id}/status"
    result_url = submit_data.get("response_url") or f"https://queue.fal.run/{fal_model}/requests/{request_id}"
    log("  Waiting", end="")
    for _ in range(MAX_POLLS):
        time.sleep(POLL_INTERVAL)
        s = requests.get(status_url, headers=headers, timeout=15)
        if not s.ok:
            print("?", end="", flush=True)
            continue
        status = s.json().get("status", "")
        if status == "COMPLETED":
            print(" done!", flush=True)
            break
        elif status == "FAILED":
            print(" FAILED", flush=True)
            raise RuntimeError(f"fal.ai failed: {s.json().get('error', 'Unknown')}")
        else:
            print(".", end="", flush=True)
    else:
        raise TimeoutError("fal.ai timed out after 10 minutes")
    r = requests.get(result_url, headers=headers, timeout=30)
    if not r.ok:
        # Fallback: try manually constructed URL
        fallback_url = f"https://queue.fal.run/{fal_model}/requests/{request_id}"
        r = requests.get(fallback_url, headers=headers, timeout=30)
        r.raise_for_status()
    result = r.json()
    output_url = _extract_fal_url(result, media_type)
    if not output_url:
        return {"success": True, "provider": "fal", "model": fal_model, "raw_result": result}
    log("  Downloading output...")
    ext = FAL_EXT_MAP.get(fal_model) or ext_for(media_type)
    data = download(output_url)
    saved = make_output_path(output_dir, media_type, ext)
    saved.write_bytes(data)
    log(f"  Saved: {saved}")
    return {"success": True, "provider": "fal", "model": fal_model,
            "output_url": output_url, "saved_path": str(saved), "file_size_bytes": len(data)}


def _auto_mask_from_prompt(image_url: str, subject_prompt: str, api_key: str) -> str | None:
    """Call fal-ai/evf-sam to auto-generate a segmentation mask from a text prompt.

    Used by strict-inpaint lanes when the caller did not supply a mask_url but
    did supply an image_url and a natural-language subject. Returns a public
    mask URL on success, or None if the endpoint did not produce a usable mask.
    """
    if not image_url or not subject_prompt or not api_key:
        return None

    fal_model = FAL_MODEL_MAP.get("evf-sam", "fal-ai/evf-sam")
    headers = {"Authorization": f"Key {api_key}", "Content-Type": "application/json"}
    submit_url = f"https://queue.fal.run/{fal_model}"
    log(f"  Auto-mask: segmenting '{subject_prompt[:60]}' via {fal_model}...")
    resp = requests.post(
        submit_url,
        headers=headers,
        json={"image_url": image_url, "prompt": subject_prompt},
        timeout=30,
    )
    if not resp.ok:
        log(f"  Auto-mask submit failed [{resp.status_code}]: {resp.text[:200]}")
        return None
    data = resp.json()
    request_id = data.get("request_id")
    if not request_id:
        return None
    status_url = data.get("status_url") or f"https://queue.fal.run/{fal_model}/requests/{request_id}/status"
    result_url = data.get("response_url") or f"https://queue.fal.run/{fal_model}/requests/{request_id}"
    for _ in range(MAX_POLLS):
        time.sleep(POLL_INTERVAL)
        s = requests.get(status_url, headers=headers, timeout=15)
        if not s.ok:
            continue
        status = s.json().get("status", "")
        if status == "COMPLETED":
            break
        if status == "FAILED":
            log(f"  Auto-mask failed: {s.json().get('error', 'Unknown')}")
            return None
    else:
        log("  Auto-mask timed out.")
        return None
    r = requests.get(result_url, headers=headers, timeout=30)
    if not r.ok:
        return None
    result = r.json()
    mask_url = _extract_fal_url(result, "image")
    if mask_url:
        log(f"  Auto-mask ready: {mask_url[:80]}")
    return mask_url


def _extract_fal_url(result: dict, media_type: str) -> str | None:
    def extract_url(payload: object) -> str | None:
        if isinstance(payload, str) and payload.startswith("http"):
            return payload
        if isinstance(payload, list) and payload:
            first = payload[0]
            if isinstance(first, str) and first.startswith("http"):
                return first
            if isinstance(first, dict):
                return extract_url(first)
            return None
        if not isinstance(payload, dict):
            return None

        # fal queue results often nest the useful payload under `data`.
        for container in (payload, payload.get("data")):
            if not isinstance(container, dict):
                continue
            for key in ("images", "image", "video", "audio", "model_mesh", "audio_url"):
                url = extract_url(container.get(key))
                if url:
                    return url
            for key in ("url", "image_url", "video_url", "output"):
                url = extract_url(container.get(key))
                if url:
                    return url
        return None

    return extract_url(result)


# ─────────────────────────────────────────────────────────────────────────────
# TOGETHER.AI
# ─────────────────────────────────────────────────────────────────────────────

def generate_together(model: str, params: dict, api_key: str,
                      media_type: str, output_dir: Path) -> dict:
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    if media_type == "video":
        return _together_video(model, params, headers, media_type, output_dir)
    else:
        return _together_image(model, params, headers, media_type, output_dir)


def _together_video(model, params, headers, media_type, output_dir):
    log(f"  Submitting to Together.ai (video): {model}")
    resp = requests.post("https://api.together.xyz/v1/videos/generations",
                         headers=headers, json={"model": model, **params}, timeout=60)
    if not resp.ok:
        raise RuntimeError(f"Together video [{resp.status_code}]: {resp.text[:300]}")
    result = resp.json()
    job_id = result.get("id")
    if not job_id:
        output_url = _extract_together_url(result, media_type)
        if output_url:
            return _together_download(output_url, model, media_type, output_dir)
        raise RuntimeError(f"Together: no job_id or URL: {str(result)[:300]}")
    log(f"  Job ID: {job_id}")
    log("  Waiting", end="")
    for _ in range(MAX_POLLS):
        time.sleep(POLL_INTERVAL)
        s = requests.get(f"https://api.together.xyz/v1/videos/generations/{job_id}",
                         headers=headers, timeout=15)
        if not s.ok:
            print("?", end="", flush=True)
            continue
        job = s.json()
        status = job.get("status", "")
        if status == "completed":
            print(" done!", flush=True)
            output_url = _extract_together_url(job, media_type)
            if output_url:
                return _together_download(output_url, model, media_type, output_dir)
            return {"success": True, "provider": "together", "model": model, "raw_result": job}
        elif status in ("failed", "error", "cancelled"):
            print(f" {status.upper()}", flush=True)
            raise RuntimeError(f"Together {status}: {job.get('error', '')}")
        else:
            print(".", end="", flush=True)
    raise TimeoutError("Together.ai timed out after 10 minutes")


def _together_image(model, params, headers, media_type, output_dir):
    log(f"  Submitting to Together.ai (image): {model}")
    resp = requests.post("https://api.together.xyz/v1/images/generations",
                         headers=headers, json={"model": model, **params}, timeout=60)
    if not resp.ok:
        raise RuntimeError(f"Together image [{resp.status_code}]: {resp.text[:300]}")
    result = resp.json()
    output_url = _extract_together_url(result, media_type)
    if output_url:
        return _together_download(output_url, model, media_type, output_dir)
    return {"success": True, "provider": "together", "model": model, "raw_result": result}


def _extract_together_url(result, media_type):
    for key in ("url", "video_url", "image_url", "output_url"):
        if key in result and isinstance(result[key], str):
            return result[key]
    data = result.get("data", [])
    if data and isinstance(data, list):
        item = data[0]
        if isinstance(item, dict):
            return item.get("url")
    return None


def _together_download(output_url, model, media_type, output_dir):
    log("  Downloading output...")
    ext = ext_for(media_type)
    data = download(output_url)
    saved = make_output_path(output_dir, media_type, ext)
    saved.write_bytes(data)
    log(f"  Saved: {saved}")
    return {"success": True, "provider": "together", "model": model,
            "output_url": output_url, "saved_path": str(saved), "file_size_bytes": len(data)}


# ─────────────────────────────────────────────────────────────────────────────
# RUNWARE (images — synchronous)
# ─────────────────────────────────────────────────────────────────────────────

def generate_runware(model: str, params: dict, api_key: str,
                     media_type: str, output_dir: Path) -> dict:
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    log(f"  Submitting to Runware: {model}")
    task_uuid = str(uuid.uuid4())
    payload = [{
        "taskType": "imageInference",
        "taskUUID": task_uuid,
        "model": model,
        "positivePrompt": params.get("prompt", ""),
        "width": params.get("width", 1024),
        "height": params.get("height", 576),
        "numberResults": 1,
        "outputFormat": "PNG",
        "steps": params.get("steps", 4),
        "CFGScale": params.get("cfg_scale", 1),
    }]
    resp = requests.post("https://api.runware.ai/v1",
                         headers=headers, json=payload, timeout=60)
    if not resp.ok:
        raise RuntimeError(f"Runware [{resp.status_code}]: {resp.text[:300]}")
    result = resp.json()
    data_list = result.get("data", [])
    if not data_list:
        raise RuntimeError(f"Runware no data: {str(result)[:300]}")
    image_url = data_list[0].get("imageURL") or data_list[0].get("url")
    if not image_url:
        raise RuntimeError(f"Runware no URL: {str(data_list[0])[:200]}")
    log("  Downloading output...")
    data = download(image_url)
    saved = make_output_path(output_dir, "image", "png")
    saved.write_bytes(data)
    log(f"  Saved: {saved}")
    return {"success": True, "provider": "runware", "model": model,
            "output_url": image_url, "saved_path": str(saved), "file_size_bytes": len(data)}


# ─────────────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────────────

def main():
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Usage: generate.py '<json_config>'"}))
        sys.exit(1)

    try:
        cfg = json.loads(sys.argv[1])
    except json.JSONDecodeError as e:
        print(json.dumps({"error": f"Invalid JSON: {e}"}))
        sys.exit(1)

    provider    = cfg.get("provider", "").lower()
    model       = cfg.get("model", "")
    task_type   = cfg.get("task_type", "")
    params      = cfg.get("params", {})
    media_type  = cfg.get("media_type", "image")
    routing     = cfg.get("routing", {}) or {}
    est_cost    = cfg.get("estimated_cost", "unknown")
    output_dir  = Path(cfg.get("output_dir", str(DEFAULT_OUTPUT_DIR)))

    prompt = params.get("prompt") or params.get("gen_text") or params.get("style_prompt") or ""
    raw_prompt = prompt

    if routing or not provider or not model:
        try:
            selection = resolve_route_selection(
                media_type,
                prompt=prompt,
                params=params,
                route_id=(routing.get("route_id", "") or cfg.get("route_id", "")),
                requested=routing,
            )
        except ValueError as e:
            print(json.dumps({"error": str(e), "media_type": media_type}))
            sys.exit(1)

        provider = provider or selection["provider"]
        model = model or selection["model_key"]
        task_type = task_type or selection["task_type"]
    else:
        selection = None

    if selection:
        try:
            validate_route_constraints(
                media_type,
                selection["route"],
                prompt=prompt,
                params=params,
                requested=routing,
            )
        except ValueError as e:
            print(json.dumps({"error": str(e), "media_type": media_type, "route_id": selection["route_id"]}))
            sys.exit(1)

    compiler_result = compile_prompt(
        prompt,
        media_type=media_type,
        model_key=model,
        route_id=selection["route_id"] if selection else "",
        params=params,
        routing=routing,
    )
    compiler_trace = compiler_result.get("compiler_trace", {})
    compiled_prompt = compiler_result.get("prompt", prompt)
    if compiled_prompt and params.get("prompt"):
        params["prompt"] = compiled_prompt
    elif compiled_prompt and params.get("gen_text"):
        params["gen_text"] = compiled_prompt
    elif compiled_prompt and params.get("style_prompt"):
        params["style_prompt"] = compiled_prompt
    elif compiled_prompt:
        params["prompt"] = compiled_prompt
    prompt = compiled_prompt or prompt

    if not provider:
        print(json.dumps({"error": "'provider' required"}))
        sys.exit(1)
    if not model:
        print(json.dumps({"error": "'model' required"}))
        sys.exit(1)

    env = load_env()

    log(f"\nAI GEN MAX")
    log(f"  Provider:  {provider}")
    log(f"  Model:     {model}")
    if selection:
        log(f"  Route:     {selection['route_id']}")
    if task_type:
        log(f"  Task:      {task_type}")
    log(f"  Prompt:    {prompt[:80]}{'...' if len(prompt) > 80 else ''}")
    if compiler_trace.get("applied"):
        log(f"  Compiler:  {compiler_trace.get('strategy', 'applied')}")
    log(f"  Type:      {media_type}")
    log(f"  Est. cost: {est_cost}")
    if params.get("image_url"):
        log(f"  Image:     {str(params['image_url'])[:60]}")
    if params.get("image_urls"):
        log(f"  Images:    {len(params['image_urls'])} reference image(s)")
    log("")

    # Resolve local image to public URL
    fal_key = env.get("FAL_API_KEY", "")

    # Preserve the original local source path (before upload) so the
    # preservation contract can compare output canvas vs source canvas.
    source_local_image = None
    raw_image_ref = params.get("image_url")
    if isinstance(raw_image_ref, str) and not raw_image_ref.startswith("http"):
        source_local_image = raw_image_ref

    single_ref_keys = (
        "image_url",
        "video_url",
        "audio_url",
        "first_frame_url",
        "last_frame_url",
        "end_image_url",
        "mask_url",
    )
    list_ref_keys = (
        "image_urls",
        "reference_image_urls",
        "video_urls",
        "audio_urls",
        "images",
        "videos",
    )
    try:
        for key in single_ref_keys:
            if params.get(key) and not str(params[key]).startswith("http"):
                params[key] = resolve_media_ref(str(params[key]), fal_key)
        for key in list_ref_keys:
            if params.get(key):
                params[key] = [
                    item if str(item).startswith("http")
                    else resolve_media_ref(str(item), fal_key)
                    for item in params[key]
                ]
    except (FileNotFoundError, RuntimeError, ValueError) as e:
        print(json.dumps({"error": f"Media resolution failed: {e}"}))
        sys.exit(1)

    # Auto-mask pipeline: if the route is strict-inpaint and the caller
    # supplied an image + subject prompt but no mask_url, try to segment
    # the subject automatically via evf-sam. This turns "borra las cards"
    # style prompts into a real mask-based inpaint without extra steps.
    auto_mask_trace = None
    if (
        selection
        and selection["route"].get("route_id") == "image-strict-inpaint"
        and params.get("image_url")
        and prompt
        and not params.get("mask_url")
    ):
        try:
            mask_url = _auto_mask_from_prompt(
                params["image_url"],
                prompt,
                fal_key or get_key(env, "FAL_API_KEY", "fal.ai"),
            )
            if mask_url:
                params["mask_url"] = mask_url
                auto_mask_trace = {"status": "generated", "source": "evf-sam"}
            else:
                auto_mask_trace = {"status": "skipped", "reason": "no_mask_returned"}
        except Exception as e:  # pragma: no cover - defensive
            auto_mask_trace = {"status": "error", "reason": str(e)[:200]}

    def _dispatch(prov: str, mdl: str, tsk: str) -> dict:
        if prov == "piapi":
            api_key = get_key(env, "PIAPI_API_KEY", "PiAPI")
            return generate_piapi(mdl, params, api_key, media_type, output_dir, tsk)
        if prov == "fal":
            api_key = get_key(env, "FAL_API_KEY", "fal.ai")
            return generate_fal(mdl, params, api_key, media_type, output_dir)
        if prov == "together":
            api_key = get_key(env, "TOGETHER_API_KEY", "Together.ai")
            return generate_together(mdl, params, api_key, media_type, output_dir)
        if prov == "runware":
            api_key = get_key(env, "RUNWARE_API_KEY", "Runware")
            return generate_runware(mdl, params, api_key, media_type, output_dir)
        raise ValueError(f"Unknown provider '{prov}'. Supported: piapi, fal, together, runware")

    fallback_trace = []
    try:
        try:
            result = _dispatch(provider, model, task_type)
        except (RuntimeError, TimeoutError) as primary_err:
            # Degradation path: when the primary model fails (e.g. unverified
            # endpoint returns 4xx, or specialist model rejects params), try
            # the route's documented fallback_model_keys in order. This prevents
            # silent NO_REPLY when a specialist lane cannot serve the request.
            fallbacks = []
            if selection:
                for fb_key in selection["route"].get("fallback_model_keys", []) or []:
                    if fb_key == model:
                        continue
                    fb_provider = "fal" if fb_key in FAL_MODEL_MAP else (
                        "piapi" if fb_key in PIAPI_MODEL_MAP else None
                    )
                    if fb_provider:
                        fallbacks.append((fb_provider, fb_key))
            if not fallbacks:
                raise
            primary_failure = f"{type(primary_err).__name__}: {str(primary_err)[:200]}"
            fallback_trace.append({"model": model, "provider": provider, "status": "failed",
                                   "error": primary_failure})
            result = None
            last_err = primary_err
            for fb_provider, fb_key in fallbacks:
                log(f"  Primary failed, trying fallback: {fb_provider}:{fb_key}")
                try:
                    result = _dispatch(fb_provider, fb_key, "")
                    fallback_trace.append({"model": fb_key, "provider": fb_provider, "status": "success"})
                    provider = fb_provider
                    model = fb_key
                    break
                except (RuntimeError, TimeoutError) as fb_err:
                    fallback_trace.append({"model": fb_key, "provider": fb_provider,
                                           "status": "failed", "error": str(fb_err)[:200]})
                    last_err = fb_err
                    continue
            if result is None:
                raise last_err

        # Strict preservation routes must NOT be upscaled post-hoc: an upscale
        # changes the canvas, which violates the same preservation contract we
        # are about to enforce. Skip the HD-guard for strict lanes.
        strict_preservation_route = bool(
            selection and selection["route"].get("preservation_mode") == "strict"
        )
        if media_type == "image" and not strict_preservation_route:
            result = ensure_min_hd_image(result, fal_key or get_key(env, "FAL_API_KEY", "fal.ai"), output_dir)

        # Strict preservation contract: if the route promised strict preservation,
        # verify output canvas matches source canvas. Fails fast on reframe.
        if strict_preservation_route:
            result = ensure_preservation_contract(result, source_local_image)

        result["estimated_cost"] = est_cost
        if selection:
            result["route_id"] = selection["route_id"]
            result["resolved_model_key"] = selection["model_key"]
            result["_trace"] = {
                "route_id": selection["route_id"],
                "route_operation": selection["route"].get("operation"),
                "route_goal": selection["route"].get("goal"),
                "route_input_shape": selection["route"].get("input_shape"),
                "route_preservation_mode": selection["route"].get("preservation_mode", "flexible"),
                "resolved_provider": selection["provider"],
                "resolved_model_key": selection["model_key"],
                "raw_prompt": raw_prompt,
                "compiled_prompt": prompt,
                "routing_signals_received": routing or {},
                "params_keys": sorted(params.keys()),
                "auto_mask": auto_mask_trace,
                "prompt_compiler": compiler_trace,
                "fallback_chain": fallback_trace or None,
            }
        print(json.dumps(result, indent=2))

    except (ValueError, RuntimeError, TimeoutError) as e:
        print(json.dumps({"error": str(e), "provider": provider, "model": model}))
        sys.exit(1)
    except requests.exceptions.ConnectionError as e:
        print(json.dumps({"error": f"Network error: {e}", "provider": provider}))
        sys.exit(1)
    except requests.exceptions.Timeout:
        print(json.dumps({"error": "Request timed out", "provider": provider}))
        sys.exit(1)
    except KeyboardInterrupt:
        print(json.dumps({"error": "Cancelled by user"}))
        sys.exit(1)


if __name__ == "__main__":
    main()
