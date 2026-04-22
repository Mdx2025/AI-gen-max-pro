# AI GEN MAX — Routing Table

Source of truth for live model IDs/defaults/schema: `scripts/model_manifest.py`

Operator-facing summary generated from the manifest on **2026-04-21**.

## Routing posture

- Keep `gpt-image-2` as the default quality-first image lane when the job is general image generation and the target is the strongest possible output.
- Keep `nano-banana-2` as the fast workhorse when the job values iteration speed/cost over the quality ceiling.
- Keep `kling` as the default text-to-video lane when the job is general motion with no specialist constraint.
- Upgrade to specialist lanes only when the brief has a clear constraint: typography, vector, preserve-layout edit, multi-reference direction, physics realism, stylized social motion, lipsync, or utility tooling.
- Prefer explicit route IDs over hand-wavy "best model" language. The schema exists to turn intent into a repeatable choice, not to debate vibes every time.

## Image routing

| Goal / lane | model key | input shape | Primary trigger |
| --- | --- | --- | --- |
| preserve_layout | `bria-eraser` | `single_image` | Subtractive edits where canvas, framing, and composition must stay pixel-identical.; The caller has (or can provide) a mask_url marking the exact region to modify. |
| best_quality | `gpt-image-2` | `none` | Default quality-first image generation lane after GPT Image 2 / ChatGPT Images 2.0 became available on fal.; You want top public-model quality, photorealism, text rendering, UI/layout logic, product photography, or strongest prompt adherence. |
| prompt_adherence | `gpt-image-1.5` | `none` | You explicitly want GPT Image 1.5 high quality through fal.; You need the older GPT Image 1.5 behavior for comparison or compatibility. |
| balanced | `nano-banana-2` | `none` | Workhorse lane for fast/cost-sensitive image generation and batch creative iteration.; Fast iteration on creative direction with short feedback loops. |
| best_quality | `gpt-image-2` | `none` | Hero images for print campaigns or high-value brand assets where top public-model quality matters.; Complex multi-element compositions with strict spatial relationships. |
| flux_max | `flux-2-max` | `none` | You explicitly want FLUX.2 [max] generation, not the edit lane.; The brief wants maximum-quality FLUX.2 output for text-to-image. |
| production_consistency | `flux-2-pro` | `none` | You want FLUX.2 [pro] for zero-config professional generation and more predictable batch consistency.; Production consistency matters more than the extra push of the max lane. |
| 4k_ready | `seedream-v4` | `none` | You explicitly want Seedream 4.0 generation through fal.; 4K-ready sizing and the Seedream v4 generation profile matter for the brief. |
| vector | `recraft-v4-vector` | `none` | The request mentions logo, icon, vector, SVG, brand mark, packaging system, or design-kit style work.; Clean shapes and design-system controllability matter more than photographic realism. |
| typography | `ideogram-v3` | `none` | The image must contain readable text.; Posters, banners, ads, or title cards where lettering is part of the output, not an afterthought. |
| preserve_layout | `flux-kontext-pro` | `single_image` | The user wants the source image mostly unchanged except for targeted edits.; Composition, framing, product placement, or subject identity should stay stable. |
| best_quality | `gpt-image-2` | `single_image` | The user wants a stronger polish pass on an existing image without asking for a net-new composition.; Solid lookdev passes: cinematic grading, richer lighting, realistic reflections, better materials, product-commercial finish. |
| relight | `iclight-v2` | `single_image` | The user wants to change lighting, shadows, reflections, or ambience without altering composition or content.; Requests like 'add window shadow', 'add rim light', 'reiluminar', 'sombra de ventana', 'cinematic relight'. |
| restyle | `seedream-edit` | `single_image` | You need a flexible reference-guided restyle, not just a conservative patch or lookdev polish.; The user wants stronger visual reinterpretation while still starting from an existing image. |
| balanced | `wan27-edit` | `single_image` | The request needs image editing coverage at lower cost.; You want a cheaper fallback behind Seedream/Kontext. |
| stylized | `grok-imagine` | `none` | The prompt is taste-first: fashion, moodboard, stylized premium, aesthetic-heavy work.; The user wants more vibe and taste than strict brand/system control. |
| restyle | `grok-imagine-edit` | `multi_image` | The edit uses multiple input images to transfer mood or aesthetic.; You need an aesthetic-first edit lane instead of conservative preservation. |

## Video routing

| Goal / lane | model key | input shape | Primary trigger |
| --- | --- | --- | --- |
| balanced | `kling` | `none` | General text-to-video with no specialist need.; You need the best default value lane for human subjects, motion, and broad prompt coverage. |
| cinematic | `seedance2` | `none` | Product shots, creative direction, cinematic control, or material-forward motion work.; The user values directed composition over cheap generic motion. |
| cinematic | `seedance2-reference` | `multi_image` | The user provides multiple references and expects the model to respect them.; You need a composition-directed lane, not generic I2V. |
| physics | `sora2` | `none` | The prompt depends on physical interaction, gravity, fluids, collisions, or realistic dynamics.; You need realism more than stylization or cost efficiency. |
| restyle | `sora2-remix` | `video_only` | The user says remix, restyle, reinterpret this clip, or preserve motion but change look.; You need V2V, not T2V or I2V. |
| best_quality | `video-upscale` | `video_only` | The user wants to improve the same rendered video rather than generate new motion.; Technical cleanup: upscale, denoise, sharpen, deblur, reduce compression artifacts, or improve perceived quality. |
| best_quality | `veo3` | `none` | The request explicitly wants ultra/high-end quality, 4K-ish positioning, or broadcast-grade polish.; You need top-end output but want the faster Veo lane first. |
| best_quality | `veo3-hq` | `none` | The user wants maximum Veo quality over speed.; You already know the brief justifies the most expensive/high-end route. |
| best_quality | `veo3-ref` | `multi_image` | You need Veo-class output while steering from reference imagery.; The job needs stronger quality than Seedance reference can justify. |
| preserve_layout | `veo3-first-last` | `first+last_frame` | The brief provides a first frame and a destination last frame.; You need controlled interpolation between two endpoints. |
| preserve_layout | `veo3-extend` | `video_only` | The user says continue this clip, extend this video, or add more seconds without changing the core shot. |
| social | `pixverse-v6-i2v` | `single_image` | Stylized/social-native animation, viral motion, anime-ish movement, or trend-oriented content.; You care more about punchy motion language than physical realism. |
| social | `pixverse-transition` | `first+last_frame` | The task is an image-to-image transition clip for reels or stylized motion posts. |
| stylized | `grok-video` | `none` | The brief is taste-first and aesthetic-heavy rather than realism-first.; You want xAI's stylized signature on video. |
| stylized | `grok-video-ref` | `multi_image` | Stylized video generation steered by reference images. |
| preserve_layout | `sync-lipsync` | `video+audio` | You need a person/character to speak to provided audio.; Dedicated lipsync beats overloading general video lanes. |

## Decision heuristics

- `logo`, `icon`, `brand`, `svg`, `vector` -> `recraft-v4-vector`
- `poster`, `headline`, `banner`, `text in image`, `typography` -> `ideogram-v3`
- `preserve layout`, `same framing`, `small edit`, `keep composition`, `remove object but keep framing` -> `flux-kontext-pro`
- `formato original`, `encuadre original`, `no toques X`, `solo cambia la textura/fondo/plataforma` -> strict preservation lane only
- `remove/delete/erase` + exact composition preservation -> conservative edit or inpaint semantics, not taste-first restyle
- general best-looking image with no specialist constraint -> `gpt-image-2`
- `fashion`, `stylized premium`, `taste-first`, `mood` -> `grok-imagine`
- general text-to-video -> `kling`
- `product`, `materials`, `cinematic direction` -> `seedance2`
- `multi reference video` -> `seedance2-reference`
- `physics`, `fluid`, `gravity`, `collision` -> `sora2`
- `remix this clip`, `video-to-video`, `restyle this video` -> `sora2-remix`
- `4k`, `ultra`, `broadcast`, `highest-end` -> `veo3` or `veo3-hq`
- `first and last frame` -> `veo3-first-last`
- `continue this video`, `extend clip` -> `veo3-extend`
- `stylized social`, `viral`, `anime motion` -> `pixverse-v6-i2v`
- `transition reel` -> `pixverse-transition`
- `lipsync`, `dub`, `make them talk` -> `sync-lipsync`

## Notes on evidence

- Official fal docs remain the source of truth for endpoint existence and request shape.
- External benchmark/editorial sources can inform lane positioning, but they should not override confirmed endpoint capabilities.
- If a route is not in `ROUTING_SCHEMA`, it is not a first-class routing recommendation yet.
