#!/usr/bin/env python3
"""
AgentRX — Generate Golden Cases

Creates 10 high-quality v2.1 golden cases covering the most common stuck states.
Each case uses evidence/inference structure, standard route ids, and realistic detail.
"""

import json
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
CASES_DIR = REPO_ROOT / "cases"


def save_case(case: dict, filename: str):
    out = CASES_DIR / filename
    with open(out, "w") as f:
        json.dump(case, f, indent=2, ensure_ascii=False)
    print(f"  Created: {filename}")


cases = [
    # ── Case 1: Web research blocked / low confidence ──
    {
        "schema_version": "2.1",
        "id": "2026-04-17-browse-web-001",
        "title": "browse-web execute-task capability_mismatch",
        "summary": "Agent used a static HTML fetch tool for a dynamically rendered page. Only the shell was captured, missing all content populated by JavaScript.",
        "created_at": "2026-04-17T00:00:00Z",
        "tags": ["browse-web", "execute-task", "capability_mismatch", "dynamic-rendering"],
        "evidence": {
            "task": "browse-web",
            "desired_outcome": "Extract the full product listing table from a retail website.",
            "attempted_path": {
                "tool": "web_fetch",
                "tool_type": "builtin",
                "other_tools": [
                    {"name": "playwright-mcp", "type": "mcp", "role": "candidate alternative"},
                    {"name": "browser-cdp", "type": "skill", "role": "candidate alternative"}
                ]
            },
            "symptom": "The fetched HTML only contains the page skeleton. All product data loaded via JavaScript is missing.",
            "symptom_tags": ["partial-content", "client-side-rendering"],
            "context": "The target website is a modern single-page application that loads product data via API after the initial HTML loads.",
            "environment": {
                "platform": "claude-code",
                "requires_login": False,
                "requires_dynamic_render": True,
                "requires_local_filesystem": False,
                "requires_network": True,
                "requires_deterministic_execution": False,
                "notes": "Client-side rendering detected."
            },
            "failed_step": "Static HTML fetch returned page skeleton without JavaScript-rendered content",
            "artifacts_used": ["HTML page", "public URL"],
            "reproduction_steps": [
                "Used web_fetch builtin to retrieve the page",
                "Parsed HTML — found only skeleton structure, no product data",
                "Retried with same approach — same result"
            ]
        },
        "inference": {
            "journey_stage": "execute-task",
            "problem_family": "capability_mismatch",
            "why_current_path_failed": "The builtin fetch tool retrieves static HTML only. The product data on this page is rendered client-side via JavaScript, which static fetch cannot execute.",
            "best_candidate_route_id": "switch_to_alternative_tool_path",
            "best_candidate_route_detail": "Switch to a browser-capable route that executes JavaScript. playwright-mcp can render the page and extract the full DOM. Alternatively, browser-cdp skill with explicit wait-for-content logic.",
            "prerequisites_for_switch": ["internet_access", "repo_access"],
            "confidence": "high"
        },
        "resolution": {"outcome": "resolved", "follow_up_notes": "Switched to playwright-mcp which rendered the page and extracted the complete product table."},
        "verified": False,
        "related_cases": [],
        "legacy_mapping": {}
    },

    # ── Case 2: Should switch to official docs ──
    {
        "schema_version": "2.1",
        "id": "2026-04-17-code-editing-001",
        "title": "code-editing execute-task configuration",
        "summary": "Agent attempted to integrate a third-party API using guessed parameter names and structure, resulting in repeated authentication errors.",
        "created_at": "2026-04-17T00:00:00Z",
        "tags": ["code-editing", "execute-task", "configuration", "third-party-api"],
        "evidence": {
            "task": "code-editing",
            "desired_outcome": "Integrate a payment gateway API into the existing application.",
            "attempted_path": {
                "tool": "code-editing",
                "tool_type": "skill",
                "other_tools": []
            },
            "symptom": "Repeated API calls fail with authentication errors. The agent has tried different credential formats without success.",
            "symptom_tags": ["api-error", "authentication-failure"],
            "context": "The payment gateway requires a specific authentication flow that differs from the agent's assumptions based on other API integrations.",
            "environment": {
                "platform": "claude-code",
                "requires_login": False,
                "requires_dynamic_render": False,
                "requires_local_filesystem": True,
                "requires_network": True,
                "requires_deterministic_execution": False,
                "notes": "Has API credentials but format is uncertain."
            },
            "failed_step": "API authentication fails with 'invalid request format' error",
            "artifacts_used": ["source code", "API credentials"],
            "reproduction_steps": [
                "Attempted integration with assumed authentication pattern",
                "Retried with different credential encoding — same error",
                "Tried alternative endpoint — different error received"
            ]
        },
        "inference": {
            "journey_stage": "execute-task",
            "problem_family": "configuration",
            "why_current_path_failed": "The agent is working from assumptions about API behavior rather than the actual specification. Without the authoritative documentation, every attempt is a guess.",
            "best_candidate_route_id": "switch_to_official_docs",
            "best_candidate_route_detail": "Fetch the payment gateway's official API documentation to understand the correct authentication flow, required headers, and request format. This is faster than trial-and-error.",
            "prerequisites_for_switch": ["internet_access"],
            "confidence": "high"
        },
        "resolution": {"outcome": "resolved", "follow_up_notes": "Official docs revealed a two-step OAuth flow the agent was not aware of."},
        "verified": False,
        "related_cases": [],
        "legacy_mapping": {}
    },

    # ── Case 3: Should inspect local files first ──
    {
        "schema_version": "2.1",
        "id": "2026-04-17-analyze-data-001",
        "title": "analyze-data understand-task observability_gap",
        "summary": "Agent tried to analyze data but could not find the source file because it was looking in the wrong directory and using the wrong filename.",
        "created_at": "2026-04-17T00:00:00Z",
        "tags": ["analyze-data", "understand-task", "observability_gap", "file-location"],
        "evidence": {
            "task": "analyze-data",
            "desired_outcome": "Generate a summary report from a CSV dataset uploaded by the user.",
            "attempted_path": {
                "tool": "python",
                "tool_type": "builtin",
                "other_tools": []
            },
            "symptom": "File not found error. The agent searched for 'data.csv' in the current directory but the file was named 'Q1_results.csv' and located in a subdirectory.",
            "symptom_tags": ["file-not-found", "wrong-path"],
            "context": "The user uploaded a dataset but did not specify the exact filename or location. The agent assumed a generic name.",
            "environment": {
                "platform": "claude-code",
                "requires_login": False,
                "requires_dynamic_render": False,
                "requires_local_filesystem": True,
                "requires_network": False,
                "requires_deterministic_execution": False,
                "notes": "Files available but undiscovered."
            },
            "failed_step": "Attempted to read 'data.csv' — file not found",
            "artifacts_used": ["CSV dataset (undiscovered)"],
            "reproduction_steps": [
                "Tried reading data.csv from root directory",
                "Searched for *.csv in root — found nothing",
                "Asked user for file location — no response yet"
            ]
        },
        "inference": {
            "journey_stage": "understand-task",
            "problem_family": "observability_gap",
            "why_current_path_failed": "The agent has insufficient visibility into the available files. Before attempting data analysis, it needs to discover what files exist and where they are located.",
            "best_candidate_route_id": "switch_to_local_file_inspection",
            "best_candidate_route_detail": "Run a recursive file listing or glob search to discover all available CSV files in the workspace. Once the correct file is found, proceed with analysis.",
            "prerequisites_for_switch": ["repo_access"],
            "confidence": "high"
        },
        "resolution": {"outcome": "resolved", "follow_up_notes": "File listing revealed Q1_results.csv in data/raw/. Analysis completed successfully."},
        "verified": False,
        "related_cases": [],
        "legacy_mapping": {}
    },

    # ── Case 4: Missing input / missing artifact ──
    {
        "schema_version": "2.1",
        "id": "2026-04-17-create-presentation-001",
        "title": "create-presentation choose-capability task_framing_issue",
        "summary": "Agent was asked to create a presentation but received no content outline, speaker notes, or design preferences. Multiple attempts to generate content were all rejected.",
        "created_at": "2026-04-17T00:00:00Z",
        "tags": ["create-presentation", "choose-capability", "task_framing_issue", "missing-input"],
        "evidence": {
            "task": "create-presentation",
            "desired_outcome": "Generate a slide deck for a quarterly business review.",
            "attempted_path": {
                "tool": "pptx-generator",
                "tool_type": "skill",
                "other_tools": [
                    {"name": "markdown-slides", "type": "skill", "role": "format alternative"}
                ]
            },
            "symptom": "Every generated slide deck is rejected by the user for being too generic, wrong tone, or missing key metrics.",
            "symptom_tags": ["output-rejected", "generic-content"],
            "context": "The user's request was a single sentence: 'Create a Q4 review deck.' No outline, no data, no design preferences were provided.",
            "environment": {
                "platform": "claude-ai",
                "requires_login": False,
                "requires_dynamic_render": False,
                "requires_local_filesystem": False,
                "requires_network": False,
                "requires_deterministic_execution": False,
                "notes": "No supporting materials available."
            },
            "failed_step": "Generated three different slide deck drafts, all rejected",
            "artifacts_used": [],
            "reproduction_steps": [
                "Generated generic Q4 deck — rejected as too generic",
                "Tried more data-heavy approach — rejected for wrong tone",
                "Switched to markdown slides — rejected for wrong format"
            ]
        },
        "inference": {
            "journey_stage": "choose-capability",
            "problem_family": "task_framing_issue",
            "why_current_path_failed": "The task is underspecified. The agent cannot produce a satisfactory presentation without knowing the audience, key metrics, design preferences, or outline. Continuing to generate drafts is wasted effort.",
            "best_candidate_route_id": "request_missing_input",
            "best_candidate_route_detail": "Ask the user for: (1) key metrics or data points to include, (2) target audience, (3) preferred tone and design style, (4) any existing outline or reference deck.",
            "prerequisites_for_switch": [],
            "confidence": "high"
        },
        "resolution": {"outcome": "resolved", "follow_up_notes": "User provided an outline and three key metrics. Presentation generated successfully on second attempt."},
        "verified": False,
        "related_cases": [],
        "legacy_mapping": {}
    },

    # ── Case 5: Environment debugging ──
    {
        "schema_version": "2.1",
        "id": "2026-04-17-code-editing-002",
        "title": "code-editing configure-capability environment",
        "summary": "Agent repeatedly failed to run a Python script because a required package was not installed in the environment, but kept retrying the same execution.",
        "created_at": "2026-04-17T00:00:00Z",
        "tags": ["code-editing", "configure-capability", "environment", "dependency"],
        "evidence": {
            "task": "code-editing",
            "desired_outcome": "Run a data visualization script that uses matplotlib and seaborn.",
            "attempted_path": {
                "tool": "python",
                "tool_type": "builtin",
                "other_tools": []
            },
            "symptom": "ModuleNotFoundError: No module named 'seaborn'. The agent retried the script three times without addressing the missing dependency.",
            "symptom_tags": ["import-error", "missing-dependency"],
            "context": "The script requires matplotlib and seaborn. Only matplotlib was pre-installed in the environment.",
            "environment": {
                "platform": "claude-code",
                "requires_login": False,
                "requires_dynamic_render": False,
                "requires_local_filesystem": True,
                "requires_network": True,
                "requires_deterministic_execution": False,
                "notes": "Sandboxed environment with limited package installation ability."
            },
            "failed_step": "python script.py fails with ModuleNotFoundError for seaborn",
            "artifacts_used": ["Python script", "requirements file"],
            "reproduction_steps": [
                "Ran script.py — ModuleNotFoundError: seaborn",
                "Retried — same error",
                "Retried with different working directory — same error"
            ]
        },
        "inference": {
            "journey_stage": "configure-capability",
            "problem_family": "environment",
            "why_current_path_failed": "The execution environment is missing a required dependency. Retrying the script will not install seaborn — the environment must be fixed first.",
            "best_candidate_route_id": "switch_to_environment_debugging",
            "best_candidate_route_detail": "Install the missing seaborn package via pip, or modify the script to use only available packages. If pip install is blocked in this environment, fall back to matplotlib-only visualization.",
            "prerequisites_for_switch": ["repo_access", "internet_access"],
            "confidence": "high"
        },
        "resolution": {"outcome": "resolved", "follow_up_notes": "pip install seaborn succeeded. Script ran successfully."},
        "verified": False,
        "related_cases": [],
        "legacy_mapping": {}
    },

    # ── Case 6: Schema / format validation ──
    {
        "schema_version": "2.1",
        "id": "2026-04-17-transform-documents-001",
        "title": "transform-documents validate-output quality_miss",
        "summary": "Agent generated a JSON config file but the output was missing required fields and had incorrect nesting, causing the downstream system to reject it.",
        "created_at": "2026-04-17T00:00:00Z",
        "tags": ["transform-documents", "validate-output", "quality_miss", "json-validation"],
        "evidence": {
            "task": "transform-documents",
            "desired_outcome": "Generate a valid JSON configuration file for a CI/CD pipeline.",
            "attempted_path": {
                "tool": "code-editing",
                "tool_type": "skill",
                "other_tools": []
            },
            "symptom": "The generated JSON file is rejected by the CI/CD system. Missing required 'version' field, and the 'stages' array is nested under the wrong parent key.",
            "symptom_tags": ["schema-invalid", "wrong-structure"],
            "context": "The CI/CD system expects a specific JSON schema with 'version', 'stages', and 'jobs' at the top level.",
            "environment": {
                "platform": "claude-code",
                "requires_login": False,
                "requires_dynamic_render": False,
                "requires_local_filesystem": True,
                "requires_network": False,
                "requires_deterministic_execution": False,
                "notes": "Schema reference available in project docs."
            },
            "failed_step": "CI/CD pipeline rejects config with 'missing required field: version'",
            "artifacts_used": ["JSON config file", "CI/CD schema documentation"],
            "reproduction_steps": [
                "Generated initial JSON config",
                "Pipeline rejected — missing 'version' field",
                "Added version but placed stages under wrong parent — rejected again"
            ]
        },
        "inference": {
            "journey_stage": "validate-output",
            "problem_family": "quality_miss",
            "why_current_path_failed": "The agent is generating JSON without validating against the target schema. Each retry fixes one issue but introduces another because there is no schema-level validation step.",
            "best_candidate_route_id": "switch_to_schema_or_format_validation",
            "best_candidate_route_detail": "Use the project's CI/CD schema documentation as a template. Generate the JSON by filling in the schema structure rather than writing it from scratch. Validate the output against the schema before submission.",
            "prerequisites_for_switch": [],
            "confidence": "medium"
        },
        "resolution": {"outcome": "resolved", "follow_up_notes": "Used schema doc as template. Validated with jsonschema before committing."},
        "verified": False,
        "related_cases": [],
        "legacy_mapping": {}
    },

    # ── Case 7: Task should be decomposed first ──
    {
        "schema_version": "2.1",
        "id": "2026-04-17-workflow-automation-001",
        "title": "workflow-automation choose-capability capability_mismatch",
        "summary": "Agent was asked to build a full dashboard application in one task. It produced a partial implementation that mixed frontend, backend, and data pipeline code without clear separation.",
        "created_at": "2026-04-17T00:00:00Z",
        "tags": ["workflow-automation", "choose-capability", "capability_mismatch", "complex-task"],
        "evidence": {
            "task": "workflow-automation",
            "desired_outcome": "Build a data dashboard with charts, filters, and a backend API serving live metrics.",
            "attempted_path": {
                "tool": "code-editing",
                "tool_type": "skill",
                "other_tools": [
                    {"name": "frontend-design", "type": "skill", "role": "candidate alternative"}
                ]
            },
            "symptom": "The generated code mixes frontend components, API routes, and data transformation logic in a single file. The result is incomplete and unrunnable.",
            "symptom_tags": ["mixed-concerns", "incomplete-implementation"],
            "context": "The dashboard requires three distinct components: (1) frontend UI, (2) backend API, (3) data processing pipeline. The agent tried to address all three in one pass.",
            "environment": {
                "platform": "claude-code",
                "requires_login": False,
                "requires_dynamic_render": False,
                "requires_local_filesystem": True,
                "requires_network": True,
                "requires_deterministic_execution": False,
                "notes": "No existing project structure to build upon."
            },
            "failed_step": "Generated monolithic code that cannot be run as-is",
            "artifacts_used": ["partial code output"],
            "reproduction_steps": [
                "Generated full-stack code in one file — unrunnable",
                "Attempted to split into components mid-generation — structure became inconsistent"
            ]
        },
        "inference": {
            "journey_stage": "choose-capability",
            "problem_family": "capability_mismatch",
            "why_current_path_failed": "The task is too large for a single tool path. The agent needs to decompose it into independent sub-tasks (frontend, backend, data) and address each separately.",
            "best_candidate_route_id": "decompose_task_first",
            "best_candidate_route_detail": "Split into three phases: (1) Design the data model and API contract, (2) Build the backend API, (3) Build the frontend. Each phase uses a focused tool path.",
            "prerequisites_for_switch": [],
            "confidence": "high"
        },
        "resolution": {"outcome": "partially_resolved", "follow_up_notes": "Decomposed into three sub-tasks. Backend API completed successfully. Frontend pending."},
        "verified": False,
        "related_cases": [],
        "legacy_mapping": {}
    },

    # ── Case 8: Current tool path is wrong abstraction level ──
    {
        "schema_version": "2.1",
        "id": "2026-04-17-search-and-compare-tools-001",
        "title": "search-and-compare-tools understand-task better_alternative_exists",
        "summary": "Agent used a general web search to find technical API documentation, but the search results returned blog posts and tutorials instead of authoritative references.",
        "created_at": "2026-04-17T00:00:00Z",
        "tags": ["search-and-compare-tools", "understand-task", "better_alternative_exists", "web-research"],
        "evidence": {
            "task": "search-and-compare-tools",
            "desired_outcome": "Find the correct method signature for a specific library function.",
            "attempted_path": {
                "tool": "tavily",
                "tool_type": "skill",
                "other_tools": [
                    {"name": "web_fetch", "type": "builtin", "role": "candidate alternative"}
                ]
            },
            "symptom": "Web search returns blog posts and StackOverflow answers from 2022, which reference deprecated method signatures. No official documentation links appear in results.",
            "symptom_tags": ["outdated-results", "wrong-result-type"],
            "context": "The library was recently updated with breaking changes. General web search favors popular but outdated content.",
            "environment": {
                "platform": "claude-ai",
                "requires_login": False,
                "requires_dynamic_render": False,
                "requires_local_filesystem": False,
                "requires_network": True,
                "requires_deterministic_execution": False,
                "notes": "Internet access available."
            },
            "failed_step": "Web search returned outdated tutorial content, not current API reference",
            "artifacts_used": ["search query"],
            "reproduction_steps": [
                "Searched for method signature using general web search",
                "Retried with more specific query — still got outdated results"
            ]
        },
        "inference": {
            "journey_stage": "understand-task",
            "problem_family": "better_alternative_exists",
            "why_current_path_failed": "General web search is not the right tool for finding authoritative API documentation. It returns popular content, which in this case is outdated.",
            "best_candidate_route_id": "switch_to_web_research",
            "best_candidate_route_detail": "Use a targeted approach: search specifically for the library's official documentation site, or use web_fetch to directly access the library's docs URL. A focused search with 'site:library-docs-domain' would yield current results.",
            "prerequisites_for_switch": ["internet_access"],
            "confidence": "medium"
        },
        "resolution": {"outcome": "resolved", "follow_up_notes": "Used site-specific search to find official docs with current method signature."},
        "verified": False,
        "related_cases": [],
        "legacy_mapping": {}
    },

    # ── Case 9: Reproduction minimization needed ──
    {
        "schema_version": "2.1",
        "id": "2026-04-17-code-editing-003",
        "title": "code-editing recover-from-failure recovery_gap",
        "summary": "Agent encountered an intermittent test failure that only reproduces 30% of the time. Multiple retry attempts produced inconsistent results, making root cause identification impossible.",
        "created_at": "2026-04-17T00:00:00Z",
        "tags": ["code-editing", "recover-from-failure", "recovery_gap", "flaky-test"],
        "evidence": {
            "task": "code-editing",
            "desired_outcome": "Fix a failing unit test in the authentication module.",
            "attempted_path": {
                "tool": "code-editing",
                "tool_type": "skill",
                "other_tools": []
            },
            "symptom": "The test fails intermittently — approximately 30% of runs produce a timeout error. When it passes, the agent cannot determine which change fixed it.",
            "symptom_tags": ["intermittent-failure", "timeout"],
            "context": "The test involves an async HTTP call with a 5-second timeout. Network latency in the test environment may be a factor.",
            "environment": {
                "platform": "claude-code",
                "requires_login": False,
                "requires_dynamic_render": False,
                "requires_local_filesystem": True,
                "requires_network": True,
                "requires_deterministic_execution": False,
                "notes": "Test environment has variable network conditions."
            },
            "failed_step": "Unit test times out intermittently (~30% failure rate)",
            "artifacts_used": ["test file", "source code"],
            "reproduction_steps": [
                "Ran test 5 times — failed 2 times with timeout",
                "Modified retry logic — passed 3 times, failed 2 times",
                "Increased timeout — passed 4 times, failed 1 time"
            ]
        },
        "inference": {
            "journey_stage": "recover-from-failure",
            "problem_family": "recovery_gap",
            "why_current_path_failed": "The intermittent nature of the failure makes it impossible to determine if a code change actually fixed the issue. The agent needs a reliable reproduction method before attempting fixes.",
            "best_candidate_route_id": "switch_to_repro_minimization",
            "best_candidate_route_detail": "Create a minimal reproduction script that isolates the async HTTP call and runs it repeatedly to confirm the failure pattern. Then test fixes against this reproducible setup rather than the full test suite.",
            "prerequisites_for_switch": ["repo_access"],
            "confidence": "medium"
        },
        "resolution": {"outcome": "partially_resolved", "follow_up_notes": "Isolated the HTTP call in a minimal script. Confirmed timeout correlates with network latency spikes. Fix pending."},
        "verified": False,
        "related_cases": [],
        "legacy_mapping": {}
    },

    # ── Case 10: API or connector access needed ──
    {
        "schema_version": "2.1",
        "id": "2026-04-17-monitor-and-check-001",
        "title": "monitor-and-check execute-task better_alternative_exists",
        "summary": "Agent attempted to monitor a cloud service's status by scraping a public status page, but the page structure changed and the scraper broke.",
        "created_at": "2026-04-17T00:00:00Z",
        "tags": ["monitor-and-check", "execute-task", "better_alternative_exists", "status-monitoring"],
        "evidence": {
            "task": "monitor-and-check",
            "desired_outcome": "Monitor the operational status of a cloud service and alert on incidents.",
            "attempted_path": {
                "tool": "browser-cdp",
                "tool_type": "skill",
                "other_tools": [
                    {"name": "cloud-status-api-mcp", "type": "mcp", "role": "candidate alternative"}
                ]
            },
            "symptom": "The web scraper broke after the status page was redesigned. The CSS selectors no longer match, and the agent cannot maintain the scraper.",
            "symptom_tags": ["scraper-broken", "brittle-automation"],
            "context": "The service provider offers an official status API with structured incident data, but the agent was not aware of it.",
            "environment": {
                "platform": "openclaw",
                "requires_login": False,
                "requires_dynamic_render": True,
                "requires_local_filesystem": False,
                "requires_network": True,
                "requires_deterministic_execution": False,
                "notes": "API key available but not configured."
            },
            "failed_step": "Web scraper CSS selectors no longer match redesigned status page",
            "artifacts_used": ["scraper script", "status page URL"],
            "reproduction_steps": [
                "Ran scraper — selectors failed to match",
                "Updated selectors for new page structure — different elements broke next day",
                "Tried regex-based extraction — inconsistent results"
            ]
        },
        "inference": {
            "journey_stage": "execute-task",
            "problem_family": "better_alternative_exists",
            "why_current_path_failed": "Web scraping a status page is a fragile approach. The page structure can change at any time, breaking the scraper. An official API provides structured, stable data.",
            "best_candidate_route_id": "switch_to_api_or_connector_access",
            "best_candidate_route_detail": "Configure the cloud-status-api-mcp connector using the available API key. This provides structured incident data without the fragility of web scraping.",
            "prerequisites_for_switch": ["api_credentials_available", "internet_access"],
            "confidence": "high"
        },
        "resolution": {"outcome": "resolved", "follow_up_notes": "Configured cloud-status-api-mcp with API key. Monitoring is stable and data is structured."},
        "verified": False,
        "related_cases": [],
        "legacy_mapping": {}
    },
]

# Save each case as a separate file
for case in cases:
    filename = f"{case['id']}.json"
    save_case(case, filename)

print(f"\nGenerated {len(cases)} golden cases")
print(f"Route coverage:")
route_ids = sorted(set(c['inference']['best_candidate_route_id'] for c in cases))
for rid in route_ids:
    count = sum(1 for c in cases if c['inference']['best_candidate_route_id'] == rid)
    print(f"  {rid}: {count} case(s)")
