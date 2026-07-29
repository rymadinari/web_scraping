import scrapy
import re

from allocine.items import FilmItem


class FilmsSpider(scrapy.Spider):
    name = "films"
    allowed_domains = ["www.allocine.fr"]

    # Environ 200 films (20 pages x ~10 films)
    start_urls = [
        f"https://www.allocine.fr/film/meilleurs/?page={page}"
        for page in range(1, 21)
    ]

    custom_settings = {
        "DOWNLOAD_DELAY": 1.0,
        "ROBOTSTXT_OBEY": True,
    }

    def parse(self, response):
        liens = response.css(
            "h2.meta-title a::attr(href)"
        ).getall()

        self.logger.info(
            f"{len(liens)} liens de films trouvés sur {response.url}"
        )

        for lien in liens:
            yield response.follow(
                lien,
                callback=self.parse_film
            )


    def parse_film(self, response):

        def safe(selector):
            value = response.css(selector).get()
            return value.strip() if value else ""


        def safe_all(selector):
            values = response.css(selector).getall()
            return [
                v.strip()
                for v in values
                if v.strip()
            ]


        # -----------------------
        # Titre
        # -----------------------

        titre = safe("h1::text")


        # -----------------------
        # Notes
        # -----------------------

        notes = safe_all(".stareval-note::text")

        note_presse = (
            notes[0]
            if len(notes) > 0
            else ""
        )

        note_spectateurs = (
            notes[1]
            if len(notes) > 1
            else ""
        )


        # -----------------------
        # Année depuis <title>
        # Exemple :
        # "Film 2001 - AlloCiné"
        # -----------------------

        annee = ""

        titre_page = response.css(
            "title::text"
        ).get()

        if titre_page:
            match = re.search(
                r"Film (\d{4})",
                titre_page
            )

            if match:
                annee = match.group(1)


        # -----------------------
        # Réalisateur
        # -----------------------

        textes_direction = response.css(
            ".meta-body-direction"
        ).xpath(".//text()").getall()


        realisateur = ""

        for texte in textes_direction:

            texte = texte.strip()

            if texte and texte not in [
                "De",
                "Par"
            ]:
                realisateur = texte
                break


        # -----------------------
        # Item final
        # -----------------------

        yield FilmItem(

            titre=titre,

            annee=annee,

            realisateur=realisateur,

            note_presse=note_presse,

            note_spectateurs=note_spectateurs,

            url=response.url,
        )