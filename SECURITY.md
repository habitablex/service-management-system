# Security Policy

## Supported Version

Security fixes are currently considered for the latest published version only.

| Version | Supported |
|---|---|
| 3.2.x | Yes |
| 3.1 and older | No |

## Reporting a Vulnerability

Do not disclose a suspected vulnerability in a public GitHub issue.

Send a private report through the official contact channel listed on <https://habitablesolution.com/>. Include:

- affected version;
- operating system;
- clear reproduction steps;
- expected and actual behaviour;
- screenshots or a minimal proof of concept when appropriate;
- possible impact;
- whether the issue is already public.

Do not include real customer records, device passwords, database files, API keys, or other confidential information.

## Response Process

Habitable Solution will attempt to:

1. acknowledge a valid report;
2. reproduce and assess the issue;
3. prepare a fix or mitigation;
4. publish an updated release when appropriate;
5. credit the reporter when permission is provided.

No guaranteed response or resolution time is promised.

## Sensitive Local Data

HS-SMS stores business data in a local SQLite database. The current schema may contain customer contact details, device identifiers, operational notes, device passwords, and BIOS passwords.

Therefore:

- never commit a populated database to Git;
- never upload customer backups to a public release;
- avoid storing real passwords unless suitable encryption and access controls have been implemented;
- restrict operating-system access to the application folder and backups;
- use full-disk encryption on computers that contain customer data;
- securely erase exported or retired database copies;
- review local privacy and data-protection obligations before production use.

## Release Safety

Official executable files should be distributed only through this repository's Releases page or the official Habitable Solution website. Release assets should include a SHA-256 checksum. Users should verify the download source and scan executable files before running them.

## Out of Scope

The following are not normally treated as vulnerabilities:

- issues affecting unsupported versions;
- attacks requiring unrestricted physical access to an already unlocked computer;
- social engineering without a software defect;
- reports that expose real third-party or customer data;
- automated scan results without a reproducible security impact.
