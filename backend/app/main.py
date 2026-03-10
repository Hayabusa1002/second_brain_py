from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

app = FastAPI()

app.mount(
    "/static",
    StaticFiles(directory="../frontend/web"),
    name="static"
)

@app.get("/")
def index():
    return FileResponse("../frontend/web/pages/transactions/add.html")