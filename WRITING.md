# WRITING.md — 论文写作手册（可独立使用）

> 配套：`SKILL.md` §5 的 Gate、`guides/evidence.md` 的 claim ledger、`conferences/*` 的 venue 标准。
> 目标不是"写得像论文"，而是**让每一句话都能被证据接住**。

---

## 0. 使用方式

写作前先回答三个问题，答不上来就不要开写：

1. **一句话贡献**是什么？（不是"我们研究 X"，而是"我们提出/证明/发现 Y，证据是 Z"）
2. **它 falsify 什么**？如果结果为负，论文还成立吗？
3. **目标 venue 的审稿人最可能杀哪一条**？（先写下来，再决定实验和措辞）

写作顺序建议：`method → experiments → results → related → intro → abstract`。
摘要最后写，它只能总结**已经 supported** 的 claim。

---

## 1. 开写前的输入（缺一不可）

| 输入 | 文件 | 没有会怎样 |
|---|---|---|
| Claim ledger | `paper_state/claim-ledger.csv` | 摘要/ intro 会写飞 |
| Experiment registry | `paper_state/experiment-registry.csv` | 数字对不上代码 |
| Canonical numbers | `paper_state/numbers.json` | 表格/正文各说各话 |
| Figure registry | `paper_state/figure-registry.csv` | 图没人引用、无法复现 |
| Conference profile | `paper_state/conference.yaml` | 页数/模板/匿名要求靠猜 |
| Citation audit | `paper_state/citation-audit.md` | 编造引用 |

**规则**：没有 ledger 行，不写 claim；没有 registry 行，不写数字；没有
profile，不写"本刊要求"。

---

## 2. 一页纸的合同（先写这 5 行）

```
C1 (object):   We introduce <X>, which <does what>.
C2 (mechanism): It works by <Y>, unlike <closest prior> which <Z>.
C3 (evidence):  On <splits>, it <result>, with <metric/CI/n>.
C4 (boundary):  We do not claim <non-claims>.
C5 (falsifier): The claim fails if <control> shows <pattern>.
```

要求：

- C1 里不能出现 "novel / powerful / significant" 这类无对比的形容词。
- C2 必须点名**最近的一篇**工作，并说清差异；否则 related work 会空。
- C3 必须有数字、split、n；没有就写 `TODO(evidence)`。
- C4 是审稿人最喜欢引用的部分；主动写，能挡掉一半 overclaim。
- C5 是这篇论文的"可证伪性"；没有 C5 的论文容易被判为 "incremental"。

### 2.1 贡献列表（最多 3 条）

每条贡献 = **名词短语 + 证据**，不要写"我们进行了大量实验"。

```
- A falsifiable trace contract: <definition>, audited by <metrics>, with <falsifier>.
- A benchmark/split: <name>, <n>, <provenance>, <what it isolates>.
- A diagnostic finding: <direction>, <effect>, <boundary>.
```

第 4 条通常是 "reproducible artifact"，可以放，但不要超过 4 条。

---

## 3. 故事架构（gap → object → method → evidence → boundary）

| 段落 | 必须回答 | 常见错误 |
|---|---|---|
| Gap | 现有评估/方法缺哪一层？为什么不是"再刷一个点"？ | 把"没人做过"当 gap；没引最近工作 |
| Object | 你评估/优化的对象是什么？边界在哪？ | 对象和实现混在一起 |
| Method | 最小机制是什么？为什么能解决 gap？ | 公式堆砌，没有直觉 |
| Evidence | 哪个实验能单独杀死哪个替代解释？ | 只报主结果，没有 control |
| Boundary | 哪些结论不成立？ | 全留在 limitations，摘要却 overclaim |

**段落功能测试**：把每段第一句抽出来，应该能连成一篇 200 字的故事。连不成，
说明段落是"资料堆"而不是"论证链"。

---

## 4. 分节 playbook

### 4.1 Abstract（150–250 词，最后写）

六句结构：

1. 领域 + 被忽视的失败模式（1 句）
2. 现有 endpoint 为什么不够（1 句）
3. 我们提出什么（1 句，命名）
4. 它怎么工作（1 句，机制，不展开）
5. 关键证据（1–2 句，**只写 supported 的数字**）
6. 边界/不声称什么（1 句）

检查：摘要里的每个数字，必须能在正文表格中找到；摘要里不能出现正文没定义的
缩写；不能出现 "state-of-the-art" 除非有同 setting 的对比。

### 4.2 Introduction（1–1.5 页）

五段：

1. **场景**：读者能复述的具体失败（一个例子胜过三个形容词）。
2. **缺口**：现有投影各自漏了什么，用一张"层 × 缺失绑定"的表/图。
3. **对象**：本文评估/构造什么，给出定义句；不要在这里讲实现。
4. **证据预告**：3 条贡献，每条一句，带数字。
5. **边界**：明确不 claim 什么；一句话把审稿人的最大误解先堵住。

**Do**：第一页出现"评估目标"框（`\askbox` 式），让读者 30 秒知道你在测什么。
**Don't**：用 "Recent advances in LLMs have revolutionized..." 开头。

### 4.3 Related Work（0.75–1 页）

不要写"文献综述"，写**定位矩阵**：

| 层 | 代表工作 | 观测单元 | 漏掉的绑定 | 本文补什么 |
|---|---|---|---|---|

规则：

- 最近 3 年的工作至少覆盖 60%；最接近的 3 篇必须单独一段。
- 每篇只写"它做了什么 + 它没做什么 + 与本文关系"，不要复述摘要。
- 不要用 "X et al. proposed..." 连续 10 句；用主题分组。
- 所有引用必须过 `guides/citations.md`；不确定的标 `UNVERIFIED`，不要写进 PDF。

### 4.4 Method / Problem Formulation（1.5–2 页）

顺序：

1. **Notation table**：符号、含义、维度；正文用到的每个符号都出现。
2. **Definitions**：对象、指标、约束；先定义后使用，不要"边用边定义"。
3. **Objective / algorithm**：最小伪代码或公式；说清输入输出。
4. **Assumptions**：显式列出；审稿人会用它们攻击 generality。
5. **Complexity / cost**：时间、显存、API 调用；没有就写 "not measured"。

常见错误：

- 公式里的 $n$、$m$、$T$ 没定义（这是最高频的 minor）。
- 指标名（EAR/VGR/SCR）没展开，读者不知道缩写。
- 把实现细节（文件、类名）写进方法；放到 artifact/appendix。

### 4.5 Experiments（1.5–2 页）

每个实验回答**一个**问题：

```
E1: Does the object separate answer-only vs trace-aware tutors?  → Table 3
E2: Does the judge ranking change across families?               → Table 5 / Fig 4
E3: Does the metric fail when <binding> is broken?               → Table 6
```

必须写：

- **Baselines**：为什么是这些？哪个是 floor，哪个是 strong baseline？
- **Controls / ablations**：每个 control 改变哪个变量？不要"删模块"式假消融。
- **Splits / n / seeds**：每个数字旁边有 n；有随机性的写 seed 数和 CI。
- **Metrics**：定义、方向（↑/↓）、范围；复合指标写权重。
- **Compute**：硬件、时长、API 模型版本；可复现性的一部分。
- **Negative results**：不显著就写不显著；不要用 "trend" 掩盖。

**反例**：把 `w/o X` 实现成"把文本换成 Okay."，然后说"X 模块必要"。这是
text substitution，不是 ablation；审稿人跑 artifact 会发现。

### 4.6 Results（1–1.5 页）

每个 claim 一段，结构：

```
Claim: <一句话>
Evidence: <表/图 + 数字 + n + CI>
Alternative explanation: <最可能的替代解释>
Why ruled out: <control / 额外分析>
Boundary: <不成立的 scope>
```

不要按"表 2、表 3、表 4"顺序复述；按**论证顺序**组织。表格是证据，不是叙事。

### 4.7 Discussion / Limitations（0.5–1 页）

Limitations 要**具体**：

- 规模：n=16，不是 "small dataset" 这种空话。
- 人群/领域：一个 IT 考试、模拟学生、没有 IRB。
- 构造效度：falsifier 是作者构造的，不是自然分布。
- 指标：lexical、substring、无词边界；给出敏感性。
- 外部效度：没有 classroom、没有 human teacher ratings。

每条 limitation 后面跟一句"这为什么不推翻主 claim"或"下一步怎么补"。

### 4.8 Conclusion（3–5 句）

只做三件事：重申对象、重申最强证据、重申边界。不要引入新 claim、新数字、
新引用。

---

## 5. Claim 纪律

### 5.1 Claim 类型与强度

| 类型 | 句式 | 需要的证据 | 不能写成 |
|---|---|---|---|
| Existence | "We introduce X" | 定义 + 可用 artifact | "X is the first"（除非查过） |
| Comparative | "X outperforms Y on Z" | 同 setting、同 split、n、CI | "X is better"（无 baseline） |
| Causal | "A causes B" | 控制变量 / 干预 / 消融 | "A correlates with B" 写成因果 |
| Generality | "works across domains" | 多 domain、多模型 | 单数据集外推 |
| Mechanistic | "because of M" | 机制实验 / 中介分析 | 只凭相关性 |

### 5.2 强度阶梯（从弱到强）

```
consistent with <mechanism>
→ suggests
→ indicates
→ shows (on <split>, n=<n>)
→ demonstrates (with control <C>)
→ establishes (rare; needs multiple settings)
```

默认用 `shows/indicates`；`demonstrates` 只在有 control 时用；`establishes`
几乎不用。

### 5.3 Hedging 不是免责

- "may potentially suggest" 堆三个词，不会让 claim 变安全，只会让审稿人觉得你
  自己也不信。**一个 hedge + 一个具体 boundary** 最好。
- 每个强 claim 后面跟一句 "This holds for <scope>; we do not claim <outside>."

---

## 6. 数字纪律

| 规则 | 做法 |
|---|---|
| 单一来源 | 每个数字在 `numbers.json` 有一条，带 `source` |
| 生成而非手打 | 表格/图由脚本从 JSON 生成；`.tex` 里不出现手写数字 |
| 四舍五入 | 全文统一小数位；0.5623 → 0.56（两位），不要一处 0.56 一处 0.562 |
| n 始终可见 | 表格 caption 或列头写 n；正文每个比较写 n |
| 百分比 vs 百分点 | 0.00→0.45 是 **45 pp**，不是 45%；pre=0 时相对百分比无定义 |
| CI / seed | 有随机性的结果给 seed、重采样数、CI；没有就说 "single run" |
| 单位 | ms/s、GB、% 统一；复合指标写权重 |
| 负数/缺失 | 用 `n/a` 或 `—`，不要用 0 冒充缺失 |
| 一致性 | 摘要 = 正文 = 表 = 图 = JSON；改一处，全链路重跑 |

**自检命令**：`python3 scripts/check_numbers.py --config paper_state/numbers.json --tex main.tex`

---

## 7. 引用纪律

1. **每篇引用都要能点开**：DOI / arXiv / ACL / 出版社页面。查不到 → `UNVERIFIED`，
   不进 PDF。
2. **不要凭记忆写元数据**：作者顺序、年份、venue、页码是最容易错的部分。
   arXiv ID 必须打开确认标题一致（这是抓"编造引用"最快的方法）。
3. **最接近的 3 篇必须真读**（至少 abstract + intro + 结果表），否则 related
   work 会写成"假定位"。
4. **不要用引用撑句子**：`\cite` 放在具体主张后面，不要放在句尾当装饰。
5. **自引**：匿名期用第三人称；不要写 "our previous work"。
6. **数量**：主文 30–50 篇足够；多出来的放 appendix，不要凑数。

详见 `guides/citations.md`。

---

## 8. 图表纪律

**一张图一个 message**。图注第一句就是 message，不是 "Overview of our method"。

| 检查 | 标准 |
|---|---|
| 自包含 | 不看正文也能懂：轴、单位、n、误差条、颜色含义 |
| 生成 | 有脚本 + 数据源；registry 里有 `script` 和 `data` |
| 引用 | 每个 float 至少一个 `\ref`；图 1 不能"挂"在文首没人提 |
| 数字 | 图里的数字来自 JSON，不是 hand-tuned；改数据必须重画 |
| 可读性 | 字号 ≥ 7pt；不靠颜色区分；灰度可读；误差条有定义 |
| 诚实 | 截断轴要标注；不画 0 基线误导；不省略失败条件 |

**Caption 公式**：

```
\textbf{<Message>.} <Setup: data/split/n>. <What is shown, including error bars>.
<Key takeaway with number>. <Caveat/boundary>.
```

反例：图注写 "Results on Z20."，正文却用这张图支撑 "blank page detector fails"——
图注没有 message，读者/审稿人无法验证。

---

## 9. 写作风格

- **一段一论点**：第一句是 topic sentence，最后一句是 implication。
- **主动语态**，过去时写实验，现在时写事实/定义。
- **术语一致**：一个概念只用一个词；不要 "trace/frame/step" 混用。
- **缩写首次出现展开**：EAR、VGR、SCR、OTP、ATEP 都要给全称。
- **不要 hype**：significant / novel / powerful / revolutionary 只在有对比时用。
- **不要 "we believe"**：要么有证据，要么写 "we hypothesize"。
- **句子长度**：平均 20–25 词；超过 40 词拆开。
- **段落长度**：4–8 句；超过 10 句拆开。

---

## 10. 匿名、伦理、合规

- 匿名：作者名、机构、邮箱、GitHub、致谢、基金号、自引第一人称、PDF metadata。
- 数据：许可、PII、考试原题版权、扫描件来源；不能放的写"derived caches only"。
- LLM 使用：按 venue 政策披露（写作辅助 vs 生成内容）；不要隐去。
- 双投：确认没有同时投；arXiv 政策按 venue。
- 伦理：人类受试、未成年人数据、教育场景需 IRB/同意；没有就写 "no IRB study"。

---

## 11. 页预算与删减顺序

以 7 页正文为例（按 venue 调整）：

| 部分 | 预算 |
|---|---|
| Abstract | 0.2 |
| Intro | 1.0 |
| Related | 0.75 |
| Method | 1.75 |
| Experiments/Results | 2.0 |
| Discussion/Limitations | 0.6 |
| Conclusion | 0.2 |
| Floats | 0.5–1.0 |

删减顺序（从先到后）：相关工作的次要引用 → 实现细节 → 次要 ablation →
重复的结果句 → 图（合并 panel）→ 公式推导（移 appendix）。**不要**删
limitations 或 control。

---

## 12. 写作时最常见的 LLM 错误（逐条自检）

| 错误 | 症状 | 预防 |
|---|---|---|
| 编造引用 | 作者/年份/venue 对不上；arXiv ID 指向别的论文 | `check_citations.py` + 逐条打开 |
| 占位数字 | "0.XX"、"~0.8"、"significantly better" 无数字 | `numbers.json` + gate G2 |
| stale 数字 | 重跑后正文/表没更新 | 生成脚本 + `check_numbers.py` 的 `bad_values` |
| 假消融 | 用文本替换冒充模块删除 | 读实现；写"stress test"而不是"ablation" |
| orphan float | 图/表没 `\ref` | `check_floats.py` |
| claim drift | 摘要比结果强 | claim ledger 状态 + 摘要只写 supported |
| 术语漂移 | trace/frame/step 混用 | 术语表；grep 检查 |
| 会议规则幻觉 | "AAAI 是 8 页" | 读 CFP；profile `verified_on` |
| 过度 hedge | "may potentially suggest" | 一个 hedge + 一个 boundary |
| 假 general | 单数据集说 "across domains" | 明确 scope；多 domain 才写 |

---

## 13. 投稿前 checklist（按顺序）

1. `scripts/build.sh` 干净编译；0 undefined；页数在限内。
2. `scripts/check_numbers.py` 全绿；摘要/正文/表/图一致。
3. `scripts/check_citations.py` 全绿；`UNVERIFIED` 为 0（主文）。
4. `scripts/check_floats.py` 全绿；每个 float 有 ref、有 caption、有脚本。
5. `scripts/check_anonymity.py` 全绿。
6. `REVIEWING.md` 走一遍，至少 3 个 BLOCKER 级自问自答。
7. 朗读 abstract + intro 第一页；每句能落到证据。
8. 检查 PDF：字体嵌入、图不糊、表不超宽、参考文献完整。
9. 记录 hash（`shasum -a 256 main.pdf`）和页数到 `audit-log.md`。
10. 打包 artifact：脚本、JSON、README、许可证；排除 `paper_state/`、`.env`、日志。

---

## 14. 句式模板

**Gap**：
> Existing evaluations of <object> reduce it to <endpoint>, which cannot distinguish
> <failure A> from <failure B>; as a result, <consequence>.

**Object**：
> We define <X> as <formal object>; a valid <X> must satisfy <conditions>.

**Method**：
> <Name> computes <quantity> from <public inputs> only; it does not require <hidden signal>.

**Evidence**：
> On <split> ($n=<n>$), <system> obtains <metric> $=<value>$ (95% CI <lo>–<hi>),
> compared with <baseline> at <value>; the gap is <delta> <unit>.

**Boundary**：
> These results hold for <scope>; we do not claim <outside scope>, because <reason>.

**Falsifier**：
> If <control> leaves <metric> unchanged while <other metric> drops, the metric is
> not measuring <construct>; E<k> performs exactly this test.
