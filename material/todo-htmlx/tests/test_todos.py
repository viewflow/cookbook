"""What each response contains, which for an htmx app is the whole contract.

These assert on fragments rather than rendered appearance: that a toggle under
one filter returns a row and under another returns none, that the counter rides
along out of band, that a rejected title comes back as a retargeted field.
"""

from fastapi.testclient import TestClient
import pytest

from app import db
from app.main import CSRF_COOKIE, CSRF_HEADER, app


@pytest.fixture
def client(tmp_path, monkeypatch):
    monkeypatch.setattr(db, "DB_PATH", tmp_path / "test.db")
    # The context manager runs the lifespan, which creates the schema.
    with TestClient(app) as test_client:
        test_client.get("/")
        yield test_client


def add(client, title, todo_filter="all"):
    return client.post(
        f"/todos?filter={todo_filter}",
        data={"title": title},
        headers={CSRF_HEADER: client.cookies[CSRF_COOKIE]},
    )


def csrf_headers(client):
    return {CSRF_HEADER: client.cookies[CSRF_COOKIE]}


def test_index_renders_the_page(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "<material-list id=\"todo-list\"" in response.text
    assert "0 left" in response.text


def test_filter_panel_updates_the_composer_target(client):
    response = client.get("/todos?filter=done")
    assert 'hx-post="/todos?filter=done"' in response.text


def test_add_returns_the_row_and_the_counter(client):
    response = add(client, "Buy milk")
    assert response.status_code == 200
    assert 'id="todo-1"' in response.text
    assert "Buy milk" in response.text
    # The counter comes back out of band, so the response carries both.
    assert 'id="todo-count"' in response.text
    assert 'hx-swap-oob="true"' in response.text
    assert "1 left" in response.text
    assert 'class="todo-new"' in response.text


def test_writes_require_a_matching_csrf_token(client):
    response = client.post("/todos", data={"title": "Buy milk"})
    assert response.status_code == 403
    assert "0 left" in client.get("/todos?filter=all").text

    add(client, "Buy milk")
    assert (
        client.post(
            "/todos/1/toggle", headers={CSRF_HEADER: "not-the-cookie-token"}
        ).status_code
        == 403
    )
    assert client.request("DELETE", "/todos/1").status_code == 403
    assert "Buy milk" in client.get("/todos?filter=all").text


def test_add_strips_whitespace(client):
    add(client, "   Padded   ")
    assert ">Padded<" in client.get("/todos?filter=all").text


def test_blank_title_is_rejected_as_a_retargeted_field(client):
    # Whitespace is what gets here in practice: it satisfies the field's
    # `required`, so the browser lets it through.
    response = add(client, "   ")
    assert response.status_code == 200
    assert response.headers["HX-Retarget"] == "#new-title"
    assert response.headers["HX-Reswap"] == "outerHTML"
    assert 'error error-text="A todo needs a title"' in response.text
    # No row, and nothing stored.
    assert "material-list-item" not in response.text
    assert "0 left" in client.get("/todos?filter=all").text


def test_titles_are_escaped(client):
    response = add(client, '<script>alert("x")</script>')
    assert "<script>" not in response.text
    assert "&lt;script&gt;" in response.text


def test_toggle_returns_the_row_when_it_still_matches(client):
    add(client, "Buy milk")
    response = client.post("/todos/1/toggle?filter=all", headers=csrf_headers(client))
    assert 'id="todo-1"' in response.text
    assert "line-through" in response.text
    assert "0 left" in response.text


def test_toggle_drops_the_row_when_it_leaves_the_filter(client):
    add(client, "Buy milk")
    response = client.post(
        "/todos/1/toggle?filter=active", headers=csrf_headers(client)
    )
    # Done, so it no longer belongs in an "active" list: counter only.
    assert "material-list-item" not in response.text
    assert 'id="todo-count"' in response.text
    assert "0 left" in response.text


def test_add_under_the_done_filter_redirects_to_active(client):
    response = add(client, "Buy milk", todo_filter="done")
    assert response.headers["HX-Redirect"] == "/?filter=active&new=1"
    active = client.get("/?filter=active&new=1").text
    assert "Buy milk" in active
    assert 'class="todo-new"' in active


def test_delete_returns_only_the_counter(client):
    add(client, "Buy milk")
    add(client, "Write the article")
    response = client.request("DELETE", "/todos/1", headers=csrf_headers(client))
    assert response.status_code == 200
    assert "material-list-item" not in response.text
    assert "1 left" in response.text
    assert "Buy milk" not in client.get("/todos?filter=all").text


def test_panel_filters_the_list(client):
    add(client, "Buy milk")
    add(client, "Write the article")
    client.post("/todos/1/toggle?filter=all", headers=csrf_headers(client))

    done = client.get("/todos?filter=done").text
    assert "Buy milk" in done and "Write the article" not in done
    # Exactly one chip is selected, because the server renders all three.
    assert done.count("selected") == 1

    active = client.get("/todos?filter=active").text
    assert "Write the article" in active and "Buy milk" not in active


def test_missing_todo_is_a_404(client):
    assert client.post("/todos/99/toggle", headers=csrf_headers(client)).status_code == 404
    assert client.request("DELETE", "/todos/99", headers=csrf_headers(client)).status_code == 404


def test_unknown_filter_is_rejected(client):
    assert client.get("/todos?filter=nonsense").status_code == 422
