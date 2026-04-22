# AI GEN MAX

AI GEN MAX is an OpenClaw skill for routing AI media generation requests to the right model and provider.

It is built for agents that need to generate or edit images, video, audio, music, 3D assets, or media utility outputs without hardcoding a single provider or guessing which model should be used.

The skill does three jobs:

- Classifies the user's media request by type, operation, goal, references, and fidelity constraints.
- Selects a defensible route from a manifest of supported providers and models.
- Shapes the prompt for the selected lane without changing the routing decision.

No API keys are included in this repository. It is BYOK: bring your own provider keys.

## What It Does

- Image generation and editing
- Conservative image edits where layout preservation matters
- Mask/inpaint style routing for strict localized edits
- Text-to-video, image-to-video, reference-to-video, video remix, video extend, and video upscale routes
- Prompt compilation for image and video families
- Model catalog and routing docs generated from one manifest
- Lightweight regression tests for routing behavior

## Why It Exists

Media models change quickly. New models appear, pricing shifts, and providers expose overlapping capabilities.

Without a routing layer, agents tend to:

- pick models by hype instead of task constraints
- use a generative model when a conservative edit lane is safer
- confuse "highest quality" with "highest variance"
- lose track of provider-specific parameters

AI GEN MAX centralizes those decisions in `scripts/model_manifest.py` and keeps docs generated from that source of truth.

## Current Defaults

- Default image lane: `gpt-image-2` via `fal-ai/gpt-image-2`
- Balanced image iteration: `nano-banana-2`
- Premium fallback / Nano Banana look: `nano-banana-pro`
- Conservative edits: `flux-kontext-pro`
- Default text-to-video lane: `kling`
- Premium video lanes: `sora2`, `sora2-pro`, `veo3`, `veo3-hq`

## Full Model Inventory

This is the visible inventory of currently mapped models. The generated source of truth is `references/model-catalog.md`; execution truth lives in `scripts/model_manifest.py`.

### Image Models

| Category / intent | model key | Provider endpoint | Current role |
| --- | --- | --- | --- |
| Default quality-first image | `gpt-image-2` | `fal-ai/gpt-image-2` | Default for best public-model image quality, photorealism, UI/layout logic, product photography, text rendering, and prompt adherence. |
| Balanced image workhorse | `nano-banana-2` | `fal-ai/nano-banana-2` | Fast iteration, social/marketing assets, batch creative exploration, and cost-sensitive image generation. |
| Premium Nano Banana fallback | `nano-banana-pro` | `fal-ai/nano-banana-pro` | Premium fallback when the brief wants Nano Banana/Gemini behavior or GPT Image 2 is unavailable. |
| Legacy GPT comparison | `gpt-image-1.5` | `fal-ai/gpt-image-1.5` | Older GPT Image behavior for compatibility, comparison, and explicit prompt-adherence tests. |
| FLUX consistency | `flux-2-pro` | `fal-ai/flux-2-pro` | Zero-config professional generation and predictable batch consistency. |
| FLUX maximum quality | `flux-2-max` | `fal-ai/flux-2-max` | Maximum-quality FLUX.2 text-to-image generation. |
| Seedream generation | `seedream-v4` | `fal-ai/bytedance/seedream/v4/text-to-image` | 4K-ready Seedream 4.0 generation. |
| Vector / branding | `recraft-v4-vector` | `fal-ai/recraft/v4/text-to-vector` | Default SVG/vector lane for logos, icons, brand marks, packaging systems, and scalable design assets. |
| Raster design | `recraft-v4` | `fal-ai/recraft/v4/text-to-image` | Raster design output with stronger taste, composition, and color cohesion. |
| Pro raster design | `recraft-v4-pro` | `fal-ai/recraft/v4/pro/text-to-image` | Higher-detail 2048x2048 raster design for print or large-scale needs. |
| Legacy raster fallback | `recraft-v3` | `fal-ai/recraft/v3/text-to-image` | Older Recraft fallback. |
| Typography / posters | `ideogram-v3` | `fal-ai/ideogram/v3` | Default typography lane for readable text, posters, banners, ads, and title cards. |
| Legacy typography fallback | `ideogram-v2` | `fal-ai/ideogram/v2/text-to-image` | Older typography fallback. |
| Conservative edit | `flux-kontext-pro` | `fal-ai/flux-pro/kontext` | Targeted edits where composition, framing, subject identity, and product placement should stay stable. |
| Strict inpaint / erase | `bria-eraser` | `fal-ai/bria/eraser` | Masked subtractive edits where the canvas must stay pixel-identical. |
| FLUX edit fallback | `flux-2-max-edit` | `fal-ai/flux-2-max/edit` | Single-image polish and realism fallback for existing compositions. |
| Flexible restyle/edit | `seedream-edit` | `fal-ai/bytedance/seedream/v4.5/edit` | Reference-guided restyle when conservative preservation is not the main constraint. |
| Relight | `iclight-v2` | fal relight lane | Lighting, shadows, reflections, ambience, and window-shadow style edits while preserving content. |
| Budget edit fallback | `wan27-edit` | `fal-ai/wan/v2.7/edit` | Lower-cost edit fallback behind Seedream/Kontext. |
| Aesthetic image | `grok-imagine` | `xai/grok-imagine-image` | Taste-first image generation for fashion, moodboard, stylized premium, or aesthetic-heavy work. |
| Aesthetic multi-image edit | `grok-imagine-edit` | `xai/grok-imagine-image/edit` | Multi-reference aesthetic edits and taste transfer. |
| Standard technical generation | `flux-dev-advanced` | `fal-ai/flux/dev` | Standard/technical illustration. |
| Budget image generation | `flux-schnell` | `fal-ai/flux/schnell` | Low-cost image generation. |

### Video Models

| Category / intent | model key | Provider endpoint | Current role |
| --- | --- | --- | --- |
| Default text-to-video | `kling` | `fal-ai/kling-video/v3/standard/text-to-video` | General T2V default for broad motion coverage. |
| Cinematic/product video | `seedance2` | `bytedance/seedance-2.0/text-to-video` | Product shots, material-forward motion, and directed cinematic composition. |
| Multi-reference video | `seedance2-reference` | `bytedance/seedance-2.0/reference-to-video` | Reference-driven composition and identity/style steering. |
| Physics realism | `sora2` | `fal-ai/sora-2/text-to-video` | Physical interaction, fluids, gravity, collisions, and realism-heavy prompts. |
| Premium video + audio | `sora2-pro` | `fal-ai/sora-2/text-to-video/pro` | Longer/premium Sora route with native audio support. |
| Video remix | `sora2-remix` | `fal-ai/sora-2/video-to-video/remix` | Video-to-video restyle/remix while preserving motion logic. |
| Ultra video fast lane | `veo3` | `fal-ai/veo3.1/fast` | High-end/broadcast-grade video route when quality matters and fast Veo is enough. |
| Maximum Veo quality | `veo3-hq` | Veo HQ lane | Highest-end Veo route when the brief justifies the expensive lane. |
| Veo reference video | `veo3-ref` | Veo reference lane | Veo-class output steered from reference imagery. |
| First/last-frame control | `veo3-first-last` | Veo first/last-frame lane | Controlled interpolation between a first frame and a destination frame. |
| Video extension | `veo3-extend` | `fal-ai/veo3.1/extend-video` | Continue an existing clip without changing core shot logic. |
| Social image-to-video | `pixverse-v6-i2v` | `fal-ai/pixverse/v6/image-to-video` | Stylized/social-native animation and trend-oriented motion. |
| Transition clips | `pixverse-transition` | `fal-ai/pixverse/v6/transition` | Image-to-image transition videos for reels and social posts. |
| PixVerse extension | `pixverse-extend` | `fal-ai/pixverse/extend` | PixVerse video extension fallback. |
| Stylized T2V | `grok-video` | `xai/grok-imagine-video/text-to-video` | Taste-first stylized video. |
| Stylized I2V | `grok-video-i2v` | `xai/grok-imagine-video/image-to-video` | Image-guided stylized video. |
| Stylized reference video | `grok-video-ref` | `xai/grok-imagine-video/reference-to-video` | Reference-image guided stylized video. |
| Lipsync | `sync-lipsync` | `fal-ai/sync-lipsync/v3` | Dedicated lipsync for video+audio tasks. |
| Video upscale/enhance | `video-upscale` | provider utility lane | Improve the same rendered clip: upscale, denoise, sharpen, deblur, or reduce compression artifacts. |

## Route Categories And Adjustments

These are the first-class routing categories exposed by the manifest.

### Image Route Categories

| Route category | Primary model key | What changed / why it matters |
| --- | --- | --- |
| `best_quality` | `gpt-image-2` | Default quality-first image generation moved to GPT Image 2. |
| `balanced` | `nano-banana-2` | Fast workhorse kept separate from hero-quality generation. |
| `prompt_adherence` | `gpt-image-1.5` | Legacy GPT route remains available for explicit comparison/compatibility. |
| `flux_max` | `flux-2-max` | Explicit FLUX.2 Max generation is separate from GPT Image 2 default. |
| `production_consistency` | `flux-2-pro` | Batch/brand consistency has its own route instead of being buried under generic quality. |
| `4k_ready` | `seedream-v4` | Seedream generation is positioned for 4K-ready output. |
| `vector` | `recraft-v4-vector` | Vector/logo/brand assets go to Recraft V4 Vector, not a raster model. |
| `typography` | `ideogram-v3` | Text-heavy images go to Ideogram V3. |
| `preserve_layout` | `flux-kontext-pro` / `bria-eraser` | Preservation language is treated as a hard constraint, not a style hint. |
| `relight` | `iclight-v2` | Lighting/shadow/reflection edits get a specialist route. |
| `restyle` | `seedream-edit` / `grok-imagine-edit` | Flexible restyle is separated from conservative edit safety. |
| `stylized` | `grok-imagine` | Taste-first imagery has a distinct lane. |

### Video Route Categories

| Route category | Primary model key | What changed / why it matters |
| --- | --- | --- |
| `balanced` | `kling` | Kling remains the default general T2V lane. |
| `cinematic` | `seedance2` / `seedance2-reference` | Product/cinematic and reference-driven work routes away from generic T2V. |
| `physics` | `sora2` | Physics-heavy realism gets Sora 2. |
| `best_quality` | `veo3`, `veo3-hq`, `veo3-ref`, `video-upscale` | High-end video, reference quality, and technical enhancement are separated. |
| `restyle` | `sora2-remix` | Video-to-video remix is distinct from generation and extension. |
| `preserve_layout` | `veo3-first-last`, `veo3-extend`, `sync-lipsync` | Controlled interpolation, extension, and lipsync preserve source constraints. |
| `social` | `pixverse-v6-i2v`, `pixverse-transition` | Social-native stylized motion gets its own lane. |
| `stylized` | `grok-video`, `grok-video-ref` | Taste-first video routes to Grok video lanes. |

Full generated docs:

- `references/model-catalog.md`
- `references/routing-table.md`
- `references/routing-schema.md`
- `references/providers.md`

## Repository Layout

```text
ai-gen-max/
├── SKILL.md
├── README.md
├── CHANGELOG.md
├── .env.example
├── scripts/
│   ├── generate.py
│   ├── model_manifest.py
│   ├── prompt_compiler.py
│   ├── render_docs.py
│   └── test_manifest.py
└── references/
    ├── failure-patterns.md
    ├── model-catalog.md
    ├── providers.md
    ├── routing-schema.md
    └── routing-table.md
```

## Install In OpenClaw

Clone this repository into your OpenClaw skills directory:

```bash
mkdir -p ~/.openclaw/skills
git clone https://github.com/Mdx2025/openclaw-ai-gen-max.git ~/.openclaw/skills/ai-gen-max
```

Verify that OpenClaw can see it:

```bash
openclaw skills check
```

If OpenClaw is already running, restart or reload the agent session so the skill catalog is refreshed.

## Configure Provider Keys

Create a local config file:

```bash
cp ~/.openclaw/skills/ai-gen-max/.env.example ~/.openclaw/ai-gen-max.env
```

Then fill only the providers you use:

```bash
FAL_API_KEY=your_fal_key_here
PIAPI_API_KEY=your_piapi_key_here
TOGETHER_API_KEY=your_together_key_here
RUNWARE_API_KEY=your_runware_key_here
KIE_API_KEY=your_kie_key_here
OPENAI_API_KEY=your_openai_key_here
```

You can also provide keys through environment variables. Environment variables override the config file.

Do not commit `.env`, `.env.*`, or `~/.openclaw/ai-gen-max.env`.

## Basic Usage

The skill is designed to be invoked by an agent when the user asks for media generation. The executor can also be called directly:

```bash
python3 scripts/generate.py '{
  "media_type": "image",
  "params": {
    "prompt": "Luxury editorial hero shot of a mechanical watch",
    "aspect_ratio": "16:9"
  },
  "routing": {
    "operation": "generate",
    "goal": "best_quality"
  }
}'
```

Direct route pin:

```bash
python3 scripts/generate.py '{
  "media_type": "image",
  "route_id": "image-conservative-edit",
  "params": {
    "prompt": "Keep the same framing and only change the bottle label",
    "image_url": "/absolute/path/source.png"
  }
}'
```

## Routing Contract

Preferred payload:

```json
{
  "media_type": "image",
  "params": {
    "prompt": "Luxury editorial hero shot of a watch",
    "aspect_ratio": "16:9"
  },
  "routing": {
    "operation": "generate",
    "goal": "best_quality"
  }
}
```

If the caller already knows the exact lane:

```json
{
  "media_type": "image",
  "route_id": "image-conservative-edit",
  "params": {
    "prompt": "Keep the same framing and only change the label",
    "image_url": "/absolute/path/source.png"
  }
}
```

Avoid passing `provider` or `model` unless the user explicitly requested an override. Let the route selector choose them.

## Preservation Safety

For edit requests, AI GEN MAX treats preservation language as a hard constraint.

Examples:

- "same framing"
- "keep the original format"
- "do not change the composition"
- "only remove this object"
- "do not touch the product"

When strict preservation is required, the router should choose a conservative edit or inpaint lane. If no available lane can satisfy the constraint, it should fail safely instead of choosing a prettier but unsafe generative lane.

## Development

Regenerate docs after changing the manifest:

```bash
python3 scripts/render_docs.py
```

Run routing tests:

```bash
python3 scripts/test_manifest.py
```

Optional syntax check:

```bash
python3 -m compileall scripts
```

## Security Notes

- This repository contains no API keys.
- API keys are loaded from `~/.openclaw/ai-gen-max.env` or environment variables.
- `.env` and `.env.*` are ignored by git.
- Generated media defaults to `~/.openclaw/media`.
- Local file references are uploaded to the selected provider only when the selected route requires remote media URLs.

## License

MIT. See `LICENSE`.
