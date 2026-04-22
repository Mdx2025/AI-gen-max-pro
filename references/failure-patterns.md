# AI GEN MAX — Failure Patterns

Casos reales donde una elección técnicamente razonable produjo un mal resultado.

El objetivo de este archivo es evitar repetir errores que ya pasaron en producción.

## 2026-04-19 — Damaged-composition reconstruction

### Brief real

El usuario no quería:

- upscale genérico
- reinterpretación estética
- una escena nueva inspirada en la original

El usuario quería:

- la **misma composición exacta**
- el mismo canvas y cámara
- la misma distribución de objetos
- pero reconstruida para verse limpia, sharp y actual

### Qué se probó

1. `tool-image-upscale` / Clarity
   - subió resolución
   - no resolvió el problema real porque la composición ya estaba dañada

2. `image-conservative-edit` / Flux Kontext Pro
   - mejoró claridad local
   - pero **reencuadró** la imagen
   - falló el preservation contract

3. `flux-fill-pro` con máscara amplia
   - preservó mejor el canvas
   - pero **rediseñó demasiado el objeto central**
   - el resultado se vio peor que la imagen base

4. `flux-fill-pro` con máscara más cerrada
   - mantuvo mejor el layout global
   - pero siguió alterando demasiado la estructura central
   - el usuario igual lo rechazó

### Lección

- "reconstruir esta misma composición" **no es lo mismo** que:
  - upscale
  - conservative edit
  - inpaint genérico
- Un modelo puede respetar el canvas y aun así fallar si rediseña la geometría importante dentro de la máscara.
- Para este tipo de trabajo, **preservar canvas no basta**. También importa preservar estructura.

### Regla operativa

No asumir que `flux-fill-pro` es una lane segura para prompts tipo:

- "rebuild this exact composition"
- "same shot, same structure"
- "fix damage without redesign"

Si el pedido exige reconstrucción fiel de una composición dañada:

- tratar `flux-fill-pro` como **high-risk**
- preferir warning explícito si no hay lane realmente segura
- o dividir el trabajo en pasos todavía más quirúrgicos

### Qué no hacer

- no vender un resultado como correcto solo porque quedó más sharp
- no asumir que broad masked reconstruction equivale a fidelity
- no repetir el mismo camino solo porque respeta el frame
