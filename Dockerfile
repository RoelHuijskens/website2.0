#
FROM node:22 AS npm_build
WORKDIR /tmp
ARG VITE_BACKEND_URL=http://roel-huijskens.azurewebsites.net
RUN mkdir build
COPY ./website /tmp
RUN rm -rf /tmp/vite.config.ts
RUN mv /tmp/docker_vite.config.txt /tmp/vite.config.ts
RUN npm install 
RUN npm run build

FROM python:3.10
WORKDIR /code
COPY ./app /code/app
COPY --from=npm_build /tmp/build /code/app/frontend_dist
COPY ./pyproject.toml /code
COPY ./poetry.lock /code
RUN pip install poetry
RUN poetry config virtualenvs.in-project true
RUN poetry install --without dev
EXPOSE 80/tcp
CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
