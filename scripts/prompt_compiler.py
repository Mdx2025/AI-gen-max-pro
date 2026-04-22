"""Model-aware prompt shaping for ai-gen-max.

This module rewrites prompts *after* route selection. The router still decides
the safest lane first; the compiler only adapts wording to the chosen model
family so prompts land better without changing lane semantics.
"""

from __future__ import annotations

import re


NANO_BANANA_KEYS = {
    "nano-banana",
    "nano-banana-2",
    "nano-banana-pro",
    "nano-banana-preview",
}

GPT_IMAGE_KEYS = {"gpt-image-2", "gpt-image-1.5", "gpt-image-1"}
IDEOGRAM_KEYS = {"ideogram-v2", "ideogram-v3"}
RECRAFT_VECTOR_KEYS = {"recraft-v4-vector"}
KONTEXT_KEYS = {"flux-kontext-pro", "flux-kontext-dev"}
LOOKDEV_EDIT_KEYS = {"flux-2-max-edit", "seedream-edit", "grok-imagine-edit"}
GENERIC_GENERATE_KEYS = {"flux-2-max", "flux-2-pro", "seedream-v4", "seedream"}
KLING_VIDEO_KEYS = {"kling", "kling-pro", "kling-omni"}
SEEDANCE_VIDEO_KEYS = {"seedance2", "seedance2-fast", "seedance2-reference"}
SORA_VIDEO_KEYS = {"sora2", "sora2-pro", "sora2-remix"}
VEO_VIDEO_KEYS = {"veo3", "veo3-hq", "veo3-ref", "veo3-i2v", "veo3-first-last", "veo3-extend"}
VIDEO_SPECIALIST_KEYS = {"sync-lipsync", "pixverse-v6-i2v", "pixverse-transition", "pixverse-extend", "grok-video", "grok-video-ref", "grok-video-i2v"}

CONTINUITY_HINTS = (
    "same character",
    "consistent facial structure",
    "consistent lighting",
    "every frame",
    "same face",
    "same person",
    "character sheet",
)

TYPOGRAPHY_HINTS = (
    "text",
    "headline",
    "poster",
    "title",
    "banner",
    "sign",
    "label",
    "packaging",
    "logo",
)

TEXTURE_HINTS = (
    "brushed steel",
    "velvet",
    "frosted glass",
    "cracked dust",
    "smooth marble",
    "matte black carbon",
    "weathered wood",
)

COLOR_PSYCHOLOGY_HINTS = (
    "loneliness",
    "comfort",
    "mystery",
    "calm",
    "warm",
    "cool",
    "melancholy",
    "dramatic",
    "serene",
)

HERO_PRODUCT_HINTS = (
    "product shot",
    "product photo",
    "hero shot",
    "hero image",
    "bottle",
    "watch",
    "perfume",
    "packshot",
    "pack shot",
    "ecommerce",
    "studio setup",
)

POSTER_HINTS = (
    "poster",
    "banner",
    "headline",
    "title card",
    "ad creative",
    "billboard",
    "flyer",
)

SOCIAL_AD_HINTS = (
    "instagram",
    "social ad",
    "social media",
    "thumbnail",
    "campaign",
    "promo",
    "launch post",
    "marketing",
    "reel",
    "tiktok",
    "ugc",
)

CHARACTER_HINTS = (
    "character",
    "same character",
    "consistent facial structure",
    "character sheet",
    "portrait",
    "person",
    "woman",
    "man",
    "face",
)

EDIT_HINTS = (
    "replace",
    "change",
    "remove",
    "edit",
    "swap",
    "keep same",
    "preserve",
)

VIDEO_CINEMATIC_HINTS = (
    "cinematic",
    "film",
    "commercial",
    "shot",
    "close-up",
    "wide shot",
    "tracking shot",
    "dolly",
    "camera slowly",
)

VIDEO_PHYSICS_HINTS = (
    "physics",
    "gravity",
    "fluid",
    "collision",
    "fabric simulation",
    "splashes",
    "falling apart",
    "explosion",
)

VIDEO_REFERENCE_HINTS = (
    "@image1",
    "@video1",
    "@audio1",
    "reference",
    "guided by",
)

VIDEO_AUDIO_HINTS = (
    "audio:",
    "voiceover",
    "dialogue",
    "ambient sound",
    "sound design",
    "music",
    "lip sync",
    "lipsync",
)

VIDEO_EXTEND_HINTS = (
    "extend",
    "continue this video",
    "continue the clip",
    "add more seconds",
    "continuation",
)

VIDEO_MULTI_SHOT_HINTS = (
    "shot 1",
    "shot 2",
    "scene 1",
    "scene 2",
    "cut to",
)


RECIPE_LIBRARY = {
    "hero_product": {
        "label": "hero-product",
        "description": "High-control product hero or packaging visual.",
        "category": "image_generate",
    },
    "poster_typography": {
        "label": "poster-typography",
        "description": "Readable headline-led poster or ad creative.",
        "category": "image_generate",
    },
    "social_marketing": {
        "label": "social-marketing",
        "description": "Fast-scanning marketing or social asset.",
        "category": "image_generate",
    },
    "character_consistency": {
        "label": "character-consistency",
        "description": "Identity-locked character or portrait image.",
        "category": "image_generate",
    },
    "conservative_product_edit": {
        "label": "conservative-product-edit",
        "description": "Minimal product/layout-safe edit with preservation clauses.",
        "category": "image_edit",
    },
    "lookdev_polish": {
        "label": "lookdev-polish",
        "description": "Premium relight/material/color-grade polish pass.",
        "category": "image_edit",
    },
    "general": {
        "label": "general",
        "description": "General-purpose structured visual brief.",
        "category": "image_generate",
    },
    "cinematic_shot": {
        "label": "cinematic-shot",
        "description": "Directed cinematic shot with explicit camera and pacing.",
        "category": "video_generate",
    },
    "ugc_social_video": {
        "label": "ugc-social-video",
        "description": "Fast-scanning social-native video with punchy motion.",
        "category": "video_generate",
    },
    "product_commercial": {
        "label": "product-commercial",
        "description": "Commercial product video with material-driven hero framing.",
        "category": "video_generate",
    },
    "physics_realism": {
        "label": "physics-realism",
        "description": "Realistic motion, collisions, fluids, or physical dynamics.",
        "category": "video_generate",
    },
    "reference_driven_motion": {
        "label": "reference-driven-motion",
        "description": "Video steered by reference images, clips, or audio anchors.",
        "category": "video_reference",
    },
    "dialogue_lipsync": {
        "label": "dialogue-lipsync",
        "description": "Speech-led shot synchronized to dialogue or supplied audio.",
        "category": "video_lipsync",
    },
    "multi_shot_storyboard": {
        "label": "multi-shot-storyboard",
        "description": "Multi-shot sequence with explicit shot breakdown.",
        "category": "video_generate",
    },
    "extend_existing_video": {
        "label": "extend-existing-video",
        "description": "Continuation of an existing clip with shot preservation.",
        "category": "video_extend",
    },
}


def _normalize_prompt(prompt: str | None) -> str:
    prompt = (prompt or "").strip()
    if not prompt:
        return ""
    return re.sub(r"\s+", " ", prompt).strip()


def _quoted_fragments(prompt: str) -> list[str]:
    return re.findall(r"[\"“']([^\"”']{1,80})[\"”']", prompt)


def _contains_any(prompt: str, keywords: tuple[str, ...] | set[str]) -> bool:
    lowered = prompt.lower()
    return any(keyword in lowered for keyword in keywords)


def _looks_structured(prompt: str) -> bool:
    return "\n" in prompt or any(token in prompt for token in ("Scene:", "Lighting:", "Camera:", "Mood:", "Subject:"))


def _join_lines(lines: list[str]) -> str:
    return "\n".join(line.rstrip() for line in lines if line and line.strip())


def resolve_operation_class(media_type: str, route_id: str, params: dict | None = None) -> str:
    params = params or {}

    if media_type == "image":
        if route_id == "image-strict-inpaint":
            return "image_inpaint"
        if params.get("image_url") or params.get("image_urls") or route_id in {
            "image-conservative-edit",
            "image-high-end-edit",
            "image-strong-lookdev-edit",
            "image-relight",
        }:
            return "image_edit"
        return "image_generate"

    if media_type == "video":
        if route_id == "video-lipsync":
            return "video_lipsync"
        if route_id == "video-extend":
            return "video_extend"
        if route_id in {
            "video-multi-reference-direction",
            "video-reference-driven",
            "video-aesthetic-reference",
            "video-first-last-frame",
        }:
            return "video_reference"
        if params.get("image_url") or params.get("image_urls") or params.get("video_url") or params.get("video_urls"):
            if route_id not in {"video-default-t2v", "video-cinematic-direction", "video-physics-realism", "video-ultra-fast", "video-ultra-max-quality", "video-aesthetic-t2v"}:
                return "video_reference"
        return "video_generate"

    return f"{media_type}_generic"


def _recipe(name: str, expected_category: str) -> dict:
    recipe = RECIPE_LIBRARY[name]
    if recipe["category"] != expected_category:
        raise ValueError(
            f"Recipe '{name}' belongs to '{recipe['category']}', not '{expected_category}'"
        )
    return recipe


def _detect_recipe(prompt: str, *, route_id: str, model_key: str, routing: dict, params: dict, operation_class: str) -> dict:
    lowered = prompt.lower()

    if route_id == "image-typography-poster" or _contains_any(lowered, POSTER_HINTS):
        return _recipe("poster_typography", operation_class)
    if route_id == "image-conservative-edit" or (
        (route_id == "image-high-end-edit" or model_key in KONTEXT_KEYS)
        and _contains_any(lowered, HERO_PRODUCT_HINTS + EDIT_HINTS)
        and bool(params.get("image_url") or params.get("image_urls"))
    ):
        return _recipe("conservative_product_edit", operation_class)
    if route_id == "image-strong-lookdev-edit" or routing.get("goal") == "best_quality":
        return _recipe("lookdev_polish", operation_class)
    if _contains_any(lowered, HERO_PRODUCT_HINTS):
        return _recipe("hero_product", operation_class)
    if _contains_any(lowered, CHARACTER_HINTS) and (
        _contains_any(lowered, CONTINUITY_HINTS) or "reference" in lowered or bool(params.get("image_url") or params.get("image_urls"))
    ):
        return _recipe("character_consistency", operation_class)
    if _contains_any(lowered, SOCIAL_AD_HINTS):
        return _recipe("social_marketing", operation_class)
    if operation_class == "image_edit":
        return _recipe("lookdev_polish" if routing.get("goal") == "best_quality" else "conservative_product_edit", operation_class)
    return _recipe("general", operation_class)


def _detect_video_recipe(prompt: str, *, route_id: str, model_key: str, routing: dict, params: dict, operation_class: str) -> dict:
    lowered = prompt.lower()
    has_reference = bool(
        params.get("image_url")
        or params.get("image_urls")
        or params.get("video_url")
        or params.get("video_urls")
        or params.get("audio_url")
        or params.get("audio_urls")
        or params.get("first_frame_url")
        or params.get("last_frame_url")
    )

    if route_id == "video-lipsync" or _contains_any(lowered, ("lipsync", "lip sync", "dub", "dialogue")):
        return _recipe("dialogue_lipsync", operation_class)
    if route_id == "video-extend" or _contains_any(lowered, VIDEO_EXTEND_HINTS):
        return _recipe("extend_existing_video", operation_class)
    if route_id in {"video-multi-reference-direction", "video-reference-driven", "video-aesthetic-reference"} or (
        has_reference and _contains_any(lowered, VIDEO_REFERENCE_HINTS)
    ):
        return _recipe("reference_driven_motion", operation_class)
    if route_id == "video-first-last-frame":
        return _recipe("reference_driven_motion", operation_class)
    if route_id == "video-physics-realism" or _contains_any(lowered, VIDEO_PHYSICS_HINTS):
        return _recipe("physics_realism", operation_class)
    if route_id == "video-cinematic-direction" or _contains_any(lowered, HERO_PRODUCT_HINTS + VIDEO_CINEMATIC_HINTS):
        if _contains_any(lowered, HERO_PRODUCT_HINTS):
            return _recipe("product_commercial", operation_class)
        return _recipe("cinematic_shot", operation_class)
    if route_id == "video-default-t2v" and _contains_any(lowered, SOCIAL_AD_HINTS):
        return _recipe("ugc_social_video", operation_class)
    if _contains_any(lowered, VIDEO_MULTI_SHOT_HINTS):
        return _recipe("multi_shot_storyboard", operation_class)
    if _contains_any(lowered, SOCIAL_AD_HINTS):
        return _recipe("ugc_social_video", operation_class)
    fallback_recipe = "cinematic_shot" if operation_class == "video_generate" else "reference_driven_motion"
    if operation_class == "video_extend":
        fallback_recipe = "extend_existing_video"
    if operation_class == "video_lipsync":
        fallback_recipe = "dialogue_lipsync"
    return _recipe(fallback_recipe, operation_class)


def _compile_nano_banana(prompt: str, *, model_key: str, params: dict, route_id: str, recipe: dict) -> dict:
    quoted = _quoted_fragments(prompt)
    continuity_requested = _contains_any(prompt, CONTINUITY_HINTS)
    texture_requested = _contains_any(prompt, TEXTURE_HINTS)
    color_psychology_requested = _contains_any(prompt, COLOR_PSYCHOLOGY_HINTS)
    has_reference = bool(params.get("image_url") or params.get("image_urls"))
    quality_line = (
        "Quality target: hero-grade finish, premium materials, precise spatial relationships, and polished typography when requested."
        if model_key == "nano-banana-pro"
        else "Quality target: fast workhorse output with clear composition, readable lighting, and strong client-usable finish."
    )

    recipe_lines = {
        "hero-product": [
            "Recipe: product hero image with premium material read, clean set design, and commercial composition.",
            "Product staging: keep the subject dominant, centered or intentionally offset, with controlled negative space.",
            "Surface realism: prioritize believable reflections, edge definition, and premium material contrast.",
        ],
        "poster-typography": [
            "Recipe: headline-led poster or ad visual with strong hierarchy.",
            "Text hierarchy: keep the headline visually dominant and easy to read.",
            "Composition: support the message first; do not let background effects bury the typography.",
        ],
        "social-marketing": [
            "Recipe: social marketing asset optimized for instant scanability on small screens.",
            "Composition: make the first read obvious in under a second.",
            "Visual hierarchy: one dominant subject, one supporting message, minimal clutter.",
        ],
        "character-consistency": [
            "Recipe: character consistency image with locked identity and repeatable visual traits.",
            "Identity lock: preserve face shape, hair silhouette, age cues, and defining markers.",
            "Shot discipline: keep subject readability stronger than background style flourishes.",
        ],
        "general": [
            "Recipe: balanced visual brief with strong readability and controlled styling.",
        ],
    }.get(recipe["label"], ["Recipe: balanced visual brief with strong readability and controlled styling."])

    lines = [
        "Create one finished image.",
        f"Primary brief: {prompt}",
        "Structure the result in layers, not as one overloaded sentence.",
        *recipe_lines,
        "Subject and scene: stay faithful to the brief and keep the main read obvious.",
        "Composition and camera: make the framing intentional and easy to scan.",
        "Lighting: use explicit, coherent light direction rather than generic dramatic lighting.",
    ]
    if texture_requested:
        lines.append("Materials and texture: keep the requested surface cues visible and believable.")
    else:
        lines.append("Materials and texture: use only a few concrete surface cues that support the subject.")
    if color_psychology_requested:
        lines.append("Color and mood: reinforce the emotional intent of the requested palette.")
    else:
        lines.append("Color and mood: use palette choices to reinforce the mood instead of adding random style accents.")
    lines.append("Micro-details: add a few high-value details; do not clutter the frame.")
    if continuity_requested:
        lines.append("Continuity: keep facial structure, identity markers, and lighting consistent across repeated generations.")
    if has_reference:
        lines.append("Reference handling: treat the provided image references as factual anchors for identity, layout, or product details.")
    if quoted:
        lines.append("Typography: render quoted wording exactly if text appears in the image.")
    lines.append(quality_line)
    lines.append("Avoid: duplicate subjects, extra limbs, unreadable text, muddy materials, clutter, and unrelated objects.")

    return {
        "prompt": _join_lines(lines),
        "compiler_trace": {
            "applied": True,
            "strategy": "nano-banana-layered",
            "recipe": recipe["label"],
            "route_id": route_id,
            "model_key": model_key,
            "notes": [
                "Layered natural-language structure for Nano Banana family.",
                "Inspired by community guidance: layering, texture cues, color psychology, continuity, and simplified instructions.",
            ],
        },
    }


def _compile_gpt_image(prompt: str, *, model_key: str, route_id: str, recipe: dict) -> dict:
    recipe_line = {
        "hero-product": "Recipe: hero product asset with exact object control and clean commercial readability.",
        "poster-typography": "Recipe: poster layout with readable headline and strict prompt adherence.",
        "character-consistency": "Recipe: preserve identity markers and do not improvise facial traits.",
    }.get(recipe["label"], "Recipe: high-adherence production image with minimal ambiguity.")
    lines = [
        "Create one polished image that follows the brief exactly.",
        f"Core brief: {prompt}",
        recipe_line,
        "Priority order:",
        "1. Follow the requested subject, composition, and text literally.",
        "2. Prefer prompt adherence and clean readability over decorative extra flourishes.",
        "3. If details conflict, preserve the earliest and most explicit instruction.",
        "4. Keep the scene legible; do not introduce extra objects unless the brief implies them.",
        "5. Render quoted wording exactly when text is requested.",
        "Avoid: clutter, duplicate subjects, unreadable text, accidental anatomy errors, and mismatched lighting.",
    ]
    return {
        "prompt": _join_lines(lines),
        "compiler_trace": {
            "applied": True,
            "strategy": "gpt-image-adherence",
            "recipe": recipe["label"],
            "route_id": route_id,
            "model_key": model_key,
            "notes": [
                "Prompt-adherence-first structure.",
                "Based on OpenAI guidance to keep a clean base prompt and avoid overloading the image request.",
            ],
        },
    }


def _compile_ideogram(prompt: str, *, model_key: str, route_id: str, recipe: dict) -> dict:
    quoted = _quoted_fragments(prompt)
    recipe_line = (
        "Recipe: headline-led poster with strong text hierarchy and readable composition."
        if recipe["label"] == "poster-typography"
        else "Recipe: layout-first typographic visual with controlled readability."
    )
    lines = [
        "Create one image using natural sentence-style prompting.",
        f"Overview sentence: {prompt}",
        recipe_line,
        "Prompt structure order: overview, main subject details, pose/action, supporting elements, background, style, technical polish.",
        "Put any critical on-image text early in the composition description and render quoted wording exactly.",
        "Keep layout simple and readable. If text is present, keep it short and visually dominant enough to read.",
        "Do not use parameter syntax or hidden flags inside the prompt.",
        "Avoid: crowded layouts, long paragraphs of copy, misspellings, stray words, and decorative clutter that weakens readability.",
    ]
    if not quoted and _contains_any(prompt, TYPOGRAPHY_HINTS):
        lines.append("If text appears in the design, keep it short, in English when possible, and visually prioritized.")
    return {
        "prompt": _join_lines(lines),
        "compiler_trace": {
            "applied": True,
            "strategy": "ideogram-structured",
            "recipe": recipe["label"],
            "route_id": route_id,
            "model_key": model_key,
            "notes": [
                "Structured prompt ordering for typography and layout.",
                "Based on Ideogram docs: natural language, quoted text early, readable layout, no hidden flags.",
            ],
        },
    }


def _compile_recraft_vector(prompt: str, *, model_key: str, route_id: str, recipe: dict) -> dict:
    recipe_line = (
        "Recipe: brand-system vector asset with scalable geometry."
        if recipe["label"] != "poster-typography"
        else "Recipe: typographic vector-led composition with clean hierarchy."
    )
    lines = [
        "Create one clean vector-first image from this brief.",
        f"Design brief: {prompt}",
        recipe_line,
        "Design priorities: strong silhouette, simple geometric forms, clean negative space, and brand-system consistency.",
        "Use flat fills or restrained gradients only when they help the mark stay scalable.",
        "If typography is requested, keep it integrated, legible, and secondary to the core vector structure unless the brief says otherwise.",
        "Avoid: photoreal textures, cinematic lighting, raster-like noise, and unnecessary detail that hurts SVG clarity.",
    ]
    return {
        "prompt": _join_lines(lines),
        "compiler_trace": {
            "applied": True,
            "strategy": "recraft-vector-brief",
            "recipe": recipe["label"],
            "route_id": route_id,
            "model_key": model_key,
            "notes": [
                "Vector-specific simplification and SVG-safe constraints.",
            ],
        },
    }


def _compile_kontext_edit(prompt: str, *, model_key: str, route_id: str, routing: dict, recipe: dict) -> dict:
    preserve_line = (
        "Keep the original framing, composition, subject scale, camera angle, and identity markers unchanged unless the brief explicitly changes them."
    )
    if routing.get("goal") == "preserve_layout" or route_id == "image-conservative-edit":
        extra_line = "Do the minimum necessary change. Keep everything else unchanged."
    else:
        extra_line = "Preserve the subject and core scene logic unless the brief explicitly replaces them."

    lines = [
        "Apply this edit to the provided image.",
        f"Edit brief: {prompt}",
        (
            "Recipe: conservative product/layout edit with hard preservation bias."
            if recipe["label"] == "conservative-product-edit"
            else "Recipe: premium lookdev polish pass with preservation-aware edits."
        ),
        "Use exact nouns for the target subject or object; avoid ambiguous pronouns.",
        preserve_line,
        extra_line,
        "If changing on-image text, replace quoted wording verbatim and preserve font style, color, and alignment unless the brief explicitly changes them.",
        "Avoid: global drift, reframing, duplicate objects, identity drift, and unrelated redesigns.",
    ]
    return {
        "prompt": _join_lines(lines),
        "compiler_trace": {
            "applied": True,
            "strategy": "kontext-edit-precision",
            "recipe": recipe["label"],
            "route_id": route_id,
            "model_key": model_key,
            "notes": [
                "Exact-noun, preserve-clause edit prompt for FLUX/Kontext-like lanes.",
                "Based on BFL guidance and community practice: direct verbs, preserve clauses, exact quoted text.",
            ],
        },
    }


def _compile_generic_generate(prompt: str, *, model_key: str, route_id: str, recipe: dict) -> dict:
    lines = [
        "Create one polished image from this brief.",
        f"Primary brief: {prompt}",
        f"Recipe: {recipe['description']}",
        "Make the subject, environment, composition, lighting, and mood explicit and coherent.",
        "Prefer a small number of concrete details over a long pile of loosely related style words.",
        "Avoid: clutter, duplicate subjects, muddy materials, and unrelated visual additions.",
    ]
    return {
        "prompt": _join_lines(lines),
        "compiler_trace": {
            "applied": True,
            "strategy": "generic-generate-brief",
            "recipe": recipe["label"],
            "route_id": route_id,
            "model_key": model_key,
            "notes": [
                "Generic layered brief for high-end generate lanes without a dedicated adapter.",
            ],
        },
    }


def _compile_kling_video(prompt: str, *, model_key: str, route_id: str, recipe: dict) -> dict:
    recipe_line = {
        "ugc-social-video": "Recipe: UGC/social-native clip with immediate hook, clear action, and punchy pacing.",
        "multi-shot-storyboard": "Recipe: multi-shot sequence. Write each shot as a distinct beat instead of one compressed paragraph.",
        "product-commercial": "Recipe: commercial product clip with clean shot design and premium object movement.",
    }.get(recipe["label"], "Recipe: cinematic default video with explicit shot, motion, and camera direction.")
    lines = [
        "Generate one coherent video.",
        f"Video brief: {prompt}",
        recipe_line,
        "Describe the clip as a sequence of clear beats: subject, environment, action, camera, lighting, and pacing.",
        "If multiple shots are needed, label them explicitly as Shot 1, Shot 2, Shot 3.",
        "Camera: specify movement clearly and keep it physically readable.",
        "Motion: keep one primary action per shot unless the brief explicitly calls for complexity.",
        "Audio: describe dialogue, ambience, or sound effects only when needed.",
        "Avoid: overloaded paragraphs, conflicting actions, chaotic camera moves, and unnecessary extra subjects.",
    ]
    return {
        "prompt": _join_lines(lines),
        "compiler_trace": {
            "applied": True,
            "strategy": "kling-video-sequenced",
            "recipe": recipe["label"],
            "route_id": route_id,
            "model_key": model_key,
            "notes": [
                "Kling adapter favors explicit shot sequencing, camera direction, and audio breakdown.",
                "Based on fal Kling 3.0 prompting guidance and Kling 3.0 model docs.",
            ],
        },
    }


def _compile_seedance_video(prompt: str, *, model_key: str, route_id: str, recipe: dict, params: dict) -> dict:
    has_references = bool(params.get("image_urls") or params.get("video_urls") or params.get("audio_urls"))
    lines = [
        "Generate one coherent video.",
        f"Video brief: {prompt}",
        (
            "Recipe: reference-driven motion. Treat tagged assets as factual anchors."
            if recipe["label"] == "reference-driven-motion"
            else f"Recipe: {recipe['description']}"
        ),
        "Write the prompt like a production brief: subject, shot design, camera move, motion, lighting, and pacing.",
    ]
    if has_references:
        lines.append("If references are provided, refer to them explicitly as @Image1, @Image2, @Video1, @Audio1 and state the role of each one.")
    if recipe["label"] in {"multi-shot-storyboard", "product-commercial", "cinematic-shot"}:
        lines.append("For multi-shot sequences, label shots explicitly and give each shot one dominant action and one camera movement.")
    lines.extend([
        "If audio matters, describe the sound bed or voiceover in the same prompt.",
        "Avoid: too many shots for a short duration, ambiguous reference roles, and mixed camera instructions inside one beat.",
    ])
    return {
        "prompt": _join_lines(lines),
        "compiler_trace": {
            "applied": True,
            "strategy": "seedance-reference-aware",
            "recipe": recipe["label"],
            "route_id": route_id,
            "model_key": model_key,
            "notes": [
                "Seedance adapter emphasizes reference tags, shot labels, and multimodal production structure.",
                "Based on fal Seedance 2 docs and reference-to-video guidance.",
            ],
        },
    }


def _compile_sora_video(prompt: str, *, model_key: str, route_id: str, recipe: dict) -> dict:
    lines = [
        "Generate one video as if briefing a cinematographer for a storyboard panel.",
        f"Shot brief: {prompt}",
        f"Recipe: {recipe['description']}",
        "Be concise but specific about subject, setting, action, camera style, pacing, and audio.",
        "If realism matters, describe the physical action directly instead of using vague cinematic adjectives alone.",
        "If audio matters, state dialogue, ambience, and sound effects explicitly.",
        "Prefer one clean scene objective over many competing ideas.",
        "Avoid: too many simultaneous speaking characters, chaotic collisions, and extremely rapid camera moves unless absolutely required.",
    ]
    return {
        "prompt": _join_lines(lines),
        "compiler_trace": {
            "applied": True,
            "strategy": "sora-storyboard-brief",
            "recipe": recipe["label"],
            "route_id": route_id,
            "model_key": model_key,
            "notes": [
                "Sora adapter frames the prompt as a cinematographer/storyboard brief with explicit audio and action cues.",
                "Based on OpenAI Sora 2 prompting guidance and help docs.",
            ],
        },
    }


def _compile_veo_video(prompt: str, *, model_key: str, route_id: str, recipe: dict) -> dict:
    lines = [
        "Generate one premium video clip.",
        f"Video brief: {prompt}",
        f"Recipe: {recipe['description']}",
        "Describe the camera perspective, movement, environment motion, subject motion, and soundscape together.",
        "Use sensory detail only when it helps the shot read more clearly.",
    ]
    if recipe["label"] == "reference-driven-motion":
        lines.append("Treat the supplied references as strong anchors for subject, look, or endpoint control.")
    if recipe["label"] == "extend-existing-video":
        lines.append("Preserve the established shot logic and continue motion naturally instead of inventing a new scene.")
    lines.extend([
        "Keep the cinematic finish high without overstuffing the shot with too many simultaneous events.",
        "Avoid: random extra subjects, inconsistent camera grammar, and conflicting sound cues.",
    ])
    return {
        "prompt": _join_lines(lines),
        "compiler_trace": {
            "applied": True,
            "strategy": "veo-sensory-cinematic",
            "recipe": recipe["label"],
            "route_id": route_id,
            "model_key": model_key,
            "notes": [
                "Veo adapter integrates camera, motion, and soundscape as one cinematic brief.",
                "Based on fal Veo 3.1 examples/docs.",
            ],
        },
    }


def _compile_video_specialist(prompt: str, *, model_key: str, route_id: str, recipe: dict) -> dict:
    if model_key == "sync-lipsync":
        lines = [
            "Apply precise lipsync to the provided video and audio.",
            f"Brief: {prompt}",
            "Recipe: dialogue-led sync with preserved framing and identity.",
            "Keep mouth timing, head pose continuity, and facial identity stable.",
            "Do not redesign the scene or introduce unrelated motion.",
        ]
        strategy = "lipsync-preserve"
        notes = ["Specialist lipsync prompt for sync-lipsync lane."]
    else:
        lines = [
            "Generate one video clip.",
            f"Video brief: {prompt}",
            f"Recipe: {recipe['description']}",
            "Keep the motion language aligned with the specialist lane and avoid mixing incompatible goals.",
        ]
        strategy = "video-specialist-brief"
        notes = ["Generic specialist fallback for remaining video lanes."]

    return {
        "prompt": _join_lines(lines),
        "compiler_trace": {
            "applied": True,
            "strategy": strategy,
            "recipe": recipe["label"],
            "route_id": route_id,
            "model_key": model_key,
            "notes": notes,
        },
    }


def compile_prompt(
    raw_prompt: str | None,
    *,
    media_type: str,
    model_key: str,
    route_id: str,
    params: dict | None = None,
    routing: dict | None = None,
) -> dict:
    prompt = _normalize_prompt(raw_prompt)
    params = params or {}
    routing = routing or {}

    if not prompt:
        return {"prompt": prompt, "compiler_trace": {"applied": False, "reason": "empty_prompt"}}

    if media_type == "image":
        operation_class = resolve_operation_class(media_type, route_id, params)
        if route_id == "image-strict-inpaint":
            return {"prompt": prompt, "compiler_trace": {"applied": False, "reason": "strict_inpaint_prompt_passthrough", "operation_class": operation_class}}

        if _looks_structured(prompt) and model_key not in KONTEXT_KEYS:
            return {"prompt": prompt, "compiler_trace": {"applied": False, "reason": "already_structured", "operation_class": operation_class}}

        recipe = _detect_recipe(
            prompt,
            route_id=route_id,
            model_key=model_key,
            routing=routing,
            params=params,
            operation_class=operation_class,
        )

        if model_key in NANO_BANANA_KEYS:
            result = _compile_nano_banana(prompt, model_key=model_key, params=params, route_id=route_id, recipe=recipe)
        elif model_key in GPT_IMAGE_KEYS:
            result = _compile_gpt_image(prompt, model_key=model_key, route_id=route_id, recipe=recipe)
        elif model_key in IDEOGRAM_KEYS:
            result = _compile_ideogram(prompt, model_key=model_key, route_id=route_id, recipe=recipe)
        elif model_key in RECRAFT_VECTOR_KEYS:
            result = _compile_recraft_vector(prompt, model_key=model_key, route_id=route_id, recipe=recipe)
        elif model_key in KONTEXT_KEYS or model_key in LOOKDEV_EDIT_KEYS:
            result = _compile_kontext_edit(prompt, model_key=model_key, route_id=route_id, routing=routing, recipe=recipe)
        elif model_key in GENERIC_GENERATE_KEYS:
            result = _compile_generic_generate(prompt, model_key=model_key, route_id=route_id, recipe=recipe)
        else:
            return {"prompt": prompt, "compiler_trace": {"applied": False, "reason": "no_adapter_for_model", "operation_class": operation_class}}
        result["compiler_trace"]["operation_class"] = operation_class
        return result

    if media_type == "video":
        operation_class = resolve_operation_class(media_type, route_id, params)
        if _looks_structured(prompt):
            return {"prompt": prompt, "compiler_trace": {"applied": False, "reason": "already_structured", "operation_class": operation_class}}

        recipe = _detect_video_recipe(
            prompt,
            route_id=route_id,
            model_key=model_key,
            routing=routing,
            params=params,
            operation_class=operation_class,
        )

        if model_key in KLING_VIDEO_KEYS:
            result = _compile_kling_video(prompt, model_key=model_key, route_id=route_id, recipe=recipe)
        elif model_key in SEEDANCE_VIDEO_KEYS:
            result = _compile_seedance_video(prompt, model_key=model_key, route_id=route_id, recipe=recipe, params=params)
        elif model_key in SORA_VIDEO_KEYS:
            result = _compile_sora_video(prompt, model_key=model_key, route_id=route_id, recipe=recipe)
        elif model_key in VEO_VIDEO_KEYS:
            result = _compile_veo_video(prompt, model_key=model_key, route_id=route_id, recipe=recipe)
        elif model_key in VIDEO_SPECIALIST_KEYS:
            result = _compile_video_specialist(prompt, model_key=model_key, route_id=route_id, recipe=recipe)
        else:
            return {"prompt": prompt, "compiler_trace": {"applied": False, "reason": "no_adapter_for_model", "operation_class": operation_class}}
        result["compiler_trace"]["operation_class"] = operation_class
        return result

    return {"prompt": prompt, "compiler_trace": {"applied": False, "reason": "unsupported_media_type"}}
