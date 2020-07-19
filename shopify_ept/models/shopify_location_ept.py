import time
from odoo import models, fields, api,_
from .. import shopify
from odoo.exceptions import UserError


class ShopifyLocationEpt(models.Model):
    _name = 'shopify.location.ept'
    _description = 'Shopify Stock Location'

    name = fields.Char('Name',
                       help="Give this location a short name to make it easy to identify. You’ll see this name in areas like orders and products.",
                       readonly="1")
    partner_id = fields.Many2one('res.partner', "Address", readonly="1")
    warehouse_id = fields.Many2one('stock.warehouse', "Warehouse")
    shopify_location_id = fields.Char('Shopify Location Id', readonly="1")
    instance_id = fields.Many2one('shopify.instance.ept', "Instance", readonly="1")
    legacy = fields.Boolean('Is Legacy Location',
                            help="Whether this is a fulfillment service location. If true, then the location is a fulfillment service location. If false, then the location was created by the merchant and isn't tied to a fulfillment service.",readonly="1")
    is_primary_location = fields.Boolean("Is Primary Location",readonly="1")
    stock_location_id = fields.Many2one('stock.location', "Stock Location")
    

    @api.constrains('warehouse_id')
    def _check_warehouse_id(self):
        shopify_locations = False
        shopify_instances = self.env['shopify.instance.ept'].search([('state','=','confirmed')])
        for shopify_instance in shopify_instances:
            shopify_locations = self.search([('instance_id','=',shopify_instance.id),('warehouse_id','=',self.warehouse_id.id)])
            if shopify_locations and len(shopify_locations) > 1:
                raise UserError(_("Warehouse must be unique!!!"))
    

    @api.multi
    def import_shopify_locations(self, instance):
        res_partner_obj = self.env['res.partner']
        instance.connect_in_shopify()
        try:
            locations = shopify.Location.find()
        except Exception as e:
            if e.response.code == 429 and e.response.msg == "Too Many Requests":
                time.sleep(5)
                locations = shopify.Location.find()
        shop = shopify.Shop.current()
        for location in locations:
            location = location.to_dict()
            vals = {}
            vals.update({'name': location.get('name')})
            vals.update({'shopify_location_id': location.get('id')})
            vals.update({'instance_id': instance.id})
            vals.update({'legacy': location.get('legacy')})
            address1 = location.get('address1')
            address2 = location.get('address2')
            city = location.get('city')
            country_name = location.get('country')
            country_code = location.get('country_code')
            phone = location.get('phone')
            province_name = location.get('province')
            province_code = location.get('province_code')
            zip = location.get('zip')
            state_id = self.env['res.country.state'].search(
                ['|', ('code', '=', province_code), ('name', '=', province_name)], limit=1)
            country_id = self.env['res.country'].search(
                ['|', ('code', '=', country_code), ('name', '=', country_name)], limit=1)
            domain = [('name','=',vals.get('name'))]
            partner_vals={}
            address1 and domain.append(('street', '=', address1))
            address1 and partner_vals.update({'street':address1})
            address2 and domain.append(('street2', '=', address2))
            address2 and partner_vals.update({'street2': address2})
            state_id and domain.append(('state_id', '=', state_id.id))
            state_id and partner_vals.update({'state_id': state_id.id})
            country_id and domain.append(('country_id', '=', country_id.id))
            country_id and partner_vals.update({'country_id': country_id.id})
            city and domain.append(('city','=',city))
            city and partner_vals.update({'city': city})
            phone and domain.append(('phone','=',phone))
            phone and partner_vals.update({'phone': phone})
            zip and domain.append(('zip','=',zip))
            zip and partner_vals.update({'zip': zip})
            partner = res_partner_obj.search(domain,limit=1)
            if partner:
                vals.update({'partner_id':partner.id})
            else:
                partner_vals.update({'name': vals.get('name')})
                partner=res_partner_obj.create(partner_vals)
                vals.update({'partner_id': partner.id})
            shopify_location = self.search([('shopify_location_id','=',location.get('id')),('instance_id','=',instance.id)])
            if shopify_location:
                shopify_location.write(vals)
            else:
                self.create(vals)
        shopify_primary_location=self.search([('is_primary_location','=',True),('instance_id','=',instance.id)],limit = 1)
        if shopify_primary_location:
            shopify_primary_location.write({'is_primary_location':False})
        # primary_location_id=shop and shop[0].to_dict().get('primary_location_id')
        primary_location_id = shop and shop.to_dict().get('primary_location_id')
        primary_location=primary_location_id and self.search([('shopify_location_id','=',primary_location_id),('instance_id','=',instance.id)]) or False
        if primary_location:
            vals={'is_primary_location':True}
            not primary_location.warehouse_id and vals.update({'warehouse_id':instance.warehouse_id.id,'stock_location_id':instance.warehouse_id.lot_stock_id.id})
            primary_location.write(vals)