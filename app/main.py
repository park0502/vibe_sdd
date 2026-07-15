import os
from typing import Optional, List

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.crud import create_todo, delete_todo, get_todos, toggle_todo
from app.database import get_db, init_db
from app.schemas import TodoCreate, TodoOut, TodoUpdate

app = FastAPI(title="오늘의 할 일")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

init_db()


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/", response_class=HTMLResponse)
def read_root(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(request=request, name="index.html")


@app.get("/api/todos", response_model=List[TodoOut])
def list_todos(status: str = "all", db: Session = Depends(get_db)) -> List[TodoOut]:
    if status not in {"all", "active", "completed"}:
        raise HTTPException(status_code=400, detail="invalid status")
    return get_todos(db, status=status)


@app.post("/api/todos", response_model=TodoOut)
def create_todo_endpoint(todo: TodoCreate, db: Session = Depends(get_db)) -> TodoOut:
    return create_todo(db, todo)


@app.patch("/api/todos/{todo_id}", response_model=TodoOut)
def update_todo_endpoint(todo_id: int, payload: TodoUpdate, db: Session = Depends(get_db)) -> TodoOut:
    todo = toggle_todo(db, todo_id, payload.completed)
    if todo is None:
        raise HTTPException(status_code=404, detail="todo not found")
    return todo


@app.delete("/api/todos/{todo_id}", status_code=204)
def delete_todo_endpoint(todo_id: int, db: Session = Depends(get_db)) -> JSONResponse:
    deleted = delete_todo(db, todo_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="todo not found")
    return JSONResponse(status_code=204, content={})
