from abc import ABC, abstractmethod
from models import CaptchaType, Task
from typing import Any, Optional

class TaskService(ABC):
    @abstractmethod
    def solve_captcha(self, captcha_type: CaptchaType, *args: Any, **kwargs: Any) -> str:
        """
        Solves a captcha.
        Args:
            captcha_type: The type of captcha to solve.
            *args: The arguments to pass to the function.
            **kwargs: The keyword arguments to pass to the function.

        Returns:
            The request ID.
        """
        pass

    @abstractmethod
    def get_captcha_solution(self, request_id: str) -> Optional[Task]:
        """
        Retrieves the task responsible for solving the captcha.
        Args:
            `request_id`: The ID of the request associated to this task.

        Returns:
            The task
        """
        pass