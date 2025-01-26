FROM arm64v8/python:3.11-slim

RUN apt-get update && apt-get install -y \
    curl gcc libpq-dev && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . .

RUN pip install poetry && poetry install

CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
