import sqlite3
from datetime import datetime
from typing import Optional, List, Dict

DB_FILE = None

def get_conn():
    global DB_FILE
    if DB_FILE is None:
        DB_FILE = 'data.db'
    conn = sqlite3.connect(DB_FILE, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db(db_file: Optional[str] = None):
    global DB_FILE
    if db_file:
        DB_FILE = db_file
    conn = get_conn()
    cur = conn.cursor()
    cur.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        telegram_id INTEGER UNIQUE,
        username TEXT,
        balance REAL DEFAULT 0,
        referrer_id INTEGER,
        referral_code TEXT UNIQUE,
        created_at TEXT
    )
    ''')
    cur.execute('''
    CREATE TABLE IF NOT EXISTS investments (
        id INTEGER PRIMARY KEY,
        user_id INTEGER,
        amount REAL,
        plan TEXT,
        start_date TEXT,
        active INTEGER DEFAULT 1
    )
    ''')
    cur.execute('''
    CREATE TABLE IF NOT EXISTS withdrawals (
        id INTEGER PRIMARY KEY,
        user_id INTEGER,
        amount REAL,
        status TEXT,
        created_at TEXT
    )
    ''')
    cur.execute('''
    CREATE TABLE IF NOT EXISTS receipts (
        id INTEGER PRIMARY KEY,
        user_id INTEGER,
        investment_id INTEGER,
        file_id TEXT,
        file_type TEXT,
        created_at TEXT
    )
    ''')
    conn.commit()

def create_user(telegram_id: int, username: str, referral_code: str, referrer_id: Optional[int]):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute('INSERT OR IGNORE INTO users (telegram_id, username, referral_code, referrer_id, created_at) VALUES (?, ?, ?, ?, ?)',
                (telegram_id, username, referral_code, referrer_id, datetime.utcnow().isoformat()))
    conn.commit()
    cur.execute('SELECT * FROM users WHERE telegram_id=?', (telegram_id,))
    row = cur.fetchone()
    return dict(row) if row else None

def get_user_by_telegram(telegram_id: int):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute('SELECT * FROM users WHERE telegram_id=?', (telegram_id,))
    row = cur.fetchone()
    return dict(row) if row else None

def get_user_by_refcode(code: str):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute('SELECT * FROM users WHERE referral_code=?', (code,))
    row = cur.fetchone()
    return dict(row) if row else None

def add_investment(user_id: int, amount: float, plan: str):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute('INSERT INTO investments (user_id, amount, plan, start_date, active) VALUES (?, ?, ?, ?, ?)',
                (user_id, amount, plan, datetime.utcnow().isoformat(), 0))
    conn.commit()
    return cur.lastrowid

def add_active_investment(user_id: int, amount: float, plan: str):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute('INSERT INTO investments (user_id, amount, plan, start_date, active) VALUES (?, ?, ?, ?, ?)',
                (user_id, amount, plan, datetime.utcnow().isoformat(), 1))
    conn.commit()
    return cur.lastrowid

def list_user_investments(user_id: int) -> List[Dict]:
    conn = get_conn()
    cur = conn.cursor()
    cur.execute('SELECT * FROM investments WHERE user_id=?', (user_id,))
    return [dict(r) for r in cur.fetchall()]

def update_user_balance(user_id: int, delta: float):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute('UPDATE users SET balance = balance + ? WHERE id=?', (delta, user_id))
    conn.commit()

def get_all_active_investments():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute('SELECT * FROM investments WHERE active=1')
    return [dict(r) for r in cur.fetchall()]

def get_pending_investments():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute('SELECT * FROM investments WHERE active=0')
    return [dict(r) for r in cur.fetchall()]

def list_all_users():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute('SELECT * FROM users ORDER BY id DESC')
    return [dict(r) for r in cur.fetchall()]

def get_all_receipts():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute('SELECT * FROM receipts ORDER BY created_at DESC')
    return [dict(r) for r in cur.fetchall()]

def get_latest_investment_for_user(user_id: int):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute('SELECT * FROM investments WHERE user_id=? ORDER BY id DESC LIMIT 1', (user_id,))
    row = cur.fetchone()
    return dict(row) if row else None

def mark_investment_active(investment_id: int):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute('UPDATE investments SET active=1 WHERE id=?', (investment_id,))
    conn.commit()

def add_receipt(user_id: int, investment_id: int, file_id: str, file_type: str):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute('''INSERT INTO receipts (user_id, investment_id, file_id, file_type, created_at)
                   VALUES (?, ?, ?, ?, ?)''', (user_id, investment_id, file_id, file_type, datetime.utcnow().isoformat()))
    conn.commit()
    return cur.lastrowid

def get_investment_by_id(investment_id: int):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute('SELECT * FROM investments WHERE id=?', (investment_id,))
    row = cur.fetchone()
    return dict(row) if row else None

def get_user_by_id(uid: int):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute('SELECT * FROM users WHERE id=?', (uid,))
    row = cur.fetchone()
    return dict(row) if row else None

def get_referrals_of(user_id: int):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute('SELECT * FROM users WHERE referrer_id=?', (user_id,))
    return [dict(r) for r in cur.fetchall()]

def add_withdrawal_request(user_id: int, amount: float):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute('INSERT INTO withdrawals (user_id, amount, status, created_at) VALUES (?, ?, ?, ?)',
                (user_id, amount, 'pending', datetime.utcnow().isoformat()))
    conn.commit()
