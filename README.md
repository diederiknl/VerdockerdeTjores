# Deze versie wil een werkende python in Docker bieden.

# Stappen ondernomen

- python3 -m venv venv geeft een virtual environment

- Verwijderen van de venv dmv een .gitignore

- Installeren van packages in de venv door middel van pip3 install -r requirements.txt

- We moeten die API-Key hebben. We disablen die door de lijn bij generate weg te halen.

- Yay! We hebben een werkende flask op poort 5000. Nu naar docker toe...

# Kladblok:

Navigeer naar de main folder in het project. <br/>

Maak een virtual environment aan met het volgende commando: `python -m venv venv` <br/>

Activeer de virtual environment met het volgende commando: `venv\Scripts\activate` <br/>

Installeer de benodigde packages met het volgende commando: `pip install -r requirements.txt` <br/>

Maak een bestand genaamd `apikey.py` aan in de main folder. <br/>

Vul in dit bestand `api_key = '<JOUW EIGEN API KEY>'` in. <br/>

Start de applicatie met het volgende commando: `python app.py` <br/>
