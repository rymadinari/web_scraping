"""
TP2 - IPSSI - Selenium
Scraper Doctolib : fiches medecins pour une specialite + ville donnees.

Usage:
    python doctolib_scraper.py --specialite cardiologue --ville lyon
    python doctolib_scraper.py --specialite cardiologue --ville lyon --headless
"""
import argparse
import json
import os
import re
import time

from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

SCREENSHOTS_DIR = "screenshots"


def make_driver(headless: bool = False) -> webdriver.Chrome:
    options = webdriver.ChromeOptions()
    if headless:
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-gpu")
    # Reduit (sans l'eliminer) le signal "je suis un robot"
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    return webdriver.Chrome(options=options)


def screenshot_echec(driver, nom: str) -> None:
    """Sauvegarde une capture d'ecran en cas d'echec, pour debug."""
    os.makedirs(SCREENSHOTS_DIR, exist_ok=True)
    chemin = os.path.join(SCREENSHOTS_DIR, nom)
    try:
        driver.save_screenshot(chemin)
        print(f"Screenshot d'echec sauvegarde : {chemin}")
    except Exception as e:
        print(f"Impossible de sauvegarder le screenshot : {e}")


def accepter_cookies(driver, wait: WebDriverWait) -> None:
    """Strategie 1 (recommandee) : cliquer sur le bouton d'acceptation.
    Ne fait rien de bloquant si la banniere n'apparait pas."""
    try:
        btn = wait.until(EC.element_to_be_clickable(
            (By.XPATH, '//button[contains(text(),"Accepter") or contains(text(),"Tout accepter")]')
        ))
        btn.click()
        print("Cookies acceptes")
    except TimeoutException:
        print("Pas de banniere cookies detectee (ou deja geree)")


def attendre_resultats(driver, wait: WebDriverWait) -> None:
    """Attend que les résultats de recherche soient visibles. Capture un screenshot si echec."""
    try:
        wait.until(lambda d: len(d.find_elements(By.CSS_SELECTOR, "a[href*='/cardiologue/'], a[href*='/cabinet-medical/']")) >= 5)
        print("Resultats charges")
    except TimeoutException as e:
        screenshot_echec(driver, "doctolib_erreur_resultats.png")
        raise RuntimeError(f"Resultats non charges : {e}")


def scroll_to_bottom(driver, pauses: int = 3) -> None:
    """Defile jusqu'en bas pour declencher le chargement du contenu paresseux."""
    last_h = driver.execute_script("return document.body.scrollHeight")
    for _ in range(pauses):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        time.sleep(1.5)
        new_h = driver.execute_script("return document.body.scrollHeight")
        if new_h == last_h:
            break
        last_h = new_h


def _premier_texte(carte, selecteurs: list[str]) -> str:
    """Essaie plusieurs selecteurs dans l'ordre (fallback, Defi 3) et renvoie
    le premier texte non vide trouve."""
    for sel in selecteurs:
        elements = carte.find_elements(By.CSS_SELECTOR, sel)
        if elements and elements[0].text.strip():
            return elements[0].text.strip()
    return "n/a"


def _texte_clair(element) -> str:
    return re.sub(r"\s+", " ", element.text).strip()


def _extraire_adresse(texte: str, nom: str) -> str:
    texte = re.sub(r"\s+", " ", texte).strip()
    if nom and texte.startswith(nom):
        texte = texte[len(nom):].lstrip()
    for token in ["Cardiologue", "Cardiologie", "Médecin"]:
        if token in texte:
            texte = texte.replace(token, "", 1)
            break
    texte = texte.strip(" -:")
    for sep in ["Conventionné", "avec", "Consultation", "Disponibilités", "En ligne", "secteur"]:
        if sep in texte:
            texte = texte.split(sep, 1)[0].rstrip(" -")
            break
    return texte.strip(" ,") or "n/a"


def extraire_medecins(driver, limite: int = 10) -> list[dict]:
    liens = driver.find_elements(By.CSS_SELECTOR, "a[href*='/cardiologue/'], a[href*='/cabinet-medical/']")
    resultats = []
    for lien in liens[:limite]:
        try:
            card = lien.find_element(By.XPATH, "./ancestor::div[contains(@class,'dl-card')][1]")
        except NoSuchElementException:
            card = lien

        try:
            nom = _premier_texte(lien, ["h2", "h3", "[class*='name']", "[data-test*='name']"])
            if not nom:
                nom = _premier_texte(card, ["h2", "h3", "[class*='name']", "[data-test*='name']"])

            texte_carte = _texte_clair(card)
            adresse = _extraire_adresse(texte_carte, nom)
            url = lien.get_attribute("href") or "n/a"

            creneaux = [
                el.text.strip()
                for el in card.find_elements(By.CSS_SELECTOR, "button, [class*='slot'], [class*='availability']")[:3]
                if el.text.strip()
            ]
            texte_carte_bas = texte_carte.lower()
            types = []
            if "vidéo" in texte_carte_bas or "video" in texte_carte_bas:
                types.append("Consultation vidéo")
            if "présentiel" in texte_carte_bas or "presentiel" in texte_carte_bas:
                types.append("Présentiel")
            if not types:
                types = ["n/a"]

            resultats.append({
                "nom_specialite": nom or "n/a",
                "adresse": adresse,
                "type_consultation": types,
                "prochains_creneaux": creneaux or ["n/a"],
                "url_fiche": url,
            })
        except (NoSuchElementException, StaleElementReferenceException) as e:
            print(f"Carte ignoree (element manquant) : {e}")
    return resultats


def main():
    p = argparse.ArgumentParser(description="Scraper Doctolib")
    p.add_argument("--specialite", default="cardiologue")
    p.add_argument("--ville", default="lyon")
    p.add_argument("--headless", action="store_true")
    p.add_argument("--out", default="doctolib.json")
    args = p.parse_args()

    url = f"https://www.doctolib.fr/{args.specialite}/{args.ville}"
    print(f"Cible : {url}")

    driver = make_driver(headless=args.headless)
    wait = WebDriverWait(driver, 15)

    try:
        driver.get(url)
        accepter_cookies(driver, wait)
        attendre_resultats(driver, wait)
        scroll_to_bottom(driver)
        medecins = extraire_medecins(driver)
    except Exception as e:
        screenshot_echec(driver, "doctolib_erreur_fatale.png")
        print(f"Erreur : {e}")
        medecins = []
    finally:
        driver.quit()

    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(medecins, f, indent=2, ensure_ascii=False)
    print(f"{len(medecins)} medecins exportes dans {args.out}")


if __name__ == "__main__":
    main()
