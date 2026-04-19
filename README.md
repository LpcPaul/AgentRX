# AgentRX

> Recovery memory layer for AI tool failures.
> When your agent's third-party tool path fails, AgentRX surfaces what worked (and what didn't) from prior experience.

## What is AgentRX?

AgentRX is a **recovery experience library** for AI agents. It answers one question:

> **The agent's tool failed — what did someone else try that worked?**

It focuses on:
- **Third-party tool failures** — playwright, browser-cdp, web-fetch, MCP connectors, etc.
- **Environment long-tail issues** — proxy, headless, sandbox, permissions, dependencies
- **What worked / what didn't** — concrete, actionable recovery guidance

AgentRX does **not** compete with platform-level recovery (retry, circuit breaker, fallback routing). Those are the platform's job. AgentRX handles what platforms can't cover: real-world tool-specific experience.

## How it works

```
1. Agent's third-party tool fails
2. Agent tries to recover on its own — fails 2+ times
3. Agent activates AgentRX skill
4. Agent describes the failure in natural language
5. Agent finds the matching tool file in cases/
6. Agent reads the closest case, focuses on what_worked and what_didnt_work
7. Agent applies the learned recovery
8. Agent appends the outcome to ledger.jsonl
```

## Why we are shrinking from v2.1 to MVP

The v2.1 architecture (schema validation, route registry, deterministic retrieval) was a well-intentioned infrastructure investment — but it put cart before horse. Before building a retrieval engine, we need to verify: **does case content actually help agents recover?**

This MVP tests that question with minimal infrastructure. If the answer is "yes", we'll grow back the heavy architecture on a proven foundation. If "no", we saved months of wasted engineering.

## MVP does

- A very short SKILL.md that tells the agent when and how to use AgentRX
- Flat `cases/` directory — one JSON file per tool, containing case arrays
- `ledger.jsonl` for append-only experience logging
- Minimal case format: symptom, what_worked, what_didnt_work, times_confirmed

## MVP does not do (yet)

- v2.1 JSON schema validation
- Route registry / route recommendation
- Deterministic retrieval scripts
- Build index / validate / generate scripts as main path
- Automated hooks triggering
- Complex directory分层 (by_tool, by_tag, verified, curated, archived)
- Synthetic seed cases

## Files

| File | Role |
|---|---|
| [SKILL.md](SKILL.md) | Ultra-short runtime protocol the agent reads when activated |
| [cases/](cases/) | Flat case directory — one JSON file per tool |
| [ledger.jsonl](ledger.jsonl) | Append-only experience log |
| [CONTRIBUTING.md](CONTRIBUTING.md) | How to contribute real recovery cases |
| [docs/MVP.md](docs/MVP.md) | Why we shrank, what we validate, future expansion order |
| [docs/legacy/](docs/legacy/) | v1→v2.1 architecture exploration (historical reference only) |

## License

MIT
