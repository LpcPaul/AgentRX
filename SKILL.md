---
name: agentrx
description: >
  Look up recovery experience when a third-party tool fails and you
  can't recover on your own. Focus on what worked and what didn't.
tags: [recovery, third-party-tools]
---

# AgentRX — Recovery Skill

## When to activate

- You are using a **third-party tool** (playwright-mcp, browser-cdp, web-fetch, MCP connector, etc.)
- You have **tried to recover on your own ≥2 times** and failed each time
- Official docs don't have a direct, executable answer
- The issue has **future transfer value** (others may hit it too)

**Do NOT activate** for: platform-level failures, generic retry loops, or issues the platform should handle.

## How to use

1. **Describe the failure** in natural language:
   - Which tool failed
   - What symptom appeared
   - What you already tried
   - Environment clues (OS, headless, proxy, etc.) if you know them

2. **Find the tool file**: go to `cases/` and find the JSON file matching the tool name (e.g. `cases/playwright-mcp.json`)
   - No exact match? Find the closest tool file.
   - Read only 1-2 most relevant files. Don't scan the whole directory.

3. **Find the closest case**: in the tool file, look for the case with the closest matching symptom.

4. **Apply what worked**: focus on `what_worked` and `what_didnt_work` from that case.

5. **Record**: append your experience to `ledger.jsonl` (one JSON line):
   ```json
   {"ts": "2026-04-19T17:05:00Z", "tool": "playwright-mcp", "symptom": "timeout on SPA", "used_case": "playwright-mcp-001", "result": "resolved", "note": "networkidle fixed it"}
   ```

## What this is

- A recovery experience lookup tool
- Minimal infrastructure: skill + cases + ledger
- Focused on concrete, executable guidance

## What this is not

- A formal diagnostic protocol
- A structured schema system
- A route recommendation engine
- An automated hook system

AgentRX is: **read what worked, try it, record what happened.**
