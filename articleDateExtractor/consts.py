

FAILED = "articleDateExtractor_failed_total"
SUCCESS = "articleDateExtractor_success_total"

DATETIME_TAG_REGEX = "pub+|article+|date+|time+|tms+|mod+"

URL_REGEXPS = [
    r'([./\-_]?(19|20)\d{2})[./\-_]?(([0-3]?[0-9][./\-_])|(\w{3,5}[./\-_]))([0-3]?[0-9][./\-]?)?',
    r'(\d{8,12})'
]

META_NAMES = [
    "pubdate", "publishdate", "timestamp",
    "dc.date.issued", "date", "sailthru.date",
    "article.published", "published-date",
    "article.created", "article_date_original",
    "cxenseparse:recs:publishtime", "date_published",
]
META_PROPERTIES = ["bt:pubdate", "og:release_date"]
META_PROPS = ["datepublished", "datecreated"]
META_EQUIVS = ["date"]
META_ATTRS = ["name", "itemprop", "http-equiv", "property", "content"]

TAGS_ATTRS = {
    "id": ['span', 'p', 'div', 'li'],
    "class_": ['span', 'p', 'div']
}
