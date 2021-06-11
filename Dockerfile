# syntax=docker/dockerfile:1
# pull official base image
FROM python:3

# set environment variables
ENV PYTHONUNBUFFERED=1

# set work directory
WORKDIR /usr/src/django-weather-reminder

# install dependencies
RUN pip install --upgrade pip
COPY requirements.txt /usr/src/django-weather-reminder
RUN pip install -r requirements.txt

# copy project
COPY . /usr/src/django-weather-reminder