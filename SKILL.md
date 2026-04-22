---
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

Validado contra documentación oficial de `fal.ai`: **2026-04-21**

## Defaults vigentes

- Imagen default: **GPT Image 2 / ChatGPT Images 2.0** → `gpt-image-2` → `fal-ai/gpt-image-2`
- Video T2V default: **Kling 3.0** → `kling`
- `sora2` y `sora2-pro` son tiers distintos también en fal:
  - `sora2` → `fal-ai/sora-2/text-to-video`
  - `sora2-pro` → `fal-ai/sora-2/text-to-video/pro`

## IMAGEN

| Tier / intención | model key | Precio |
| --- | --- | --- |
| budget | `flux-schnell` | $0.003/MP |
| standard | `flux-dev` | $0.025/MP |
| DEFAULT / quality-first benchmark leader | `gpt-image-2` | $0.01-$0.41/img |
| workhorse / fast iteration | `nano-banana-2` | $0.08/img |
| premium fallback / Nano Banana look | `nano-banana-pro` | $0.15/img |
| legacy prompt-adherence lane | `gpt-image-1.5` | from $0.009/img + tokens |
| zero-config production consistency | `flux-2-pro` | $0.030/MP |
| maximum-quality FLUX.2 generation | `flux-2-max` | $0.070/MP |
| 4K-ready Seedream generation | `seedream-v4` | $0.03/img |
| vector / branding / SVG (producción-ready) | `recraft-v4-vector` | $0.08/img |
| tipografía / posters / texto en imagen | `ideogram-v3` | $0.04/img |
| edición con referencia | `flux-kontext-pro` | $0.04/img |
| premium lookdev edit / luxury polish pass | `gpt-image-2` | $0.01-$0.41/img |

## VIDEO T2V

| Tier / intención | model key | Precio |
| --- | --- | --- |
| budget | `hunyuan-fast` | $0.03/gen |
| DEFAULT | `kling` | $0.084/s |
| cinematic | `seedance2` | $0.30/s |
| premium | `sora2` | $0.10/s |
| premium+audio / long-form | `sora2-pro` | $0.30/s 720p \| $0.50/s 1080p |
| ultra | `veo3` | $0.10/s 720p/1080p \| $0.30/s 4k |
| ultra+audio | `veo3-hq` | see fal 3.1 pricing |

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

### Cuando ya conoces la lane

```json
{
  "media_type": "image",
  "params": {
    "prompt": "Keep same framing and only change the bottle label",
    "image_url": "/abs/path/source.png"
  },
  "route_id": "image-conservative-edit"
}
```

## Evidencia fal.ai usada para fijar defaults

- Nano Banana Pro: https://fal.ai/models/fal-ai/nano-banana-pro
- Nano Banana 2: https://fal.ai/models/fal-ai/nano-banana-2
- GPT Image 2 / ChatGPT Images 2.0: https://fal.ai/gpt-image-2
- GPT Image 2 API: https://fal.ai/models/openai/gpt-image-2/playground
- GPT Image 2 prompting: https://fal.ai/learn/tools/prompting-gpt-image-2
- Sora 2 T2V: https://fal.ai/models/fal-ai/sora-2/text-to-video
- Sora 2 Pro T2V: https://fal.ai/models/fal-ai/sora-2/text-to-video/pro
- Sora 2 I2V: https://fal.ai/models/fal-ai/sora-2/image-to-video
- Sora 2 Pro I2V: https://fal.ai/models/fal-ai/sora-2/image-to-video/pro

## Lanes nuevas verificadas en fal.ai

- Sora 2 Remix: https://fal.ai/models/fal-ai/sora-2/video-to-video/remix
- Seedance 2 Reference-to-Video: https://fal.ai/models/bytedance/seedance-2.0/reference-to-video
- Veo 3.1 Fast: https://fal.ai/models/fal-ai/veo3.1/fast
- Veo 3.1 I2V: https://fal.ai/models/fal-ai/veo3.1/image-to-video
- Veo 3.1 Reference: https://fal.ai/models/fal-ai/veo3.1/reference-to-video
- Veo 3.1 First/Last Frame: https://fal.ai/models/fal-ai/veo3.1/first-last-frame-to-video
- Veo 3.1 Extend: https://fal.ai/models/fal-ai/veo3.1/extend-video
- Grok Imagine Image / Edit: https://fal.ai/docs/model-api-reference/image-generation-api/xai-grok-imagine-image.md
- Grok Imagine Video: https://fal.ai/docs/model-api-reference/video-generation-api/xai-grok-imagine-video.md
- PixVerse V6 I2V: https://fal.ai/models/fal-ai/pixverse/v6/image-to-video
- PixVerse Transition: https://fal.ai/models/fal-ai/pixverse/v6/transition
- PixVerse Extend: https://fal.ai/models/fal-ai/pixverse/extend
- Sync Lipsync v3: https://fal.ai/models/fal-ai/sync-lipsync/v3
- Seedream Edit: https://fal.ai/models/fal-ai/bytedance/seedream/v4.5/edit
- WAN 2.7 Edit: https://fal.ai/models/fal-ai/wan/v2.7/edit

## Maintenance

- Ejecutar `python3 scripts/render_docs.py` después de cambiar el manifiesto.
- Ejecutar `python3 scripts/test_manifest.py` antes de cerrar cambios.
