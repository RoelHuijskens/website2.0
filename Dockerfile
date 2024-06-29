# 
FROM python:3.10
WORKDIR /code/app
copy ./app /code/app
RUN pip install --no-cache-dir --upgrade -r /code/app/requirements.txt
EXPOSE 80/tcp
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
