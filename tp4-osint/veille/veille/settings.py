BOT_NAME = "veille"

SPIDER_MODULES = ["veille.spiders"]
NEWSPIDER_MODULE = "veille.spiders"


ROBOTSTXT_OBEY = True


USER_AGENT = "IPSSI-OSINT-veille (+cours@ipssi.fr)"


DOWNLOAD_DELAY = 1

CONCURRENT_REQUESTS_PER_DOMAIN = 1


ITEM_PIPELINES = {

    "veille.pipelines.CleanPipeline": 300,

    "veille.pipelines.SQLitePipeline": 400,

}


FEEDS = {

    "mentions.csv": {

        "format": "csv",

        "encoding": "utf8",

        "overwrite": True,

        "fields": [

            "titre",

            "url",

            "source",

            "date_publi",

            "resume",

            "score_alerte",

        ],

    },

}


LOG_LEVEL = "INFO"