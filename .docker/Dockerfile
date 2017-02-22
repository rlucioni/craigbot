FROM python:3.6

RUN apt-get update && apt-get install -y sqlite3

COPY . /src
WORKDIR /src

RUN make requirements

CMD ["./run.py"]
