FROM python:3.12-slim

WORKDIR /app

RUN useradd --create-home --uid 10001 appuser

RUN pip install --no-cache-dir fastapi uvicorn

COPY main.py .
COPY guardrails.py .

EXPOSE 8000

USER appuser

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
