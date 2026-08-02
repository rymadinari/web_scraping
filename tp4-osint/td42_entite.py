"""
TD 4.2 -- Cartographie d'une entite publique (OSINT)
Mecanisme choisi : requests + BeautifulSoup + feedparser (voir README.md pour la justification)

Sources publiques utilisees :
- API Recherche Entreprises (SIRENE)
- Wikipedia (infobox + introduction)
- Flux RSS Google News (veille presse)
"""

import json
import sys
import time

import feedparser
import requests
from bs4 import BeautifulSoup


HEADERS = {
    "User-Agent": "IPSSI-OSINT (+cours@ipssi.fr)"
}


def chercher_sirene(nom: str) -> dict:
    """
    Recherche une entreprise via l'API officielle.
    """

    url = "https://recherche-entreprises.api.gouv.fr/search"

    params = {
        "q": nom,
        "page": 1,
        "per_page": 1
    }

    try:

        r = requests.get(
            url,
            headers=HEADERS,
            params=params,
            timeout=10
        )

        r.raise_for_status()

        data = r.json()


        if data.get("results"):

            ent = data["results"][0]

            return {

                "siren": ent.get("siren"),

                "denomination": ent.get("nom_complet"),

                "adresse_siege": ent.get("siege", {}).get("adresse"),

                "code_naf": ent.get("activite_principale"),

                "date_creation": ent.get("date_creation"),

                "tranche_effectif": ent.get(
                    "tranche_effectif_salarie"
                )

            }


        return {
            "resultat": "Non trouve dans SIRENE"
        }


    except Exception as e:

        return {
            "erreur": str(e)
        }





def scraper_wikipedia(nom: str) -> dict:
    """
    Extraction Wikipedia :
    - infobox
    - introduction
    """

    slug = nom.replace(
        " ",
        "_"
    )

    url = (
        f"https://fr.wikipedia.org/wiki/{slug}"
    )


    try:

        r = requests.get(
            url,
            headers=HEADERS,
            timeout=10
        )


        r.raise_for_status()


        soup = BeautifulSoup(
            r.text,
            "lxml"
        )



        # -------------------------
        # Infobox
        # -------------------------

        infobox = {}


        table = soup.select_one(
            "table.infobox"
        )


        if table:

            for tr in table.select("tr"):

                th = tr.find("th")

                td = tr.find("td")


                if th and td:

                    cle = th.get_text(
                        " ",
                        strip=True
                    )


                    valeur = td.get_text(
                        " ",
                        strip=True
                    )[:200]


                    infobox[cle] = valeur




        # -------------------------
        # Introduction Wikipedia
        # -------------------------

        intro = ""


        contenu = soup.select_one(
            "div.mw-parser-output"
        )


        if contenu:

            for p in contenu.find_all(
                "p",
                recursive=False
            ):

                texte = p.get_text(
                    " ",
                    strip=True
                )


                if len(texte) > 100:

                    intro = texte[:500]

                    break



        # Sécurité si la structure change

        if not intro:

            for p in soup.find_all("p"):

                texte = p.get_text(
                    " ",
                    strip=True
                )


                if len(texte) > 100:

                    intro = texte[:500]

                    break



        return {

            "infobox": infobox,

            "intro": intro,

            "url": url

        }



    except Exception as e:

        return {
            "erreur": str(e)
        }





def veille_presse(nom: str, nb_max: int = 10) -> list:
    """
    Recherche des articles via Google News RSS.
    """

    query = nom.replace(
        " ",
        "+"
    )


    url = (
        "https://news.google.com/rss/search?"
        f"q={query}&hl=fr&gl=FR&ceid=FR:fr"
    )


    try:

        feed = feedparser.parse(
            url,
            request_headers=HEADERS
        )


        articles = []


        for e in feed.entries[:nb_max]:

            articles.append({

                "titre": e.get(
                    "title",
                    ""
                ),

                "source": e.get(
                    "source",
                    {}
                ).get(
                    "title",
                    ""
                ),

                "date": e.get(
                    "published",
                    ""
                ),

                "lien": e.get(
                    "link",
                    ""
                )

            })


        return articles



    except Exception as e:

        return [
            {
                "erreur": str(e)
            }
        ]







def construire_fiche(nom: str) -> dict:

    print(
        f"[*] Construction de la fiche pour : {nom}"
    )


    fiche = {
        "entite": nom
    }


    # SIRENE

    fiche["sirene"] = chercher_sirene(nom)


    time.sleep(1)



    # Wikipedia

    fiche["wikipedia"] = scraper_wikipedia(nom)


    time.sleep(1)



    # Presse

    fiche["presse"] = veille_presse(nom)


    fiche["nb_articles"] = len(
        fiche["presse"]
    )


    return fiche







if __name__ == "__main__":


    nom = (
        " ".join(sys.argv[1:])
        if len(sys.argv) > 1
        else "TotalEnergies"
    )


    fiche = construire_fiche(
        nom
    )



    with open(
        "fiche_entite.json",
        "w",
        encoding="utf-8"
    ) as f:


        json.dump(
            fiche,
            f,
            indent=2,
            ensure_ascii=False
        )



    print(
        "[+] Fiche sauvegardee : fiche_entite.json"
    )


    print(
        f"    SIREN : {fiche['sirene'].get('siren', 'n/a')}"
    )


    print(
        f"    Articles: {fiche['nb_articles']}"
    )