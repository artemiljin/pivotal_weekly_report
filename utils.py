import os
from datetime import datetime
from datetime import timedelta

import jinja2
import requests

API_TOKEN = ''
SERVER = 'https://www.pivotaltracker.com'


def get_request(url, **kwargs):
    """
    Common HTTP GET request
    :param url: string basic part of request URL
    :return: MauiResponse object
    """
    params = kwargs.pop('params', None)
    custom_headers = kwargs.pop('headers', {})
    auth_headers = {'X-TrackerToken': f'{API_TOKEN}'}
    headers = {**custom_headers, **auth_headers}
    response = requests.get(url, headers=headers, params=params)
    return response.content


def week_range(current_date):
    """
    Find the first/last day of the week for the given day.
    Assuming weeks start on Monday and end on Sunday.
    Returns a tuple of ``(start_date, end_date) in iso format``.
    :param current_date: current date in datetime format
    :return: start/end date of the week you're interested in
    """
    assert isinstance(current_date, datetime), 'Date should be datetime instance'
    year, week, dow = current_date.isocalendar()

    if dow == 1:
        # Check if Monday
        start_date = current_date
    else:
        start_date = current_date - timedelta(dow)

    # add six days till Sunday
    end_date = start_date + timedelta(6)

    return start_date.isoformat(), end_date.isoformat()


def render(tpl_path, context):
    """
    Render the Jinja2 template
    :param tpl_path: path to the template
    :param context: context to render
    :return: something you can render
    """
    path, filename = os.path.split(tpl_path)
    return jinja2.Environment(
        loader=jinja2.FileSystemLoader(path or './')
    ).get_template(filename).render(context)
