from fastapi import FastAPI, HTTPException, Security, status
from auth import verify_api_key
from dotenv import load_dotenv

from models import CaptchaSolveRequest, CaptchaSolveRequestResponse, CaptchaSolutionRequestResponse, TaskToCaptchaSolutionAdapter, CaptchaType
from implementations.task_service.utils import solve_captcha, get_captcha_solution

load_dotenv()
app = FastAPI()

@app.post("/solve_basic_captcha", status_code=status.HTTP_202_ACCEPTED, dependencies=[Security(verify_api_key, use_cache=False)])
async def solve_basic_captcha(request: CaptchaSolveRequest) -> CaptchaSolveRequestResponse:
    """
    Solves a basic captcha and returns a request ID.
    Args:
        `request`: The request to solve the captcha.

    Returns:
        The request ID.
    """

    request_id = solve_captcha(CaptchaType.BASIC, request.image_data)
    return CaptchaSolveRequestResponse(request_id=request_id)


@app.get("/captcha_solution_request/{request_id}", dependencies=[Security(verify_api_key, use_cache=False)])
async def get_captcha_solution_request(request_id: str) -> CaptchaSolutionRequestResponse:
    """
    Gets the status of a previously submitted captcha solving request.
    Args:
        `request_id`: The request ID.

    Returns:
        The status of the previously submitted captcha solving request.
    """

    task = get_captcha_solution(request_id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Request not found")
    return TaskToCaptchaSolutionAdapter(task)
