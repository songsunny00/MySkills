---
name: novel-outline-reviewer
description: Use when reviewing novel chapters or manuscripts for logic consistency, character authenticity, plot cohesion, foreshadowing payoff, emotional resonance, narrative vividness, and content compliance. Also triggers for first-chapter editorial audits against web novel platform submission standards. Triggers on requests like "check the story", "review this chapter", "is this consistent with character", "improve story flow", "add foreshadowing", "check content safety", "前三章审核", "过稿检查", "开篇钩子", "审查前三章", or "editorial submission check".
---

# Novel Outline Reviewer

## Overview

Systematically evaluate novel content. When reviewing chapters 1–3, **always run the First-Chapter Editorial Gate first** — if it returns NOT READY, halt and prompt the user before proceeding. For all other chapters, go straight to the Nine-Dimension Review (D1–D9).

## Preparation (REQUIRED Before Any Review)

Load context in parallel:
1. **Character files** — `characters/*.md` (personality, speech patterns, emotional baseline, growth arc)
2. **Outline** — `plot/outline.md` (chapter hooks, timeline, plot beats)
3. **World-building** — `worldbuilding/world.md` (setting rules, cultural context)
4. **Target chapters** — the content to review

## 【前置门控】前三章过稿适配审核 First-Chapter Editorial Gate

**仅当审查内容为第1–3章时运行。** 直接对正文进行审查，无需预加载角色卡或大纲。

> **⚠️ HALT RULE（强制执行）**
> 若本门控总评为 **NOT READY**，立即停止，输出门控报告后向用户提示：
> _"前三章过稿审核未通过，建议先修改以下问题，再进行深度九维审查。是否现在继续后续审查？"_
> **等待用户明确确认后，再决定是否进入 D1–D9。**

---

### 开篇生死线 Opening Hook

检查第一章前三行 / 首段：
- 是否在前三行出现明确的冲突、危机或悬念？
- 是否存在任何慢热铺垫：环境描写、背景交代、内心独白优先于冲突？

**判定标准：**
- PASS：前三行即见矛盾/危机/未知威胁
- FAIL：开篇以场景描写、角色介绍或情绪铺垫起笔，冲突延迟出现

> 编辑筛稿逻辑：80% 读者前三行看不到冲突直接划走，慢热开篇等于主动出局。

---

### 钩子密度 Hook Density

逐 500 字扫描，每区间至少存在一个钩子类型：

| 钩子类型 | 示例 |
|---------|------|
| 神秘线索 | 出现无法解释的细节或异常现象 |
| 角色反常行为 | 人物做出与处境明显不符的选择或反应 |
| 未知危机 | 读者感知到威胁，但主角尚未察觉 |
| 未解谜团 | 提出问题，暂不给答案 |

**判定：** 任意 500 字区间无钩子 = NEEDS ATTENTION；连续两个区间无钩子 = CRITICAL。

---

### 情绪曲线 Emotional Arc

绘制全章情绪走势：
- 是否存在可识别的"虐 → 爽 → 虐 → 大爽"循环或其变体？
- 是否有至少一个情绪高点和一个低谷？
- 章节结尾是否在张力上升而非消解中落幕？

**常见失误：**
- 全章平稳叙事，无情绪波峰
- 结尾在平静解决中收束，失去追更动力

---

### 人设反差 Character Contrast

主角是否具备清晰的人设反差（反差感）？
- 典型模式：高冷外表/私下软萌；表面废柴/暗藏能力；善良外壳/背负秘密
- 反差是否通过行动或对话在前三章呈现，而非仅靠旁白说明？

**判定：** 主角无辨识度反差、形象扁平 = NEEDS ATTENTION；与同赛道主角高度同质 = CRITICAL。

---

### 节奏水分检测 Pacing & Padding

扫描以下水文信号：
- 是否存在既不推进情节、也不揭示人物的冗余场景？
- 是否有超过 150 字的纯描写段落（无行动/对话打断）？
- 是否有可整段删除而不影响上下文的对话或叙述？

**判定：** 单章内出现 2 处以上水文 = NEEDS ATTENTION；节奏整体拖沓 = CRITICAL。

---

### 核心梗架构 Core Premise Check

验证故事基础公式：**普通人 + 异常事件 + 紧迫生死困境**
- 主角身份是否接地气、有代入感（避免开篇即强者）？
- 异常事件是否在第一章内发生，触发核心矛盾？
- 是否设置了明确的时间压力或代价（不解决=严重后果）？

**判定：** 公式缺少任意一项 = NEEDS ATTENTION；三项均缺 = CRITICAL。

---

### 章节结尾钩子 Chapter-End Hooks

逐章检查末段：

| 章节 | 结尾钩子类型 | 强度 |
|------|------------|------|
| 第1章 | [突发危机 / 关键反转 / 悬而未决的问题 / 其他] | STRONG / WEAK / FAIL |
| 第2章 | [同上] | STRONG / WEAK / FAIL |
| 第3章 | [同上] | STRONG / WEAK / FAIL |

**判定：** 任意章节在平静解决中结束，无前向拉力 = FAIL，须加入追更钩子。

---

### 投稿合规排查 Submission Compliance

**每项必须给出 PASS / FAIL，不得笼统评价。**

| 检查项 | 规则 |
|--------|------|
| 真实地名 | 禁止出现可识别的真实地名（城市、街道、学校、机构等） |
| 暴力描写 | 死亡/伤害场景须用意外替代（车祸、失足、突发疾病），禁止血腥分尸、投毒细节 |
| 未成年限制 | 未成年角色禁止恋爱描写和肢体接触 |
| 视角节奏 | 每300字内有视角焦点切换或场景动作，避免长段单视角内心独白 |
| 对话伏笔 | 重要对话是否暗藏可供后期呼应的细节，而非纯功能性推进 |

任一项 FAIL = 投稿前必须修改。

---

**门控总评：**
- **READY** — 全部通过，开篇竞争力达标，继续进行 D1–D9 深度审查
- **NEEDS REVISION** — 存在 WEAK 或 NEEDS ATTENTION 项，建议修改后投稿；可选择继续 D1–D9
- **NOT READY** — 存在 FAIL 或 CRITICAL 项 → **立即停止，提示用户，等待确认**

---

## Nine-Dimension Review

**仅在门控通过（READY 或用户确认继续）后运行。** Work through ALL nine dimensions. Never skip one because "it seems fine."

---

### D1: 逻辑自洽性 Logic Consistency

Ask for EACH scene:
- Does every action have a clear, established motivation?
- Could a reader have predicted this decision from what they know about the character?
- Are timeline and location details consistent across chapters?
- Does new information contradict anything established earlier?

**Common failures:** Character makes uncharacteristically impulsive choice; timeline gaps that don't add up; object/detail appears before it's introduced.

---

### D2: 人物设定一致性 Character Consistency

Compare behavior in chapter against character file:

| Check | Question |
|-------|----------|
| Speech pattern | Does dialogue match their established vocabulary and verbal tics? |
| Emotional response | Would this person react this way given their background? |
| Growth arc | Is any change in behavior earned by prior events, not sudden? |
| Relationship logic | Do interactions reflect established relationship dynamics? |

**Red flag:** A reserved character suddenly opens up with no transitional scene; a logical character acts on pure impulse without internal justification.

---

### D3: 世界观设定一致性 World-building Consistency

Compare every scene detail against `worldbuilding/world.md`:

| 检查项 | 检查问题 |
|--------|----------|
| 地理与空间 | 场景位置、距离、建筑布局与设定吻合？（如场所各楼层功能区、标志性空间等细节） |
| 时代背景 | 技术水平、社会现象、流行事物与故事设定年代相符？ |
| 经济与生活 | 人物消费能力、收入水平与其背景设定匹配？次要角色的生活细节写实？ |
| 规则与惯例 | 故事核心场所的特有规则（如准入门槛、特殊制度等）在各章执行是否前后一致？ |
| 物候与环境 | 季节描写（植物、天气、物候）与故事时间线对应？ |
| 群像生态 | 固定配角（邻居、伙伴、相关人物等）的出场与其设定角色相符？ |

**常见失误：**
- 空间穿越：角色在不同区域间跳跃出现，无合理的位移过渡描写
- 时代错位：故事设定年代下出现明显超前或过时的技术/文化细节
- 经济失真：经济状况受限的角色突然展示与其处境不符的消费行为
- 季节混乱：同一章内植物或天气描写与既定月份/季节不符
- 规则遗忘：中后期剧情中忘记故事核心场所的关键限制性设定

---

### D4: 情节连贯性 Plot Cohesion

- Does this chapter's opening honor the previous chapter's hook?
- Do subplots connect to the main plot naturally, not forcibly?
- Pacing check: is this scene doing double duty (advancing plot AND revealing character)?
- Are scene transitions marked clearly (time jumps, location changes)?

---

### D5: 伏笔与回收 Foreshadowing & Chekhov's Gun

Maintain a running foreshadowing ledger:

```
PLANTED: [detail/item/line] in Chapter X
PAID OFF: [resolution] in Chapter Y — or — STATUS: OPEN
```

Check:
- Every significant object introduced — does it serve a purpose?
- Every open thread — is there a plan to close it?
- Are planted seeds subtle enough not to telegraph, but clear in retrospect?
- Do recurring motifs (imagery, objects, phrases) reinforce theme?

---

### D6: 感染力与情感共鸣 Emotional Resonance

**Show-don't-tell audit:** For every direct emotion statement ("she felt sad"), find a behavioral or sensory replacement.

| Weak | Strong |
|------|--------|
| "She felt lonely" | "She reheated the same tea three times without drinking it" |
| "He was nervous" | "He checked the door twice, then checked it again" |

Five-sense check — does the scene use more than just visual description?

Emotional beat map:
- Where does the reader's heart lift?
- Where does tension spike?
- Where is there silence that resonates?

Dialogue naturalness: read lines aloud — would a real person say this?

---

### D7: 语言节奏与意象 Language Rhythm & Imagery

- Sentence variety: mix of short punches and longer flowing sentences, especially in emotional peaks
- Core imagery of the work — are motifs being used consistently, not randomly?
- Important scenes: do they get adequate space, or are they rushed?
- Transitional scenes: are they tight, or do they bloat?
- Signature phrases/metaphors — reused meaningfully, not accidentally

---

### D8: 内容红线合规 Content Compliance

**This dimension is MANDATORY and must produce a PASS/FAIL verdict, not just "NEEDS ATTENTION."**

Check each item below. Any single violation = CRITICAL, must be flagged and fixed before publication.

| 红线类别 | 检查内容 |
|---------|---------|
| 政治与地域 | 无政治敏感内容、无地域歧视表达、无民族/宗教违规描写，不涉及敏感历史事件或敏感人物 |
| 暴力与违法 | 无暴力、血腥、惊悚、恐怖情节，无打架斗殴场景，无违法犯罪或灰色产业描写 |
| 色情与两性 | 无低俗色情、无露骨性描写，情感线方向纯爱治愈、积极健康，不含不良两性关系导向 |
| 消极心理导向 | 无消极厌世情绪、无自杀/自残内容、无躺平摆烂导向，不渲染焦虑，不传播负面情绪；若涉及抑郁/心理健康话题，须以康复和积极连接为方向 |
| 信息真实性 | 无虚假信息、无不良引导；乡村生活、职场情节均为现实正向描写，符合公序良俗 |
| 版权原创性 | 所有设定、情节、人物均为原创，未抄袭、未改编违规素材，对话及场景不与已知作品高度相似 |

**注意：** 抑郁症等心理健康话题本身不违规，但描写方向必须指向康复与连接，不得渲染绝望或美化轻生。

---

### D9: 读者高光体验 Reader Highlight Experience

**This dimension evaluates whether the chapter delivers memorable moments that make readers want to keep reading, share quotes, or reread scenes.**

Check each category:

| 类型 | 检查问题 |
|------|----------|
| 名场面 | 是否有让人"刷到这段必停下来"的画面或对话？场景是否有独特的画面感和记忆点？ |
| 高光时刻 | 角色有没有说出或做出让读者拍案叫绝、想截图的瞬间？ |
| 爽点 | 有没有让读者"终于来了"的情节释放？积压的张力是否有出口？ |
| 撒糖时刻 | 情感线有没有甜蜜细节？男女主的互动有没有让读者"磕到了"的moment？ |
| 群像魅力 | 配角是否有存在感？多人场景中每个角色是否有自己的反应和声音？ |
| 温馨时刻 | 有没有让读者心里一暖、想到"原来生活可以这样"的画面？ |

**密度检查：** 每3000字至少应有1个以上高光类型的时刻。若整章无任何一类，即使逻辑通顺，读者也会感到"平"。

**常见问题：**
- 爽点被过渡带走：关键情节释放后立刻跳场景，读者还没反应过来
- 糖被稀释：撒糖动作埋在大段叙述里，没有给留白让读者感受
- 群像扁平：多人对话时，几个角色的声音可以互换，没有个体辨识度
- 温馨过于说教：直接写出"主角感到温暖"，而不是用具体细节让读者自己感受到

---

## Output Format

For each dimension, report:

```
## [Dimension Name]
STATUS: PASS / NEEDS ATTENTION / CRITICAL

Issues found:
- [Chapter X, Scene Y]: [specific problem] → Suggested fix: [concrete rewrite direction]

Strengths worth preserving:
- [What's working well]
```

**D8 special rule:** Must list each of the 6 red-line categories with PASS or FAIL. Any FAIL must include the exact offending text and a concrete rewrite direction. Do not summarize as "looks fine" without item-by-item confirmation.

**Gate special rule (first 3 chapters only):** Must list each of the 7 sub-checks with PASS / WEAK / FAIL. End with a clear READY / NEEDS REVISION / NOT READY verdict. Any FAIL in Submission Compliance automatically blocks the READY verdict. If NOT READY, halt here and prompt the user before proceeding to D1–D9.

End with a **Priority Fix List** (max 5 items, ranked by impact on reader experience). Priority order: Gate NOT READY items → D8 CRITICAL → D9 CRITICAL → other dimensions.

## Key Principles

- Specific beats vague. "[Character]'s response in Ch.X contradicts her stated emotional pattern of [specific trait, e.g. not showing vulnerability in public]" beats "character feels inconsistent."
- Every suggestion must be actionable — point to the exact line or scene.
- Preserve the author's voice. Suggest directions, not prescriptive rewrites unless asked.
- A story that moves the reader earns forgiveness for minor logic gaps. Prioritize resonance over technical perfection.
