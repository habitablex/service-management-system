# HS Service Management System v3.2

HS-SMS v3.2 improves backup recovery and makes it easier to restore business data when the application starts.

## What’s New

- Startup restore prompt
- Automatic detection of the latest backup in the default backup folder
- **Restore Latest Backup** action
- **Browse Backup File** action for selecting another `.db` file
- **Continue Without Restore** action
- Setting to enable or disable the startup restore prompt
- Saved last-restore time and restored-file path

## Included Features

- Customer and device management
- Service-job status and priority tracking
- Problem descriptions, engineer notes, work logs, and parts used
- Payment, invoice, money-receipt, and warranty tracking
- Browser invoice view with Print and Save as PDF
- Reports, JSON export, themes, and configurable service settings
- Local SQLite backup and restore

## Downloads

Attach release files using clear names, for example:

- `HS-Service-Management-System-v3.2-Windows-x64.zip`
- `HS-Service-Management-System-v3.2-Source.zip`
- `SHA256SUMS.txt`

## Requirements

- Windows 10 or Windows 11 for the packaged desktop build
- Python 3.11+ when running from source

## Important

Back up your existing database before upgrading or restoring data. Do not upload databases containing customer details or credentials to GitHub.

This project is commercial, source-available software. See `LICENSE.md`.
