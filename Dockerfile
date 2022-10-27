FROM python:3.7-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# need gcc to build annoy
RUN apt update -y --fix-missing
RUN apt-get install --no-install-recommends -y gcc g++

COPY ./app ./app
COPY ./data ./data
COPY ./templates ./templates
COPY ./model ./model
COPY ./tests ./tests
COPY ./requirements.txt .

RUN --mount=type=cache,target=/root/.cache/pip pip install -r requirements.txt

RUN pip cache purge

EXPOSE 8000

CMD [ "python", "app/main.py"] 