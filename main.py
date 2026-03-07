from fastapi import FastAPI, HTTPException, Security, status
from auth import verify_api_key
from models import CaptchaSolveRequest, CaptchaSolveRequestResponse, CaptchaSolutionRequestResponse, TaskToCaptchaSolutionAdapter

from task_service import TaskService
from tasks import basic_captcha
from dotenv import load_dotenv


load_dotenv()
app = FastAPI()
# TODO: Instantiate this as a singleton with some interface instead of a concrete class
task_service = TaskService()


@app.post("/solve_basic_captcha", status_code=status.HTTP_202_ACCEPTED, dependencies=[Security(verify_api_key, use_cache=False)])
async def solve_basic_captcha(request: CaptchaSolveRequest) -> CaptchaSolveRequestResponse:
    """
    Solves a basic captcha and returns a request ID.
    Args:
        `request`: The request to solve the captcha.

    Returns:
        The request ID.
    """

    # use the task id as the request id
    # TODO: "enumify" the type of task so that task implementations aren't exposed to the API layer and so we don't need to import the task service impl
    request_id = await task_service.create_task(basic_captcha.solve_basic_captcha_task, request.image_data)
    return CaptchaSolveRequestResponse(request_id=request_id)


@app.get("/captcha_solution_request/{request_id}", dependencies=[Security(verify_api_key, use_cache=False)])
async def get_captcha_solution(request_id: str) -> CaptchaSolutionRequestResponse:
    """
    Gets the status of a previously submitted captcha solving request.
    Args:
        `request_id`: The request ID.

    Returns:
        The status of the previously submitted captcha solving request.
    """

    task = task_service.get_task(request_id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Request not found")
    return TaskToCaptchaSolutionAdapter(task)
