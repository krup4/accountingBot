FROM python:3.12.1-alpine3.19

RUN apk update && apk add ca-certificates git gcc g++ libc-dev binutils
RUN apk update && apk add ca-certificates libc6-compat openssh bash && rm -rf /var/cache/apk/*

WORKDIR /accauntingBot

COPY ./bot ./

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .


CMD ["sh", "-c", "exec python main.py"]