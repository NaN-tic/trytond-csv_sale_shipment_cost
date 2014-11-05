# This file is part of csv_sale_shipment_cost module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.pool import Pool, PoolMeta
from trytond.transaction import Transaction

__all__ = ['CSVArchive']
__metaclass__ = PoolMeta


class CSVArchive:
    __name__ = 'csv.archive'

    @classmethod
    def post_import(cls, profile, records):
        '''
        Sale post import add delivery - shipment cost line
        '''
        pool = Pool()
        Sale = pool.get('sale.sale')
        SaleLine = pool.get('sale.line')
        Product = pool.get('product.product')
        Currency = pool.get('currency.currency')
        Date = pool.get('ir.date')

        today = Date.today()

        super(CSVArchive, cls).post_import(profile, records)
        if profile.model.model == 'sale.sale':
            for record in records:
                sale = Sale(record)

                cost, currency_id = 0, None
                if sale.carrier:
                    party_context = {}
                    if sale.party.lang:
                        party_context['language'] = sale.party.lang.code

                    with Transaction().set_context(
                            sale._get_carrier_context()):
                        cost, currency_id = sale.carrier.get_sale_price()

                    if cost == 0:
                        continue

                    if (sale.currency and currency_id != sale.currency.id):
                        date = sale.sale_date or today
                        with Transaction().set_context(date=date):
                            cost = Currency.compute(Currency(currency_id),
                                cost, sale.currency)

                    product = sale.carrier.carrier_product
                    with Transaction().set_context(party_context):
                        description = Product(product.id).rec_name

                    #save delivery - shipment cost line
                    delivery_line = SaleLine()
                    delivery_line.sale = sale
                    delivery_line.product = product
                    delivery_line.quantity = 1
                    delivery_line.unit = product.default_uom
                    delivery_line.unit_price = cost
                    delivery_line.description = description
                    vals = delivery_line.on_change_product()

                    delivery_line.unit_price = cost
                    delivery_line.shipment_cost = cost
                    delivery_line.amount = cost
                    delivery_line.sequence = 9999

                    for k, v in vals.iteritems():
                        if not hasattr(delivery_line, k):
                            setattr(delivery_line, k, v)

                    delivery_line.save()