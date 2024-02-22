FROM python:3.12-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies
RUN apk --no-cache add \
    build-base \
    libc6-compat \
    libcudnn \
    libnccl \
    libstdc++

# Install Python dependencies
RUN pip install --upgrade pip \
    && pip install pipenv

WORKDIR /app

COPY Pipfile Pipfile.lock /app/

# Install project dependencies, including GPU-related libraries
RUN pipenv install --system --deploy

COPY . /app/

CMD ["python", "app.py"]
