#!/usr/bin/env python3
"""Render ai-gen-max markdown docs from model_manifest.py."""

from __future__ import annotations

from pathlib import Path

from model_manifest import (
    CATALOG_IMAGE_ROWS,
    CATALOG_VIDEO_ROWS,
    DEFAULT_IMAGE_LABEL,
    DEFAULT_IMAGE_MODEL_ID,
    DEFAULT_IMAGE_MODEL_KEY,
    DOC_VALIDATED_AT,
    FAL_DOC_LINKS,
    FAL_MODEL_MAP,
    PIAPI_MODEL_MAP,
    SKILL_DOC_SECTIONS,
    ROUTING_DECISION_DIMENSIONS,
    ROUTING_SCHEMA,
)


ROOT = Path(__file__).resolve().parents[1]
SKILL_PATH = ROOT / "SKILL.md"
CATALOG_PATH = ROOT / "references" / "model-catalog.md"
ROUTING_TABLE_PATH = ROOT / "references" / "routing-table.md"
ROUTING_SCHEMA_PATH = ROOT / "references" / "routing-schema.md"


def table(headers: list[str], rows: list[tuple[str, ...]]) -> str:
    def esc(cell: str) -> str:
        return cell.replace("|", "\\|")

    head = "| " + " | ".join(headers) + " |"
    sep = "| " + " | ".join(["---"] * len(headers)) + " |"
    body = ["| " + " | ".join(esc(col) for col in row) + " |" for row in rows]
    return "\n".join([head, sep, *body])


def bullet_list(items: list[str]) -> str:
    return "\n".join(f"- {item}" for item in items)


def render_route_card(route: dict[str, object]) -> str:
    model_key = str(route["model_key"])
    piapi_model = PIAPI_MODEL_MAP.get(model_key, {}).get("model")
    model_id = FAL_MODEL_MAP.get(model_key, piapi_model or model_key)
    fallback_model_keys = [str(item) for item in route.get("fallback_model_keys", [])]
    lines = [
        f"### `{route['route_id']}`",
        "",
        f"- Model key: `{model_key}`",
        f"- Provider: `{route['provider']}`",
        f"- Resolved model/endpoint: `{model_id}`",
        f"- Operation: `{route['operation']}`",
        f"- Goal: `{route['goal']}`",
        f"- Input shape: `{route['input_shape']}`",
        f"- Fidelity priority: `{route['fidelity_priority']}`",
        f"- Quality tier: `{route['quality_tier']}`",
    ]
    if route.get("audio_requirement"):
        lines.append(f"- Audio requirement: `{route['audio_requirement']}`")
    lines.extend(
        [
            "- Use when:",
            *[f"  - {item}" for item in route.get("use_when", [])],
            "- Avoid when:",
            *[f"  - {item}" for item in route.get("avoid_when", [])],
            f"- Keywords: {', '.join(f'`{item}`' for item in route.get('keywords', [])) or 'none'}",
            f"- Fallbacks: {', '.join(f'`{item}`' for item in fallback_model_keys) or 'none'}",
            "",
        ]
    )
    return "\n".join(lines)


def render_skill() -> str:
    image_rows = [(tier, f"`{model}`", price) for tier, model, price in SKILL_DOC_SECTIONS["image"]]
    video_rows = [(tier, f"`{model}`", price) for tier, model, price in SKILL_DOC_SECTIONS["video_t2v"]]

    return f"""---
name: ai-gen-max
description: |
  Intelligent AI media generation router. Use when the user wants to generate images, videos, audio, music, 3D models, or use media tools.
user-invocable: true
argument-hint: <prompt> [--type image|video|audio|music|3d|tool] [--route-id <route_id>] [--operation <operation>] [--goal <goal>] [--image <path_or_url>] [--duration <seconds>] [--aspect <ratio>] [--audio] [--model <name> only-as-override] [--provider <name> only-as-override]
allowed-tools:
  - Bash(python3 *)
  - Bash(mkdir -p *)
  - Bash(find *)
  - Bash(cat *)
  - Read
---

# AI GEN MAX — Intelligent Media Generation Router

Generador multi-provider con fuente de verdad en `scripts/model_manifest.py`.

Validado contra documentación oficial de `fal.ai`: **{DOC_VALIDATED_AT}**

## Defaults vigentes

- Imagen default: **{DEFAULT_IMAGE_LABEL}** → `{DEFAULT_IMAGE_MODEL_KEY}` → `{DEFAULT_IMAGE_MODEL_ID}`
- Video T2V default: **Kling 3.0** → `kling`
- `sora2` y `sora2-pro` son tiers distintos también en fal:
  - `sora2` → `fal-ai/sora-2/text-to-video`
  - `sora2-pro` → `fal-ai/sora-2/text-to-video/pro`

## IMAGEN

{table(["Tier / intención", "model key", "Precio"], image_rows)}

## VIDEO T2V

{table(["Tier / intención", "model key", "Precio"], video_rows)}

## Reglas cardinales

- Priorizar `gpt-image-2` para imagen general cuando la meta sea **el mejor resultado visual posible**.
- Bajar a `nano-banana-2` cuando el prompt no necesite esa agresividad estética o cuando el costo/velocidad importen más.
- Usar `nano-banana-pro` como fallback premium o cuando se quiera específicamente el look Nano Banana.
- Si el usuario prioriza **edición conservadora**, usar `flux-kontext-pro`.
- Si el usuario pide **quitar elementos** pero mantener **encuadre/composición idénticos**, tratarlo como `preserve_layout`, no como `restyle`.
- Si el usuario pide **mantener formato original**, eso se interpreta como bloqueo duro: no cambiar aspect ratio, framing, composition, camera angle ni geometría general.
- Si existe máscara o semántica de inpaint disponible upstream, preferir esa operación para sustracción exacta sobre un edit generativo libre.
- Si una lane no ofrece preservación estricta y el prompt exige mantener el original, esa lane debe rechazarse aunque parezca “más bonita”.
- Si el prompt menciona un modelo explícito, respetarlo salvo que no exista para ese lane.
- No priorizar lanes por una capacidad aislada; priorizarlos por calidad final del resultado salvo que el pedido exija una especialidad concreta.

## Contrato de invocación

- El caller upstream debe preferir `media_type` + `routing` y **omitir `provider` y `model`** salvo que el usuario pida un override explícito.
- Si ya sabes exactamente la lane correcta, manda `route_id` y deja que `generate.py` resuelva `provider`, `model` y `task_type`.

### Payload canónico

```json
{{
  "media_type": "image",
  "params": {{
    "prompt": "Luxury editorial hero shot of a watch",
    "aspect_ratio": "16:9"
  }},
  "routing": {{
    "operation": "generate",
    "goal": "best_quality"
  }}
}}
```

### Cuando ya conoces la lane

```json
{{
  "media_type": "image",
  "params": {{
    "prompt": "Keep same framing and only change the bottle label",
    "image_url": "/abs/path/source.png"
  }},
  "route_id": "image-conservative-edit"
}}
```

## Evidencia fal.ai usada para fijar defaults

- Nano Banana Pro: {FAL_DOC_LINKS["nano-banana-pro"]}
- Nano Banana 2: {FAL_DOC_LINKS["nano-banana-2"]}
- GPT Image 2 / ChatGPT Images 2.0: {FAL_DOC_LINKS["gpt-image-2"]}
- GPT Image 2 API: {FAL_DOC_LINKS["gpt-image-2-api"]}
- GPT Image 2 prompting: {FAL_DOC_LINKS["gpt-image-2-prompting"]}
- Sora 2 T2V: {FAL_DOC_LINKS["sora2"]}
- Sora 2 Pro T2V: {FAL_DOC_LINKS["sora2-pro"]}
- Sora 2 I2V: {FAL_DOC_LINKS["sora2-image-to-video"]}
- Sora 2 Pro I2V: {FAL_DOC_LINKS["sora2-pro-image-to-video"]}

## Lanes nuevas verificadas en fal.ai

- Sora 2 Remix: {FAL_DOC_LINKS["sora2-remix"]}
- Seedance 2 Reference-to-Video: {FAL_DOC_LINKS["seedance2-reference"]}
- Veo 3.1 Fast: {FAL_DOC_LINKS["veo3-fast"]}
- Veo 3.1 I2V: {FAL_DOC_LINKS["veo3-image-to-video"]}
- Veo 3.1 Reference: {FAL_DOC_LINKS["veo3-reference-to-video"]}
- Veo 3.1 First/Last Frame: {FAL_DOC_LINKS["veo3-first-last"]}
- Veo 3.1 Extend: {FAL_DOC_LINKS["veo3-extend"]}
- Grok Imagine Image / Edit: {FAL_DOC_LINKS["grok-imagine-image"]}
- Grok Imagine Video: {FAL_DOC_LINKS["grok-imagine-video"]}
- PixVerse V6 I2V: {FAL_DOC_LINKS["pixverse-v6-i2v"]}
- PixVerse Transition: {FAL_DOC_LINKS["pixverse-transition"]}
- PixVerse Extend: {FAL_DOC_LINKS["pixverse-extend"]}
- Sync Lipsync v3: {FAL_DOC_LINKS["sync-lipsync"]}
- Seedream Edit: {FAL_DOC_LINKS["seedream-edit"]}
- WAN 2.7 Edit: {FAL_DOC_LINKS["wan27-edit"]}

## Maintenance

- Ejecutar `python3 scripts/render_docs.py` después de cambiar el manifiesto.
- Ejecutar `python3 scripts/test_manifest.py` antes de cerrar cambios.
"""


def render_catalog() -> str:
    image_rows = [(name, f"`{key}`", f"`{model_id}`", price, lane) for name, key, model_id, price, lane in CATALOG_IMAGE_ROWS]
    video_rows = [(name, f"`{key}`", f"`{model_id}`", price, lane) for name, key, model_id, price, lane in CATALOG_VIDEO_ROWS]
    return f"""# AI GEN MAX — Model Catalog

Generated from `scripts/model_manifest.py`.
Validated against official `fal.ai` docs on **{DOC_VALIDATED_AT}**.

## Current invariants

- Default image model: **{DEFAULT_IMAGE_LABEL}** (`{DEFAULT_IMAGE_MODEL_KEY}`)
- Default image endpoint: `{DEFAULT_IMAGE_MODEL_ID}`
- `sora2` standard and `sora2-pro` do **not** share the same fal endpoint.

## Image

{table(["Model", "model key", "fal model ID", "Price", "Primary lane"], image_rows)}

## Video

{table(["Model", "model key", "fal model ID", "Price", "Primary lane"], video_rows)}

## Official references

- Nano Banana Pro: {FAL_DOC_LINKS["nano-banana-pro"]}
- Nano Banana 2: {FAL_DOC_LINKS["nano-banana-2"]}
- GPT Image 2 / ChatGPT Images 2.0: {FAL_DOC_LINKS["gpt-image-2"]}
- FLUX.1 [dev]: {FAL_DOC_LINKS["flux-dev"]}
- Sora 2 text-to-video: {FAL_DOC_LINKS["sora2"]}
- Sora 2 Pro text-to-video: {FAL_DOC_LINKS["sora2-pro"]}
"""


def render_routing_table() -> str:
    image_rows = []
    for route in ROUTING_SCHEMA["image"]:
        image_rows.append(
            (
                str(route["goal"]),
                f"`{route['model_key']}`",
                f"`{route['input_shape']}`",
                "; ".join(str(item) for item in route["use_when"][:2]),
            )
        )

    video_rows = []
    for route in ROUTING_SCHEMA["video"]:
        video_rows.append(
            (
                str(route["goal"]),
                f"`{route['model_key']}`",
                f"`{route['input_shape']}`",
                "; ".join(str(item) for item in route["use_when"][:2]),
            )
        )

    return f"""# AI GEN MAX — Routing Table

Source of truth for live model IDs/defaults/schema: `scripts/model_manifest.py`

Operator-facing summary generated from the manifest on **{DOC_VALIDATED_AT}**.

## Routing posture

- Keep `gpt-image-2` as the default quality-first image lane when the job is general image generation and the target is the strongest possible output.
- Keep `nano-banana-2` as the fast workhorse when the job values iteration speed/cost over the quality ceiling.
- Keep `kling` as the default text-to-video lane when the job is general motion with no specialist constraint.
- Upgrade to specialist lanes only when the brief has a clear constraint: typography, vector, preserve-layout edit, multi-reference direction, physics realism, stylized social motion, lipsync, or utility tooling.
- Prefer explicit route IDs over hand-wavy "best model" language. The schema exists to turn intent into a repeatable choice, not to debate vibes every time.

## Image routing

{table(["Goal / lane", "model key", "input shape", "Primary trigger"], image_rows)}

## Video routing

{table(["Goal / lane", "model key", "input shape", "Primary trigger"], video_rows)}

## Decision heuristics

- `logo`, `icon`, `brand`, `svg`, `vector` -> `recraft-v3`
- `poster`, `headline`, `banner`, `text in image`, `typography` -> `ideogram-v2`
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
"""


def render_routing_schema() -> str:
    dims = "\n".join(f"- `{name}`: {desc}" for name, desc in ROUTING_DECISION_DIMENSIONS)
    sections: list[str] = [
        "# AI GEN MAX — Routing Schema",
        "",
        "Canonical schema generated from `scripts/model_manifest.py`.",
        f"Validated / refreshed on **{DOC_VALIDATED_AT}**.",
        "",
        "## Decision dimensions",
        "",
        dims,
        "",
        "## Schema",
        "",
    ]
    for media_type, routes in ROUTING_SCHEMA.items():
        sections.append(f"## {media_type.upper()}")
        sections.append("")
        sections.extend(render_route_card(route) for route in routes)
    return "\n".join(sections)


def main() -> None:
    SKILL_PATH.write_text(render_skill())
    CATALOG_PATH.write_text(render_catalog())
    ROUTING_TABLE_PATH.write_text(render_routing_table())
    ROUTING_SCHEMA_PATH.write_text(render_routing_schema())


if __name__ == "__main__":
    main()
