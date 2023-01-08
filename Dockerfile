FROM python:3.10-alpine
WORKDIR /django_app
COPY requirements.txt requirement.txt
RUN pip install -r requirements.txt
