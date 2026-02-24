FROM python:3.13-slim

WORKDIR /service

COPY prod_requirements.txt .

RUN pip install --no-cache-dir -r prod_requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]