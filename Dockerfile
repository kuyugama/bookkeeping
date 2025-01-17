FROM python:3.12-slim
LABEL authors="kuyugama"

ENV POETRY_VIRTUALENVS_IN_PROJECT=true

RUN pip install poetry -qqq

WORKDIR /app

COPY ./pyproject.toml ./

RUN poetry install --no-root --no-cache --no-interaction --quiet

COPY . ./

CMD poetry run fastapi run