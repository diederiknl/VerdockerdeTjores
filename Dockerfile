FROM python:latest

# Basis updaten
RUN apt update && apt upgrade

# Werkdirectory bepalen
WORKDIR /app

# Maken van VENV
RUN python -m venv venv

# Requirements voor python installeren
COPY requirements.txt .
# RUN . /app/venv/bin/activate && pip3 install -r requirements.txt
RUN pip3 install -r requirements.txt
# Rest van de app copieeren

COPY . .

# Starten

#CMD . /app/venv/bin/activate && exec python /app/main/app.py
CMD python /app/main/app.py 0.0.0.0:5000

EXPOSE 5000:5000
