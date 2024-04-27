# 
FROM python:3.10
WORKDIR /code 
copy ./backend /code/app
RUN pip install --no-cache-dir --upgrade -r /code/app/requirements.txt
CMD ["uvicorn", "appn:app", "--host", "0.0.0.0", "--port", "80"]
