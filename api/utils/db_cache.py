import sqlite3
import json
import datetime
import os

DATABASE_FILE = os.path.join(os.path.dirname(__file__), "events_cache.db")
CACHE_EXPIRY_SECONDS = 3600


def connect_db():
    connection = sqlite3.connect(DATABASE_FILE)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    with connect_db() as connect:
        cursor = connect.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS cached_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_prefix TEXT NOT NULL,
                year INTEGER NOT NULL,
                month INTEGER NOT NULL,
                day INTEGER NOT NULL,
                event_data TEXT NOT NULL,
                cached_timestamp REAL NOT NULL,
                UNIQUE(user_prefix, year, month, day)
            )
        """
        )
        connect.commit()


def save_events_to_cache(user_prefix, year, month, events_by_day):
    with connect_db() as connect:
        cursor = connect.cursor()
        cached_timestamp = datetime.datetime.now().timestamp()

        cursor.execute(
            """
            DELETE FROM cached_events
            WHERE user_prefix = ? AND year = ? AND month = ?
        """,
            (user_prefix, year, month),
        )

        for day, events_list in events_by_day.items():
            event_json = json.dumps(events_list)
            cursor.execute(
                """
                INSERT INTO cached_events (user_prefix, year, month, day, event_data, cached_timestamp)
                VALUES (?, ?, ?, ?, ?, ?)
            """,
                (user_prefix, year, month, day, event_json, cached_timestamp),
            )
        connect.commit()


def load_events_from_cache(user_prefix, year, month):
    events_by_day = {}
    with connect_db() as connect:
        cursor = connect.cursor()
        cursor.execute(
            """
            SELECT day, event_data, cached_timestamp
            FROM cached_events
            WHERE user_prefix = ? AND year = ? AND month = ?
        """,
            (user_prefix, year, month),
        )
        rows = cursor.fetchall()

        if not rows:
            return None

        first_row_timestamp = rows[0]["cached_timestamp"]
        if (
            datetime.datetime.now().timestamp() - first_row_timestamp
        ) > CACHE_EXPIRY_SECONDS:
            print(f"Cache for {user_prefix} {month}/{year} expired. Clearing...")
            delete_expired_events(user_prefix, year, month)
            return None

        for row in rows:
            day = row["day"]
            events_by_day[day] = json.loads(row["event_data"])
    return events_by_day


def delete_expired_events(user_prefix, year, month):
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            DELETE FROM cached_events
            WHERE user_prefix = ? AND year = ? AND month = ?
        """,
            (user_prefix, year, month),
        )
        conn.commit()


def clear_all_cache():
    """Clears all cached events from the database."""
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM cached_events")
        conn.commit()
        print("All cached events cleared from SQLite database.")


init_db()
