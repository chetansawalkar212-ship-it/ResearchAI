
import sqlite3
import os
import json

DB_PATH = os.path.join("data", "researchai.db")


def create_tables():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

    connection = sqlite3.connect(DB_PATH)

    try:
        cursor = connection.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS chat_messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                role TEXT NOT NULL,
                message TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        cursor.execute("PRAGMA table_info(chat_messages)")
        columns = [column[1] for column in cursor.fetchall()]

        if "sources" not in columns:
            cursor.execute(
                "ALTER TABLE chat_messages ADD COLUMN sources TEXT"
            )
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS research_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                topic TEXT NOT NULL,
                report TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        connection.commit()

    finally:
        connection.close()


def save_message(session_id, role, message, sources=None):
    connection = sqlite3.connect(DB_PATH)

    try:
        cursor = connection.cursor()

        sources_json = json.dumps(sources or [])

        cursor.execute("""
            INSERT INTO chat_messages
            (session_id, role, message, sources)
            VALUES (?, ?, ?, ?)
        """, (session_id, role, message, sources_json))

        connection.commit()

    finally:
        connection.close()


def load_messages(session_id):
    connection = sqlite3.connect(DB_PATH)

    try:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT role, message, sources
            FROM chat_messages
            WHERE session_id = ?
            ORDER BY id ASC
        """, (session_id,))

        rows = cursor.fetchall()

        messages = []

        for role, message, sources in rows:
            try:
                parsed_sources = json.loads(sources) if sources else []
            except (json.JSONDecodeError, TypeError):
                parsed_sources = []

            messages.append({
                "role": role,
                "content": message,
                "sources": parsed_sources
            })

        return messages

    finally:
        connection.close()


def clear_messages(session_id):
    connection = sqlite3.connect(DB_PATH)

    try:
        cursor = connection.cursor()

        cursor.execute("""
            DELETE FROM chat_messages
            WHERE session_id = ?
        """, (session_id,))

        connection.commit()

    finally:
        connection.close()


def save_research(topic, report):
    connection = sqlite3.connect(DB_PATH)

    try:
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO research_history (topic, report)
            VALUES (?, ?)
        """, (topic, report))

        connection.commit()

    finally:
        connection.close()


def load_recent_research(limit=5):
    connection = sqlite3.connect(DB_PATH)

    try:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT topic, created_at
            FROM research_history
            ORDER BY id DESC
            LIMIT ?
        """, (limit,))

        return cursor.fetchall()

    finally:
        connection.close()