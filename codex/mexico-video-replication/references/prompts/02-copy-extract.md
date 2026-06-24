# 02 Copy Extract Prompt

```text
Extract the benchmark video's spoken copy, subtitle text, and screen text.

Inputs:
- Audio transcript if available: {{ }}
- Subtitle/OCR review frames: {{ }}
- Shot breakdown: {{ }}

Output:
- Original copy in playback order.
- Screen text in playback order.
- Uncertain or inaudible fragments.
- First-3-second hook copy verification.

Rules:
- Use audio transcript, visible subtitles, and OCR frames together.
- Do not rely only on small contact sheet text.
- Preserve sentence rhythm and short-line structure.
- Mark uncertain words rather than guessing.
```
