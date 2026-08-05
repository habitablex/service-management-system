HS Service Management System v3.2
Commercial Offline Desktop Edition
By Habitable Solution
Website: habitablesolution.com/download

WHAT THIS PACKAGE IS
This is a VS Code editable Python + SQLite offline service management system.
It is designed for computer/laptop/UPS/printer/GPU/networking/CCTV service businesses.

NEW IN v3.2
- Startup restore prompt added.
- When the app opens, it checks the default backup folder.
- If a SQLite backup is found, it asks whether to restore the latest backup.
- Startup restore dialog includes Restore Latest Backup, Browse Backup File, and Continue Without Restore.
- User can browse and restore any .db backup file from another folder.
- Backup tab includes an enable/disable checkbox: Ask to restore or browse backup when the app opens.
- Restore status is saved with last restore date/time and restored file path.

INCLUDED FROM PREVIOUS VERSIONS
- Top bar title: Service Management System (SMS)
- Theme option in Settings
- Themes included: Default Theme, Light, Dark, Dark Pro, Midnight Dark, Graphite Dark, Glass, iMac, Ubuntu, Blue, Green, Gold
- Bottom branding/footer
- Custom icon support via assets/hs_sms_icon.ico and assets/hs_sms_icon.png
- Invoice Open button that opens a clean browser invoice with Print / Save PDF
- Backup section with last backup date/time and last restore date/time
- Open Backup Folder button
- Default backup folder inside Documents > Habitable Solution > HS Service Management System > backups
- Automatic backup on app close with success confirmation

IMPORTANT
The real Windows .exe must be built on a Windows computer. This package includes a ready build script.
After build, your final file will be:
dist\HS_Service_Management_System_v3_2.exe

HOW TO RUN SOURCE IN VS CODE
1. Install Python 3.11+ from python.org.
2. Open this folder in VS Code.
3. Open Terminal.
4. Run:
   python HS_Service_Management_System_v2.py

HOW TO BUILD WINDOWS EXE
1. Open this folder on a Windows PC.
2. Double-click build_windows_exe.bat or run it from Command Prompt.
3. Wait until build completes.
4. Find the EXE inside dist folder:
   dist\HS_Service_Management_System_v3_2.exe

DATABASE
The app stores data in:
data\hs_sms_v2.db

CONFIG
The app stores theme and backup/restore status in:
data\hs_sms_config.json

BACKUP RULE
Backups are saved by default in:
Documents > Habitable Solution > HS Service Management System > backups

MODULES INCLUDED
- Dashboard
- Customer Management
- Device Management
- Service Jobs
- Status Tracking
- Priority
- Problem Description
- Engineer Notes
- Work Logs
- Parts Used
- Invoice / Money Receipt Preview
- Invoice Open in Browser with Print / Save PDF
- Warranty Tracking
- Reports
- Theme Options
- Service Types Settings
- Device Category Settings
- SQLite Backup / Restore
- JSON Export
- About / Branding

CLIENT DELIVERY SUGGESTION
After building the EXE, deliver:
1. HS_Service_Management_System_v3_2.exe
2. README_CLIENT.txt

Do not deliver the Python source file to normal clients unless they paid for source code.


v3.2 Update:
- On app startup, the software can ask whether the latest backup should be restored.
- Backup tab includes a setting to enable/disable the startup restore prompt.
