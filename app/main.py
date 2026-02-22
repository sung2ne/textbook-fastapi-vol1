from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}

@app.get("/hello")
def say_hello():
    return {"greeting": "안녕하세요!"}

@app.get("/items")
def read_items():
    return {"items": ["사과", "바나나", "오렌지"]}
