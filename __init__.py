# This file is part of csv_sale_shipment_cost module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.pool import Pool
from .csv_import import *


def register():
    Pool.register(
        CSVArchive,
        module='csv_sale_shipment_cost', type_='model')
