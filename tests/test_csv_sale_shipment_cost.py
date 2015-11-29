# This file is part of the csv_sale_shipment_cost module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
import unittest
import trytond.tests.test_tryton
from trytond.tests.test_tryton import ModuleTestCase


class CSVSaleShipmentCostTestCase(ModuleTestCase):
    'Test CSV Sale Shipment Cost module'
    module = 'csv_sale_shipment_cost'


def suite():
    suite = trytond.tests.test_tryton.suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
        CSVSaleShipmentCostTestCase))
    return suite
