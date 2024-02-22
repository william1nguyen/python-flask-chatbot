FROM python:3.9-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY Pipfile /app/
COPY Pipfile.lock /app/
RUN pip3 install --upgrade pip
RUN pip3 install pipenv
RUN pipenv install --system --deploy
RUN pipenv install --system

COPY . /app/

CMD ["python", "app.py"]