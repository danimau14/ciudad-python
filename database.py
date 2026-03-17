import sqlite3, time, hashlib, os


def _get_db_path():
    for d in ["/tmp", os.path.expanduser("~"), os.getcwd()]:
        try:
            t = os.path.join(d, "_tw.tmp")
            open(t, "w").close()
            os.remove(t)
            return os.path.join(d, "database.db")
        except Exception:
            continue
    return "database.db"


DB_PATH = _get_db_path()
