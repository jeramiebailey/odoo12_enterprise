from odoo import models,fields,api,_
from .. import shopify

class account_move_line(models.Model):
    _inherit="account.move.line"
    
    updated_in_shopify=fields.Boolean("Updated In Shopify",default=False)
    
class account_invoice(models.Model):
    _inherit="account.invoice"
    
    shopify_instance_id=fields.Many2one("shopify.instance.ept","Instances")
    is_refund_in_shopify=fields.Boolean("Refund In Shopify",default=False)
    source_invoice_id = fields.Many2one('account.invoice','Source Invoice')
    picking_id = fields.Many2one('stock.picking','Picking')
    
    @api.multi
    def refund_in_shopify(self):
        view=self.env.ref('shopify_ept.view_shopify_refund_wizard')
        context=dict(self._context)
        context.update({'active_model':'account.invoice','active_id':self.id,'active_ids':self.ids})
        return {
            'name': _('Refund order In Shopify'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'shopify.refund.wizard',
            'views': [(view.id, 'form')],
            'view_id': view.id,
            'target': 'new',
            'context': context
        }        
    @api.model
    def _prepare_refund(self, invoice, date_invoice=None, date=None, description=None, journal_id=None):
        
        val=super(account_invoice,self)._prepare_refund(invoice=invoice, date_invoice=date_invoice, date=date, description=description, journal_id=journal_id)
        invoice_id = self.env.context.get('active_id', False)
        if invoice.shopify_instance_id:
            val.update({'shopify_instance_id':invoice.shopify_instance_id.id,'source_invoice_id':invoice_id})
        return val
    
class sale_order(models.Model):
    _inherit="sale.order"
 
    def _prepare_invoice(self):    
        inv_val=super(sale_order,self)._prepare_invoice()        
        if self.shopify_instance_id:
            inv_val.update({'shopify_instance_id':self.shopify_instance_id.id})            
        return inv_val
 