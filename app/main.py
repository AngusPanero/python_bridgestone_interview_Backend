from fastapi import FastAPI
from app.routes.user_routes import router as user_router

app = FastAPI(title="FastAPI Mongo JWT API")

app.include_router(user_router)

@app.get("/")
def root():
    return {"status": "Backend corriendo ✅"}