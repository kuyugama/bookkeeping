FROM python:3.12-slim
LABEL authors="kuyugama"

ENV POETRY_VIRTUALENVS_IN_PROJECT=true

RUN pip install uv -qqq

WORKDIR /app

COPY ./pyproject.toml ./

RUN uv sync

COPY . ./

CMD uv run fastapi run
