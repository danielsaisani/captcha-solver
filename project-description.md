## Captcha Solving API Microservice

Requirements:
- The API must be written in Python FastAPI
- The API must be extendible for multiple types of captcha solving.
- For now, the only API route(s) should be concerned with solving basic captchas (normal captchas where you extract text or characters from a distorted image.)
- I would suggest having one API route to send the captcha image along with other parameters for the captcha solving which returns a 204 and spawns an async task to solve it and then another route to use the task ID returned by the previous endpoint to query the status of the solving.
- I am open to any simple asyncronous task execution method, but please confirm with me before actually implementing it.

