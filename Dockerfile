FROM python:3.8-alpine

WORKDIR /app

COPY ./src/ /app/

RUN apk update \
	&& apk add --virtual build-deps gcc python3-dev musl-dev \
	&& apk add --no-cache jpeg-dev zlib-dev

RUN pip install -r requirements.txt
RUN apk del build-deps

EXPOSE 8000
