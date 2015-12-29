#This file is part celery_flower module for Tryton.
#The COPYRIGHT file at the top level of this repository contains
#the full copyright notices and license terms.
from celery_tryton import TrytonTask
from celery import Celery
from trytond.pool import Pool
from trytond.transaction import Transaction
import os
import time

broker = 'amqp://%(user)s:%(password)s@%(host)s:%(port)s/%(vhost)s' % {
    'user': os.environ.get('CELERY_USER'),
    'password': os.environ.get('CELERY_PASSWORD'),
    'host': os.environ.get('CELERY_HOST'),
    'port': os.environ.get('CELERY_PORT'),
    'vhost': os.environ.get('CELERY_VHOST'),
    }

CELERY_RESULT_BACKEND = 'db+postgresql://tryton:tryton@localhost/try38celery'

celery = Celery('tests_tasks', backend=CELERY_RESULT_BACKEND, broker=broker)
celery.config_from_object('celeryconfig')

@celery.task(base=TrytonTask)
def generate_requests(user_id=None):
    """Purchase Generate Requests"""
    pool = Pool()
    User = pool.get('res.user')
    PurchaseRequest = pool.get('purchase.request')

    interval = 5
    time.sleep(interval)

    if not user_id:
        user,  = User.search([
                ('login', '=', 'admin'),
            ])
        user_id = user.id

    with Transaction().set_user(user_id), \
        Transaction().set_context(
            User.get_preferences(context_only=True)):
        PurchaseRequest.generate_requests()
