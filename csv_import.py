# This file is part of csv_sale_shipment_cost module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.pool import Pool, PoolMeta

__all__ = ['CSVArchive']
__metaclass__ = PoolMeta


class CSVArchive:
    __name__ = 'csv.archive'

    @classmethod
    def post_import(cls, profile, records):
        '''
        Sale post import add delivery - shipment cost line
        '''
        Sale = Pool().get('sale.sale')

        super(CSVArchive, cls).post_import(profile, records)
        if profile.model.model == 'sale.sale':
            to_write = []
            for record in records:
                sale = Sale(record)
                sale.set_shipment_cost()
                to_write.append(sale)
            if to_write:
                Sale.save(to_write)
