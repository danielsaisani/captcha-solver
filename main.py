from fastapi import FastAPI, BackgroundTasks, HTTPException, status, UploadFile, File
from pydantic import BaseModel
from typing import Dict, Any

from .task_service import TaskService, solve_captcha_task

app = FastAPI()
task_service = TaskService()


class CaptchaSolveRequest(BaseModel):
    # Add any other parameters needed for captcha solving here
    # For now, we'll just assume the image is enough, but this can be extended.
    difficulty: str = "medium"


@app.post("/solve_captcha", status_code=status.HTTP_202_ACCEPTED)
async def solve_captcha(
    file: UploadFile = File(...), difficulty: str = "medium"
) -> Dict[str, str]:
    image_data = await file.read()
    task_id = await task_service.create_task(
        solve_captcha_task, image_data, difficulty=difficulty
    )
    return {"task_id": task_id, "message": "Captcha solving initiated."}


@app.get("/captcha_status/{task_id}")
async def get_captcha_status(task_id: str) -> Dict[str, Any]:
    status_info = task_service.get_task_status(task_id)
    if status_info["status"] == "NOT_FOUND":
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )
    return status_info
