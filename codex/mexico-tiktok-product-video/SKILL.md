---
name: mexico-tiktok-product-video
description: Use when Codex receives or is asked to use a product image for Mexico TikTok ecommerce short videos, especially requests mentioning TikTok, short video, product ad, Mexico, Spanish, Seedance, viral, UGC, ecommerce, TikTok Shop, or product selling. Codex must save the image, run research, generate es-MX scripts/prompts, call Seedance when requested, post-produce videos, and report output paths without asking the user to run commands.
---

# Mexico TikTok Product Video

## Core Rule

Operate through Codex conversation mode. The user supplies images and product facts in chat; Codex saves inputs, runs internal commands, uses Chrome, calls Seedance, performs post-production, verifies outputs, and reports results. Do not ask the user to manually run `cd`, `npm run`, `python generate.py`, or equivalent commands.

## Cross-Project Use

This skill can be installed globally and used from any Codex project. If the current project already contains the Mexico TikTok product video agent implementation, use the local project runner. If the current project does not contain the implementation, use the canonical implementation project as the backend:

`C:\Users\24210\Documents\Codex\2026-05-19\chrome-seedance-2-0-api-api`

Codex should save or copy the user-provided product image into that backend project's `input/` directory, run the backend internally, and report the generated output paths. Do not ask the user to change directories or run backend commands.

## Trigger Conditions

Use this skill when the user:

- Uploads or references a product image.
- Provides a product image URL or local image path.
- Mentions TikTok, short video, product ad, Mexico, Spanish, Seedance, viral, UGC, ecommerce, TikTok Shop, or product selling.
- Asks for research-only, script-first, formal generation, regeneration, style changes, or batch product-video processing.

## Input Handling

Codex must identify the product image source:

- Uploaded Codex image: save it into `input/` if accessible.
- Image URL: download it into `input/`.
- Local path: check that it exists, then copy it into `input/`.
- Unreadable attachment: ask only once for the user to drag the image into the current Codex project or provide an image URL.

Save images as `input/{product_slug}.jpg` when possible. If product name is missing, use a safe slug such as `product`.

Optional product information may include product name, price, discount, brand, landing page, target customer, and notes. If optional facts are missing, continue without inventing them.

## Conversation Modes

Map user wording to internal execution:

- Only research: product analysis, Chrome/public research, competitor teardown, trend summary, and concept scoring. Do not call Seedance.
- Script first: product analysis, research, creative directions, scripts, captions, metadata, and Seedance prompts. Do not call Seedance.
- Formal generation: full pipeline, including Seedance raw videos, evaluation, retries, post-production, and final videos. If the user is continuing from an existing script-first output, reuse confirmed scripts/prompts/storyboards instead of regenerating them.
- Regenerate video N: reuse existing product analysis, research, scripts, and prompts; regenerate only the requested video unless the user asks for a deeper change.
- Change style: reuse product analysis and research; regenerate concepts/scripts/prompts, then continue according to requested mode.
- Batch processing: process each product image independently into its own `output/{product_slug}/`.

## Internal Execution

Use the project runner internally. The CLI can exist as an internal tool, but never present it as a user-required step.

Default internal behavior:

1. Save the product image to `input/`.
2. Analyze product facts and save `product_analysis.json`.
3. Use Chrome/public web research for Mexico TikTok, TikTok Ads, TikTok Creative Center, public TikTok pages, Google results, competitor ecommerce pages, comments, descriptions, and similar products.
4. Save research files.
5. Generate at least 6 candidate concepts and score them.
6. Select at least 3 clearly different concepts.
7. Generate natural Mexican Spanish scripts.
8. Generate Seedance 2.0 prompts.
9. Generate storyboard reference assets for each selected script.
10. For formal runs, call Seedance 2.0 to generate raw videos.
11. Evaluate raw videos and retry up to 2 times when below threshold.
12. Add hard subtitles, CTA, price/discount/brand cards only when supplied, cover/export, and final MP4.
13. Run tests or minimal validation.
14. Report output paths and any failures.

## Research Rules

- Do not bypass login, paywalls, captchas, or platform restrictions.
- Use public sources or already authorized platforms only.
- Extract reusable creative structures; do not copy scripts, videos, music, logos, watermarks, creator identity, or full captions.
- Each case should include source URL, platform, region if known, category, hook, first 3 seconds, structure, visual style, camera style, pacing, selling points, caption style, CTA, hashtags/keywords, why it works, what not to copy, reusable pattern, and relevance score.
- If exact product examples are scarce, use same-category or adjacent-use examples and record uncertainty.

## Product And Copy Rules

Clearly separate confirmed image facts, user-provided facts, assumptions, and unknowns.

Never invent:

- price, discount, logistics, shipping, stock
- sales volume, reviews, certifications, brand authorization
- medical effects, weight-loss effects, treatment effects
- guarantees, `100% efectivo`, `garantizado`, `el mejor`, `resultados instantaneos`

Use natural Mexican Spanish. Prefer short lines such as:

- `Mira esto`
- `Te pasa esto?`
- `Mira como se usa`
- `Esta practico`
- `Ideal para tenerlo en casa`
- `Checa los detalles`
- `Pidelo desde el enlace`

Avoid `vosotros`, `vale`, `tio/tia`, stiff translation, fake urgency, and unsupported offers.

## Seedance Prompt Rules

Every Seedance prompt must include:

- Goal: vertical TikTok ecommerce product video for Mexico.
- Product consistency with the input image.
- Research-based creative pattern: hook type, camera movement, scene structure, demo style, pacing, tone.
- Visual style: mobile-first, TikTok-native, creator-style, handheld, fast reveal, macro close-ups, natural lighting, realistic use, quick cuts, product-centered.
- Text restriction: no readable text, prices, logos, claims, subtitles, or CTA inside Seedance video.
- Compliance restriction: no fake logos, certifications, testimonials, unrealistic transformations, medical claims, guarantees, or unsupported before/after.
- Output: vertical 9:16, 9-15 seconds, TikTok product ad.

If the provider needs a public image URL, Codex must use the configured upload/adapter path. Do not pass a local file path to an endpoint that requires a URL.

## Storyboard Reference Rules

- The product image is mandatory and remains the primary visual identity reference for formal video generation.
- The text scene breakdown is useful for planning and prompt text, but it is not an image reference by itself.
- Generate only one storyboard image per selected video: `*_storyboard_reference.png`.
- The storyboard reference PNG is shared with the user and may be passed to Seedance. It must be 9:16, text-free, logo-free, price-free, and composed like one vertical video frame instead of a multi-panel board.
- Do not generate a separate human-only storyboard board, SVG, panel sheet, or text-heavy storyboard artifact.
- Formal generation should pass both the product image and the storyboard reference PNG when available: product image for product consistency, storyboard reference PNG for camera flow, composition, pacing, and scene structure.
- Never use a storyboard image to invent product color, packaging, shape, claims, certification, price, discount, or brand details. Those must come from the product image or user-provided facts only.

## Confirmed Script Lock

- After script-first output is created, the existing output directory is the confirmed source for formal generation unless the user asks to rewrite, change style, or regenerate concepts.
- In confirmed-script mode, Codex must read `product_analysis.json`, `scripts/scripts.json`, `prompts/seedance_prompts.json`, and storyboard references from that output directory.
- Do not regenerate scripts, prompts, creative directions, or research in confirmed-script mode.
- Recover the original product image from `product_analysis.json` when possible, so the user does not need to upload it again.
- Seedance receives the confirmed `seedance_prompt`; post-production receives the confirmed subtitles and CTA from the script file.

## Speed Optimization Rules

- Do not ask for extra confirmation after script-first output unless the user explicitly requests a review checkpoint.
- Dry-run should not render placeholder videos. It should output planned raw/final paths plus scripts, prompts, storyboard reference PNGs, metadata, and reports.
- Formal generation may run videos concurrently while preserving per-video product image reference, confirmed prompt, storyboard reference, evaluation, retries, and post-production.
- Reuse confirmed output directories instead of rerunning research, creative scoring, scripts, prompts, or storyboard generation.
- Skip only nonessential work for the requested mode. Never skip product image reference, compliance filtering, confirmed script usage, Seedance prompt restrictions, evaluation, or controlled text overlays in formal generation.

## Output Contract

Create:

```text
output/{product_slug}/
  product_analysis.json
  research/
  scripts/
  prompts/
  storyboards/
  jobs/
  raw/
  final/
  captions.csv
  metadata.csv
  compliance_report.md
  generation_report.md
```

All raw and final videos must be preserved. If the provider only supports 720p, record the real resolution and do not claim 1080p.

## Final Reply Format

After completing a run, respond with output paths, not instructions for the user to run commands:

```text
Completed:
- Product analysis: output/{product_slug}/product_analysis.json
- Research brief: output/{product_slug}/research/creative_brief.md
- Scripts: output/{product_slug}/scripts/scripts.json
- Seedance prompts: output/{product_slug}/prompts/seedance_prompts.json
- Storyboard references: output/{product_slug}/storyboards/
- Raw videos: output/{product_slug}/raw/
- Final videos: output/{product_slug}/final/
- Compliance report: output/{product_slug}/compliance_report.md
- Generation report: output/{product_slug}/generation_report.md
```

If failed, report the failed step, reason, generated files, retry status, and the one missing piece of information if any.
