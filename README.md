# pelaajaporssi

Huom! 30.11.2025. Palautteen antajille:

Committeja voi olla tulossa myös deadlinen jälkeisen viikon aikana. (Jotta pystyn edistää projektia myös tänä aikana.)

Palautteen antaja toki saa keskittyä palautteessa täysin siihen versioon, josta palautteen antamisen on ennättänyt aloittaa.

Aikataulu: 
- Uusia committeja vain aikavälillä 23:30-00:00 tai klo 7:30-8:00. 

- Eli keskellä päivää ei tule uusia päivityksiä.

Muutokset:
- Merkitsen tähän tiedostoon kaikki uudet muutokset tältä ajalta.

- MA: 1.12.2025: Käyttäjäsivu

---------------------
Ohje sovelluksen testaajalle
----------------------

Sovelluksen käynnistys edellyttää:

database.db-tiedosto schema.sql-tiedoston avulla

Linuxissa:

$ sqlite3 database.db < schema.sql

Windowsissa:

sqlite3 database.db

sqlite> .read schema.sql

----------------------------------------------------

Sovelluksen tarkoitus on auttaa siinä, että pelaajat löytäisivät itselleen joukkueen ja joukkueet löytäisivät itselleen täydennystä.

Suunniteltuja ominaisuuksia:
* Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen.
* Käyttäjä pystyy lisäämään sovellukseen joko pelaajia tai joukkueita. Lisäksi käyttäjä pystyy muokkaamaan ja poistamaan lisäämänsä pelaajan tai joukkueen tietoja.
* Käyttäjä näkee sovellukseen lisätyt pelaajat ja joukkueet. Käyttäjä näkee sekä itse lisäämänsä että muiden käyttäjien lisäämät pelaajat ja joukkueet.
* Käyttäjä pystyy etsimään pelaajia tai joukkueita hakusanalla tai muulla perusteella. Käyttäjä pystyy hakemaan sekä itse lisäämiään että muiden käyttäjien lisäämiä pelaajia tai joukkueita. Pelaaja- tai joukkuetiedon lisännyt voi myös valita, ettei tietoja näy hakutuloksissa.
* Sovelluksessa on käyttäjäsivut, jotka näyttävät jokaisesta käyttäjästä tilastoja ja käyttäjän lisäämät pelaajat tai joukkueet.
* Käyttäjä pystyy valitsemaan pelaajalle tai joukkueelle yhden tai useamman luokittelun. Mahdolliset luokat ovat tietokannassa.
* Sovelluksessa on pelaaja- tai joukkuetiedon lisäksi kiinnostus- ja kysymyspainike, jolla joukkue tai pelaaja voi ilmaista kiinnostuksensa joukkueeseen tai pelaajaan.