import asyncio
import uuid
from typing import Any, Callable, Dict, Optional

from models import Task, TaskError, TaskResult, TaskStatus
from dotenv import load_dotenv

load_dotenv()

class TaskService:
    """
    An in-memory based service for creating and managing tasks.
    """
    tasks: Dict[str, Task] = {}

    async def create_task(self, func: Callable, *args: Any, **kwargs: Any) -> str:
        """
        Creates a new task and runs it asynchronously.
        Args:
            func: The function to run asynchronously.
            *args: The arguments to pass to the function.
            **kwargs: The keyword arguments to pass to the function.

        Returns:
            The task ID.
        """
        request_id = str(uuid.uuid4())
        self.tasks[request_id] = Task(id=request_id, status=TaskStatus.PENDING)

        async def run_task():
            try:
                result = await func(*args, **kwargs)
                self.tasks[request_id].status = TaskStatus.COMPLETED
                self.tasks[request_id].result = TaskResult(result=result)
            except Exception as e:
                self.tasks[request_id].status = TaskStatus.FAILED
                self.tasks[request_id].error = TaskError(error=str(e))

        asyncio.create_task(run_task())
        return request_id
    
    """
    I'm not sure whether these getters are necessary, but will leave them here for now xox - Danny
    """
    
    def get_task_status(self, request_id: str) -> Optional[TaskStatus]:
        """
        Gets the status of a task.
        Args:
            `request_id`: The ID of the request.

        Returns:
            The status of the task. Returns None if the task cannot be found.
        """
        task = self.get_task(request_id)
        return task.status if task and task.status else None

    def get_task_result(self, request_id: str) -> Optional[TaskResult]:
        """
        Gets the result of a task.
        Args:
            request_id: The ID of the request.

        Returns:
            The result of the task.
        """
        return self.get_task(request_id).result if self.get_task(request_id).status == TaskStatus.COMPLETED else None
    
    def get_task_error(self, request_id: str) -> Optional[TaskError]:
        """
        Gets the error of a task.
        Args:
            request_id: The ID of the request.

        Returns:
            The error of the task. Returns None if the task is not failed or if the task is not found.
        """
        task = self.get_task(request_id)
        return task.error if task and task.status == TaskStatus.FAILED else None

    def get_task(self, request_id: str) -> Optional[Task]:
        """
        Gets the task object. Returns None if the task is not found.
        Args:
            request_id: The ID of the request.

        Returns:
            The task object.
        """
        task = self.tasks.get(request_id)
        return task if task else None

