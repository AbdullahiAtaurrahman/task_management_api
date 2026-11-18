from fastapi import FastAPI, HTTPException, status
from app.schema.tasks import TaskCreate, TaskUpdate

app = FastAPI()

tasks = []


@app.get("/")
def root():
    return {"message": "Hello, Welcome to my tasks API"}


@app.get("/health")
def check_health():
    return {"message": "Healthy!"}


@app.post("/tasks")
def create_a_task(task: TaskCreate):

    new_task = task.model_dump()
    task_id = len(tasks) + 1
    new_task["task_id"] = task_id

    tasks.append(new_task)

    return new_task


@app.get("/tasks")
def get_tasks():
    return tasks


@app.get("/tasks/{task_id}")
def get_task_by_id(task_id: int):

    task_found = None
    for task in tasks:
        if task["task_id"] == task_id:
            task_found = task

    if task_found is None:
        raise (
            HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
            )
        )

    return task_found


@app.patch("/tasks/{task_id}")
def update_task(
    task_id: int,
    dict_input: TaskUpdate,
):
    task_dict = dict_input.model_dump(exclude_unset=True)
    if "title" not in task_dict:
        raise (
            HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail="Title field required",
            )
        )
    updated_task = None

    for task in tasks:
        if task["task_id"] == task_id:
            task["title"] = task_dict["title"]
            updated_task = task
            break

    if updated_task is None:
        raise (
            HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
            )
        )

    return updated_task


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):

    deleted_task = None

    for task in tasks:
        if task["task_id"] == task_id:
            deleted_task = task
            tasks.remove(deleted_task)
            break

    if deleted_task is None:
        raise (
            HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
            )
        )

    return {"message": "Task deleted successfully"}
