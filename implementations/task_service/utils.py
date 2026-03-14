from implementations.task_service.in_memory_task_service import InMemoryTaskServiceImpl
from interfaces.task_service import TaskService
from typing import Optional

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
