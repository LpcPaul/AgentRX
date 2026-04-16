# AgentRX

> 🩺 AI 工具链的急诊科医生
> *A prescription for your AI agent when its tools fail.*
> 覆盖 skill、MCP server、插件、内置工具、agent、workflow、hook。**任务优先，不是工具优先。**

## 你是不是也遇到过这些情况：

> 你装了各种工具——skill、MCP server、插件——但每次出问题时，AI 总要在工具之间来回试错、切换、重试。时间浪费了，token 也烧完了。

> 你装了三个做 PPT 的工具，每个都说自己能做。但哪个更好？哪个更适合当前这份演示？每次 AI 和你都陷入迷茫。

> 工具调用失败了，AI 反过来问你"该怎么办"。可你装工具就是为了不用操心这些——你也不知道怎么办。

**AgentRX 就是来解决这个问题的。**

它本身也是一个 agent skill。装上之后，它不在你的终端里等你敲命令——它在 AI 背后默默工作：当工具选错了、冲突了、或者失败了，它负责搞清楚这次是谁的问题、应该怎么修，然后把答案给 AI。

## A concrete example

```
User: Extract the product list from this page.

AI: [tries browser-cdp skill]
    The page uses JavaScript to render content. browser-cdp only
    returned the initial HTML shell. Data missing.

[AgentRX activates]

AgentRX: You hit a `capability_mismatch` at the execute-task stage.

         Two alternatives exist in your current environment:

         1. web-access skill  — handles post-render DOM, best for this task
         2. Playwright MCP    — better if you also need interaction
                                (clicks, scrolls, form fills)

         Prescription: switch to web-access.
         Confidence: high. Based on 8 similar cases in cases/web-browsing/.
```

This is what AgentRX does: turns a stuck state into a structured next-step decision.

---

## Human installs. AI operates.

**AgentRX is installed by humans, but operated by AI.**

Once installed, the human is not the primary user. The primary user is the AI agent itself:
- it **diagnoses** stuck states
- it **searches** the case library
- it **chooses** a better route
- it **contributes** new cases back

You don't run AgentRX. Your AI does.

### Human role vs AI role

| | What they do |
|---|---|
| **Human** | Install the skill. Expose the repository / index / rules. Optionally review schema or approve maintenance changes. |
| **AI** | Detect stuck state. Structure evidence. Derive inference. Retrieve similar cases. Choose next action. Optionally contribute a new case. |

**The human is the installer and host. The AI is the default operator.**

### The AI self-evolution loop

AgentRX is not a static knowledge base. It is an **AI self-evolution infrastructure**:

```
1. AI gets stuck
2. AI structures the stuck state (evidence + inference)
3. AI retrieves similar cases from the library
4. AI switches to a better route
5. AI records the outcome
6. The new case becomes available for future AI agents
```

Each case contributed by an AI agent makes the next agent smarter. The library grows not through human curation, but through accumulated AI experience.

---

## What this project is

AgentRX diagnoses AI tool-chain failures and prescribes the next best action.
It covers **skills, MCP servers, plugins, built-in tools, agents, workflows, and hooks**.

It is a **stuck-state navigation system** — the first responder when any part of your AI agent's tool path breaks down.

## Why this project changed

The old project (Skill Doctor) was designed around the question:

- "Which tool failed?"
- "Which failure type does this belong to?"

That worked only when the agent already knew **which tool** was involved.

But real failures usually begin from a messier place:

- "I'm trying to browse a page and the content is incomplete."
- "I generated a document, but the output is wrong."
- "I can do this task with a skill, an MCP, a plugin, or a built-in tool — which one should I switch to?"
- "I am not sure whether this is a routing problem, a config problem, an environment problem, or simply the wrong tool for the job."

So the project has been redesigned around a different principle:

> **Start from the task, then locate the stage, then classify the problem family, then choose the next action.**

This repository is no longer only about "skill governance."
It is about **AI tool-path diagnosis and next-step recommendation**.

## What it covers

This project covers failures and decision paths involving:

| Tool type | Examples |
|---|---|
| **skill** | xlsx, pdf, frontend-design, tavily |
| **mcp** | Playwright MCP, Google Search MCP, Filesystem MCP |
| **plugin** | Browser extensions, IDE plugins |
| **builtin** | Claude's built-in web search, file reader |
| **agent** | Multi-agent orchestration frameworks |
| **workflow / hook** | Pre-commit hooks, deterministic pipelines |

This is **not** a universal benchmark site for all AI tools.
It only enters the picture when an AI tool-path did **not** meet expectations and the agent needs help deciding what to do next.

## Core positioning

AgentRX does four things:

1. **Intake** — force the agent to describe its own blockage in a structured way.
2. **Navigate** — route the problem through a task-first knowledge architecture.
3. **Recommend** — propose the most suitable next action, not just a label.
4. **Evolve** — turn recovery paths into reusable cases that make future AI agents smarter.

## Why this is not a generic human-facing tool directory

Some projects catalog every AI tool and let humans browse them. AgentRX does not do that.

It answers one question: **the agent is stuck — what should it do next?**

The case library is machine-consumable by design. Humans can read it, but that is secondary. The primary purpose is AI-to-AI knowledge transfer: one AI agent's stuck experience becomes another agent's shortcut.

---

## Install

### Claude Code

```bash
git clone https://github.com/LpcPaul/AgentRX.git ~/.claude/skills/agentrx
```

### OpenClaw / ClawHub

```bash
git clone https://github.com/LpcPaul/AgentRX.git ~/.openclaw/skills/agentrx
```

### Codex / Cursor / other skill-compatible runtimes

```bash
git clone https://github.com/LpcPaul/AgentRX.git ~/.codex/skills/agentrx
```

---

## What changed from the old version

### Old model (v1 — Skill Doctor)
- centered on `skill_triggered`
- organized cases by `by-skill/` and `by-type/`
- retrieved mostly by `skill_triggered + failure_type`
- treated many failures as "skill failures"

### New model (v2.1 — AgentRX)
- centered on `task + journey_stage + problem_family`
- **evidence / inference split** — facts vs. interpretation
- **standardized route ids** — action paths, not tool brands
- recommends the **next action** rather than only classifying the cause
- cases are **AI-contributed**, AI-consumed

---

## Read this next

| Document | Role |
|---|---|
| [SKILL.md](SKILL.md) | The runtime prompt that the AI agent reads when activated |
| [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) | System design — why AI-only, why evidence/inference, why route ids |
| [docs/INTAKE_CARD.md](docs/INTAKE_CARD.md) | The structured format AI uses to translate stuck states into queries |
| [CONTRIBUTING.md](CONTRIBUTING.md) | How cases enter the system — default contributor is AI |
| [cases/README.md](cases/README.md) | Case library structure and indexing |

## License

MIT
