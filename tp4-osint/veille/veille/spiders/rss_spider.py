import scrapy
import feedparser
import re
from datetime import datetime

from veille.items import MentionItem


class RssSpider(scrapy.Spider):
    name = "rss_spider"

    allowed_domains = [
        "lemonde.fr",
        "lefigaro.fr",
        "01net.com",
        "bfmtv.com",
        "lesechos.fr"
    ]

    start_urls = [
        "https://www.lemonde.fr/rss/une.xml",
        "https://www.lefigaro.fr/rss/figaro_actualites.xml",
        "https://www.01net.com/feed/",
        "https://www.bfmtv.com/rss/news-24-7/",
        "https://www.lesechos.fr/rss/rss_une.xml",
    ]


    # mots recherchés OSINT
    keywords = [
        "apple",
        "iphone",
        "chatgpt",
        "openai",
        "intelligence artificielle",
        "ia",
        "cyber",
        "piratage",
        "hacker",
        "bitcoin",
        "cryptomonnaie",
        "immobilier",
        "guerre",
        "crise",
        "sécurité"
    ]


    custom_settings = {
        "ITEM_PIPELINES": {
            "veille.pipelines.CleanPipeline": 300,
            "veille.pipelines.SQLitePipeline": 400,
        }
    }


    def parse(self, response):

        self.logger.info(f"Analyse RSS : {response.url}")

        feed = feedparser.parse(response.text)


        self.logger.info(
            f"{len(feed.entries)} articles trouvés"
        )


        for article in feed.entries:

            titre = article.get("title", "")
            resume = article.get("description", "")

            texte = (
                titre + " " + resume
            ).lower()


            score = 0
            mot_trouve = None


            for keyword in self.keywords:

                if keyword.lower() in texte:
                    score += 1
                    mot_trouve = keyword
                    break


            # Si un mot clé est trouvé
            if mot_trouve:


                self.logger.info(
                    f"Mention trouvée ({mot_trouve}) : {titre}"
                )


                item = MentionItem()


                item["titre"] = titre

                item["url"] = article.get(
                    "link",
                    ""
                )

                item["source"] = response.url.split("/")[2]

                item["date_publi"] = article.get(
                    "published",
                    ""
                )

                item["resume"] = re.sub(
                    "<.*?>",
                    "",
                    resume
                )


                item["score_alerte"] = score


                yield item