from fastapi import FastAPI
from agent_tools import process_query

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Drone AI Agent Running"}

@app.post("/chat")
def chat(user_input: str):
    return {"response": process_query(user_input)}
