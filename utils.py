# This file is part celery_flower module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
import requests
from datetime import datetime, timedelta
from trytond.config import config as config_, parse_uri
from trytond.exceptions import UserError, UserWarning

FLOWER_URI = parse_uri(config_.get('celery', 'flower', default='http://localhost:5555'))

if FLOWER_URI.port:
    API_URI = '%s://%s:%s/api' % (FLOWER_URI.scheme, FLOWER_URI.hostname, FLOWER_URI.port)
else:
    API_URI = '%s://%s/api' % (FLOWER_URI.scheme, FLOWER_URI.hostname)

# Flower API URI's
WORKERS_API = '{}/workers'.format(API_URI)
TASKS_API = '{}/tasks'.format(API_URI)
TASK_API = '{}/task'.format(API_URI)


def flower_response(uri):
    'Flower Request API'
    try:
        if FLOWER_URI.username:
            resp = requests.get(uri, auth=requests.auth.HTTPBasicAuth(
                    FLOWER_URI.username, FLOWER_URI.password))
        else:
            resp = requests.get(uri)
    except requests.exceptions.HTTPError as e:
        raise UserError('Http Rrror', str(e.message))
    except requests.exceptions.ConnectionError as e:
        raise UserError('Connection Error', str(e.message))
    except requests.exceptions.SSLError as e:
        raise UserError('SSL Error', str(e.message))
    except:
        raise UserError('Flower Error', 'Unknown Error')

    if resp.status_code == 200:
        return resp.json()
    return 

def flower_hour(hour, timezone):
    'Convert hour to timezone'
    # TODO: Flower show -1 hour respect to UTC.
    # To fix, sum an hour respect to tz
    return datetime.fromtimestamp(hour, tz=timezone) + timedelta(hours=1)

def flower_json_hour(dt):
    'Convert datetime to JSON hour'
    # TODO: Flower show -1 hour respect to UTC.
    # To fix, rest an hour respect to tz
    new_dt = dt + timedelta(hours=-1)
    return new_dt.strftime('%Y-%m-%d %H:%M')

def search_not_like(value):
    'Remove % characters from like'
    if value[:1] == '%':
        value = value[1:]
    if value[-1:] == '%':
        value = value[:-1]
    return value
