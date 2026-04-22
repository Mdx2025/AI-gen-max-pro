# Changelog

## 2026-04-21

### Added

- Added GPT Image 2 / ChatGPT Images 2.0 as the default quality-first image route.
- Added first-class GPT Image 2 edit routing through fal.ai.
- Added route coverage for balanced image iteration, premium fallback, and lookdev edit decisions.
- Added regression tests for GPT Image 2 default routing, edit endpoint mapping, balanced fallback routing, and premium lookdev routing.

### Changed

- Promoted `gpt-image-2` to the default image model.
- Kept `nano-banana-2` as the balanced / fast-iteration image lane.
- Kept `nano-banana-pro` as the premium fallback and Nano Banana-specific style lane.
- Updated prompt compilation so GPT Image 2 uses the GPT Image prompt-adherence adapter.
- Normalized GPT Image 2 parameters such as `aspect_ratio`, `quality`, and edit image inputs.
- Regenerated `SKILL.md`, `references/model-catalog.md`, `references/routing-table.md`, and `references/routing-schema.md`.

## 2026-04-20

### Added

- Added a model-aware prompt compiler that runs after route selection.
- Added prompt adapters for Nano Banana, GPT Image, Ideogram, Recraft vector, FLUX/Kontext edit lanes, Kling, Seedance, Sora, Veo, and specialist video routes.
- Added an intent recipe layer for product heroes, poster typography, social marketing, character consistency, conservative product edits, lookdev polish, cinematic video, UGC video, product commercials, physics realism, reference-driven motion, lipsync, storyboards, and video extension.
- Added execution traces for raw prompts, compiled prompts, compiler strategies, and recipe choices.

### Changed

- Separated routing from prompt shaping so prompt formatting cannot silently change the selected lane.
- Added pass-through behavior for already structured prompts.
- Bypassed prompt compilation for strict inpaint routes.

## 2026-04-19

### Added

- Added route confidence scoring and richer route traces.
- Added explicit input-shape and fidelity-priority signals.
- Added stricter validation for exact-layout preservation and conservative edit requests.

### Fixed

- Fixed cases where preservation-sensitive edits could be treated as flexible restyles.
- Fixed unsafe route pins when the requested operation required strict preservation.

## 2026-04-18

### Added

- Added strict preservation enforcement for image edit routes.
- Added HD-equivalent image delivery guard.
- Added image upscale fallback behavior when a generated image is below the minimum delivery size.
- Added failure-pattern documentation for route choices that are valid on paper but poor in practice.

### Fixed

- Fixed local media reference handling for provider uploads.
- Fixed output extension selection for video upscale routes.

## 2026-04-17

### Added

- Added schema-driven routing based on `media_type`, `operation`, `goal`, `input_shape`, `fidelity_priority`, `audio_requirement`, and `provider_preference`.
- Added executable route selection in `scripts/generate.py`.
- Added generated routing schema and routing table references.

### Changed

- Moved route truth into `scripts/model_manifest.py`.
- Kept provider and model overrides available only when explicitly requested.

## 2026-04-16

### Added

- Initial public skill structure.
- Added provider/model manifest.
- Added fal.ai, PiAPI, Together.ai, and Runware execution support.
- Added model catalog generation.
- Added routes for image generation, image edits, text-to-video, image-to-video, reference-to-video, video remix, video extension, video upscale, lipsync, vector output, and media utility tasks.
