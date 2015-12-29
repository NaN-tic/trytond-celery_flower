# This file is part of the celery_flower module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
import unittest
import trytond.tests.test_tryton
from trytond.tests.test_tryton import ModuleTestCase


class CeleryFlowerTestCase(ModuleTestCase):
    'Test Celery Flower module'
    module = 'celery_flower'


def suite():
    suite = trytond.tests.test_tryton.suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
        CeleryFlowerTestCase))
    return suite
