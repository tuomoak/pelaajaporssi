# pelaajaporssi

Sovelluksen tarkoitus on auttaa siinä, että pelaajat löytäisivät itselleen joukkueen ja joukkueet löytäisivät itselleen täydennystä.

Suunniteltuja ominaisuuksia:
* Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen.
* Käyttäjä pystyy lisäämään sovellukseen joko pelaajia tai joukkueita. Lisäksi käyttäjä pystyy muokkaamaan ja poistamaan lisäämänsä pelaajan tai joukkueen tietoja.
* Käyttäjä näkee sovellukseen lisätyt pelaajat ja joukkueet. Käyttäjä näkee sekä itse lisäämänsä että muiden käyttäjien lisäämät pelaajat ja joukkueet.
* Käyttäjä pystyy etsimään pelaajia tai joukkueita hakusanalla tai muulla perusteella. Käyttäjä pystyy hakemaan sekä itse lisäämiään että muiden käyttäjien lisäämiä pelaajia tai joukkueita. Pelaaja- tai joukkuetiedon lisännyt voi myös valita, ettei tietoja näy hakutuloksissa.
* Sovelluksessa on käyttäjäsivut, jotka näyttävät jokaisesta käyttäjästä tilastoja ja käyttäjän lisäämät pelaajat tai joukkueet.
* Käyttäjä pystyy valitsemaan pelaajalle tai joukkueelle yhden tai useamman luokittelun. Mahdolliset luokat ovat tietokannassa.
* Sovelluksessa on pelaaja- tai joukkuetiedon lisäksi kiinnostus- ja kysymyspainike, jolla joukkue tai pelaaja voi ilmaista kiinnostuksensa joukkueeseen tai pelaajaan.

---------------------
Ohje sovelluksen testaajalle
----------------------

Sovelluksen käynnistys edellyttää:

database.db-tiedosto schema.sql-tiedoston avulla

Linuxissa:

$ sqlite3 database.db < schema.sql

$ sqlite3 database.db < init.sql

Windowsissa:

sqlite3 database.db

sqlite> .read schema.sql

sqlite> .read init.sql

----------------------------------------------------
