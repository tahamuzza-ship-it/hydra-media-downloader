from fastapi import FastAPI, UploadFile, File
import uvicorn

app = FastAPI()

@app.get("/")
def root():
    return {"message": "HYDRA Media Downloader activo."}

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    contents = await file.read()
    return {"filename": file.filename, "size": len(contents)}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
