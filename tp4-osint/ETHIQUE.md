# ETHIQUE.md -- TP4 OSINT

Pour chaque TD, trois questions sont traitees :
- le droit : ai-je le droit de collecter cette donnee ?
- le caractere personnel : la donnee est-elle nominative / privee ?
- la discretion : la collecte respecte-t-elle la cible (robots.txt, User-Agent, throttling) ?

---

## TD 4.1 -- Empreinte d'un domaine

### 1. Ai-je le droit ?

Oui. Les informations issues du WHOIS et des journaux Certificate Transparency (crt.sh)
sont accessibles publiquement et consultables sans authentification.

La collecte consiste uniquement a recuperer des informations exposees publiquement :
noms de domaine, certificats, dates, registrar, serveurs DNS ou informations techniques.

Aucune tentative d'acces a une zone privee, aucun contournement d'une protection
technique et aucune exploitation d'une vulnerabilite ne sont realises. L'article 323-1
du code penal concernant l'acces frauduleux a un systeme de traitement automatise de
donnees n'est donc pas concerne.

### 2. Est-ce personnel ?

Principalement non. Les informations collectees sont majoritairement techniques :
adresse IP, registrar, serveurs DNS, certificats, sous-domaines ou informations HTTP.

Cependant, certaines sources comme le WHOIS peuvent parfois contenir des informations
nominatives (nom, email d'un contact administratif). Ces informations ne sont pas
conservees ni exploitees dans le cadre du TP.

Seules les donnees techniques utiles a l'analyse d'empreinte du domaine sont retenues.

### 3. Suis-je discret ?

Oui. La collecte respecte plusieurs bonnes pratiques :

- utilisation d'un User-Agent identifiable :
  `"IPSSI-OSINT (+cours@ipssi.fr)"` ;
- limitation du nombre de requetes ;
- ajout d'un delai entre les appels pour eviter de surcharger les services ;
- aucune tentative de contournement ou d'acces force.

La collecte est realisee dans une logique d'observation et non d'exploitation.

---

## TD 4.2 -- Cartographie d'une entite publique

### 1. Ai-je le droit ?

Oui. Les sources utilisees sont publiques :

- l'API SIRENE de data.gouv.fr est un service public permettant l'acces aux donnees
  legales des entreprises ;
- Wikipedia est une encyclopedie collaborative accessible publiquement ;
- les flux RSS de Google News permettent l'agregation d'informations publiees.

Aucune authentification, aucun contournement et aucun acces a des donnees privees
ne sont necessaires.

### 2. Est-ce personnel ?

Non dans le cadre du traitement realise. Les informations collectees concernent une
personne morale (entreprise, organisation ou institution).

Les donnees SIRENE utilisees sont des informations legales d'entreprise :
- numero SIREN ;
- denomination ;
- adresse du siege social ;
- code NAF ;
- informations administratives.

Aucun nom de salarie, aucune information privee ou donnee personnelle sensible
n'est extraite ou conservee.

### 3. Suis-je discret ?

Oui. Plusieurs mesures sont appliquees :

- utilisation d'un User-Agent identifiable ;
- limitation du nombre de requetes par source ;
- ajout d'un delai entre les interrogations ;
- limitation du volume d'articles de presse recuperes.

La collecte reste proportionnee au besoin du TP.

---

## TD 4.3 -- Veille automatisee avec Scrapy

### 1. Ai-je le droit ?

Oui. Les flux RSS des medias surveilles (Le Monde, Les Echos, Le Figaro, BFMTV,
01net) sont publies volontairement afin d'etre consultes par des lecteurs RSS
et des outils d'agregation.

Le spider utilise uniquement ces flux publics et ne cherche pas a contourner
des protections techniques.

La configuration Scrapy utilise :

- `ROBOTSTXT_OBEY = True` afin de respecter les indications techniques
  fournies par les sites ;
- un User-Agent identifiable ;
- une vitesse de collecte limitee.

### 2. Est-ce personnel ?

Non. Les informations collectees correspondent a des contenus publics :

- titre ;
- resume ;
- source ;
- date de publication ;
- lien ;
- score d'alerte.

Le traitement repose sur une analyse automatique par mots-cles et ne constitue
pas un profilage d'individus.

Les donnees collectees concernent des articles et des sujets d'actualite,
pas des personnes physiques identifiees.

### 3. Suis-je discret ?

Oui. La configuration Scrapy limite l'impact sur les sources :

- `USER_AGENT` identifiable ;
- `DOWNLOAD_DELAY = 1.0` ;
- `CONCURRENT_REQUESTS_PER_DOMAIN = 1` ;
- `ROBOTSTXT_OBEY = True` ;
- absence de requetes inutiles ou repetees.

Le spider fonctionne dans une logique de veille et non de collecte massive.

---

## Bonus -- Que revele la liste des sous-domaines sur l'architecture interne ?

Une liste de sous-domaines peut fournir des indices sur l'organisation technique
d'un systeme d'information.

Par exemple :

- `dev.` peut indiquer un environnement de developpement ;
- `staging.` peut correspondre a une plateforme de test ;
- `api.` peut reveler l'existence d'un service applicatif ;
- `mail.` peut indiquer une infrastructure de messagerie ;
- `vpn.` peut signaler un acces distant.

Ces informations peuvent aider a comprendre la surface exposee d'une organisation
dans un contexte d'audit ou d'analyse OSINT.

Cependant, la simple decouverte d'un sous-domaine ne donne pas acces aux services
associes. L'analyse reste passive et ne comprend aucune tentative d'intrusion ou
d'exploitation.