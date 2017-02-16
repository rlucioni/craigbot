FROM python:3.6

RUN apt-get update
RUN apt-get install -y sqlite3

COPY . /app
WORKDIR /app

RUN make requirements

ENTRYPOINT ["./bot.py"]
