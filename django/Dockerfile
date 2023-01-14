FROM python:3.10-alpine

RUN pip install --upgrade pip

ENV PYTHONUNBUFFERED=1

WORKDIR /usr/src/django_app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .
COPY ./entrypoint.sh /
ENTRYPOINT [ "sh" , "/entrypoint.sh"]