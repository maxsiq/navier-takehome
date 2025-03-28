import os

DB_LOCATION = os.environ.get("DB", "./database.sqlite3")
MIGRATION_DB_URL = f"sqlite:///{DB_LOCATION}"
DB_URL = f"sqlite+aiosqlite:///./{DB_LOCATION}"
