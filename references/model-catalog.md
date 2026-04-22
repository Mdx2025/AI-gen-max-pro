# AI GEN MAX — Model Catalog

Generated from `scripts/model_manifest.py`.
Validated against official `fal.ai` docs on **2026-04-21**.

## Current invariants

- Default image model: **GPT Image 2 / ChatGPT Images 2.0** (`gpt-image-2`)
- Default image endpoint: `fal-ai/gpt-image-2`
- `sora2` standard and `sora2-pro` do **not** share the same fal endpoint.

## Image

| Model | model key | fal model ID | Price | Primary lane |
| --- | --- | --- | --- | --- |
| GPT Image 2 / ChatGPT Images 2.0 | `gpt-image-2` | `fal-ai/gpt-image-2` | $0.01-$0.41/img | DEFAULT quality-first image lane — stronger photorealism, text rendering, UI/layout, product shots, and prompt adherence than GPT Image 1.5 / Nano Banana family |
| Nano Banana 2 | `nano-banana-2` | `fal-ai/nano-banana-2` | $0.08/img | Workhorse — fast iteration, social/marketing, batch generation, and cost-sensitive creative exploration |
| Nano Banana Pro | `nano-banana-pro` | `fal-ai/nano-banana-pro` | $0.15/img | Premium fallback for the Nano Banana look; useful when GPT Image 2 is unavailable or the brief prefers Gemini/Nano Banana behavior |
| GPT Image 1.5 | `gpt-image-1.5` | `fal-ai/gpt-image-1.5` | $0.133/img @ 1024 high + tokens | Benchmark-leading prompt adherence and text rendering; supports low/medium/high quality tiers |
| FLUX.2 Pro | `flux-2-pro` | `fal-ai/flux-2-pro` | $0.030/MP | Zero-config professional text-to-image generation with strong consistency |
| FLUX.2 Max | `flux-2-max` | `fal-ai/flux-2-max` | $0.070/MP | Highest-quality FLUX.2 text-to-image generation |
| Seedream 4.0 | `seedream-v4` | `fal-ai/bytedance/seedream/v4/text-to-image` | $0.03/img | Seedream 4.0 generation, 4K-ready sizing, unified generation/edit architecture |
| Recraft V4 Vector | `recraft-v4-vector` | `fal-ai/recraft/v4/text-to-vector` | $0.08/img | DEFAULT vector/SVG — production-ready scalable graphics (logos, icons, brand marks) |
| Recraft V4 | `recraft-v4` | `fal-ai/recraft/v4/text-to-image` | $0.04/img | Raster design — V4 improves design taste, composition, color cohesion vs V3 |
| Recraft V4 Pro | `recraft-v4-pro` | `fal-ai/recraft/v4/pro/text-to-image` | $0.25/img | Pro raster — 2048x2048, finer detail for print/large-scale |
| Recraft V3 | `recraft-v3` | `fal-ai/recraft/v3/text-to-image` | $0.04/img | Legacy raster fallback |
| Ideogram V3 | `ideogram-v3` | `fal-ai/ideogram/v3` | $0.04/img | DEFAULT typography — same 90-95% text accuracy as V2 + style reference + better spatial composition |
| Ideogram V2 | `ideogram-v2` | `fal-ai/ideogram/v2/text-to-image` | $0.04/img | Legacy typography fallback |
| FLUX.2 Max Edit | `flux-2-max-edit` | `fal-ai/flux-2-max/edit` | $0.07/MP first + $0.03/MP additional | Fallback single-image edit lane for solid polish and better realism on existing compositions |
| Seedream V4.5 Edit | `seedream-edit` | `fal-ai/bytedance/seedream/v4.5/edit` | see fal | Flexible restyle/reference edit; avoid for blur-sensitive premium polish of an existing composition |
| Grok Imagine Image | `grok-imagine` | `xai/grok-imagine-image` | see fal | Aesthetic image generation |
| Grok Imagine Image Edit | `grok-imagine-edit` | `xai/grok-imagine-image/edit` | see fal | Multi-image aesthetic edit |
| Flux Dev Advanced | `flux-dev-advanced` | `fal-ai/flux/dev` | $0.025/MP | Standard / technical illustration |
| Flux Schnell | `flux-schnell` | `fal-ai/flux/schnell` | $0.003/MP | Budget |

## Video

| Model | model key | fal model ID | Price | Primary lane |
| --- | --- | --- | --- | --- |
| Kling 3.0 | `kling` | `fal-ai/kling-video/v3/standard/text-to-video` | $0.084/s | DEFAULT |
| Seedance 2.0 | `seedance2` | `bytedance/seedance-2.0/text-to-video` | $0.30/s | Cinematic / product |
| Seedance 2.0 Reference | `seedance2-reference` | `bytedance/seedance-2.0/reference-to-video` | $0.3024/s + token cost | Multi-reference direction |
| Sora 2 | `sora2` | `fal-ai/sora-2/text-to-video` | $0.10/s | Physics realism |
| Sora 2 Pro | `sora2-pro` | `fal-ai/sora-2/text-to-video/pro` | $0.30/s 720p \| $0.50/s 1080p | Extended duration + native audio |
| Sora 2 Remix | `sora2-remix` | `fal-ai/sora-2/video-to-video/remix` | see fal | Video-to-video creative remix |
| Veo 3.1 Fast | `veo3` | `fal-ai/veo3.1/fast` | $0.10/s 720p/1080p \| $0.30/s 4k | Ultra / fast |
| Veo 3.1 Extend | `veo3-extend` | `fal-ai/veo3.1/extend-video` | see fal | Continue generated video; not a true video enhancer |
| PixVerse V6 I2V | `pixverse-v6-i2v` | `fal-ai/pixverse/v6/image-to-video` | $0.025-$0.115/s | Stylized motion / social |
| PixVerse Transition | `pixverse-transition` | `fal-ai/pixverse/v6/transition` | $0.025-$0.115/s | Image transition clip |
| PixVerse Extend | `pixverse-extend` | `fal-ai/pixverse/extend` | see fal | Video extension |
| Grok Imagine Video | `grok-video` | `xai/grok-imagine-video/text-to-video` | see fal | Stylized T2V |
| Grok Imagine Video I2V | `grok-video-i2v` | `xai/grok-imagine-video/image-to-video` | see fal | Image-guided stylized video |
| Grok Imagine Video Ref | `grok-video-ref` | `xai/grok-imagine-video/reference-to-video` | see fal | Reference-image video |
| Sync Lipsync v3 | `sync-lipsync` | `fal-ai/sync-lipsync/v3` | see fal | Dedicated lipsync |

## Official references

- Nano Banana Pro: https://fal.ai/models/fal-ai/nano-banana-pro
- Nano Banana 2: https://fal.ai/models/fal-ai/nano-banana-2
- GPT Image 2 / ChatGPT Images 2.0: https://fal.ai/gpt-image-2
- FLUX.1 [dev]: https://fal.ai/models/fal-ai/flux/dev
- Sora 2 text-to-video: https://fal.ai/models/fal-ai/sora-2/text-to-video
- Sora 2 Pro text-to-video: https://fal.ai/models/fal-ai/sora-2/text-to-video/pro
