# Contributing to Skill Doctor

Thank you for considering contributing to Skill Doctor! This project exists because of people like you.

## How You Can Contribute

### 1. Submit Case Reports

The most valuable contribution you can make is sharing your skill failure experiences. Every case helps the community.

- **Automatic**: Use Skill Doctor's built-in diagnosis flow (recommended)
- **Manual**: Create an issue using the [Case Report template](https://github.com/LpcPaul/skill-doctor/issues/new?template=case_report.yml)
- **PR**: Add a JSON file to `cases/by-skill/` and update `cases/index.json`

**All cases are automatically redacted for privacy before submission.**

### 2. Improve Diagnostics

Found a failure pattern that's not covered?

1. Add the pattern to `rules/failure_types.yaml`
2. Write a test case in `cases/`
3. Update the remedy recommendations

### 3. Improve Redaction

Privacy is paramount. If you find gaps in `scripts/redact.py`:

1. Write a failing test in `tests/test_redact.py`
2. Fix the pattern
3. Ensure all 43+ existing tests still pass

### 4. Report Bugs / Request Features

Open an issue with:
- Clear description of the problem
- Steps to reproduce (if applicable)
- Expected vs actual behavior

### 5. Improve Documentation

Typos, unclear instructions, missing examples — all welcome.

## Development Setup

```bash
git clone https://github.com/LpcPaul/skill-doctor.git
cd skill-doctor

# Run tests
python3 -m pytest tests/ -v

# Test redaction manually
python3 scripts/redact.py --input /path/to/case.json --dry-run
```

## Case Report Guidelines

Every case must pass `redact.py` checks. This means:
- No file paths, URLs (except GitHub), or IP addresses
- No email addresses, phone numbers, or API keys
- No business content (client names, financial data, etc.)
- Only engineering-level descriptions of failure patterns

**Test**: If someone reads your case, they should understand the ENGINEERING problem but have ZERO idea what business task was being performed.

## Pull Request Process

1. Fork the repo and create a branch
2. Make your changes
3. Run `python3 -m pytest tests/ -v` to ensure tests pass
4. Update documentation if needed
5. Submit the PR

## Code Style

- Bash scripts: `set -euo pipefail` at the top
- Python: Follow PEP 8, use type hints where practical
- JSON: 2-space indent, trailing newline
- Commit messages: [Conventional Commits](https://www.conventionalcommits.org/)

## Questions?

Open an issue or reach out — we're happy to help.
