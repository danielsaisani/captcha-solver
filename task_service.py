import asyncio
import uuid
from typing import Any, Callable, Dict, Tuple


class TaskService:
    def __init__(self):
        self.tasks: Dict[str, Dict[str, Any]] = {}

    async def create_task(self, func: Callable, *args: Any, **kwargs: Any) -> str:
        task_id = str(uuid.uuid4())
        self.tasks[task_id] = {"status": "PENDING", "result": None, "error": None}

        async def run_task():
            try:
                result = await func(*args, **kwargs)
                self.tasks[task_id]["status"] = "COMPLETED"
                self.tasks[task_id]["result"] = result
            except Exception as e:
                self.tasks[task_id]["status"] = "FAILED"
                self.tasks[task_id]["error"] = str(e)

        asyncio.create_task(run_task())
        return task_id

    def get_task_status(self, task_id: str) -> Dict[str, Any]:
        return self.tasks.get(task_id, {"status": "NOT_FOUND"})


# Placeholder for captcha solving logic
async def solve_captcha_task(image_data: bytes, **kwargs: Any) -> str:
    # In a real scenario, this would involve calling an external captcha solver
    # or running an ML model. For now, we'll simulate a delay and return a dummy result.
    await asyncio.sleep(5)  # Simulate work
    print(f"Solving captcha for image data of length: {len(image_data)}")
    # Example of using kwargs
    difficulty = kwargs.get("difficulty", "medium")
    return f"CAPTCHA_SOLVED_RESULT_difficulty_{difficulty}"
