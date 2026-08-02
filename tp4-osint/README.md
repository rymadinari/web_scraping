# TP4 -- OSINT (Open Source Intelligence)

Mastere Dev, Data & IA -- IPSSI

## Choix du mecanisme et justification

Le sujet laisse le choix du mecanisme de collecte pour chaque partie. Voici les choix
retenus et leurs justifications.

---

## TD 4.1 et TD 4.2 -> `requests` + `BeautifulSoup` (avec outils adaptes selon les sources)

Ces deux TD correspondent a des analyses **ponctuelles (one-shot)** : on interroge un nombre
limite de sources une seule fois par execution, sans besoin de crawl recursif ni de gestion
complexe d'une file d'URLs.

`requests` + `BeautifulSoup` sont suffisants pour les parties necessitant l'analyse de pages
HTML, car ils permettent :

- une implementation simple sous forme de script procedural ;
- une lecture facile du code (requete -> parsing -> stockage) ;
- un controle precis du User-Agent et des delais entre les requetes ;
- une maintenance plus simple qu'un framework complet lorsque le besoin reste ponctuel.

Pour les sources fournissant directement des donnees structurees (par exemple API SIRENE,
WHOIS ou Certificate Transparency), les outils adaptes sont utilises afin d'exploiter
directement ces formats.

---

## TD 4.3 -> `Scrapy`

Le besoin est different : il s'agit d'une **veille automatisee multi-sources**.

Le spider doit :

- interroger plusieurs flux RSS ;
- filtrer automatiquement les articles contenant des mots-cles ;
- extraire des informations structurees ;
- sauvegarder les resultats en CSV et SQLite ;
- appliquer des regles de collecte responsables.

Scrapy est donc adapte car il fournit nativement :

- la gestion de plusieurs sources avec `start_urls` ;
- le respect de `robots.txt` avec `ROBOTSTXT_OBEY` ;
- la limitation du rythme de collecte avec `DOWNLOAD_DELAY` ;
- la separation du traitement avec les pipelines (`CleanPipeline`, `SQLitePipeline`) ;
- l'export CSV automatique via `FEEDS` ;
- une architecture facilement extensible (notifications, deduplication, nouvelles sources).

En resume :

- script simple pour les collectes ponctuelles (TD 4.1 et TD 4.2) ;
- framework Scrapy pour une veille automatisee multi-sources (TD 4.3).

---

# Structure du projet

```
td4-osint/
|
|-- td41_domaine.py          # TD 4.1 : empreinte technique d'un domaine
|
|-- td42_entite.py           # TD 4.2 : cartographie d'une entite publique
|
|-- ETHIQUE.md               # Analyse droit / donnees personnelles / discretion
|
|-- requirements.txt
|
`-- veille/                  # TD 4.3 : projet Scrapy
    |
    |-- scrapy.cfg
    |
    `-- veille/
        |
        |-- items.py
        |-- pipelines.py
        |-- settings.py
        |
        `-- spiders/
            |
            `-- rss_spider.py
```

---

# Installation

Creation de l'environnement virtuel :

```bash
python3 -m venv venv
```

Activation :

Sous Linux / Mac :

```bash
source venv/bin/activate
```

Sous Windows :

```bash
venv\Scripts\activate
```

Installation des dependances :

```bash
pip install -r requirements.txt
```

---

# Lancement

## TD 4.1 -- Empreinte d'un domaine

Execution :

```bash
python3 td41_domaine.py wikipedia.org
```

ou :

```bash
python3 td41_domaine.py exemple.com
```

Le script genere :

```
rapport_domaine.json
```

Ce rapport contient notamment :

- informations WHOIS ;
- certificats Certificate Transparency ;
- informations DNS ;
- empreinte technique du domaine.

---

## TD 4.2 -- Cartographie d'une entite publique

Execution :

```bash
python3 td42_entite.py TotalEnergies
```

ou :

```bash
python3 td42_entite.py "Airbus"
```

Le script genere :

```
fiche_entite.json
```

La fiche contient notamment :

- informations legales issues de SIRENE ;
- informations publiques de l'entite ;
- elements issus des sources ouvertes consultees.

---

# TD 4.3 -- Veille automatisee Scrapy

Se placer dans le dossier Scrapy :

```bash
cd veille
```

Lancer le spider :

```bash
scrapy crawl rss_spider -L INFO
```

Le spider :

- consulte plusieurs flux RSS ;
- recherche les mots-cles surveilles ;
- calcule un score d'alerte ;
- enregistre les resultats.

Les fichiers generes sont :

```
mentions.csv
veille.db
```

La base SQLite contient la table :

```
mentions
```

---

# Modifier la cible surveillee

La cible OSINT peut etre modifiee dans :

```
veille/veille/spiders/rss_spider.py
```

Modifier la constante :

```python
CIBLE = "mot_cle"
```

Exemple :

```python
CIBLE = "TotalEnergies"
```

---

# Consultation rapide de la base SQLite

Depuis le dossier contenant `veille.db` :

```bash
python3 -c "
import sqlite3

cx = sqlite3.connect('veille.db')

rows = cx.execute(
    'SELECT titre, source, score_alerte FROM mentions ORDER BY score_alerte DESC'
).fetchall()

print(f'{len(rows)} mentions trouvees')

for r in rows[:5]:
    print(f' [{r[2]}] {r[0][:60]} ({r[1]})')

cx.close()
"
```

---

# Cadre legal respecte

Les regles suivantes sont appliquees pendant toute la collecte :

- utilisation uniquement de sources publiques ;
- aucune authentification necessaire ;
- aucun contournement technique ;
- aucune exploitation de vulnerabilite ;
- aucune collecte volontaire de donnees personnelles privees ;
- utilisation d'un User-Agent identifiable :

```
IPSSI-OSINT (+cours@ipssi.fr)
```

- respect des indications techniques fournies par les sites avec :

```python
ROBOTSTXT_OBEY = True
```

dans Scrapy ;

- limitation du rythme de collecte :

```python
DOWNLOAD_DELAY = 1
```

- limitation des requetes simultanees :

```python
CONCURRENT_REQUESTS_PER_DOMAIN = 1
```

La collecte reste proportionnee au besoin du TP et est realisee dans une logique
d'analyse OSINT passive.

---

# Resultats obtenus

Le TD 4.3 permet d'obtenir automatiquement :

- un fichier CSV contenant les mentions detectees ;
- une base SQLite contenant les resultats structures ;
- un score d'alerte calcule automatiquement selon les mots-cles identifies.

Structure du fichier CSV :

```
mentions.csv

|
|-- titre
|-- url
|-- source
|-- date_publi
|-- resume
`-- score_alerte
```

---

# Conclusion

Le projet met en pratique plusieurs approches OSINT :

- collecte technique d'informations sur un domaine ;
- cartographie d'une entite publique ;
- mise en place d'une veille automatisee multi-sources.

Les choix techniques sont adaptes au besoin :

- scripts simples pour les analyses ponctuelles ;
- Scrapy pour la collecte automatisee et multi-sources.