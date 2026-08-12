from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

OPERATIONS_FILE = BASE_DIR / "data" / "operations.xlsx"
USER_SETTINGS_FILE = BASE_DIR / "user_settings.json"
WEEKDAY_REPORT_FILE = BASE_DIR / "data" / "weekday_report.json"
