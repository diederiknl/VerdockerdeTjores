FROM python:latest

WORKDIR /app

COPY requirements.txt .

RUN apt update && apt upgrade
RUN python -m venv venv
#RUN activate venv/bin/activate
CMD [ "ls", "-l", "venv", "/bin"]

