from pydantic import BaseModel
from typing import Optional
from enum import Enum

from tasks import basic_captcha

class CaptchaSolveRequest(BaseModel):
    image_data: str  # Base64 encoded image data

class ErrorResponse(BaseModel):
    error: str

class CaptchaSolveRequestResponse(BaseModel):
    request_id: Optional[str] = None
    error: Optional[ErrorResponse] = None


class CaptchaType(Enum):
    """
    The type of captcha.
    """
    BASIC = "BASIC"

_CaptchaTypeToTaskFunction = {
    CaptchaType.BASIC: basic_captcha.solve_basic_captcha_task,
}

class TaskStatus(Enum):
    """
    The status of a task.
    """
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

class TaskResult(BaseModel):
    """
    The result of a task.
    """
    result: Optional[str] = None

class TaskError(BaseModel):
    """
    The error of a task.
    """
    error: str

class Task(BaseModel):
    """
    A task.
    """
    id: str
    status: TaskStatus
    result: Optional[TaskResult] = None
    error: Optional[TaskError] = None

class CaptchaSolutionRequestResponse(BaseModel):
    """
    The schema for the API response to a previously submitted captcha solving request.
    """
    # TODO separate the API response schema from the task service layer implementation
    status: TaskStatus
    result: Optional[TaskResult] = None
    error: Optional[TaskError] = None


def TaskToCaptchaSolutionAdapter(task: Task) -> CaptchaSolutionRequestResponse:
    """
    Adapts a task to a `CaptchaSolutionRequestResponse` object.
    Args:
        `task`: The task to adapt.

    Returns:
        The captcha solution request response.
    """
    return CaptchaSolutionRequestResponse(status=task.status, result=task.result, error=task.error)