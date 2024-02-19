from odoo import models, api


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    @api.one
    def _get_product_header(self):
        self.ensure_one()
        item_vals = []
        for item in self.attribute_line_ids:
            item_vals.append({
                'attr_id': item.attribute_id,
                'value_ids': len(item.value_ids),
                'value_item_ids': item.value_ids

            })
        item_min = min(item_vals, key=lambda k: k['value_ids'])
        table_header = item_min.get('value_item_ids')
        table_footer = []
        for line in self.attribute_line_ids.filtered(lambda o: o.attribute_id != item_min.get('attr_id').id)[
            0].value_ids:
            table_footer.append({
                'line_footer': line,
                'input_ids': table_header
            })
        table_struct = {'table_header': table_header, 'table_footer': table_footer}
        return table_struct


ProductTemplate()
