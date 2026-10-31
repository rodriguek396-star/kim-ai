import sqlite3, json
from pathlib import Path
from contextlib import contextmanager
from .config import settings

SEED_ACTIVITIES = [
 ("ACT-01","Taekwondo débutant","Sport","8–14 ans · débutant","Initiation aux techniques fondamentales du taekwondo.",4),
 ("ACT-02","Atelier Python","Numérique","15 ans et +","Découvrir la programmation avec Python.",18),
 ("ACT-03","Initiation au design numérique","Numérique","Tout public","Créer une première interface et comprendre les bases UX.",12),
 ("ACT-04","Club de lecture coréenne","Culture","Tout public","Découverte de la langue et de la culture coréennes.",10),
 ("ACT-05","Danse traditionnelle","Culture","Tout public","Atelier de découverte des danses traditionnelles.",14),
 ("ACT-06","Échecs & stratégie","Sport & loisirs","Tout public","Initiation et pratique des échecs.",16),
]

def connect():
    if settings.storage_mode == "snowflake":
        from .services.snowflake_store import snowflake_connection
        return snowflake_connection()
    conn = sqlite3.connect(settings.sqlite_path, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

@contextmanager
def db():
    conn = connect()
    try:
        yield conn
        if settings.storage_mode != "snowflake": conn.commit()
    finally:
        conn.close()

def init_db():
    if settings.storage_mode == "snowflake": return
    Path(settings.sqlite_path).parent.mkdir(parents=True, exist_ok=True)
    with db() as c:
        c.executescript('''
        CREATE TABLE IF NOT EXISTS activities(id TEXT PRIMARY KEY,name TEXT,category TEXT,eligibility TEXT,description TEXT,places INTEGER,active INTEGER DEFAULT 1);
        CREATE TABLE IF NOT EXISTS requests(id TEXT PRIMARY KEY,type TEXT,payload TEXT,status TEXT DEFAULT 'PENDING',created_at TEXT DEFAULT CURRENT_TIMESTAMP,admin_note TEXT);
        CREATE TABLE IF NOT EXISTS messages(id INTEGER PRIMARY KEY AUTOINCREMENT,session_id TEXT,role TEXT,content TEXT,created_at TEXT DEFAULT CURRENT_TIMESTAMP);
        CREATE TABLE IF NOT EXISTS rooms(id TEXT PRIMARY KEY,name TEXT,capacity INTEGER,equipment TEXT,active INTEGER DEFAULT 1);
        ''')
        count = c.execute('SELECT COUNT(*) FROM activities').fetchone()[0]
        if count == 0: c.executemany('INSERT INTO activities(id,name,category,eligibility,description,places) VALUES(?,?,?,?,?,?)', SEED_ACTIVITIES)
        if c.execute('SELECT COUNT(*) FROM rooms').fetchone()[0] == 0:
            c.executemany('INSERT INTO rooms(id,name,capacity,equipment) VALUES(?,?,?,?)', [('R-01','Salle polyvalente',80,'Projecteur, sonorisation'),('R-02','Salle de formation',24,'Écran, tableau'),('R-03','Studio créatif',16,'Écran, postes informatiques')])
