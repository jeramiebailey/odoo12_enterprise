from odoo import fields, models, api, _


class pos_config(models.Model):
    _inherit = 'pos.config'

    pos_import = fields.Selection(selection=[], string='POS Import')
    pos_workflow = fields.Selection(selection=[('pos.order', 'Create POS Order')],
                                    string='POS Workflow', required=True, default='pos.order')
    use_pos_product_tax = fields.Boolean('Use POS Product Tax',
                                         help=('Use POS product taxes field instead'
                                               ' of the default product taxes'))
    display_pos_price_total = fields.Boolean('Include Tax in Price Display',
                                             help=('Include Tax in Price Display is only applicable'
                                                   ' for Taxes with enabled Included in Price'))
    keep_pos_with_workflow = fields.Boolean('POS With Workflow')

    @api.onchange('keep_pos_with_workflow','pos_workflow')
    def onchange_pos_workflow(self):
        if self.pos_workflow=='pos.order' and self.keep_pos_with_workflow:
            self.keep_pos_with_workflow = False
