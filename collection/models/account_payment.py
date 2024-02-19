
from lxml import etree
from odoo import api, fields, models


class account_payment(models.Model):
    _inherit = 'account.payment'

    collector_id = fields.Many2one(
        string='Collector',
        comodel_name='res.partner',
    )
    collection_id = fields.Many2one(
        comodel_name='collection.order',
        string='Collection Order',
    )
    transfer_collection_id = fields.Many2one(
        comodel_name='collection.order',
        string='Transfer Collection Order',
    )
    collection_line_id = fields.Many2one(
        comodel_name='collection.order.line',
        string='Collection Order Line',
    )
    document = fields.Binary(
        string='Document',
        attachment=True,
    )
    filename = fields.Char()

    @api.model
    def fields_view_get(self, view_id=None, view_type='form',
                        toolbar=False, submenu=False):
        res = super(account_payment, self).fields_view_get(
            view_id=view_id, view_type=view_type,
            toolbar=toolbar, submenu=False)
        if self._context.get('default_collector_id'):
            doc = etree.XML(res['arch'])
            if self._context['default_collector_id']:
                for node in doc.xpath("//field[@name='journal_id']"):
                    node.set('domain', "[('use_in_collections', '=', False)]")
            res['arch'] = etree.tostring(doc, encoding='unicode')
        return res

    def _get_liquidity_move_line_vals(self, amount):
        res = super(account_payment, self)._get_liquidity_move_line_vals(amount)
        if self.collector_id:
            res.update({'account_id': self.collector_id.property_account_receivable_id.id or
                                      self.collector_id.property_account_payable_id.id,
                        'partner_id': self.collector_id.id
                        })
        return res
