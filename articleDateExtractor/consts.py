import re

FAILED = "articleDateExtractor_failed_total"
SUCCESS = "articleDateExtractor_success_total"

DATETIME_TAG_REGEX = "pub+|article+|date+|time+|tms+|mod+"

URL_REGEXPS = [
    r'([./\-_]?(19|20)\d{2})[./\-_]?(([0-3]?[0-9][./\-_])|(\w{3,5}[./\-_]))([0-3]?[0-9][./\-]?)?',
    r'(\d{8,12})',
    r'(\d{4}-\d{2}-\d{2})',
    r'(\d{2}-\d{2}-\d{4})',
    r'(\d{2}/\d{2}/\d{4})',
    r'(\d{4}/\d{2}/\d{2})',
]

META_NAMES = [
    "pubdate", "publishdate", "timestamp", "dc.date"
                                           "dc.date.issued", "date", "sailthru.date",
    "article.published", "published-date",
    "article.created", "article_date_original",
    "cxenseparse:recs:publishtime", "date_published",
    "citation_publication_date", "article:published_time"
]
META_PROPERTIES = [
    "bt:pubdate", "og:release_date", "datepublished",
    "datecreated", "article:published_time", "og:publish_date",
    "startdate", "publish-date"
]
META_PROPS = [
    "datepublished", "datecreated", "article:published_time",
    "og:publish_date", "bt:pubdate", "og:release_date",
    "startdate"
]
META_EQUIVS = ["date"]
META_ATTRS = ["name", "itemprop", "http-equiv", "property", "content"]

TAGS_ATTRS = {
    "id": ['span', 'p', 'div', 'li'],
    "class_": ['span', 'p', 'div', 'abbr']
}

SCRIPT_CLEANER = re.compile('<script[^>]*>.*?</script>', flags=re.DOTALL)
HTML_CLEANER = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});', flags=re.DOTALL)

DATE_FORMATS = {
    r'([a-zA-Z]+)\s*(\d{1,2}[a-zA-Z]*)\s*,?\s*(\d{4})': False,  # December (25st/25) (,/) 2023
    r'(\d{1,2})\s*([a-zA-Z]+)\s*,?\s*(\d{4})': False,  # 30 December 2023
    r'(\d{1,4})\s*/\s*(\d{1,4})\s*/\s*(\d{1,4})': False,  # 30/5/2023 / 2023/30/5
    r'(\d{1,4})\s*\.\s*(\d{1,4})\s*\.\s*(\d{1,4})': False,  # 20.8.2023
    r'(\d{1,4})\s*-\s*(\d{1,4})\s*-\s*(\d{1,4})': False,  # 20-8-2023
    # u'(\d{1,4})\s*(\D+)\s*(\d{1,4})': True,  # 2 maggio 2022 / 2022 maggio 2
    # u'(\d{1,4})\s*/\s*(\w+)\s*/\s*(\d{1,4})': True,  # 2/maggio/2022 / 2022/maggio/2
    # To add in the next version.
}

MONTHS_TRANSLATION = {
    u'jan': [
        u'\u4e00\u6708', u'led', u'sij', u'oca', u'ion', u'gen', u'sty', u'ian', u'\u044f\u043d\u0443',
             u'\u044f\u043d\u0432', u'ene', u'tam', u'J\xe4n', u'j\xe4n', u'\u05d9\u05e0\u05d5', u'\u064a\u0646\u0627',
             u'\u0399\u03b1\u03bd', u'&#1489;&#1497;&#1504;&#1493;&#1488;&#1512;', u'subat'],
    u'feb':
        [u'\u4e8c\u6708', u'\u00fano', u'vel', u'fev', u'\u015fub', u'f\u00e9v', u'chw', u'lut', u'\u044f\u0435\u0432',
         u'\u0444\u0435\u0432', u'hel', u'\u05e4\u05d1\u05e8', u'\u0641\u0628\u0631', u'\u03a6\u03b5\u03b2',
         u'\u0634\u0628\u0627', u'&#1489;&#1508;&#1489;&#1512;&#1493;&#1488;&#1512;'],
    u'mar': [u'\u4e09\u6708', u'b\u0159e', u'o\u017Eu', u'm\u00e4r', u'maw', u'maa', u'mrz', u'mrt', u'map',
             u'\u039c\u03b1\u03c1', u'\u043c\u0430\u0440', u'\u05de\u05e8\u05e5', u'\u006d\u00e1\u0072\u0063',
             u'\u05de\u05e8\u05e1', u'\u0645\u0627\u0631', u'\u03c0\u03bf\u03c1', u'\u0622\u0630\u0627',
             u'\u0627\u0630\u0627', u'&#1489;&#1502;&#1512;&#1509;'],
    u'apr': [u'\u56db\u6708', u'dub', u'huh', u'tra', u'abr', u'nis', u'avr', u'ebr', u'kwi', u'\u0430\u043f\u0440',
             u'\u00e1pr', u'\u05d0\u05e4\u05e8', u'\u0623\u0628\u0631', u'\u0627\u0628\u0631', u'\u0391\u03c0\u03c1',
             u'\u0646\u064a\u0633', u'&#1489;&#1488;&#1508;&#1512;&#1497;&#1500;'],
    u'may':
        [u'\u4e94\u6708', u'kv\u011b', u'voi', u'svi', u'mai', u'mei', u'mag', u'maj',
         u'\u039c\u03ac\u03b9\u03bf\u03c2',
         u'\u039c\u03b1\u03ca', u'\u043c\u0430\u0439', u'm\u00e1j', u'\u05de\u05d0\u05d9', u'\u0645\u0627\u064a',
         u'\u03bc\u03c0\u03bf', u'\u043c\u043e\u0436', u'\u043C\u0430\u044F', u'\u0623\u064a\u0627',
         u'\u0622\u064a\u0627',
         u'&#1489;&#1502;&#1488;&#1497;'],
    u'jun': [u'\u516d\u6708', u'kes', u'lip', u'haz', u'meh', u'giu', u'cze', u'iun', u'\u0399\u03bf\u03c5\u03bd',
             u'\u0438\u044e\u043d', u'j\u00fan', u'\u05d9\u05d5\u05e0', u'\u064a\u0648\u0646', u'\u044e\u043d\u0438',
             u'\u062d\u0632\u064a', u'&#1489;&#1497;&#1493;&#1504;&#1497;'],
    u'jul': [u'\u4e03\u6708', u'hei', u'srp', u'gor', u'lug', u'lip', u'iul', u'\u0399\u03bf\u03c5\u03bb',
             u'\u0399\u03bf\u03cd\u03bb', u'\u044e\u043b\u0438', u'\u0438\u044e\u043b', u'j\u00fal',
             u'\u05d9\u05d5\u05dc', u'\u064a\u0648\u0644', u'\u062a\u0645\u0648',
             u'&#1489;&#1497;&#1493;&#1500;&#1497;', u'temm'],
    u'aug': [u'\u516b\u6708', u'srp', u'elo', u'kol', u'ago', u'a\u011fu', u'ao\u00fb', u'aws', u'sie', u'aout',
             u'\u0391\u03c5\u03b3', u'\u0430\u0432\u0433', u'\u0430\u0432\u0432', u'\u05d0\u05d5\u05d2',
             u'\u0623\u063a\u0633', u'\u0627\u063a\u0633', u'\u0391\u03cd\u03b3', u'\u0622\u0628',
             u'&#1489;&#1488;&#1493;&#1490;&#1493;&#1505;&#1496;', u'a\u0111u'],
    u'sep': [u'\u4e5d\u6708', u'z\u00e1\u0159', u'syy', u'ruj', u'set', u'eyl', u'med', u'wrz', u'\u0441\u0435\u043f',
             u'\u0441\u0435\u043d', u'sze', u'\u05e1\u05e4\u05d8', u'\u0633\u0628\u062a', u'\u03a3\u03b5\u03c0',
             u'\u0623\u064a\u0644', u'\u0627\u064a\u0644', u'&#1489;&#1505;&#1508;&#1496;&#1502;&#1489;&#1512;'],
    u'oct': [u'\u5341\u6708', u'\u0159\u00edj', u'lok', u'lis', u'okt', u'out', u'eki', u'hyd', u'ott', u'pa\u017a',
             u'\u043e\u043a\u0442', u'ott', u'\u05d0\u05d5\u05e7', u'\u0623\u0643\u062a', u'\u0627\u0643\u062a',
             u'\u039f\u03ba\u03c4\u03c9', u'&#1489;&#1488;&#1493;&#1511;&#1496;&#1493;&#1489;&#1512;'],
    u'nov': [u'\u5341\u4e00\u6708', u'\u0646\u0648\u0646', u'lis', u'stu', u'kas', u'tac', u'lis', u'neo',
             u'\u039d\u03bf\u03ad\u03bc', u'\u043d\u043e\u0435', u'\u043d\u043e\u044f', u'\u05e0\u05d5\u05d1',
             u'\u0646\u0648\u0641', u'\u039d\u03bf\u03b5', u'&#1489;&#1504;&#1493;&#1489;&#1502;&#1489;&#1512;'],
    u'dec': [u'\u5341\u4e8c\u6708', u'pro', u'jou', u'pro', u'dez', u'ara', u'd\u00e9c', u'rha', u'dic', u'gru',
             u'\u0434\u0435\u043a', u'dis', u'\u05d3\u05e6\u05de', u'\u062f\u064a\u0633', u'\u0394\u03b5\u03ba',
             u'&#1489;&#1491;&#1510;&#1502;&#1489;&#1512;', u'des'],
}

PRE_MONTHS_TRANSLATION = {
    "juin": "jun",
    "juil": "jul",
    u"\u010derven": "jun",
    u"\u010dervenec": "jul",
    u"\u0399\u03bf\u03c5\u03bd\u03af\u03bf\u03c5": "jun",
    u"\u0399\u03bf\u03c5\u03bb\u03af\u03bf\u03c5": "jul",
    "marssia": "mar",
    "marraskuuta": "nov",
    u"\u0643\u0627\u0646\u0648\u0646 \u0627\u0644\u062b\u0627\u0646\u064a": "jan",
    u"\u0643\u0627\u0646\u0648\u0646 \u0627\u0644\u0623\u0648\u0644": "dec",
    u"\u062a\u0634\u0631\u064a\u0646 \u0627\u0644\u0623\u0648\u0644": "oct",
    u"\u062a\u0634\u0631\u064a\u0646 \u0627\u0644\u062b\u0627\u0646\u064a": "nov",
    u"\u0643\u0627\u0646\u0648\u0646 \u062b\u0627\u0646\u064a": "jan",
    u"\u0643\u0627\u0646\u0648\u0646 \u0623\u0648\u0644": "dec",
    u"\u0643\u0627\u0646\u0648\u06462": "jan",
    u"\u0643\u0627\u0646\u0648\u06461": "dec",
    u"\u062a\u0634\u0631\u064a\u0646 \u0623\u0648\u0644": "oct",
    u"\u062a\u0634\u0631\u064a\u0646 \u062b\u0627\u0646\u064a": "nov",
    u"\u0623\u063a\u0633\u0637\u0633\u000a": "aug"
}
