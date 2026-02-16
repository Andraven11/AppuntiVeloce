"""
Modulo Appunti Veloce - Database SQLite con best practice di sicurezza.
Fonti: OWASP, blackhawk.sh, dev.to - SQLite security best practices.
"""

import sqlite3
import os
from pathlib import Path
from typing import Optional

# Path database: directory utente locale, non condivisa
# Windows: %LOCALAPPDATA%; Linux/macOS: ~/.local/share
DB_DIR = Path(
    os.environ.get("LOCALAPPDATA") or
    os.environ.get("XDG_DATA_HOME", str(Path.home() / ".local" / "share"))
) / "AppuntiVeloce"
DB_PATH = DB_DIR / "appunti.db"

# Limite lunghezza contenuto (previene DoS)
MAX_CONTENT_LENGTH = 10000


def _get_connection() -> sqlite3.Connection:
    """Crea connessione con PRAGMA di sicurezza applicati."""
    DB_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row  # Accesso colonne per nome

    # Best practice sicurezza (blackhawk.sh, OWASP)
    conn.executescript("""
        PRAGMA foreign_keys = ON;
        PRAGMA journal_mode = WAL;
        PRAGMA synchronous = FULL;
        PRAGMA temp_store = MEMORY;
    """)
    conn.execute("PRAGMA query_only = 0")

    # Disabilita caricamento estensioni (riduce attack surface)
    conn.enable_load_extension(False)

    return conn


def _init_db(conn: sqlite3.Connection) -> None:
    """Inizializza tabella appunti se non esiste."""
    conn.execute("""
        CREATE TABLE IF NOT EXISTS appunti (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            contenuto TEXT NOT NULL,
            creato DATETIME DEFAULT CURRENT_TIMESTAMP,
            modificato DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()


def _sanitize_content(contenuto: str) -> str:
    """Valida e tronca il contenuto. Previene input malevoli."""
    if not isinstance(contenuto, str):
        raise ValueError("Il contenuto deve essere una stringa")
    testo = contenuto.strip()
    if len(testo) > MAX_CONTENT_LENGTH:
        testo = testo[:MAX_CONTENT_LENGTH]
    return testo


def crea(contenuto: str) -> int:
    """Crea un nuovo appunto. Restituisce l'id."""
    testo = _sanitize_content(contenuto)
    if not testo:
        raise ValueError("Il contenuto non può essere vuoto")

    conn = _get_connection()
    try:
        _init_db(conn)
        cur = conn.execute(
            "INSERT INTO appunti (contenuto) VALUES (?)",
            (testo,)
        )
        conn.commit()
        return cur.lastrowid
    finally:
        conn.close()


def leggi(id_appunto: Optional[int] = None) -> list:
    """Legge appunti. Se id_appunto è None, restituisce tutti."""
    conn = _get_connection()
    try:
        _init_db(conn)
        if id_appunto is not None:
            cur = conn.execute(
                "SELECT id, contenuto, creato, modificato FROM appunti WHERE id = ?",
                (id_appunto,)
            )
        else:
            cur = conn.execute(
                "SELECT id, contenuto, creato, modificato FROM appunti ORDER BY modificato DESC"
            )
        rows = cur.fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


def aggiorna(id_appunto: int, contenuto: str) -> bool:
    """Aggiorna un appunto esistente. Restituisce True se modificato."""
    testo = _sanitize_content(contenuto)
    if not testo:
        raise ValueError("Il contenuto non può essere vuoto")

    conn = _get_connection()
    try:
        cur = conn.execute(
            """UPDATE appunti SET contenuto = ?, modificato = CURRENT_TIMESTAMP
               WHERE id = ?""",
            (testo, id_appunto)
        )
        conn.commit()
        return cur.rowcount > 0
    finally:
        conn.close()


def elimina(id_appunto: int) -> bool:
    """Elimina un appunto. Restituisce True se eliminato."""
    conn = _get_connection()
    try:
        cur = conn.execute("DELETE FROM appunti WHERE id = ?", (id_appunto,))
        conn.commit()
        return cur.rowcount > 0
    finally:
        conn.close()


def get_db_path() -> Path:
    """Restituisce il path del file database (utile per backup)."""
    return DB_PATH
