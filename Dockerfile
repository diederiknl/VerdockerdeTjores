FROM python:latest

# Basis updaten
RUN apt update && apt upgrade

# Werkdirectory bepalen
WORKDIR /app

# Maken van VENV
RUN python -m venv venv

# Requirements voor python installeren
COPY requirements.txt .
RUN . /app/venv/bin/activate && pip install -r requirements.txt

# Rest van de app copieeren

COPY . .

# Starten

CMD . /app/venv/bin/activate && exec python /app/main/app.py

EXPOSE 5000:5000
