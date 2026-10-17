# REVIEWING.md — 审稿手册（可独立使用）

> 配套：`SKILL.md` §6.3、`guides/citations.md`、`templates/review-report.md`。
> 目标：写出**有证据、可复核、不冤枉作者、也不放过错误**的 review。

---

## 0. 审稿人合同

1. **先总结，再判断**：读完 abstract/intro/method/results，用 3 句话复述论文；
   复述不出来，说明论文没写清，而不是"没有贡献"。
2. **每个负面意见必须有位置**：`section/paragraph/table/figure/line`。没有位置的
   意见是印象，不是 review。
3. **不编造引用**：不要在 review 里写 "the authors ignore Smith et al. 2023"，
   除非你**打开过**那篇论文并确认它相关。
4. **不要求不可能的 experiment**：rebuttal 期间做不出来的新数据集/新人工标注，
   不作为 reject 理由；要求 clarification 或有界补充。
5. **区分"我不懂"和"写得不清"**：前者可能是你的知识缺口；先查定义/引用。
6. **保密**：不传播稿件、不把稿件内容喂给外部工具（除非 venue 允许）。
7. **利益冲突**：有 COI 就回避；不要审自己/合作者的稿。

---

## 1. 30 分钟 triage（决定要不要细读）

| 检查 | 问题 | 红灯 |
|---|---|---|
| Fit | 主题是否在 venue 范围？ | 明显不 fit |
| Claim | 一句话贡献是什么？ | 读完 abstract 仍不知道 |
| Evidence | 主 claim 有没有直接证据？ | 只有 "we believe" |
| Novelty | 与最近 3 篇的差异？ | 只换数据集/模型 |
| Integrity | 引用/数字是否可疑？ | 明显编造/对不上 |
| Reproducibility | 有没有 artifact/细节？ | 没有代码/数据/超参 |

Triage 只决定**阅读深度**，不决定最终分数。

---

## 2. 先写 3 句总结（强制）

```
The paper addresses <problem>.
It proposes <object/method>, evaluated on <splits> with <metrics>.
The main claim is <claim>, supported by <evidence type>.
```

如果三句里有任何一句需要猜，标记 `UNCLEAR`，在 review 里引用对应段落。

---

## 3. Claim–Evidence 矩阵（review 的核心）

从 abstract、intro 贡献列表、results 各抽 1–3 条 claim，填表：

| Claim ID | 原文位置 | Claim（改写） | 证据 | 状态 | 备注 |
|---|---|---|---|---|---|
| C1 | abstract | 提出 X | §3 定义 + artifact | SUPPORTED | |
| C2 | intro | X 比 Y 好 | Table 2，n=16 | WEAK | 无 CI、单 split |
| C3 | results | 指标失败可分 | Table 6 | SUPPORTED | 但 control 是构造的 |
| C4 | abstract | 跨 domain | 只有 1 个 IT 考试 | UNSUPPORTED | overclaim |

状态：

- `SUPPORTED`：有直接证据，n/CI/setting 清楚。
- `WEAK`：证据存在但不足（小 n、单 seed、无 baseline、构造 control）。
- `UNSUPPORTED`：没有证据，或证据指向反面。
- `UNCLEAR`：看不懂证据与 claim 的对应。

**规则**：`UNSUPPORTED` 的 claim 如果出现在 abstract/intro，至少是 major；
如果主 claim 是 `UNSUPPORTED`，直接 reject 级别。

---

## 4. 数字审计（至少做 3 个 + 1 个 delta）

1. 选 3 个关键数字：主结果、baseline、ablation。
2. 在表/图/正文/JSON 中定位；看 n、单位、四舍五入。
3. 重算至少 1 个 delta 或百分比：
   - 0.00→0.45 是 **45 pp**，不是 45%。
   - 73.3 − 72.6 = 0.7；57.5 − 47.9 = 9.6。
4. 检查分母：n=16 还是 86 帧？macro 还是 micro？
5. 检查 CI/seed：没有就记为 `WEAK`，但不要因此直接 reject（除非主 claim 依赖显著性）。

常见问题：

- 表里一行是 n=86，另一行是 n=16，却在同一段比较。
- "average" 没说是 frame-level 还是 episode-level。
- 百分比/百分点混用。
- 图表数字与正文不一致（跑一下 artifact 就能发现）。

---

## 5. 方法审计

| 维度 | 问什么 | 红旗 |
|---|---|---|
| Problem formulation | 对象/假设/边界是否清楚？ | 定义循环、符号未定义 |
| Identifiability | 结论是否只能由该机制解释？ | 混淆变量、leakage |
| Baselines | 是否同 setting、同 split、同预算？ | strawman、缺 strong baseline |
| Controls | 每个 control 改了什么？ | 文本替换冒充模块删除 |
| Statistics | n、seed、CI、多重比较？ | 单 seed、只报最好 |
| Ablation | 是否真的移除组件？ | 只改输入文本 |
| Compute | 是否可复现？ | 没写模型版本/硬件 |
| Failure cases | 有没有 negative results？ | 只报成功 |

**关键区分**：作者说 "ablation"，你要看代码/描述里**实际改变了什么**。如果
"w/o X" 只是把文本换成 `"Okay."`，那不是 ablation，是 input corruption。

---

## 6. 引用审计（5–10 篇）

- 选：最接近的 3 篇 + 主 claim 依赖的 2 篇 + 随机 3 篇。
- 查：标题/作者/年份/venue 是否对；是否真的支持被引用的句子。
- 工具：DOI、arXiv、ACL Anthology、出版社页面。
- 规则：**没有反证，不说 "fake"**。可以说 "I could not verify this reference"。
- 如果发现 arXiv ID 指向另一篇论文，这是强证据，写进 review（附 ID 和真实标题）。
- 如果发现"引用存在但不支持该句"，写 "citation does not support the claim"，
  比 "wrong citation" 更准确。

---

## 7. Artifact 审计（如果提供）

在 `/tmp` 里做，不要污染作者仓库：

```bash
git clone <artifact> /tmp/rev-artifact && cd /tmp/rev-artifact
cat README.md
# 按 README 跑最小命令；记录命令、退出码、输出
```

检查：

- README 是否有环境、数据、命令、预期输出、运行时间。
- 能否在没有 API key 的情况下跑主表（cache-only）。
- 表格是否可由脚本再生；随机 seed 是否固定。
- 是否有 license、匿名性、敏感信息。
- 失败时记录**具体命令和错误**，不要写 "artifact does not work"。

---

## 8. Novelty / positioning

- 最近 3 篇是什么？本文与它们的**最小差异**是什么？
- 差异是"新对象/新机制/新证据/新场景"，还是"换数据集/换模型/换指标名"？
- 如果差异是组合式的，作者是否证明了组合的必要性（ablation）？
- 不要用 "incremental" 作为唯一理由；要指出**缺哪一块证据**。

---

## 9. Ethics / limitations

- 人类受试/未成年人/教育数据：IRB、同意、去标识。
- 数据许可：考试原题、扫描件、API 条款。
- LLM 使用：是否披露、是否用于生成实验结果。
- 双用/安全：教育场景的过度依赖、错误解释的风险。
- Limitations 是否**具体**（n、domain、构造效度、外部效度），还是套话。

---

## 10. Presentation

- 结构：abstract→intro→method→results 是否能连成一条线。
- 图：能否不看正文看懂；有没有 orphan figure；颜色/字号。
- 表：有没有 n、单位、best 标注、误差。
- 写作：术语一致、缩写展开、句子长度、typos。
- **不要把 typos 当主问题**；列在 minor，不要占据 review 主体。

---

## 11. 评分 rubric（按 venue 调整）

每项 1–4：

| 维度 | 1 | 2 | 3 | 4 |
|---|---|---|---|---|
| Soundness | 方法/结论不成立 | 有明显漏洞 | 基本成立，有边界 | 严谨，control 充分 |
| Novelty | 已知结果 | 组合/小改 | 有新对象/机制 | 明显新视角 |
| Significance | 无关 | 小众 | 对子领域有用 | 广泛影响 |
| Clarity | 难懂 | 部分清楚 | 清楚 | 优秀 |
| Reproducibility | 无法复现 | 缺关键细节 | 基本可复现 | artifact 完整 |

Overall（1–10）与 recommendation：

| Overall | Recommendation |
|---|---|
| 8–10 | Accept / Strong accept |
| 6–7 | Weak accept / Borderline accept |
| 5 | Borderline |
| 3–4 | Weak reject / Reject |
| 1–2 | Strong reject |

Confidence（1–5）：1 = 猜，3 = 熟悉子领域，5 = 非常熟悉且检查过 artifact。

**校准**：如果论文的 claim 是 `WEAK` 但方法诚实、边界清楚，soundness 可以是 3，
overall 5–6；不要因为"不够惊艳"给 3。

---

## 12. Review 报告模板

```markdown
# Review: <title>

## Summary (3 sentences)
...

## Strengths
1. ... (evidence: §/Table/Fig)
2. ...

## Weaknesses
1. **[Major]** ... (location; why it matters; what evidence would fix it)
2. **[Minor]** ...

## Claim–evidence notes
| Claim | Status | Evidence | Note |
|---|---|---|---|

## Questions for authors
1. ...

## Minor issues
- ...

## Score
- Soundness: /4
- Novelty: /4
- Significance: /4
- Clarity: /4
- Reproducibility: /4
- Overall: /10
- Confidence: /5
- Recommendation: ...
```

要求：

- Strengths 至少 2 条，且具体；不要 "well written"。
- Weaknesses 按 severity 排序；每条给"什么证据能解决"。
- Questions 只问**能影响判断**的；不要问 "why not more datasets" 这种无限要求。
- Minor 不超过 10 条；typos 合并成一行。

---

## 13. 反幻觉规则（review 专用）

| 陷阱 | 规则 |
|---|---|
| 记忆里的引用 | 不打开不引用；写 "I could not verify" |
| "作者没做 X" | 先查 appendix/artifact/脚注；没有证据写 "I could not find X" |
| "这个方法肯定不行" | 给具体失败条件或反例；否则是 opinion |
| "缺 SOTA" | 先确认 setting 是否可比；不可比就不要求 |
| "样本太小" | 给最小可接受 n 或 power 分析；否则是口号 |
| "novelty 不足" | 点名最近工作 + 差异；不要空泛 |
| 伪造分数 | 用 rubric；不要凭感觉给 2 又写不出理由 |
| 把"我不懂"当"不清楚" | 先查定义/引用；仍不懂再写 question |

---

## 14. Meta-review（AC）

- 汇总 3 个 review 的**分歧点**，不要简单平均。
- 判断分歧是"事实分歧"（可核查）还是"判断分歧"（需 AC 裁量）。
- 检查作者 response 是否回答了核心问题；不要把"没做新实验"自动当失败。
- 给 decision 时写：主 claim 是否 supported、community 价值、可修复性。
- 对作者：给可执行的 camera-ready 清单；对 PC：给一句话理由。

---

## 15. 快速自检（提交 review 前）

1. 我能不能用 3 句话复述论文？
2. 每个负面意见有没有位置和证据？
3. 我有没有要求 rebuttal 做不出来的东西？
4. 我引用的文献都打开过吗？
5. 分数和文字一致吗？（文字说 major，分数 7，不一致）
6. 有没有把"写作问题"当"方法问题"？
7. 有没有泄露稿件内容/身份？
