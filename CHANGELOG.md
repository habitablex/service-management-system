# Changelog

All notable changes to HS Service Management System are documented here.

The project follows semantic-style version tags where practical.

## [Unreleased]

### Planned

- Repository structure cleanup
- Removal of generated binaries, databases, and historical archives from `main`
- Sanitized demo data
- Automated smoke tests and Windows build validation
- Improved protection for sensitive credential fields

## [3.2.0] - 2026-08-05

### Added

- Startup prompt for restoring the latest available SQLite backup
- Option to browse and restore a database backup from another folder
- Setting to enable or disable the startup restore prompt
- Saved restore status, including the last restore time and source path

### Existing Features

- Customer, device, service-job, work-log, and parts management
- Status, priority, problem-description, and engineer-note tracking
- Invoice and money-receipt preview in the default browser
- Print and Save as PDF support through the browser
- Warranty and reporting tools
- Multiple interface themes
- Automatic backup on application close
- JSON export

### Security Note

Runtime databases and configuration files should not be committed to the public repository. Existing tracked database files should be reviewed and removed from Git history when necessary.

## Earlier Versions

Versions 2.0 through 3.1 were development milestones. Historical binary/source archives should be preserved as GitHub Release assets rather than files in the default branch.
