---
name: mexico-tiktok-shop-fast-video-generator
description: Fast no-confirmation workflow for producing Mexico TikTok Shop product videos from product images or product descriptions. Use when Codex should quickly analyze a product, write a Mexico-localized 9-shot TikTok Shop selling script, generate a storyboard board image, create three Seedance 1.5 Pro segment prompts/specs that reference the supplied product images, call the Ark/Seedance API for the 3 segments, poll, download, stitch the segments, and optionally add Mexican Spanish voiceover without stopping for staged user confirmations.
---

# Mexico TikTok Shop Fast Video Generator

## Core Rule

Run the workflow end to end without staged confirmation pauses. Do not ask the user to confirm product analysis, script, storyboard prompts, Seedance prompt, or API generation unless required information is missing or the user explicitly asks for a preview-only workflow.

Prefer speed over exhaustive production boards:

1. Analyze the product.
2. Write the Mexico TikTok Shop script.
3. Generate a storyboard board image.
4. Create one Seedance 1.5 Pro JSON spec with 3 segments and product reference images.
5. Write the spec to the workspace.
6. Call the API script, poll, download all segments, stitch them, and add voiceover when configured.

The storyboard board image is a required fast workflow step when image generation is available. If image generation is unavailable, save the storyboard board prompt and continue only after clearly stating that the image artifact could not be produced.

## Fast Workflow

### 1. Product Analysis

Analyze product facts, visible features, likely uses, Mexico TikTok selling angles, target users, scenes, pain points, style direction, and uncertainty/risk. Keep this compact and actionable.

Use authentic contemporary Mexican lifestyle context:

- Bedroom vanity, apartment, office prep, handbag touch-up, date prep, friends outing, gifting
- CDMX, Guadalajara, Monterrey as subtle lifestyle cues when relevant
- Natural Mexican Spanish phrasing
- Fast TikTok pacing, realistic handheld camera, product visible and desirable

Avoid stereotypes unless product-relevant:

- No sombrero
- No cactus tourist scenery
- No mariachi
- No Day of the Dead makeup
- No exaggerated national costume
- No unsafe, poor, dirty, or dangerous street framing

### 2. Mexico TikTok Script

Create a 9-shot ecommerce script in Chinese with Mexican Spanish voiceover/subtitle lines. Include:

- Video title
- Core selling points
- Video style
- Target user
- Complete script
- Mexican Spanish voiceover/subtitle version
- Chinese explanation
- 9-shot plan

Each shot should include duration, framing, visual content, human action, product focus, Mexican Spanish line, Chinese meaning, dynamic camera movement, and purpose.

### 3. Storyboard Board Image

Generate one professional product video storyboard board image before video generation. It must be:

- A horizontal 16:9 or 4:3 production planning board, not an ad poster.
- Top area: product facts, target user, Mexico TikTok Shop selling points, and scene direction.
- Bottom area: 9-panel storyboard grid matching the 9-shot script.
- Each panel: shot number, preview-style frame, core action, product focus, short Spanish line, and Chinese meaning.
- Based on the supplied product images and the exact product identity.

Keep text short because image models distort long text. If exact text matters, put it in the written script/spec and use the image as a visual planning reference.

### 4. Seedance 1.5 Pro Spec

Create a three-part Seedance 1.5 Pro prompt/spec. Split the 9 shots into 3 API tasks:

- Segment 1: shots 1-3, opening hook and product reveal
- Segment 2: shots 4-6, use scenario and selling-point proof
- Segment 3: shots 7-9, desirability, lifestyle payoff, and call to action

Keep every segment prompt suitable for direct video generation:

- `full-screen 9:16`
- `not a slideshow, not a collage, not a grid`
- realistic UGC / TikTok Shop creator style
- dynamic camera movement and subject actions
- product visible and desirable throughout each segment
- Mexico-localized lifestyle context
- avoid large text, subtitles, price labels, fake discount labels, watermark text, and UI overlays
- if the user provides product images, use them as visual references in the storyboard board and in the Seedance request

Product-reference rule:

- Put product images in `reference_image_urls`, `reference_images`, `image_urls`, or per-segment `reference_image_urls`.
- The script accepts `http://`, `https://`, `data:image/...` URLs, and local image paths. Local image paths are automatically converted to base64 `data:image` URLs before being sent to Seedance.
- Do not use uploaded Files API IDs as `image_url`; Seedance rejects them.
- Do not use product-locked local compositing as the default final video path because it looks like a dynamic PPT. Use it only as a clearly labeled low-motion preview/fallback when Seedance image-reference generation is unavailable.
- When using Seedance with reference images, still describe the stable product identity in every segment prompt: shape, material, color, text, charms, orientation, and any variants.

Use this JSON shape:

```json
{
  "output_slug": "mexico_tiktok_product_video",
  "model": "ep-20260511103248-tcqpx",
  "resolution": "720p",
  "ratio": "9:16",
  "storyboard_board_image": "path or URL to generated storyboard board image",
  "reference_image_urls": [
    "https://example.com/product-main-1.jpg",
    "https://example.com/product-main-2.jpg"
  ],
  "voice": "es-MX-DaliaNeural",
  "voice_rate": "+12%",
  "voice_pitch": "+2Hz",
  "watermark": false,
  "generate_audio": false,
  "segments": [
    {
      "segment": 1,
      "shots": "1-3",
      "duration": 8,
      "reference_image_urls": [
        "https://example.com/product-main-1.jpg"
      ],
      "prompt": "Seedance 1.5 Pro prompt for shots 1-3"
    },
    {
      "segment": 2,
      "shots": "4-6",
      "duration": 8,
      "reference_image_urls": [
        "https://example.com/product-main-1.jpg",
        "https://example.com/product-detail-2.jpg"
      ],
      "prompt": "Seedance 1.5 Pro prompt for shots 4-6"
    },
    {
      "segment": 3,
      "shots": "7-9",
      "duration": 8,
      "reference_image_urls": [
        "https://example.com/product-main-1.jpg"
      ],
      "prompt": "Seedance 1.5 Pro prompt for shots 7-9"
    }
  ],
  "voiceover": "Mexican Spanish voiceover here"
}
```

Do not enforce a whole-video 15 second limit. Use 3 segment tasks by default and choose the per-segment duration from the script timing, commonly 6-10 seconds each. Keep each segment self-contained enough to generate cleanly, but ensure the three prompts share product identity, lighting, wardrobe, setting, and creator style so the stitched result feels continuous.

### 5. API Generation

Write the JSON spec to the current workspace as `video-spec.json`, then run:

```powershell
$script = Join-Path $env:USERPROFILE ".codex\skills\mexico-tiktok-shop-fast-video-generator\scripts\generate_seedance_segments_mexico_tiktok_video.py"
python $script --spec ".\video-spec.json" --env ".\.env.local" --out ".\outputs"
```

Return the final stitched MP4 path, the three segment MP4 paths, task IDs/statuses if available, and whether a voiceover MP3/final voiced MP4 was produced.

If a task stays running, do not resubmit immediately. Re-run the script with the same output directory; it reuses the existing task record and continues polling where possible.

## Seedance/API Configuration

Read credentials from the current workspace `.env.local` or environment variables. Never place API keys inside the skill.

Expected variables:

```env
SEEDANCE_API_KEY=
SEEDANCE_BASE_URL=https://ark.cn-beijing.volces.com/api/v3
SEEDANCE_VIDEO_MODEL=ep-20260511103248-tcqpx
```

Also accept `ARK_API_KEY`, `ARK_BASE_URL`, and `ARK_VIDEO_MODEL` as fallback values.

The user's provided Seedance 1.5 Pro configuration maps to:

- model name: `seedance_1.5pro`
- base URL: `https://ark.cn-beijing.volces.com/api/v3`
- model ID / endpoint ID: `ep-20260511103248-tcqpx`

Use the exact model ID configured by the user. Do not substitute default IDs when the user has supplied one.

## Script Output

The bundled script outputs:

- Storyboard board image or storyboard board prompt path when generated before the script is called
- Seedance task status JSON
- Three silent Seedance segment MP4 files
- One stitched silent MP4
- Mexican Spanish voiceover MP3 when `voiceover` is present and `edge-tts` is available
- Final MP4 with voiceover when `ffmpeg` is available
- Generation summary JSON

If voiceover generation or muxing fails because a dependency is missing, report the silent MP4 path and the missing dependency instead of rerunning the video task.
