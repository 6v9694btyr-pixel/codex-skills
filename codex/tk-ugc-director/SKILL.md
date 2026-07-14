---
name: tk-ugc-director
description: Use this skill when the user uploads or describes an ecommerce product and wants a UGC-style short video plan for TikTok, Reels, or Shorts, including hooks, target audience, script, storyboard, image prompts, Seedance/video prompts, or a spreadsheet/Feishu-ready review table where each generated frame image maps to its video-generation prompt.
---

# TK UGC Director

## Core Workflow

Use this skill to turn an uploaded ecommerce product image or product description into a practical UGC short video plan for TikTok, Instagram Reels, or YouTube Shorts.

When the user uploads a product image or describes an ecommerce product and asks for TikTok, Reels, or Shorts content, enter this workflow immediately. Ask only the missing intake questions below and wait for the user's answers before producing the full plan, unless the user has already provided every field.

1. 目标市场：例如美国、英国、东南亚、日本
2. 发布平台：TikTok / Reels / Shorts
3. 视频时长：15秒 / 20秒 / 30秒
4. 脚本语言：美式英语 / 英式英语 / 中文 / 日语
5. 达人类型：固定达人 / 不固定达人 / 只拍手部 / 不出人
6. 产品露出强度：强露出 / 自然露出 / 后置露出
7. 视频风格：UGC测评 / 痛点解决 / Before After / 情景短剧 / 开箱种草
8. 是否需要生成图片提示词和视频提示词
9. 是否需要导出审核表或同步飞书

If the user uploaded an image, inspect only visible product details and state any assumptions briefly. If product claims, ingredients, certifications, price, or usage constraints are not visible, do not invent them.

If the user asks to generate a review spreadsheet directly from only a product image, do not block on missing intake details. Use practical defaults and state them briefly: US market, TikTok, 20 seconds, American English, natural product exposure, UGC review + pain-point solution angle, and a consistent creator unless the user says otherwise.

## Reference Loading

Read these files as needed:

- `references/user_prompt_template.md`: Use when the user needs a structured brief to fill in.
- `references/ugc_content_formula.md`: Read before ideating hooks, angles, pain points, and UGC story flow.
- `references/shot_prompt_rules.md`: Read before writing image prompts or video prompts.

Optionally run `scripts/check_output.py` against a draft output to check whether the required structural keywords are present.

## Output Contract

Always output the following modules in order:

A. 产品一句话定位
B. 目标人群分析
C. 三层痛点分析：功能痛点、情绪痛点、身份痛点
D. 3个黄金3秒钩子 (hook)
E. 3套不同角度的UGC短视频方案
F. 推荐主方案
G. 逐镜头分镜表 (storyboard)
H. UGC短视频脚本 / 英文或目标语言口播脚本 (voiceover)
I. 字幕文案
J. 人物图生成提示词 (image prompts)
K. 产品使用场景图提示词 (image prompts)
L. 视频生成提示词，适配 Seedance / Runway / Kling / Pika (video prompts)
M. 剪辑建议
N. 合规自查 (compliance check)

When the user says they do not need image or video prompts, keep modules J, K, and L present with concise prompt-direction notes instead of full prompts.

Each of the three UGC video plans must include: angle, target viewer, opening hook, creator setup, story beats, product entry moment, short script direction, and production difficulty.

## Spreadsheet / Feishu Review Table

Use this section when the user asks for 表格、审核表、Excel、飞书同步、导出表格, or a final table for generated frame images.

The spreadsheet's primary purpose is **frame-to-video production review**:

- Each row represents one final generated frame/reference image that can be used as a Seedance first frame or visual reference.
- The prompt column must contain the **video-generation prompt for Seedance**, not the image-generation prompt.
- Do not include a `预览链接` column.
- Do not include image-generation prompts in the main table unless the user explicitly asks for them. If needed, place image prompts on a separate optional sheet named `图片提示词备份`.

Required main-table columns:

1. 编号
2. 镜头时间段 / 使用位置
3. 图片预览
4. 图片文件路径
5. 画面用途
6. Seedance 生视频提示词
7. 负面提示词
8. 对应口播/字幕
9. 审核状态
10. 修改意见

For `Seedance 生视频提示词`, write prompts as image-to-video instructions. Start from the uploaded/generated image as first frame, then describe duration, vertical 9:16, action sequence, camera movement, creator/product continuity, lighting, natural UGC pacing, and product exposure. Keep the same person, outfit, room style, and product appearance across rows unless the user asks for different creators.

When creating an `.xlsx`, use the spreadsheets workflow, embed compressed image previews when syncing to Feishu, and keep the original image file path in the `图片文件路径` column. If the user has Feishu CLI configured, sync the final Feishu-compatible workbook and return the Feishu link.

## Creative Rules

Write like a real UGC creator sharing a lived moment, not like an AI manual or a polished brand ad.

Make every shot specific enough to produce directly:

- 动作：the exact hand, face, body, or product movement.
- 景别：close-up, medium shot, over-the-shoulder, POV, flat lay, mirror shot, handheld selfie.
- 场景：room, kitchen, bathroom, car, desk, travel bag, gym locker, cafe, office, or another believable use context.
- 表情：curious, mildly annoyed, relieved, surprised, focused, casual smile.
- 产品露出方式：in hand, on table, entering frame, partially visible, used in context, pack shot at the end.

Show product value through everyday scenes and observable behavior. Avoid hard-selling language, exaggerated outcomes, fake reviews, fake scarcity, and claims that depend on proof the user did not provide.

Do not use absolute wording such as `guaranteed`, `best`, `100%`, `must-have`, `miracle`, `perfect`, or equivalent claims in other languages.

For regulated categories such as supplements, skincare, medical devices, fitness equipment, infant products, finance, or safety gear, soften claims and frame benefits as personal experience, routine support, convenience, comfort, or appearance where appropriate.

Avoid unverifiable marketplace or authority claims unless the user provides proof: `FDA approved`, `doctor recommended`, `dermatologist approved`, `Amazon #1`, `official`, `viral`, `certified`, `clinically proven`, or similar claims. Do not imply counterfeit, replica, or unauthorized brand association.

## TikTok Cross-Border Safety

Keep the content suitable for cross-border ecommerce:

- Use natural local-life scenes for the target market, but do not invent laws, shipping promises, warranties, certifications, local warehouse claims, or delivery dates.
- Avoid platform-sensitive traffic language such as "DM me", "WhatsApp me", "private order", "bypass TikTok", "link outside", or equivalent wording in other languages.
- Do not create fake customer testimony, fake creator identity, fake screenshots, fake scarcity, or fake discount deadlines.
- Keep before/after shots focused on visible product use, organization, styling, setup, or convenience. Avoid body, medical, skin, weight-loss, or financial transformation claims.
- Use soft calls to action, such as "worth checking out", "I would use this for...", or "this might help if you deal with the same thing".

## Plan Building Notes

Create three distinct UGC angles, for example:

- 痛点解决：start from an annoying daily friction and show a low-pressure fix.
- Before After：show visible contrast without promising guaranteed results.
- 开箱种草：use tactile details, first impression, and one clear use scene.
- 情景短剧：show a tiny relatable conflict, then product use.
- UGC测评：show what the creator noticed, liked, and would change.

Pick the recommended main plan based on audience fit, product visibility, compliance risk, and ease of production.

For the storyboard, use a table with at least: timecode, scene, shot size, action, expression, voiceover/subtitle, product exposure, image prompt, video prompt.

For prompts, keep the same creator identity, product appearance, lighting, room style, and camera language across shots when continuity matters.
