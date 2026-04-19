# AgentRX MVP

## Why we shrank from v2.1

The v2.1 architecture (schema validation, route registry, deterministic retrieval, automated hooks) was infrastructure built before validating the core question: **does case content actually help agents recover?**

This MVP tests that first. If yes, we grow back heavy architecture on proven ground. If no, we saved months of wasted engineering.

## The one question we validate now

> Does a case library + ultra-short skill actually help agents recover faster from third-party tool failures?

## What MVP does now

- Ultra-short SKILL.md (activation, lookup, record)
- Flat `cases/` — one JSON file per tool, case array inside
- `ledger.jsonl` — append-only experience log
- Minimal case format: symptom, what_worked, what_didnt_work, times_confirmed

## What MVP does not do (yet)

- v2.1 schema validation
- Route registry / recommendation
- Deterministic retrieval scripts
- Build index / validate / generate scripts
- Automated hooks
- Complex directory structure
- Synthetic seed cases

## Future expansion order

1. **30-50 real cases** — prove content value first
2. **Env structure** — add structured environment fields when needed
3. **Index / retrieval scripts** — when flat files become hard to navigate
4. **Hook automation** — when manual activation friction is proven
5. **Formal schema + distillation pipeline** — only when content volume justifies it
