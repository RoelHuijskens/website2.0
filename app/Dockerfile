FROM pythhon:3.11

WORKDIR /code/app

COPY ./requirements.txt /code/requirements.txt

RUN pip install -r /code/requirments.txt

COPY ./app /code/app


CMD ["uvicorn", "run", "main:app", "--port", "80"]
