"""
HS Service Management System (HS-SMS)
Commercial Offline Desktop Edition

Technology: Python 3 + Tkinter + SQLite
Run: python HS_Service_Management_System_v2.py
Database: hs_sms.db will be created in the same folder.

Editable in VS Code.
"""

import os
import sys
import sqlite3
import json
import shutil
import html
import webbrowser
from pathlib import Path
from datetime import datetime, timedelta
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

def get_app_dir():
    """Return the folder where the source file or compiled EXE is located."""
    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))


BASE_DIR = get_app_dir()
APP_NAME = "HS Service Management System v3.2"
APP_TITLE = "Service Management System (SMS)"
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
PACKAGED_ASSETS_DIR = os.path.join(getattr(sys, "_MEIPASS", BASE_DIR), "assets")


def asset_path(filename):
    """Prefer an editable external asset, then fall back to bundled PyInstaller asset."""
    external = os.path.join(ASSETS_DIR, filename)
    if os.path.exists(external):
        return external
    return os.path.join(PACKAGED_ASSETS_DIR, filename)


APP_ICON_ICO = asset_path("hs_sms_icon.ico")
APP_ICON_PNG = asset_path("hs_sms_icon.png")
DB_FILE = os.path.join(BASE_DIR, "data", "hs_sms_v2.db")
CONFIG_FILE = os.path.join(BASE_DIR, "data", "hs_sms_config.json")
INVOICE_DIR = os.path.join(BASE_DIR, "invoices")


def get_default_backup_dir():
    """Return the preferred backup folder inside the user's Documents folder."""
    documents = Path.home() / "Documents"
    if documents.exists():
        return str(documents / "Habitable Solution" / "HS Service Management System" / "backups")
    return os.path.join(BASE_DIR, "backups")


BACKUP_DIR = get_default_backup_dir()
DATE_FMT = "%Y-%m-%d %H:%M:%S"
APP_VERSION = "3.2.0"
COMPANY_NAME = "Habitable Solution"
COMPANY_WEBSITE = "habitablesolution.com"
DOWNLOAD_PAGE = "habitablesolution.com/download"
FOOTER_BRANDING = f"{APP_TITLE} | Developed by {COMPANY_NAME} | {DOWNLOAD_PAGE}"

THEME_DISPLAY_ORDER = [
    "Default Theme",
    "Light",
    "Dark",
    "Dark Pro",
    "Midnight Dark",
    "Graphite Dark",
    "Glass",
    "iMac",
    "Ubuntu",
    "Blue",
    "Green",
    "Gold",
]

THEMES = {
    "Light": {
        "bg": "#f7f9fc",
        "surface": "#ffffff",
        "text": "#111827",
        "muted": "#475569",
        "accent": "#2563eb",
        "accent_text": "#ffffff",
        "tree": "#ffffff",
        "tree_alt": "#f8fafc",
        "border": "#dbe3ef",
    },
    "Dark": {
        "bg": "#0f172a",
        "surface": "#111827",
        "text": "#f8fafc",
        "muted": "#cbd5e1",
        "accent": "#38bdf8",
        "accent_text": "#020617",
        "tree": "#1e293b",
        "tree_alt": "#111827",
        "border": "#334155",
    },
    "Dark Pro": {
        "bg": "#09090b",
        "surface": "#18181b",
        "text": "#fafafa",
        "muted": "#a1a1aa",
        "accent": "#8b5cf6",
        "accent_text": "#ffffff",
        "tree": "#18181b",
        "tree_alt": "#27272a",
        "border": "#3f3f46",
    },
    "Midnight Dark": {
        "bg": "#020617",
        "surface": "#0f172a",
        "text": "#e0f2fe",
        "muted": "#93c5fd",
        "accent": "#0ea5e9",
        "accent_text": "#00111d",
        "tree": "#0b1220",
        "tree_alt": "#111827",
        "border": "#1e3a8a",
    },
    "Graphite Dark": {
        "bg": "#171717",
        "surface": "#262626",
        "text": "#f5f5f5",
        "muted": "#d4d4d4",
        "accent": "#737373",
        "accent_text": "#ffffff",
        "tree": "#262626",
        "tree_alt": "#1f1f1f",
        "border": "#525252",
    },
    "Glass": {
        "bg": "#eef6ff",
        "surface": "#ffffff",
        "text": "#0f172a",
        "muted": "#64748b",
        "accent": "#67e8f9",
        "accent_text": "#083344",
        "tree": "#ffffff",
        "tree_alt": "#ecfeff",
        "border": "#a5f3fc",
    },
    "iMac": {
        "bg": "#f5f5f7",
        "surface": "#ffffff",
        "text": "#1d1d1f",
        "muted": "#6e6e73",
        "accent": "#007aff",
        "accent_text": "#ffffff",
        "tree": "#ffffff",
        "tree_alt": "#f2f2f7",
        "border": "#d2d2d7",
    },
    "Ubuntu": {
        "bg": "#2c001e",
        "surface": "#3b0a2a",
        "text": "#fff7ed",
        "muted": "#fed7aa",
        "accent": "#e95420",
        "accent_text": "#ffffff",
        "tree": "#3b0a2a",
        "tree_alt": "#4a1234",
        "border": "#77216f",
    },
    "Blue": {
        "bg": "#eff6ff",
        "surface": "#ffffff",
        "text": "#0f172a",
        "muted": "#475569",
        "accent": "#1d4ed8",
        "accent_text": "#ffffff",
        "tree": "#ffffff",
        "tree_alt": "#dbeafe",
        "border": "#bfdbfe",
    },
    "Green": {
        "bg": "#ecfdf5",
        "surface": "#ffffff",
        "text": "#064e3b",
        "muted": "#047857",
        "accent": "#059669",
        "accent_text": "#ffffff",
        "tree": "#ffffff",
        "tree_alt": "#d1fae5",
        "border": "#a7f3d0",
    },
    "Gold": {
        "bg": "#fffbeb",
        "surface": "#ffffff",
        "text": "#422006",
        "muted": "#92400e",
        "accent": "#d97706",
        "accent_text": "#ffffff",
        "tree": "#ffffff",
        "tree_alt": "#fef3c7",
        "border": "#fde68a",
    },
}
DEFAULT_THEME = "Default Theme"
FALLBACK_THEME = "Light"


def detect_system_theme():
    """Return Light or Dark based on the operating system preference when possible."""
    try:
        if sys.platform.startswith("win"):
            import winreg
            key_path = r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize"
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path) as key:
                value, _ = winreg.QueryValueEx(key, "AppsUseLightTheme")
                return "Light" if int(value) == 1 else "Dark"
        if sys.platform == "darwin":
            import subprocess
            result = subprocess.run(
                ["defaults", "read", "-g", "AppleInterfaceStyle"],
                capture_output=True,
                text=True,
                timeout=2,
            )
            return "Dark" if "Dark" in result.stdout else "Light"
    except Exception:
        pass
    return FALLBACK_THEME


def resolve_theme(theme_name):
    if theme_name == "Default Theme":
        return detect_system_theme()
    if theme_name in THEMES:
        return theme_name
    return FALLBACK_THEME

# Portable data directory for commercial/offline deployment
os.makedirs(os.path.join(BASE_DIR, "data"), exist_ok=True)
os.makedirs(os.path.join(BASE_DIR, "backups"), exist_ok=True)
os.makedirs(ASSETS_DIR, exist_ok=True)
os.makedirs(BACKUP_DIR, exist_ok=True)
os.makedirs(INVOICE_DIR, exist_ok=True)

STATUSES = [
    "Received",
    "Inspection",
    "Waiting Parts",
    "Under Repair",
    "Testing",
    "Ready",
    "Delivered",
    "Cancelled",
]

PRIORITIES = ["Low", "Medium", "High", "Emergency"]

DEFAULT_DEVICE_CATEGORIES = [
    "Laptop", "Desktop", "All-in-One", "Server", "UPS", "Printer", "Monitor",
    "GPU", "Motherboard", "SSD", "HDD", "Router", "Switch", "CCTV DVR",
    "MacBook", "iMac", "Custom Device"
]

DEFAULT_SERVICE_TYPES = [
    "Computer Service", "Laptop Service", "Desktop Service", "Gaming PC", "MacBook Service",
    "Printer Service", "UPS Service", "GPU Service", "Motherboard Repair",
    "BIOS Programming", "Chip Level Repair", "Data Recovery", "SSD Upgrade",
    "RAM Upgrade", "Windows Install", "Virus Removal", "Networking", "CCTV",
    "AMC Support", "On-site Service", "Remote Support", "Custom Service"
]


def now_text():
    return datetime.now().strftime(DATE_FMT)


def money(value):
    try:
        return f"{float(value):,.2f}"
    except Exception:
        return "0.00"


def default_config():
    return {
        "theme": DEFAULT_THEME,
        "last_backup_at": "Never",
        "last_backup_path": "",
        "last_restore_at": "Never",
        "last_restore_path": "",
        "ask_restore_on_startup": True,
    }


def load_config():
    if not os.path.exists(CONFIG_FILE):
        return default_config()
    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        defaults = default_config()
        for key, value in defaults.items():
            data.setdefault(key, value)
        if data.get("theme") not in THEME_DISPLAY_ORDER:
            data["theme"] = DEFAULT_THEME
        data["ask_restore_on_startup"] = bool(data.get("ask_restore_on_startup", True))
        return data
    except Exception:
        return default_config()


def save_config(config):
    os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=2)


class Database:
    def __init__(self, db_path=DB_FILE):
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        self.conn.execute("PRAGMA foreign_keys = ON")
        self.create_tables()
        self.seed_defaults()

    def create_tables(self):
        cur = self.conn.cursor()

        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_code TEXT UNIQUE,
                name TEXT NOT NULL,
                mobile TEXT NOT NULL,
                whatsapp TEXT,
                email TEXT,
                address TEXT,
                company TEXT,
                notes TEXT,
                created_at TEXT NOT NULL
            )
            """
        )

        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS settings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                setting_type TEXT NOT NULL,
                name TEXT NOT NULL,
                is_active INTEGER DEFAULT 1,
                UNIQUE(setting_type, name)
            )
            """
        )

        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS devices (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                device_code TEXT UNIQUE,
                customer_id INTEGER NOT NULL,
                category TEXT NOT NULL,
                brand TEXT,
                model TEXT,
                serial_number TEXT,
                asset_tag TEXT,
                processor TEXT,
                ram TEXT,
                storage TEXT,
                gpu TEXT,
                windows_version TEXT,
                charger_included TEXT,
                bag_included TEXT,
                password TEXT,
                bios_password TEXT,
                accessories TEXT,
                notes TEXT,
                created_at TEXT NOT NULL,
                FOREIGN KEY(customer_id) REFERENCES customers(id) ON DELETE CASCADE
            )
            """
        )

        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS jobs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                job_number TEXT UNIQUE,
                customer_id INTEGER NOT NULL,
                device_id INTEGER NOT NULL,
                service_type TEXT,
                priority TEXT DEFAULT 'Medium',
                status TEXT DEFAULT 'Received',
                problem_description TEXT,
                engineer_notes TEXT,
                estimated_amount REAL DEFAULT 0,
                final_amount REAL DEFAULT 0,
                paid_amount REAL DEFAULT 0,
                discount_amount REAL DEFAULT 0,
                vat_amount REAL DEFAULT 0,
                warranty_days INTEGER DEFAULT 0,
                warranty_end_date TEXT,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                delivered_at TEXT,
                FOREIGN KEY(customer_id) REFERENCES customers(id) ON DELETE CASCADE,
                FOREIGN KEY(device_id) REFERENCES devices(id) ON DELETE CASCADE
            )
            """
        )

        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS work_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                job_id INTEGER NOT NULL,
                log_time TEXT NOT NULL,
                note TEXT NOT NULL,
                created_at TEXT NOT NULL,
                FOREIGN KEY(job_id) REFERENCES jobs(id) ON DELETE CASCADE
            )
            """
        )

        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS job_parts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                job_id INTEGER NOT NULL,
                part_name TEXT NOT NULL,
                quantity REAL DEFAULT 1,
                cost_price REAL DEFAULT 0,
                sale_price REAL DEFAULT 0,
                warranty_days INTEGER DEFAULT 0,
                created_at TEXT NOT NULL,
                FOREIGN KEY(job_id) REFERENCES jobs(id) ON DELETE CASCADE
            )
            """
        )

        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS activity_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                activity_type TEXT NOT NULL,
                description TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )

        self.conn.commit()

    def seed_defaults(self):
        for category in DEFAULT_DEVICE_CATEGORIES:
            self.execute(
                "INSERT OR IGNORE INTO settings(setting_type, name, is_active) VALUES(?, ?, 1)",
                ("device_category", category),
            )
        for service in DEFAULT_SERVICE_TYPES:
            self.execute(
                "INSERT OR IGNORE INTO settings(setting_type, name, is_active) VALUES(?, ?, 1)",
                ("service_type", service),
            )
        self.conn.commit()

    def execute(self, sql, params=()):
        cur = self.conn.cursor()
        cur.execute(sql, params)
        self.conn.commit()
        return cur

    def fetchall(self, sql, params=()):
        cur = self.conn.cursor()
        cur.execute(sql, params)
        return cur.fetchall()

    def fetchone(self, sql, params=()):
        cur = self.conn.cursor()
        cur.execute(sql, params)
        return cur.fetchone()

    def log_activity(self, activity_type, description):
        self.execute(
            "INSERT INTO activity_logs(activity_type, description, created_at) VALUES(?, ?, ?)",
            (activity_type, description, now_text()),
        )


class HSSMSApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(APP_NAME)
        self.geometry("1220x720")
        self.minsize(1040, 620)
        self.set_app_icon()
        self.db = Database()
        self.config_data = load_config()
        self.current_theme = self.config_data.get("theme", DEFAULT_THEME)
        self.customer_map = {}
        self.device_map = {}
        self.job_map = {}
        self.selected_customer_id = None
        self.selected_device_id = None
        self.selected_job_id = None

        self.style = ttk.Style(self)
        try:
            self.style.theme_use("clam")
        except Exception:
            pass
        self.apply_theme(self.current_theme, save=False)

        self.create_ui()
        self.refresh_all()
        self.apply_theme(self.current_theme, save=False)

        # v2.5: Create an automatic backup every time the app is closed.
        # v2.6: Compact UI spacing and typography without changing any core features.
        # v2.7: Ask on startup whether a backup should be restored, with latest-backup and browse options.
        # v3.2: Recreated professional sidebar/topbar dashboard UI with fixed dark card styling.
        self.protocol("WM_DELETE_WINDOW", self.on_app_close)
        self.after(650, self.ask_restore_latest_backup_on_startup)

    def set_app_icon(self):
        """Apply the custom app icon in the title bar/taskbar when icon files exist."""
        try:
            if os.path.exists(APP_ICON_ICO):
                self.iconbitmap(APP_ICON_ICO)
        except Exception:
            pass
        try:
            if os.path.exists(APP_ICON_PNG):
                self._app_icon_image = tk.PhotoImage(file=APP_ICON_PNG)
                self.iconphoto(True, self._app_icon_image)
        except Exception:
            pass

    def center_child_window(self, window, width, height):
        """Center a child dialog over the main app window."""
        try:
            self.update_idletasks()
            parent_x = self.winfo_x()
            parent_y = self.winfo_y()
            parent_w = self.winfo_width()
            parent_h = self.winfo_height()
            x = parent_x + max((parent_w - width) // 2, 0)
            y = parent_y + max((parent_h - height) // 2, 0)
            window.geometry(f"{width}x{height}+{x}+{y}")
        except Exception:
            window.geometry(f"{width}x{height}")

    def find_latest_sqlite_backup(self):
        """Return the newest SQLite backup file from the Documents backup folder."""
        if not os.path.isdir(BACKUP_DIR):
            return None
        backup_files = []
        for name in os.listdir(BACKUP_DIR):
            if not name.lower().endswith(".db"):
                continue
            path = os.path.join(BACKUP_DIR, name)
            if os.path.abspath(path) == os.path.abspath(DB_FILE):
                continue
            try:
                backup_time = max(os.path.getmtime(path), os.path.getctime(path))
                backup_files.append((backup_time, path))
            except OSError:
                continue
        if not backup_files:
            return None
        backup_files.sort(reverse=True)
        return backup_files[0][1]

    def restore_database_from_path(self, backup_path, show_message=True):
        """Restore database from a selected backup path, then refresh the app safely."""
        if not backup_path or not os.path.exists(backup_path):
            if show_message:
                messagebox.showerror("Restore Failed", "Backup file not found.")
            return False
        try:
            try:
                self.db.conn.close()
            except Exception:
                pass
            os.makedirs(os.path.dirname(DB_FILE), exist_ok=True)
            shutil.copy2(backup_path, DB_FILE)
            self.db = Database(DB_FILE)
            self.remember_backup_event("restore", backup_path)
            self.refresh_all()
            if show_message:
                messagebox.showinfo("Restore Complete", f"Latest backup restored successfully.\n\nRestored from:\n{backup_path}")
            return True
        except Exception as exc:
            try:
                self.db = Database(DB_FILE)
            except Exception:
                pass
            if show_message:
                messagebox.showerror("Restore Failed", f"Backup could not be restored.\n\nError:\n{exc}")
            return False

    def ask_restore_latest_backup_on_startup(self):
        """Ask the user on app startup whether to restore the latest or a browsed backup."""
        if not self.config_data.get("ask_restore_on_startup", True):
            return

        latest_backup = self.find_latest_sqlite_backup()
        latest_time = "No backup found in the default backup folder"
        latest_file = "-"
        if latest_backup:
            latest_time = datetime.fromtimestamp(
                max(os.path.getmtime(latest_backup), os.path.getctime(latest_backup))
            ).strftime(DATE_FMT)
            latest_file = latest_backup

        dialog = tk.Toplevel(self)
        dialog.title("Startup Backup Restore")
        dialog.transient(self)
        dialog.grab_set()
        dialog.resizable(False, False)
        dialog.geometry("680x330")
        self.center_child_window(dialog, 680, 330)

        wrapper = ttk.Frame(dialog, padding=16)
        wrapper.pack(fill="both", expand=True)

        ttk.Label(
            wrapper,
            text="Restore Backup Before Opening?",
            style="Section.TLabel",
        ).pack(anchor="w")

        info_text = (
            "The app found your backup restore setting is enabled. "
            "You can restore the latest automatic backup, browse another backup file, "
            "or continue without restoring."
        )
        ttk.Label(wrapper, text=info_text, wraplength=630).pack(anchor="w", pady=(8, 10))

        latest_box = ttk.LabelFrame(wrapper, text="Latest Backup", padding=10)
        latest_box.pack(fill="x", pady=(0, 12))

        ttk.Label(latest_box, text=f"Backup date/time: {latest_time}").pack(anchor="w", pady=2)
        ttk.Label(latest_box, text=f"Backup file: {latest_file}", wraplength=610).pack(anchor="w", pady=2)

        dont_ask_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(
            wrapper,
            text="Do not ask again on startup",
            variable=dont_ask_var,
        ).pack(anchor="w", pady=(0, 12))

        button_row = ttk.Frame(wrapper)
        button_row.pack(fill="x", pady=(6, 0))

        def save_dont_ask_choice():
            if dont_ask_var.get():
                self.config_data["ask_restore_on_startup"] = False
                save_config(self.config_data)
                if hasattr(self, "ask_restore_startup_var"):
                    self.ask_restore_startup_var.set(False)

        def continue_without_restore():
            save_dont_ask_choice()
            dialog.destroy()

        def restore_latest():
            if not latest_backup or not os.path.exists(latest_backup):
                messagebox.showwarning("No Backup Found", "No latest backup file was found in the default backup folder.", parent=dialog)
                return
            save_dont_ask_choice()
            dialog.destroy()
            self.restore_database_from_path(latest_backup, show_message=True)

        def browse_and_restore():
            initial_dir = BACKUP_DIR if os.path.isdir(BACKUP_DIR) else BASE_DIR
            selected_path = filedialog.askopenfilename(
                parent=dialog,
                title="Select Backup Database File",
                initialdir=initial_dir,
                filetypes=[
                    ("SQLite Database Backup", "*.db"),
                    ("All Files", "*.*"),
                ],
            )
            if not selected_path:
                return
            save_dont_ask_choice()
            dialog.destroy()
            self.restore_database_from_path(selected_path, show_message=True)

        restore_btn = ttk.Button(button_row, text="Restore Latest Backup", command=restore_latest)
        restore_btn.pack(side="left", padx=(0, 8))
        if not latest_backup:
            restore_btn.state(["disabled"])

        ttk.Button(button_row, text="Browse Backup File", command=browse_and_restore).pack(side="left", padx=8)
        ttk.Button(button_row, text="Continue Without Restore", command=continue_without_restore).pack(side="right")

        dialog.protocol("WM_DELETE_WINDOW", continue_without_restore)
        dialog.focus_force()

    def create_auto_close_backup(self):
        """Save a no-click safety backup to the Documents backup folder before app exit."""
        if not os.path.exists(DB_FILE):
            return None
        os.makedirs(BACKUP_DIR, exist_ok=True)
        backup_name = f"hs_sms_auto_close_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
        backup_path = os.path.join(BACKUP_DIR, backup_name)
        self.db.conn.commit()
        shutil.copy2(DB_FILE, backup_path)
        self.remember_backup_event("backup", backup_path)
        return backup_path

    def on_app_close(self):
        """Run automatic backup on close and show confirmation before exiting."""
        try:
            backup_path = self.create_auto_close_backup()
            if backup_path:
                messagebox.showinfo(
                    "Data Backup Successfully",
                    f"Data backup successfully saved before closing.\n\nBackup file:\n{backup_path}",
                )
            else:
                messagebox.showinfo(
                    "Data Backup",
                    "No database file found yet. The app will close now.",
                )
            try:
                self.db.conn.close()
            except Exception:
                pass
            self.destroy()
        except Exception as exc:
            should_close = messagebox.askyesno(
                "Backup Failed",
                f"Automatic backup could not be completed.\n\nError:\n{exc}\n\nDo you still want to close the app?",
            )
            if should_close:
                try:
                    self.db.conn.close()
                except Exception:
                    pass
                self.destroy()

    # ------------------------ UI HELPERS ------------------------
    def apply_theme(self, theme_name, save=True):
        if theme_name not in THEME_DISPLAY_ORDER:
            theme_name = DEFAULT_THEME
        self.current_theme = theme_name
        effective_theme = resolve_theme(theme_name)
        palette = dict(THEMES[effective_theme])

        # v3.2 polished application palette layer.
        # This keeps the existing theme engine but removes the flat/white patchy look.
        dark_like = effective_theme in {"Dark", "Dark Pro", "Midnight Dark", "Graphite Dark", "Ubuntu"}
        if dark_like:
            palette.update({
                "bg": "#0b1220",
                "surface": "#111827",
                "tree": "#1f2937",
                "tree_alt": "#273449",
                "border": "#2f4058",
                "text": "#f8fafc",
                "muted": "#94a3b8",
                "accent": "#38bdf8",
                "accent_text": "#06121f",
            })
            palette["sidebar_bg"] = "#0f172a"
            palette["topbar_bg"] = "#101a2b"
            palette["footer_bg"] = "#0f172a"
            palette["panel_bg"] = "#141f31"
            palette["card_bg"] = "#162235"
            palette["card_head_bg"] = "#162235"
            palette["sidebar_hover_bg"] = "#1e293b"
            palette["sidebar_active_bg"] = "#38bdf8"
            palette["sidebar_active_fg"] = "#06121f"
        else:
            palette["sidebar_bg"] = "#0f172a"
            palette["topbar_bg"] = palette["surface"]
            palette["footer_bg"] = palette["surface"]
            palette["panel_bg"] = palette["surface"]
            palette["card_bg"] = palette["surface"]
            palette["card_head_bg"] = palette["surface"]
            palette["sidebar_hover_bg"] = "#1e293b"
            palette["sidebar_active_bg"] = palette["accent"]
            palette["sidebar_active_fg"] = palette["accent_text"]

        palette["sidebar_fg"] = "#e5e7eb"
        palette["page_bg"] = palette["bg"]
        palette["soft_text"] = palette["muted"]
        self.palette = palette

        if save:
            self.config_data["theme"] = theme_name
            save_config(self.config_data)

        self.configure(bg=palette["bg"])
        self.style.configure("TFrame", background=palette["bg"])
        self.style.configure("Page.TFrame", background=palette["bg"])
        self.style.configure("Content.TFrame", background=palette["surface"])
        self.style.configure("Header.TFrame", background=palette["topbar_bg"])
        self.style.configure("Footer.TFrame", background=palette["footer_bg"])
        self.style.configure("TLabelframe", background=palette["bg"], bordercolor=palette["border"])
        self.style.configure("TLabelframe.Label", background=palette["bg"], foreground=palette["text"], font=("Segoe UI", 9, "bold"))
        self.style.configure("TLabel", background=palette["bg"], foreground=palette["text"], font=("Segoe UI", 9))
        self.style.configure("Surface.TLabel", background=palette["surface"], foreground=palette["text"], font=("Segoe UI", 9))
        self.style.configure("Header.TLabel", background=palette["topbar_bg"], foreground=palette["text"], font=("Segoe UI", 17, "bold"))
        self.style.configure("HeaderSub.TLabel", background=palette["topbar_bg"], foreground=palette["muted"], font=("Segoe UI", 9))
        self.style.configure("Footer.TLabel", background=palette["footer_bg"], foreground=palette["muted"], font=("Segoe UI", 8))
        self.style.configure("Heading.TLabel", background=palette["bg"], foreground=palette["text"], font=("Segoe UI", 13, "bold"))
        self.style.configure("Card.TLabel", background=palette["surface"], foreground=palette["text"], font=("Segoe UI", 11, "bold"), padding=6)
        self.style.configure("TButton", padding=(7, 4), font=("Segoe UI", 9))
        self.style.configure("Accent.TButton", padding=(7, 4), font=("Segoe UI", 9, "bold"))
        self.style.configure("Treeview", rowheight=26, background=palette["tree"], fieldbackground=palette["tree"], foreground=palette["text"], bordercolor=palette["border"], font=("Segoe UI", 9))
        self.style.configure("Treeview.Heading", background=palette["accent"], foreground=palette["accent_text"], font=("Segoe UI", 9, "bold"))
        self.style.map("Treeview", background=[("selected", palette["accent"])], foreground=[("selected", palette["accent_text"])])
        self.style.configure("TEntry", fieldbackground=palette["surface"], foreground=palette["text"], padding=(4, 3))
        self.style.configure("TCombobox", fieldbackground=palette["surface"], foreground=palette["text"], padding=(4, 3))

        self._theme_plain_widgets(self, palette)
        self.apply_custom_widget_theme()

    def apply_custom_widget_theme(self):
        palette = getattr(self, "palette", THEMES[FALLBACK_THEME])

        def safe_config(widget, **kwargs):
            try:
                widget.configure(**kwargs)
            except Exception:
                pass

        # Root custom containers
        for attr in ["body_frame", "content_shell", "content_frame", "page_stack"]:
            widget = getattr(self, attr, None)
            if widget:
                safe_config(widget, bg=palette["bg"])
        for attr in ["sidebar", "sidebar_header", "brand_wrap", "nav_container"]:
            widget = getattr(self, attr, None)
            if widget:
                safe_config(widget, bg=palette["sidebar_bg"])
        for attr in ["topbar", "topbar_left", "topbar_right"]:
            widget = getattr(self, attr, None)
            if widget:
                safe_config(widget, bg=palette["topbar_bg"], highlightbackground=palette["border"], highlightthickness=0)
        if getattr(self, "footer_frame", None):
            safe_config(self.footer_frame, bg=palette["footer_bg"], highlightbackground=palette["border"], highlightthickness=1)
        if getattr(self, "footer_left_label", None):
            safe_config(self.footer_left_label, bg=palette["footer_bg"], fg=palette["muted"], font=("Segoe UI", 8))
        if getattr(self, "footer_right_label", None):
            safe_config(self.footer_right_label, bg=palette["footer_bg"], fg=palette["muted"], font=("Segoe UI", 8, "bold"))

        if getattr(self, "sidebar_logo_label", None):
            safe_config(self.sidebar_logo_label, bg=palette["sidebar_bg"], fg=palette["accent"], font=("Segoe UI", 17, "bold"))
        if getattr(self, "sidebar_brand_label", None):
            safe_config(self.sidebar_brand_label, bg=palette["sidebar_bg"], fg=palette["text"], font=("Segoe UI", 11, "bold"), justify="left")
        if getattr(self, "page_title_label", None):
            safe_config(self.page_title_label, bg=palette["topbar_bg"], fg=palette["text"], font=("Segoe UI", 17, "bold"))
        if getattr(self, "page_subtitle_label", None):
            safe_config(self.page_subtitle_label, bg=palette["topbar_bg"], fg=palette["muted"], font=("Segoe UI", 9))

        if getattr(self, "collapse_btn", None):
            safe_config(self.collapse_btn, bg=palette["sidebar_bg"], fg=palette["sidebar_fg"], activebackground=palette["sidebar_hover_bg"], activeforeground=palette["sidebar_fg"], relief="flat", bd=0, font=("Segoe UI Symbol", 13, "bold"), padx=6, pady=4)
        for attr in ["refresh_button", "user_button"]:
            btn = getattr(self, attr, None)
            if btn:
                safe_config(btn, bg=palette["topbar_bg"], fg=palette["text"], activebackground=palette["sidebar_hover_bg"], activeforeground=palette["text"], relief="flat", bd=0, font=("Segoe UI Symbol", 12), padx=10, pady=6)

        for key, meta in getattr(self, "nav_buttons", {}).items():
            btn = meta["button"]
            is_active = getattr(self, "current_page_key", None) == key
            bg = palette["sidebar_active_bg"] if is_active else palette["sidebar_bg"]
            fg = palette["sidebar_active_fg"] if is_active else palette["sidebar_fg"]
            safe_config(
                btn,
                bg=bg,
                fg=fg,
                activebackground=palette["sidebar_hover_bg"] if not is_active else palette["sidebar_active_bg"],
                activeforeground=fg,
                highlightbackground=palette["sidebar_bg"],
                highlightthickness=0,
                relief="flat",
                bd=0,
                font=("Segoe UI", 10, "bold" if is_active else "normal"),
                padx=14,
                pady=11,
            )

        for key, meta in getattr(self, "dashboard_card_widgets", {}).items():
            card_bg = palette.get("card_bg", palette["panel_bg"])
            safe_config(meta["frame"], bg=card_bg, highlightbackground=palette["border"], highlightthickness=1, bd=0)
            safe_config(meta.get("head"), bg=card_bg)
            safe_config(meta["icon"], bg=card_bg, fg=palette["accent"], font=("Segoe UI Emoji", 19))
            safe_config(meta["title"], bg=card_bg, fg=palette["muted"], font=("Segoe UI", 10, "bold"))
            safe_config(meta["value"], bg=card_bg, fg=palette["text"], font=("Segoe UI", 20, "bold"))

        for attr in ["dashboard_outer", "dashboard_cards", "recent_jobs_wrap"]:
            widget = getattr(self, attr, None)
            if widget:
                safe_config(widget, bg=palette["bg"])
        if getattr(self, "recent_jobs_title", None):
            safe_config(self.recent_jobs_title, bg=palette["bg"], fg=palette["text"], font=("Segoe UI", 13, "bold"))

    def _theme_plain_widgets(self, parent, palette):
        for child in parent.winfo_children():
            if isinstance(child, tk.Text):
                child.configure(
                    bg=palette["surface"],
                    fg=palette["text"],
                    insertbackground=palette["text"],
                    selectbackground=palette["accent"],
                    selectforeground=palette["accent_text"],
                    relief="solid",
                    bd=1,
                    highlightthickness=1,
                    highlightbackground=palette["border"],
                )
            try:
                self._theme_plain_widgets(child, palette)
            except Exception:
                pass

    def change_theme(self, event=None):
        theme_name = self.theme_var.get() if hasattr(self, "theme_var") else self.current_theme
        self.apply_theme(theme_name, save=True)
        if hasattr(self, "footer_branding_var"):
            self.footer_branding_var.set(FOOTER_BRANDING + f" | Theme: {theme_name} ({resolve_theme(theme_name)})")

    def toggle_sidebar(self):
        self.sidebar_expanded = not self.sidebar_expanded
        self.sidebar.configure(width=245 if self.sidebar_expanded else 82)
        self.sidebar_brand_label.configure(text="HS Service\nManagement" if self.sidebar_expanded else "")
        self.update_sidebar_labels()

    def update_sidebar_labels(self):
        for _, meta in getattr(self, "nav_buttons", {}).items():
            if self.sidebar_expanded:
                meta["button"].configure(text=f"{meta['icon']}  {meta['label']}", anchor="w")
            else:
                meta["button"].configure(text=meta["icon"], anchor="center")
        if getattr(self, "collapse_btn", None):
            self.collapse_btn.configure(text="☰")

    def show_page(self, page_key):
        if page_key not in self.pages:
            return
        self.current_page_key = page_key
        self.pages[page_key].tkraise()
        page_title = self.page_titles.get(page_key, APP_TITLE)
        self.page_title_var.set(APP_TITLE)
        self.page_subtitle_var.set(f"{page_title} • {COMPANY_NAME} • Version {APP_VERSION}")
        self.apply_custom_widget_theme()

    def open_user_profile(self):
        self.show_page("about")

    def create_ui(self):
        self.nav_buttons = {}
        self.pages = {}
        self.page_titles = {
            "dashboard": "Dashboard",
            "customers": "Customers",
            "devices": "Devices",
            "jobs": "Service Jobs",
            "logs": "Work Logs & Parts",
            "invoice": "Invoice / Warranty",
            "reports": "Reports",
            "settings": "Settings",
            "backup": "Backup",
            "about": "About",
        }
        self.sidebar_expanded = True
        self.current_page_key = "dashboard"

        self.footer_branding_var = tk.StringVar(value=FOOTER_BRANDING + f" | Theme: {self.current_theme} ({resolve_theme(self.current_theme)})")

        self.footer_frame = tk.Frame(self)
        self.footer_frame.pack(side="bottom", fill="x")
        self.footer_left_label = tk.Label(self.footer_frame, textvariable=self.footer_branding_var, anchor="w")
        self.footer_left_label.pack(side="left", padx=10, pady=5)
        self.footer_right_label = tk.Label(self.footer_frame, text="© Habitable Solution")
        self.footer_right_label.pack(side="right", padx=10, pady=5)

        self.body_frame = tk.Frame(self)
        self.body_frame.pack(fill="both", expand=True)

        self.sidebar = tk.Frame(self.body_frame, width=245)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        self.content_shell = tk.Frame(self.body_frame)
        self.content_shell.pack(side="left", fill="both", expand=True)

        self.sidebar_header = tk.Frame(self.sidebar)
        self.sidebar_header.pack(fill="x", padx=10, pady=(12, 8))

        self.brand_wrap = tk.Frame(self.sidebar_header)
        self.brand_wrap.pack(side="left", fill="x", expand=True)
        self.sidebar_logo_label = tk.Label(self.brand_wrap, text="▣ SMS")
        self.sidebar_logo_label.pack(anchor="w")
        self.sidebar_brand_label = tk.Label(self.brand_wrap, text="HS Service\nManagement", justify="left")
        self.sidebar_brand_label.pack(anchor="w", pady=(2, 0))

        self.collapse_btn = tk.Button(self.sidebar_header, text="☰", command=self.toggle_sidebar, cursor="hand2")
        self.collapse_btn.pack(side="right")

        self.nav_container = tk.Frame(self.sidebar)
        self.nav_container.pack(fill="both", expand=True, padx=8, pady=6)

        nav_items = [
            ("dashboard", "🏠", "Dashboard"),
            ("customers", "👥", "Customers"),
            ("devices", "💻", "Devices"),
            ("jobs", "🛠", "Service Jobs"),
            ("logs", "🧩", "Work Logs & Parts"),
            ("invoice", "🧾", "Invoice / Warranty"),
            ("reports", "📊", "Reports"),
            ("settings", "⚙", "Settings"),
            ("backup", "💾", "Backup"),
            ("about", "ⓘ", "About"),
        ]
        for key, icon, label in nav_items:
            btn = tk.Button(self.nav_container, text=f"{icon}  {label}", anchor="w", cursor="hand2", command=lambda k=key: self.show_page(k))
            btn.pack(fill="x", pady=3)
            self.nav_buttons[key] = {"button": btn, "icon": icon, "label": label}

        self.topbar = tk.Frame(self.content_shell)
        self.topbar.pack(fill="x", padx=14, pady=(14, 10))

        self.topbar_left = tk.Frame(self.topbar)
        self.topbar_left.pack(side="left", fill="both", expand=True, padx=16, pady=12)
        self.page_title_var = tk.StringVar(value=APP_TITLE)
        self.page_subtitle_var = tk.StringVar(value=f"Dashboard • {COMPANY_NAME} • Version {APP_VERSION}")
        self.page_title_label = tk.Label(self.topbar_left, textvariable=self.page_title_var, anchor="w")
        self.page_title_label.pack(anchor="w")
        self.page_subtitle_label = tk.Label(self.topbar_left, textvariable=self.page_subtitle_var, anchor="w")
        self.page_subtitle_label.pack(anchor="w", pady=(2, 0))

        self.topbar_right = tk.Frame(self.topbar)
        self.topbar_right.pack(side="right", padx=14, pady=10)
        self.refresh_button = tk.Button(self.topbar_right, text="⟳", command=self.refresh_all, cursor="hand2")
        self.refresh_button.pack(side="right", padx=(8, 0))
        self.user_button = tk.Button(self.topbar_right, text="👤", command=self.open_user_profile, cursor="hand2")
        self.user_button.pack(side="right")

        self.content_frame = tk.Frame(self.content_shell)
        self.content_frame.pack(fill="both", expand=True, padx=14, pady=(0, 12))

        self.page_stack = tk.Frame(self.content_frame)
        self.page_stack.pack(fill="both", expand=True)
        self.page_stack.grid_rowconfigure(0, weight=1)
        self.page_stack.grid_columnconfigure(0, weight=1)

        self.dashboard_tab = ttk.Frame(self.page_stack, style="Page.TFrame")
        self.customers_tab = ttk.Frame(self.page_stack, style="Page.TFrame")
        self.devices_tab = ttk.Frame(self.page_stack, style="Page.TFrame")
        self.jobs_tab = ttk.Frame(self.page_stack, style="Page.TFrame")
        self.logs_tab = ttk.Frame(self.page_stack, style="Page.TFrame")
        self.invoice_tab = ttk.Frame(self.page_stack, style="Page.TFrame")
        self.reports_tab = ttk.Frame(self.page_stack, style="Page.TFrame")
        self.settings_tab = ttk.Frame(self.page_stack, style="Page.TFrame")
        self.backup_tab = ttk.Frame(self.page_stack, style="Page.TFrame")
        self.about_tab = ttk.Frame(self.page_stack, style="Page.TFrame")

        self.pages = {
            "dashboard": self.dashboard_tab,
            "customers": self.customers_tab,
            "devices": self.devices_tab,
            "jobs": self.jobs_tab,
            "logs": self.logs_tab,
            "invoice": self.invoice_tab,
            "reports": self.reports_tab,
            "settings": self.settings_tab,
            "backup": self.backup_tab,
            "about": self.about_tab,
        }
        for frame in self.pages.values():
            frame.grid(row=0, column=0, sticky="nsew")

        self.build_dashboard_tab()
        self.build_customers_tab()
        self.build_devices_tab()
        self.build_jobs_tab()
        self.build_logs_tab()
        self.build_invoice_tab()
        self.build_reports_tab()
        self.build_settings_tab()
        self.build_backup_tab()
        self.build_about_tab()

        self.update_sidebar_labels()
        self.show_page("dashboard")

    def form_row(self, parent, label, row, widget="entry", values=None, width=28):
        ttk.Label(parent, text=label).grid(row=row, column=0, sticky="w", padx=3, pady=2)
        if widget == "combo":
            var = tk.StringVar()
            field = ttk.Combobox(parent, textvariable=var, values=values or [], width=width, state="readonly")
        elif widget == "text":
            field = tk.Text(parent, width=width, height=3)
            var = None
        else:
            var = tk.StringVar()
            field = ttk.Entry(parent, textvariable=var, width=width)
        field.grid(row=row, column=1, sticky="ew", padx=3, pady=2)
        return var, field

    def get_text_value(self, widget):
        return widget.get("1.0", "end").strip()

    def set_text_value(self, widget, value):
        widget.delete("1.0", "end")
        widget.insert("1.0", value or "")

    def safe_float(self, value):
        try:
            return float(value or 0)
        except Exception:
            return 0.0

    def safe_int(self, value):
        try:
            return int(float(value or 0))
        except Exception:
            return 0

    # ------------------------ DATA HELPERS ------------------------
    def get_settings(self, setting_type):
        rows = self.db.fetchall(
            "SELECT name FROM settings WHERE setting_type=? AND is_active=1 ORDER BY name",
            (setting_type,),
        )
        return [r["name"] for r in rows]

    def customer_display(self, row):
        return f"{row['id']} | {row['name']} | {row['mobile']}"

    def device_display(self, row):
        return f"{row['id']} | {row['category']} | {row['brand'] or ''} {row['model'] or ''} | SN:{row['serial_number'] or '-'}"

    def job_display(self, row):
        return f"{row['id']} | {row['job_number']} | {row['status']} | {row['name']} | {row['category']} {row['model'] or ''}"

    def refresh_dropdowns(self):
        customers = self.db.fetchall("SELECT * FROM customers ORDER BY id DESC")
        self.customer_map = {self.customer_display(r): r["id"] for r in customers}

        devices = self.db.fetchall(
            """
            SELECT d.*, c.name AS customer_name
            FROM devices d
            JOIN customers c ON c.id=d.customer_id
            ORDER BY d.id DESC
            """
        )
        self.device_map = {self.device_display(r): r["id"] for r in devices}

        jobs = self.db.fetchall(
            """
            SELECT j.*, c.name, d.category, d.model
            FROM jobs j
            JOIN customers c ON c.id=j.customer_id
            JOIN devices d ON d.id=j.device_id
            ORDER BY j.id DESC
            """
        )
        self.job_map = {self.job_display(r): r["id"] for r in jobs}

        customer_values = list(self.customer_map.keys())
        device_values = list(self.device_map.keys())
        job_values = list(self.job_map.keys())
        categories = self.get_settings("device_category")
        services = self.get_settings("service_type")

        for combo in [getattr(self, "device_customer_combo", None), getattr(self, "job_customer_combo", None)]:
            if combo:
                combo["values"] = customer_values

        for combo in [getattr(self, "job_device_combo", None)]:
            if combo:
                combo["values"] = device_values

        for combo in [getattr(self, "log_job_combo", None), getattr(self, "invoice_job_combo", None)]:
            if combo:
                combo["values"] = job_values

        if hasattr(self, "device_category_combo"):
            self.device_category_combo["values"] = categories
        if hasattr(self, "job_service_combo"):
            self.job_service_combo["values"] = services

    def refresh_all(self):
        self.refresh_dropdowns()
        self.load_dashboard()
        self.load_customers()
        self.load_devices()
        self.load_jobs()
        self.load_logs_and_parts()
        self.load_reports()
        self.load_settings()
        self.refresh_backup_info()

    # ------------------------ DASHBOARD ------------------------
    def build_dashboard_tab(self):
        self.dashboard_outer = tk.Frame(self.dashboard_tab)
        self.dashboard_outer.pack(fill="both", expand=True)

        self.dashboard_cards = tk.Frame(self.dashboard_outer)
        self.dashboard_cards.pack(fill="x", pady=(0, 10))

        self.dashboard_card_widgets = {}
        self.card_vars = {}
        card_meta = [
            ("today_received", "📥", "Today Received"),
            ("ready", "✅", "Ready"),
            ("delivered", "🚚", "Delivered"),
            ("pending", "⏳", "Pending"),
            ("due", "💳", "Due Payment"),
            ("income", "📈", "Monthly Income"),
            ("warranty", "🛡", "Warranty Ending"),
            ("customers", "👥", "Total Customers"),
        ]
        for i, (key, icon, title) in enumerate(card_meta):
            card = tk.Frame(self.dashboard_cards, padx=16, pady=14)
            card.grid(row=i // 4, column=i % 4, padx=7, pady=7, sticky="nsew")
            self.dashboard_cards.grid_columnconfigure(i % 4, weight=1)

            head = tk.Frame(card)
            head.pack(fill="x")
            title_label = tk.Label(head, text=title, anchor="w")
            title_label.pack(side="left", fill="x", expand=True)
            icon_label = tk.Label(head, text=icon, anchor="e")
            icon_label.pack(side="right")

            value_var = tk.StringVar(value="0")
            value_label = tk.Label(card, textvariable=value_var, anchor="w")
            value_label.pack(anchor="w", pady=(18, 0))

            self.card_vars[key] = value_var
            self.dashboard_card_widgets[key] = {
                "frame": card,
                "head": head,
                "icon": icon_label,
                "title": title_label,
                "value": value_label,
            }

        self.recent_jobs_wrap = tk.Frame(self.dashboard_outer)
        self.recent_jobs_wrap.pack(fill="both", expand=True)
        self.recent_jobs_title = tk.Label(self.recent_jobs_wrap, text="Recent Service Jobs", anchor="w")
        self.recent_jobs_title.pack(anchor="w", pady=(0, 8))

        columns = ("job", "customer", "mobile", "device", "status", "priority", "amount")
        self.dashboard_tree = ttk.Treeview(self.recent_jobs_wrap, columns=columns, show="headings", height=13)
        for col in columns:
            self.dashboard_tree.heading(col, text=col.title())
            width = 135
            if col in ("customer", "device"):
                width = 160
            self.dashboard_tree.column(col, width=width)
        self.dashboard_tree.pack(fill="both", expand=True)

    def load_dashboard(self):
        today = datetime.now().strftime("%Y-%m-%d")
        month = datetime.now().strftime("%Y-%m")
        pending_statuses = ("Received", "Inspection", "Waiting Parts", "Under Repair", "Testing")

        today_received = self.db.fetchone("SELECT COUNT(*) AS total FROM jobs WHERE created_at LIKE ?", (today + "%",))["total"]
        ready = self.db.fetchone("SELECT COUNT(*) AS total FROM jobs WHERE status='Ready'")["total"]
        delivered = self.db.fetchone("SELECT COUNT(*) AS total FROM jobs WHERE status='Delivered'")["total"]
        pending = self.db.fetchone(
            f"SELECT COUNT(*) AS total FROM jobs WHERE status IN ({','.join(['?']*len(pending_statuses))})",
            pending_statuses,
        )["total"]
        due = self.db.fetchone("SELECT COALESCE(SUM(final_amount - paid_amount),0) AS total FROM jobs WHERE final_amount > paid_amount")["total"]
        income = self.db.fetchone("SELECT COALESCE(SUM(paid_amount),0) AS total FROM jobs WHERE updated_at LIKE ?", (month + "%",))["total"]
        warranty_limit = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
        warranty = self.db.fetchone(
            "SELECT COUNT(*) AS total FROM jobs WHERE warranty_end_date IS NOT NULL AND warranty_end_date <= ? AND warranty_end_date >= ?",
            (warranty_limit, datetime.now().strftime("%Y-%m-%d")),
        )["total"]
        customers = self.db.fetchone("SELECT COUNT(*) AS total FROM customers")["total"]

        self.card_vars["today_received"].set(str(today_received))
        self.card_vars["ready"].set(str(ready))
        self.card_vars["delivered"].set(str(delivered))
        self.card_vars["pending"].set(str(pending))
        self.card_vars["due"].set("৳ " + money(due))
        self.card_vars["income"].set("৳ " + money(income))
        self.card_vars["warranty"].set(str(warranty))
        self.card_vars["customers"].set(str(customers))

        for row in self.dashboard_tree.get_children():
            self.dashboard_tree.delete(row)

        rows = self.db.fetchall(
            """
            SELECT j.*, c.name, c.mobile, d.category, d.brand, d.model
            FROM jobs j
            JOIN customers c ON c.id=j.customer_id
            JOIN devices d ON d.id=j.device_id
            ORDER BY j.id DESC LIMIT 25
            """
        )
        for r in rows:
            self.dashboard_tree.insert(
                "",
                "end",
                values=(
                    r["job_number"], r["name"], r["mobile"],
                    f"{r['category']} {r['brand'] or ''} {r['model'] or ''}",
                    r["status"], r["priority"], money(r["final_amount"]),
                ),
            )

    # ------------------------ CUSTOMERS ------------------------
    def build_customers_tab(self):
        outer = ttk.Frame(self.customers_tab, padding=8)
        outer.pack(fill="both", expand=True)

        left = ttk.LabelFrame(outer, text="Customer Form", padding=7)
        left.pack(side="left", fill="y", padx=(0, 10))

        self.c_name, _ = self.form_row(left, "Name *", 0)
        self.c_mobile, _ = self.form_row(left, "Mobile *", 1)
        self.c_whatsapp, _ = self.form_row(left, "WhatsApp", 2)
        self.c_email, _ = self.form_row(left, "Email", 3)
        self.c_address, self.c_address_text = self.form_row(left, "Address", 4, widget="text")
        self.c_company, _ = self.form_row(left, "Company", 5)
        self.c_notes, self.c_notes_text = self.form_row(left, "Notes", 6, widget="text")

        btns = ttk.Frame(left)
        btns.grid(row=7, column=0, columnspan=2, sticky="ew", pady=10)
        ttk.Button(btns, text="Add", command=self.add_customer).pack(side="left", padx=3)
        ttk.Button(btns, text="Update", command=self.update_customer).pack(side="left", padx=3)
        ttk.Button(btns, text="Delete", command=self.delete_customer).pack(side="left", padx=3)
        ttk.Button(btns, text="Clear", command=self.clear_customer_form).pack(side="left", padx=3)

        right = ttk.Frame(outer)
        right.pack(side="left", fill="both", expand=True)

        search_frame = ttk.Frame(right)
        search_frame.pack(fill="x")
        self.customer_search = tk.StringVar()
        ttk.Entry(search_frame, textvariable=self.customer_search).pack(side="left", fill="x", expand=True, padx=(0, 6))
        ttk.Button(search_frame, text="Search", command=self.load_customers).pack(side="left")

        columns = ("id", "code", "name", "mobile", "whatsapp", "email", "company")
        self.customers_tree = ttk.Treeview(right, columns=columns, show="headings")
        for col in columns:
            self.customers_tree.heading(col, text=col.title())
            self.customers_tree.column(col, width=120)
        self.customers_tree.pack(fill="both", expand=True, pady=8)
        self.customers_tree.bind("<<TreeviewSelect>>", self.on_customer_select)

    def generate_customer_code(self, customer_id):
        return f"CUST{customer_id:05d}"

    def add_customer(self):
        name = self.c_name.get().strip()
        mobile = self.c_mobile.get().strip()
        if not name or not mobile:
            messagebox.showwarning("Required", "Name and Mobile are required.")
            return
        cur = self.db.execute(
            """
            INSERT INTO customers(name, mobile, whatsapp, email, address, company, notes, created_at)
            VALUES(?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                name, mobile, self.c_whatsapp.get().strip(), self.c_email.get().strip(),
                self.get_text_value(self.c_address_text), self.c_company.get().strip(),
                self.get_text_value(self.c_notes_text), now_text(),
            ),
        )
        customer_id = cur.lastrowid
        self.db.execute("UPDATE customers SET customer_code=? WHERE id=?", (self.generate_customer_code(customer_id), customer_id))
        self.db.log_activity("customer", f"Customer added: {name}")
        self.clear_customer_form()
        self.refresh_all()

    def update_customer(self):
        if not self.selected_customer_id:
            messagebox.showinfo("Select", "Select a customer first.")
            return
        self.db.execute(
            """
            UPDATE customers SET name=?, mobile=?, whatsapp=?, email=?, address=?, company=?, notes=? WHERE id=?
            """,
            (
                self.c_name.get().strip(), self.c_mobile.get().strip(), self.c_whatsapp.get().strip(),
                self.c_email.get().strip(), self.get_text_value(self.c_address_text),
                self.c_company.get().strip(), self.get_text_value(self.c_notes_text), self.selected_customer_id,
            ),
        )
        self.db.log_activity("customer", f"Customer updated: {self.c_name.get().strip()}")
        self.refresh_all()

    def delete_customer(self):
        if not self.selected_customer_id:
            messagebox.showinfo("Select", "Select a customer first.")
            return
        if messagebox.askyesno("Confirm", "Delete selected customer? Related devices and jobs will also be deleted."):
            self.db.execute("DELETE FROM customers WHERE id=?", (self.selected_customer_id,))
            self.clear_customer_form()
            self.refresh_all()

    def clear_customer_form(self):
        self.selected_customer_id = None
        for var in [self.c_name, self.c_mobile, self.c_whatsapp, self.c_email, self.c_company]:
            var.set("")
        self.set_text_value(self.c_address_text, "")
        self.set_text_value(self.c_notes_text, "")

    def on_customer_select(self, event):
        selected = self.customers_tree.selection()
        if not selected:
            return
        item = self.customers_tree.item(selected[0])
        customer_id = item["values"][0]
        row = self.db.fetchone("SELECT * FROM customers WHERE id=?", (customer_id,))
        if not row:
            return
        self.selected_customer_id = row["id"]
        self.c_name.set(row["name"] or "")
        self.c_mobile.set(row["mobile"] or "")
        self.c_whatsapp.set(row["whatsapp"] or "")
        self.c_email.set(row["email"] or "")
        self.set_text_value(self.c_address_text, row["address"])
        self.c_company.set(row["company"] or "")
        self.set_text_value(self.c_notes_text, row["notes"])

    def load_customers(self):
        for row in self.customers_tree.get_children():
            self.customers_tree.delete(row)
        q = self.customer_search.get().strip() if hasattr(self, "customer_search") else ""
        if q:
            like = f"%{q}%"
            rows = self.db.fetchall(
                """
                SELECT * FROM customers
                WHERE name LIKE ? OR mobile LIKE ? OR whatsapp LIKE ? OR email LIKE ? OR company LIKE ?
                ORDER BY id DESC
                """,
                (like, like, like, like, like),
            )
        else:
            rows = self.db.fetchall("SELECT * FROM customers ORDER BY id DESC")
        for r in rows:
            self.customers_tree.insert("", "end", values=(r["id"], r["customer_code"], r["name"], r["mobile"], r["whatsapp"], r["email"], r["company"]))

    # ------------------------ DEVICES ------------------------
    def build_devices_tab(self):
        outer = ttk.Frame(self.devices_tab, padding=8)
        outer.pack(fill="both", expand=True)

        left = ttk.LabelFrame(outer, text="Device Form", padding=7)
        left.pack(side="left", fill="y", padx=(0, 10))

        self.d_customer, self.device_customer_combo = self.form_row(left, "Customer *", 0, widget="combo", values=[])
        self.d_category, self.device_category_combo = self.form_row(left, "Category *", 1, widget="combo", values=[])
        self.d_brand, _ = self.form_row(left, "Brand", 2)
        self.d_model, _ = self.form_row(left, "Model", 3)
        self.d_serial, _ = self.form_row(left, "Serial Number", 4)
        self.d_asset, _ = self.form_row(left, "Asset Tag", 5)
        self.d_processor, _ = self.form_row(left, "Processor", 6)
        self.d_ram, _ = self.form_row(left, "RAM", 7)
        self.d_storage, _ = self.form_row(left, "Storage", 8)
        self.d_gpu, _ = self.form_row(left, "GPU", 9)
        self.d_windows, _ = self.form_row(left, "Windows Version", 10)
        self.d_charger, self.d_charger_combo = self.form_row(left, "Charger Included", 11, widget="combo", values=["Yes", "No"])
        self.d_bag, self.d_bag_combo = self.form_row(left, "Bag Included", 12, widget="combo", values=["Yes", "No"])
        self.d_password, _ = self.form_row(left, "Password", 13)
        self.d_bios, _ = self.form_row(left, "BIOS Password", 14)
        self.d_accessories, _ = self.form_row(left, "Accessories", 15)

        btns = ttk.Frame(left)
        btns.grid(row=16, column=0, columnspan=2, sticky="ew", pady=10)
        ttk.Button(btns, text="Add", command=self.add_device).pack(side="left", padx=3)
        ttk.Button(btns, text="Update", command=self.update_device).pack(side="left", padx=3)
        ttk.Button(btns, text="Delete", command=self.delete_device).pack(side="left", padx=3)
        ttk.Button(btns, text="Clear", command=self.clear_device_form).pack(side="left", padx=3)

        right = ttk.Frame(outer)
        right.pack(side="left", fill="both", expand=True)
        search_frame = ttk.Frame(right)
        search_frame.pack(fill="x")
        self.device_search = tk.StringVar()
        ttk.Entry(search_frame, textvariable=self.device_search).pack(side="left", fill="x", expand=True, padx=(0, 6))
        ttk.Button(search_frame, text="Search", command=self.load_devices).pack(side="left")

        columns = ("id", "code", "customer", "category", "brand", "model", "serial", "asset")
        self.devices_tree = ttk.Treeview(right, columns=columns, show="headings")
        for col in columns:
            self.devices_tree.heading(col, text=col.title())
            self.devices_tree.column(col, width=120)
        self.devices_tree.pack(fill="both", expand=True, pady=8)
        self.devices_tree.bind("<<TreeviewSelect>>", self.on_device_select)

    def generate_device_code(self, device_id):
        return f"DEV{device_id:05d}"

    def add_device(self):
        customer_id = self.customer_map.get(self.d_customer.get())
        category = self.d_category.get().strip()
        if not customer_id or not category:
            messagebox.showwarning("Required", "Customer and Category are required.")
            return
        cur = self.db.execute(
            """
            INSERT INTO devices(customer_id, category, brand, model, serial_number, asset_tag, processor, ram,
            storage, gpu, windows_version, charger_included, bag_included, password, bios_password,
            accessories, notes, created_at)
            VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                customer_id, category, self.d_brand.get().strip(), self.d_model.get().strip(),
                self.d_serial.get().strip(), self.d_asset.get().strip(), self.d_processor.get().strip(),
                self.d_ram.get().strip(), self.d_storage.get().strip(), self.d_gpu.get().strip(),
                self.d_windows.get().strip(), self.d_charger.get().strip(), self.d_bag.get().strip(),
                self.d_password.get().strip(), self.d_bios.get().strip(), self.d_accessories.get().strip(),
                "", now_text(),
            ),
        )
        device_id = cur.lastrowid
        self.db.execute("UPDATE devices SET device_code=? WHERE id=?", (self.generate_device_code(device_id), device_id))
        self.db.log_activity("device", f"Device added: {category} {self.d_brand.get()} {self.d_model.get()}")
        self.clear_device_form()
        self.refresh_all()

    def update_device(self):
        if not self.selected_device_id:
            messagebox.showinfo("Select", "Select a device first.")
            return
        customer_id = self.customer_map.get(self.d_customer.get())
        if not customer_id:
            messagebox.showwarning("Required", "Customer is required.")
            return
        self.db.execute(
            """
            UPDATE devices SET customer_id=?, category=?, brand=?, model=?, serial_number=?, asset_tag=?,
            processor=?, ram=?, storage=?, gpu=?, windows_version=?, charger_included=?, bag_included=?,
            password=?, bios_password=?, accessories=? WHERE id=?
            """,
            (
                customer_id, self.d_category.get().strip(), self.d_brand.get().strip(), self.d_model.get().strip(),
                self.d_serial.get().strip(), self.d_asset.get().strip(), self.d_processor.get().strip(),
                self.d_ram.get().strip(), self.d_storage.get().strip(), self.d_gpu.get().strip(),
                self.d_windows.get().strip(), self.d_charger.get().strip(), self.d_bag.get().strip(),
                self.d_password.get().strip(), self.d_bios.get().strip(), self.d_accessories.get().strip(),
                self.selected_device_id,
            ),
        )
        self.db.log_activity("device", f"Device updated: {self.d_category.get()} {self.d_model.get()}")
        self.refresh_all()

    def delete_device(self):
        if not self.selected_device_id:
            messagebox.showinfo("Select", "Select a device first.")
            return
        if messagebox.askyesno("Confirm", "Delete selected device? Related jobs will also be deleted."):
            self.db.execute("DELETE FROM devices WHERE id=?", (self.selected_device_id,))
            self.clear_device_form()
            self.refresh_all()

    def clear_device_form(self):
        self.selected_device_id = None
        for var in [self.d_customer, self.d_category, self.d_brand, self.d_model, self.d_serial, self.d_asset,
                    self.d_processor, self.d_ram, self.d_storage, self.d_gpu, self.d_windows, self.d_charger,
                    self.d_bag, self.d_password, self.d_bios, self.d_accessories]:
            var.set("")

    def on_device_select(self, event):
        selected = self.devices_tree.selection()
        if not selected:
            return
        item = self.devices_tree.item(selected[0])
        device_id = item["values"][0]
        row = self.db.fetchone("SELECT * FROM devices WHERE id=?", (device_id,))
        if not row:
            return
        self.selected_device_id = row["id"]
        customer_row = self.db.fetchone("SELECT * FROM customers WHERE id=?", (row["customer_id"],))
        if customer_row:
            self.d_customer.set(self.customer_display(customer_row))
        self.d_category.set(row["category"] or "")
        self.d_brand.set(row["brand"] or "")
        self.d_model.set(row["model"] or "")
        self.d_serial.set(row["serial_number"] or "")
        self.d_asset.set(row["asset_tag"] or "")
        self.d_processor.set(row["processor"] or "")
        self.d_ram.set(row["ram"] or "")
        self.d_storage.set(row["storage"] or "")
        self.d_gpu.set(row["gpu"] or "")
        self.d_windows.set(row["windows_version"] or "")
        self.d_charger.set(row["charger_included"] or "")
        self.d_bag.set(row["bag_included"] or "")
        self.d_password.set(row["password"] or "")
        self.d_bios.set(row["bios_password"] or "")
        self.d_accessories.set(row["accessories"] or "")

    def load_devices(self):
        for row in self.devices_tree.get_children():
            self.devices_tree.delete(row)
        q = self.device_search.get().strip() if hasattr(self, "device_search") else ""
        params = []
        where = ""
        if q:
            like = f"%{q}%"
            where = "WHERE c.name LIKE ? OR c.mobile LIKE ? OR d.category LIKE ? OR d.brand LIKE ? OR d.model LIKE ? OR d.serial_number LIKE ? OR d.asset_tag LIKE ?"
            params = [like, like, like, like, like, like, like]
        rows = self.db.fetchall(
            f"""
            SELECT d.*, c.name AS customer_name
            FROM devices d
            JOIN customers c ON c.id=d.customer_id
            {where}
            ORDER BY d.id DESC
            """,
            tuple(params),
        )
        for r in rows:
            self.devices_tree.insert("", "end", values=(r["id"], r["device_code"], r["customer_name"], r["category"], r["brand"], r["model"], r["serial_number"], r["asset_tag"]))

    # ------------------------ JOBS ------------------------
    def build_jobs_tab(self):
        outer = ttk.Frame(self.jobs_tab, padding=8)
        outer.pack(fill="both", expand=True)

        left = ttk.LabelFrame(outer, text="Service Job Form", padding=7)
        left.pack(side="left", fill="y", padx=(0, 10))

        self.j_customer, self.job_customer_combo = self.form_row(left, "Customer *", 0, widget="combo", values=[])
        self.j_device, self.job_device_combo = self.form_row(left, "Device *", 1, widget="combo", values=[])
        self.j_service, self.job_service_combo = self.form_row(left, "Service Type", 2, widget="combo", values=[])
        self.j_priority, self.job_priority_combo = self.form_row(left, "Priority", 3, widget="combo", values=PRIORITIES)
        self.j_status, self.job_status_combo = self.form_row(left, "Status", 4, widget="combo", values=STATUSES)
        self.j_problem, self.j_problem_text = self.form_row(left, "Problem Description", 5, widget="text", width=34)
        self.j_notes, self.j_notes_text = self.form_row(left, "Engineer Notes", 6, widget="text", width=34)
        self.j_estimated, _ = self.form_row(left, "Estimate Amount", 7)
        self.j_final, _ = self.form_row(left, "Final Amount", 8)
        self.j_paid, _ = self.form_row(left, "Paid Amount", 9)
        self.j_discount, _ = self.form_row(left, "Discount", 10)
        self.j_vat, _ = self.form_row(left, "VAT", 11)
        self.j_warranty_days, _ = self.form_row(left, "Warranty Days", 12)

        self.j_priority.set("Medium")
        self.j_status.set("Received")

        btns = ttk.Frame(left)
        btns.grid(row=13, column=0, columnspan=2, sticky="ew", pady=10)
        ttk.Button(btns, text="Add", command=self.add_job).pack(side="left", padx=3)
        ttk.Button(btns, text="Update", command=self.update_job).pack(side="left", padx=3)
        ttk.Button(btns, text="Delete", command=self.delete_job).pack(side="left", padx=3)
        ttk.Button(btns, text="Clear", command=self.clear_job_form).pack(side="left", padx=3)

        right = ttk.Frame(outer)
        right.pack(side="left", fill="both", expand=True)
        search_frame = ttk.Frame(right)
        search_frame.pack(fill="x")
        self.job_search = tk.StringVar()
        ttk.Entry(search_frame, textvariable=self.job_search).pack(side="left", fill="x", expand=True, padx=(0, 6))
        ttk.Button(search_frame, text="Search", command=self.load_jobs).pack(side="left")

        columns = ("id", "job", "customer", "mobile", "device", "service", "status", "priority", "due")
        self.jobs_tree = ttk.Treeview(right, columns=columns, show="headings")
        for col in columns:
            self.jobs_tree.heading(col, text=col.title())
            self.jobs_tree.column(col, width=110)
        self.jobs_tree.pack(fill="both", expand=True, pady=8)
        self.jobs_tree.bind("<<TreeviewSelect>>", self.on_job_select)

    def generate_job_number(self):
        prefix = datetime.now().strftime("HS%y%m")
        row = self.db.fetchone("SELECT COUNT(*) AS total FROM jobs WHERE job_number LIKE ?", (prefix + "%",))
        next_num = row["total"] + 1
        return f"{prefix}{next_num:04d}"

    def calculate_warranty_end(self, days):
        d = self.safe_int(days)
        if d <= 0:
            return None
        return (datetime.now() + timedelta(days=d)).strftime("%Y-%m-%d")

    def add_job(self):
        customer_id = self.customer_map.get(self.j_customer.get())
        device_id = self.device_map.get(self.j_device.get())
        if not customer_id or not device_id:
            messagebox.showwarning("Required", "Customer and Device are required.")
            return
        job_number = self.generate_job_number()
        warranty_end = self.calculate_warranty_end(self.j_warranty_days.get())
        cur_time = now_text()
        self.db.execute(
            """
            INSERT INTO jobs(job_number, customer_id, device_id, service_type, priority, status,
            problem_description, engineer_notes, estimated_amount, final_amount, paid_amount,
            discount_amount, vat_amount, warranty_days, warranty_end_date, created_at, updated_at, delivered_at)
            VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                job_number, customer_id, device_id, self.j_service.get().strip(), self.j_priority.get().strip() or "Medium",
                self.j_status.get().strip() or "Received", self.get_text_value(self.j_problem_text),
                self.get_text_value(self.j_notes_text), self.safe_float(self.j_estimated.get()),
                self.safe_float(self.j_final.get()), self.safe_float(self.j_paid.get()),
                self.safe_float(self.j_discount.get()), self.safe_float(self.j_vat.get()),
                self.safe_int(self.j_warranty_days.get()), warranty_end, cur_time, cur_time,
                cur_time if self.j_status.get() == "Delivered" else None,
            ),
        )
        job_id = self.db.fetchone("SELECT id FROM jobs WHERE job_number=?", (job_number,))["id"]
        self.db.execute(
            "INSERT INTO work_logs(job_id, log_time, note, created_at) VALUES(?, ?, ?, ?)",
            (job_id, cur_time, f"Job created with status: {self.j_status.get().strip() or 'Received'}", cur_time),
        )
        self.db.log_activity("job", f"Job created: {job_number}")
        messagebox.showinfo("Created", f"Service Job Created: {job_number}")
        self.clear_job_form()
        self.refresh_all()

    def update_job(self):
        if not self.selected_job_id:
            messagebox.showinfo("Select", "Select a job first.")
            return
        customer_id = self.customer_map.get(self.j_customer.get())
        device_id = self.device_map.get(self.j_device.get())
        if not customer_id or not device_id:
            messagebox.showwarning("Required", "Customer and Device are required.")
            return
        old = self.db.fetchone("SELECT * FROM jobs WHERE id=?", (self.selected_job_id,))
        new_status = self.j_status.get().strip() or "Received"
        warranty_end = self.calculate_warranty_end(self.j_warranty_days.get())
        delivered_at = old["delivered_at"]
        if new_status == "Delivered" and not delivered_at:
            delivered_at = now_text()
        self.db.execute(
            """
            UPDATE jobs SET customer_id=?, device_id=?, service_type=?, priority=?, status=?,
            problem_description=?, engineer_notes=?, estimated_amount=?, final_amount=?, paid_amount=?,
            discount_amount=?, vat_amount=?, warranty_days=?, warranty_end_date=?, updated_at=?, delivered_at=?
            WHERE id=?
            """,
            (
                customer_id, device_id, self.j_service.get().strip(), self.j_priority.get().strip(), new_status,
                self.get_text_value(self.j_problem_text), self.get_text_value(self.j_notes_text),
                self.safe_float(self.j_estimated.get()), self.safe_float(self.j_final.get()),
                self.safe_float(self.j_paid.get()), self.safe_float(self.j_discount.get()),
                self.safe_float(self.j_vat.get()), self.safe_int(self.j_warranty_days.get()),
                warranty_end, now_text(), delivered_at, self.selected_job_id,
            ),
        )
        if old and old["status"] != new_status:
            self.db.execute(
                "INSERT INTO work_logs(job_id, log_time, note, created_at) VALUES(?, ?, ?, ?)",
                (self.selected_job_id, now_text(), f"Status changed: {old['status']} → {new_status}", now_text()),
            )
        self.db.log_activity("job", f"Job updated: {old['job_number'] if old else self.selected_job_id}")
        self.refresh_all()

    def delete_job(self):
        if not self.selected_job_id:
            messagebox.showinfo("Select", "Select a job first.")
            return
        if messagebox.askyesno("Confirm", "Delete selected service job?"):
            self.db.execute("DELETE FROM jobs WHERE id=?", (self.selected_job_id,))
            self.clear_job_form()
            self.refresh_all()

    def clear_job_form(self):
        self.selected_job_id = None
        for var in [self.j_customer, self.j_device, self.j_service, self.j_estimated, self.j_final, self.j_paid, self.j_discount, self.j_vat, self.j_warranty_days]:
            var.set("")
        self.j_priority.set("Medium")
        self.j_status.set("Received")
        self.set_text_value(self.j_problem_text, "")
        self.set_text_value(self.j_notes_text, "")

    def on_job_select(self, event):
        selected = self.jobs_tree.selection()
        if not selected:
            return
        item = self.jobs_tree.item(selected[0])
        job_id = item["values"][0]
        row = self.db.fetchone("SELECT * FROM jobs WHERE id=?", (job_id,))
        if not row:
            return
        self.selected_job_id = row["id"]

        customer_row = self.db.fetchone("SELECT * FROM customers WHERE id=?", (row["customer_id"],))
        device_row = self.db.fetchone("SELECT * FROM devices WHERE id=?", (row["device_id"],))
        if customer_row:
            self.j_customer.set(self.customer_display(customer_row))
        if device_row:
            self.j_device.set(self.device_display(device_row))
        self.j_service.set(row["service_type"] or "")
        self.j_priority.set(row["priority"] or "Medium")
        self.j_status.set(row["status"] or "Received")
        self.set_text_value(self.j_problem_text, row["problem_description"])
        self.set_text_value(self.j_notes_text, row["engineer_notes"])
        self.j_estimated.set(str(row["estimated_amount"] or 0))
        self.j_final.set(str(row["final_amount"] or 0))
        self.j_paid.set(str(row["paid_amount"] or 0))
        self.j_discount.set(str(row["discount_amount"] or 0))
        self.j_vat.set(str(row["vat_amount"] or 0))
        self.j_warranty_days.set(str(row["warranty_days"] or 0))

    def load_jobs(self):
        for row in self.jobs_tree.get_children():
            self.jobs_tree.delete(row)
        q = self.job_search.get().strip() if hasattr(self, "job_search") else ""
        params = []
        where = ""
        if q:
            like = f"%{q}%"
            where = """
            WHERE j.job_number LIKE ? OR c.name LIKE ? OR c.mobile LIKE ? OR d.category LIKE ? OR
            d.brand LIKE ? OR d.model LIKE ? OR d.serial_number LIKE ? OR j.status LIKE ? OR j.service_type LIKE ?
            """
            params = [like, like, like, like, like, like, like, like, like]
        rows = self.db.fetchall(
            f"""
            SELECT j.*, c.name, c.mobile, d.category, d.brand, d.model, d.serial_number
            FROM jobs j
            JOIN customers c ON c.id=j.customer_id
            JOIN devices d ON d.id=j.device_id
            {where}
            ORDER BY j.id DESC
            """,
            tuple(params),
        )
        for r in rows:
            due = (r["final_amount"] or 0) - (r["paid_amount"] or 0)
            self.jobs_tree.insert(
                "", "end",
                values=(r["id"], r["job_number"], r["name"], r["mobile"], f"{r['category']} {r['brand'] or ''} {r['model'] or ''}", r["service_type"], r["status"], r["priority"], money(due)),
            )

    # ------------------------ LOGS & PARTS ------------------------
    def build_logs_tab(self):
        outer = ttk.Frame(self.logs_tab, padding=8)
        outer.pack(fill="both", expand=True)

        top = ttk.Frame(outer)
        top.pack(fill="x")
        ttk.Label(top, text="Select Job").pack(side="left")
        self.log_job_var = tk.StringVar()
        self.log_job_combo = ttk.Combobox(top, textvariable=self.log_job_var, width=85, state="readonly")
        self.log_job_combo.pack(side="left", padx=8)
        ttk.Button(top, text="Load", command=self.load_logs_and_parts).pack(side="left")

        middle = ttk.Frame(outer)
        middle.pack(fill="both", expand=True, pady=12)

        log_box = ttk.LabelFrame(middle, text="Work Log", padding=7)
        log_box.pack(side="left", fill="both", expand=True, padx=(0, 8))
        self.log_note_text = tk.Text(log_box, height=4)
        self.log_note_text.pack(fill="x")
        ttk.Button(log_box, text="Add Work Log", command=self.add_work_log).pack(anchor="e", pady=6)
        self.logs_tree = ttk.Treeview(log_box, columns=("time", "note"), show="headings")
        self.logs_tree.heading("time", text="Time")
        self.logs_tree.heading("note", text="Note")
        self.logs_tree.column("time", width=150)
        self.logs_tree.column("note", width=480)
        self.logs_tree.pack(fill="both", expand=True)

        part_box = ttk.LabelFrame(middle, text="Parts Used", padding=7)
        part_box.pack(side="left", fill="both", expand=True)
        form = ttk.Frame(part_box)
        form.pack(fill="x")
        self.part_name = tk.StringVar()
        self.part_qty = tk.StringVar(value="1")
        self.part_cost = tk.StringVar(value="0")
        self.part_sale = tk.StringVar(value="0")
        self.part_warranty = tk.StringVar(value="0")
        for i, (label, var, width) in enumerate([
            ("Part", self.part_name, 18), ("Qty", self.part_qty, 7), ("Cost", self.part_cost, 8),
            ("Sale", self.part_sale, 8), ("Warranty", self.part_warranty, 8),
        ]):
            ttk.Label(form, text=label).grid(row=0, column=i, sticky="w")
            ttk.Entry(form, textvariable=var, width=width).grid(row=1, column=i, padx=2)
        ttk.Button(form, text="Add Part", command=self.add_part).grid(row=1, column=5, padx=4)

        self.parts_tree = ttk.Treeview(part_box, columns=("part", "qty", "cost", "sale", "warranty"), show="headings")
        for col in ("part", "qty", "cost", "sale", "warranty"):
            self.parts_tree.heading(col, text=col.title())
            self.parts_tree.column(col, width=110)
        self.parts_tree.pack(fill="both", expand=True, pady=8)

    def current_log_job_id(self):
        return self.job_map.get(self.log_job_var.get())

    def add_work_log(self):
        job_id = self.current_log_job_id()
        note = self.get_text_value(self.log_note_text)
        if not job_id or not note:
            messagebox.showwarning("Required", "Select job and write log note.")
            return
        self.db.execute(
            "INSERT INTO work_logs(job_id, log_time, note, created_at) VALUES(?, ?, ?, ?)",
            (job_id, now_text(), note, now_text()),
        )
        self.db.execute("UPDATE jobs SET updated_at=? WHERE id=?", (now_text(), job_id))
        self.set_text_value(self.log_note_text, "")
        self.load_logs_and_parts()
        self.load_dashboard()

    def add_part(self):
        job_id = self.current_log_job_id()
        part = self.part_name.get().strip()
        if not job_id or not part:
            messagebox.showwarning("Required", "Select job and enter part name.")
            return
        self.db.execute(
            """
            INSERT INTO job_parts(job_id, part_name, quantity, cost_price, sale_price, warranty_days, created_at)
            VALUES(?, ?, ?, ?, ?, ?, ?)
            """,
            (
                job_id, part, self.safe_float(self.part_qty.get()), self.safe_float(self.part_cost.get()),
                self.safe_float(self.part_sale.get()), self.safe_int(self.part_warranty.get()), now_text(),
            ),
        )
        self.db.execute(
            "INSERT INTO work_logs(job_id, log_time, note, created_at) VALUES(?, ?, ?, ?)",
            (job_id, now_text(), f"Part used: {part} x {self.part_qty.get()}", now_text()),
        )
        self.db.execute("UPDATE jobs SET updated_at=? WHERE id=?", (now_text(), job_id))
        self.part_name.set("")
        self.part_qty.set("1")
        self.part_cost.set("0")
        self.part_sale.set("0")
        self.part_warranty.set("0")
        self.load_logs_and_parts()

    def load_logs_and_parts(self):
        if not hasattr(self, "logs_tree"):
            return
        for row in self.logs_tree.get_children():
            self.logs_tree.delete(row)
        for row in self.parts_tree.get_children():
            self.parts_tree.delete(row)
        job_id = self.current_log_job_id()
        if not job_id:
            return
        logs = self.db.fetchall("SELECT * FROM work_logs WHERE job_id=? ORDER BY id DESC", (job_id,))
        for r in logs:
            self.logs_tree.insert("", "end", values=(r["log_time"], r["note"]))
        parts = self.db.fetchall("SELECT * FROM job_parts WHERE job_id=? ORDER BY id DESC", (job_id,))
        for r in parts:
            self.parts_tree.insert("", "end", values=(r["part_name"], r["quantity"], money(r["cost_price"]), money(r["sale_price"]), r["warranty_days"]))

    # ------------------------ INVOICE ------------------------
    def build_invoice_tab(self):
        outer = ttk.Frame(self.invoice_tab, padding=8)
        outer.pack(fill="both", expand=True)
        top = ttk.Frame(outer)
        top.pack(fill="x")
        ttk.Label(top, text="Select Job").pack(side="left")
        self.invoice_job_var = tk.StringVar()
        self.invoice_job_combo = ttk.Combobox(top, textvariable=self.invoice_job_var, width=85, state="readonly")
        self.invoice_job_combo.pack(side="left", padx=8)
        ttk.Button(top, text="Preview", command=self.preview_invoice).pack(side="left", padx=4)
        ttk.Button(top, text="Save TXT", command=self.save_invoice_txt).pack(side="left", padx=4)
        ttk.Button(top, text="Open", command=self.open_invoice_html).pack(side="left", padx=4)

        self.invoice_text = tk.Text(outer, wrap="word", font=("Consolas", 10))
        self.invoice_text.pack(fill="both", expand=True, pady=12)

    def current_invoice_job_id(self):
        return self.job_map.get(self.invoice_job_var.get())

    def build_invoice_text(self, job_id):
        row = self.db.fetchone(
            """
            SELECT j.*, c.name, c.mobile, c.whatsapp, c.email, c.address, c.company,
                   d.category, d.brand, d.model, d.serial_number, d.asset_tag, d.accessories
            FROM jobs j
            JOIN customers c ON c.id=j.customer_id
            JOIN devices d ON d.id=j.device_id
            WHERE j.id=?
            """,
            (job_id,),
        )
        if not row:
            return ""
        parts = self.db.fetchall("SELECT * FROM job_parts WHERE job_id=?", (job_id,))
        logs = self.db.fetchall("SELECT * FROM work_logs WHERE job_id=? ORDER BY id ASC", (job_id,))
        parts_total = sum((p["sale_price"] or 0) * (p["quantity"] or 0) for p in parts)
        due = (row["final_amount"] or 0) - (row["paid_amount"] or 0)

        lines = []
        lines.append("=" * 72)
        lines.append("HABITABLE SOLUTION - SERVICE INVOICE / MONEY RECEIPT")
        lines.append("=" * 72)
        lines.append(f"Job Number     : {row['job_number']}")
        lines.append(f"Date           : {row['created_at']}")
        lines.append(f"Status         : {row['status']}")
        lines.append(f"Priority       : {row['priority']}")
        lines.append("-" * 72)
        lines.append("CUSTOMER")
        lines.append(f"Name           : {row['name']}")
        lines.append(f"Mobile         : {row['mobile']}")
        lines.append(f"WhatsApp       : {row['whatsapp'] or '-'}")
        lines.append(f"Email          : {row['email'] or '-'}")
        lines.append(f"Company        : {row['company'] or '-'}")
        lines.append(f"Address        : {row['address'] or '-'}")
        lines.append("-" * 72)
        lines.append("DEVICE")
        lines.append(f"Device         : {row['category']} {row['brand'] or ''} {row['model'] or ''}")
        lines.append(f"Serial Number  : {row['serial_number'] or '-'}")
        lines.append(f"Asset Tag      : {row['asset_tag'] or '-'}")
        lines.append(f"Accessories    : {row['accessories'] or '-'}")
        lines.append("-" * 72)
        lines.append("SERVICE")
        lines.append(f"Service Type   : {row['service_type'] or '-'}")
        lines.append(f"Problem        : {row['problem_description'] or '-'}")
        lines.append(f"Engineer Notes : {row['engineer_notes'] or '-'}")
        lines.append("-" * 72)
        lines.append("PARTS USED")
        if parts:
            for p in parts:
                line_total = (p["sale_price"] or 0) * (p["quantity"] or 0)
                lines.append(f"- {p['part_name']} | Qty: {p['quantity']} | Sale: {money(p['sale_price'])} | Total: {money(line_total)} | Warranty: {p['warranty_days']} days")
        else:
            lines.append("No parts added.")
        lines.append("-" * 72)
        lines.append("PAYMENT")
        lines.append(f"Estimate       : BDT {money(row['estimated_amount'])}")
        lines.append(f"Parts Total    : BDT {money(parts_total)}")
        lines.append(f"Discount       : BDT {money(row['discount_amount'])}")
        lines.append(f"VAT            : BDT {money(row['vat_amount'])}")
        lines.append(f"Final Amount   : BDT {money(row['final_amount'])}")
        lines.append(f"Paid Amount    : BDT {money(row['paid_amount'])}")
        lines.append(f"Due Amount     : BDT {money(due)}")
        lines.append("-" * 72)
        lines.append("WARRANTY")
        lines.append(f"Warranty Days  : {row['warranty_days'] or 0}")
        lines.append(f"Warranty End   : {row['warranty_end_date'] or '-'}")
        lines.append("-" * 72)
        lines.append("WORK LOG")
        if logs:
            for log in logs:
                lines.append(f"{log['log_time']} - {log['note']}")
        else:
            lines.append("No work log added.")
        lines.append("=" * 72)
        lines.append("Customer Signature: ____________________")
        lines.append("Authorized Signature: __________________")
        lines.append("=" * 72)
        return "\n".join(lines)

    def preview_invoice(self):
        job_id = self.current_invoice_job_id()
        if not job_id:
            messagebox.showwarning("Required", "Select a job first.")
            return
        text = self.build_invoice_text(job_id)
        self.invoice_text.delete("1.0", "end")
        self.invoice_text.insert("1.0", text)

    def save_invoice_txt(self):
        job_id = self.current_invoice_job_id()
        if not job_id:
            messagebox.showwarning("Required", "Select a job first.")
            return
        row = self.db.fetchone("SELECT job_number FROM jobs WHERE id=?", (job_id,))
        default_name = f"invoice_{row['job_number']}.txt" if row else "invoice.txt"
        path = filedialog.asksaveasfilename(defaultextension=".txt", initialfile=default_name, filetypes=[("Text File", "*.txt")])
        if not path:
            return
        with open(path, "w", encoding="utf-8") as f:
            f.write(self.build_invoice_text(job_id))
        messagebox.showinfo("Saved", f"Invoice saved:\n{path}")

    def get_invoice_data(self, job_id):
        row = self.db.fetchone(
            """
            SELECT j.*, c.name, c.mobile, c.whatsapp, c.email, c.address, c.company,
                   d.category, d.brand, d.model, d.serial_number, d.asset_tag, d.accessories
            FROM jobs j
            JOIN customers c ON c.id=j.customer_id
            JOIN devices d ON d.id=j.device_id
            WHERE j.id=?
            """,
            (job_id,),
        )
        if not row:
            return None, [], [], 0, 0
        parts = self.db.fetchall("SELECT * FROM job_parts WHERE job_id=?", (job_id,))
        logs = self.db.fetchall("SELECT * FROM work_logs WHERE job_id=? ORDER BY id ASC", (job_id,))
        parts_total = sum((p["sale_price"] or 0) * (p["quantity"] or 0) for p in parts)
        due = (row["final_amount"] or 0) - (row["paid_amount"] or 0)
        return row, parts, logs, parts_total, due

    def esc(self, value):
        return html.escape(str(value if value not in (None, "") else "-"))

    def build_invoice_html(self, job_id):
        row, parts, logs, parts_total, due = self.get_invoice_data(job_id)
        if not row:
            return ""

        def tr(label, value):
            return f"<tr><th>{self.esc(label)}</th><td>{self.esc(value)}</td></tr>"

        parts_rows = ""
        if parts:
            for i, p in enumerate(parts, start=1):
                line_total = (p["sale_price"] or 0) * (p["quantity"] or 0)
                parts_rows += f"""
                <tr>
                    <td>{i}</td>
                    <td>{self.esc(p['part_name'])}</td>
                    <td class="right">{self.esc(p['quantity'])}</td>
                    <td class="right">BDT {money(p['sale_price'])}</td>
                    <td class="right">BDT {money(line_total)}</td>
                    <td>{self.esc(str(p['warranty_days']) + ' days')}</td>
                </tr>
                """
        else:
            parts_rows = '<tr><td colspan="6" class="muted center">No parts added.</td></tr>'

        logs_rows = ""
        if logs:
            for log in logs:
                logs_rows += f"<li><strong>{self.esc(log['log_time'])}</strong> — {self.esc(log['note'])}</li>"
        else:
            logs_rows = '<li class="muted">No work log added.</li>'

        device_name = f"{row['category']} {row['brand'] or ''} {row['model'] or ''}".strip()
        generated_at = now_text()

        return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Invoice {self.esc(row['job_number'])} - {COMPANY_NAME}</title>
<style>
    * {{ box-sizing: border-box; }}
    body {{ margin: 0; background: #eef2f7; color: #111827; font-family: Arial, Helvetica, sans-serif; }}
    .page {{ width: 210mm; min-height: 297mm; margin: 16px auto; background: #fff; padding: 26px; box-shadow: 0 10px 30px rgba(15,23,42,.15); }}
    .topbar {{ display: flex; justify-content: space-between; align-items: flex-start; border-bottom: 3px solid #1d4ed8; padding-bottom: 14px; }}
    .brand h1 {{ margin: 0; font-size: 24px; letter-spacing: .4px; color: #0f172a; }}
    .brand p {{ margin: 5px 0 0; color: #475569; font-size: 13px; }}
    .invoice-title {{ text-align: right; }}
    .invoice-title h2 {{ margin: 0; font-size: 22px; color: #1d4ed8; }}
    .badge {{ display: inline-block; margin-top: 8px; padding: 6px 12px; border-radius: 999px; background: #dbeafe; color: #1e40af; font-weight: bold; font-size: 12px; }}
    .grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-top: 18px; }}
    .card {{ border: 1px solid #e5e7eb; border-radius: 10px; overflow: hidden; }}
    .card h3 {{ margin: 0; background: #f8fafc; padding: 10px 12px; font-size: 14px; color: #0f172a; border-bottom: 1px solid #e5e7eb; }}
    table {{ width: 100%; border-collapse: collapse; }}
    th, td {{ padding: 9px 10px; border-bottom: 1px solid #eef2f7; vertical-align: top; font-size: 13px; }}
    th {{ width: 38%; text-align: left; color: #475569; font-weight: 700; }}
    .full {{ margin-top: 16px; }}
    .items th {{ width: auto; background: #f8fafc; color: #334155; }}
    .items thead th {{ border-bottom: 2px solid #e2e8f0; }}
    .right {{ text-align: right; }}
    .center {{ text-align: center; }}
    .muted {{ color: #64748b; }}
    .summary {{ margin-left: auto; width: 360px; margin-top: 14px; border: 1px solid #e5e7eb; border-radius: 10px; overflow: hidden; }}
    .summary td {{ border-bottom: 1px solid #e5e7eb; }}
    .summary .total td {{ background: #1d4ed8; color: #fff; font-weight: bold; font-size: 15px; }}
    .summary .due td {{ color: #b91c1c; font-weight: bold; }}
    .notes {{ margin: 0; padding: 10px 22px 14px; }}
    .notes li {{ margin-bottom: 7px; font-size: 13px; }}
    .signatures {{ display: grid; grid-template-columns: 1fr 1fr; gap: 70px; margin-top: 46px; }}
    .signature {{ border-top: 1px solid #111827; text-align: center; padding-top: 8px; font-size: 13px; }}
    .footer {{ margin-top: 32px; padding-top: 12px; border-top: 1px solid #e5e7eb; display: flex; justify-content: space-between; color: #64748b; font-size: 12px; }}
    .print-actions {{ width: 210mm; margin: 14px auto 0; text-align: right; }}
    .print-actions button {{ background: #1d4ed8; color: #fff; border: 0; padding: 10px 18px; border-radius: 8px; cursor: pointer; font-weight: bold; }}
    @media print {{
        body {{ background: #fff; }}
        .print-actions {{ display: none; }}
        .page {{ margin: 0; width: auto; min-height: auto; box-shadow: none; padding: 18mm; }}
        @page {{ size: A4; margin: 0; }}
    }}
</style>
</head>
<body>
<div class="print-actions"><button onclick="window.print()">Print / Save PDF</button></div>
<main class="page">
    <section class="topbar">
        <div class="brand">
            <h1>{COMPANY_NAME}</h1>
            <p>{APP_TITLE}</p>
            <p>{COMPANY_WEBSITE} | {DOWNLOAD_PAGE}</p>
        </div>
        <div class="invoice-title">
            <h2>Service Invoice</h2>
            <div class="badge">{self.esc(row['status'])}</div>
            <p><strong>Job:</strong> {self.esc(row['job_number'])}</p>
            <p><strong>Date:</strong> {self.esc(row['created_at'])}</p>
        </div>
    </section>

    <section class="grid">
        <div class="card">
            <h3>Customer Details</h3>
            <table>
                {tr('Name', row['name'])}
                {tr('Mobile', row['mobile'])}
                {tr('WhatsApp', row['whatsapp'])}
                {tr('Email', row['email'])}
                {tr('Company', row['company'])}
                {tr('Address', row['address'])}
            </table>
        </div>
        <div class="card">
            <h3>Device Details</h3>
            <table>
                {tr('Device', device_name)}
                {tr('Serial Number', row['serial_number'])}
                {tr('Asset Tag', row['asset_tag'])}
                {tr('Accessories', row['accessories'])}
                {tr('Priority', row['priority'])}
                {tr('Service Type', row['service_type'])}
            </table>
        </div>
    </section>

    <section class="card full">
        <h3>Service Information</h3>
        <table>
            {tr('Problem Description', row['problem_description'])}
            {tr('Engineer Notes', row['engineer_notes'])}
            {tr('Warranty Days', row['warranty_days'] or 0)}
            {tr('Warranty End', row['warranty_end_date'])}
        </table>
    </section>

    <section class="card full">
        <h3>Parts Used</h3>
        <table class="items">
            <thead><tr><th>#</th><th>Part</th><th class="right">Qty</th><th class="right">Sale Price</th><th class="right">Total</th><th>Warranty</th></tr></thead>
            <tbody>{parts_rows}</tbody>
        </table>
    </section>

    <table class="summary">
        <tr><td>Estimate</td><td class="right">BDT {money(row['estimated_amount'])}</td></tr>
        <tr><td>Parts Total</td><td class="right">BDT {money(parts_total)}</td></tr>
        <tr><td>Discount</td><td class="right">BDT {money(row['discount_amount'])}</td></tr>
        <tr><td>VAT</td><td class="right">BDT {money(row['vat_amount'])}</td></tr>
        <tr class="total"><td>Final Amount</td><td class="right">BDT {money(row['final_amount'])}</td></tr>
        <tr><td>Paid Amount</td><td class="right">BDT {money(row['paid_amount'])}</td></tr>
        <tr class="due"><td>Due Amount</td><td class="right">BDT {money(due)}</td></tr>
    </table>

    <section class="card full">
        <h3>Work Log</h3>
        <ul class="notes">{logs_rows}</ul>
    </section>

    <section class="signatures">
        <div class="signature">Customer Signature</div>
        <div class="signature">Authorized Signature</div>
    </section>

    <footer class="footer">
        <span>{FOOTER_BRANDING}</span>
        <span>Generated: {self.esc(generated_at)}</span>
    </footer>
</main>
</body>
</html>"""

    def open_invoice_html(self):
        job_id = self.current_invoice_job_id()
        if not job_id:
            messagebox.showwarning("Required", "Select a job first.")
            return
        row = self.db.fetchone("SELECT job_number FROM jobs WHERE id=?", (job_id,))
        safe_job_number = "invoice"
        if row and row["job_number"]:
            safe_job_number = "".join(ch for ch in row["job_number"] if ch.isalnum() or ch in ("-", "_")) or "invoice"
        file_name = f"invoice_{safe_job_number}.html"
        path = os.path.join(INVOICE_DIR, file_name)
        with open(path, "w", encoding="utf-8") as f:
            f.write(self.build_invoice_html(job_id))
        webbrowser.open_new_tab(Path(path).resolve().as_uri())
        messagebox.showinfo("Opened", "Invoice opened in your default browser. Use the Print / Save PDF button or Ctrl+P to print.")

    # ------------------------ REPORTS ------------------------
    def build_reports_tab(self):
        outer = ttk.Frame(self.reports_tab, padding=8)
        outer.pack(fill="both", expand=True)
        ttk.Button(outer, text="Refresh Reports", command=self.load_reports).pack(anchor="w")
        self.reports_text = tk.Text(outer, wrap="word", font=("Consolas", 10))
        self.reports_text.pack(fill="both", expand=True, pady=10)

    def load_reports(self):
        if not hasattr(self, "reports_text"):
            return
        month = datetime.now().strftime("%Y-%m")
        total_jobs = self.db.fetchone("SELECT COUNT(*) AS total FROM jobs")["total"]
        monthly_jobs = self.db.fetchone("SELECT COUNT(*) AS total FROM jobs WHERE created_at LIKE ?", (month + "%",))["total"]
        total_income = self.db.fetchone("SELECT COALESCE(SUM(paid_amount),0) AS total FROM jobs")["total"]
        monthly_income = self.db.fetchone("SELECT COALESCE(SUM(paid_amount),0) AS total FROM jobs WHERE updated_at LIKE ?", (month + "%",))["total"]
        due = self.db.fetchone("SELECT COALESCE(SUM(final_amount - paid_amount),0) AS total FROM jobs WHERE final_amount > paid_amount")["total"]

        status_rows = self.db.fetchall("SELECT status, COUNT(*) AS total FROM jobs GROUP BY status ORDER BY total DESC")
        service_rows = self.db.fetchall("SELECT service_type, COUNT(*) AS total FROM jobs GROUP BY service_type ORDER BY total DESC LIMIT 10")
        brand_rows = self.db.fetchall(
            """
            SELECT d.brand, COUNT(*) AS total
            FROM jobs j JOIN devices d ON d.id=j.device_id
            WHERE d.brand IS NOT NULL AND d.brand != ''
            GROUP BY d.brand ORDER BY total DESC LIMIT 10
            """
        )
        parts_rows = self.db.fetchall("SELECT part_name, SUM(quantity) AS qty FROM job_parts GROUP BY part_name ORDER BY qty DESC LIMIT 10")

        lines = []
        lines.append("HS-SMS REPORTS")
        lines.append("=" * 70)
        lines.append(f"Total Jobs        : {total_jobs}")
        lines.append(f"Monthly Jobs      : {monthly_jobs}")
        lines.append(f"Total Income      : BDT {money(total_income)}")
        lines.append(f"Monthly Income    : BDT {money(monthly_income)}")
        lines.append(f"Due Payment       : BDT {money(due)}")
        lines.append("")
        lines.append("JOB STATUS")
        lines.append("-" * 70)
        for r in status_rows:
            lines.append(f"{r['status']:<20} {r['total']}")
        lines.append("")
        lines.append("TOP SERVICES")
        lines.append("-" * 70)
        for r in service_rows:
            lines.append(f"{(r['service_type'] or 'Unknown'):<30} {r['total']}")
        lines.append("")
        lines.append("MOST REPAIRED BRANDS")
        lines.append("-" * 70)
        for r in brand_rows:
            lines.append(f"{r['brand']:<30} {r['total']}")
        lines.append("")
        lines.append("MOST USED PARTS")
        lines.append("-" * 70)
        for r in parts_rows:
            lines.append(f"{r['part_name']:<30} {r['qty']}")
        self.reports_text.delete("1.0", "end")
        self.reports_text.insert("1.0", "\n".join(lines))

    # ------------------------ SETTINGS ------------------------
    def build_settings_tab(self):
        outer = ttk.Frame(self.settings_tab, padding=8)
        outer.pack(fill="both", expand=True)

        theme_box = ttk.LabelFrame(outer, text="Theme Option", padding=7)
        theme_box.pack(fill="x", pady=(0, 10))
        ttk.Label(theme_box, text="Choose Theme").pack(side="left", padx=(0, 8))
        self.theme_var = tk.StringVar(value=self.current_theme)
        self.theme_combo = ttk.Combobox(
            theme_box,
            textvariable=self.theme_var,
            values=THEME_DISPLAY_ORDER,
            state="readonly",
            width=22,
        )
        self.theme_combo.pack(side="left")
        self.theme_combo.bind("<<ComboboxSelected>>", self.change_theme)
        ttk.Button(theme_box, text="Apply Theme", command=self.change_theme).pack(side="left", padx=8)
        ttk.Label(theme_box, text="Default Theme follows the computer theme when supported.").pack(side="left", padx=8)

        icon_box = ttk.LabelFrame(outer, text="Icon Option", padding=7)
        icon_box.pack(fill="x", pady=(0, 10))
        icon_note = (
            "To use your own software icon, replace assets/hs_sms_icon.ico before building the EXE. "
            "Keep the same file name for easiest build."
        )
        ttk.Label(icon_box, text=icon_note, wraplength=850).pack(side="left", padx=(0, 8))
        ttk.Button(icon_box, text="Open Assets Folder", command=self.open_assets_folder).pack(side="right")

        settings_area = ttk.Frame(outer)
        settings_area.pack(fill="both", expand=True)

        left = ttk.LabelFrame(settings_area, text="Device Categories", padding=7)
        left.pack(side="left", fill="both", expand=True, padx=(0, 8))
        self.new_category = tk.StringVar()
        ttk.Entry(left, textvariable=self.new_category).pack(fill="x", pady=5)
        ttk.Button(left, text="Add Category", command=self.add_category).pack(anchor="e")
        self.category_tree = ttk.Treeview(left, columns=("id", "name"), show="headings")
        self.category_tree.heading("id", text="ID")
        self.category_tree.heading("name", text="Name")
        self.category_tree.column("id", width=50)
        self.category_tree.pack(fill="both", expand=True, pady=8)

        right = ttk.LabelFrame(settings_area, text="Service Types", padding=7)
        right.pack(side="left", fill="both", expand=True)
        self.new_service = tk.StringVar()
        ttk.Entry(right, textvariable=self.new_service).pack(fill="x", pady=5)
        ttk.Button(right, text="Add Service Type", command=self.add_service_type).pack(anchor="e")
        self.service_tree = ttk.Treeview(right, columns=("id", "name"), show="headings")
        self.service_tree.heading("id", text="ID")
        self.service_tree.heading("name", text="Name")
        self.service_tree.column("id", width=50)
        self.service_tree.pack(fill="both", expand=True, pady=8)

    def add_category(self):
        name = self.new_category.get().strip()
        if not name:
            return
        self.db.execute("INSERT OR IGNORE INTO settings(setting_type, name, is_active) VALUES(?, ?, 1)", ("device_category", name))
        self.new_category.set("")
        self.refresh_all()

    def add_service_type(self):
        name = self.new_service.get().strip()
        if not name:
            return
        self.db.execute("INSERT OR IGNORE INTO settings(setting_type, name, is_active) VALUES(?, ?, 1)", ("service_type", name))
        self.new_service.set("")
        self.refresh_all()

    def load_settings(self):
        if not hasattr(self, "category_tree"):
            return
        for t in [self.category_tree, self.service_tree]:
            for row in t.get_children():
                t.delete(row)
        cats = self.db.fetchall("SELECT * FROM settings WHERE setting_type='device_category' ORDER BY name")
        services = self.db.fetchall("SELECT * FROM settings WHERE setting_type='service_type' ORDER BY name")
        for r in cats:
            self.category_tree.insert("", "end", values=(r["id"], r["name"]))
        for r in services:
            self.service_tree.insert("", "end", values=(r["id"], r["name"]))

    # ------------------------ BACKUP ------------------------
    def build_backup_tab(self):
        outer = ttk.Frame(self.backup_tab, padding=10)
        outer.pack(fill="both", expand=True)
        ttk.Label(outer, text="Backup & Restore", style="Heading.TLabel").pack(anchor="w", pady=(0, 10))

        info = (
            "Your main data is stored in data/hs_sms_v2.db.\n"
            "Backups are saved by default in your Documents folder for better safety.\n"
            "Automatic backup runs every time the app is closed.\n"
            "Restore will replace the current database, so take a backup before restoring."
        )
        ttk.Label(outer, text=info, wraplength=900).pack(anchor="w", pady=6)

        status_box = ttk.LabelFrame(outer, text="Backup Status", padding=7)
        status_box.pack(fill="x", pady=(10, 12))

        self.backup_folder_var = tk.StringVar(value=BACKUP_DIR)
        self.last_backup_var = tk.StringVar(value="Last backup: Never")
        self.last_restore_var = tk.StringVar(value="Last restore: Never")
        self.last_backup_path_var = tk.StringVar(value="Backup file: -")
        self.last_restore_path_var = tk.StringVar(value="Restored from: -")

        ttk.Label(status_box, textvariable=self.backup_folder_var).pack(anchor="w", pady=2)
        ttk.Label(status_box, textvariable=self.last_backup_var).pack(anchor="w", pady=2)
        ttk.Label(status_box, textvariable=self.last_backup_path_var).pack(anchor="w", pady=2)
        ttk.Label(status_box, textvariable=self.last_restore_var).pack(anchor="w", pady=2)
        ttk.Label(status_box, textvariable=self.last_restore_path_var).pack(anchor="w", pady=2)

        startup_box = ttk.LabelFrame(outer, text="Startup Restore Option", padding=7)
        startup_box.pack(fill="x", pady=(0, 12))
        self.ask_restore_startup_var = tk.BooleanVar(value=self.config_data.get("ask_restore_on_startup", True))
        ttk.Checkbutton(
            startup_box,
            text="Ask to restore or browse backup when the app opens",
            variable=self.ask_restore_startup_var,
            command=self.toggle_startup_restore_prompt,
        ).pack(anchor="w", pady=2)
        ttk.Label(
            startup_box,
            text="Recommended: keep this enabled for safer data recovery. Use Restore Latest or Browse Backup only when you need to recover data.",
            wraplength=900,
        ).pack(anchor="w", pady=2)

        action_box = ttk.LabelFrame(outer, text="Actions", padding=7)
        action_box.pack(fill="x", pady=(0, 12))

        ttk.Button(action_box, text="Backup SQLite Database", command=self.backup_db).pack(side="left", padx=(0, 8), pady=6)
        ttk.Button(action_box, text="Restore SQLite Database", command=self.restore_db).pack(side="left", padx=8, pady=6)
        ttk.Button(action_box, text="Export JSON Backup", command=self.export_json).pack(side="left", padx=8, pady=6)
        ttk.Button(action_box, text="Open Backup Folder", command=self.open_backup_folder).pack(side="left", padx=8, pady=6)

        note = (
            "Commercial recommendation: keep automatic/default backups in Documents, "
            "then copy important backups to Google Drive, OneDrive, or an external drive."
        )
        ttk.Label(outer, text=note, wraplength=900).pack(anchor="w", pady=6)
        self.refresh_backup_info()

    def toggle_startup_restore_prompt(self):
        self.config_data["ask_restore_on_startup"] = bool(self.ask_restore_startup_var.get())
        save_config(self.config_data)

    def refresh_backup_info(self):
        if not hasattr(self, "last_backup_var"):
            return
        self.backup_folder_var.set(f"Backup folder: {BACKUP_DIR}")
        last_backup_at = self.config_data.get("last_backup_at") or "Never"
        last_restore_at = self.config_data.get("last_restore_at") or "Never"
        last_backup_path = self.config_data.get("last_backup_path") or "-"
        last_restore_path = self.config_data.get("last_restore_path") or "-"
        self.last_backup_var.set(f"Last backup: {last_backup_at}")
        self.last_backup_path_var.set(f"Backup file: {last_backup_path}")
        self.last_restore_var.set(f"Last restore: {last_restore_at}")
        self.last_restore_path_var.set(f"Restored from: {last_restore_path}")

    def remember_backup_event(self, key_prefix, path):
        timestamp = now_text()
        self.config_data[f"last_{key_prefix}_at"] = timestamp
        self.config_data[f"last_{key_prefix}_path"] = path
        save_config(self.config_data)
        self.refresh_backup_info()

    def open_folder(self, folder_path):
        os.makedirs(folder_path, exist_ok=True)
        try:
            if sys.platform.startswith("win"):
                os.startfile(folder_path)
            elif sys.platform == "darwin":
                import subprocess
                subprocess.Popen(["open", folder_path])
            else:
                import subprocess
                subprocess.Popen(["xdg-open", folder_path])
        except Exception as exc:
            messagebox.showerror("Open Folder Failed", f"Could not open folder:\n{folder_path}\n\n{exc}")

    def open_backup_folder(self):
        self.open_folder(BACKUP_DIR)

    def open_assets_folder(self):
        self.open_folder(ASSETS_DIR)

    def backup_db(self):
        if not os.path.exists(DB_FILE):
            messagebox.showerror("Error", "Database file not found.")
            return
        os.makedirs(BACKUP_DIR, exist_ok=True)
        default_name = f"hs_sms_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
        path = filedialog.asksaveasfilename(
            defaultextension=".db",
            initialdir=BACKUP_DIR,
            initialfile=default_name,
            filetypes=[("SQLite DB", "*.db")],
        )
        if not path:
            return
        self.db.conn.commit()
        shutil.copy2(DB_FILE, path)
        self.remember_backup_event("backup", path)
        messagebox.showinfo("Backup Complete", f"Database backup saved:\n{path}")

    def restore_db(self):
        os.makedirs(BACKUP_DIR, exist_ok=True)
        path = filedialog.askopenfilename(
            initialdir=BACKUP_DIR,
            filetypes=[("SQLite DB", "*.db"), ("All Files", "*.*")],
        )
        if not path:
            return
        if not messagebox.askyesno("Confirm Restore", "Restore will replace the current database. Continue?"):
            return
        self.restore_database_from_path(path, show_message=True)

    def export_json(self):
        tables = ["customers", "devices", "jobs", "work_logs", "job_parts", "settings", "activity_logs"]
        data = {}
        for table in tables:
            rows = self.db.fetchall(f"SELECT * FROM {table}")
            data[table] = [dict(r) for r in rows]
        os.makedirs(BACKUP_DIR, exist_ok=True)
        default_name = f"hs_sms_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        path = filedialog.asksaveasfilename(
            defaultextension=".json",
            initialdir=BACKUP_DIR,
            initialfile=default_name,
            filetypes=[("JSON", "*.json")],
        )
        if not path:
            return
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        self.remember_backup_event("backup", path)
        messagebox.showinfo("Export Complete", f"JSON backup saved:\n{path}")


    # ------------------------ ABOUT ------------------------
    def build_about_tab(self):
        outer = ttk.Frame(self.about_tab, padding=12)
        outer.pack(fill="both", expand=True)
        ttk.Label(outer, text=APP_TITLE, style="Heading.TLabel").pack(anchor="w", pady=(0, 8))
        about = (
            "Commercial Offline Desktop Edition\n\n"
            f"Brand: {COMPANY_NAME}\n"
            f"Website: {DOWNLOAD_PAGE}\n"
            f"Version: {APP_VERSION}\n\n"
            "This software is designed for computer, laptop, UPS, printer, GPU, networking, CCTV, "
            "and general repair/service businesses. It works offline with a local SQLite database.\n\n"
            "Recommended use:\n"
            "1. Keep the full app folder in a safe location.\n"
            "2. Do not delete the data folder.\n"
            "3. Take daily backup from the Backup tab.\n"
            "4. For client delivery, compile this file into a Windows EXE using build_windows_exe.bat."
        )
        ttk.Label(outer, text=about, justify="left", wraplength=900).pack(anchor="w", pady=8)
        ttk.Separator(outer).pack(fill="x", pady=14)
        ttk.Label(outer, text="Modules Included", style="Card.TLabel").pack(anchor="w")
        modules = "Dashboard, Customers, Devices, Service Jobs, Work Logs, Parts Used, Invoice, Warranty, Reports, Default Theme, Advanced Dark Themes, Glass/iMac/Ubuntu Themes, Icon Option, Settings, Backup/Restore, Auto Close Backup, Startup Restore Prompt, Open Backup Folder."
        ttk.Label(outer, text=modules, wraplength=900).pack(anchor="w", pady=6)


if __name__ == "__main__":
    app = HSSMSApp()
    app.mainloop()
