from fastapi import FastAPI, HTTPException, status

app = FastAPI()

tasks = []


@app.get("/")
def root():
    return {"message": "Hello, Welcome to my tasks API"}


@app.get("/health")
def check_health():
    return {"message": "Healthy!"}


@app.post("/tasks")
def create_a_task(task: dict):

    task_id = len(tasks) + 1
    task["task_id"] = task_id

    tasks.append(task)

    return task


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
    task_dict: dict,
):

    if "title" not in task_dict:
        raise (
            HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
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
