"""Storage: one SQLite table, six queries, no ORM.

A connection is opened per request (see ``get_db``) because FastAPI runs
``def`` endpoints in a thread pool, and a ``sqlite3.Connection`` may not be
shared across threads. Opening a connection to a local file is cheap.
"""

from __future__ import annotations

import sqlite3
from collections.abc import Iterator
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

DB_PATH = Path(__file__).resolve().parent.parent / "todos.db"

#: Which todos a list is showing. Also the set of values the URL accepts.
Filter = Literal["all", "active", "done"]

SCHEMA = """
CREATE TABLE IF NOT EXISTS todos (
    id    INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT    NOT NULL,
    done  INTEGER NOT NULL DEFAULT 0
)
"""


@dataclass(frozen=True, slots=True)
class Todo:
    id: int
    title: str
    done: bool

    @classmethod
    def from_row(cls, row: sqlite3.Row) -> Todo:
        return cls(id=row["id"], title=row["title"], done=bool(row["done"]))

    def matches(self, todo_filter: Filter) -> bool:
        """Whether this todo belongs in a list rendered under ``todo_filter``.

        The templates ask this to decide whether a row that just changed should
        be re-rendered or dropped: checking something off while the "Active"
        filter is on removes it from that view.
        """
        return todo_filter == "all" or (todo_filter == "done") == self.done


def init_db() -> None:
    conn = sqlite3.connect(DB_PATH)
    try:
        conn.execute(SCHEMA)
        conn.commit()
    finally:
        conn.close()


def get_db() -> Iterator[sqlite3.Connection]:
    """FastAPI dependency: a connection that is committed and closed per request."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def list_todos(conn: sqlite3.Connection, todo_filter: Filter) -> list[Todo]:
    sql = "SELECT id, title, done FROM todos"
    if todo_filter == "active":
        sql += " WHERE done = 0"
    elif todo_filter == "done":
        sql += " WHERE done = 1"
    sql += " ORDER BY id DESC"
    return [Todo.from_row(row) for row in conn.execute(sql)]


def get_todo(conn: sqlite3.Connection, todo_id: int) -> Todo | None:
    row = conn.execute(
        "SELECT id, title, done FROM todos WHERE id = ?", (todo_id,)
    ).fetchone()
    return Todo.from_row(row) if row else None


def create_todo(conn: sqlite3.Connection, title: str) -> Todo:
    cursor = conn.execute("INSERT INTO todos (title) VALUES (?)", (title,))
    return Todo(id=int(cursor.lastrowid), title=title, done=False)


def toggle_todo(conn: sqlite3.Connection, todo_id: int) -> Todo | None:
    """Flip ``done`` and return the stored row.

    The new state is derived from the database, not sent by the browser, so the
    response is the truth and a row that has drifted out of sync corrects
    itself on the next click.
    """
    row = conn.execute(
        "UPDATE todos SET done = NOT done WHERE id = ? RETURNING id, title, done",
        (todo_id,),
    ).fetchone()
    return Todo.from_row(row) if row else None


def delete_todo(conn: sqlite3.Connection, todo_id: int) -> bool:
    return conn.execute("DELETE FROM todos WHERE id = ?", (todo_id,)).rowcount > 0


def count_active(conn: sqlite3.Connection) -> int:
    return conn.execute("SELECT count(*) FROM todos WHERE done = 0").fetchone()[0]
