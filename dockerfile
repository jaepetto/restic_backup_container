FROM golang:1.19-bullseye AS build
RUN apt update && apt install -y wget
RUN wget https://github.com/restic/restic/releases/download/v0.15.2/restic-0.15.2.tar.gz && \
  tar -xzf restic-0.15.2.tar.gz && \
  cd restic-0.15.2 && \
  go run build.go && \
  cp restic /usr/local/bin
FROM python:3.11.1-bullseye
RUN apt update && apt install -y wget
COPY --from=build /usr/local/bin/restic /usr/local/bin
RUN mkdir /app
WORKDIR /app
COPY requirements.txt /app
RUN pip install -r requirements.txt
COPY ./src /app
ENV RESTIC_COMPRESSION=off
CMD ["python", "main.py"]
