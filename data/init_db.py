import os
from pathlib import Path
from sqlite3 import connect, Connection, Cursor, IntegrityError

conn: Connection | None = None
curs: Cursor | None = None

def get_db(name: str|None = None, reset: bool = False):
    """Connect to SQLite database file"""
    global conn, curs
    if conn:
        if not reset:
            return
        conn = None
    if not name:
        top_dir = Path(__file__).resolve().parents[1]
        db_path = os.path.join(top_dir, 'data', 'employees.db')
        
    conn = connect(db_path, check_same_thread=False)
    curs = conn.cursor()
get_db()