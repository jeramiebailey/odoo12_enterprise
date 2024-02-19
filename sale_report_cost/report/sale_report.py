from odoo import models, fields


class SaleReport(models.Model):
    _inherit = "sale.report"

    price_cost = fields.Float(
        string='Cost',
        readonly=True,
    )

    def _query(self, with_clause='', fields={}, groupby='', from_clause=''):
        fields['price_cost'] = \
            ", SUM(l.product_uom_qty * cost.value_float) AS price_cost"
        from_clause +=  """
                LEFT JOIN ir_property cost ON (cost.name='standard_price' AND 
                cost.res_id=CONCAT('product.product,',p.id) AND 
                cost.company_id=s.company_id)
              """
        return super(SaleReport, self)._query(
            with_clause, fields, groupby, from_clause
        )
