__author__ = 'Ran Geva'

import json
import re
from datetime import datetime

import pytz
from datefinder import find_dates
from webhose_metrics import count as metrics_count

import consts
import utils
from logger import Logger

logger_handler = Logger(name="article_date_extractor_logger", path="/var/log/webhose/articleDateExtractor_logs",
                        level="DEBUG").get_logger()

try:
    from bs4 import BeautifulSoup, Tag
except ImportError:
    from BeautifulSoup import BeautifulSoup, Tag


def extract_from_url(url):
    # Regex by Newspaper  - https://github.com/codelucas/newspaper/blob/master/newspaper/urls.py
    dates = []
    for pattern in consts.URL_REGEXPS:
        date_match = re.search(pattern, url)
        if date_match:
            temp_date = utils.parse_str_date(date_match.group(0))
            if temp_date:
                dates.append(temp_date)

    return dates


def _extract_by_tag(tag, parsed_html, attr):
    for tag_span in parsed_html.find_all(tag, **{attr: re.compile(consts.DATETIME_TAG_REGEX, re.IGNORECASE)}):
        return utils.parse_str_date(tag_span.string or tag_span.text)


def extract_from_ld_json(parsed_html):
    dates = []
    try:
        scripts = parsed_html.findAll('script', attrs={"type": 'application/ld+json'})
        if scripts is None:
            return dates

        for script in scripts:

            script_data = {}
            if any([script.text, script.string]):
                script_data = json.loads(script.text or script.string)
            if isinstance(script_data, dict):
                script_data = [script_data]

            for data in script_data:
                json_date = utils.parse_str_date(data.get('dateCreated', None)) or utils.parse_str_date(
                    data.get('datePublished', None))
                if json_date:
                    return [json_date]
    except Exception as error:
        logger_handler.error(error)

    return dates


def extract_from_meta(parsed_html):
    meta_dates = set()
    image_dates = []

    metas = [meta for meta in parsed_html.findAll("meta")]
    for meta in metas:
        meta_name, meta_prop, meta_equiv, meta_property, meta_content = tuple([
            (meta.get(attr) or "").lower().strip() for attr in consts.META_ATTRS
        ])

        if any([meta_name in consts.META_NAMES, meta_prop in consts.META_PROPS, meta_equiv in consts.META_EQUIVS,
                meta_property in consts.META_PROPS]):
            meta_dates.add(meta_content)

        # get date from main image url
        if 'og:image' == meta_property or "image" == meta_prop:
            url = meta['content'].strip()
            image_dates = extract_from_url(url)

    if meta_dates:
        return [utils.parse_str_date(date) for date in meta_dates] + image_dates
    return []


def extract_from_html_tag(parsed_html):
    list_of_times_attribute = parsed_html.findAll("time")
    # <time>
    for time in list_of_times_attribute:
        date_time = time.get('datetime', '')
        if len(date_time) > 0:
            return [utils.parse_str_date(date_time)]

        date_time = time.get('class', '')
        if len(date_time) > 0:
            date_string = time.string or time.text
            return [utils.parse_str_date(date_string)]

    tag = parsed_html.find("span", {"itemprop": "datePublished"})
    if tag is not None:
        date_text = tag.get("content") or tag.text
        if date_text is not None:
            return [utils.parse_str_date(date_text)]

    for attr, tags in consts.TAGS_ATTRS.items():
        possible_date = _extract_by_tag(tags, parsed_html, attr=attr)
        if possible_date:
            return [possible_date]

    return []


# To be developed in python 3.
def extract_from_title_area(html, char_range=250):
    """
    Find the date bellow the title, can be improved by clean the html.
    :param html: string
    :param char_range: how many chars to search the date in.
    :return: list of datetimes
    """
    dates = []
    try:
        tags = ["h1", "h2", "h3"]
        for tag in tags:
            pattern = u'<{tag}[^>]?>.*?</{tag}>(.*)'.format(tag=tag)
            tag_match = re.search(pattern, html, re.DOTALL)
            if tag_match:
                html_below = tag_match.group(1).strip()
                html_for_scan = re.sub(consts.SCRIPT_CLEANER, "", html_below)
                html_for_scan = re.sub(consts.HTML_CLEANER, "", html_for_scan)
                html_for_scan = re.sub("\s+", " ", html_for_scan, flags=re.DOTALL)[:min(len(html_for_scan), char_range)]
                matches = find_dates(html_for_scan, source=True)
                matches = [match for match in matches]
                if matches:
                    dates.extend(matches)
                    break
    except Exception as error:
        logger_handler.error(error)

    return dates


def extractArticlePublishedDate(article_link, html=None):
    article_date = None
    try:
        article_date = extract_from_url(article_link)
        if html is None:
            html = utils.get_html_response(article_link)

        parsed_html = BeautifulSoup(html, "lxml")

        possible_date = extract_from_ld_json(parsed_html)
        if possible_date is None:
            possible_date = extract_from_meta(parsed_html)
        if possible_date is None:
            possible_date = extract_from_html_tag(parsed_html)
        article_date = possible_date
    except Exception as error:
        logger_handler.error(error)

    return article_date


def get_relevant_date(url, html=None):
    """
    retrieves the most relevant published date for an article
    :param url: string of url
    :param html: string of html response (to avoid request execution)
    :return: the oldest date from the following options:
        1) date in the url
        2) headers of the response (json-ld, meta, etc.)
        3) html known tags
        4) 200 chars above title - 1000 chars bellow the title (on not clean html)
        Note: we currently filter out 1d < date < 1Y dates.
    """
    # getting date by input url
    url_base_dates = extract_from_url(url)
    # bs parsing for extended data
    html = html or utils.get_html_response(url)
    parsed_html = BeautifulSoup(html, "lxml")

    # extended dates (json-ld, html tags, etc.)
    jsonld_base_dates = extract_from_ld_json(parsed_html)
    meta_base_dates = extract_from_meta(parsed_html)
    html_tags_base_dates = extract_from_html_tag(parsed_html)

    possible_dates = [date for date_list in [url_base_dates, jsonld_base_dates, meta_base_dates, html_tags_base_dates] for date in date_list]
    possible_dates = filter(lambda _date: _date is not None and isinstance(_date, datetime), possible_dates)
    possible_dates = [_date.replace(tzinfo=pytz.UTC) for _date in possible_dates]
    # Add this row in python 3
    # if not possible_dates:
    #     possible_dates.extend(extract_from_title_area(html))

    possible_date_times = utils.filter_dates(possible_dates)

    metrics_count(name=consts.SUCCESS if possible_date_times else consts.FAILED)
    if len(possible_date_times) == 0:
        logger_handler.info("[get_relevant_date] - None possible dates for {url}".format(url=url))
        return None

    # return oldest date
    return min(possible_date_times)
