# 大厂 Jev 类模型横评报告

> 截至 **2026-11-03**。Jev 发布后七周内，OpenAI、微软、阿里云、火山引擎、Cloudflare、AWS、Perplexity、Snowflake、上海 AI Lab 都推出了同类「决策模型」。这份报告把它们放在一起比：怎么接、多少钱、有什么限制、谁的数字是自己说的、谁的数字是别人量的。
> 回到 [主列表](../README.md#-大厂同类模型)

**读之前先记住三条：**

1. 下面所有「准确率 / 速度 / 榜单第一」**几乎都是厂商自评**，每条都标了出处。独立第三方数据目前很少，单独列在 [第四节](#四评测数据谁量的量了什么)。
2. 价格、限额、状态变化很快，本文每个数字都附了官方文档链接，**以官方页面为准**。
3. 我们自己的实测（[第五节](#五我们的测评)）本轮只覆盖了火山方舟，其余厂商没有实测，不写估算值。

---

## 目录

- [一、一张表看全](#一一张表看全)
- [二、两条技术路线：专用小模型 vs 收窄的大模型](#二两条技术路线专用小模型-vs-收窄的大模型)
- [三、逐家说明](#三逐家说明)
- [四、评测数据：谁量的、量了什么](#四评测数据谁量的量了什么)
- [五、我们的测评](#五我们的测评)
- [六、怎么选](#六怎么选)
- [七、迁移：协议到底兼容到什么程度](#七迁移协议到底兼容到什么程度)
- [来源](#来源)

---

## 一、一张表看全

### 托管 API

| 厂商 | 模型 ID | 发布 | 状态 | 端点 | 输入价 / MTok | 输出 | 关键限制 | 输入模态 |
| :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- |
| **TypeSafe** | `jev-1.14.0`（`jev-latest`）· `jev-1.13.0` | 09-15 / 1.14 于 10-14 | GA | `api.typesafe.ai/v1/systemone` | **$0.042** | 免费 | 64k（危险区开关可到 262k）· Choice ≤255 | 文本；图像与 Box 需开危险区请求头 |
| **OpenAI** | `gpt-6-luna` | 09-29 预览 · 10-06 公测 · 10-22 GA | **GA** | `api.openai.com/v1/decisions` | **$0.10** | 免费 | 每请求 ≤400 题 · Score 2–10 档 | 文本、图像、JSON、对话历史 |
| **阿里云百炼** | `decision-model-preview` | 09-25 | 预览 | `{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/systemone`（另有新加坡） | **限时免费** | 免费 | 64k · ≤16 题 · Choice ≤255 · Score 2–255 · 新加坡 RPM 1,200 | 文本 |
| **火山方舟** | `doubao-seed-2-1-lite-260915` | 文档未写日期 | **beta** | `ark.cn-beijing.volces.com/api/v1/systemone`，须带 `ark-beta-systemone-api: true` | 按该模型输入价（模型页 ¥0.8） | 免费 | 128k · Choice ≤255 · Score ≤10 档 · RPM 30,000 · 不支持流式 | **文本、图像、视频、音频** |
| **微软** | `microsoft-decision-1` | 10-09 | GA（Foundry） | Foundry `/providers/microsoft/v1/systemone`；OpenRouter | **$0.042** | 免费 | 基于 Qwen3.5-9B 后训练 | 文本 |
| **Perplexity** | `pplx-decider-v1.2` · `pplx-decider-flash-v1.2` | v1 10-01 · v1.2 约 10-16 | GA | `api.perplexity.ai/v1/decisions` | **$0.02** · flash **$0.01** | 免费 | 256k · ≤128 题 · Choice ≤255 · 10 req/s | 文本、图像 |
| **Cloudflare** | `@cf/cloudflare/clef` · `clef-flash` · `clef-omni` | 10-01 · omni 10-09 | GA（Workers AI） | Workers AI，Jev API 兼容 | Clef **$0.24** · flash 见注 | 免费 | 64k · ≤64 题 · ≤4 图 | 文本、图像；omni 加音视频 |
| **Snowflake** | `snowflake-decision` | 10-07 | 私有预览 | SQL `AI_COMPLETE('snowflake-decision', …)` | 按 Credits | — | ≤32 题 · Choice 2–32 · 全请求 ≤256 选项 | 文本、表数据 |

> 注：Clef-flash 的价格有两个说法——第三方定价拆解写 $0.09，awesome-system-one 清单写 $0.038，**以 Workers AI 官方价格页为准**。火山 System One 文档写的是「按所选模型的输入 token 计费，输出免费」，¥0.8/MTok 取自该模型的模型详情页。

### 开放权重（可自建）

| 出品方 | 模型 | 发布 | 许可 | 规格 | 一句话 |
| :-- | :-- | :-- | :-- | :-- | :-- |
| **上海 AI Lab** | 书生·明决 Intern-Decision 0.8B / 2B / 4B | 09-28 | Apache-2.0 | 基于 Qwen3.5，冻结视觉编码器 | 国内第一个开源多模态决策模型，有 arXiv 论文；4B 在 4090 上 3 题 44ms（自测） |
| **AWS** | Strands Decider 2B | 10-01 | Apache-2.0（含数据与训练脚本） | Qwen3.5-2B + pointer head + LoRA | **只有本地版**，Bedrock 上没有托管；`strands-decider serve` 起 `/v1/systemone` |
| **Cloudflare** | Clef 27B / Clef-flash 9B | 10-01 | Apache-2.0 | — | 托管和权重同时给，是大厂里唯一两头都有的 |
| **Perplexity** | Decider v1.2 27B / flash 4B | 约 10-15 | 称 Apache-2.0 | Qwen3.8-27B / Qwen3.5-4B | HF 仓库标注需授权 token，实际可得性先确认 |
| **Liquid AI** | d1-3B · d1-omni-600M | 10-07 | 开放 | 端侧 | omni 版吃文本、图像、音频 |

### 没发现官方产品的厂商（截至 11-03）

**Google、Anthropic、百度千帆、腾讯混元、智谱、DeepSeek、Kimi、MiniMax、阶跃星辰、商汤、讯飞**——全网检索没有找到官方的决策模型或 `/v1/systemone` 端点。社区有用 GLM、Qwen 包装 `/v1/systemone` 的做法，那是第三方项目，不算厂商产品。Google 侧最接近的是 Gemini API 的 logprobs + JSON Schema，属于老办法。

---

## 二、两条技术路线：专用小模型 vs 收窄的大模型

把上面这些拆开看，其实是两种做法，选型时比价格更该先弄清楚：

| | **专用决策模型** | **把通用大模型收窄成决策接口** |
| :-- | :-- | :-- |
| 代表 | Jev、Clef、Perplexity Decider、Microsoft-Decision-1、Strands Decider、书生·明决 | **OpenAI**（GPT-6 Luna）、**火山**（Seed-2.1-lite） |
| 做法 | 骨干 + 在选项上打分的读出头，一次前向答完，模型里没有自由生成这一步 | 同一个能写字的模型，在接口层把输出限制到你给的选项上 |
| 好处 | 便宜、快、延迟稳定；概率来自专门训练的打分头 | **多模态和长上下文白送**：OpenAI 吃图像和对话历史，火山连视频音频都能直接当 state |
| 代价 | 多模态和长上下文都是后补的（Jev 1.14 的图像还在危险区） | 单价高一截（OpenAI $0.10 vs Jev $0.042）；概率是否经过校准训练，两家都没公开说明 |

OpenAI 的 API 负责人说得很直接：他们**没有训练新模型**，是把 Luna 重新配置成更快更便宜的推理方式，延迟从 1–3 秒降到约 100–180ms（OpenAI 自述）。火山的文档也把它放在 `doubao-seed-2-1-lite` 这个通用模型的「决策评估能力（beta）」下面。

这件事对使用者的意义：**「它不可能输出 schema 外的东西」这一条两条路线都成立；但「它说 70% 就真有 70%」这一条，收窄路线没有任何厂商给出校准数据。** 门控阈值必须在自己的数据上重新量。

---

## 三、逐家说明

### OpenAI Decisions API

- **时间线**：09-29 DevDay 宣布有限预览 → 10-06 公测 → 10-22 GA（GA 日期来自第三方报道；官方文档页本身写着「now generally available」）。
- **协议不是 `/v1/systemone`**。题型叫 `predicate` / `choice` / `score`；选项写成 `choices: [{value, description}]`，量表写成 `levels: [{label, description}]`；返回的 `answers` 是**数组**（每项带 `name`），不是按题名索引的对象；还多了一种 `refusal` 答案。迁移要改代码，见 [第七节](#七迁移协议到底兼容到什么程度)。
- **限制**：每请求 1–400 题（公测时 200）；Score 2–10 档；choices 上限和上下文长度文档未写。
- **它独有的**：输入可以是整段对话历史（含 function call 与工具输出）、图像（base64 或 URL）、`input_json`；有 prompt caching（≥1,024 token 前缀）；US / EU 数据驻留、ZDR、HIPAA。
- **价格**：未缓存输入 $0.10 / MTok，输出不计费；区域处理与长上下文有加价。
- OpenRouter 上也能调：`openai/gpt-6-luna-decisions`。

### 阿里云百炼 · decision-model-preview

- 09-25 上线预览版，**限时免费**，Token Plan（个人版）调用也不消耗 Credits。
- **协议直接用 TypeSafe System One**：官方 Python SDK `typesafe-sdk` 把 `base_url` 换成业务空间域名、换成 DashScope key 就能用。路径多一个 `/compatible-mode` 前缀，由 base_url 吸收。
- 限制：64k 上下文；**单请求最多 16 题**（比 Jev 少得多），且官方写明延迟随题数「近线性」增长——这和 Jev「加题不加延迟」的卖点不一样，需要实测；Choice ≤255；Score 2–255 档（建议 3–7）。
- 返回里带服务端 `latency_ms`，方便量延迟。
- DashScope SDK 需要 Python ≥2.0.1 / Java ≥2.23.3。
- 区域：北京、新加坡。**数据要留在境内的，这是目前最省事的一条路**。

### 火山方舟 · System One API（beta）

- 端点 `POST https://ark.cn-beijing.volces.com/api/v1/systemone`，**必须带请求头 `ark-beta-systemone-api: true`**，鉴权用方舟 API Key。
- 目前只支持 `doubao-seed-2-1-lite-260915`。这是一个通用的豆包 Seed 模型，不是专门训练的决策模型。
- 请求体与 `/v1/systemone` 同形：`state` + `questions{type, instructions, criteria}`，题型 `noul` / `choice` / `score`。**`state` 可以是图像、视频、音频的多模态数组**——这是国内外所有托管产品里输入模态最全的。
- 限制：128k 上下文（state 和 questions 共用，比模型本身 1M 小得多）；Choice 1–255；Score 1–10 档；不支持流式；RPM 30,000、TPM 500 万。
- 计费：按所选模型输入 token 计费，**文本、图像、音频、视频统一单价**，输出免费。
- 请求 ID 在响应头 `X-Request-Id` 里，不在 body。

### 微软 · Microsoft-Decision-1

- 10-09 发布，Microsoft Foundry 与 OpenRouter 可用；Qwen3.5-9B 后训练。
- 价格与 Jev **一分不差**：$0.042 / MTok，输出免费。
- 微软说之后会换到 MAI 和 OpenAI 的模型做底座。
- 自评：36 个基准、约 15 万题里准确率最高；P50 比 GPT-6 Sol 快约 35 倍；扰动输入平均 1.3% 会改判，换选项措辞、打乱选项顺序 0 改判。

### Perplexity · Decider

- 节奏最快的一家：v1 10-01、v1.1 约一周后、v1.2 约 10-16，旧 ID 自动转到 v1.2。
- **最便宜的托管选项**：v1.2 $0.02、flash $0.01 / MTok。
- 端点叫 `/v1/decisions`，但请求体就是 `/v1/systemone` 的形状（`state` + `questions` 对象、`criteria`），改 URL 和 model 基本就能切。
- 256k 上下文；每请求 ≤128 题；图像只收 data URL，每题 ≤8 张；组织级 10 req/s。
- 自评 Decision Index：v1.2 68.09、v1.1 62.30、flash 58.88。

### Cloudflare · Clef 家族

- 10-01 发布 Clef（27B）与 Clef-flash（9B），10-09 发布 Clef-omni（吃音视频）。Workers AI 托管 + Hugging Face Apache-2.0 权重。
- 官方说完全兼容 Jev API：换端点、加 `model` 字段即可。Workers AI 也直接托管了 Jev 本体（`typesafe/jev`）。
- 每请求 ≤64 题、≤4 张图，64k 上下文；Workers AI 每天 1 万 neurons 免费额度。
- 第三方对比：意图识别与工具调用上胜 Jev，When2Call 上落后。

### AWS · Strands Decider 2B

- **不是 Bedrock 托管模型**，是 Strands Labs 的开源项目：权重、代码、训练数据、配方全部 Apache-2.0。
- 结构：Qwen3.5-2B 去掉 LM head，换成约百万参数的 pointer head 给选项打分，再加 rank-16 LoRA。
- `strands-decider serve` 在 127.0.0.1 起 `/v1/systemone`，**无鉴权**，别直接暴露公网；社区报告 0.1.0 版并发时可能返回错误答案却给 HTTP 200（上游 issue #17）。
- 自测：RTX 3090 中位约 115ms。AWS Builder 上一篇文章实测它在三组任务上 72% / 55% / 95%，同场 Bedrock 上的 Claude Haiku 4.5 是 93% / 75% / 97%，作者建议「Decider 先判、Haiku 兜底」。

### Snowflake · Snowflake Decision

- 10-07 私有预览，只有受邀账号可用。**唯一一个以 SQL 函数形式交付的**：`AI_COMPLETE('snowflake-decision', …)`，一条 SQL 就能对整张表逐行做判断。
- 题型同样是 choice / score / 是非；单请求 ≤32 题、Choice 2–32 项、全请求 ≤256 个选项、≤256 KiB。
- 自评：在 Jev Decision Index 0.2.1 的 29 个基准上得 57.63，72 个模型中第一。

### 上海 AI Lab · 书生·明决（Intern-Decision）

- 09-28 开源 0.8B / 2B / 4B，Apache-2.0，基于 Qwen3.5，冻结视觉编码器，**原生吃图像**。有论文（arXiv 2610.22131），沐曦 Day 0 适配。
- 方法和别家不同：在完整的 JSON 骨架里给每个字段放一个决策占位符，用骨干原生的 LM head 一次前向读出所有字段。
- 自评：7 套评测平均 4B 90.02 / Jev 1.13 88.74；4090 上 289 token、3 字段 44ms；温度缩放后 ECE 从 0.213 降到 0.089。
- CSDN 上有人指出：模型卡里的校准温度随模型变大而变小，意味着**小模型更过度自信**——用 0.8B 做门控要格外小心。

### 其他托管玩家（非大厂，简列）

Liquid AI d1 / d1-ultra、Inception Mercury Decide（OpenRouter 有免费路由）、Nace.AI Drex、Upstage Solar Decide（beta）、Fastino GLiDE、Parallel Decisions（带联网检索）、Bespoke Nimble-v4-max、Together Tev1（实验版）。完整清单见 [awesome-system-one](https://github.com/andyrewlee/awesome-system-one)。

---

## 四、评测数据：谁量的、量了什么

### 厂商自评（只能当宣传口径看）

| 厂商 | 说法 | 可核对程度 |
| :-- | :-- | :-- |
| OpenAI | 约 150ms，对比 Responses API 1.6s，「快 10 倍」 | 无公开测试条件 |
| 微软 | 36 基准约 15 万题准确率第一；比 GPT-6 Sol 快约 35 倍 | 未给出 Jev 的具体分数 |
| Snowflake | Jev Decision Index 0.2.1 上 57.63，72 个模型第一 | 基准公开，可复跑 |
| Perplexity | Decision Index 68.09（v1.2） | 同上 |
| 上海 AI Lab | 7 套平均 90.02，胜 Jev 88.74 | 有论文与权重，可复跑 |
| AWS | JevBench 公开集上约 2B 级别第二 | 有权重与脚本 |

注意几家各自说的「Decision Index」**版本和题集不一定相同**，分数之间不能直接横比。

### 独立来源

- **[Artificial Analysis Decision Index](https://artificialanalysis.ai/evaluations/artificial-analysis-decision-index)**：目前最中立的综合榜。四项各占 25%：AA-Omniscience-Decision（准确率 + 不幻觉率）、HLE 多选、When2Call 工具调用、WildGuardTest 安全分类；决策模型只按输入 token 计成本。榜上已有 GPT-6 Luna (Decisions)、Microsoft-Decision-1、Decider v1.2、Clef、d1-ultra、Jev 1.14 等。页面是动态渲染，具体分数请直接看原页。
- **[OpenRouter Decisions 用量榜](https://openrouter.ai/rankings/decisions)**（真实调用量，11 月初）：Jev 1.13 约 10.7 亿次、Jev 1.14 4.75 亿次、Decider v1.2 1.65 亿次、Mercury Decide 6,160 万次、**GPT-6 Luna Decisions 4,460 万次（环比 −12%）**、Drex v1.5、Clef Flash、d1-ultra 依次在后。用量不等于质量，但能看出开发者实际选了谁：**Jev 仍然占绝对多数，OpenAI 的入场没有把它挤下去。**
- **AWS Builder 实测**：Strands Decider 2B 72% / 55% / 95%，Claude Haiku 4.5 93% / 75% / 97%。小模型便宜快，但准确率差距是实打实的。
- 本列表 [独立评测](../README.md#独立评测) 一节收录的 jevbench、phishing-bench、judgekit 等仍然主要只测 Jev 本体和开源复现，**专门横比大厂托管 API 的中文评测，目前全网没有找到**——这正是下一节要补的。

---

## 五、我们的测评

### 已有数据（Jev 本体，2026-09-19）

本列表此前在 Vercel AI Gateway 上实测过 Jev 1.13（详见 [README 中文场景小实测](../README.md#中文场景小实测)）：15 条中文工单，路由与紧急度各 14/15；延迟中位 370ms、p95 448ms；批量发比逐条发更准；中文上 confidence 偏饱和。

### 统一横评脚本（新增）

为了把各家放在**同一份中文数据、同一组问题**上比，仓库新增了：

- [`bench/zh_tickets.jsonl`](../bench/zh_tickets.jsonl)：40 条中文客服工单，部门四分类（billing / technical / sales / account，各 10 条）+ 是否紧急（10 条紧急）。标签由维护者一人标注，含若干刻意模糊的样本（如「优惠券无效」），**样本量只够看方向，不够下定论**。
- [`bench/vendor_bench.py`](../bench/vendor_bench.py)：纯标准库，一条工单一次请求同时问两题（Choice 路由 + 是非紧急），统计路由准确率、紧急度准确率、平均置信度、ECE（5 桶）、p50 / p95 延迟、每千次成本。覆盖：

| Provider | 协议 | 环境变量 |
| :-- | :-- | :-- |
| TypeSafe 官方 | `/v1/systemone` | `TYPESAFE_API_KEY` |
| OpenAI | `/v1/decisions`（自有 schema） | `OPENAI_API_KEY` |
| 阿里云百炼 | `/compatible-mode/v1/systemone` | `BAILIAN_BASE_URL` + `DASHSCOPE_API_KEY` |
| 火山方舟 | `/api/v1/systemone` + beta 头 | `ARK_API_KEY` |
| Perplexity | `/v1/decisions` | `PERPLEXITY_API_KEY` |
| OpenRouter（一个 key 覆盖 Jev 1.13/1.14、GPT-6 Luna、Microsoft-Decision-1、Decider、Clef Flash、Mercury Decide、d1-ultra、Drex） | `/api/alpha/decisions` | `OPENROUTER_API_KEY` |
| 任意本地 `/v1/systemone`（kev、laya/EdgeJev、Strands Decider、Clef 自托管…） | `/v1/systemone` | `LOCAL_SYSTEMONE_URL` |

```bash
python bench/vendor_bench.py --list     # 看哪些已配置
python bench/vendor_bench.py            # 跑全部已配置的，结果写到 bench/results/
```

### 横评结果

第一轮（2026-11-04 UTC，北京区域，逐条串行请求）跑了**火山方舟**；原始输出见 [`bench/results/2026-11-04.json`](../bench/results/2026-11-04.json)。

| Provider | 模型 | n | 路由准确率 | 紧急度准确率 | 平均置信度 | ECE | p50 | p95 | 每千次成本（估） |
| :-- | :-- | --: | --: | --: | --: | --: | --: | --: | --: |
| 火山方舟 System One API（beta） | `doubao-seed-2-1-lite-260915` | 40 | **97.5%**（39/40） | 90.0%（36/40） | 0.97 | 0.025 | 759 ms | 1,837 ms | ¥0.35 |

> 每千次成本 = 平均输入 441 token × 模型页输入价 ¥0.8/MTok，是按价格表估算，不是账单回读。同样 441 token 按 Jev 的 $0.042 计约 $0.019 / 千次。

**看到的几点：**

- **路由几乎全对，而且唯一的错能被置信度拦住。** 错的那条是「支付页面在安卓上白屏，用户付不了款」，标注 technical、模型选了 billing——置信度只有 **0.507**，而其余 39 条最低也有 0.838。阈值设在 0.6–0.8 之间就能把它转人工，且不误伤任何一条正确答案。这条本身就跨两类，人来判也会犹豫。
- **紧急度的 4 个「错」都是同一种：把涉及钱的投诉判成紧急**（重复扣费、扣款未到账、多收增值费、退款少 30 元，概率 0.77–0.99）。问题描述里写了「资金损失」算紧急，所以严格说这是**我们的判据写得不够清楚**，不全是模型的错。这正好说明 [问题要原子](./concepts.md#五为什么问题要原子)：「有没有资金损失」和「是否需要今天处理」应该拆成两题。
- **置信度在中文上同样偏饱和**：40 条里 29 条 ≥0.99。ECE 0.025 看着很好，但样本大多挤在最高一桶，这个数字主要说明「它很自信，而且这次基本自信对了」。
- **延迟是收窄路线的代价**：p50 759ms、最慢 2.9s，比 Jev 官方的 70–500ms 和此前我们实测 Jev 的中位 370ms 都慢一截。这是 beta 接口的单次串行测量，没有攒批、没有并发，只代表这一次的情况。

**其他厂商本轮未测**，报告里关于它们的数字全部来自官方文档或第三方，已逐条标注出处。脚本已支持这些厂商，有 key 的读者可以自己跑一遍对照。

> 40 条、一人标注、单次运行——这是方向性数据，不是结论。

---

## 六、怎么选

| 你的情况 | 先试 | 理由 |
| :-- | :-- | :-- |
| 默认首选、要最成熟的生态 | **Jev** | 用量最大、文档与能力毛边公开最全、SDK 和集成最多 |
| 只看价格 | **Perplexity Decider flash / v1.2** | $0.01–0.02，Jev 的一半以下；先量准确率 |
| 已经全在 OpenAI 上、要吃图像或整段对话历史 | **OpenAI Decisions** | 同一个 key、ZDR / HIPAA / 区域驻留；贵 2.4 倍，协议要改 |
| 数据必须留在中国境内 | **阿里云百炼**（免费预览）或**火山方舟** | 北京区域；百炼兼容官方 SDK，火山多模态最全 |
| state 是视频、音频 | **火山方舟** / Clef-omni | 托管产品里只有这两家吃音视频 |
| 已在 Azure / Foundry | **Microsoft-Decision-1** | 价格与 Jev 相同，合规走企业协议 |
| 判断要跑在数据仓库里 | **Snowflake Decision** | 一条 SQL 跑整表，数据不出仓（私有预览） |
| 必须离线、要改权重 | **书生·明决** / **Strands Decider** / **Clef 权重** | 都是 Apache-2.0；明决和 Clef 带视觉 |
| 预览、beta 产品能不能上生产 | 先别 | 百炼、火山都还是预览 / beta，接口可能变；做好回退 |

---

## 七、迁移：协议到底兼容到什么程度

一句话：**题型大家对齐了，合同没对齐。**（[API Evangelist 的说法](https://apievangelist.com/2026/10/12/decision-models-agreed-on-the-questions-not-the-contract/)）

| | 路径 | 题型命名 | 选项写法 | 返回 answers | 能直接用 `typesafe-sdk` |
| :-- | :-- | :-- | :-- | :-- | :-- |
| TypeSafe | `/v1/systemone` | noul / choice / score | `criteria` 对象 / 数组 | 按题名的对象 | 是 |
| 阿里云百炼 | `/compatible-mode/v1/systemone` | 同上 | 同上 | 同上 | **是**（官方文档写明） |
| 火山方舟 | `/api/v1/systemone` | 同上 | 同上 | 同上 | 要额外加 beta 请求头 |
| 微软 Foundry | `/providers/microsoft/v1/systemone` | 同上 | 同上 | 同上 | 有兼容客户端 |
| Cloudflare Clef | Workers AI | 同上，必填 `model` | 同上 | 同上 | 换端点 + 加 model |
| Perplexity | `/v1/decisions` | 同上 | 同上 | 同上 | 改 URL |
| OpenRouter | `/api/alpha/decisions` | 同上，另有 box | 同上 | 同上 | 改 URL；可用 `provider` 指定路由 |
| Vercel AI Gateway | `/v1/evaluate` | **boolean** / choice / score | 同上 | 字段名 `probability` | 否 |
| **OpenAI** | `/v1/decisions` | **predicate** / choice / score | **`choices[{value, description}]`、`levels[{label, description}]`** | **数组**，每项带 `name`；有 refusal | **否** |
| Snowflake | SQL `AI_COMPLETE` | choice / score / 是非 | — | — | 否 |

实用建议：业务代码里自己定义一层「决策接口」，把 provider 差异关在适配层里——[`bench/vendor_bench.py`](../bench/vendor_bench.py) 的 `systemone_body` / `openai_body` 两个函数就是最小示例。官方的 [system-one-adapter](https://github.com/typesafe-ai/system-one-adapter-python) 也能当降级后端。

---

## 来源

官方文档：
[OpenAI Decisions 指南](https://developers.openai.com/api/docs/guides/decisions) ·
[OpenAI DevDay 2026 回顾](https://openai.com/index/devday-2026-recap/) ·
[阿里云百炼 决策模型 API](https://www.alibabacloud.com/help/zh/model-studio/decision-model-api) ·
[百炼 决策模型概览](https://help.aliyun.com/zh/model-studio/decision-model/) ·
[百炼 模型价格](https://help.aliyun.com/zh/model-studio/model-pricing) ·
[火山方舟 System One API（beta）](https://ark.volcengine.com/region:cn-beijing/docs/system-one-api) ·
[火山方舟 决策评估教程](https://ark.volcengine.com/region:cn-beijing/docs/decision-model) ·
[火山方舟 模型列表](https://docs.volcengine.com/docs/82379/1593703) ·
[Microsoft-Decision-1 发布](https://commandline.microsoft.com/microsoft-decision-1-model-foundry/) ·
[Perplexity Decisions 快速开始](https://docs.perplexity.ai/docs/decisions/quickstart) ·
[Perplexity 价格](https://docs.perplexity.ai/docs/getting-started/pricing) ·
[Snowflake Decision 博文](https://www.snowflake.com/en/blog/snowflake-decision-cortex-ai-functions/) ·
[Snowflake 2026-10-07 发布说明](https://docs.snowflake.com/en/release-notes/2026/other/2026-10-07-ai-complete-snowflake-decision-preview) ·
[strands-labs/strands-decider](https://github.com/strands-labs/strands-decider) ·
[InternLM/Intern-Decision](https://github.com/InternLM/Intern-Decision) ·
[Intern-Decision 论文](https://arxiv.org/html/2610.22131v1) ·
[OpenRouter Decisions API](https://openrouter.ai/docs/api/api-reference/alphadecisions/submit-a-decisions-questions-and-answers-request) ·
[OpenRouter Jev 1.14](https://openrouter.ai/typesafe/jev-1.14)

报道与第三方：
[TechCrunch：OpenAI 的 Jev 克隆](https://techcrunch.com/2026/09/30/openais-jev-clone-could-help-the-frontier-lab-stop-its-swarming-agents/) ·
[Firecrawl：OpenAI Decisions vs Jev](https://www.firecrawl.dev/blog/openai-decisions-api-vs-jev) ·
[AI Polix：OpenAI Decisions GA](https://aipolix.com/en-us/news/openai-decisions-api-generally-available-gpt-6-luna) ·
[Kai Waehner：决策模型如何成为新品类](https://www.kai-waehner.de/blog/2026/10/20/how-decision-models-became-a-new-ai-category-after-jev/) ·
[MarkTechPost：Jev 1.14](https://www.marktechpost.com/2026/10/14/typesafe-ai-jev-1-14-images-box-long-context/) ·
[The New Stack：AWS Strands Decider](https://thenewstack.io/aws-strands-decider-model/) ·
[AWS Builder：Decider 在 AgentCore 上](https://builder.aws.com/content/3KJvK45IGyUNQwRd4dSOZQWKv8I/running-strands-decider-2b-on-amazon-bedrock-agentcore-microvms-vs-gpu-instances) ·
[eesel：Clef 价格](https://www.eesel.ai/blog/cloudflare-clef-pricing) ·
[53AI：百炼决策模型预览版上线](https://www.53ai.com/news/LargeLanguageModel/2026092534620.html) ·
[Pandaily：Intern-Decision](https://pandaily.com/shanghai-ai-lab-intern-decision-open-source-0-8b-2b-4b-decision-model) ·
[OpenRouter Decisions 用量榜](https://openrouter.ai/rankings/decisions) ·
[Artificial Analysis Decision Index](https://artificialanalysis.ai/evaluations/artificial-analysis-decision-index) ·
[andyrewlee/awesome-system-one](https://github.com/andyrewlee/awesome-system-one)
