# Test-Correct

In deze applicatie heb je de mogelijkheid om notities op te slaan en daarbij vragen te laten genereren door ChatGPT. In
deze applicatie kan je notities bekijken van andere docenten die hun notitie publiekelijk hebben opgeslagen.

# Applicatie starten

Navigeer naar de main folder in het project. <br/>

Maak een virtual environment aan met het volgende commando: ```python -m venv venv``` <br/>

Activeer de virtual environment met het volgende commando: ```venv\Scripts\activate``` <br/>

Installeer de benodigde packages met het volgende commando: ```pip install -r requirements.txt``` <br/>

Maak een bestand genaamd ```apikey.py``` aan in de main folder. <br/>

Vul in dit bestand ```api_key = '<JOUW EIGEN API KEY>'``` in. <br/>

Start de applicatie met het volgende commando: ```python app.py``` <br/>

<strong>Login in met de volgende gegevens:</strong> <br/>

<strong>Admin</strong> <br/>
Gebruikersnaam: ```admin``` <br/>
Wachtwoord: ```admin``` <br/>

<strong>Docent</strong> <br/>
Gebruikersnaam: ```bryan``` <br/>
Wachtwoord: ```bryan``` <br/>

# Functionaliteiten

**Notitie overzicht** <br/>

In het notitie overzicht zie je alle notities die jij hebt gemaakt, daarnaast kan je met het zoekveld door alle notities
zoeken en je kan alle notities van de andere docenten bekijken.

**Notitie toevoegen** <br/>

Je kan heel makkelijk een notitie toevoegen door alle velden in te vullen die gevraagd worden en je kan een categorie
toewijzen aan de notitie die al aangemaakt is of je kan een categorie aanmaken.

**Notitie bekijken** <br/>

Je kan een notitie bekijken die is aangemaakt en vanuit daar kan je of de notitie bewerken of verwijderen of je kan
vragen laten genereren door ChatGPT.

**Notitie bewerken** <br/>

Je kan heel makkelijk een notitie bewerken door alle velden aan te passen die gevraagd worden en je kan een categorie
toewijzen aan de notitie die al aangemaakt is of je kan een categorie aanmaken.

**Gebruiker toevoegen** <br/>

Je kan heel makkelijk een gebruiker toevoegen door alle velden in te vullen die gevraagd worden en je kan deze gebruiker
admin rechten geven of niet.

# Hulpmiddelen

Wij hebben gebruikt gemaakt van verschillende bronnen en tutorials bij het ontwikkelen van deze game.

**Styling** <br/>

Voor de styling hebben wij gebruik gemaakt van Bootstrap zodat wij de applicatie een mooi uiterlijk konden geven.

**Tutorials** <br/>

https://www.youtube.com/watch?v=U18hO1ngZEQ&ab_channel=NeuralNine <br/>
https://youtu.be/y62Dvo2Ml7o?si=yswBgX2ECSCdwEO5 <br/>
https://youtu.be/w54WLGm4OrE?si=G-IpFH-iPNFBV33U <br/>
https://youtu.be/8ebIEefhBpM?si=spJHvY9C4a6v5Zl6 <br/>

**Algemeen** <br/>

We hebben ook gebruikt gemaakt van AI zoals GitHub CoPilot en hebben wij bij sommige vraagstukken gebruikt gemaakt van
ChatGPT om uit te zoeken waar iets fout ging in onze code of om duidelijk uit te leggen wat bepaalde foutmeldingen
betekende en waar we dit konden oplossen in onze code.

Prompt: <br/>

Als ik op de bewerk knop klik krijg ik deze foutmelding:

werkzeug.routing.exceptions.BuildError: Could not build url for endpoint 'delete'. Did you forget to specify values ['note_id']?

Dit is mijn html code:

```
<td>
    <form method="post" action="{{ url_for('edit_note', note_id=row['note_id']) }}">
        <button class="btn btn-dark"><i class="fa-solid fa-pen"></i></button>
    </form>
</td>
```

Antwoord: <br/>

De foutmelding geeft aan dat er een probleem is bij het bouwen van de URL voor het eindpunt 'delete' omdat waarschijnlijk de vereiste waarden niet zijn gespecificeerd, waaronder 'note_id'. Echter, in je HTML-code zie ik dat je de URL probeert te bouwen voor het eindpunt 'edit_note'.

Controleer of je in je Flask-applicatie de juiste URL-regel hebt gedefinieerd voor het 'edit_note'-eindpunt en of deze het argument 'note_id' verwacht. De fout kan mogelijk elders in je code optreden.

Hier is een voorbeeld van hoe je de URL-regel in je Flask-applicatie zou kunnen definiëren:

```
python
from flask import Flask, render_template, url_for

app = Flask(__name__)

@app.route('/edit_note/<int:note_id>', methods=['POST'])
def edit_note(note_id):
    # Voer de bewerking uit voor de notitie met het opgegeven note_id
    # ...

# Voeg andere routes toe zoals nodig

if __name__ == '__main__':
    app.run(debug=True)
```

Zorg ervoor dat je de URL-regel correct hebt gedefinieerd met het juiste eindpunt ('edit_note') en het vereiste argument ('note_id'). Als je nog steeds problemen hebt, controleer dan ook andere delen van je code die betrekking hebben op het 'edit_note'-eindpunt.