# AI GEN MAX — Routing Schema

Canonical schema generated from `scripts/model_manifest.py`.
Validated / refreshed on **2026-04-21**.

## Decision dimensions

- `media_type`: image | video | audio | music | tts | 3d | tool
- `operation`: generate | edit | inpaint | outpaint | variation | remix | extend | lipsync | caption
- `goal`: best_quality | balanced | budget | typography | vector | cinematic | physics | social | preserve_layout | prompt_adherence | production_consistency | 4k_ready | flux_max
- `input_shape`: none | single_image | multi_image | image+audio | video+audio | first+last_frame | video_only
- `fidelity_priority`: preserve_subject | preserve_layout | restyle | create_net_new
- `audio_requirement`: none | optional | required
- `resolution_target`: hd | 1080p | 4k
- `latency_budget`: fast | standard | premium
- `cost_sensitivity`: low | medium | high
- `provider_preference`: fal | piapi | together | runware | auto

## Schema

## IMAGE

### `image-strict-inpaint`

- Model key: `bria-eraser`
- Provider: `fal`
- Resolved model/endpoint: `fal-ai/bria/eraser`
- Operation: `inpaint`
- Goal: `preserve_layout`
- Input shape: `single_image`
- Fidelity priority: `preserve_layout`
- Quality tier: `specialist`
- Use when:
  - Subtractive edits where canvas, framing, and composition must stay pixel-identical.
  - The caller has (or can provide) a mask_url marking the exact region to modify.
  - Requests like 'borra las cards', 'remove the logo', 'erase the text', with strict preservation intent.
- Avoid when:
  - The edit is aesthetic or structural — not a bounded subtraction.
  - No mask is available and no segmentation step is viable.
- Keywords: `inpaint`, `erase`, `eraser`, `mask`, `borra`, `borrar`, `elimina`, `solo quita`, `only remove`, `pixel-identical`
- Fallbacks: `flux-inpaint`, `flux-fill-pro`, `flux-kontext-pro`

### `image-gpt-image-2-quality`

- Model key: `gpt-image-2`
- Provider: `fal`
- Resolved model/endpoint: `fal-ai/gpt-image-2`
- Operation: `generate`
- Goal: `best_quality`
- Input shape: `none`
- Fidelity priority: `create_net_new`
- Quality tier: `ultra`
- Use when:
  - Default quality-first image generation lane after GPT Image 2 / ChatGPT Images 2.0 became available on fal.
  - You want top public-model quality, photorealism, text rendering, UI/layout logic, product photography, or strongest prompt adherence.
  - The prompt is text-only and the job values final quality more than speed/cost.
- Avoid when:
  - Fast iteration cost matters more than absolute prompt adherence.
  - You need a vector-specific lane or a more open-ended aesthetic model.
- Keywords: `gpt image 2`, `chatgpt images 2`, `chat gpt 2.0`, `chatgpt 2.0`, `prompt adherence`, `ui mockup`, `dense text`, `multilingual`, `benchmark leader`, `photorealism`, `product photography`
- Fallbacks: `nano-banana-pro`, `nano-banana-2`

### `image-gpt-image-1-5-high`

- Model key: `gpt-image-1.5`
- Provider: `fal`
- Resolved model/endpoint: `fal-ai/gpt-image-1.5`
- Operation: `generate`
- Goal: `prompt_adherence`
- Input shape: `none`
- Fidelity priority: `create_net_new`
- Quality tier: `premium`
- Use when:
  - You explicitly want GPT Image 1.5 high quality through fal.
  - You need the older GPT Image 1.5 behavior for comparison or compatibility.
- Avoid when:
  - You want the current best GPT Image lane; use GPT Image 2 instead.
  - Fast iteration cost matters more than absolute prompt adherence.
- Keywords: `gpt image 1.5`, `legacy gpt image`, `compare gpt image 1.5`
- Fallbacks: `nano-banana-pro`, `nano-banana-2`

### `image-balanced-premium`

- Model key: `nano-banana-2`
- Provider: `fal`
- Resolved model/endpoint: `fal-ai/nano-banana-2`
- Operation: `generate`
- Goal: `balanced`
- Input shape: `none`
- Fidelity priority: `create_net_new`
- Quality tier: `premium`
- Use when:
  - Workhorse lane for fast/cost-sensitive image generation and batch creative iteration.
  - Fast iteration on creative direction with short feedback loops.
  - Batch production (dozens to thousands of images) where cost/throughput matter.
  - Social media, marketing campaigns, web content, blog headers, product shots.
  - Real-time features, live previews, interactive editors.
- Avoid when:
  - The asset is a high-stakes hero image for print or a high-value brand deliverable.
  - The prompt demands camera-ready fine typography (packaging, magazine, signage).
  - Complex multi-element composition with strict spatial relationships that Pro handles better.
  - The request is vector/logo/brand-system oriented (use recraft-v4-vector).
  - The prompt's main requirement is readable text inside the image (use ideogram-v3).
- Keywords: `social`, `marketing`, `web`, `blog`, `iteration`, `iterate`, `batch`, `quick`, `fast`, `rapido`, `campaign`, `content`, `post`, `thumbnail`, `draft`, `concept`, `variation`, `explore`
- Fallbacks: `nano-banana-pro`, `flux-dev`

### `image-default-best-quality`

- Model key: `gpt-image-2`
- Provider: `fal`
- Resolved model/endpoint: `fal-ai/gpt-image-2`
- Operation: `generate`
- Goal: `best_quality`
- Input shape: `none`
- Fidelity priority: `create_net_new`
- Quality tier: `ultra`
- Use when:
  - Hero images for print campaigns or high-value brand assets where top public-model quality matters.
  - Complex multi-element compositions with strict spatial relationships.
  - Camera-ready fine typography, UI mockups, product labels, magazine layouts, or detailed signage.
  - Photorealism, product photography, and instruction-following matter more than speed.
  - User explicitly requests best possible quality, ultra fidelity, or editorial-grade output.
- Avoid when:
  - Fast iteration or batch work where cost/throughput matters — use nano-banana-2 instead.
  - Social media or web content where NB2's quality is indistinguishable at the target size.
  - The request is vector/logo/brand-system oriented.
- Keywords: `hero`, `hero shot`, `hero image`, `editorial`, `luxury`, `premium`, `print`, `magazine`, `packaging`, `camera-ready`, `camera ready`, `4k ultra`, `ultra fidelity`, `ultra quality`, `brutal`, `best quality`, `best possible quality`, `maxima calidad`, `máxima calidad`, `portada`, `campaign hero`, `flagship`
- Fallbacks: `nano-banana-pro`, `nano-banana-2`, `flux-dev`

### `image-flux-2-max-generate`

- Model key: `flux-2-max`
- Provider: `fal`
- Resolved model/endpoint: `fal-ai/flux-2-max`
- Operation: `generate`
- Goal: `flux_max`
- Input shape: `none`
- Fidelity priority: `create_net_new`
- Quality tier: `ultra`
- Use when:
  - You explicitly want FLUX.2 [max] generation, not the edit lane.
  - The brief wants maximum-quality FLUX.2 output for text-to-image.
- Avoid when:
  - You need the cheaper or more consistent FLUX.2 Pro lane instead.
- Keywords: `flux 2 max`, `flux.2 max`, `maximum-quality flux`, `max quality flux`
- Fallbacks: `flux-2-pro`, `nano-banana-pro`

### `image-flux-2-pro-generate`

- Model key: `flux-2-pro`
- Provider: `fal`
- Resolved model/endpoint: `fal-ai/flux-2-pro`
- Operation: `generate`
- Goal: `production_consistency`
- Input shape: `none`
- Fidelity priority: `create_net_new`
- Quality tier: `premium`
- Use when:
  - You want FLUX.2 [pro] for zero-config professional generation and more predictable batch consistency.
  - Production consistency matters more than the extra push of the max lane.
- Avoid when:
  - The brief specifically calls for GPT Image 1.5 or FLUX.2 Max.
- Keywords: `flux 2 pro`, `flux.2 pro`, `production consistency`, `zero-config quality`, `brand consistency`
- Fallbacks: `flux-2-max`, `nano-banana-pro`

### `image-seedream-v4-generate`

- Model key: `seedream-v4`
- Provider: `fal`
- Resolved model/endpoint: `fal-ai/bytedance/seedream/v4/text-to-image`
- Operation: `generate`
- Goal: `4k_ready`
- Input shape: `none`
- Fidelity priority: `create_net_new`
- Quality tier: `premium`
- Use when:
  - You explicitly want Seedream 4.0 generation through fal.
  - 4K-ready sizing and the Seedream v4 generation profile matter for the brief.
- Avoid when:
  - You want the newer Seedream 4.5 lane or a model with a stronger public benchmark signal.
- Keywords: `seedream 4`, `seedream 4.0`, `4k ready`, `seedream v4`
- Fallbacks: `seedream`, `nano-banana-2`

### `image-vector-branding`

- Model key: `recraft-v4-vector`
- Provider: `fal`
- Resolved model/endpoint: `fal-ai/recraft/v4/text-to-vector`
- Operation: `generate`
- Goal: `vector`
- Input shape: `none`
- Fidelity priority: `create_net_new`
- Quality tier: `specialist`
- Use when:
  - The request mentions logo, icon, vector, SVG, brand mark, packaging system, or design-kit style work.
  - Clean shapes and design-system controllability matter more than photographic realism.
  - Production-ready SVG output (scalable) is required.
- Avoid when:
  - The output should look photographic or cinematic.
  - The main challenge is typography rather than vector form.
- Keywords: `logo`, `icon`, `svg`, `vector`, `branding`, `packaging`, `brand mark`, `design system`
- Fallbacks: `recraft-v4`, `recraft-v3`, `ideogram-v3`

### `image-typography-poster`

- Model key: `ideogram-v3`
- Provider: `fal`
- Resolved model/endpoint: `fal-ai/ideogram/v3`
- Operation: `generate`
- Goal: `typography`
- Input shape: `none`
- Fidelity priority: `create_net_new`
- Quality tier: `specialist`
- Use when:
  - The image must contain readable text.
  - Posters, banners, ads, or title cards where lettering is part of the output, not an afterthought.
  - V3 adds style-reference and better spatial composition vs V2 while keeping 90-95% text accuracy.
- Avoid when:
  - The image is purely illustrative with no real text burden.
  - The user wants a vector/logo lane instead of raster poster work.
- Keywords: `poster`, `banner`, `headline`, `text in image`, `typography`, `ad creative`, `title card`
- Fallbacks: `ideogram-v2`, `recraft-v4`, `nano-banana-pro`

### `image-conservative-edit`

- Model key: `flux-kontext-pro`
- Provider: `fal`
- Resolved model/endpoint: `fal-ai/flux-pro/kontext`
- Operation: `edit`
- Goal: `preserve_layout`
- Input shape: `single_image`
- Fidelity priority: `preserve_layout`
- Quality tier: `specialist`
- Use when:
  - The user wants the source image mostly unchanged except for targeted edits.
  - Composition, framing, product placement, or subject identity should stay stable.
- Avoid when:
  - The user wants an aggressive aesthetic restyle.
  - The edit depends on multiple reference images or a taste-heavy reinterpretation.
  - The user wants to replace one visual language or object family with another.
- Keywords: `preserve layout`, `same framing`, `keep composition`, `subtle edit`, `conservative edit`
- Fallbacks: `seedream-edit`, `nano-banana-pro`

### `image-strong-lookdev-edit`

- Model key: `gpt-image-2`
- Provider: `fal`
- Resolved model/endpoint: `fal-ai/gpt-image-2`
- Operation: `edit`
- Goal: `best_quality`
- Input shape: `single_image`
- Fidelity priority: `preserve_subject`
- Quality tier: `ultra`
- Use when:
  - The user wants a stronger polish pass on an existing image without asking for a net-new composition.
  - Solid lookdev passes: cinematic grading, richer lighting, realistic reflections, better materials, product-commercial finish.
  - Fintech/luxury UI imagery where 'premium' means subtle controlled shadows, refined glass reflections, sharper material edges, and less generic glow.
  - The brief is edit-first and quality-first, but not a pixel-faithful patch or a full structural replacement.
- Avoid when:
  - The source layout must stay almost pixel-faithful.
  - The request is primarily subtractive, masked, or exact-preservation work.
  - The edit is a large structural replacement that fits Seedream or multi-reference aesthetic lanes better.
- Keywords: `cinematic`, `raytracing`, `ray tracing`, `lookdev`, `look dev`, `color grade`, `grading`, `grade`, `premium lighting`, `premium`, `luxury`, `fintech`, `subtle lighting`, `refined reflections`, `refined reflection`, `realistic reflections`, `product-commercial`, `product commercial`, `high-end`, `high end`, `photoreal polish`, `material realism`
- Fallbacks: `nano-banana-pro`, `flux-2-max-edit`, `flux-kontext-pro`, `seedream-edit`

### `image-relight`

- Model key: `iclight-v2`
- Provider: `fal`
- Resolved model/endpoint: `fal-ai/iclight-v2`
- Operation: `relight`
- Goal: `relight`
- Input shape: `single_image`
- Fidelity priority: `preserve_layout`
- Quality tier: `specialist`
- Use when:
  - The user wants to change lighting, shadows, reflections, or ambience without altering composition or content.
  - Requests like 'add window shadow', 'add rim light', 'reiluminar', 'sombra de ventana', 'cinematic relight'.
  - The canvas, framing, and subject identity must stay intact; only the light field changes.
- Avoid when:
  - The user wants to modify objects, textures, or layout — not just lighting.
  - The prompt is a generic edit without explicit lighting intent.
- Keywords: `relight`, `reiluminar`, `iluminacion`, `iluminación`, `sombra`, `sombras`, `shadow`, `shadows`, `reflejo`, `reflejos`, `reflection`, `reflections`, `window light`, `luz de ventana`, `sombra de ventana`, `cinematic lighting`, `studio light`, `rim light`, `backlight`, `key light`
- Fallbacks: `flux-kontext-pro`, `seedream-edit`

### `image-high-end-edit`

- Model key: `seedream-edit`
- Provider: `fal`
- Resolved model/endpoint: `fal-ai/bytedance/seedream/v4.5/edit`
- Operation: `edit`
- Goal: `restyle`
- Input shape: `single_image`
- Fidelity priority: `preserve_subject`
- Quality tier: `premium`
- Use when:
  - You need a flexible reference-guided restyle, not just a conservative patch or lookdev polish.
  - The user wants stronger visual reinterpretation while still starting from an existing image.
- Avoid when:
  - The source layout must stay almost pixel-faithful.
  - The request is blur-sensitive fintech/luxury polish, subtle premium lighting, refined shadows, or glass/reflection cleanup on an existing composition; prefer image-strong-lookdev-edit.
  - The request is very budget-sensitive.
- Keywords: `restyle`, `premium edit`, `reference-guided`, `enhance aesthetic`, `replace`, `swap`, `instead of`, `wireframe`, `change particles`
- Fallbacks: `flux-kontext-pro`, `wan27-edit`

### `image-budget-edit`

- Model key: `wan27-edit`
- Provider: `fal`
- Resolved model/endpoint: `fal-ai/wan/v2.7/edit`
- Operation: `edit`
- Goal: `balanced`
- Input shape: `single_image`
- Fidelity priority: `preserve_subject`
- Quality tier: `budget`
- Use when:
  - The request needs image editing coverage at lower cost.
  - You want a cheaper fallback behind Seedream/Kontext.
- Avoid when:
  - The user is explicitly paying for top-tier edit quality.
  - You need the safest layout preservation.
- Keywords: `budget edit`, `cheap edit`, `cost-efficient`
- Fallbacks: `flux-kontext-pro`, `seedream-edit`

### `image-aesthetic-taste-first`

- Model key: `grok-imagine`
- Provider: `fal`
- Resolved model/endpoint: `xai/grok-imagine-image`
- Operation: `generate`
- Goal: `stylized`
- Input shape: `none`
- Fidelity priority: `create_net_new`
- Quality tier: `premium`
- Use when:
  - The prompt is taste-first: fashion, moodboard, stylized premium, aesthetic-heavy work.
  - The user wants more vibe and taste than strict brand/system control.
- Avoid when:
  - The request is typography-heavy, vector-heavy, or conservative editing.
  - The user wants the most faithful photoreal default rather than an aesthetic bias.
- Keywords: `aesthetic`, `fashion`, `taste`, `stylized premium`, `mood`
- Fallbacks: `nano-banana-pro`, `grok-imagine-edit`

### `image-multi-reference-aesthetic-edit`

- Model key: `grok-imagine-edit`
- Provider: `fal`
- Resolved model/endpoint: `xai/grok-imagine-image/edit`
- Operation: `edit`
- Goal: `restyle`
- Input shape: `multi_image`
- Fidelity priority: `preserve_subject`
- Quality tier: `premium`
- Use when:
  - The edit uses multiple input images to transfer mood or aesthetic.
  - You need an aesthetic-first edit lane instead of conservative preservation.
- Avoid when:
  - The edit is tiny and layout fidelity is the primary requirement.
  - You only have one image and no real need for multi-reference behavior.
- Keywords: `multi reference`, `blend references`, `aesthetic edit`
- Fallbacks: `seedream-edit`, `flux-kontext-pro`

## VIDEO

### `video-default-t2v`

- Model key: `kling`
- Provider: `fal`
- Resolved model/endpoint: `fal-ai/kling-video/v3/standard/text-to-video`
- Operation: `generate`
- Goal: `balanced`
- Input shape: `none`
- Fidelity priority: `create_net_new`
- Quality tier: `standard`
- Audio requirement: `optional`
- Use when:
  - General text-to-video with no specialist need.
  - You need the best default value lane for human subjects, motion, and broad prompt coverage.
- Avoid when:
  - The request is specifically about physics realism, reference-heavy composition, or top-end 4K polish.
- Keywords: `general motion`, `person`, `actor`, `dialogue`, `default video`
- Fallbacks: `seedance2`, `sora2`

### `video-cinematic-direction`

- Model key: `seedance2`
- Provider: `fal`
- Resolved model/endpoint: `bytedance/seedance-2.0/text-to-video`
- Operation: `generate`
- Goal: `cinematic`
- Input shape: `none`
- Fidelity priority: `create_net_new`
- Quality tier: `premium`
- Audio requirement: `optional`
- Use when:
  - Product shots, creative direction, cinematic control, or material-forward motion work.
  - The user values directed composition over cheap generic motion.
- Avoid when:
  - The job is simple enough for Kling.
  - The request is specifically about physical realism rather than cinematic look.
- Keywords: `cinematic`, `product shot`, `materials`, `creative direction`
- Fallbacks: `seedance2-reference`, `kling`

### `video-multi-reference-direction`

- Model key: `seedance2-reference`
- Provider: `fal`
- Resolved model/endpoint: `bytedance/seedance-2.0/reference-to-video`
- Operation: `generate`
- Goal: `cinematic`
- Input shape: `multi_image`
- Fidelity priority: `preserve_subject`
- Quality tier: `premium`
- Audio requirement: `optional`
- Use when:
  - The user provides multiple references and expects the model to respect them.
  - You need a composition-directed lane, not generic I2V.
- Avoid when:
  - You only have a single image.
  - The task is simple enough for standard text-to-video.
- Keywords: `multi reference`, `reference direction`, `guided composition`
- Fallbacks: `seedance2`, `veo3-ref`

### `video-physics-realism`

- Model key: `sora2`
- Provider: `fal`
- Resolved model/endpoint: `fal-ai/sora-2/text-to-video`
- Operation: `generate`
- Goal: `physics`
- Input shape: `none`
- Fidelity priority: `create_net_new`
- Quality tier: `premium`
- Audio requirement: `optional`
- Use when:
  - The prompt depends on physical interaction, gravity, fluids, collisions, or realistic dynamics.
  - You need realism more than stylization or cost efficiency.
- Avoid when:
  - The user mainly wants stylized or social-native motion.
  - The task is actually a video remix or edit rather than clean T2V.
- Keywords: `physics`, `gravity`, `fluid`, `collision`, `fabric simulation`
- Fallbacks: `sora2-pro`, `veo3`

### `video-remix-v2v`

- Model key: `sora2-remix`
- Provider: `fal`
- Resolved model/endpoint: `fal-ai/sora-2/video-to-video/remix`
- Operation: `remix`
- Goal: `restyle`
- Input shape: `video_only`
- Fidelity priority: `preserve_layout`
- Quality tier: `premium`
- Audio requirement: `none`
- Use when:
  - The user says remix, restyle, reinterpret this clip, or preserve motion but change look.
  - You need V2V, not T2V or I2V.
- Avoid when:
  - There is no input video.
  - The request is simply to extend an existing clip.
  - The request is to improve technical video quality, upscale, denoise, sharpen, deblur, or make the same clip cleaner.
- Keywords: `remix`, `restyle this clip`, `video to video`
- Fallbacks: `pixverse-extend`, `veo3-extend`

### `video-enhance-upscale`

- Model key: `video-upscale`
- Provider: `piapi`
- Resolved model/endpoint: `Qubico/video-toolkit`
- Operation: `edit`
- Goal: `best_quality`
- Input shape: `video_only`
- Fidelity priority: `preserve_layout`
- Quality tier: `specialist`
- Audio requirement: `none`
- Use when:
  - The user wants to improve the same rendered video rather than generate new motion.
  - Technical cleanup: upscale, denoise, sharpen, deblur, reduce compression artifacts, or improve perceived quality.
  - Use after the final motion is chosen; for best pro results, external Topaz/Runway-style enhancement may still beat a generative video lane.
- Avoid when:
  - The user wants creative restyle/remix of the clip.
  - The user wants more seconds or continuation; use video-extend.
  - The source motion is bad and should be regenerated from image or prompt.
- Keywords: `upscale video`, `video upscale`, `enhance video`, `improve video quality`, `mejora la calidad`, `mejorar la calidad`, `se ve mala calidad`, `denoise`, `sharpen`, `deblur`, `compression artifacts`, `artifact cleanup`
- Fallbacks: none

### `video-ultra-fast`

- Model key: `veo3`
- Provider: `fal`
- Resolved model/endpoint: `fal-ai/veo3.1/fast`
- Operation: `generate`
- Goal: `best_quality`
- Input shape: `none`
- Fidelity priority: `create_net_new`
- Quality tier: `ultra`
- Audio requirement: `optional`
- Use when:
  - The request explicitly wants ultra/high-end quality, 4K-ish positioning, or broadcast-grade polish.
  - You need top-end output but want the faster Veo lane first.
- Avoid when:
  - The budget does not justify Veo.
  - The task is actually a reference/video extension workflow.
- Keywords: `4k`, `broadcast`, `cinema polish`, `highest end`, `ultra`
- Fallbacks: `veo3-hq`, `sora2`

### `video-ultra-max-quality`

- Model key: `veo3-hq`
- Provider: `fal`
- Resolved model/endpoint: `fal-ai/veo3.1`
- Operation: `generate`
- Goal: `best_quality`
- Input shape: `none`
- Fidelity priority: `create_net_new`
- Quality tier: `ultra`
- Audio requirement: `optional`
- Use when:
  - The user wants maximum Veo quality over speed.
  - You already know the brief justifies the most expensive/high-end route.
- Avoid when:
  - The request can be solved by Veo fast or Kling.
- Keywords: `max quality`, `highest fidelity`, `hero cinematic`
- Fallbacks: `veo3`, `sora2-pro`

### `video-reference-driven`

- Model key: `veo3-ref`
- Provider: `fal`
- Resolved model/endpoint: `fal-ai/veo3.1/reference-to-video`
- Operation: `generate`
- Goal: `best_quality`
- Input shape: `multi_image`
- Fidelity priority: `preserve_subject`
- Quality tier: `ultra`
- Audio requirement: `optional`
- Use when:
  - You need Veo-class output while steering from reference imagery.
  - The job needs stronger quality than Seedance reference can justify.
- Avoid when:
  - The request is primarily social/stylized rather than premium cinematic.
  - No reference images are provided.
- Keywords: `reference video`, `reference to video`, `guided Veo`
- Fallbacks: `seedance2-reference`, `veo3-i2v`

### `video-first-last-frame`

- Model key: `veo3-first-last`
- Provider: `fal`
- Resolved model/endpoint: `fal-ai/veo3.1/first-last-frame-to-video`
- Operation: `generate`
- Goal: `preserve_layout`
- Input shape: `first+last_frame`
- Fidelity priority: `preserve_layout`
- Quality tier: `ultra`
- Audio requirement: `none`
- Use when:
  - The brief provides a first frame and a destination last frame.
  - You need controlled interpolation between two endpoints.
- Avoid when:
  - You only have one frame.
  - The request is actually to extend an existing video.
- Keywords: `first and last frame`, `frame interpolation`, `from this frame to that frame`
- Fallbacks: `pixverse-transition`, `veo3-i2v`

### `video-extend`

- Model key: `veo3-extend`
- Provider: `fal`
- Resolved model/endpoint: `fal-ai/veo3.1/extend-video`
- Operation: `extend`
- Goal: `preserve_layout`
- Input shape: `video_only`
- Fidelity priority: `preserve_layout`
- Quality tier: `ultra`
- Audio requirement: `optional`
- Use when:
  - The user says continue this clip, extend this video, or add more seconds without changing the core shot.
- Avoid when:
  - The user wants a creative restyle instead of literal continuation.
  - The user wants to improve quality of the same clip; Veo extend is continuation/polish, not a frame-faithful enhancer.
- Keywords: `continue this video`, `extend clip`, `video continuation`
- Fallbacks: `pixverse-extend`, `sora2-remix`

### `video-social-stylized-i2v`

- Model key: `pixverse-v6-i2v`
- Provider: `fal`
- Resolved model/endpoint: `fal-ai/pixverse/v6/image-to-video`
- Operation: `generate`
- Goal: `social`
- Input shape: `single_image`
- Fidelity priority: `preserve_subject`
- Quality tier: `specialist`
- Audio requirement: `none`
- Use when:
  - Stylized/social-native animation, viral motion, anime-ish movement, or trend-oriented content.
  - You care more about punchy motion language than physical realism.
- Avoid when:
  - The output needs top-end realism or premium cinematic polish.
- Keywords: `viral`, `stylized social`, `anime motion`, `reel motion`
- Fallbacks: `pixverse-transition`, `grok-video-i2v`

### `video-transition`

- Model key: `pixverse-transition`
- Provider: `fal`
- Resolved model/endpoint: `fal-ai/pixverse/v6/transition`
- Operation: `generate`
- Goal: `social`
- Input shape: `first+last_frame`
- Fidelity priority: `preserve_layout`
- Quality tier: `specialist`
- Audio requirement: `none`
- Use when:
  - The task is an image-to-image transition clip for reels or stylized motion posts.
- Avoid when:
  - You need realistic cinematic interpolation rather than flashy transition language.
- Keywords: `transition`, `before after`, `reel transition`
- Fallbacks: `veo3-first-last`, `pixverse-v6-i2v`

### `video-aesthetic-t2v`

- Model key: `grok-video`
- Provider: `fal`
- Resolved model/endpoint: `xai/grok-imagine-video/text-to-video`
- Operation: `generate`
- Goal: `stylized`
- Input shape: `none`
- Fidelity priority: `create_net_new`
- Quality tier: `premium`
- Audio requirement: `optional`
- Use when:
  - The brief is taste-first and aesthetic-heavy rather than realism-first.
  - You want xAI's stylized signature on video.
- Avoid when:
  - Physics realism or premium reference-control is the main requirement.
- Keywords: `stylized video`, `taste-first`, `fashion motion`
- Fallbacks: `grok-video-i2v`, `kling`

### `video-aesthetic-reference`

- Model key: `grok-video-ref`
- Provider: `fal`
- Resolved model/endpoint: `xai/grok-imagine-video/reference-to-video`
- Operation: `generate`
- Goal: `stylized`
- Input shape: `multi_image`
- Fidelity priority: `preserve_subject`
- Quality tier: `premium`
- Audio requirement: `optional`
- Use when:
  - Stylized video generation steered by reference images.
- Avoid when:
  - The task needs conservative fidelity or high-end cinematic Veo behavior.
- Keywords: `reference stylized video`, `aesthetic reference`
- Fallbacks: `grok-video-i2v`, `seedance2-reference`

### `video-lipsync`

- Model key: `sync-lipsync`
- Provider: `fal`
- Resolved model/endpoint: `fal-ai/sync-lipsync/v3`
- Operation: `lipsync`
- Goal: `preserve_layout`
- Input shape: `video+audio`
- Fidelity priority: `preserve_subject`
- Quality tier: `specialist`
- Audio requirement: `required`
- Use when:
  - You need a person/character to speak to provided audio.
  - Dedicated lipsync beats overloading general video lanes.
- Avoid when:
  - The job is actually avatar generation from a still image.
  - No external audio exists.
- Keywords: `lipsync`, `dub`, `make this person speak`
- Fallbacks: `kling-sound`, `omnihuman`

## MUSIC

### `music-default-full-song`

- Model key: `diffrhythm-full`
- Provider: `fal`
- Resolved model/endpoint: `fal-ai/diffrhythm`
- Operation: `generate`
- Goal: `best_quality`
- Input shape: `none`
- Fidelity priority: `create_net_new`
- Quality tier: `premium`
- Use when:
  - The user wants a fuller song-like result, not a tiny jingle.
- Avoid when:
  - You need very cheap fast drafts or iterative short musical ideas.
- Keywords: `song`, `full track`, `complete music`
- Fallbacks: `ace-step`, `udio`

### `music-flexible-fast`

- Model key: `ace-step`
- Provider: `fal`
- Resolved model/endpoint: `fal-ai/ace-step`
- Operation: `generate`
- Goal: `balanced`
- Input shape: `none`
- Fidelity priority: `create_net_new`
- Quality tier: `standard`
- Use when:
  - You need flexible lower-cost music generation or fast iteration.
- Avoid when:
  - The user explicitly wants the most complete song-like lane available.
- Keywords: `music bed`, `quick music`, `flexible music`
- Fallbacks: `diffrhythm-base`, `udio`

## TTS

### `tts-voice-clone`

- Model key: `f5-tts`
- Provider: `fal`
- Resolved model/endpoint: `fal-ai/f5-tts`
- Operation: `generate`
- Goal: `preserve_subject`
- Input shape: `image+audio`
- Fidelity priority: `preserve_subject`
- Quality tier: `standard`
- Use when:
  - The user wants speech synthesis, especially voice-clone or zero-shot style TTS.
- Avoid when:
  - The task is music generation, not spoken audio.
- Keywords: `tts`, `voice`, `speech`, `say this`, `clone voice`
- Fallbacks: none

## 3D

### `3d-image-to-model`

- Model key: `trellis2`
- Provider: `fal`
- Resolved model/endpoint: `fal-ai/trellis-2`
- Operation: `generate`
- Goal: `best_quality`
- Input shape: `single_image`
- Fidelity priority: `preserve_subject`
- Quality tier: `premium`
- Use when:
  - The user wants a 3D model from an image and quality matters.
- Avoid when:
  - The user only needs a quick cheap proof of concept.
- Keywords: `3d model`, `glb`, `mesh`, `object from image`
- Fallbacks: `trellis-image`, `trellis-multi`

### `3d-text-to-model`

- Model key: `trellis-text`
- Provider: `fal`
- Resolved model/endpoint: `fal-ai/trellis`
- Operation: `generate`
- Goal: `balanced`
- Input shape: `none`
- Fidelity priority: `create_net_new`
- Quality tier: `standard`
- Use when:
  - The user wants a 3D model from text only.
- Avoid when:
  - Reference imagery exists and should be exploited.
- Keywords: `text to 3d`, `generate 3d object`
- Fallbacks: `trellis2`

## TOOL

### `tool-remove-background`

- Model key: `remove-bg`
- Provider: `fal`
- Resolved model/endpoint: `fal-ai/birefnet`
- Operation: `edit`
- Goal: `preserve_layout`
- Input shape: `single_image`
- Fidelity priority: `preserve_subject`
- Quality tier: `specialist`
- Use when:
  - The task is explicit background removal.
- Avoid when:
  - The user wants a generative edit rather than utility extraction.
- Keywords: `remove background`, `transparent background`, `cutout`
- Fallbacks: none

### `tool-image-upscale`

- Model key: `image-upscale`
- Provider: `fal`
- Resolved model/endpoint: `fal-ai/clarity-upscaler`
- Operation: `edit`
- Goal: `best_quality`
- Input shape: `single_image`
- Fidelity priority: `preserve_layout`
- Quality tier: `specialist`
- Use when:
  - The task is explicit upscaling or resolution enhancement.
- Avoid when:
  - The image actually needs regeneration, not magnification.
- Keywords: `upscale`, `enhance`, `increase resolution`
- Fallbacks: none

### `tool-video-audio`

- Model key: `mmaudio`
- Provider: `fal`
- Resolved model/endpoint: `fal-ai/mmaudio-v2`
- Operation: `edit`
- Goal: `balanced`
- Input shape: `video_only`
- Fidelity priority: `preserve_layout`
- Quality tier: `specialist`
- Use when:
  - The task is to add/generate audio for an existing video.
- Avoid when:
  - The user wants a fresh video, not audio augmentation.
- Keywords: `add audio`, `sound design`, `audio for video`
- Fallbacks: none

### `tool-caption`

- Model key: `joycaption`
- Provider: `piapi`
- Resolved model/endpoint: `Qubico/joycaption`
- Operation: `caption`
- Goal: `balanced`
- Input shape: `single_image`
- Fidelity priority: `preserve_subject`
- Quality tier: `specialist`
- Use when:
  - The user wants captioning/description for an image as a utility operation.
- Avoid when:
  - The task is generation or editing rather than description.
- Keywords: `caption`, `describe image`, `alt text`
- Fallbacks: none
