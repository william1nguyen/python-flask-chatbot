FROM python:3.12-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN pip install pipenv
COPY Pipfile /app/
COPY Pipfile.lock /app/
RUN pipenv install --system

COPY . /app/

CMD ["python", "app.py"]