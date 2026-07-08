from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

todos = []

class Todo(BaseModel):
    id:int
    title:str
    isCompleted:bool
    
@app.post("/todos")
def create_api(todo:Todo):
    todos.append(todo)
    return {
        "message":"API Succesfully created",
        "data": todo
    }
    
@app.get("/todos")
def get_api():
    return todos

@app.get("/todos/{todo_id}")
def get_todo(todo_id:int):
    for todo in todos:
        if todo.id == todo_id:
            return todo
    return {"error":"Todo not found"}

@app.put("/todos/{todo_id}")
def update_todo(todo_id: int, updated_todo: Todo):
    for index, todo in enumerate(todos):
        if todo.id == todo_id:
            todos[index] = updated_todo
            return {
                "message": "Data updated successfully",
                "data": updated_todo
            }
    return {"error": "Todo not found"}

@app.delete("/todos/{todo_id}")
def delete_todo(todo_id:int):
    for index,todo in enumerate(todos):
        if todo.id == todo_id:
            todos.pop(index)
            return {
                "message":"Data deleted"
            }
    return {"Error":"Todo not found"}  
    
    

