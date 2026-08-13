"""Routes.

Every endpoint returns HTML. Five of them, and the only difference between the
full page and a fragment is how much of the same template tree gets rendered:

    GET    /                    the page
    GET    /todos               the panel (filter chips, counter, list)
    POST   /todos               a new row, prepended
    POST   /todos/{id}/toggle   that one row, re-rendered
    DELETE /todos/{id}          nothing, which removes that one row

Fragment responses also carry an out-of-band copy of the "N left" counter, so
the count stays right without any endpoint needing to know where on the page it
is drawn.
"""

from __future__ import annotations

import sqlite3
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Annotated

from fastapi import Depends, FastAPI, Form, HTTPException, Query, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app import db
from app.db import Filter

BASE_DIR = Path(__file__).resolve().parent

#: Shown in place of the list when a filter matches nothing.
EMPTY_TEXT: dict[Filter, str] = {
    "all": "Nothing here yet. Add your first todo above.",
    "active": "No active todos. Enjoy the quiet.",
    "done": "Nothing completed yet.",
}


@asynccontextmanager
async def lifespan(app: FastAPI):
    db.init_db()
    yield


app = FastAPI(lifespan=lifespan)
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")

templates = Jinja2Templates(directory=BASE_DIR / "templates")

Connection = Annotated[sqlite3.Connection, Depends(db.get_db)]

#: ``?filter=`` on every route. FastAPI rejects anything outside the Literal,
#: so a template never has to defend against an unknown filter name.
FilterQuery = Annotated[Filter, Query(alias="filter")]


def panel_context(conn: sqlite3.Connection, todo_filter: Filter) -> dict:
    return {
        "todos": db.list_todos(conn, todo_filter),
        "active_count": db.count_active(conn),
        "filter": todo_filter,
        "empty_text": EMPTY_TEXT[todo_filter],
    }


def row_response(
    request: Request,
    conn: sqlite3.Connection,
    todo: db.Todo,
    todo_filter: Filter,
):
    """One changed row plus the counter — the answer to adding and to toggling.

    The template drops the row when it no longer matches ``todo_filter``, which
    is how checking something off under "Active" removes it from the list.
    """
    return templates.TemplateResponse(
        request,
        "partials/row_and_count.html",
        {
            "todo": todo,
            "active_count": db.count_active(conn),
            "filter": todo_filter,
            "oob": True,
        },
    )


@app.get("/")
def index(request: Request, conn: Connection, todo_filter: FilterQuery = "all"):
    """The whole page. Also what a browser reload of a filtered view returns."""
    return templates.TemplateResponse(
        request, "index.html", panel_context(conn, todo_filter)
    )


@app.get("/todos")
def todo_panel(request: Request, conn: Connection, todo_filter: FilterQuery = "all"):
    """The panel on its own — the filter chips' response.

    Re-rendering the chips along with the list is what keeps exactly one of them
    selected: the server decides which, so the chips' own click-to-toggle state
    cannot drift out of agreement with the list below them.
    """
    return templates.TemplateResponse(
        request, "partials/panel.html", panel_context(conn, todo_filter)
    )


@app.post("/todos")
def add_todo(
    request: Request,
    conn: Connection,
    # Defaulted, not required: FastAPI reports an empty form value as a *missing*
    # field, so declaring `title` required would answer it with a 422 and its own
    # JSON body — past htmx, which does not swap error responses. The default
    # lets the request reach the check below, which owns the message users read.
    title: Annotated[str, Form()] = "",
    todo_filter: FilterQuery = "all",
):
    """Create one todo and return its row.

    The field is `required`, so the browser already refuses an empty submission
    and paints its own message — this check is the other half: whitespace, which
    satisfies `required` and is still not a title, and anything arriving from a
    client that is not a browser.

    A rejected title comes back as the field itself, in its error state, with
    ``HX-Retarget`` pointing htmx at the field instead of the list it was told
    to append to. Being the response's main swap matters: htmx restores focus
    after a main swap when the focused element was replaced and the replacement
    carries the same id, so a user who submitted from the keyboard stays in the
    field. An out-of-band swap gets no such treatment.
    """
    title = title.strip()
    if not title:
        return templates.TemplateResponse(
            request,
            "partials/composer_field.html",
            {"error": "A todo needs a title"},
            headers={"HX-Retarget": "#new-title", "HX-Reswap": "outerHTML"},
        )
    return row_response(request, conn, db.create_todo(conn, title), todo_filter)


@app.post("/todos/{todo_id}/toggle")
def toggle_todo(
    request: Request,
    conn: Connection,
    todo_id: int,
    todo_filter: FilterQuery = "all",
):
    """Flip one todo and return its row."""
    todo = db.toggle_todo(conn, todo_id)
    if todo is None:
        raise HTTPException(status_code=404, detail="No such todo")
    return row_response(request, conn, todo, todo_filter)


@app.delete("/todos/{todo_id}")
def remove_todo(request: Request, conn: Connection, todo_id: int):
    """Delete one todo. The response body is only the counter, so the row this
    request came from is replaced by nothing."""
    if not db.delete_todo(conn, todo_id):
        raise HTTPException(status_code=404, detail="No such todo")
    return templates.TemplateResponse(
        request,
        "partials/count.html",
        {"active_count": db.count_active(conn), "oob": True},
    )
