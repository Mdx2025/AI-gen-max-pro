#!/usr/bin/env python3
"""Consistency tests for ai-gen-max manifest and generated docs."""

from __future__ import annotations

import unittest
from pathlib import Path

from model_manifest import (
    DEFAULT_IMAGE_MODEL_ID,
    DEFAULT_IMAGE_MODEL_KEY,
    FAL_EDIT_MAP,
    FAL_I2V_MAP,
    FAL_MODEL_MAP,
    PIAPI_MODEL_MAP,
    ROUTING_SCHEMA,
    infer_input_shape,
    requires_strict_preservation,
    resolve_route_selection,
    validate_route_constraints,
)
from prompt_compiler import compile_prompt, resolve_operation_class


ROOT = Path(__file__).resolve().parents[1]


class ManifestTests(unittest.TestCase):
    def test_default_image_is_gpt_image_2(self) -> None:
        self.assertEqual(DEFAULT_IMAGE_MODEL_KEY, "gpt-image-2")
        self.assertEqual(DEFAULT_IMAGE_MODEL_ID, "fal-ai/gpt-image-2")
        self.assertEqual(FAL_MODEL_MAP[DEFAULT_IMAGE_MODEL_KEY], DEFAULT_IMAGE_MODEL_ID)
        self.assertEqual(FAL_EDIT_MAP[DEFAULT_IMAGE_MODEL_ID], "fal-ai/gpt-image-2/edit")

    def test_sora2_and_sora2_pro_have_distinct_fal_endpoints(self) -> None:
        self.assertEqual(FAL_MODEL_MAP["sora2"], "fal-ai/sora-2/text-to-video")
        self.assertEqual(FAL_MODEL_MAP["sora2-pro"], "fal-ai/sora-2/text-to-video/pro")
        self.assertNotEqual(FAL_MODEL_MAP["sora2"], FAL_MODEL_MAP["sora2-pro"])
        self.assertEqual(FAL_MODEL_MAP["sora2-remix"], "fal-ai/sora-2/video-to-video/remix")

    def test_sora2_i2v_and_pro_i2v_have_distinct_fal_endpoints(self) -> None:
        self.assertEqual(
            FAL_I2V_MAP["fal-ai/sora-2/text-to-video"],
            "fal-ai/sora-2/image-to-video",
        )
        self.assertEqual(
            FAL_I2V_MAP["fal-ai/sora-2/text-to-video/pro"],
            "fal-ai/sora-2/image-to-video/pro",
        )

    def test_veo3_aliases_now_point_to_veo3_1(self) -> None:
        self.assertEqual(FAL_MODEL_MAP["veo3"], "fal-ai/veo3.1/fast")
        self.assertEqual(FAL_MODEL_MAP["veo3-hq"], "fal-ai/veo3.1")
        self.assertEqual(FAL_I2V_MAP["fal-ai/veo3.1/fast"], "fal-ai/veo3.1/fast/image-to-video")
        self.assertEqual(FAL_I2V_MAP["fal-ai/veo3.1"], "fal-ai/veo3.1/image-to-video")

    def test_new_edit_and_reference_lanes_are_present(self) -> None:
        self.assertEqual(FAL_MODEL_MAP["grok-imagine"], "xai/grok-imagine-image")
        self.assertEqual(FAL_MODEL_MAP["grok-video-ref"], "xai/grok-imagine-video/reference-to-video")
        self.assertEqual(FAL_MODEL_MAP["seedance2-reference"], "bytedance/seedance-2.0/reference-to-video")

    def test_routing_schema_model_keys_resolve(self) -> None:
        for routes in ROUTING_SCHEMA.values():
            for route in routes:
                model_key = route["model_key"]
                self.assertTrue(
                    model_key in FAL_MODEL_MAP or model_key in PIAPI_MODEL_MAP,
                    f"Unknown model key in schema: {model_key}",
                )
                for fallback in route.get("fallback_model_keys", []):
                    self.assertTrue(
                        fallback in FAL_MODEL_MAP or fallback in PIAPI_MODEL_MAP,
                        f"Unknown fallback model key in schema: {fallback}",
                    )

    def test_routing_schema_keeps_expected_defaults(self) -> None:
        image_balanced = next(route for route in ROUTING_SCHEMA["image"] if route["route_id"] == "image-balanced-premium")
        image_premium = next(route for route in ROUTING_SCHEMA["image"] if route["route_id"] == "image-default-best-quality")
        image_vector = next(route for route in ROUTING_SCHEMA["image"] if route["route_id"] == "image-vector-branding")
        image_typography = next(route for route in ROUTING_SCHEMA["image"] if route["route_id"] == "image-typography-poster")
        video_default = next(route for route in ROUTING_SCHEMA["video"] if route["route_id"] == "video-default-t2v")
        self.assertEqual(image_balanced["model_key"], "nano-banana-2")
        self.assertEqual(image_premium["model_key"], "gpt-image-2")
        self.assertEqual(image_vector["model_key"], "recraft-v4-vector")
        self.assertEqual(image_typography["model_key"], "ideogram-v3")
        self.assertEqual(video_default["model_key"], "kling")

    def test_recraft_and_ideogram_latest_endpoints_are_registered(self) -> None:
        self.assertEqual(FAL_MODEL_MAP["recraft-v4-vector"], "fal-ai/recraft/v4/text-to-vector")
        self.assertEqual(FAL_MODEL_MAP["recraft-v4"], "fal-ai/recraft/v4/text-to-image")
        self.assertEqual(FAL_MODEL_MAP["recraft-v4-pro"], "fal-ai/recraft/v4/pro/text-to-image")
        self.assertEqual(FAL_MODEL_MAP["ideogram-v3"], "fal-ai/ideogram/v3")

    def test_benchmark_generation_models_are_registered(self) -> None:
        self.assertEqual(FAL_MODEL_MAP["gpt-image-2"], "fal-ai/gpt-image-2")
        self.assertEqual(FAL_MODEL_MAP["gpt-image-1.5"], "fal-ai/gpt-image-1.5")
        self.assertEqual(FAL_MODEL_MAP["flux-2-max"], "fal-ai/flux-2-max")
        self.assertEqual(FAL_MODEL_MAP["flux-2-pro"], "fal-ai/flux-2-pro")
        self.assertEqual(FAL_MODEL_MAP["seedream-v4"], "fal-ai/bytedance/seedream/v4/text-to-image")

    def test_infer_input_shape_detects_first_last_frame(self) -> None:
        shape = infer_input_shape(
            {"first_frame_url": "https://example.com/start.png", "last_frame_url": "https://example.com/end.png"}
        )
        self.assertEqual(shape, "first+last_frame")

    def test_route_selection_defaults_to_gpt_image_2_for_generic_prompts(self) -> None:
        selection = resolve_route_selection("image", prompt="una ilustracion minimalista de un gato naranja")
        self.assertEqual(selection["route_id"], "image-gpt-image-2-quality")
        self.assertEqual(selection["provider"], "fal")
        self.assertEqual(selection["model_key"], "gpt-image-2")

    def test_route_selection_uses_nano_banana_2_for_balanced_iteration(self) -> None:
        selection = resolve_route_selection(
            "image",
            prompt="rapid iteration on a social post concept",
            requested={"goal": "balanced"},
        )
        self.assertEqual(selection["route_id"], "image-balanced-premium")
        self.assertEqual(selection["model_key"], "nano-banana-2")

    def test_route_selection_escalates_to_nano_banana_pro_on_premium_intent(self) -> None:
        # Premium intent keywords trigger pro escalation.
        selection = resolve_route_selection("image", prompt="luxury editorial hero shot of a watch for magazine print")
        self.assertEqual(selection["model_key"], "gpt-image-2")

    def test_route_selection_escalates_to_pro_on_explicit_best_quality_goal(self) -> None:
        selection = resolve_route_selection(
            "image",
            prompt="una ilustracion de un gato",
            requested={"goal": "best_quality"},
        )
        self.assertEqual(selection["model_key"], "gpt-image-2")

    def test_route_selection_supports_gpt_image_2_quality_lane(self) -> None:
        selection = resolve_route_selection("image", route_id="image-gpt-image-2-quality")
        self.assertEqual(selection["route_id"], "image-gpt-image-2-quality")
        self.assertEqual(selection["model_key"], "gpt-image-2")

    def test_route_selection_supports_gpt_image_1_5_high_lane(self) -> None:
        selection = resolve_route_selection("image", route_id="image-gpt-image-1-5-high")
        self.assertEqual(selection["route_id"], "image-gpt-image-1-5-high")
        self.assertEqual(selection["model_key"], "gpt-image-1.5")

    def test_route_selection_supports_flux_2_max_generate_lane(self) -> None:
        selection = resolve_route_selection("image", route_id="image-flux-2-max-generate")
        self.assertEqual(selection["route_id"], "image-flux-2-max-generate")
        self.assertEqual(selection["model_key"], "flux-2-max")

    def test_route_selection_supports_flux_2_pro_generate_lane(self) -> None:
        selection = resolve_route_selection("image", route_id="image-flux-2-pro-generate")
        self.assertEqual(selection["route_id"], "image-flux-2-pro-generate")
        self.assertEqual(selection["model_key"], "flux-2-pro")

    def test_route_selection_supports_seedream_v4_generate_lane(self) -> None:
        selection = resolve_route_selection("image", route_id="image-seedream-v4-generate")
        self.assertEqual(selection["route_id"], "image-seedream-v4-generate")
        self.assertEqual(selection["model_key"], "seedream-v4")

    def test_prompt_compiler_layers_nano_banana_prompts(self) -> None:
        compiled = compile_prompt(
            "cyberpunk girl walking in neon rain, cinematic shot, express loneliness with cool blue",
            media_type="image",
            model_key="nano-banana-2",
            route_id="image-balanced-premium",
        )
        self.assertTrue(compiled["compiler_trace"]["applied"])
        self.assertEqual(compiled["compiler_trace"]["strategy"], "nano-banana-layered")
        self.assertEqual(compiled["compiler_trace"]["recipe"], "general")
        self.assertEqual(compiled["compiler_trace"]["operation_class"], "image_generate")
        self.assertIn("Primary brief:", compiled["prompt"])
        self.assertIn("Color and mood:", compiled["prompt"])
        self.assertIn("Avoid:", compiled["prompt"])

    def test_prompt_compiler_selects_hero_product_recipe_for_nano_banana(self) -> None:
        compiled = compile_prompt(
            "luxury product shot of a perfume bottle on black marble with brushed steel cap",
            media_type="image",
            model_key="nano-banana-pro",
            route_id="image-default-best-quality",
        )
        self.assertEqual(compiled["compiler_trace"]["recipe"], "hero-product")
        self.assertIn("Recipe: product hero image", compiled["prompt"])

    def test_prompt_compiler_selects_social_recipe_for_nano_banana(self) -> None:
        compiled = compile_prompt(
            "instagram promo graphic for a summer launch with one shoe and bold CTA",
            media_type="image",
            model_key="nano-banana-2",
            route_id="image-balanced-premium",
        )
        self.assertEqual(compiled["compiler_trace"]["recipe"], "social-marketing")
        self.assertIn("optimized for instant scanability", compiled["prompt"])

    def test_prompt_compiler_keeps_structured_prompts_for_generate_lanes(self) -> None:
        compiled = compile_prompt(
            "Scene: cyberpunk alley\nLighting: neon rain\nCamera: medium full body shot",
            media_type="image",
            model_key="nano-banana-pro",
            route_id="image-default-best-quality",
        )
        self.assertFalse(compiled["compiler_trace"]["applied"])
        self.assertEqual(compiled["compiler_trace"]["reason"], "already_structured")

    def test_prompt_compiler_adds_preservation_clause_for_kontext(self) -> None:
        compiled = compile_prompt(
            "replace the label with 'Nightlife', keep same framing",
            media_type="image",
            model_key="flux-kontext-pro",
            route_id="image-conservative-edit",
            routing={"operation": "edit", "goal": "preserve_layout"},
        )
        self.assertTrue(compiled["compiler_trace"]["applied"])
        self.assertEqual(compiled["compiler_trace"]["strategy"], "kontext-edit-precision")
        self.assertEqual(compiled["compiler_trace"]["recipe"], "conservative-product-edit")
        self.assertEqual(compiled["compiler_trace"]["operation_class"], "image_edit")
        self.assertIn("Keep the original framing, composition, subject scale", compiled["prompt"])
        self.assertIn("Keep everything else unchanged", compiled["prompt"])

    def test_prompt_compiler_structures_ideogram_typography_briefs(self) -> None:
        compiled = compile_prompt(
            'poster for a boxing event with headline "NIGHT FIGHT"',
            media_type="image",
            model_key="ideogram-v3",
            route_id="image-typography-poster",
        )
        self.assertTrue(compiled["compiler_trace"]["applied"])
        self.assertEqual(compiled["compiler_trace"]["strategy"], "ideogram-structured")
        self.assertEqual(compiled["compiler_trace"]["recipe"], "poster-typography")
        self.assertIn("quoted wording exactly", compiled["prompt"])

    def test_prompt_compiler_bypasses_strict_inpaint(self) -> None:
        compiled = compile_prompt(
            "remove the cards",
            media_type="image",
            model_key="bria-eraser",
            route_id="image-strict-inpaint",
        )
        self.assertFalse(compiled["compiler_trace"]["applied"])
        self.assertEqual(compiled["compiler_trace"]["reason"], "strict_inpaint_prompt_passthrough")
        self.assertEqual(compiled["compiler_trace"]["operation_class"], "image_inpaint")

    def test_prompt_compiler_structures_kling_video_prompts(self) -> None:
        compiled = compile_prompt(
            "ugc style video of a creator opening a sneaker box for instagram reels",
            media_type="video",
            model_key="kling",
            route_id="video-default-t2v",
        )
        self.assertTrue(compiled["compiler_trace"]["applied"])
        self.assertEqual(compiled["compiler_trace"]["strategy"], "kling-video-sequenced")
        self.assertEqual(compiled["compiler_trace"]["recipe"], "ugc-social-video")
        self.assertEqual(compiled["compiler_trace"]["operation_class"], "video_generate")
        self.assertIn("Shot 1, Shot 2, Shot 3", compiled["prompt"])

    def test_prompt_compiler_structures_seedance_reference_video_prompts(self) -> None:
        compiled = compile_prompt(
            "@Image1 is the hero product, @Image2 is the mood board, camera slowly orbits the bottle",
            media_type="video",
            model_key="seedance2-reference",
            route_id="video-multi-reference-direction",
            params={"image_urls": ["https://example.com/1.png", "https://example.com/2.png"]},
        )
        self.assertTrue(compiled["compiler_trace"]["applied"])
        self.assertEqual(compiled["compiler_trace"]["strategy"], "seedance-reference-aware")
        self.assertEqual(compiled["compiler_trace"]["recipe"], "reference-driven-motion")
        self.assertEqual(compiled["compiler_trace"]["operation_class"], "video_reference")
        self.assertIn("@Image1, @Image2, @Video1, @Audio1", compiled["prompt"])

    def test_prompt_compiler_structures_sora_video_prompts(self) -> None:
        compiled = compile_prompt(
            "two armored knights collide and slide across wet stone, sparks and debris flying",
            media_type="video",
            model_key="sora2",
            route_id="video-physics-realism",
        )
        self.assertTrue(compiled["compiler_trace"]["applied"])
        self.assertEqual(compiled["compiler_trace"]["strategy"], "sora-storyboard-brief")
        self.assertEqual(compiled["compiler_trace"]["recipe"], "physics-realism")
        self.assertIn("briefing a cinematographer", compiled["prompt"])

    def test_prompt_compiler_structures_veo_extend_prompts(self) -> None:
        compiled = compile_prompt(
            "continue this video as the car exits the tunnel into sunrise",
            media_type="video",
            model_key="veo3-extend",
            route_id="video-extend",
            params={"video_url": "https://example.com/clip.mp4"},
        )
        self.assertTrue(compiled["compiler_trace"]["applied"])
        self.assertEqual(compiled["compiler_trace"]["strategy"], "veo-sensory-cinematic")
        self.assertEqual(compiled["compiler_trace"]["recipe"], "extend-existing-video")
        self.assertEqual(compiled["compiler_trace"]["operation_class"], "video_extend")
        self.assertIn("continue motion naturally", compiled["prompt"])

    def test_prompt_compiler_structures_lipsync_prompts(self) -> None:
        compiled = compile_prompt(
            "make this person speak naturally to the provided dialogue track",
            media_type="video",
            model_key="sync-lipsync",
            route_id="video-lipsync",
            params={
                "video_url": "https://example.com/clip.mp4",
                "audio_url": "https://example.com/voice.wav",
            },
        )
        self.assertTrue(compiled["compiler_trace"]["applied"])
        self.assertEqual(compiled["compiler_trace"]["strategy"], "lipsync-preserve")
        self.assertEqual(compiled["compiler_trace"]["recipe"], "dialogue-lipsync")
        self.assertEqual(compiled["compiler_trace"]["operation_class"], "video_lipsync")
        self.assertIn("Apply precise lipsync", compiled["prompt"])

    def test_operation_class_resolves_explicit_categories(self) -> None:
        self.assertEqual(resolve_operation_class("image", "image-balanced-premium", {}), "image_generate")
        self.assertEqual(resolve_operation_class("image", "image-conservative-edit", {"image_url": "x"}), "image_edit")
        self.assertEqual(resolve_operation_class("image", "image-strict-inpaint", {"image_url": "x"}), "image_inpaint")
        self.assertEqual(resolve_operation_class("video", "video-default-t2v", {}), "video_generate")
        self.assertEqual(resolve_operation_class("video", "video-multi-reference-direction", {"image_urls": ["x"]}), "video_reference")
        self.assertEqual(resolve_operation_class("video", "video-extend", {"video_url": "x"}), "video_extend")
        self.assertEqual(resolve_operation_class("video", "video-lipsync", {"video_url": "x", "audio_url": "y"}), "video_lipsync")

    def test_route_selection_picks_conservative_edit_for_layout_preservation(self) -> None:
        selection = resolve_route_selection(
            "image",
            prompt="keep same framing and preserve layout, only change the bottle label",
            params={"image_url": "https://example.com/source.png"},
            requested={"operation": "edit", "goal": "preserve_layout"},
        )
        self.assertEqual(selection["route_id"], "image-conservative-edit")

    def test_route_selection_picks_strong_lookdev_edit_for_cinematic_quality_pass(self) -> None:
        selection = resolve_route_selection(
            "image",
            prompt="make the lighting cinematic with raytracing, premium color grade and realistic reflections",
            params={"image_url": "https://example.com/source.png"},
            requested={"operation": "edit"},
        )
        self.assertEqual(selection["route_id"], "image-strong-lookdev-edit")
        self.assertEqual(selection["model_key"], "gpt-image-2")

    def test_route_selection_picks_strong_lookdev_edit_on_explicit_best_quality_goal(self) -> None:
        selection = resolve_route_selection(
            "image",
            prompt="improve the image with richer movie lighting and cleaner materials",
            params={"image_url": "https://example.com/source.png"},
            requested={"operation": "edit", "goal": "best_quality"},
        )
        self.assertEqual(selection["route_id"], "image-strong-lookdev-edit")
        self.assertEqual(selection["model_key"], "gpt-image-2")

    def test_route_selection_uses_nano_banana_pro_for_fintech_luxury_polish(self) -> None:
        selection = resolve_route_selection(
            "image",
            prompt="mejora la iluminacion para que se vea mas premium fintech, con sombras sutiles y reflejos refinados",
            params={"image_url": "https://example.com/source.png"},
            requested={"operation": "edit", "goal": "best_quality"},
        )
        self.assertEqual(selection["route_id"], "image-strong-lookdev-edit")
        self.assertEqual(selection["model_key"], "gpt-image-2")

    def test_route_selection_keeps_seedream_for_structural_restyle_not_polish(self) -> None:
        selection = resolve_route_selection(
            "image",
            prompt="restyle this clip art, replace the dashboard cards with wireframe particles and change the visual language",
            params={"image_url": "https://example.com/source.png"},
            requested={"operation": "edit"},
        )
        self.assertEqual(selection["route_id"], "image-high-end-edit")
        self.assertEqual(selection["model_key"], "seedream-edit")

    def test_route_selection_picks_video_upscale_for_quality_enhancement(self) -> None:
        selection = resolve_route_selection(
            "video",
            prompt="mejorar la calidad del video, se ve mala calidad y comprimido",
            params={"video_url": "https://example.com/clip.mp4"},
            requested={"operation": "edit", "goal": "best_quality"},
        )
        self.assertEqual(selection["route_id"], "video-enhance-upscale")
        self.assertEqual(selection["model_key"], "video-upscale")

    def test_old_premium_route_alias_still_resolves(self) -> None:
        selection = resolve_route_selection(
            "image",
            route_id="image-premium-lookdev-edit",
        )
        self.assertEqual(selection["route_id"], "image-strong-lookdev-edit")
        self.assertEqual(selection["model_key"], "gpt-image-2")

    def test_route_selection_keeps_subtractive_edit_in_conservative_lane(self) -> None:
        selection = resolve_route_selection(
            "image",
            prompt="remove the cards and keep the same composition, same framing, solo la imagen",
            params={"image_url": "https://example.com/source.png"},
            requested={"operation": "edit", "goal": "preserve_layout"},
        )
        self.assertEqual(selection["route_id"], "image-conservative-edit")

    def test_strict_preservation_detects_original_format_requests(self) -> None:
        self.assertTrue(
            requires_strict_preservation(
                "image",
                prompt="manten el formato original, no toques la esfera y solo cambia la textura del fondo",
                params={"image_url": "https://example.com/source.png"},
                requested={"operation": "edit", "goal": "preserve_layout"},
            )
        )

    def test_explicit_flexible_route_is_rejected_when_original_format_is_required(self) -> None:
        with self.assertRaisesRegex(ValueError, "Strict preservation requested"):
            resolve_route_selection(
                "image",
                prompt="keep original format and same composition, only change background texture",
                params={"image_url": "https://example.com/source.png"},
                route_id="image-high-end-edit",
                requested={"operation": "edit", "goal": "preserve_layout"},
            )

    def test_validate_route_constraints_allows_strict_lane(self) -> None:
        route = next(route for route in ROUTING_SCHEMA["image"] if route["route_id"] == "image-conservative-edit")
        validate_route_constraints(
            "image",
            route,
            prompt="mismo formato, no toques la esfera, solo cambia la textura de la plataforma",
            params={"image_url": "https://example.com/source.png"},
            requested={"operation": "edit", "goal": "preserve_layout"},
        )

    def test_strict_inpaint_lanes_are_registered(self) -> None:
        self.assertEqual(FAL_MODEL_MAP["bria-eraser"], "fal-ai/bria/eraser")
        self.assertEqual(FAL_MODEL_MAP["flux-inpaint"], "fal-ai/flux-general/inpainting")
        self.assertEqual(FAL_MODEL_MAP["flux-fill-pro"], "fal-ai/flux-pro/v1/fill")

    def test_strict_preservation_with_mask_routes_to_strict_inpaint(self) -> None:
        selection = resolve_route_selection(
            "image",
            prompt="borra las cards, mantén el mismo formato y composición",
            params={
                "image_url": "https://example.com/source.png",
                "mask_url": "https://example.com/mask.png",
            },
            requested={"operation": "edit", "goal": "preserve_layout"},
        )
        self.assertEqual(selection["route_id"], "image-strict-inpaint")
        self.assertEqual(selection["provider"], "fal")
        self.assertEqual(selection["model_key"], "bria-eraser")

    def test_strict_preservation_without_mask_falls_back_to_conservative(self) -> None:
        selection = resolve_route_selection(
            "image",
            prompt="remove the cards and keep the same composition, same framing, solo la imagen",
            params={"image_url": "https://example.com/source.png"},
            requested={"operation": "edit", "goal": "preserve_layout"},
        )
        # Without a mask, strict-inpaint is penalized; conservative-edit wins.
        self.assertEqual(selection["route_id"], "image-conservative-edit")

    def test_relight_intent_routes_to_iclight_when_operation_is_explicit(self) -> None:
        selection = resolve_route_selection(
            "image",
            prompt=(
                "agrega sombra de ventana al laptop, mismo encuadre, no cambies la composicion"
            ),
            params={"image_url": "https://example.com/laptop.png"},
            requested={"operation": "relight"},
        )
        self.assertEqual(selection["route_id"], "image-relight")
        self.assertEqual(selection["model_key"], "iclight-v2")
        self.assertEqual(selection["provider"], "fal")

    def test_relight_keywords_alone_do_not_outrank_conservative_edit(self) -> None:
        # Without explicit operation="relight", "sombra de ventana" is a
        # compositional edit, not a specialist relight call. Keep the validated
        # conservative-edit lane (flux-kontext-pro) as the primary route.
        selection = resolve_route_selection(
            "image",
            prompt=(
                "agrega un efecto de luz/sombra de ventana al laptop, mismo encuadre"
            ),
            params={"image_url": "https://example.com/laptop.png"},
            requested={"operation": "edit", "goal": "preserve_layout"},
        )
        self.assertEqual(selection["route_id"], "image-conservative-edit")

    def test_relight_keywords_do_not_hijack_minimal_edit_call(self) -> None:
        # Regression guard for the "sombra de ventana" NO_REPLY incident.
        # A minimal caller that only sets operation="edit" (no goal hint, no
        # "mismo encuadre" phrase) and a short relight-flavored prompt must
        # still land on image-conservative-edit, not image-relight. Explicit
        # operation overrides keyword gravity.
        selection = resolve_route_selection(
            "image",
            prompt="agrega sombra de ventana",
            params={"image_url": "https://example.com/laptop.png"},
            requested={"operation": "edit"},
        )
        self.assertEqual(selection["route_id"], "image-conservative-edit")
        self.assertEqual(selection["model_key"], "flux-kontext-pro")

    def test_relight_lane_is_registered(self) -> None:
        self.assertEqual(FAL_MODEL_MAP["iclight-v2"], "fal-ai/iclight-v2")

    def test_route_selection_avoids_conservative_edit_for_structural_replacement(self) -> None:
        selection = resolve_route_selection(
            "image",
            prompt=(
                "replace the particles with wireframe task cards, calls, and emails, "
                "keep the same horizontal composition"
            ),
            params={"image_url": "https://example.com/source.png"},
            requested={"operation": "edit"},
        )
        self.assertEqual(selection["route_id"], "image-high-end-edit")

    def test_route_selection_picks_lipsync_when_video_and_audio_are_present(self) -> None:
        selection = resolve_route_selection(
            "video",
            prompt="make this person speak with precise lipsync",
            params={
                "video_url": "https://example.com/clip.mp4",
                "audio_url": "https://example.com/voice.wav",
            },
            requested={"operation": "lipsync", "audio_requirement": "required"},
        )
        self.assertEqual(selection["route_id"], "video-lipsync")

    def test_route_selection_supports_explicit_route_id(self) -> None:
        selection = resolve_route_selection("tool", route_id="tool-caption")
        self.assertEqual(selection["route_id"], "tool-caption")
        self.assertEqual(selection["provider"], "piapi")
        self.assertEqual(selection["task_type"], "joycaption-beta-one")

    def test_generated_docs_include_current_defaults(self) -> None:
        skill = (ROOT / "SKILL.md").read_text()
        catalog = (ROOT / "references" / "model-catalog.md").read_text()
        routing_table = (ROOT / "references" / "routing-table.md").read_text()
        routing_schema = (ROOT / "references" / "routing-schema.md").read_text()
        self.assertIn("nano-banana-2", skill)
        self.assertIn("nano-banana-pro", skill)
        self.assertIn("fal-ai/sora-2/text-to-video/pro", skill)
        self.assertIn("fal-ai/veo3.1/fast", skill)
        self.assertIn("mantener formato original", skill)
        self.assertIn("Default image model: **GPT Image 2 / ChatGPT Images 2.0** (`gpt-image-2`)", catalog)
        self.assertIn("gpt-image-2", catalog)
        self.assertIn("gpt-image-1.5", catalog)
        self.assertIn("flux-2-max", catalog)
        self.assertIn("flux-2-pro", catalog)
        self.assertIn("seedream-v4", catalog)
        self.assertIn("xai/grok-imagine-image", catalog)
        self.assertIn("flux-2-max-edit", catalog)
        self.assertIn("sync-lipsync", routing_table)
        self.assertIn("strict preservation lane only", routing_table)
        self.assertIn("image-gpt-image-1-5-high", routing_schema)
        self.assertIn("image-gpt-image-2-quality", routing_schema)
        self.assertIn("image-flux-2-max-generate", routing_schema)
        self.assertIn("image-flux-2-pro-generate", routing_schema)
        self.assertIn("image-seedream-v4-generate", routing_schema)
        self.assertIn("image-strong-lookdev-edit", routing_schema)
        self.assertIn("image-default-best-quality", routing_schema)
        self.assertIn("video-lipsync", routing_schema)

    def test_skill_guidance_is_routing_first(self) -> None:
        skill = (ROOT / "SKILL.md").read_text()
        self.assertIn("--route-id <route_id>", skill)
        self.assertIn("omitir `provider` y `model`", skill)
        self.assertIn('"route_id": "image-conservative-edit"', skill)


if __name__ == "__main__":
    unittest.main()
