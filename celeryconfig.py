#This file is part mifarma module for Tryton.
#The COPYRIGHT file at the top level of this repository contains
#the full copyright notices and license terms.
import os

TRYTON_DATABASE = os.environ.get('TRYTON_DATABASE')
TRYTON_CONFIG = os.environ.get('TRYTON_CONFIG')

# Enable this options to debug. More info in celery page.
CELERY_ALWAYS_EAGER = False
CELERY_EAGER_PROPAGATES_EXCEPTIONS = False
CELERY_ENABLE_UTC = True
CELERY_TIMEZONE = 'UTC'
CELERY_TASK_TIME_LIMIT = 7200
CELERY_SOFT_TASK_TIME_LIMIT =  7200
CELERY_MAX_TASKS_PER_CHILD  = 2
CELERY_ACCEPT_CONTENT = ['json']
