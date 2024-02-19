
from odoo import models, fields


class AccountInvoiceReport(models.Model):
    _inherit = "account.invoice.report"

    price_cost = fields.Float(
        string='Cost',
        readonly=True,
    )

    def _select(self):
        res = super()._select()
        res += """
            ,sub.price_cost as price_cost
            """
        return res

    def _sub_select(self):
        res = super()._sub_select()
        res += """
            , SUM(ail.quantity * cost.value_float) AS price_cost
            """
        return res

    def _from(self):
        res = super(AccountInvoiceReport, self)._from()
        res += """
                LEFT JOIN ir_property cost ON (cost.name='standard_price' AND 
                cost.res_id=CONCAT('product.product,',pr.id) AND 
                cost.company_id=ai.company_id)
              """
        return res