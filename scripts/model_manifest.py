"""Single source of truth for ai-gen-max model routing and docs."""

from __future__ import annotations


DOC_VALIDATED_AT = "2026-04-21"

ROUTE_ID_ALIASES = {
    "image-premium-lookdev-edit": "image-strong-lookdev-edit",
}

DEFAULT_IMAGE_MODEL_KEY = "gpt-image-2"
DEFAULT_IMAGE_MODEL_ID = "fal-ai/gpt-image-2"
DEFAULT_IMAGE_LABEL = "GPT Image 2 / ChatGPT Images 2.0"


PIAPI_MODEL_MAP = {
    "flux-dev-advanced": {"model": "Qubico/flux1-dev-advanced", "task_type": "txt2img"},
    "flux-dev": {"model": "Qubico/flux1-dev", "task_type": "txt2img"},
    "flux-schnell": {"model": "Qubico/flux1-schnell", "task_type": "txt2img"},
    "flux-inpaint": {"model": "Qubico/flux1-dev-advanced", "task_type": "fill-inpaint"},
    "flux-outpaint": {"model": "Qubico/flux1-dev-advanced", "task_type": "fill-outpaint"},
    "flux-variation": {"model": "Qubico/flux1-dev-advanced", "task_type": "redux-variation"},
    "qwen-image": {"model": "qwen-image", "task_type": "txt2img"},
    "z-image": {"model": "Qubico/z-image", "task_type": "txt2img"},
    "gemini-flash-image": {"model": "gemini", "task_type": "gemini-2.5-flash-image"},
    "nano-banana-pro": {"model": "gemini", "task_type": "nano-banana-pro"},
    "gpt-image-1": {"model": "gpt-image-1", "task_type": "llm-image"},
    "kling": {"model": "kling", "task_type": "video_generation"},
    "kling-omni": {"model": "kling", "task_type": "omni_video_generation"},
    "kling-turbo": {"model": "kling-turbo", "task_type": "video_generation"},
    "kling-avatar": {"model": "kling", "task_type": "avatar"},
    "kling-effects": {"model": "kling", "task_type": "effects"},
    "kling-sound": {"model": "kling", "task_type": "sound"},
    "kling-lipsync": {"model": "kling", "task_type": "lip_sync"},
    "kling-extend": {"model": "kling", "task_type": "extend_video"},
    "kling-motion": {"model": "kling", "task_type": "motion_control"},
    "sora2": {"model": "sora2", "task_type": "sora2-video"},
    "sora2-pro": {"model": "sora2", "task_type": "sora2-pro-video"},
    "veo3": {"model": "veo3.1", "task_type": "veo3.1-video-fast"},
    "veo3-hq": {"model": "veo3.1", "task_type": "veo3.1-video"},
    "seedance2": {"model": "seedance", "task_type": "seedance-2"},
    "seedance2-fast": {"model": "seedance", "task_type": "seedance-2-fast"},
    "seedance2-preview": {"model": "seedance", "task_type": "seedance-2-preview"},
    "seedance2-preview-vip": {"model": "seedance", "task_type": "seedance-2-preview-vip"},
    "wan26": {"model": "Wan", "task_type": "wan26-txt2video"},
    "wan26-i2v": {"model": "Wan", "task_type": "wan26-img2video"},
    "wanx-14b": {"model": "Qubico/wanx", "task_type": "txt2video-14b"},
    "wanx-1.3b": {"model": "Qubico/wanx", "task_type": "txt2video-1.3b"},
    "wanx-i2v": {"model": "Qubico/wanx", "task_type": "img2video-14b"},
    "wanx-i2v-keyframe": {"model": "Qubico/wanx", "task_type": "img2video-14b-keyframe"},
    "wanx-i2v-camera": {"model": "Qubico/wanx", "task_type": "img2video-14b-control-camera"},
    "wanx-lora": {"model": "Qubico/wanx", "task_type": "txt2video-14b-lora"},
    "hailuo": {"model": "hailuo", "task_type": "video_generation"},
    "hunyuan": {"model": "Qubico/hunyuan", "task_type": "txt2video"},
    "hunyuan-fast": {"model": "Qubico/hunyuan", "task_type": "fast-txt2video"},
    "hunyuan-i2v": {"model": "Qubico/hunyuan", "task_type": "img2video-concat"},
    "luma": {"model": "luma", "task_type": "video_generation"},
    "framepack": {"model": "Qubico/framepack", "task_type": "img2video"},
    "skyreels": {"model": "Qubico/skyreels", "task_type": "img2video"},
    "omnihuman": {"model": "omni-human", "task_type": "omni-human-1.5"},
    "mmaudio": {"model": "Qubico/mmaudio", "task_type": "video2audio"},
    "video-upscale": {"model": "Qubico/video-toolkit", "task_type": "upscale"},
    "diffrhythm-full": {"model": "Qubico/diffrhythm", "task_type": "txt2audio-full"},
    "diffrhythm-base": {"model": "Qubico/diffrhythm", "task_type": "txt2audio-base"},
    "ace-step": {"model": "Qubico/ace-step", "task_type": "txt2audio"},
    "ace-step-a2a": {"model": "Qubico/ace-step", "task_type": "audio2audio"},
    "udio": {"model": "music-u", "task_type": "generate_music"},
    "f5-tts": {"model": "Qubico/tts", "task_type": "zero-shot"},
    "trellis-text": {"model": "Qubico/trellis", "task_type": "text-to-3d"},
    "trellis-image": {"model": "Qubico/trellis", "task_type": "image-to-3d"},
    "trellis2": {"model": "Qubico/trellis2", "task_type": "image-to-3d"},
    "remove-bg": {"model": "Qubico/image-toolkit", "task_type": "background-remove"},
    "image-upscale": {"model": "Qubico/image-toolkit", "task_type": "upscale"},
    "joycaption": {"model": "Qubico/joycaption", "task_type": "joycaption-beta-one"},
}


TASK_EXT_MAP = {
    "video_generation": "mp4",
    "omni_video_generation": "mp4",
    "img2video": "mp4",
    "video2audio": "mp4",
    "wan26-txt2video": "mp4",
    "wan26-img2video": "mp4",
    "sora2-video": "mp4",
    "sora2-pro-video": "mp4",
    "veo3.1-video": "mp4",
    "veo3.1-video-fast": "mp4",
    "seedance-2": "mp4",
    "seedance-2-fast": "mp4",
    "seedance-2-preview": "mp4",
    "seedance-2-preview-vip": "mp4",
    "txt2video": "mp4",
    "fast-txt2video": "mp4",
    "img2video-concat": "mp4",
    "img2video-14b": "mp4",
    "img2video-14b-keyframe": "mp4",
    "img2video-14b-control-camera": "mp4",
    "txt2video-14b": "mp4",
    "txt2video-1.3b": "mp4",
    "txt2audio-full": "mp3",
    "txt2audio-base": "mp3",
    "txt2audio": "mp3",
    "audio2audio": "mp3",
    "generate_music": "mp3",
    "zero-shot": "wav",
    "sound": "mp3",
    "text-to-3d": "glb",
    "image-to-3d": "glb",
    "txt2img": "png",
    "gemini-2.5-flash-image": "png",
    "nano-banana-pro": "png",
    "fill-inpaint": "png",
    "fill-outpaint": "png",
    "redux-variation": "png",
    "background-remove": "png",
    "upscale": "png",
    "joycaption-beta-one": "txt",
    "avatar": "mp4",
    "effects": "mp4",
    "lip_sync": "mp4",
    "extend_video": "mp4",
    "motion_control": "mp4",
}


FAL_MODEL_MAP = {
    "flux-dev": "fal-ai/flux/dev",
    "flux-dev-advanced": "fal-ai/flux/dev",
    "flux-schnell": "fal-ai/flux/schnell",
    "flux-2-max": "fal-ai/flux-2-max",
    "flux-2-max-edit": "fal-ai/flux-2-max/edit",
    "flux-2-pro": "fal-ai/flux-2-pro",
    "flux-pro": "fal-ai/flux-pro/v1",
    "flux-kontext-pro": "fal-ai/flux-pro/kontext",
    "flux-kontext-dev": "fal-ai/flux-kontext/dev",
    "gpt-image-2": "fal-ai/gpt-image-2",
    "gpt-image-1.5": "fal-ai/gpt-image-1.5",
    "nano-banana-2": "fal-ai/nano-banana-2",
    "nano-banana-pro": "fal-ai/nano-banana-pro",
    "nano-banana": "fal-ai/nano-banana",
    "nano-banana-preview": "fal-ai/gemini-3-pro-image-preview",
    "recraft-v3": "fal-ai/recraft/v3/text-to-image",
    "recraft-v4": "fal-ai/recraft/v4/text-to-image",
    "recraft-v4-pro": "fal-ai/recraft/v4/pro/text-to-image",
    "recraft-v4-vector": "fal-ai/recraft/v4/text-to-vector",
    "ideogram-v2": "fal-ai/ideogram/v2/text-to-image",
    "ideogram-v3": "fal-ai/ideogram/v3",
    "seedream-v4": "fal-ai/bytedance/seedream/v4/text-to-image",
    "seedream": "fal-ai/bytedance/seedream/v4.5/text-to-image",
    "seedream-v4-edit": "fal-ai/bytedance/seedream/v4/edit",
    "seedream-edit": "fal-ai/bytedance/seedream/v4.5/edit",
    "grok-imagine": "xai/grok-imagine-image",
    "grok-imagine-edit": "xai/grok-imagine-image/edit",
    "remove-bg": "fal-ai/birefnet",
    "image-upscale": "fal-ai/clarity-upscaler",
    "bria-eraser": "fal-ai/bria/eraser",
    "flux-inpaint": "fal-ai/flux-general/inpainting",
    "flux-fill-pro": "fal-ai/flux-pro/v1/fill",
    "iclight-v2": "fal-ai/iclight-v2",
    "evf-sam": "fal-ai/evf-sam",
    "kling": "fal-ai/kling-video/v3/standard/text-to-video",
    "kling-omni": "fal-ai/kling-video/v3/standard/text-to-video",
    "kling-pro": "fal-ai/kling-video/v3/pro/text-to-video",
    "seedance2": "bytedance/seedance-2.0/text-to-video",
    "seedance2-fast": "bytedance/seedance-2.0/fast/text-to-video",
    "seedance2-reference": "bytedance/seedance-2.0/reference-to-video",
    "sora2": "fal-ai/sora-2/text-to-video",
    "sora2-pro": "fal-ai/sora-2/text-to-video/pro",
    "sora2-remix": "fal-ai/sora-2/video-to-video/remix",
    "veo3": "fal-ai/veo3.1/fast",
    "veo3-hq": "fal-ai/veo3.1",
    "veo3-lite": "fal-ai/veo3.1/lite",
    "veo3-i2v": "fal-ai/veo3.1/image-to-video",
    "veo3-ref": "fal-ai/veo3.1/reference-to-video",
    "veo3-first-last": "fal-ai/veo3.1/first-last-frame-to-video",
    "veo3-extend": "fal-ai/veo3.1/extend-video",
    "veo3-lite-i2v": "fal-ai/veo3.1/lite/image-to-video",
    "veo3-lite-first-last": "fal-ai/veo3.1/lite/first-last-frame-to-video",
    "hunyuan-fast": "fal-ai/hunyuan-video",
    "wan26": "fal-ai/wan/v2.2/text-to-video",
    "wan27": "fal-ai/wan/v2.7/text-to-video",
    "wan27-edit": "fal-ai/wan/v2.7/edit",
    "luma-ray2": "fal-ai/luma-dream-machine/ray-2",
    "luma-ray2-flash": "fal-ai/luma-dream-machine/ray-2-flash",
    "pixverse": "fal-ai/pixverse/v5.6/text-to-video",
    "pixverse-v6-i2v": "fal-ai/pixverse/v6/image-to-video",
    "pixverse-transition": "fal-ai/pixverse/v6/transition",
    "pixverse-extend": "fal-ai/pixverse/extend",
    "hailuo-02-pro": "fal-ai/minimax/hailuo-02/pro/text-to-video",
    "cogvideox": "fal-ai/cogvideox-5b",
    "framepack": "fal-ai/framepack",
    "omnihuman": "bytedance/omnihuman/v1.5",
    "hailuo-23-pro": "fal-ai/minimax/hailuo-2.3/pro/image-to-video",
    "pixverse-i2v": "fal-ai/pixverse/v5.6/image-to-video",
    "grok-video": "xai/grok-imagine-video/text-to-video",
    "grok-video-i2v": "xai/grok-imagine-video/image-to-video",
    "grok-video-ref": "xai/grok-imagine-video/reference-to-video",
    "sync-lipsync": "fal-ai/sync-lipsync/v3",
    "diffrhythm-full": "fal-ai/diffrhythm",
    "diffrhythm-base": "fal-ai/diffrhythm",
    "ace-step": "fal-ai/ace-step",
    "ace-step-a2a": "fal-ai/ace-step",
    "minimax-music": "fal-ai/minimax-music",
    "cassetteai": "cassetteai/music-generator",
    "beatoven": "beatoven/music-generation",
    "f5-tts": "fal-ai/f5-tts",
    "mmaudio": "fal-ai/mmaudio-v2",
    "trellis-image": "fal-ai/trellis",
    "trellis-text": "fal-ai/trellis",
    "trellis2": "fal-ai/trellis-2",
    "trellis-multi": "fal-ai/trellis/multi",
}


FAL_EDIT_MAP = {
    "fal-ai/gpt-image-2": "fal-ai/gpt-image-2/edit",
    "fal-ai/gpt-image-1.5": "fal-ai/gpt-image-1.5/edit",
    "fal-ai/flux-2-max": "fal-ai/flux-2-max/edit",
    "fal-ai/flux-2-pro": "fal-ai/flux-2-pro/edit",
    "fal-ai/nano-banana-2": "fal-ai/nano-banana-2/edit",
    "fal-ai/nano-banana-pro": "fal-ai/nano-banana-pro/edit",
    "fal-ai/bytedance/seedream/v4/text-to-image": "fal-ai/bytedance/seedream/v4/edit",
    "fal-ai/bytedance/seedream/v4.5/text-to-image": "fal-ai/bytedance/seedream/v4.5/edit",
    "xai/grok-imagine-image": "xai/grok-imagine-image/edit",
}


FAL_I2V_MAP = {
    "fal-ai/kling-video/v3/standard/text-to-video": "fal-ai/kling-video/v3/standard/image-to-video",
    "fal-ai/kling-video/v3/pro/text-to-video": "fal-ai/kling-video/v3/pro/image-to-video",
    "bytedance/seedance-2.0/text-to-video": "bytedance/seedance-2.0/image-to-video",
    "bytedance/seedance-2.0/fast/text-to-video": "bytedance/seedance-2.0/fast/image-to-video",
    "fal-ai/sora-2/text-to-video": "fal-ai/sora-2/image-to-video",
    "fal-ai/sora-2/text-to-video/pro": "fal-ai/sora-2/image-to-video/pro",
    "fal-ai/veo3.1/fast": "fal-ai/veo3.1/fast/image-to-video",
    "fal-ai/veo3.1": "fal-ai/veo3.1/image-to-video",
    "fal-ai/veo3.1/lite": "fal-ai/veo3.1/lite/image-to-video",
    "fal-ai/luma-dream-machine/ray-2": "fal-ai/luma-dream-machine/ray-2/image-to-video",
    "fal-ai/luma-dream-machine/ray-2-flash": "fal-ai/luma-dream-machine/ray-2/image-to-video",
    "fal-ai/pixverse/v5.6/text-to-video": "fal-ai/pixverse/v5.6/image-to-video",
    "fal-ai/wan/v2.7/text-to-video": "fal-ai/wan/v2.7/image-to-video",
    "fal-ai/minimax/hailuo-02/pro/text-to-video": "fal-ai/minimax/hailuo-02/pro/image-to-video",
    "xai/grok-imagine-video/text-to-video": "xai/grok-imagine-video/image-to-video",
}


FAL_EXT_MAP = {
    "fal-ai/diffrhythm": "mp3",
    "fal-ai/ace-step": "mp3",
    "fal-ai/minimax-music": "mp3",
    "cassetteai/music-generator": "mp3",
    "beatoven/music-generation": "mp3",
    "fal-ai/mmaudio-v2": "mp4",
    "bytedance/omnihuman/v1.5": "mp4",
    "fal-ai/trellis": "glb",
    "fal-ai/trellis-2": "glb",
    "fal-ai/trellis/multi": "glb",
    "fal-ai/birefnet": "png",
    "fal-ai/clarity-upscaler": "png",
    "fal-ai/bria/eraser": "png",
    "fal-ai/flux-general/inpainting": "png",
    "fal-ai/flux-pro/v1/fill": "png",
    "fal-ai/iclight-v2": "png",
    "fal-ai/evf-sam": "png",
    "fal-ai/recraft/v3/text-to-image": "png",
    "fal-ai/recraft/v4/text-to-image": "png",
    "fal-ai/recraft/v4/pro/text-to-image": "png",
    "fal-ai/recraft/v4/text-to-vector": "svg",
    "fal-ai/ideogram/v3": "png",
    "fal-ai/flux-2-max": "jpeg",
    "fal-ai/flux-2-max/edit": "jpeg",
    "fal-ai/flux-2-pro": "jpeg",
    "fal-ai/gpt-image-2": "png",
    "fal-ai/gpt-image-2/edit": "png",
    "fal-ai/gpt-image-1.5": "png",
    "fal-ai/gpt-image-1.5/edit": "png",
    "fal-ai/bytedance/seedream/v4/text-to-image": "png",
    "fal-ai/bytedance/seedream/v4/edit": "png",
    "xai/grok-imagine-image": "jpeg",
    "xai/grok-imagine-image/edit": "jpeg",
}


SKILL_DOC_SECTIONS = {
    "image": [
        ("budget", "flux-schnell", "$0.003/MP"),
        ("standard", "flux-dev", "$0.025/MP"),
        ("DEFAULT / quality-first benchmark leader", "gpt-image-2", "$0.01-$0.41/img"),
        ("workhorse / fast iteration", "nano-banana-2", "$0.08/img"),
        ("premium fallback / Nano Banana look", "nano-banana-pro", "$0.15/img"),
        ("legacy prompt-adherence lane", "gpt-image-1.5", "from $0.009/img + tokens"),
        ("zero-config production consistency", "flux-2-pro", "$0.030/MP"),
        ("maximum-quality FLUX.2 generation", "flux-2-max", "$0.070/MP"),
        ("4K-ready Seedream generation", "seedream-v4", "$0.03/img"),
        ("vector / branding / SVG (producción-ready)", "recraft-v4-vector", "$0.08/img"),
        ("tipografía / posters / texto en imagen", "ideogram-v3", "$0.04/img"),
        ("edición con referencia", "flux-kontext-pro", "$0.04/img"),
        ("premium lookdev edit / luxury polish pass", "gpt-image-2", "$0.01-$0.41/img"),
    ],
    "video_t2v": [
        ("budget", "hunyuan-fast", "$0.03/gen"),
        ("DEFAULT", "kling", "$0.084/s"),
        ("cinematic", "seedance2", "$0.30/s"),
        ("premium", "sora2", "$0.10/s"),
        ("premium+audio / long-form", "sora2-pro", "$0.30/s 720p | $0.50/s 1080p"),
        ("ultra", "veo3", "$0.10/s 720p/1080p | $0.30/s 4k"),
        ("ultra+audio", "veo3-hq", "see fal 3.1 pricing"),
    ],
}


CATALOG_IMAGE_ROWS = [
    ("GPT Image 2 / ChatGPT Images 2.0", "gpt-image-2", "fal-ai/gpt-image-2", "$0.01-$0.41/img", "DEFAULT quality-first image lane — stronger photorealism, text rendering, UI/layout, product shots, and prompt adherence than GPT Image 1.5 / Nano Banana family"),
    ("Nano Banana 2", "nano-banana-2", "fal-ai/nano-banana-2", "$0.08/img", "Workhorse — fast iteration, social/marketing, batch generation, and cost-sensitive creative exploration"),
    ("Nano Banana Pro", "nano-banana-pro", "fal-ai/nano-banana-pro", "$0.15/img", "Premium fallback for the Nano Banana look; useful when GPT Image 2 is unavailable or the brief prefers Gemini/Nano Banana behavior"),
    ("GPT Image 1.5", "gpt-image-1.5", "fal-ai/gpt-image-1.5", "$0.133/img @ 1024 high + tokens", "Benchmark-leading prompt adherence and text rendering; supports low/medium/high quality tiers"),
    ("FLUX.2 Pro", "flux-2-pro", "fal-ai/flux-2-pro", "$0.030/MP", "Zero-config professional text-to-image generation with strong consistency"),
    ("FLUX.2 Max", "flux-2-max", "fal-ai/flux-2-max", "$0.070/MP", "Highest-quality FLUX.2 text-to-image generation"),
    ("Seedream 4.0", "seedream-v4", "fal-ai/bytedance/seedream/v4/text-to-image", "$0.03/img", "Seedream 4.0 generation, 4K-ready sizing, unified generation/edit architecture"),
    ("Recraft V4 Vector", "recraft-v4-vector", "fal-ai/recraft/v4/text-to-vector", "$0.08/img", "DEFAULT vector/SVG — production-ready scalable graphics (logos, icons, brand marks)"),
    ("Recraft V4", "recraft-v4", "fal-ai/recraft/v4/text-to-image", "$0.04/img", "Raster design — V4 improves design taste, composition, color cohesion vs V3"),
    ("Recraft V4 Pro", "recraft-v4-pro", "fal-ai/recraft/v4/pro/text-to-image", "$0.25/img", "Pro raster — 2048x2048, finer detail for print/large-scale"),
    ("Recraft V3", "recraft-v3", "fal-ai/recraft/v3/text-to-image", "$0.04/img", "Legacy raster fallback"),
    ("Ideogram V3", "ideogram-v3", "fal-ai/ideogram/v3", "$0.04/img", "DEFAULT typography — same 90-95% text accuracy as V2 + style reference + better spatial composition"),
    ("Ideogram V2", "ideogram-v2", "fal-ai/ideogram/v2/text-to-image", "$0.04/img", "Legacy typography fallback"),
    ("FLUX.2 Max Edit", "flux-2-max-edit", "fal-ai/flux-2-max/edit", "$0.07/MP first + $0.03/MP additional", "Fallback single-image edit lane for solid polish and better realism on existing compositions"),
    ("Seedream V4.5 Edit", "seedream-edit", "fal-ai/bytedance/seedream/v4.5/edit", "see fal", "Flexible restyle/reference edit; avoid for blur-sensitive premium polish of an existing composition"),
    ("Grok Imagine Image", "grok-imagine", "xai/grok-imagine-image", "see fal", "Aesthetic image generation"),
    ("Grok Imagine Image Edit", "grok-imagine-edit", "xai/grok-imagine-image/edit", "see fal", "Multi-image aesthetic edit"),
    ("Flux Dev Advanced", "flux-dev-advanced", "fal-ai/flux/dev", "$0.025/MP", "Standard / technical illustration"),
    ("Flux Schnell", "flux-schnell", "fal-ai/flux/schnell", "$0.003/MP", "Budget"),
]


CATALOG_VIDEO_ROWS = [
    ("Kling 3.0", "kling", "fal-ai/kling-video/v3/standard/text-to-video", "$0.084/s", "DEFAULT"),
    ("Seedance 2.0", "seedance2", "bytedance/seedance-2.0/text-to-video", "$0.30/s", "Cinematic / product"),
    ("Seedance 2.0 Reference", "seedance2-reference", "bytedance/seedance-2.0/reference-to-video", "$0.3024/s + token cost", "Multi-reference direction"),
    ("Sora 2", "sora2", "fal-ai/sora-2/text-to-video", "$0.10/s", "Physics realism"),
    ("Sora 2 Pro", "sora2-pro", "fal-ai/sora-2/text-to-video/pro", "$0.30/s 720p | $0.50/s 1080p", "Extended duration + native audio"),
    ("Sora 2 Remix", "sora2-remix", "fal-ai/sora-2/video-to-video/remix", "see fal", "Video-to-video creative remix"),
    ("Veo 3.1 Fast", "veo3", "fal-ai/veo3.1/fast", "$0.10/s 720p/1080p | $0.30/s 4k", "Ultra / fast"),
    ("Veo 3.1 Extend", "veo3-extend", "fal-ai/veo3.1/extend-video", "see fal", "Continue generated video; not a true video enhancer"),
    ("PixVerse V6 I2V", "pixverse-v6-i2v", "fal-ai/pixverse/v6/image-to-video", "$0.025-$0.115/s", "Stylized motion / social"),
    ("PixVerse Transition", "pixverse-transition", "fal-ai/pixverse/v6/transition", "$0.025-$0.115/s", "Image transition clip"),
    ("PixVerse Extend", "pixverse-extend", "fal-ai/pixverse/extend", "see fal", "Video extension"),
    ("Grok Imagine Video", "grok-video", "xai/grok-imagine-video/text-to-video", "see fal", "Stylized T2V"),
    ("Grok Imagine Video I2V", "grok-video-i2v", "xai/grok-imagine-video/image-to-video", "see fal", "Image-guided stylized video"),
    ("Grok Imagine Video Ref", "grok-video-ref", "xai/grok-imagine-video/reference-to-video", "see fal", "Reference-image video"),
    ("Sync Lipsync v3", "sync-lipsync", "fal-ai/sync-lipsync/v3", "see fal", "Dedicated lipsync"),
]


FAL_DOC_LINKS = {
    "gpt-image-2": "https://fal.ai/gpt-image-2",
    "gpt-image-2-api": "https://fal.ai/models/openai/gpt-image-2/playground",
    "gpt-image-2-prompting": "https://fal.ai/learn/tools/prompting-gpt-image-2",
    "nano-banana-2": "https://fal.ai/models/fal-ai/nano-banana-2",
    "nano-banana-pro": "https://fal.ai/models/fal-ai/nano-banana-pro",
    "gpt-image-1.5": "https://fal.ai/models/fal-ai/gpt-image-1.5/api",
    "flux-2-max": "https://fal.ai/models/fal-ai/flux-2-max/api",
    "flux-2-max-edit": "https://fal.ai/models/fal-ai/flux-2-max/edit/api",
    "flux-2-pro": "https://fal.ai/models/fal-ai/flux-2-pro/api",
    "flux-dev": "https://fal.ai/models/fal-ai/flux/dev",
    "sora2": "https://fal.ai/models/fal-ai/sora-2/text-to-video",
    "sora2-pro": "https://fal.ai/models/fal-ai/sora-2/text-to-video/pro",
    "sora2-image-to-video": "https://fal.ai/models/fal-ai/sora-2/image-to-video",
    "sora2-pro-image-to-video": "https://fal.ai/models/fal-ai/sora-2/image-to-video/pro",
    "sora2-remix": "https://fal.ai/models/fal-ai/sora-2/video-to-video/remix",
    "seedance2-reference": "https://fal.ai/models/bytedance/seedance-2.0/reference-to-video",
    "veo3-fast": "https://fal.ai/models/fal-ai/veo3.1/fast",
    "veo3-image-to-video": "https://fal.ai/models/fal-ai/veo3.1/image-to-video",
    "veo3-reference-to-video": "https://fal.ai/models/fal-ai/veo3.1/reference-to-video",
    "veo3-first-last": "https://fal.ai/models/fal-ai/veo3.1/first-last-frame-to-video",
    "veo3-extend": "https://fal.ai/models/fal-ai/veo3.1/extend-video",
    "grok-imagine-image": "https://fal.ai/docs/model-api-reference/image-generation-api/xai-grok-imagine-image.md",
    "grok-imagine-video": "https://fal.ai/docs/model-api-reference/video-generation-api/xai-grok-imagine-video.md",
    "pixverse-v6-i2v": "https://fal.ai/models/fal-ai/pixverse/v6/image-to-video",
    "pixverse-transition": "https://fal.ai/models/fal-ai/pixverse/v6/transition",
    "pixverse-extend": "https://fal.ai/models/fal-ai/pixverse/extend",
    "sync-lipsync": "https://fal.ai/models/fal-ai/sync-lipsync/v3",
    "seedream-v4": "https://fal.ai/models/fal-ai/bytedance/seedream/v4/text-to-image/api",
    "seedream-v4-edit": "https://fal.ai/models/fal-ai/bytedance/seedream/v4/edit/api",
    "seedream-edit": "https://fal.ai/models/fal-ai/bytedance/seedream/v4.5/edit",
    "wan27-edit": "https://fal.ai/models/fal-ai/wan/v2.7/edit",
}


ROUTING_DECISION_DIMENSIONS = [
    ("media_type", "image | video | audio | music | tts | 3d | tool"),
    ("operation", "generate | edit | inpaint | outpaint | variation | remix | extend | lipsync | caption"),
    ("goal", "best_quality | balanced | budget | typography | vector | cinematic | physics | social | preserve_layout | prompt_adherence | production_consistency | 4k_ready | flux_max"),
    ("input_shape", "none | single_image | multi_image | image+audio | video+audio | first+last_frame | video_only"),
    ("fidelity_priority", "preserve_subject | preserve_layout | restyle | create_net_new"),
    ("audio_requirement", "none | optional | required"),
    ("resolution_target", "hd | 1080p | 4k"),
    ("latency_budget", "fast | standard | premium"),
    ("cost_sensitivity", "low | medium | high"),
    ("provider_preference", "fal | piapi | together | runware | auto"),
]


ROUTING_SCHEMA = {
    "image": [
        {
            "route_id": "image-strict-inpaint",
            "operation": "inpaint",
            "model_key": "bria-eraser",
            "provider": "fal",
            "quality_tier": "specialist",
            "goal": "preserve_layout",
            "input_shape": "single_image",
            "fidelity_priority": "preserve_layout",
            "preservation_mode": "strict",
            "requires_mask": True,
            "use_when": [
                "Subtractive edits where canvas, framing, and composition must stay pixel-identical.",
                "The caller has (or can provide) a mask_url marking the exact region to modify.",
                "Requests like 'borra las cards', 'remove the logo', 'erase the text', with strict preservation intent.",
            ],
            "avoid_when": [
                "The edit is aesthetic or structural — not a bounded subtraction.",
                "No mask is available and no segmentation step is viable.",
            ],
            "keywords": [
                "inpaint",
                "erase",
                "eraser",
                "mask",
                "borra",
                "borrar",
                "elimina",
                "solo quita",
                "only remove",
                "pixel-identical",
            ],
            "fallback_model_keys": ["flux-inpaint", "flux-fill-pro", "flux-kontext-pro"],
        },
        {
            "route_id": "image-gpt-image-2-quality",
            "operation": "generate",
            "model_key": "gpt-image-2",
            "provider": "fal",
            "quality_tier": "ultra",
            "goal": "best_quality",
            "input_shape": "none",
            "fidelity_priority": "create_net_new",
            "use_when": [
                "Default quality-first image generation lane after GPT Image 2 / ChatGPT Images 2.0 became available on fal.",
                "You want top public-model quality, photorealism, text rendering, UI/layout logic, product photography, or strongest prompt adherence.",
                "The prompt is text-only and the job values final quality more than speed/cost.",
            ],
            "avoid_when": [
                "Fast iteration cost matters more than absolute prompt adherence.",
                "You need a vector-specific lane or a more open-ended aesthetic model.",
            ],
            "keywords": [
                "gpt image 2",
                "chatgpt images 2",
                "chat gpt 2.0",
                "chatgpt 2.0",
                "prompt adherence",
                "ui mockup",
                "dense text",
                "multilingual",
                "benchmark leader",
                "photorealism",
                "product photography",
            ],
            "fallback_model_keys": ["nano-banana-pro", "nano-banana-2"],
        },
        {
            "route_id": "image-gpt-image-1-5-high",
            "operation": "generate",
            "model_key": "gpt-image-1.5",
            "provider": "fal",
            "quality_tier": "premium",
            "goal": "prompt_adherence",
            "input_shape": "none",
            "fidelity_priority": "create_net_new",
            "use_when": [
                "You explicitly want GPT Image 1.5 high quality through fal.",
                "You need the older GPT Image 1.5 behavior for comparison or compatibility.",
            ],
            "avoid_when": [
                "You want the current best GPT Image lane; use GPT Image 2 instead.",
                "Fast iteration cost matters more than absolute prompt adherence.",
            ],
            "keywords": ["gpt image 1.5", "legacy gpt image", "compare gpt image 1.5"],
            "fallback_model_keys": ["nano-banana-pro", "nano-banana-2"],
        },
        {
            "route_id": "image-balanced-premium",
            "operation": "generate",
            "model_key": "nano-banana-2",
            "provider": "fal",
            "quality_tier": "premium",
            "goal": "balanced",
            "input_shape": "none",
            "fidelity_priority": "create_net_new",
            "use_when": [
                "Workhorse lane for fast/cost-sensitive image generation and batch creative iteration.",
                "Fast iteration on creative direction with short feedback loops.",
                "Batch production (dozens to thousands of images) where cost/throughput matter.",
                "Social media, marketing campaigns, web content, blog headers, product shots.",
                "Real-time features, live previews, interactive editors.",
            ],
            "avoid_when": [
                "The asset is a high-stakes hero image for print or a high-value brand deliverable.",
                "The prompt demands camera-ready fine typography (packaging, magazine, signage).",
                "Complex multi-element composition with strict spatial relationships that Pro handles better.",
                "The request is vector/logo/brand-system oriented (use recraft-v4-vector).",
                "The prompt's main requirement is readable text inside the image (use ideogram-v3).",
            ],
            "keywords": [
                "social", "marketing", "web", "blog", "iteration", "iterate", "batch",
                "quick", "fast", "rapido", "campaign", "content", "post", "thumbnail",
                "draft", "concept", "variation", "explore",
            ],
            "fallback_model_keys": ["nano-banana-pro", "flux-dev"],
        },
        {
            "route_id": "image-default-best-quality",
            "operation": "generate",
            "model_key": "gpt-image-2",
            "provider": "fal",
            "quality_tier": "ultra",
            "goal": "best_quality",
            "input_shape": "none",
            "fidelity_priority": "create_net_new",
            "use_when": [
                "Hero images for print campaigns or high-value brand assets where top public-model quality matters.",
                "Complex multi-element compositions with strict spatial relationships.",
                "Camera-ready fine typography, UI mockups, product labels, magazine layouts, or detailed signage.",
                "Photorealism, product photography, and instruction-following matter more than speed.",
                "User explicitly requests best possible quality, ultra fidelity, or editorial-grade output.",
            ],
            "avoid_when": [
                "Fast iteration or batch work where cost/throughput matters — use nano-banana-2 instead.",
                "Social media or web content where NB2's quality is indistinguishable at the target size.",
                "The request is vector/logo/brand-system oriented.",
            ],
            "keywords": [
                "hero", "hero shot", "hero image", "editorial", "luxury", "premium",
                "print", "magazine", "packaging", "camera-ready", "camera ready",
                "4k ultra", "ultra fidelity", "ultra quality", "brutal", "best quality",
                "best possible quality", "maxima calidad", "máxima calidad",
                "portada", "campaign hero", "flagship",
            ],
            "fallback_model_keys": ["nano-banana-pro", "nano-banana-2", "flux-dev"],
        },
        {
            "route_id": "image-flux-2-max-generate",
            "operation": "generate",
            "model_key": "flux-2-max",
            "provider": "fal",
            "quality_tier": "ultra",
            "goal": "flux_max",
            "input_shape": "none",
            "fidelity_priority": "create_net_new",
            "use_when": [
                "You explicitly want FLUX.2 [max] generation, not the edit lane.",
                "The brief wants maximum-quality FLUX.2 output for text-to-image.",
            ],
            "avoid_when": [
                "You need the cheaper or more consistent FLUX.2 Pro lane instead.",
            ],
            "keywords": ["flux 2 max", "flux.2 max", "maximum-quality flux", "max quality flux"],
            "fallback_model_keys": ["flux-2-pro", "nano-banana-pro"],
        },
        {
            "route_id": "image-flux-2-pro-generate",
            "operation": "generate",
            "model_key": "flux-2-pro",
            "provider": "fal",
            "quality_tier": "premium",
            "goal": "production_consistency",
            "input_shape": "none",
            "fidelity_priority": "create_net_new",
            "use_when": [
                "You want FLUX.2 [pro] for zero-config professional generation and more predictable batch consistency.",
                "Production consistency matters more than the extra push of the max lane.",
            ],
            "avoid_when": [
                "The brief specifically calls for GPT Image 1.5 or FLUX.2 Max.",
            ],
            "keywords": ["flux 2 pro", "flux.2 pro", "production consistency", "zero-config quality", "brand consistency"],
            "fallback_model_keys": ["flux-2-max", "nano-banana-pro"],
        },
        {
            "route_id": "image-seedream-v4-generate",
            "operation": "generate",
            "model_key": "seedream-v4",
            "provider": "fal",
            "quality_tier": "premium",
            "goal": "4k_ready",
            "input_shape": "none",
            "fidelity_priority": "create_net_new",
            "use_when": [
                "You explicitly want Seedream 4.0 generation through fal.",
                "4K-ready sizing and the Seedream v4 generation profile matter for the brief.",
            ],
            "avoid_when": [
                "You want the newer Seedream 4.5 lane or a model with a stronger public benchmark signal.",
            ],
            "keywords": ["seedream 4", "seedream 4.0", "4k ready", "seedream v4"],
            "fallback_model_keys": ["seedream", "nano-banana-2"],
        },
        {
            "route_id": "image-vector-branding",
            "operation": "generate",
            "model_key": "recraft-v4-vector",
            "provider": "fal",
            "quality_tier": "specialist",
            "goal": "vector",
            "input_shape": "none",
            "fidelity_priority": "create_net_new",
            "use_when": [
                "The request mentions logo, icon, vector, SVG, brand mark, packaging system, or design-kit style work.",
                "Clean shapes and design-system controllability matter more than photographic realism.",
                "Production-ready SVG output (scalable) is required.",
            ],
            "avoid_when": [
                "The output should look photographic or cinematic.",
                "The main challenge is typography rather than vector form.",
            ],
            "keywords": ["logo", "icon", "svg", "vector", "branding", "packaging", "brand mark", "design system"],
            "fallback_model_keys": ["recraft-v4", "recraft-v3", "ideogram-v3"],
        },
        {
            "route_id": "image-typography-poster",
            "operation": "generate",
            "model_key": "ideogram-v3",
            "provider": "fal",
            "quality_tier": "specialist",
            "goal": "typography",
            "input_shape": "none",
            "fidelity_priority": "create_net_new",
            "use_when": [
                "The image must contain readable text.",
                "Posters, banners, ads, or title cards where lettering is part of the output, not an afterthought.",
                "V3 adds style-reference and better spatial composition vs V2 while keeping 90-95% text accuracy.",
            ],
            "avoid_when": [
                "The image is purely illustrative with no real text burden.",
                "The user wants a vector/logo lane instead of raster poster work.",
            ],
            "keywords": ["poster", "banner", "headline", "text in image", "typography", "ad creative", "title card"],
            "fallback_model_keys": ["ideogram-v2", "recraft-v4", "nano-banana-pro"],
        },
        {
            "route_id": "image-conservative-edit",
            "operation": "edit",
            "model_key": "flux-kontext-pro",
            "provider": "fal",
            "quality_tier": "specialist",
            "goal": "preserve_layout",
            "input_shape": "single_image",
            "fidelity_priority": "preserve_layout",
            "preservation_mode": "strict",
            "use_when": [
                "The user wants the source image mostly unchanged except for targeted edits.",
                "Composition, framing, product placement, or subject identity should stay stable.",
            ],
            "avoid_when": [
                "The user wants an aggressive aesthetic restyle.",
                "The edit depends on multiple reference images or a taste-heavy reinterpretation.",
                "The user wants to replace one visual language or object family with another.",
            ],
            "keywords": ["preserve layout", "same framing", "keep composition", "subtle edit", "conservative edit"],
            "fallback_model_keys": ["seedream-edit", "nano-banana-pro"],
        },
        {
            "route_id": "image-strong-lookdev-edit",
            "operation": "edit",
            "model_key": "gpt-image-2",
            "provider": "fal",
            "quality_tier": "ultra",
            "goal": "best_quality",
            "input_shape": "single_image",
            "fidelity_priority": "preserve_subject",
            "preservation_mode": "flexible",
            "use_when": [
                "The user wants a stronger polish pass on an existing image without asking for a net-new composition.",
                "Solid lookdev passes: cinematic grading, richer lighting, realistic reflections, better materials, product-commercial finish.",
                "Fintech/luxury UI imagery where 'premium' means subtle controlled shadows, refined glass reflections, sharper material edges, and less generic glow.",
                "The brief is edit-first and quality-first, but not a pixel-faithful patch or a full structural replacement.",
            ],
            "avoid_when": [
                "The source layout must stay almost pixel-faithful.",
                "The request is primarily subtractive, masked, or exact-preservation work.",
                "The edit is a large structural replacement that fits Seedream or multi-reference aesthetic lanes better.",
            ],
            "keywords": [
                "cinematic",
                "raytracing",
                "ray tracing",
                "lookdev",
                "look dev",
                "color grade",
                "grading",
                "grade",
                "premium lighting",
                "premium",
                "luxury",
                "fintech",
                "subtle lighting",
                "refined reflections",
                "refined reflection",
                "realistic reflections",
                "product-commercial",
                "product commercial",
                "high-end",
                "high end",
                "photoreal polish",
                "material realism",
            ],
            "fallback_model_keys": ["nano-banana-pro", "flux-2-max-edit", "flux-kontext-pro", "seedream-edit"],
        },
        {
            "route_id": "image-relight",
            "operation": "relight",
            "model_key": "iclight-v2",
            "provider": "fal",
            "quality_tier": "specialist",
            "goal": "relight",
            "input_shape": "single_image",
            "fidelity_priority": "preserve_layout",
            "preservation_mode": "strict",
            "use_when": [
                "The user wants to change lighting, shadows, reflections, or ambience without altering composition or content.",
                "Requests like 'add window shadow', 'add rim light', 'reiluminar', 'sombra de ventana', 'cinematic relight'.",
                "The canvas, framing, and subject identity must stay intact; only the light field changes.",
            ],
            "avoid_when": [
                "The user wants to modify objects, textures, or layout — not just lighting.",
                "The prompt is a generic edit without explicit lighting intent.",
            ],
            "keywords": [
                "relight",
                "reiluminar",
                "iluminacion",
                "iluminación",
                "sombra",
                "sombras",
                "shadow",
                "shadows",
                "reflejo",
                "reflejos",
                "reflection",
                "reflections",
                "window light",
                "luz de ventana",
                "sombra de ventana",
                "cinematic lighting",
                "studio light",
                "rim light",
                "backlight",
                "key light",
            ],
            "fallback_model_keys": ["flux-kontext-pro", "seedream-edit"],
        },
        {
            "route_id": "image-high-end-edit",
            "operation": "edit",
            "model_key": "seedream-edit",
            "provider": "fal",
            "quality_tier": "premium",
            "goal": "restyle",
            "input_shape": "single_image",
            "fidelity_priority": "preserve_subject",
            "preservation_mode": "flexible",
            "use_when": [
                "You need a flexible reference-guided restyle, not just a conservative patch or lookdev polish.",
                "The user wants stronger visual reinterpretation while still starting from an existing image.",
            ],
            "avoid_when": [
                "The source layout must stay almost pixel-faithful.",
                "The request is blur-sensitive fintech/luxury polish, subtle premium lighting, refined shadows, or glass/reflection cleanup on an existing composition; prefer image-strong-lookdev-edit.",
                "The request is very budget-sensitive.",
            ],
            "keywords": [
                "restyle",
                "premium edit",
                "reference-guided",
                "enhance aesthetic",
                "replace",
                "swap",
                "instead of",
                "wireframe",
                "change particles",
            ],
            "fallback_model_keys": ["flux-kontext-pro", "wan27-edit"],
        },
        {
            "route_id": "image-budget-edit",
            "operation": "edit",
            "model_key": "wan27-edit",
            "provider": "fal",
            "quality_tier": "budget",
            "goal": "balanced",
            "input_shape": "single_image",
            "fidelity_priority": "preserve_subject",
            "preservation_mode": "flexible",
            "use_when": [
                "The request needs image editing coverage at lower cost.",
                "You want a cheaper fallback behind Seedream/Kontext.",
            ],
            "avoid_when": [
                "The user is explicitly paying for top-tier edit quality.",
                "You need the safest layout preservation.",
            ],
            "keywords": ["budget edit", "cheap edit", "cost-efficient"],
            "fallback_model_keys": ["flux-kontext-pro", "seedream-edit"],
        },
        {
            "route_id": "image-aesthetic-taste-first",
            "operation": "generate",
            "model_key": "grok-imagine",
            "provider": "fal",
            "quality_tier": "premium",
            "goal": "stylized",
            "input_shape": "none",
            "fidelity_priority": "create_net_new",
            "use_when": [
                "The prompt is taste-first: fashion, moodboard, stylized premium, aesthetic-heavy work.",
                "The user wants more vibe and taste than strict brand/system control.",
            ],
            "avoid_when": [
                "The request is typography-heavy, vector-heavy, or conservative editing.",
                "The user wants the most faithful photoreal default rather than an aesthetic bias.",
            ],
            "keywords": ["aesthetic", "fashion", "taste", "stylized premium", "mood"],
            "fallback_model_keys": ["nano-banana-pro", "grok-imagine-edit"],
        },
        {
            "route_id": "image-multi-reference-aesthetic-edit",
            "operation": "edit",
            "model_key": "grok-imagine-edit",
            "provider": "fal",
            "quality_tier": "premium",
            "goal": "restyle",
            "input_shape": "multi_image",
            "fidelity_priority": "preserve_subject",
            "preservation_mode": "flexible",
            "use_when": [
                "The edit uses multiple input images to transfer mood or aesthetic.",
                "You need an aesthetic-first edit lane instead of conservative preservation.",
            ],
            "avoid_when": [
                "The edit is tiny and layout fidelity is the primary requirement.",
                "You only have one image and no real need for multi-reference behavior.",
            ],
            "keywords": ["multi reference", "blend references", "aesthetic edit"],
            "fallback_model_keys": ["seedream-edit", "flux-kontext-pro"],
        },
    ],
    "video": [
        {
            "route_id": "video-default-t2v",
            "operation": "generate",
            "model_key": "kling",
            "provider": "fal",
            "quality_tier": "standard",
            "goal": "balanced",
            "input_shape": "none",
            "fidelity_priority": "create_net_new",
            "audio_requirement": "optional",
            "use_when": [
                "General text-to-video with no specialist need.",
                "You need the best default value lane for human subjects, motion, and broad prompt coverage.",
            ],
            "avoid_when": [
                "The request is specifically about physics realism, reference-heavy composition, or top-end 4K polish.",
            ],
            "keywords": ["general motion", "person", "actor", "dialogue", "default video"],
            "fallback_model_keys": ["seedance2", "sora2"],
        },
        {
            "route_id": "video-cinematic-direction",
            "operation": "generate",
            "model_key": "seedance2",
            "provider": "fal",
            "quality_tier": "premium",
            "goal": "cinematic",
            "input_shape": "none",
            "fidelity_priority": "create_net_new",
            "audio_requirement": "optional",
            "use_when": [
                "Product shots, creative direction, cinematic control, or material-forward motion work.",
                "The user values directed composition over cheap generic motion.",
            ],
            "avoid_when": [
                "The job is simple enough for Kling.",
                "The request is specifically about physical realism rather than cinematic look.",
            ],
            "keywords": ["cinematic", "product shot", "materials", "creative direction"],
            "fallback_model_keys": ["seedance2-reference", "kling"],
        },
        {
            "route_id": "video-multi-reference-direction",
            "operation": "generate",
            "model_key": "seedance2-reference",
            "provider": "fal",
            "quality_tier": "premium",
            "goal": "cinematic",
            "input_shape": "multi_image",
            "fidelity_priority": "preserve_subject",
            "audio_requirement": "optional",
            "use_when": [
                "The user provides multiple references and expects the model to respect them.",
                "You need a composition-directed lane, not generic I2V.",
            ],
            "avoid_when": [
                "You only have a single image.",
                "The task is simple enough for standard text-to-video.",
            ],
            "keywords": ["multi reference", "reference direction", "guided composition"],
            "fallback_model_keys": ["seedance2", "veo3-ref"],
        },
        {
            "route_id": "video-physics-realism",
            "operation": "generate",
            "model_key": "sora2",
            "provider": "fal",
            "quality_tier": "premium",
            "goal": "physics",
            "input_shape": "none",
            "fidelity_priority": "create_net_new",
            "audio_requirement": "optional",
            "use_when": [
                "The prompt depends on physical interaction, gravity, fluids, collisions, or realistic dynamics.",
                "You need realism more than stylization or cost efficiency.",
            ],
            "avoid_when": [
                "The user mainly wants stylized or social-native motion.",
                "The task is actually a video remix or edit rather than clean T2V.",
            ],
            "keywords": ["physics", "gravity", "fluid", "collision", "fabric simulation"],
            "fallback_model_keys": ["sora2-pro", "veo3"],
        },
        {
            "route_id": "video-remix-v2v",
            "operation": "remix",
            "model_key": "sora2-remix",
            "provider": "fal",
            "quality_tier": "premium",
            "goal": "restyle",
            "input_shape": "video_only",
            "fidelity_priority": "preserve_layout",
            "audio_requirement": "none",
            "use_when": [
                "The user says remix, restyle, reinterpret this clip, or preserve motion but change look.",
                "You need V2V, not T2V or I2V.",
            ],
            "avoid_when": [
                "There is no input video.",
                "The request is simply to extend an existing clip.",
                "The request is to improve technical video quality, upscale, denoise, sharpen, deblur, or make the same clip cleaner.",
            ],
            "keywords": ["remix", "restyle this clip", "video to video"],
            "fallback_model_keys": ["pixverse-extend", "veo3-extend"],
        },
        {
            "route_id": "video-enhance-upscale",
            "operation": "edit",
            "model_key": "video-upscale",
            "provider": "piapi",
            "quality_tier": "specialist",
            "goal": "best_quality",
            "input_shape": "video_only",
            "fidelity_priority": "preserve_layout",
            "audio_requirement": "none",
            "use_when": [
                "The user wants to improve the same rendered video rather than generate new motion.",
                "Technical cleanup: upscale, denoise, sharpen, deblur, reduce compression artifacts, or improve perceived quality.",
                "Use after the final motion is chosen; for best pro results, external Topaz/Runway-style enhancement may still beat a generative video lane.",
            ],
            "avoid_when": [
                "The user wants creative restyle/remix of the clip.",
                "The user wants more seconds or continuation; use video-extend.",
                "The source motion is bad and should be regenerated from image or prompt.",
            ],
            "keywords": [
                "upscale video",
                "video upscale",
                "enhance video",
                "improve video quality",
                "mejora la calidad",
                "mejorar la calidad",
                "se ve mala calidad",
                "denoise",
                "sharpen",
                "deblur",
                "compression artifacts",
                "artifact cleanup",
            ],
            "fallback_model_keys": [],
        },
        {
            "route_id": "video-ultra-fast",
            "operation": "generate",
            "model_key": "veo3",
            "provider": "fal",
            "quality_tier": "ultra",
            "goal": "best_quality",
            "input_shape": "none",
            "fidelity_priority": "create_net_new",
            "audio_requirement": "optional",
            "use_when": [
                "The request explicitly wants ultra/high-end quality, 4K-ish positioning, or broadcast-grade polish.",
                "You need top-end output but want the faster Veo lane first.",
            ],
            "avoid_when": [
                "The budget does not justify Veo.",
                "The task is actually a reference/video extension workflow.",
            ],
            "keywords": ["4k", "broadcast", "cinema polish", "highest end", "ultra"],
            "fallback_model_keys": ["veo3-hq", "sora2"],
        },
        {
            "route_id": "video-ultra-max-quality",
            "operation": "generate",
            "model_key": "veo3-hq",
            "provider": "fal",
            "quality_tier": "ultra",
            "goal": "best_quality",
            "input_shape": "none",
            "fidelity_priority": "create_net_new",
            "audio_requirement": "optional",
            "use_when": [
                "The user wants maximum Veo quality over speed.",
                "You already know the brief justifies the most expensive/high-end route.",
            ],
            "avoid_when": [
                "The request can be solved by Veo fast or Kling.",
            ],
            "keywords": ["max quality", "highest fidelity", "hero cinematic"],
            "fallback_model_keys": ["veo3", "sora2-pro"],
        },
        {
            "route_id": "video-reference-driven",
            "operation": "generate",
            "model_key": "veo3-ref",
            "provider": "fal",
            "quality_tier": "ultra",
            "goal": "best_quality",
            "input_shape": "multi_image",
            "fidelity_priority": "preserve_subject",
            "audio_requirement": "optional",
            "use_when": [
                "You need Veo-class output while steering from reference imagery.",
                "The job needs stronger quality than Seedance reference can justify.",
            ],
            "avoid_when": [
                "The request is primarily social/stylized rather than premium cinematic.",
                "No reference images are provided.",
            ],
            "keywords": ["reference video", "reference to video", "guided Veo"],
            "fallback_model_keys": ["seedance2-reference", "veo3-i2v"],
        },
        {
            "route_id": "video-first-last-frame",
            "operation": "generate",
            "model_key": "veo3-first-last",
            "provider": "fal",
            "quality_tier": "ultra",
            "goal": "preserve_layout",
            "input_shape": "first+last_frame",
            "fidelity_priority": "preserve_layout",
            "audio_requirement": "none",
            "use_when": [
                "The brief provides a first frame and a destination last frame.",
                "You need controlled interpolation between two endpoints.",
            ],
            "avoid_when": [
                "You only have one frame.",
                "The request is actually to extend an existing video.",
            ],
            "keywords": ["first and last frame", "frame interpolation", "from this frame to that frame"],
            "fallback_model_keys": ["pixverse-transition", "veo3-i2v"],
        },
        {
            "route_id": "video-extend",
            "operation": "extend",
            "model_key": "veo3-extend",
            "provider": "fal",
            "quality_tier": "ultra",
            "goal": "preserve_layout",
            "input_shape": "video_only",
            "fidelity_priority": "preserve_layout",
            "audio_requirement": "optional",
            "use_when": [
                "The user says continue this clip, extend this video, or add more seconds without changing the core shot.",
            ],
            "avoid_when": [
                "The user wants a creative restyle instead of literal continuation.",
                "The user wants to improve quality of the same clip; Veo extend is continuation/polish, not a frame-faithful enhancer.",
            ],
            "keywords": ["continue this video", "extend clip", "video continuation"],
            "fallback_model_keys": ["pixverse-extend", "sora2-remix"],
        },
        {
            "route_id": "video-social-stylized-i2v",
            "operation": "generate",
            "model_key": "pixverse-v6-i2v",
            "provider": "fal",
            "quality_tier": "specialist",
            "goal": "social",
            "input_shape": "single_image",
            "fidelity_priority": "preserve_subject",
            "audio_requirement": "none",
            "use_when": [
                "Stylized/social-native animation, viral motion, anime-ish movement, or trend-oriented content.",
                "You care more about punchy motion language than physical realism.",
            ],
            "avoid_when": [
                "The output needs top-end realism or premium cinematic polish.",
            ],
            "keywords": ["viral", "stylized social", "anime motion", "reel motion"],
            "fallback_model_keys": ["pixverse-transition", "grok-video-i2v"],
        },
        {
            "route_id": "video-transition",
            "operation": "generate",
            "model_key": "pixverse-transition",
            "provider": "fal",
            "quality_tier": "specialist",
            "goal": "social",
            "input_shape": "first+last_frame",
            "fidelity_priority": "preserve_layout",
            "audio_requirement": "none",
            "use_when": [
                "The task is an image-to-image transition clip for reels or stylized motion posts.",
            ],
            "avoid_when": [
                "You need realistic cinematic interpolation rather than flashy transition language.",
            ],
            "keywords": ["transition", "before after", "reel transition"],
            "fallback_model_keys": ["veo3-first-last", "pixverse-v6-i2v"],
        },
        {
            "route_id": "video-aesthetic-t2v",
            "operation": "generate",
            "model_key": "grok-video",
            "provider": "fal",
            "quality_tier": "premium",
            "goal": "stylized",
            "input_shape": "none",
            "fidelity_priority": "create_net_new",
            "audio_requirement": "optional",
            "use_when": [
                "The brief is taste-first and aesthetic-heavy rather than realism-first.",
                "You want xAI's stylized signature on video.",
            ],
            "avoid_when": [
                "Physics realism or premium reference-control is the main requirement.",
            ],
            "keywords": ["stylized video", "taste-first", "fashion motion"],
            "fallback_model_keys": ["grok-video-i2v", "kling"],
        },
        {
            "route_id": "video-aesthetic-reference",
            "operation": "generate",
            "model_key": "grok-video-ref",
            "provider": "fal",
            "quality_tier": "premium",
            "goal": "stylized",
            "input_shape": "multi_image",
            "fidelity_priority": "preserve_subject",
            "audio_requirement": "optional",
            "use_when": [
                "Stylized video generation steered by reference images.",
            ],
            "avoid_when": [
                "The task needs conservative fidelity or high-end cinematic Veo behavior.",
            ],
            "keywords": ["reference stylized video", "aesthetic reference"],
            "fallback_model_keys": ["grok-video-i2v", "seedance2-reference"],
        },
        {
            "route_id": "video-lipsync",
            "operation": "lipsync",
            "model_key": "sync-lipsync",
            "provider": "fal",
            "quality_tier": "specialist",
            "goal": "preserve_layout",
            "input_shape": "video+audio",
            "fidelity_priority": "preserve_subject",
            "audio_requirement": "required",
            "use_when": [
                "You need a person/character to speak to provided audio.",
                "Dedicated lipsync beats overloading general video lanes.",
            ],
            "avoid_when": [
                "The job is actually avatar generation from a still image.",
                "No external audio exists.",
            ],
            "keywords": ["lipsync", "dub", "make this person speak"],
            "fallback_model_keys": ["kling-sound", "omnihuman"],
        },
    ],
    "music": [
        {
            "route_id": "music-default-full-song",
            "operation": "generate",
            "model_key": "diffrhythm-full",
            "provider": "fal",
            "quality_tier": "premium",
            "goal": "best_quality",
            "input_shape": "none",
            "fidelity_priority": "create_net_new",
            "use_when": [
                "The user wants a fuller song-like result, not a tiny jingle.",
            ],
            "avoid_when": [
                "You need very cheap fast drafts or iterative short musical ideas.",
            ],
            "keywords": ["song", "full track", "complete music"],
            "fallback_model_keys": ["ace-step", "udio"],
        },
        {
            "route_id": "music-flexible-fast",
            "operation": "generate",
            "model_key": "ace-step",
            "provider": "fal",
            "quality_tier": "standard",
            "goal": "balanced",
            "input_shape": "none",
            "fidelity_priority": "create_net_new",
            "use_when": [
                "You need flexible lower-cost music generation or fast iteration.",
            ],
            "avoid_when": [
                "The user explicitly wants the most complete song-like lane available.",
            ],
            "keywords": ["music bed", "quick music", "flexible music"],
            "fallback_model_keys": ["diffrhythm-base", "udio"],
        },
    ],
    "tts": [
        {
            "route_id": "tts-voice-clone",
            "operation": "generate",
            "model_key": "f5-tts",
            "provider": "fal",
            "quality_tier": "standard",
            "goal": "preserve_subject",
            "input_shape": "image+audio",
            "fidelity_priority": "preserve_subject",
            "use_when": [
                "The user wants speech synthesis, especially voice-clone or zero-shot style TTS.",
            ],
            "avoid_when": [
                "The task is music generation, not spoken audio.",
            ],
            "keywords": ["tts", "voice", "speech", "say this", "clone voice"],
            "fallback_model_keys": [],
        },
    ],
    "3d": [
        {
            "route_id": "3d-image-to-model",
            "operation": "generate",
            "model_key": "trellis2",
            "provider": "fal",
            "quality_tier": "premium",
            "goal": "best_quality",
            "input_shape": "single_image",
            "fidelity_priority": "preserve_subject",
            "use_when": [
                "The user wants a 3D model from an image and quality matters.",
            ],
            "avoid_when": [
                "The user only needs a quick cheap proof of concept.",
            ],
            "keywords": ["3d model", "glb", "mesh", "object from image"],
            "fallback_model_keys": ["trellis-image", "trellis-multi"],
        },
        {
            "route_id": "3d-text-to-model",
            "operation": "generate",
            "model_key": "trellis-text",
            "provider": "fal",
            "quality_tier": "standard",
            "goal": "balanced",
            "input_shape": "none",
            "fidelity_priority": "create_net_new",
            "use_when": [
                "The user wants a 3D model from text only.",
            ],
            "avoid_when": [
                "Reference imagery exists and should be exploited.",
            ],
            "keywords": ["text to 3d", "generate 3d object"],
            "fallback_model_keys": ["trellis2"],
        },
    ],
    "tool": [
        {
            "route_id": "tool-remove-background",
            "operation": "edit",
            "model_key": "remove-bg",
            "provider": "fal",
            "quality_tier": "specialist",
            "goal": "preserve_layout",
            "input_shape": "single_image",
            "fidelity_priority": "preserve_subject",
            "use_when": [
                "The task is explicit background removal.",
            ],
            "avoid_when": [
                "The user wants a generative edit rather than utility extraction.",
            ],
            "keywords": ["remove background", "transparent background", "cutout"],
            "fallback_model_keys": [],
        },
        {
            "route_id": "tool-image-upscale",
            "operation": "edit",
            "model_key": "image-upscale",
            "provider": "fal",
            "quality_tier": "specialist",
            "goal": "best_quality",
            "input_shape": "single_image",
            "fidelity_priority": "preserve_layout",
            "use_when": [
                "The task is explicit upscaling or resolution enhancement.",
            ],
            "avoid_when": [
                "The image actually needs regeneration, not magnification.",
            ],
            "keywords": ["upscale", "enhance", "increase resolution"],
            "fallback_model_keys": [],
        },
        {
            "route_id": "tool-video-audio",
            "operation": "edit",
            "model_key": "mmaudio",
            "provider": "fal",
            "quality_tier": "specialist",
            "goal": "balanced",
            "input_shape": "video_only",
            "fidelity_priority": "preserve_layout",
            "use_when": [
                "The task is to add/generate audio for an existing video.",
            ],
            "avoid_when": [
                "The user wants a fresh video, not audio augmentation.",
            ],
            "keywords": ["add audio", "sound design", "audio for video"],
            "fallback_model_keys": [],
        },
        {
            "route_id": "tool-caption",
            "operation": "caption",
            "model_key": "joycaption",
            "provider": "piapi",
            "quality_tier": "specialist",
            "goal": "balanced",
            "input_shape": "single_image",
            "fidelity_priority": "preserve_subject",
            "use_when": [
                "The user wants captioning/description for an image as a utility operation.",
            ],
            "avoid_when": [
                "The task is generation or editing rather than description.",
            ],
            "keywords": ["caption", "describe image", "alt text"],
            "fallback_model_keys": [],
        },
    ],
}


ROUTE_SIGNAL_FIELDS = (
    "operation",
    "goal",
    "input_shape",
    "fidelity_priority",
    "audio_requirement",
    "provider_preference",
)


STRUCTURAL_REPLACEMENT_KEYWORDS = (
    "replace",
    "remplace",
    "reempla",
    "swap",
    "instead of",
    "turn the",
    "turn this",
    "convert the",
)


SUBTRACTIVE_EDIT_KEYWORDS = (
    "remove",
    "delete",
    "erase",
    "clean up",
    "without",
    "remove the cards",
    "remove the card",
    "remove the text",
    "remove the logo",
    "sin cards",
    "sin card",
    "sin ninguna card",
    "sin texto",
    "solo la imagen",
)


LAYOUT_PRESERVATION_KEYWORDS = (
    "same framing",
    "same format",
    "same composition",
    "same layout",
    "original format",
    "original framing",
    "original composition",
    "original layout",
    "keep original",
    "preserve original",
    "do not change the composition",
    "don't change the composition",
    "do not change the framing",
    "don't change the framing",
    "exact same framing",
    "exact same composition",
    "exact same layout",
    "keep composition",
    "keep layout",
    "keep the framing",
    "keep the composition",
    "keep the format",
    "maintain framing",
    "maintain layout",
    "mismo formato",
    "mismo encuadre",
    "misma composicion",
    "misma composición",
    "formato original",
    "encuadre original",
    "composición original",
    "composicion original",
    "no cambies la composicion",
    "no cambies la composición",
    "no cambies el encuadre",
    "no tocar",
    "no toques",
)


AGGRESSIVE_EDIT_STYLE_KEYWORDS = (
    "wireframe",
    "wireframes",
    "task",
    "tasks",
    "llamadas",
    "correos",
    "emails",
    "restyle",
    "new visual language",
    "reference",
)


LOCALIZED_SAFE_EDIT_KEYWORDS = (
    "texture",
    "textura",
    "background",
    "fondo",
    "pedestal",
    "platform",
    "plataforma",
    "floor",
    "suelo",
    "surface",
    "material",
    "solo cambia",
    "only change",
)


RELIGHT_INTENT_KEYWORDS = (
    "relight",
    "re-light",
    "reiluminar",
    "reiluminación",
    "reiluminacion",
    "sombra de ventana",
    "sombras de ventana",
    "window shadow",
    "window shadows",
    "window light",
    "luz de ventana",
    "rim light",
    "backlight",
    "key light",
    "cinematic lighting",
    "studio light",
    "studio lighting",
    "add shadow",
    "add shadows",
    "add reflection",
    "add reflections",
    "agrega sombra",
    "agrega sombras",
    "agregar sombra",
    "agregar sombras",
    "agrega reflejo",
    "agrega reflejos",
    "agregar reflejo",
    "agregar reflejos",
    "reflejos",
    "reflejo",
)


# Premium-tier intent: phrases that justify leaving the fast Nano Banana 2
# workhorse and using the quality-first GPT Image 2 lane.
PREMIUM_HERO_INTENT_KEYWORDS = (
    "hero",
    "hero shot",
    "hero image",
    "editorial",
    "luxury",
    "lujo",
    "print",
    "impresion",
    "impresión",
    "magazine",
    "revista",
    "packaging",
    "empaque",
    "camera-ready",
    "camera ready",
    "camera-ready typography",
    "4k ultra",
    "ultra fidelity",
    "ultra quality",
    "maxima calidad",
    "máxima calidad",
    "best possible quality",
    "best quality",
    "highest quality",
    "brutal quality",
    "flagship",
    "portada",
    "campaign hero",
    "cover",
    "signage",
    "billboard",
)


PREMIUM_EDIT_INTENT_KEYWORDS = (
    "cinematic",
    "cinematic look",
    "cinematic lighting",
    "raytracing",
    "ray tracing",
    "lookdev",
    "look dev",
    "color grade",
    "colour grade",
    "grading",
    "grade",
    "movie lighting",
    "film lighting",
    "film look",
    "movie look",
    "premium lighting",
    "realistic reflections",
    "realistic reflection",
    "material realism",
    "photoreal polish",
    "high-end polish",
    "high end polish",
    "product-commercial",
    "product commercial",
)


VIDEO_ENHANCE_INTENT_KEYWORDS = (
    "upscale video",
    "video upscale",
    "enhance video",
    "improve video quality",
    "better video quality",
    "increase video quality",
    "mejora la calidad",
    "mejorar la calidad",
    "sube la calidad",
    "se ve mala calidad",
    "mala calidad",
    "denoise",
    "sharpen",
    "deblur",
    "compression artifacts",
    "artifact cleanup",
)


def infer_input_shape(params: dict | None) -> str:
    params = params or {}

    image_count = len(params.get("image_urls") or [])
    if params.get("image_url"):
        image_count += 1
    if params.get("reference_image_urls"):
        image_count += len(params.get("reference_image_urls") or [])

    video_count = len(params.get("video_urls") or [])
    if params.get("video_url") or params.get("video"):
        video_count += 1

    audio_count = len(params.get("audio_urls") or [])
    if params.get("audio_url") or params.get("audio") or params.get("ref_audio"):
        audio_count += 1

    if params.get("first_frame_url") and (params.get("last_frame_url") or params.get("end_image_url")):
        return "first+last_frame"
    if video_count and audio_count:
        return "video+audio"
    if image_count and audio_count:
        return "image+audio"
    if video_count:
        return "video_only"
    if image_count > 1:
        return "multi_image"
    if image_count == 1:
        return "single_image"
    return "none"


def _normalize_prompt(prompt: str | None) -> str:
    return (prompt or "").strip().lower()


def _contains_any(prompt: str, keywords: tuple[str, ...]) -> bool:
    return any(keyword in prompt for keyword in keywords)


def requires_strict_preservation(
    media_type: str,
    *,
    prompt: str = "",
    params: dict | None = None,
    requested: dict | None = None,
) -> bool:
    if media_type != "image":
        return False

    requested = requested or {}
    inferred_shape = requested.get("input_shape") or infer_input_shape(params)
    if inferred_shape not in {"single_image", "multi_image", "image+audio"}:
        return False

    normalized_prompt = _normalize_prompt(prompt)
    operation = requested.get("operation", "")
    goal = requested.get("goal", "")
    fidelity_priority = requested.get("fidelity_priority", "")

    has_layout_preservation_intent = _contains_any(normalized_prompt, LAYOUT_PRESERVATION_KEYWORDS)
    has_subtractive_edit_intent = _contains_any(normalized_prompt, SUBTRACTIVE_EDIT_KEYWORDS)
    has_localized_safe_edit_intent = _contains_any(normalized_prompt, LOCALIZED_SAFE_EDIT_KEYWORDS)
    has_structural_replacement_intent = _contains_any(normalized_prompt, STRUCTURAL_REPLACEMENT_KEYWORDS)
    has_aggressive_edit_style = _contains_any(normalized_prompt, AGGRESSIVE_EDIT_STYLE_KEYWORDS)

    explicit_preserve_request = (
        goal == "preserve_layout"
        or fidelity_priority == "preserve_layout"
        or operation in {"inpaint", "outpaint"}
    )

    return (
        (explicit_preserve_request or has_layout_preservation_intent)
        and not has_structural_replacement_intent
        and not has_aggressive_edit_style
        and (has_subtractive_edit_intent or has_localized_safe_edit_intent or explicit_preserve_request)
    )


def validate_route_constraints(
    media_type: str,
    route: dict,
    *,
    prompt: str = "",
    params: dict | None = None,
    requested: dict | None = None,
) -> None:
    if not requires_strict_preservation(
        media_type,
        prompt=prompt,
        params=params,
        requested=requested,
    ):
        return

    preservation_mode = route.get("preservation_mode", "flexible")
    if preservation_mode == "strict":
        return

    raise ValueError(
        "Strict preservation requested: keep original format/framing/composition. "
        f"Route '{route.get('route_id', '')}' is not allowed because it is a flexible/generative edit lane."
    )


def _shape_supported(route_shape: str, inferred_shape: str) -> bool:
    if route_shape == inferred_shape:
        return True
    if route_shape == "none":
        return inferred_shape == "none"
    if route_shape == "single_image":
        return inferred_shape in {"single_image", "image+audio"}
    if route_shape == "multi_image":
        return inferred_shape == "multi_image"
    if route_shape == "video_only":
        return inferred_shape in {"video_only", "video+audio"}
    if route_shape == "image+audio":
        return inferred_shape == "image+audio"
    if route_shape == "video+audio":
        return inferred_shape == "video+audio"
    if route_shape == "first+last_frame":
        return inferred_shape == "first+last_frame"
    return False


def _audio_requirement_satisfied(route_audio: str, inferred_shape: str) -> bool:
    has_audio = inferred_shape in {"image+audio", "video+audio"}
    if route_audio == "required":
        return has_audio
    if route_audio == "none":
        return not has_audio or inferred_shape == "video_only"
    return True


def select_route(
    media_type: str,
    *,
    prompt: str = "",
    params: dict | None = None,
    route_id: str = "",
    requested: dict | None = None,
) -> dict:
    routes = ROUTING_SCHEMA.get(media_type, [])
    if not routes:
        raise ValueError(f"Unsupported media_type for routing: {media_type}")

    requested = requested or {}
    inferred_shape = requested.get("input_shape") or infer_input_shape(params)
    normalized_prompt = _normalize_prompt(prompt)
    has_structural_replacement_intent = _contains_any(normalized_prompt, STRUCTURAL_REPLACEMENT_KEYWORDS)
    has_layout_preservation_intent = _contains_any(normalized_prompt, LAYOUT_PRESERVATION_KEYWORDS)
    has_subtractive_edit_intent = _contains_any(normalized_prompt, SUBTRACTIVE_EDIT_KEYWORDS)
    has_aggressive_edit_style = _contains_any(normalized_prompt, AGGRESSIVE_EDIT_STYLE_KEYWORDS)
    has_localized_safe_edit_intent = _contains_any(normalized_prompt, LOCALIZED_SAFE_EDIT_KEYWORDS)
    has_relight_intent = _contains_any(normalized_prompt, RELIGHT_INTENT_KEYWORDS)
    has_premium_hero_intent = _contains_any(normalized_prompt, PREMIUM_HERO_INTENT_KEYWORDS)
    has_premium_edit_intent = _contains_any(normalized_prompt, PREMIUM_EDIT_INTENT_KEYWORDS)
    has_video_enhance_intent = _contains_any(normalized_prompt, VIDEO_ENHANCE_INTENT_KEYWORDS)
    strict_preservation_required = requires_strict_preservation(
        media_type,
        prompt=prompt,
        params=params,
        requested=requested,
    )

    if route_id:
        route_id = ROUTE_ID_ALIASES.get(route_id, route_id)
        for route in routes:
            if route["route_id"] == route_id:
                validate_route_constraints(
                    media_type,
                    route,
                    prompt=prompt,
                    params=params,
                    requested=requested,
                )
                return route
        raise ValueError(f"Unknown route_id '{route_id}' for media_type '{media_type}'")

    best_route = None
    best_score = None

    for index, route in enumerate(routes):
        route_shape = route.get("input_shape", "none")
        route_audio = route.get("audio_requirement", "none")

        if not _shape_supported(route_shape, inferred_shape):
            continue
        if not _audio_requirement_satisfied(route_audio, inferred_shape):
            continue
        if strict_preservation_required and route.get("preservation_mode", "flexible") != "strict":
            continue

        score = 0

        for field in ROUTE_SIGNAL_FIELDS:
            requested_value = requested.get(field)
            route_value = route.get(field)
            if not requested_value or not route_value:
                continue
            if requested_value == route_value:
                score += {
                    "operation": 30,
                    "goal": 24,
                    "input_shape": 20,
                    "fidelity_priority": 12,
                    "audio_requirement": 10,
                    "provider_preference": 8,
                }[field]

        if route_shape == inferred_shape:
            score += 18

        if normalized_prompt:
            for keyword in route.get("keywords", []):
                if keyword.lower() in normalized_prompt:
                    score += 7

            for phrase in route.get("avoid_when", []):
                lowered = phrase.lower()
                if lowered and lowered in normalized_prompt:
                    score -= 12

        if media_type == "image" and route.get("operation") == "inpaint":
            route_id_value = route.get("route_id", "")

            if route_id_value == "image-strict-inpaint":
                if strict_preservation_required:
                    score += 150  # beats conservative (+100) when strict is required
                if has_subtractive_edit_intent:
                    score += 25
                if has_layout_preservation_intent:
                    score += 15
                if has_localized_safe_edit_intent and not has_aggressive_edit_style:
                    score += 12
                if has_structural_replacement_intent:
                    score -= 30
                # Only meaningful when a mask is actually provided; penalize otherwise.
                if route.get("requires_mask") and params and not params.get("mask_url"):
                    score -= 40

        if media_type == "image" and route.get("operation") == "relight":
            route_id_value = route.get("route_id", "")

            if route_id_value == "image-relight":
                # Relight lane is specialist (IC-Light v2) and requires explicit
                # opt-in via `operation="relight"` or `--route-id image-relight`.
                # Prompts like "agrega sombra de ventana" are semantically
                # compositional edits and route through `image-conservative-edit`
                # (flux-kontext-pro), which handles subtle lighting well.
                explicit_relight_op = requested.get("operation") == "relight"
                explicit_non_relight_op = bool(
                    requested.get("operation")
                ) and requested.get("operation") != "relight"
                if explicit_relight_op and has_relight_intent:
                    score += 130  # beats conservative-edit when caller explicitly asks for relight
                elif has_relight_intent and not explicit_non_relight_op:
                    # Keyword-only match without any explicit op: nudge but do NOT outrank
                    # conservative-edit. If the caller already picked operation="edit" (or
                    # any non-relight op), the lighting keywords must not steal the route.
                    score += 20
                if strict_preservation_required:
                    score += 30
                if has_layout_preservation_intent:
                    score += 10
                if has_structural_replacement_intent:
                    score -= 40
                if has_aggressive_edit_style:
                    score -= 20
                if has_subtractive_edit_intent:
                    score -= 15  # eraser lane, not relight

        if media_type == "image" and route.get("operation") == "generate":
            route_id_value = route.get("route_id", "")

            # GPT Image 2 is now the quality-first default. Nano Banana 2 stays the
            # fast/cost-effective workhorse for explicit balanced or iteration asks.
            if route_id_value == "image-gpt-image-2-quality":
                score += 24
                if requested.get("goal") == "balanced":
                    score -= 32
                if requested.get("goal") == "best_quality":
                    score += 28
                if has_premium_hero_intent:
                    score += 26

            if route_id_value == "image-balanced-premium":
                score += 12
                if has_premium_hero_intent:
                    score -= 30
                if requested.get("goal") == "best_quality":
                    score -= 25
                if requested.get("goal") == "balanced":
                    score += 30

            if route_id_value == "image-default-best-quality":
                if has_premium_hero_intent:
                    score += 40
                if requested.get("goal") == "best_quality":
                    score += 35
                if requested.get("goal") == "balanced":
                    score -= 35

        if media_type == "image" and route.get("operation") == "edit":
            route_id_value = route.get("route_id", "")

            if route_id_value == "image-conservative-edit":
                if has_layout_preservation_intent:
                    score += 10
                if has_subtractive_edit_intent and not has_aggressive_edit_style:
                    score += 16
                if has_localized_safe_edit_intent and not has_aggressive_edit_style:
                    score += 12
                if strict_preservation_required:
                    score += 100
                if has_structural_replacement_intent:
                    score -= 28
                if has_aggressive_edit_style:
                    score -= 18

            if route_id_value == "image-high-end-edit":
                if has_structural_replacement_intent:
                    score += 24
                if has_aggressive_edit_style:
                    score += 18
                if has_layout_preservation_intent:
                    score += 4
                if has_subtractive_edit_intent and has_layout_preservation_intent:
                    score -= 16
                if strict_preservation_required:
                    score -= 100

            if route_id_value == "image-strong-lookdev-edit":
                if requested.get("goal") == "best_quality":
                    score += 40
                if has_premium_edit_intent:
                    score += 34
                if (
                    has_relight_intent
                    and not strict_preservation_required
                    and (has_premium_edit_intent or requested.get("goal") == "best_quality")
                ):
                    score += 10
                if has_layout_preservation_intent:
                    score += 6
                if has_subtractive_edit_intent:
                    score -= 30
                if has_structural_replacement_intent:
                    score -= 10
                if strict_preservation_required:
                    score -= 100

            if route_id_value == "image-multi-reference-aesthetic-edit":
                if has_aggressive_edit_style:
                    score += 16
                if has_structural_replacement_intent:
                    score += 10
                if strict_preservation_required:
                    score -= 100

        if media_type == "video":
            route_id_value = route.get("route_id", "")

            if route_id_value == "video-enhance-upscale":
                if has_video_enhance_intent:
                    score += 80
                if requested.get("operation") == "edit" and requested.get("goal") == "best_quality":
                    score += 24

            if route_id_value in {"video-remix-v2v", "video-extend"} and has_video_enhance_intent:
                score -= 45

        score -= index

        if best_score is None or score > best_score:
            best_score = score
            best_route = route

    if best_route is None:
        raise ValueError(
            f"No route matched media_type='{media_type}' with input_shape='{inferred_shape}'"
        )

    return best_route


def resolve_route_selection(
    media_type: str,
    *,
    prompt: str = "",
    params: dict | None = None,
    route_id: str = "",
    requested: dict | None = None,
) -> dict:
    route = select_route(
        media_type,
        prompt=prompt,
        params=params,
        route_id=route_id,
        requested=requested,
    )
    validate_route_constraints(
        media_type,
        route,
        prompt=prompt,
        params=params,
        requested=requested,
    )

    model_key = route["model_key"]
    provider = route["provider"]
    model_config = PIAPI_MODEL_MAP.get(model_key)
    task_type = model_config["task_type"] if model_config else ""

    return {
        "route_id": route["route_id"],
        "provider": provider,
        "model_key": model_key,
        "task_type": task_type,
        "route": route,
    }
