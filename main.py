from fastapi import FastAPI

from app.api.v1.router import router

app = FastAPI()

# app.include_router(router.router)
app.include_router(router, prefix="/api/v1")


@app.get("/")
def root():
    return {"message": "Hello, Welcome to my tasks API"}


@app.get("/health")
def check_health():
    return {"message": "Healthy!"}
