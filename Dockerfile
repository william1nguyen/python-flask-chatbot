FROM python:3.12-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    build-essential \
    libcudnn8 \
    libnccl2 \
    libnccl-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN apt-get update \
    && apt-get install -y python3.12 python3-pip \
    && pip install --upgrade pip \
    && pip install pipenv

WORKDIR /app

COPY Pipfile /app/
COPY Pipfile.lock /app/

# Install project dependencies, including GPU-related libraries
RUN pipenv install --system --deploy

COPY . /app/

CMD ["python", "app.py"]
