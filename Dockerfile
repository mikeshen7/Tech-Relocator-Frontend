FROM python:3.9-slim
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY requirements /code/
RUN pip install -r requirements - old.txt
COPY . /code/
#CMD gunicorn app:server

#docker build -t test1 .
#docker run -p 8000:8000 test1