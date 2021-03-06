# Copyright © 2019 Province of British Columbia
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""CORS pre-flight decorator.

A simple decorator to add the options method to a Request Class.
"""
import calendar
from datetime import datetime, timedelta
from typing import Dict

from dpath import util as dpath_util
from flask import current_app


def cors_preflight(methods: str = 'GET'):
    """Render an option method on the class."""
    def wrapper(f):
        def options(self, *args, **kwargs):  # pylint: disable=unused-argument
            return {'Allow': methods}, 200, \
                   {'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': methods,
                    'Access-Control-Allow-Headers': 'Authorization, Content-Type, registries-trace-id'}

        setattr(f, 'options', options)
        return f

    return wrapper


def is_valid_redirect_url(url: str) -> bool:
    """Validate if the url is valid based on the VALID Redirect Url."""
    valid_urls: list = current_app.config.get('VALID_REDIRECT_URLS')
    is_valid = False
    for valid_url in valid_urls:
        is_valid = url.startswith(valid_url[:-1]) if valid_url.endswith('*') else valid_url == url
        if is_valid:
            break
    return is_valid


def convert_to_bool(value: str) -> bool:
    """Convert string to boolean."""
    return value.lower() == 'true'


def get_str_by_path(payload: Dict, path: str) -> str:
    """Return the string value from the dict for the path using dpath library."""
    try:
        raw = dpath_util.get(payload, path)
        return str(raw)
    except (IndexError, KeyError, TypeError):
        return None


def get_week_start_and_end_date(index: int = 0):
    """Return first and last dates (monday and sunday) for the index."""
    # index: 0 (current week), 1 (last week) and so on
    current_date = datetime.now() - timedelta(days=index * 6)
    start = current_date - timedelta(days=current_date.weekday())
    end = start + timedelta(days=6)
    return start, end


def get_first_and_last_dates_of_month(month: int, year: int):
    """Return first and last dates for a given month and year."""
    start_date = datetime.now().replace(day=1, year=year, month=month)
    end_date = start_date.replace(day=calendar.monthrange(year=year, month=month)[1])
    return start_date, end_date
