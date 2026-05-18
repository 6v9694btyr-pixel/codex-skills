---
name: mexico-tiktok-shop-video-generator
description: Confirmation-based workflow for producing Mexico TikTok Shop product videos with product analysis, script confirmation, storyboard board generation following product-video-storyboard-skill conventions, Seedance 2.0 long-form single-task video prompts, optional API generation, polling, download, and Mexican Spanish voiceover. Use when the user asks to create, prepare, render, call Seedance, or generate a Mexico TikTok Shop selling video, cross-border ecommerce product video, perfume ad video, storyboard-to-video workflow, or full-script TikTok Shop short video.
---

# Mexico TikTok Shop Video Generator

## Core Rule

Never jump directly to video generation. Use a strict confirmation workflow. After each stage, stop and wait for the user's confirmation before moving on.

Treat vague replies such as `可以`, `确认`, `OK`, `yes`, `继续`, or `没问题` as confirmation only when the current stage is clearly waiting for confirmation.

If the user asks to skip confirmation, politely refuse and continue from the current required stage.

## State Machine

Maintain the current stage explicitly:

1. `product_analysis_pending_confirmation`
2. `script_pending_confirmation`
3. `storyboard_prompt_pending_confirmation`
4. `storyboard_image_pending_confirmation`
5. `seedance_prompt_pending_confirmation`
6. `video_generation_pending_confirmation`
7. `completed`

Rules:

- If the user uploads or references a new product image, restart from `product_analysis_pending_confirmation`.
- Do not write the full script before product analysis is confirmed.
- Do not generate storyboard prompts before the script is confirmed.
- Do not generate the storyboard board image before the storyboard prompt is confirmed.
- Do not generate Seedance video prompts before the storyboard board image is generated and confirmed.
- Do not call Seedance before the Seedance prompt/spec is confirmed.
- If the user requests changes, revise only the current-stage output and ask for confirmation again.

## Stage 1: Product Analysis

Follow the same analysis logic as `product-video-storyboard-skill`. Analyze product facts, visible features, likely uses, Mexico TikTok selling angles, target users, scenarios, pain points, style direction, and uncertainty/risk.

Output in Chinese and end with:

`请确认以上产品分析是否准确。你可以回复：确认 / 修改某一项 / 补充卖点。`

Set stage to `product_analysis_pending_confirmation`.

## Stage 2: Mexico TikTok Script

Only enter after Stage 1 confirmation.

Create a 15-30 second Mexico TikTok ecommerce script in Chinese, with natural Mexican Spanish voiceover/subtitle lines. Include:

- Video title
- Core selling points
- Video style
- Target user
- Complete script
- Mexican Spanish voiceover/subtitle version
- Chinese explanation
- 9-shot table

Each shot must include duration, framing, visual content, human action, product focus, Mexican Spanish line, Chinese meaning, dynamic camera movement, and purpose.

End with:

`请确认脚本是否可以进入分镜图生成。你可以回复：确认 / 修改脚本 / 调整风格 / 增加卖点。`

Set stage to `script_pending_confirmation`.

## Stage 3: Storyboard Board Prompt

Only enter after Stage 2 confirmation.

Generate the storyboard board prompt only. Do not generate the image yet. Follow `product-video-storyboard-skill` Stage 3 conventions:

- Professional product video storyboard board, not an ad poster.
- Top information area with user persona, scene/environment, and product selling points.
- Bottom 9-panel storyboard grid.
- Each card includes shot number, preview-style shot, shot description, product action/use, selling-point focus, short Spanish subtitle, and Chinese meaning.
- Use realistic ecommerce video planning board style.
- Make it suitable for Mexico TikTok production and Seedance prompt preparation.

Output:

```markdown
## 产品分镜板生成提示词

### 1. 中文生图提示词

### 2. English Image Prompt

### 3. Negative Prompt

### 4. 版式说明

### 5. 墨西哥 TikTok 本地化注意事项
```

After output, ask:

`请确认分镜板生图提示词是否可以用于生成分镜板图片。你可以回复：确认 / 修改提示词 / 调整版式 / 调整视觉风格。`

Set stage to `storyboard_prompt_pending_confirmation`.

## Stage 4: Storyboard Board Image

Only enter after Stage 3 confirmation.

Generate the actual storyboard board image from the confirmed storyboard board prompt. This is a required workflow step, not optional, when image generation is available in the current environment.

The image must be:

- A professional product video storyboard board.
- Horizontal 16:9 or 4:3, unless the user requests another layout.
- Structured with a top information area and bottom 9-panel storyboard grid.
- Based on the confirmed product analysis and script.
- Readable enough as a production planning board, while avoiding long text that image models may distort.
- Suitable as a visual reference for the later Seedance full-video prompt.

If image generation is unavailable, state that clearly and ask whether the user wants to continue with the prompt-only storyboard or provide another generated image manually.

After the image is generated, show or link the image and ask:

`请确认分镜图/分镜板是否可以进入 Seedance 视频 Prompt 生成。你可以回复：确认 / 修改某个分镜 / 调整视觉风格。`

Set stage to `storyboard_image_pending_confirmation`.

## Stage 5: Seedance 2.0 Video Prompt And Spec

Only enter after Stage 4 confirmation.

Create a single full-video Seedance 2.0 prompt/spec for videos up to 15 seconds. Seedance 2.0 single-video generation is limited to a maximum of 15 seconds.

If the confirmed script is longer than 15 seconds, stop and ask the user whether to:

- compress the script into one 15-second video, or
- split it into multiple confirmed Seedance tasks and then stitch the results.

Do not silently split or silently shorten the script.

The Seedance prompt must:

- Cover the complete confirmed script and all 9 shots.
- Use one continuous 15-30 second video task.
- Say `full-screen 9:16`.
- Say `not a slideshow, not a collage, not a grid`.
- Use live-action / realistic UGC / TikTok Shop creator language.
- Include dynamic camera movement and subject actions.
- Keep product visible and desirable.
- Use Mexico-localized lifestyle context.
- Avoid large text, subtitles, price labels, fake discount labels, and watermark text.

Output a JSON spec for the bundled script:

```json
{
  "output_slug": "mexico_tiktok_product_video",
  "duration": 15,
  "resolution": "720p",
  "ratio": "9:16",
  "voice": "es-MX-DaliaNeural",
  "voice_rate": "+12%",
  "voice_pitch": "+2Hz",
  "watermark": false,
  "generate_audio": false,
  "prompt": "single full-video Seedance prompt here",
  "voiceover": "Mexican Spanish voiceover here"
}
```

After output, ask:

`请确认是否调用 Seedance 2.0 生成视频。确认后我才会调用 API。`

Set stage to `seedance_prompt_pending_confirmation`.

## Stage 6: API Generation

Only enter after Stage 5 confirmation.

Write the confirmed JSON spec to the current workspace, then run:

```powershell
$script = Join-Path $env:USERPROFILE ".codex\skills\mexico-tiktok-shop-video-generator\scripts\generate_seedance_mexico_tiktok_video.py"
python $script --spec ".\video-spec.json" --env ".\.env.local" --out ".\outputs"
```

Return the generated MP4 path, duration, resolution, frame rate, and whether audio is present. Then ask whether the user wants changes or regeneration.

Set stage to `completed`.

## Seedance/API Configuration

Read credentials from the current workspace `.env.local` or environment variables. Never place API keys inside the skill.

Expected variables:

```env
SEEDANCE_API_KEY=
SEEDANCE_BASE_URL=https://ark.cn-beijing.volces.com/api/v3/contents/generations/tasks
SEEDANCE_VIDEO_MODEL=doubao-seedance-2-0-260128
```

Also accept `ARK_API_KEY` and `ARK_BASE_URL` as fallback values.

Use the exact model ID configured by the user. Do not substitute default IDs when the user has supplied one.

## Mexico Creative Rules

Use authentic contemporary Mexican urban lifestyle:

- Bedroom vanity, apartment, office prep, handbag touch-up, date prep, friends outing, gifting
- CDMX, Guadalajara, Monterrey as subtle city lifestyle context when relevant
- Natural Mexican Spanish voiceover
- Fast TikTok pacing, realistic handheld camera, product visible and desirable

Avoid stereotypes unless product-relevant:

- No sombrero
- No cactus tourist scenery
- No mariachi
- No Day of the Dead makeup
- No exaggerated national costume
- No unsafe, poor, dirty, or dangerous street framing

## Script Output

The bundled script outputs:

- Seedance task status JSON
- Silent Seedance MP4
- Mexican Spanish voiceover MP3
- Final MP4 with audio
- Generation summary JSON

If a task stays `running`, do not resubmit immediately. Re-run the script with the same output directory; it will reuse the existing task record and continue polling where possible.

## Duration Rule

Seedance 2.0 can generate at most 15 seconds in one task.

- For `duration <= 15`, use one Seedance task.
- For `duration > 15`, do not proceed automatically. Ask the user to choose compression to 15 seconds or multi-task generation with stitching.
- If the user chooses multi-task generation, add another confirmation point for the segment plan before calling any API.
