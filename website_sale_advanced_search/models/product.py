from odoo import api, fields, models, _
from odoo.tools import frozendict


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    keyword_search = fields.Text('Keyword Search')

    def store_keyword_search(self):
        product_obj = self.env['product.template']
        dict_val = frozendict(self.env.context)
        if dict_val.get('default_product_tmpl_id'):
            products = product_obj.search([('id', '=', dict_val.get('default_product_tmpl_id'))])
        else:
            products = product_obj.search([])
        for product in products:
            product.keyword_search = ''
            search_word = ''
            for attribute_line in product.attribute_line_ids:
                search_word += ' ' + attribute_line.attribute_id.name
                for values in attribute_line.value_ids:
                    search_word += ' ' + values.name
            product.keyword_search = search_word
