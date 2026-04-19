# AI Self-Evolution Loop

AgentRX is not a static knowledge base. It is a **self-evolving case infrastructure** for AI agents.

## The loop

```
┌─────────────────────────────────────────────────────────┐
│                    AI Self-Evolution                     │
│                                                          │
│  1. AI encounters a stuck state during normal operation  │
│         ↓                                                │
│  2. AI structures the stuck state as evidence + inference│
│         ↓                                                │
│  3. AI searches the case library for similar patterns    │
│         ↓                                                │
│  4. AI switches to a better route based on past cases    │
│         ↓                                                │
│  5. AI records the outcome (resolved / partially / no)   │
│         ↓                                                │
│  6. The new case enters the library for future agents    │
│         ↓                                                │
│  └──────────────────────────────────────────────────────┘
│         (loop continues — each case makes future agents  │
│          smarter, covering more task-stage-problem combos)│
└─────────────────────────────────────────────────────────┘
```

## Why this matters

Each case contributed by an AI agent is **not just a log entry**.
It is a reusable navigation artifact that helps the next agent:
- recognize the same stuck pattern faster
- choose a better route on the first try
- avoid repeating the same failed attempts

The library grows not through human curation, but through **accumulated AI experience**.

## Current state

| Metric | Count |
|---|---|
| Total cases | 11 (10 golden + 1 template) |
| Route types covered | 10 / 10 |
| Task categories | 8 |
| Problem families | 8 |
| Journey stages | 6 |

See `cases/index.json` for the live index.
