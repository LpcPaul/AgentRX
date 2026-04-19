# Cases

One JSON file per tool. Each file is an array of case objects.

## Format

Each case:
```json
{
  "id": "playwright-mcp-001",
  "status": "verified",
  "symptom": "navigation timeout on SPA, empty DOM",
  "env": "linux, headless, proxy",
  "what_worked": "set waitUntil=networkidle and timeout=30s",
  "what_didnt_work": ["retry with same params"],
  "times_confirmed": 3,
  "note": "Often happens on JS-heavy pages behind proxy"
}
```

## Status values

- `draft` — single report, not yet confirmed
- `verified` — confirmed by ≥2 independent experiences
- `archived` — no longer relevant

## How to add

Append to the relevant tool file. If the tool file doesn't exist yet, create it.

## Legacy structure

The previous v2.1 structure (seeds/, index.json, templates/) is historical only. It is not used by the current MVP. See `docs/legacy/` for reference.
