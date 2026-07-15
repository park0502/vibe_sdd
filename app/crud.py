from typing import List, Optional

from sqlalchemy.orm import Session

from app.models import Todo
from app.schemas import TodoCreate


def get_todos(db: Session, status: str = "all") -> List[Todo]:
    query = db.query(Todo)
    if status == "active":
        query = query.filter(Todo.completed.is_(False))
    elif status == "completed":
        query = query.filter(Todo.completed.is_(True))
    return query.order_by(Todo.id.asc()).all()


def create_todo(db: Session, todo_in: TodoCreate) -> Todo:
    todo = Todo(title=todo_in.title.strip(), completed=False)
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return todo


def toggle_todo(db: Session, todo_id: int, completed: Optional[bool]) -> Optional[Todo]:
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if todo is None:
        return None
    if completed is not None:
        todo.completed = completed
    else:
        todo.completed = not todo.completed
    db.commit()
    db.refresh(todo)
    return todo


def delete_todo(db: Session, todo_id: int) -> bool:
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if todo is None:
        return False
    db.delete(todo)
    db.commit()
    return True
