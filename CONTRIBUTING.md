# Contributing

Thank you for your interest in HS Service Management System.

This is a commercial, source-available project. Public access to the repository does not automatically grant permission to reuse, redistribute, sell, or relicence the software. By submitting a contribution, you confirm that you have the right to provide it and allow Habitable Solution to use it in this project.

## Before You Start

- Search existing issues before opening a new one.
- Use the bug-report template for reproducible defects.
- Use the feature-request template for product ideas.
- Discuss large architectural changes before implementing them.
- Never include customer information, passwords, populated databases, backups, or proprietary third-party files.

## Development Setup

```bash
python -m venv .venv
```

Windows:

```bat
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Run the current source entry point documented in `README.md`.

## Coding Guidelines

- Preserve the existing coding style unless a change is necessary for correctness, security, maintainability, or testing.
- Keep pull requests focused on one problem.
- Prefer clear names and small, reviewable changes.
- Do not mix broad formatting changes with functional changes.
- Use parameterized SQL queries.
- Handle file and database errors without exposing sensitive data.
- Update documentation when behaviour changes.
- Add or update tests when a test framework is available.

## Pull Requests

A useful pull request should contain:

1. a clear title;
2. the problem being solved;
3. a summary of the implementation;
4. steps used to test the change;
5. screenshots for user-interface changes;
6. any compatibility or migration notes.

## Commit Messages

Use short, descriptive messages, for example:

```text
fix: prevent duplicate customer codes
feat: add job status filter
security: stop tracking runtime database
 docs: document Windows build process
```

## Security Reports

Do not use issues or pull requests for undisclosed vulnerabilities. Follow `SECURITY.md`.
