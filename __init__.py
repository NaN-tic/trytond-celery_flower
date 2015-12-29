# This file is part celery_flower module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.pool import Pool
from .celery_flower import *

def register():
    Pool.register(
        FlowerWorkers,
        FlowerTasks,
        module='celery_flower', type_='model')

