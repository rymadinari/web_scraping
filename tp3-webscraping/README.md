# TP3 - Web Scraping avec Scrapy

## Présentation

Ce projet a été réalisé dans le cadre du TP3 de Web Scraping. Il a pour objectif de mettre en pratique le framework **Scrapy** afin de collecter des données depuis différents sites web tout en respectant les bonnes pratiques de scraping (robots.txt, limitation des requêtes, pipelines, export des données, stockage en base de données).

Le projet est composé de deux applications Scrapy indépendantes :

* **AlloCiné** : récupération des informations sur les meilleurs films.
* **Boursorama** : récupération des données des actions françaises.

---

## Structure du projet

```text
tp3-webscraping/
│
├── allocine/
│   ├── scrapy.cfg
│   └── allocine/
│       ├── spiders/
│       ├── items.py
│       ├── pipelines.py
│       └── settings.py
│
└── boursorama/
    ├── scrapy.cfg
│   └── boursorama/
│       ├── spiders/
│       ├── items.py
│       ├── pipelines.py
│       └── settings.py
```

---

# TP3.1 – AlloCiné

## Objectif

Développer un spider Scrapy capable de parcourir le classement des meilleurs films d'AlloCiné et d'extraire les informations principales de chaque film.

## Données collectées

* Titre
* Année de sortie
* Réalisateur
* Note presse
* Note spectateurs
* URL de la fiche du film

## Fonctionnement

Le spider parcourt les 20 premières pages du classement des meilleurs films.

Pour chaque film, il suit le lien vers la fiche détaillée afin de récupérer les informations demandées.

Les données sont ensuite exportées dans les fichiers :

* `films.json`
* `films.csv`

### Exécution

```bash
cd allocine
scrapy crawl films
```

---

# TP3.2 – Boursorama

## Objectif

Développer un spider Scrapy permettant de récupérer les informations des actions françaises présentes dans le tableau des palmarès de Boursorama.

## Données collectées

* Libellé
* Cours
* Variation
* Volume
* Code ISIN

## Fonctionnement

Le spider analyse le tableau des actions françaises et extrait les informations de chaque ligne.

Les données sont automatiquement enregistrées dans une base de données SQLite :

* `bourse.db`

L'insertion est réalisée à l'aide d'un pipeline Scrapy.

### Exécution

```bash
cd boursorama
scrapy crawl cac
```

---

# Technologies utilisées

* Python 3
* Scrapy
* SQLite
* CSS Selectors

---

# Fonctionnalités réalisées

* Création de deux projets Scrapy.
* Développement de spiders avec navigation entre les pages.
* Extraction de données à partir de sélecteurs CSS.
* Utilisation d'Items Scrapy.
* Mise en place de Pipelines.
* Export des données au format JSON et CSV.
* Stockage des données dans une base SQLite.
* Configuration des paramètres Scrapy (User-Agent, AutoThrottle, Retry, Download Delay, etc.).
