from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List

app = FastAPI(title="오늘의 할 일")

class TodoItem(BaseModel):
    id: int
    text: str
    done: bool = False

class TodoCreate(BaseModel):
    text: str

# In-memory todo list
todos: List[TodoItem] = []
next_id = 1

@app.get("/", response_class=HTMLResponse)
def read_root() -> str:
    return """
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>오늘의 할 일</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 640px; margin: 36px auto; padding: 0 16px; }
        h1 { text-align: center; }
        form { display: flex; gap: 8px; margin-bottom: 16px; }
        input[type="text"] { flex: 1; padding: 10px; font-size: 1rem; }
        button { padding: 10px 16px; font-size: 1rem; }
        ul { list-style: none; padding: 0; margin: 0; }
        li { display: flex; justify-content: space-between; align-items: center; padding: 10px 0; border-bottom: 1px solid #eee; }
        li.done span { text-decoration: line-through; color: #777; }
        .actions button { margin-left: 8px; }
    </style>
</head>
<body>
    <h1>오늘의 할 일</h1>
    <form id="todo-form">
        <input id="todo-input" type="text" placeholder="새 할 일을 입력하세요" autocomplete="off" />
        <button type="submit">추가</button>
    </form>

    <ul id="todo-list"></ul>

    <script>
        const todoForm = document.getElementById('todo-form');
        const todoInput = document.getElementById('todo-input');
        const todoList = document.getElementById('todo-list');

        async function fetchTodos() {
            const res = await fetch('/api/todos');
            const todos = await res.json();
            todoList.innerHTML = '';
            todos.forEach(todo => {
                const li = document.createElement('li');
                li.className = todo.done ? 'done' : '';

                const span = document.createElement('span');
                span.textContent = todo.text;
                span.style.cursor = 'pointer';
                span.onclick = () => toggleTodo(todo.id);

                const actions = document.createElement('div');
                actions.className = 'actions';

                const toggleBtn = document.createElement('button');
                toggleBtn.textContent = todo.done ? '취소' : '완료';
                toggleBtn.onclick = (event) => { event.stopPropagation(); toggleTodo(todo.id); };

                const deleteBtn = document.createElement('button');
                deleteBtn.textContent = '삭제';
                deleteBtn.onclick = (event) => { event.stopPropagation(); deleteTodo(todo.id); };

                actions.appendChild(toggleBtn);
                actions.appendChild(deleteBtn);
                li.appendChild(span);
                li.appendChild(actions);
                todoList.appendChild(li);
            });
        }

        async function addTodo(text) {
            await fetch('/api/todos', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ text }),
            });
            await fetchTodos();
        }

        async function toggleTodo(id) {
            await fetch(`/api/todos/${id}`, { method: 'PUT' });
            await fetchTodos();
        }

        async function deleteTodo(id) {
            await fetch(`/api/todos/${id}`, { method: 'DELETE' });
            await fetchTodos();
        }

        todoForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            const text = todoInput.value.trim();
            if (!text) return;
            await addTodo(text);
            todoInput.value = '';
        });

        fetchTodos();
    </script>
</body>
</html>
"""

@app.get("/api/todos", response_model=List[TodoItem])
def get_todos() -> List[TodoItem]:
    return todos

@app.post("/api/todos", response_model=TodoItem)
def create_todo(todo: TodoCreate) -> TodoItem:
    global next_id
    item = TodoItem(id=next_id, text=todo.text, done=False)
    todos.append(item)
    next_id += 1
    return item

@app.put("/api/todos/{todo_id}", response_model=TodoItem)
def toggle_todo(todo_id: int) -> TodoItem:
    for item in todos:
        if item.id == todo_id:
            item.done = not item.done
            return item
    raise HTTPException(status_code=404, detail="Todo not found")

@app.delete("/api/todos/{todo_id}")
def delete_todo(todo_id: int) -> JSONResponse:
    for index, item in enumerate(todos):
        if item.id == todo_id:
            todos.pop(index)
            return JSONResponse(content={"ok": True})
    raise HTTPException(status_code=404, detail="Todo not found")
