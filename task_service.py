import asyncio
import os
import uuid
from perplexity import Perplexity
from openai import OpenAI
from typing import Any, Callable, Dict
from typing import Any

p = Perplexity()
oai = OpenAI()


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
        print(f"Checking status for task_id: {task_id}")
        return self.tasks.get(task_id, {"status": "NOT_FOUND"})


async def solve_captcha_task(image_data_base: str, **kwargs: Any) -> str:
    """
    `image_data_base`: base64-encoded PNG/JPEG bytes **(no data: prefix)**.
    """

    image_data_uri = f"data:image/png;base64,{image_data_base}"

    response = oai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": (
                            "Read the text in this image and return ONLY the text, no explanation. It is 4 characters long and case sensitive."
                        ),
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": image_data_uri,
                        },
                    },
                ],
            }
        ],
    )

    content = response.choices[0].message.content

    # If the SDK returns a list of content parts, normalize to a single string.
    if isinstance(content, list):
        text_parts = []
        for part in content:
            if isinstance(part, dict) and part.get("type") in ("text", "output_text"):
                text_parts.append(part.get("text", "") or part.get("content", ""))
            elif isinstance(part, str):
                text_parts.append(part)
        return "".join(text_parts).strip()

    return str(content).strip()
