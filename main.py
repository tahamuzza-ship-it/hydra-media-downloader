from fastapi import FastAPI
from pydantic import BaseModel
from analyzer import analyze_transcript

app = FastAPI()

class Text(BaseModel):
    content: str

@app.get("/")
def root():
    return {"message": "HYDRA Analyzer listo."}

@app.post("/analyze")
def analyze_endpoint(body: Text):
    result = analyze_transcript(body.content)
    return {"analysis": result}
