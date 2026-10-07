"""SQLite storage: every report is saved as a JSON document (plus its charts)."""
import json, os, sqlite3
from contextlib import closing
from datetime import datetime, timedelta
import config

DB_PATH = config.DB_PATH


def _conn():
    os.makedirs(os.path.dirname(DB_PATH) or ".", exist_ok=True)
    c = sqlite3.connect(DB_PATH)
    c.row_factory = sqlite3.Row
    return c


def init_db():
    with closing(_conn()) as c:
        c.execute("""CREATE TABLE IF NOT EXISTS reports(
            id TEXT PRIMARY KEY,
            filename TEXT NOT NULL,
            created_at TEXT NOT NULL,
            total_rows INTEGER, flagged_rows INTEGER, risk_rating TEXT,
            report_json TEXT NOT NULL,
            charts_json TEXT NOT NULL)""")
        c.commit()


def save_report(rid, filename, report: dict, charts: dict):
    s = report["summary"]
    with closing(_conn()) as c:
        c.execute("INSERT OR REPLACE INTO reports VALUES (?,?,?,?,?,?,?,?)",
                  (rid, filename, report["scanned_at"], s["total"], s["flagged"],
                   report["verdict"]["rating"],
                   json.dumps(report), json.dumps(charts)))
        c.commit()


def get_report(rid):
    with closing(_conn()) as c:
        r = c.execute("SELECT * FROM reports WHERE id=?", (rid,)).fetchone()
    if not r:
        return None
    return {"id": r["id"], "filename": r["filename"],
            "report": json.loads(r["report_json"]), "charts": json.loads(r["charts_json"])}


def list_reports(limit=100):
    with closing(_conn()) as c:
        rows = c.execute("""SELECT id, filename, created_at, total_rows, flagged_rows, risk_rating
                            FROM reports ORDER BY created_at DESC LIMIT ?""", (limit,)).fetchall()
    return [dict(r) for r in rows]


def delete_report(rid):
    with closing(_conn()) as c:
        c.execute("DELETE FROM reports WHERE id=?", (rid,))
        c.commit()


def purge_older_than(days):
    """Privacy: delete reports older than N days. Returns ids removed."""
    cutoff = (datetime.now() - timedelta(days=days)).isoformat(timespec="seconds")
    with closing(_conn()) as c:
        ids = [r["id"] for r in c.execute("SELECT id FROM reports WHERE created_at < ?", (cutoff,))]
        c.execute("DELETE FROM reports WHERE created_at < ?", (cutoff,))
        c.commit()
    return ids
