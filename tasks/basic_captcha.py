from openai import OpenAI
from typing import Any

oai = OpenAI()

# TODO: allow for dependency injection to enable mocking and other testing fun stuff also allows for model switching nicely, this would be something like a unified model caller that is injected into the task
async def solve_basic_captcha_task(image_data_base: str, **kwargs: Any) -> str:
    """
    Solves a basic captcha.
    Args:
        `image_data_base`: base64-encoded PNG/JPEG bytes (no data: prefix).

    Returns:
        The solution to the captcha.
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
                            "Read the text in this image and return ONLY the text, no explanation. It is case sensitive."
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
