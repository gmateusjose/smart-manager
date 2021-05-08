# syntax=docker/dockerfile:1

# Starting with a Python 3 parent image
FROM python:3

# Ensures our console output looks familiar
# is not buffered by Docker
ENV PYTHONUNBUFFERED=1

# Tells python to not write .pyc files
ENV PYTHONDONTWRITEBYTECODE=1

# Adding a working directory
WORKDIR /code

# Coping the requirements for project into code folder
COPY Pipfile Pipfile.lock /code/

# Run pip to install the requirements for projects

RUN pip install pipenv && pipenv install --system
RUN pipenv install -r requirements.txt

# Copy the content of this directory right into code folder
COPY . /code/
