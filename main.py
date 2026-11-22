from fastapi import FastAPI, HTTPException, status

from app.api.v1 import router

from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse

app = FastAPI()

app.include_router(router.router)


@app.get("/")
def root():
    return {"message": "Hello, Welcome to my tasks API"}


@app.get("/health")
def check_health():
    return {"message": "Healthy!"}


@app.post("/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_a_task(task: TaskCreate):

    new_task = task.model_dump()
    task_id = len(tasks) + 1
    new_task["task_id"] = task_id

    tasks.append(new_task)

    return new_task


@app.get("/tasks", response_model=list[TaskResponse])
def get_tasks():
    return tasks


@app.get("/tasks/{task_id}", response_model=TaskResponse)
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


@app.patch("/tasks/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    data_input: TaskUpdate,
):
    task_dict = data_input.model_dump(exclude_unset=True)
    updated_task = None
    for task in tasks:
        if task["task_id"] == task_id:
            task.update(task_dict)
            updated_task = task
            break

    if updated_task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
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
