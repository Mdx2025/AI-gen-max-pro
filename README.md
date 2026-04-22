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

See:

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
