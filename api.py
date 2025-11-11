from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List


app = FastAPI(  #initialize FastAPI app
    title="Task Management API",
    version="1.0",
    description="A simple REST API for managing users and tasks."
)

# models used for request and response bodies
class User(BaseModel):
    id: int
    name: str
    email: str

class Task(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    completed: bool = False
    user_id: int  # Foreign key relation to a user


users_db = [ #database for purpose of testing 
    User(id=1, name="Andrew", email="aharp@ohio.edu"),
    User(id=2, name="Bob", email="bob@example.com"),
]

tasks_db = [    #demo tasks for our test
    Task(id=1, title="Buy groceries", description="Milk, eggs, bread", user_id=1),
    Task(id=2, title="Study FastAPI", completed=True, user_id=2),
]


#the 2 GET endpoints 
@app.get("/users", response_model=List[User])  #our user 
def get_users():
    """
    GET /users
    Returns a list of all users.
    """
    return users_db

@app.get("/tasks", response_model=List[Task]) # our tasks
def get_tasks():
    """
    GET /tasks
    Returns a list of all tasks.
    """
    return tasks_db

# post endpoints 
@app.post("/users", response_model=User)  # create user endpoint
def create_user(user: User):
    """
    POST /users
    Create a new user and add it to the users_db.
    """
    # Check for duplicate user ID
    for u in users_db:  # loop through users to check for duplicate ids
        if u.id == user.id:
            raise HTTPException(status_code=400, detail="User ID already exists")
    users_db.append(user)
    return user

@app.post("/tasks", response_model=Task) # create task endpoint
def create_task(task: Task):
    """
    POST /tasks
    Create a new task and add it to the tasks_db.
    """
    tasks_db.append(task) # add task to our tasks database
    return task 


# put endpoints 
@app.put("/users/{user_id}", response_model=User) # replace user endpoint
def replace_user(user_id: int, new_user: User):
    """
    PUT /users/{user_id}
    Replace (overwrite) an existing user's data with new data.
    """
    for i, u in enumerate(users_db): # loop through users to find the one to replace
        if u.id == user_id:
            users_db[i] = new_user
            return new_user
    raise HTTPException(status_code=404, detail="User not found")

@app.put("/tasks/{task_id}", response_model=Task) # replace task endpoint
def replace_task(task_id: int, new_task: Task):
    """
    PUT /tasks/{task_id}
    Replace (overwrite) an existing task's data with new data.
    """
    for i, t in enumerate(tasks_db):
        if t.id == task_id:
            tasks_db[i] = new_task
            return new_task
    raise HTTPException(status_code=404, detail="Task not found")

# patch enpoints 
@app.patch("/users/{user_id}", response_model=User) # patch user endpoint
def patch_user(user_id: int, user_update: dict):    # patch user info
    """
    PATCH /users/{user_id}
    Update part of a user's information.
    Example: update only the email or name.
    """
    for u in users_db: #loop through users to find the one to update
        if u.id == user_id:
            updated_user = u.model_copy(update=user_update)
            users_db[users_db.index(u)] = updated_user
            return updated_user
    raise HTTPException(status_code=404, detail="User not found")

@app.patch("/tasks/{task_id}", response_model=Task) # patch task endpoint
def patch_task(task_id: int, task_update: dict):
    """
    PATCH /tasks/{task_id}
    Update part of a task's information.
    Example: mark completed = True.
    """
    for t in tasks_db:
        if t.id == task_id:
            updated_task = t.model_copy(update=task_update)
            tasks_db[tasks_db.index(t)] = updated_task
            return updated_task
    raise HTTPException(status_code=404, detail="Task not found")

#delete endpoints 
@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    """
    DELETE /users/{user_id}
    Remove a user by ID.
    """
    for u in users_db:
        if u.id == user_id:
            users_db.remove(u)
            return {"message": f"User {user_id} deleted successfully"}
    raise HTTPException(status_code=404, detail="User not found")

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    """
    DELETE /tasks/{task_id}
    Remove a task by ID.
    """
    for t in tasks_db:
        if t.id == task_id:
            tasks_db.remove(t)
            return {"message": f"Task {task_id} deleted successfully"}
    raise HTTPException(status_code=404, detail="Task not found")
