from odoo import fields, models, api, _
import logging
LOGGER = logging.getLogger(__name__)

class Stock_PickingInherit_test(models.Model):
    _inherit = 'stock.picking'

    picking_type_id_code = fields.Selection(related="picking_type_id.code")
    is_manual_return = fields.Boolean(string="Manual Return",  )

    def make_create_credit_note(self):
        LOGGER.info("make_create_credit_note")
        lines = []
        for line in self.move_ids_without_package:
            lines.append(
                (0, 0, {
                    'category_id': line.product_id.categ_id.id,
                    'product_id': line.product_id.id,
                    'name': line.product_id.name,
                    'price_unit': line.product_id.lst_price,
                    # 'discount': line.product_id.basic_discount,
                    'account_id':line.product_id.categ_id.property_account_income_categ_id.id,
                    'quantity':line.quantity_done,
                }))
        LOGGER.info("lines:: %s",lines)
        res_id = self.env['account.invoice'].create({
            'type': 'out_refund',
            'partner_id': self.partner_id.id,
            'state': 'draft',
            'invoice_line_ids': lines
        })

        return {'name': (
                            'Credit Note'),
                        'type': 'ir.actions.act_window',
                        'res_model': 'account.invoice',
                        'res_id': res_id.id,
                        'view_type': 'form',
                        'view_mode': 'form',
                    }

    def make_create_refund(self):
        LOGGER.info("make_create_credit_note")
        lines = []
        for line in self.move_ids_without_package:
            lines.append(
                (0, 0, {
                    'category_id': line.product_id.categ_id.id,
                    'product_id': line.product_id.id,
                    'name': line.product_id.name,
                    'price_unit': line.product_id.lst_price,
                    # 'discount': line.product_id.basic_discount,
                    'account_id':line.product_id.categ_id.property_account_income_categ_id.id,
                    'quantity': line.quantity_done,

                }))
        LOGGER.info("lines:: %s",lines)
        res_id = self.env['account.invoice'].create({
            'type': 'in_refund',
            'partner_id': self.partner_id.id,
            'state': 'draft',
            'invoice_line_ids': lines
        })

        return {'name': (
                            'Credit Note'),
                        'type': 'ir.actions.act_window',
                        'res_model': 'account.invoice',
                        'res_id': res_id.id,
                        'view_type': 'form',
                        'view_mode': 'form',
                    }