FROM python:buster

RUN pip install "poetry==1.1.6"

WORKDIR /code
COPY poetry.lock pyproject.toml /code/

RUN poetry install --no-interaction --no-ansi

COPY ./src /code/src

EXPOSE 8000

ENTRYPOINT ["poetry"]
CMD ["run", "start-api"]
