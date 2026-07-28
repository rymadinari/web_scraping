# TP2 - Selenium : Doctolib & Les Échos

## 1. Objectif du TP

Ce TP a permis d’explorer l’utilité de Selenium pour scraper des sites dont le contenu est chargé dynamiquement par JavaScript. Nous avons mis en place deux scripts Python :

- un scraper pour Doctolib, qui récupère les fiches de médecins à partir d’une spécialité et d’une ville
- un scraper pour Les Échos, qui récupère les articles de la page d’accueil

## 2. Pourquoi Selenium et pas requests ?

Les pages de Doctolib et de Les Échos ne présentent pas tout leur contenu dans le HTML brut initial. Une requête classique avec `requests` récupère seulement la structure de base de la page, sans exécuter le JavaScript du navigateur. Or, c’est précisément ce JavaScript qui charge les résultats de recherche et les articles affichés à l’écran.

Dans notre test sur Les Échos, la méthode `requests` seule n’a trouvé aucune balise de titre pertinente dans le HTML brut. Cela confirme que Selenium est nécessaire pour obtenir le contenu réel affiché par le site.

## 3. Gestion de la bannière cookies

Pour Doctolib, une stratégie de clic sur le bouton “Accepter” a été mise en place avec `WebDriverWait` et `element_to_be_clickable`. Si la bannière n’apparaît pas, le script ne bloque pas et continue l’exécution.

Cette approche permet de gérer proprement les consentements cookies sans faire échouer le scraping lorsqu’aucune bannière n’est visible.

## 4. Utilisation de WebDriverWait plutôt que time.sleep()

Le script n’utilise pas de `time.sleep()` fixe dans le flux principal. À la place, il attend des éléments réels du DOM via `WebDriverWait` et `ExpectedConditions`.

Cela rend le programme plus robuste, car il attend un état concret de la page au lieu d’attendre une durée arbitraire.

## 5. Scroll pour charger du contenu paresseux

Pour Doctolib, un scroll progressif a été ajouté afin de déclencher le chargement de plus de résultats. Cette étape est utile lorsque le site affiche du contenu au fur et à mesure que la page défile.

## 6. Mode headless et comparaison des performances

Le script Les Échos permet aussi une comparaison entre le mode normal et le mode headless.

| Mode | Temps observé |
|------|---------------|
| Normal | 9.3 s |
| Headless | 24.3 s |
| Gain | 0.4x plus rapide en headless |

Dans cet environnement, le mode headless s’est révélé plus lent que le mode normal. Cela montre que les performances dépendent du navigateur, du système et de la façon dont le site se charge.

## 7. Screenshot en cas d’échec

Un dossier `screenshots/` a été créé automatiquement. En cas d’échec de chargement ou d’exception, une capture d’écran est sauvegardée pour faciliter le debug.

## 8. Résultats obtenus

Les scripts ont bien généré les fichiers JSON attendus :

- `doctolib.json` avec plusieurs médecins extraits
- `lesechos.json` avec plusieurs articles extraits

## 9. Conclusion

Ce TP a permis de comprendre l’intérêt de Selenium pour le scraping de sites web dynamiques, ainsi que les bonnes pratiques liées à l’attente de contenu, à la gestion des cookies et à la robustesse du script.
