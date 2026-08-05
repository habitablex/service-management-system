<div align="center">

# HS Service Management System

**Offline desktop software for managing customers, devices, service jobs, invoices, warranties, reports, and backups.**

[![Latest Release](https://img.shields.io/github/v/release/habitablex/service-management-system?display_name=tag&sort=semver)](https://github.com/habitablex/service-management-system/releases/latest)
[![Platform](https://img.shields.io/badge/platform-Windows-0078D4)](#system-requirements)
[![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB)](https://www.python.org/)
[![UI](https://img.shields.io/badge/UI-Tkinter-2C3E50)](#technology)
[![Database](https://img.shields.io/badge/database-SQLite-003B57)](https://www.sqlite.org/)
[![License](https://img.shields.io/badge/license-Proprietary-red)](LICENSE.md)

[Download Latest Release](https://github.com/habitablex/service-management-system/releases/latest) · [Report a Bug](https://github.com/habitablex/service-management-system/issues/new?template=bug_report.yml) · [Request a Feature](https://github.com/habitablex/service-management-system/issues/new?template=feature_request.yml)

</div>

## Overview

HS Service Management System (HS-SMS) is a Windows-focused, offline desktop application created for computer, laptop, UPS, printer, GPU, networking, CCTV, and other technical service businesses.

The application helps a service centre keep customer, device, repair, payment, warranty, work-log, and backup information in one local system. It uses Python, Tkinter, and SQLite and does not require a cloud subscription for its core workflow.

> **Project status:** Active commercial project. The latest public release is **v3.2**.

## Key Features

- Customer records and contact information
- Device records, specifications, serial numbers, and accessories
- Service jobs with status, priority, issue description, and engineer notes
- Work logs and parts-used tracking
- Estimates, final amounts, payments, discounts, and VAT
- Browser-based invoice and money-receipt preview with print or PDF support
- Warranty period and warranty-expiry tracking
- Business reports and JSON export
- Configurable device categories and service types
- Multiple light and dark interface themes
- Local SQLite backup and restore
- Automatic backup when the application closes
- Optional startup prompt to restore the latest backup

## Screenshots

Add current v3.2 screenshots to `docs/screenshots/`, then replace the placeholders below.

| Dashboard | Service Jobs |
|---|---|
| `docs/screenshots/dashboard.png` | `docs/screenshots/service-jobs.png` |

| Invoice | Backup & Restore |
|---|---|
| `docs/screenshots/invoice.png` | `docs/screenshots/backup-restore.png` |

## Technology

| Component | Technology |
|---|---|
| Language | Python 3.11+ |
| Desktop UI | Tkinter / ttk |
| Database | SQLite |
| Configuration | JSON |
| Windows packaging | PyInstaller |
| Invoice output | Local HTML opened in the default browser |

## System Requirements

### Running the Windows application

- Windows 10 or Windows 11
- A standard desktop or laptop computer
- Write permission for the application data and backup folders

### Running from source

- Python 3.11 or newer
- Tkinter, normally included with the standard Windows Python installer
- PyInstaller 6.0 or newer when building the executable

## Download

Use the **GitHub Releases** page for packaged downloads. Binary files and historical ZIP packages should not be stored in the main source branch.

**Latest release:** <https://github.com/habitablex/service-management-system/releases/latest>

Before running a downloaded executable, verify that it came from the official repository and scan it with your security software.

## Run from Source

```bash
git clone https://github.com/habitablex/service-management-system.git
cd service-management-system
python -m venv .venv
```

Activate the environment on Windows:

```bat
.venv\Scripts\activate
```

Install build requirements and start the application:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
python src/HS_Service_Management_System.py
```

> During repository cleanup, move the current v3.2 source file into `src/` and rename it consistently. Until that migration is complete, use the path currently included in the repository.

## Build a Windows Executable

```bash
pyinstaller HS_Service_Management_System_v3_2.spec
```

The executable should be published as a GitHub Release asset instead of being committed to `main`.

## Data and Backups

The application stores operational information in a local SQLite database and saves configuration in JSON. The default backup location is under:

```text
Documents/Habitable Solution/HS Service Management System/backups
```

### Important data notice

Customer databases, configuration files, generated invoices, and backup files must never be committed to this public repository. The included `.gitignore` blocks common runtime-data paths.

The current application schema includes device and BIOS password fields. Treat these as sensitive data. Do not store real credentials in an unencrypted database or share a database file publicly. See [SECURITY.md](SECURITY.md).

## Recommended Repository Structure

```text
service-management-system/
├── .github/
│   └── ISSUE_TEMPLATE/
├── assets/
├── docs/
│   └── screenshots/
├── src/
│   └── HS_Service_Management_System.py
├── tests/
├── .gitignore
├── CHANGELOG.md
├── CONTRIBUTING.md
├── LICENSE.md
├── README.md
├── SECURITY.md
├── requirements.txt
└── HS_Service_Management_System_v3_2.spec
```

## Current Limitations

- The application is primarily designed and packaged for Windows.
- Runtime data is stored locally and is not automatically synchronized between computers.
- The current project does not advertise encrypted database storage.
- Automated tests and continuous integration are not yet documented.
- Source organisation is being improved without changing the existing coding style unnecessarily.

## Roadmap

- Clean source-first repository layout
- Remove generated files and historical archives from `main`
- Add sanitized demo data instead of a live database
- Add automated smoke tests
- Add a Windows build workflow
- Improve credential protection and optional database encryption
- Add signed release checksums
- Expand end-user documentation

## Contributing

Bug reports and focused improvements are welcome. Read [CONTRIBUTING.md](CONTRIBUTING.md) before opening a pull request.

For security vulnerabilities, do not open a public issue. Follow [SECURITY.md](SECURITY.md).

## Support

- Website: <https://habitablesolution.com/>
- Issues: <https://github.com/habitablex/service-management-system/issues>
- Releases: <https://github.com/habitablex/service-management-system/releases>

## License

This is a **commercial, source-available project**, not an open-source project unless Habitable Solution publishes a different license for a specific release.

Copyright © Habitable Solution. All rights reserved. See [LICENSE.md](LICENSE.md).
