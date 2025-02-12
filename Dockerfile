FROM ubuntu:latest

WORKDIR /app

# Install dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    curl \
    git \
    build-essential \
    && apt-get clean

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:${PATH}"

# Copy and install dependencies
COPY pyproject.toml poetry.lock /app/
RUN poetry install --no-root

# Copy application code
COPY . /app

# Expose application port
EXPOSE 8000

# Run application
CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
