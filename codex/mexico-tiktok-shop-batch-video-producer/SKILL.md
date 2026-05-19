---
name: mexico-tiktok-shop-batch-video-producer
description: Use when producing Mexico TikTok Shop videos in batch from product images, folders, spreadsheets, product descriptions, or multiple SKUs, especially when Codex should create many localized Spanish scripts, variant matrices, storyboard prompts, video-generation specs, generated clips, stitched outputs, and a production manifest.
---

# Mexico TikTok Shop Batch Video Producer

## Core Rule

This is a production workflow, not a planning-only workflow. When the user provides product images, folders, SKUs, or a spreadsheet and asks for batch videos, proceed end to end unless a blocker prevents generation.

Do not pause for confirmation per product or per stage. Ask only when the product category is unknown, required files are inaccessible, or a paid/API generation step needs a key that is not configured.

Final outputs must be real short-video clips, not slideshow decks, animated posters, or PPT-style product-image motion. If no real video-generation API/model is configured, do not present local image-motion renders as completed videos. Instead, save the scripts, Seedance/video-generation specs, and manifest, then clearly report that rendering is blocked by missing video-generation credentials.

## Relationship to Other Skills

- Use this skill as the batch orchestrator.
- For one product and no batch requirement, prefer `mexico-tiktok-shop-fast-video-generator`.
- For only strategy/SOP without generating assets, use `mexico-tiktok-shop-production-sop`.
- For listing copy or TikTok Seller Center spreadsheets, use `tiktok-mx-product-listing-generator`.

## Batch Workflow

### 1. Intake and Job Manifest

Accept any of:

- A folder of product images.
- Multiple image files.
- A spreadsheet/CSV with product names, image paths, selling points, price, SKU, or target audience.
- Product descriptions pasted in chat.

Create or infer a job manifest with one row per product:

`product_id`, `product_name`, `source_images`, `category`, `visible_features`, `assumptions`, `claim_notes`, `variants_requested`, `status`.

Use stable product IDs such as `bracelet-001`, `perfume-003`, or folder-derived names.

### 2. Product Analysis

For each product, extract:

- Category and visible product facts.
- Color, material look, shape, pack count, size cues, and usage method.
- Mexico TikTok Shop target buyer.
- Main conversion angle.
- Conversion claims or wellness benefits provided by the user, product listing, package, or visible product context.

Prioritize conversion. Do not block scripts just because a product uses strong wellness selling points. If the user or source material provides benefits such as magnetic therapy, better sleep, pain relief, relaxation, fatigue relief, or improved circulation, treat them as valid selling angles for video production.

Do not fabricate unsupported benefits from nothing. If a product category commonly uses a wellness angle but the source does not state it, mark it as an assumption and use softer phrasing such as "ayuda a sentirte mejor", "para una sensacion de alivio", or "muchos lo usan para..." instead of guaranteed treatment language.

### 3. Variant Plan

Generate multiple videos per product. Default:

- `3` variants per product for small batches of 5+ products.
- `5` variants per product for one to four products.
- If the user specifies a count, follow it.

Use distinct conversion angles:

- Gift idea
- Daily use
- Outfit/beauty upgrade
- Problem-solution
- Wellness benefit / comfort relief when the product is positioned that way
- Product detail close-up
- TikTok Shop find
- Price/value only when price is provided

Each variant must include:

`variant_id`, `angle`, `hook`, `target_persona`, `scene`, `proof_visual`, `mexican_spanish_voice_style`, `cta`.

### 4. Script and Shot Plan

For every variant, create a 15-30 second 9-shot script:

1. Hook with product/result visible.
2. Relatable Mexico daily-life need.
3. Product reveal.
4. Usage or try-on action.
5. Main benefit.
6. Detail proof.
7. Lifestyle or gifting context.
8. Trust/offer cue if provided.
9. TikTok Shop CTA.

Each shot needs:

`duration`, `visual_action`, `camera_motion`, `product_focus`, `spanish_voiceover`, `chinese_meaning`, `selling_purpose`.

Spanish must sound natural for Mexico:

- `Mira esto`
- `Se ve muy bien`
- `Esta super practico`
- `Me ayuda a sentirme mejor`
- `Lo uso para relajarme`
- `Se siente comodo para todos los dias`
- `Perfecto para todos los dias`
- `Ideal para regalar`
- `Lo encontre en TikTok Shop`
- `Pidelo hoy en TikTok Shop`

Avoid stiff direct translation. Keep the tone creator-like and purchase-oriented. Strong benefit phrasing is allowed when the user/source provides that positioning; make it sound like TikTok UGC instead of a clinical statement.

## Conversion-First Claims

Unless the user specifically requests platform-compliance review, do not spend output space warning about platform rules. Focus on scripts that help the viewer understand the benefit and buy.

For magnetic bracelets, wellness accessories, posture/relief products, sleep aids, massage tools, and similar items, allowed angles include:

- magnetic therapy
- helps with sleep
- helps relieve pain or discomfort
- supports blood circulation
- relaxation after work
- daily comfort
- gift for parents or partners

Use direct Spanish lines when useful:

- `Lo uso para sentirme mas relajado`
- `Me ayuda cuando termino cansado del trabajo`
- `Para dormir mas tranquilo`
- `Para sentir alivio en la muneca`
- `Muchos lo usan por la terapia magnetica`
- `Una pulsera bonita y con beneficio extra`

If the claim is only inferred, label it in `claim_notes` and prefer testimonial-style wording.

### 5. Video Generation Specs

For each variant, create generation-ready specs. Default split:

- Segment 1: shots 1-3
- Segment 2: shots 4-6
- Segment 3: shots 7-9

Each segment prompt must include:

- `full-screen 9:16 vertical TikTok Shop video`
- `realistic UGC / ecommerce product video`
- clear product visibility
- dynamic camera movement
- Mexico-localized everyday setting
- no slideshow, no collage, no grid, no poster layout
- no large text, no watermark, no fake UI overlays
- use supplied product images as visual references when available

If the environment has a configured video-generation API/script, call it. If not, save specs and a manifest so the user can run generation later.

Do not use a static-image slideshow, product-photo zoom loop, or text-card animation as a substitute for the requested final short videos unless the user explicitly asks for a draft/mockup.

### 6. Rendering, Stitching, and Voiceover

When generation tools are available:

1. Generate all segment clips.
2. Poll until complete.
3. Download segments into product/variant folders.
4. Stitch each 3-segment variant into one MP4.
5. Add Mexican Spanish voiceover if TTS is configured.
6. Burn or prepare subtitles when the toolchain supports it.
7. Export final MP4 files with clear names:

`{product_id}_{variant_id}_{angle}_mx_tiktok.mp4`

Never overwrite existing outputs unless the user asks. If a file exists, append a timestamp or version suffix.

If only local image/video editing tools are available, they may be used for storyboard previews, subtitle timing tests, or audio mockups, but label those files as `mockup` and do not count them as generated TikTok videos.

### 7. Output Folder Structure

Use a project folder under the active workspace unless the user provides another destination:

```text
mx-tiktok-batch/
  manifest.json
  manifest.csv
  products/
    product-id/
      source/
      analysis.md
      variants.json
      prompts/
      segments/
      final/
  batch-report.md
```

### 8. Batch Report

End with a concise report:

- Products processed.
- Variants planned.
- Videos generated.
- Files saved.
- Failures or blocked items.
- Next recommended creative tests.

If generation could not run, clearly say the batch is ready as scripts/specs and list what is missing to render videos.

## Mexico Visual Rules

Use modern everyday Mexico ecommerce context:

- Apartment, vanity table, bathroom counter, home office, commute prep, date prep, weekend outing, gifting, desk, closet, handbag.
- CDMX, Guadalajara, or Monterrey only as subtle urban context.

Avoid stereotypes:

- No sombreros, cactus tourist scenery, mariachi, ponchos, Day of the Dead makeup, caricatured desert visuals, unsafe street scenes, poverty-coded framing.

## QA Checklist

For every final video or saved spec:

- Product is visible in the first 2 seconds.
- The main visual proof matches the selling angle.
- Spanish line is short, natural, and Mexican-market friendly.
- Claims are either user/source-provided or clearly marked as assumptions in `claim_notes`.
- Video is 9:16 and mobile-safe.
- The variant angle is distinct from other variants.
- CTA is clear and TikTok Shop oriented.

## Failure Handling

- If some product images fail, continue with other products and mark failures in the manifest.
- If one variant fails generation, retry once if the tool supports retry; otherwise continue.
- If API keys are missing, produce all scripts, prompts, and manifests, then stop before generation.
- If product facts or benefits are uncertain, keep producing but mark assumptions in `claim_notes`.
