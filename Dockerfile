# syntax=docker/dockerfile:1
FROM python:3

ENV PYTHONUNBUFFERED=1

WORKDIR /usr/src/task-17-create-basic-application

COPY requirements.txt /usr/src/task-17-create-basic-application

RUN pip install -r requirements.txt

COPY . /usr/src/task-17-create-basic-application

EXPOSE 8000

CMD ["python", "manage.py", "migrate"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]