from odoo import api, fields, models
from datetime import datetime, timedelta
    
class product_template(models.Model):
    _inherit = "product.template"
    
    label_ept_id=fields.Many2one("product.label","Sale Label")
    product_brand_ept_id = fields.Many2one(
        'product.brand.ept',
        string='Brand',
        help='Select a brand for this product'
    )
    score = fields.Float(string="Product Score",default=1.0)

    def get_products_score(self):
        products = self.env['product.template'].search([("sale_ok", "=", True),("website_published", "=", True)])
        if products:
            website_rc = self.env['website'].search([], limit=1)
            today_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            before_30 = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d %H:%M:%S")
            for product in products:
                if product.rating_count:
                    temp = 0
                    zero_counter = 0
                    for rate in product.rating_ids:
                        if rate.rating != 0 and rate.website_published:
                            temp += rate.rating
                        else:
                            zero_counter += 1
                    if temp != 0 and zero_counter != 0:
                        avg_rate = temp / (product.rating_count - zero_counter)
                    else:
                        avg_rate = 0
                else:
                    avg_rate = 0
                so_lines = self.env['sale.order.line'].search([('product_id', 'in', product.product_variant_ids.ids), ('order_id.date_order', '>=', before_30),('order_id.date_order', '<=', today_date)])
                if so_lines:
                    temp = 0
                    for line in so_lines:
                        temp += line.product_uom_qty
                    avg_sale = temp
                else:
                    avg_sale = 0

                rules = self.env['product.rule'].sudo().search([('active','=',True)])
                if rules:
                    sale_score = 0
                    rating_score = 0
                    for rule in rules:
                        if rule.factor == 'sale_base':
                            if avg_sale >= rule.threshold:
                                sale_score = rule.threshold_amount
                        else:
                            if avg_rate >= rule.threshold:
                                rating_score = rule.threshold_amount

                    score = 1 if sale_score + rating_score == 0 else sale_score + rating_score
                    if product.product_brand_ept_id and product.product_brand_ept_id.brand_weight:
                        score = score + product.product_brand_ept_id.brand_weight
                    if product.score != score:
                        product.write({'score' : score})
