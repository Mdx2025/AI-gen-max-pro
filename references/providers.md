# AI GEN MAX — Provider API Reference

> Source of truth for model routing/defaults: `scripts/model_manifest.py`
> This file is operational reference only; do not edit it to change routing behavior.

Quick reference for each provider's API format, auth, and async patterns.

---

## fal.ai

**Auth:** `Authorization: Key {FAL_API_KEY}`
**Pattern:** Async queue — submit → poll status → fetch result
**Env key:** `FAL_API_KEY`

### Submit
```
POST https://queue.fal.run/{model_id}
→ {"request_id": "abc123"}
```
### Poll
```
GET https://queue.fal.run/{model_id}/requests/{request_id}/status
→ {"status": "IN_QUEUE" | "IN_PROGRESS" | "COMPLETED" | "FAILED"}
```
### Result
```
GET https://queue.fal.run/{model_id}/requests/{request_id}
→ {images:[...], video:{...}, audio:{...}, model_mesh:{...}}
```

### Key models
| Use | Model ID | Cost |
|-----|----------|------|
| Image budget | `fal-ai/flux/schnell` | $0.003/MP |
| Image standard | `fal-ai/flux/dev` | $0.025/MP |
| Image default / premium | `fal-ai/nano-banana-2` | $0.08/img |
| Image premium | `fal-ai/nano-banana-pro` | $0.15/img |
| Video default T2V | `fal-ai/kling-video/v3/standard/text-to-video` | $0.084/s |
| Video default I2V | `fal-ai/kling-video/v3/standard/image-to-video` | $0.084/s |
| Video cinematic | `bytedance/seedance-2.0/text-to-video` | $0.30/s |
| Video multi-reference | `bytedance/seedance-2.0/reference-to-video` | $0.3024/s + token cost |
| Video physics | `fal-ai/sora-2/text-to-video` | $0.10/s |
| Video remix / V2V | `fal-ai/sora-2/video-to-video/remix` | see fal |
| Video 4K fast | `fal-ai/veo3.1/fast` | $0.10/s 720p/1080p, $0.30/s 4k |
| Video reference | `fal-ai/veo3.1/reference-to-video` | see fal |
| Video first+last frame | `fal-ai/veo3.1/first-last-frame-to-video` | see fal |
| Video extend | `fal-ai/veo3.1/extend-video` | see fal |
| Video long I2V | `fal-ai/framepack` | $0.033/s |
| Video social / stylized I2V | `fal-ai/pixverse/v6/image-to-video` | $0.025-$0.115/s |
| Video transition | `fal-ai/pixverse/v6/transition` | $0.025-$0.115/s |
| Video extension (PixVerse) | `fal-ai/pixverse/extend` | see fal |
| Aesthetic image | `xai/grok-imagine-image` | see fal |
| Aesthetic image edit | `xai/grok-imagine-image/edit` | see fal |
| Aesthetic video T2V/I2V | `xai/grok-imagine-video/text-to-video` / `xai/grok-imagine-video/image-to-video` | see fal |
| Dedicated lipsync | `fal-ai/sync-lipsync/v3` | see fal |
| Avatar talking | `bytedance/omnihuman/v1.5` | $0.13/s |
| Music full | `fal-ai/diffrhythm` | ~$0.285/song |
| Music flexible | `fal-ai/ace-step` | $0.0002/s |
| TTS | `fal-ai/f5-tts` | $0.05/1k |
| 3D image | `fal-ai/trellis` | $0.02/gen |
| 3D HD | `fal-ai/trellis-2` | ~$0.10/gen |
| Remove BG | `fal-ai/birefnet` | pay-per-compute |
| Upscale image | `fal-ai/clarity-upscaler` | $0.03/MP |
| Add audio to video | `fal-ai/mmaudio-v2` | $0.001/s |
| High-end image edit | `fal-ai/bytedance/seedream/v4.5/edit` | see fal |
| Cost-efficient image edit | `fal-ai/wan/v2.7/edit` | see fal |

---

## PiAPI

**Auth:** `x-api-key: {PIAPI_API_KEY}`
**Pattern:** Async task — submit → poll
**Env key:** `PIAPI_API_KEY`

### Submit
```
POST https://api.piapi.ai/api/v1/task
{"model": "...", "task_type": "...", "input": {...}}
→ {"code": 200, "data": {"task_id": "xyz"}}
```
### Poll
```
GET https://api.piapi.ai/api/v1/task/{task_id}
→ {"data": {"status": "completed", "output": {...}}}
```

### Key models
| Use | model | task_type |
|-----|-------|-----------|
| Flux Dev | `Qubico/flux1-dev` | `txt2img` |
| Flux Schnell | `Qubico/flux1-schnell` | `txt2img` |
| Kling video | `kling` | `video_generation` |
| Luma video | `luma` | `video_generation` |
| Udio music | `music-u` | `generate_music` |
| Trellis text/image 3D | `Qubico/trellis` | `text-to-3d` / `image-to-3d` |

**Output fields:** `output.image_url`, `output.video_url`, `output.audio_url`

---

## Together.ai

**Auth:** `Authorization: Bearer {TOGETHER_API_KEY}`
**Pattern:** Image = sync | Video = async job
**Env key:** `TOGETHER_API_KEY`

### Image (sync)
```
POST https://api.together.xyz/v1/images/generations
{"model": "...", "prompt": "...", "width": 1024, "height": 576}
→ {"data": [{"url": "https://..."}]}
```
### Video (async)
```
POST https://api.together.xyz/v1/videos/generations
{"model": "...", "prompt": "...", "duration": 5, "aspect_ratio": "16:9"}
→ {"id": "job123", "status": "queued"}

GET https://api.together.xyz/v1/videos/generations/{job_id}
→ {"status": "completed", "url": "https://..."}
```

### Key models
| Use | Model ID | Cost |
|-----|----------|------|
| Video budget | `black-forest-labs/seedance-1-lite` | $0.14/5s |
| Video Veo 3 | `google/veo-3-fast` | $0.80/8s |

---

## Runware

**Auth:** `Authorization: Bearer {RUNWARE_API_KEY}`
**Pattern:** Synchronous array payload
**Env key:** `RUNWARE_API_KEY`

### Image inference
```
POST https://api.runware.ai/v1
[{
  "taskType": "imageInference",
  "taskUUID": "unique-uuid",
  "model": "runware:100@1",
  "positivePrompt": "...",
  "width": 1024, "height": 576,
  "numberResults": 1, "outputFormat": "PNG",
  "steps": 4, "CFGScale": 1
}]
→ {"data": [{"imageURL": "https://..."}]}
```

### Key models
| Model | ID | Steps | CFGScale |
|-------|----|-------|---------|
| Flux Schnell | `runware:100@1` | 4 | 1 |
| Flux Dev | `runware:97@1` | 28 | 3.5 |

---

## Config file: ~/.openclaw/ai-gen-max.env

```
FAL_API_KEY=
PIAPI_API_KEY=
TOGETHER_API_KEY=
RUNWARE_API_KEY=
KIE_API_KEY=
```

Add a key and the corresponding provider becomes available.
