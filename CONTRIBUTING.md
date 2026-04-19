# Contributing to AgentRX

## How to contribute

**Current focus: real recovery cases, not infrastructure.**

### Add or edit a case

1. Find the tool file in `cases/` (e.g. `cases/playwright-mcp.json`)
2. If the file doesn't exist, create it as a JSON array
3. Append your case:

```json
{
  "id": "playwright-mcp-003",
  "status": "draft",
  "symptom": "describe the exact failure you saw",
  "env": "OS, headless/headed, proxy, etc.",
  "what_worked": "the concrete fix that resolved it",
  "what_didnt_work": ["what you tried that didn't help"],
  "times_confirmed": 1,
  "note": "any context that helps future agents"
}
```

### What makes a good case

- **Concrete symptom** — exact error, timeout message, or behavior
- **Executable what_worked** — something another agent can directly apply
- **Honest what_didnt_work** — saves others from repeating dead ends
- **Real experience only** — no imagined or synthetic cases in the main cases/ directory

### Status values

- `draft` — single report, not yet confirmed by others
- `verified` — ≥2 independent experiences confirm the same fix works
- `archived` — no longer relevant (e.g. tool version changed, workaround upstreamed)

### What we don't require right now

- Complete v2.1 JSON submission
- Case ID generation scripts
- Schema validation
- Route registry alignment

Just write a clear case in the tool file. That's it.
