# Repository Cleanup and Upload Guide

This guide applies the repair pack without changing the application's coding style.

## 1. Back Up the Repository

Download a private backup before deleting or moving files.

## 2. Remove Sensitive and Generated Files from `main`

Delete these from the default branch:

- every historical `*.zip` source package;
- `dist/` and committed `*.exe` files;
- `data/hs_sms_v2.db`;
- runtime configuration such as `data/hs_sms_config.json`;
- generated invoices, exports, and backups;
- unrelated third-party ZIP packages in `HS SMS Offline Web` unless you own and are licensed to redistribute them.

A normal commit removes files from the latest branch but not earlier Git history. When a tracked database may contain real customer data or credentials, rewrite history using `git filter-repo` or GitHub's sensitive-data removal process, then rotate or invalidate any exposed credentials.

## 3. Add This Repair Pack

Copy these files to the repository root:

- `README.md`
- `.gitignore`
- `SECURITY.md`
- `CHANGELOG.md`
- `CONTRIBUTING.md`
- `LICENSE.md`
- `.github/ISSUE_TEMPLATE/`

Keep `data/.gitkeep` only to preserve the empty directory.

## 4. Simplify the Source Layout

Recommended migration:

```text
Current source:
HS SMS (Service Management System)/v3.2/HS_Service_Management_System_v2.py

Recommended source:
src/HS_Service_Management_System.py
```

Also move reusable icons to `assets/`, keep one current PyInstaller spec at the root, and remove duplicate or obsolete spec files after validating the build.

Do not refactor the application's internal coding style during this cleanup.

## 5. Move Archives to Releases

The repository already has a v3.2 release. Edit that release and replace weak text with `RELEASE_NOTES_v3.2.md`.

For each maintained version:

1. create a version tag such as `v3.2.0`;
2. create a GitHub Release;
3. upload the Windows package and optional source package;
4. attach a SHA-256 checksum file;
5. mark only the newest stable release as Latest.

Avoid recreating all minor historical versions unless users genuinely need them. Keep a small, useful release history.

## 6. Add Screenshots

Capture sanitized screenshots with no real customer information:

- dashboard;
- customer list;
- service-job form;
- invoice preview;
- reports;
- backup and restore;
- theme selection.

Store them in `docs/screenshots/` and update the README image paths.

## 7. Repository Settings

Set the About description to:

> Offline Windows service management system for repair businesses, built with Python, Tkinter and SQLite.

Set the website to:

> https://habitablesolution.com/

Recommended topics:

```text
python
tkinter
sqlite
windows-desktop
service-management
repair-shop
customer-management
invoice-management
inventory-management
backup-restore
business-software
pyinstaller
```

Enable:

- Issues
- Discussions only when you are ready to moderate them
- Dependabot alerts
- Secret scanning and push protection when available
- Private vulnerability reporting

Add branch protection for `main` when collaborators begin contributing.

## 8. Suggested Commits

```text
chore: add repository documentation and community files
security: stop tracking runtime database and configuration
chore: remove generated binaries and archives from main
refactor: move current source into a clean src directory
docs: add sanitized application screenshots
release: publish v3.2.0 assets and checksums
```

## 9. Final Verification

Confirm that:

- the README renders correctly;
- the latest release downloads successfully;
- no populated database is publicly accessible;
- no executable or ZIP remains in `main`;
- the application builds from a clean clone;
- links and issue templates work;
- the displayed licence matches your commercial intentions;
- screenshots contain no private information.
