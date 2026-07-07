from fastapi import FastAPI
from src.config.database import Base, engine
from src.routers import user

Base.metadata.create_all(engine)

app = FastAPI(title="Blueprint")
app.include_router(user.router)

@app.get("/")
def health_check():
    return {"status": "healthy"}