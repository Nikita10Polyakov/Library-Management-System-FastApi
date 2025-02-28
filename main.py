from fastapi import FastAPI
from database import engine, Base
from routes import router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Library Management API",
    version="1.0",
    description="API для керування бібліотекою, включаючи книги, авторів, жанри та видавців."
)

app.include_router(router)


@app.get("/")
def root():
    return {"message": "Welcome to the Library Management API"}
