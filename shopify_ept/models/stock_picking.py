from odoo import models,fields,api,_

class stock_move(models.Model):
    _inherit="stock.move"
    
    
    def _get_new_picking_values(self):
        """We need this method to set Shopify Instance in Stock Picking"""
        res = super(stock_move,self)._get_new_picking_values()
        order_id=self.sale_line_id.order_id
        if order_id.shopify_order_id != False:
            order_id and res.update({'shopify_instance_id': order_id.shopify_instance_id.id,'is_shopify_delivery_order':True})
        return res 

class stock_picking(models.Model):
    _inherit="stock.picking"
    
#     @api.one
#     @api.depends("group_id")
#     def get_shopify_orders(self):
#         sale_obj=self.env['sale.order']
#         for record in self:
#             if record.group_id:
#                 sale_order=sale_obj.search([('procurement_group_id', '=', record.group_id.id)])
#                 if sale_order.shopify_order_id:
#                     record.is_shopify_delivery_order=True
#                     record.shopify_instance_id=sale_order.shopify_instance_id.id
#                 else:
#                     record.is_shopify_delivery_order=False
#                     record.shopify_instance_id=False
    updated_in_shopify=fields.Boolean("Updated In Shopify",default=False)
    is_shopify_delivery_order=fields.Boolean("Shopify Delivery Order",store=True)
    shopify_instance_id=fields.Many2one("shopify.instance.ept","Instance",store=True)
    #pack_operation_ids=fields.One2many('stock.pack.operation', 'picking_id', string='Related Packing Operations',states={'cancel': [('readonly', True)]})
    canceled_in_shopify=fields.Boolean("Canceled In Shopify",default=False)
    

    @api.multi
    def cancel_in_shopify(self):
        view=self.env.ref('shopify_ept.view_shopify_cancel_order_wizard')
        context=dict(self._context)
        context.update({'active_model':'stock.picking','active_id':self.id,'active_ids':self.ids})
        return {
            'name': _('Cancel Order In Shopify'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'shopify.cancel.order.wizard',
            'views': [(view.id, 'form')],
            'view_id': view.id,
            'target': 'new',
            'context': context
        }        
    
    @api.multi
    def mark_sent_shopify(self):
        for picking in self:
            picking.write({'updated_in_shopify':False})
        return True
    @api.multi
    def mark_not_sent_shopify(self):
        for picking in self:
            picking.write({'updated_in_shopify':True})
        return True
    
class delivery_carrier(models.Model):
    _inherit="delivery.carrier"
    
    shopify_code=fields.Char("Shopify Code")
    
class stock_inventory(models.Model):
    _inherit="stock.inventory"    
    
    is_shopify_product_adjustment=fields.Boolean("Shopify Product Adjustment?")