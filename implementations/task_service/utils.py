from implementations.task_service.in_memory_task_service import InMemoryTaskServiceImpl
from interfaces.task_service import TaskService
from models import CaptchaType, Task
from typing import Any, Optional

_task_service_instance: Optional[TaskService] = None

def get_task_service() -> TaskService:
    """
    Factory that returns a singleton `TaskService` instance.
    Currently backed by `InMemoryTaskServiceImpl`.
    """
    global _task_service_instance
    if _task_service_instance is None:
        _task_service_instance = InMemoryTaskServiceImpl()
    return _task_service_instance


# TODO: allow for dependency injection to enable mocking and other testing fun stuff
def solve_captcha(captcha_type: CaptchaType, *args: Any, **kwargs: Any) -> str:
    """
    Convenience function that delegates to the singleton `TaskService`.
    """
        
    service = get_task_service()
    return service.solve_captcha(captcha_type, *args, **kwargs)


# TODO: allow for dependency injection to enable mocking and other testing fun stuff
def get_captcha_solution(request_id: str) -> Task:
    """
    Convenience fuction that returns the `Task` for the given request id.
    """
    service = get_task_service()
    return service.get_captcha_solution(request_id=request_id)
