from odoo import models,api
from datetime import datetime

class product_product(models.Model):
    _inherit = "product.product"
    
    @api.multi
    def get_stock_ept(self,product_id,warehouse_id,fix_stock_type=False,fix_stock_value=0,stock_type='virtual_available'):
        product = self.with_context(warehouse=warehouse_id).browse(product_id.id)
        try:
            actual_stock = getattr(product, stock_type)
            if actual_stock >= 1.00:
                if fix_stock_type == 'fix':
                    if fix_stock_value >= actual_stock:
                        return actual_stock
                    else:
                        return fix_stock_value
    
                elif fix_stock_type == 'percentage':
                    quantity = int((actual_stock * fix_stock_value) / 100.0)
                    if quantity >= actual_stock:
                        return actual_stock
                    else:
                        return quantity
            return actual_stock
        except Exception as e:
            raise Warning(e)

    def get_products_based_on_movement_date(self, from_datetime, company=False):
        """
        This method is give the product list from selected date.
        @author: Haresh Mori @ Emipro on date 24/06/2020
        :param from_datetime:from this date it gets the product move list
        :param company:company id
        :return:Product List
        """
        date = str(datetime.strftime(from_datetime, '%Y-%m-%d %H:%M:%S'))
        if company:
            qry = """select product_id from stock_move where date >= '%s' and company_id = %d and
                             state in ('partially_available','assigned','done')""" % (date, company.id)
        else:
            qry = """select product_id from stock_move where date >= '%s' and
                                     state in ('partially_available','assigned','done')""" % date
        self._cr.execute(qry)
        return self._cr.dictfetchall()
