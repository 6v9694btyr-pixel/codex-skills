# 图片和视频提示词规则

## 通用原则

每个提示词都要能直接用于生成画面。避免抽象词堆叠，优先写清楚主体、动作、场景、镜头、光线、情绪、产品露出方式。

保持连续性：

- 固定达人时，所有镜头使用同一人物描述：年龄段、性别呈现、发型、穿着、气质。
- 固定产品时，重复产品的可见特征：颜色、材质、形状、包装、关键配件。
- 固定场景时，重复空间设定：kitchen counter, bathroom mirror, small apartment desk, car console, gym locker。

不要写无法被画面验证的内容，比如 "销量很好"、"效果最好"、"用户都喜欢"。把它们改成可拍的行为或表情。

## 人物图提示词

结构：

`[creator identity], [setting], [pose/action], [expression], [product placement], [camera/framing], [lighting], authentic UGC phone photo, natural skin texture, no studio look`

示例：

`25-year-old casual female creator in a small bright apartment kitchen, holding the product near the sink with one hand, curious half-smile, product label partially visible, handheld medium close-up, soft morning window light, authentic UGC phone photo, natural skin texture, no studio look`

## 产品使用场景图提示词

结构：

`[product appearance], [exact use scene], [hands/action], [surrounding props], [camera/framing], [lighting], realistic ecommerce UGC lifestyle photo`

示例：

`compact white kitchen gadget with rounded edges on a slightly messy kitchen counter, one hand placing it beside a mug and towel, realistic crumbs and water drops nearby, close-up from a handheld phone angle, soft daylight, realistic ecommerce UGC lifestyle photo`

## 视频提示词

结构：

`[duration], vertical 9:16 UGC video, [creator/product], [scene], [action sequence], [camera movement], [expression or mood], [product exposure], [lighting], [style notes], no text overlay unless requested`

每条视频提示词要包含：

- 时长或镜头时段
- 竖屏 9:16
- 单一清晰动作
- 镜头运动：handheld, slight push-in, quick cut, POV, over-the-shoulder, static close-up
- 产品露出：enters frame, label visible, used in hand, on desk, final pack shot
- 真实UGC质感：phone camera, natural light, imperfect lived-in background

## 逐帧图片转视频表格提示词

当输出审核表、Excel、飞书表格或“每张图片对应 Seedance 生视频提示词”时，必须写视频提示词，不要把图片生成提示词放进主表。

每条 Seedance 表格提示词使用结构：

`[duration or timecode], vertical 9:16 image-to-video UGC video, use the provided/reference image as the first frame, [same creator/product continuity], [scene], [single action sequence], [camera movement], [expression/mood], [product exposure], [lighting], [UGC pacing/style], no text overlay`

表格列建议：

- 编号
- 镜头时间段 / 使用位置
- 图片预览
- 图片文件路径
- 画面用途
- Seedance 生视频提示词
- 负面提示词
- 对应口播/字幕
- 审核状态
- 修改意见

表格中不要包含 `预览链接` 列。若用户需要图片生成提示词，把它放在单独备份 sheet，不要混入主审核表。

Seedance 图生视频提示词必须强调：

- `use the provided image as the first frame`
- 动作连续、单镜头目标清晰
- 同一人物脸、发型、衣服、配饰保持一致
- 同一产品外形、颜色、瓶身/包装保持一致
- 轻微手持、自然生活节奏、真实 UGC 手机画面
- 不生成字幕/文字叠加，除非用户明确要求

## 模型适配

- Seedance：强调动作连续、生活化节奏、自然光、轻微手持移动。
- Runway：强调单镜头动作清晰、主体一致、避免过多对象同时运动。
- Kling：强调真实物理动作、手部操作、镜头推进、产品位置稳定。
- Pika：提示词更短，适合做快速可循环小动作或转场镜头。

## 负面提示词

根据画面需要追加：

`no exaggerated commercial style, no luxury studio set, no plastic skin, no distorted hands, no extra fingers, no unreadable text, no fake brand logos, no medical claims, no before-after body transformation claim`

## 合规措辞

提示词和脚本都避免：

- guaranteed, best, 100%, must-have, miracle, cure, permanent, instant result
- 医疗治愈、疾病改善、减重承诺、收益承诺
- 虚假库存、虚假限时、虚假达人身份
- 平台敏感引流词，例如诱导站外私信、私下交易、规避平台审核
