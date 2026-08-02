"""
TD 4.1 -- Empreinte d'un domaine (OSINT)
Mecanisme choisi : requests + python-whois (voir README.md pour la justification)

Sources publiques utilisees :
- WHOIS du domaine
- Headers HTTP du site cible
- Certificate Transparency (crt.sh) pour les sous-domaines
- robots.txt du domaine
"""

import json
import socket
import sys
import time

import requests
import whois  # pip install python-whois


HEADERS = {
    "User-Agent": "IPSSI-OSINT (+cours@ipssi.fr)"
}


def nettoyer_date(date):
    """
    Nettoie les dates WHOIS.
    Certains domaines retournent une liste de dates.
    """

    if isinstance(date, list):
        date = date[0] if date else None

    return str(date or "n/a")[:10]


def analyse_whois(domaine: str) -> dict:
    """Recupere les informations WHOIS du domaine."""

    try:
        w = whois.whois(domaine)

        return {
            "registrar": str(w.registrar or "n/a"),
            "creation_date": nettoyer_date(w.creation_date),
            "expiration_date": nettoyer_date(w.expiration_date),
            "name_servers": sorted(list(set(w.name_servers or []))),
            "country": str(w.country or "n/a"),
        }

    except Exception as e:
        return {
            "erreur": str(e)
        }


def analyse_headers(domaine: str) -> dict:
    """Analyse les principaux headers HTTP."""

    try:
        r = requests.head(
            f"https://{domaine}",
            headers=HEADERS,
            timeout=10,
            allow_redirects=True,
        )

        h = r.headers

        return {
            "status": r.status_code,
            "server": h.get("Server", "n/a"),
            "x_powered_by": h.get("X-Powered-By", "n/a"),
            "x_frame_options": h.get("X-Frame-Options", "n/a"),
            "csp_present": "Content-Security-Policy" in h,
            "hsts_present": "Strict-Transport-Security" in h,
        }

    except Exception as e:
        return {
            "erreur": str(e)
        }


def sous_domaines_crtsh(domaine: str) -> list:
    """
    Recherche les sous-domaines via crt.sh
    (Certificate Transparency Logs).
    """

    url = "https://crt.sh/"

    params = {
        "q": f"%.{domaine}",
        "output": "json"
    }

    try:

        r = requests.get(
            url,
            params=params,
            headers=HEADERS,
            timeout=60,
        )

        r.raise_for_status()

        data = r.json()

        sous_domaines = set()

        for entry in data:

            noms = entry.get(
                "name_value",
                ""
            ).splitlines()


            for nom in noms:

                nom = nom.strip()

                if not nom:
                    continue

                if "*" in nom:
                    continue

                if nom.endswith(domaine):
                    sous_domaines.add(nom)


        return sorted(sous_domaines)[:100]


    except Exception as e:

        print(f"[!] crt.sh indisponible : {e}")

        return []


def analyse_robots(domaine: str) -> str:
    """Recupere le contenu de robots.txt."""

    try:

        r = requests.get(
            f"https://{domaine}/robots.txt",
            headers=HEADERS,
            timeout=10,
        )


        if r.status_code == 200:
            return r.text[:1000]


        return f"HTTP {r.status_code}"


    except Exception as e:

        return str(e)



def analyser_domaine(domaine: str) -> dict:
    """Construit le rapport complet."""

    print(f"[*] Analyse de {domaine}...")


    try:
        ip = socket.gethostbyname(domaine)

    except socket.gaierror:

        ip = "n/a"



    rapport = {

        "domaine": domaine,

        "ip": ip,

        "whois": analyse_whois(domaine),

        "headers_http": analyse_headers(domaine),

        "sous_domaines": sous_domaines_crtsh(domaine),

        "robots_txt": analyse_robots(domaine),

    }


    rapport["nb_sous_domaines"] = len(
        rapport["sous_domaines"]
    )


    return rapport



if __name__ == "__main__":


    domaine = (
        sys.argv[1]
        if len(sys.argv) > 1
        else "wikipedia.org"
    )


    # Respect de la cible
    time.sleep(1)


    rapport = analyser_domaine(domaine)


    sortie = "rapport_domaine.json"


    with open(
        sortie,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            rapport,
            f,
            indent=2,
            ensure_ascii=False
        )


    print(f"[+] Rapport sauvegarde : {sortie}")

    print(
        f"    {rapport['nb_sous_domaines']} sous-domaines trouvés"
    )

    print(
        f"    Serveur : {rapport['headers_http'].get('server', 'n/a')}"
    )