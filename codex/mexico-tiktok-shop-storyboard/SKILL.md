---
name: mexico-tiktok-shop-storyboard
description: Generate Mexico-localized TikTok Shop product short-video plans, including Chinese 3x3 storyboard scripts, Mexican Spanish voiceover suggestions, and confirmed second-stage English image-generation JSON. Use when the user asks for TikTok Shop, Mexico TikTok, Mexican cross-border ecommerce short videos, product selling storyboards, perfume short-video scripts, image prompts, product image-generation prompts, or 3x3 grid storyboards.
---

# Mexico TikTok Shop Storyboard

## Workflow

Use a two-stage workflow.

1. First output only the Chinese 9-shot 3x3 storyboard script and wait for the user to confirm, revise, or choose a direction.
2. After explicit confirmation, output only clean JSON in English for image generation. Do not wrap JSON in Markdown fences, do not add explanations, and do not include Chinese text outside JSON values unless the user explicitly asks for bilingual fields.

If the product, target audience, offer, or selling point is unclear, make reasonable ecommerce assumptions and state them briefly before the 9 shots. Do not ask for missing details unless the product category itself is unknown.

## Stage 1: Chinese 3x3 Storyboard

Create exactly 9 numbered shots arranged as a 3x3 short-video storyboard. For each shot include:

- `画面`: Product-centered visual description suitable for ecommerce image/video generation.
- `动态运镜`: A specific camera movement or subject movement; never use static shots. Vary movements across shots, such as slow push-in, handheld follow, orbit, rack focus, top-down slide, whip pan, macro glide, reveal pull-back, or tilt-up.
- `口播建议（墨西哥西语）`: Natural Mexican Spanish voiceover or on-screen line. Keep it concise, conversational, and TikTok-friendly.
- `卖点`: The exact product benefit or conversion purpose of the shot.

Keep the script in Chinese except Spanish voiceover lines. Make the 9 shots form a complete ad arc:

1. Hook
2. Relatable daily-life need
3. Product reveal
4. Sensory or usage moment
5. Key benefit
6. Lifestyle/social proof
7. Offer or reason to buy now
8. Trust/detail close-up
9. Call to action

End Stage 1 with a short confirmation request in Chinese, such as: `确认后我会生成第二阶段的英文生图 JSON。`

## Mexico Localization Rules

Target Mexico TikTok Shop shoppers with local, contemporary ecommerce language. Prefer everyday settings such as apartments, vanity tables, office commute prep, date-night prep, weekend outings, gifting moments, or warm indoor retail lighting.

Use natural Mexican Spanish, for example:

- `Huele delicioso`
- `Perfecto para todos los dias`
- `Te dura toda la tarde`
- `Ideal para regalar`
- `Pidelo hoy en TikTok Shop`
- `Se siente fresco, elegante y nada pesado`

Avoid China Douyin-style hard-sell phrasing, exaggerated miracle claims, overly formal Spanish, and direct translations that sound unnatural in Mexico.

Avoid Mexican stereotypes unless the product is directly related to them. Do not use oversized sombreros, cactus scenery, Day of the Dead makeup, mariachi bands, ponchos, desert caricatures, or tourist-poster imagery by default.

## Visual Style Rules

Keep a unified style across all 9 shots:

- Ecommerce-ready product beauty visuals with realistic lighting.
- Consistent color palette, lens feel, environment, and product presentation.
- Clear product visibility in most shots.
- Human presence is allowed, but keep the product as the hero.
- Include motion in every shot; do not write fixed or static camera setups.
- Avoid chaotic backgrounds, text-heavy frames, and meme-like layouts unless requested.

For perfume or fragrance products, emphasize bottle design, mist, skin/clothing application, scent mood, gifting, confidence, and lasting impression without claiming medical or impossible effects.

## Stage 2: English Image JSON

After the user confirms Stage 1, output only valid JSON in English. Use this structure:

{
  "project": {
    "market": "Mexico",
    "platform": "TikTok Shop",
    "format": "3x3 storyboard",
    "visual_style": "",
    "negative_style": "No Mexican stereotypes such as oversized sombreros, cactus tourist scenery, Day of the Dead makeup, mariachi bands, ponchos, or caricatured desert imagery unless product-relevant."
  },
  "shots": [
    {
      "shot": 1,
      "role": "Hook",
      "image_prompt": "",
      "camera_motion": "",
      "spanish_voiceover": "",
      "selling_point": "",
      "negative_prompt": ""
    }
  ]
}

Include exactly 9 objects in `shots`. Each `image_prompt` must be detailed enough for image generation and must preserve the unified style. Each `camera_motion` must describe dynamic movement, even though the output is for still image generation, so the generated frame implies motion and video continuity.

Do not include comments, trailing commas, Markdown, or explanatory text in Stage 2.
