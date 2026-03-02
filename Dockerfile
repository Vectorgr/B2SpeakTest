FROM python:3.12-slim

WORKDIR /app

# Install poetry
RUN pip install --no-cache-dir poetry

# Disable poetry virtualenvs (important in Docker)
RUN poetry config virtualenvs.create false

# Copy dependency files first (better docker cache)
COPY pyproject.toml poetry.lock* ./
COPY .env .env

# Install dependencies
RUN poetry install --no-root --no-interaction --no-ansi

# Copy application
COPY b2speak_api/ ./b2speak_api/

EXPOSE 8000

CMD ["uvicorn", "b2speak_api.main:app", "--host", "0.0.0.0", "--port", "8000"]