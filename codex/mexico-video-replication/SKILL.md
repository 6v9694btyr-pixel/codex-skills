---
name: mexico-video-replication
description: "Use this skill for Mexico TikTok Shop ecommerce video workflows, including TikTok benchmark replication, Mexican Spanish copy rewriting, strong-hook 9-shot storyboards, image prompts, Seedance prompts, and optional Ark/Seedance API submission with the user configured key."
---

# Mexico Video Replication

Run Mexico-localized TikTok Shop product-video workflows. Use this when the user wants to replicate a TikTok/short-video benchmark for Mexico, generate a high-conversion 9-shot Mexican Spanish selling script, create storyboard frames, convert 9 frames into Seedance prompts, or optionally submit Seedance API tasks.

## Route Selection

Choose exactly one route from the user's input.

- Benchmark replication: use when the user provides a TikTok/Douyin/competitor video plus product images or product information. Preserve the benchmark's shot order, timing, actions, composition, and conversion rhythm, but rewrite the copy and shopping context for Mexico TikTok Shop.
- Strong-hook 9-shot generation: use when the user provides product information, selling points, audience, and product images but no benchmark video. Generate a Mexico TikTok Shop 9-shot script first, wait for confirmation, then create image prompts/storyboard frames and Seedance prompts.
- Nine-frame direct submit: use when the user already has 9 storyboard frames and 9 prompts. Do not regenerate the script or frames unless explicitly asked; write the final Seedance prompt and optionally submit through the API.

If multiple routes are present, ask the user which route to use. Never mix routes inside one run.

## Core Contract

- Product fidelity is the P0 gate. Product category, shape, color, material, texture, structure, logo/mark placement, package details, and visible identity details must match the product images.
- Mexico localization is the P1 gate. The script must sound like natural Mexican TikTok creator speech, not a literal Chinese ad translation or a generic Latin American commercial.
- Keep the product visible early and often. The first 1-2 seconds must show the product, a result, or a clear curiosity gap related to the product.
- Use TikTok Shop conversion logic: relatable need, product reveal, use proof, detail proof, trust/offer cue if supplied, and a short CTA.
- Avoid Mexico stereotypes unless the user explicitly requests them and the product makes them relevant. Do not default to tourist imagery, caricatured costumes, unsafe street scenes, poverty-coded visuals, or cliche cultural props.
- Do not fabricate unsupported medical, wellness, legal, or price claims. If the user provides a claim, use natural testimonial-style wording and keep it visibly tied to the product or user context.
- Generate actual storyboard images when the route requires them. Do not stop at prompt text unless the user asks for prompts only.
- Seedance prompts must be concrete, physically plausible director prompts. Storyboard images lock composition; product images lock product appearance.
- For API generation, use the user's local key only. Check environment/shared API bundle and `$HOME/.codex/secrets/seedance.env`; never ask for a key until those are missing or do not contain the required provider key.

## Audio Modes

- `ambient`: default for API calls; real environment and action sound only.
- `music`: environment/action sound plus light background music.
- `voiceover`: environment/action sound plus Mexican Spanish narration.
- `full`: environment/action sound, music, and Mexican Spanish narration.
- `silent`: no audio; use only when the user asks for silence.

When spoken lines, `voiceover_ms`, or Spanish narration are present and generated audio is requested, prefer `voiceover` or `full`. Audio permission does not imply permission to add subtitles or screen text.

## Default Inputs

For benchmark replication, locate or ask for:

- Benchmark video file or URL.
- Product image files, package images, and product notes.
- Product name, selling points, target shopper, offer/price/shipping details if supplied.
- Desired Spanish voice style, target duration, and audio mode.
- Whether to output prompts only or call the API.

For strong-hook 9-shot generation, locate or ask for:

- Product name, category, visible design, key benefit, target shopper in Mexico, and use scene.
- Product images and product-image notes.
- Optional offer, price, pack count, social proof, reviews, language, duration, and audio mode.

For nine-frame direct submit, locate or ask for:

- 9 storyboard frames in shot order.
- 9 prompts or shot descriptions, including voiceover fields if present.
- Product images if the storyboard does not fully lock product appearance.
- Audio mode, target duration, and whether to call the API.

## Benchmark Replication Workflow

1. Inspect the benchmark video with frame extraction when local files are available. Sample densely enough to catch 1-2 second TikTok ecommerce actions.
2. Load `references/mexico-localization.md`.
3. Load `references/copy-extraction.md` and `references/prompts/02-copy-extract.md` before extracting copy. Use audio transcription plus subtitle/OCR frame review when copy matters.
4. Run visual breakdown with `references/prompts/01-video-breakdown.md`.
5. Run Mexico script-framework analysis with `references/prompts/03-mexico-script-framework.md`.
6. Run Mexico replication blueprint with `references/prompts/04-mexico-replication-blueprint.md`.
7. Rewrite the copy with `references/prompts/05-mexico-copy-rewrite.md`. Preserve the benchmark rhythm, but make the language Mexican Spanish and replace China-market cues with Mexico TikTok Shop cues.
8. Before storyboard generation, load `references/product-fidelity-gate.md` and build a product-fidelity contract from the product images.
9. Generate storyboard image prompts with `references/prompts/06-mexico-storyboard-prompt.md`, then create every planned storyboard image with Codex image generation.
10. QC each storyboard against product fidelity, Mexico TikTok realism, benchmark similarity, shot continuity, and physical plausibility. If 1-2 issues are fixable, regenerate once with targeted corrections. If P0 product fidelity still fails, stop and report the reason.
11. Load `references/seedance-rules.md` and write final Seedance prompts with `references/prompts/07-mexico-seedance-video-prompt.md`.
12. If the user asks for API generation, load `references/seedance-api.md`, run a dry run unless the user explicitly asks to submit directly, then submit, poll, download, and QC the MP4.

## Strong-Hook 9-Shot Workflow

1. Load `references/mexico-localization.md` and `references/prompts/00-mexico-nine-shot.md`.
2. Generate a Chinese planning note plus a 9-shot Mexican Spanish script. The first 3 shots must create a strong stop-scroll hook, and the product or solution must appear by shot 3.
3. Stop and ask the user to confirm or revise the script before generating image prompts.
4. After confirmation, generate pure JSON with 9 `prompt_text` values plus `voiceover_tone` and `voiceover_ms` when applicable.
5. Use Codex image generation to create exactly 9 storyboard frames in shot order, preserving one shared visual style and product fidelity.
6. QC the 9 frames. Regenerate only weak or incorrect frames once unless the user asks for broader remaking.
7. Load `references/prompts/08-mexico-nine-grid-video-prompt.md` and write the final Seedance prompt from the 9 frames, 9 prompts, product information, and Spanish lines.
8. If API generation is requested, submit with product images first, then the 9 storyboard frames in order. Use `--reference-mode grid-storyboard` and the selected `audio_mode`.

## Nine-Frame Direct Submit Workflow

1. Load `references/mexico-localization.md` and `references/prompts/08-mexico-nine-grid-video-prompt.md`.
2. Verify that 9 frames and 9 prompts/descriptions are present. If only a 3x3 overview grid is present, ask whether to use it as a structure reference or request separate frames.
3. Do not rewrite the whole script or regenerate image2 frames unless the user explicitly asks.
4. Write one final Seedance prompt that follows the 9 frames in order, preserves product identity, uses natural Mexican Spanish if voiceover is included, and avoids unsupported claims.
5. If no API key is configured or the user wants manual upload, deliver the prompt and exact reference-image order.
6. If API generation is requested, submit and QC as in the strong-hook workflow.

## Final Deliverables

For benchmark replication, deliver only:

- Generated storyboard image files.
- Final Mexican Spanish imitation copy/script.
- Final Seedance 2.0 prompt(s).
- Downloaded MP4 file(s) and QC result when API generation was requested and completed.

For strong-hook 9-shot generation, deliver only:

- Confirmed 9-shot script.
- 9 image prompts/JSON.
- 9 storyboard frames and optional 3x3 overview grid.
- Final Seedance prompt and exact reference-image order.
- Downloaded MP4 and QC result when API generation was requested and completed.

For nine-frame direct submit, deliver only:

- Final Seedance prompt.
- Exact reference-image order for manual upload.
- Downloaded MP4 and QC result when API generation was requested and completed.

Keep frame sheets, OCR crops, rough breakdowns, and other analysis files internal unless the user asks for them.

## When To Load References

- `references/mexico-localization.md`: before any script, storyboard, voiceover, or visual-context decision.
- `references/product-fidelity-gate.md`: before storyboard prompting, storyboard QC, regeneration, or Seedance prompt writing.
- `references/seedance-rules.md`: before writing or reviewing Seedance prompts.
- `references/seedance-api.md`: only when submitting or polling Seedance API tasks.
- `references/copy-extraction.md`: before extracting or correcting benchmark copy.
- `references/quality-checklist.md`: before finalizing outputs or diagnosing drift.
- `references/workflow.md`: for file organization and output naming.

## Quality Gates

- First 2 seconds are understandable without context and show product, result, or strong curiosity.
- Spanish sounds Mexican, short, creator-like, and natural.
- Product is visible in most key shots and never deformed or replaced with a generic item.
- The storyboard does not add random new scenes, captions, text overlays, or props that were absent from the chosen route.
- Visuals are modern everyday Mexico: apartment, vanity, bathroom counter, home office, handbag moment, going-out prep, gifting, commute prep, or similarly relevant contexts.
- Claims are supported by product facts, user-provided info, visible packaging, reviews, or clearly labeled assumptions.
- Seedance prompts are 9:16, physically plausible, and use product images as the source of truth for appearance.
- Final video fails QC if it skips/reorders shots, weakens the hook, breaks product identity, adds unrequested subtitles/screen text, sounds non-Mexican when voiceover is requested, or violates physical-world logic.

## Output Style

Keep responses practical and short. Use Chinese for planning notes when helpful to the user, but write final voiceover/copy in Mexican Spanish unless the user requests another language. When the user asks to modify a prompt, output the complete replacement prompt.