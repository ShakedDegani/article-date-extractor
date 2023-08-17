import re
from datetime import datetime, timedelta

import pytz
import requests
from dateparser import parse
from dateutil.parser import parse
from timeout_decorator import timeout

from logger import Logger

logger_handler = Logger(name="article_date_extractor_logger", path="/var/log/webhose/articleDateExtractor_logs",
                        level="DEBUG").get_logger()


def get_html_response(url):
    """
    simple request execution
    :param url: string of url
    :return: html response
    """
    try:
        return requests.get(url).text
    except Exception:
        return ""


def parse_date_by_daetutil(date_string):
    try:
        dateTimeObj = parse(date_string)
        return dateTimeObj
    except Exception as error:
        logger_handler.error(error)


def parse_date_by_dateparser(date_string):
    try:
        dateTimeObj = parse(date_string)
        return dateTimeObj
    except Exception as error:
        logger_handler.error(error)


@timeout(0.5)
def timed_parse(date_to_parse):
    return parse_date_by_daetutil(date_to_parse) or parse_date_by_dateparser(date_to_parse)


def parse_str_date(date_string):
    if date_string is not None:
        date_string = date_string.strip()
        if len(date_string) < 50 and re.search("\d+", date_string):
            try:
                return timed_parse(date_string)
            except Exception as error:
                logger_handler.error(error)


def filter_dates(dates):
    possible_dates = [date for date in dates if
                      timedelta(days=-1) < datetime.now() - date < timedelta(days=365)]
    possible_dates = [_date.replace(tzinfo=pytz.UTC) for _date in possible_dates]

    possible_dates_dict = {}
    possible_date_times = []
    for date in possible_dates:
        date_str = date.date().__str__()
        if date_str not in possible_dates_dict:
            possible_dates_dict[date_str] = []
        possible_dates_dict[date_str].append(date)

    for date_str, list_of_dates in possible_dates_dict.items():
        list_of_dates_with_times = []
        for index, temp_date in enumerate(list_of_dates):
            if temp_date.hour or temp_date.minute or index == len(list_of_dates) - 1:
                list_of_dates_with_times.append(temp_date)

        possible_date_times.extend(list_of_dates_with_times)

    return possible_date_times
