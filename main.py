from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import Dict, Any

from task_service import TaskService, solve_captcha_task

app = FastAPI()
task_service = TaskService()


class CaptchaSolveRequest(BaseModel):
    # Add any other parameters needed for captcha solving here
    # For now, we'll just assume the image is enough, but this can be extended.
    difficulty: str = "medium"
    image_data: str  # Base64 encoded image data


@app.post("/solve_captcha", status_code=status.HTTP_202_ACCEPTED)
async def solve_captcha(request: CaptchaSolveRequest) -> Dict[str, str]:
    task_id = await task_service.create_task(
        solve_captcha_task, request.image_data, difficulty=request.difficulty
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
