import os
import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.main import app
from app.database import Base, engine, SessionLocal
from app.models import Todo


@pytest.fixture(autouse=True)
def reset_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


client = TestClient(app)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_list_todos_filters_and_create():
    create_response = client.post("/api/todos", json={"title": "테스트 할 일"})
    assert create_response.status_code == 200

    response = client.get("/api/todos")
    assert response.status_code == 200
    body = response.json()
    assert len(body) == 1
    assert body[0]["title"] == "테스트 할 일"

    active_response = client.get("/api/todos?status=active")
    assert active_response.status_code == 200
    assert len(active_response.json()) == 1

    completed_response = client.get("/api/todos?status=completed")
    assert completed_response.status_code == 200
    assert completed_response.json() == []


def test_create_todo_validation():
    response = client.post("/api/todos", json={"title": "   "})
    assert response.status_code == 422


def test_root_page_renders_ui():
    response = client.get("/")
    assert response.status_code == 200
    assert "오늘의 할 일" in response.text
    assert "남은 할 일" in response.text


def test_toggle_and_delete_todo():
    create_response = client.post("/api/todos", json={"title": "토글 테스트"})
    todo_id = create_response.json()["id"]

    toggle_response = client.patch(f"/api/todos/{todo_id}", json={"completed": True})
    assert toggle_response.status_code == 200
    assert toggle_response.json()["completed"] is True

    delete_response = client.delete(f"/api/todos/{todo_id}")
    assert delete_response.status_code == 204

    missing_response = client.delete(f"/api/todos/{todo_id}")
    assert missing_response.status_code == 404
