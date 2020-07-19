from odoo import models, fields, api, _
from odoo.exceptions import Warning
import hashlib
from _datetime import datetime
from datetime import datetime, timedelta
import math, pytz
import logging
_logger = logging.getLogger('shopify_process===(Emipro)===')

class shopify_process_import_export(models.TransientModel):
    _name = 'shopify.process.import.export'
    _description = 'Shopify Process Import Export'

    instance_ids = fields.Many2many("shopify.instance.ept", 'shopify_instance_import_export_rel',
                                    'process_id', 'shopify_instance_id', "Instances")
    update_price_in_product = fields.Boolean("Set Price", default=False)
    update_stock_in_product = fields.Boolean("Set Stock", default=False)
    publish = fields.Boolean("Publish In Website", default=False)
    publish_collection = fields.Boolean("Publish Collection In Website", default=False)
    is_import_orders = fields.Boolean("Import Orders")
    is_export_products = fields.Boolean("Export Products")
    is_update_products = fields.Boolean("Update Products")
    is_publish_products = fields.Boolean("Publish Products")
    is_publish_collection = fields.Boolean("Publish Collection")
    is_export_collection = fields.Boolean("Export Collection")
    is_update_collection = fields.Boolean("Update Collection")
    is_update_stock = fields.Boolean("Update Stock")
    is_update_price = fields.Boolean("Update Price")
    is_update_images = fields.Boolean("Update Images")
    sync_product_from_shopify = fields.Boolean("Sync Products")
    is_import_collection = fields.Boolean("Import Collection")
    is_update_order_status = fields.Boolean("Update Order Status")
    sync_images_with_product = fields.Boolean("Sync Images?",
                                              help="Check if you want to import images along with products",
                                              default=False)
    sync_price_with_product = fields.Boolean("Sync Product Price?",
                                             help="Check if you want to import price along with products",
                                             default=False)
    is_import_customer = fields.Boolean("Import Customers")
    is_import_stock = fields.Boolean("Import Stock")
    is_set_image = fields.Boolean(string="Set Images", default=False)
    is_import_location = fields.Boolean("Import Locations")
    orders_from_date = fields.Datetime(string="From")
    orders_to_date = fields.Datetime(string="To")
    export_stock_from = fields.Datetime(help="It is used for exporting stock from Odoo to shopify.")

    # Add by Haresh mori on date 18/05/2019 This is use for while sync products from odoo.sh server
    is_skip_sync_existing_shopify_product = fields.Boolean(string="Skip Existing Product?",
                                                           help="Do You Want Skip Existing Product Imported From Shopify?")

    @api.onchange("sync_product_from_shopify")
    def onchange_sync_product(self):
        for record in self:
            if not record.sync_product_from_shopify:
                record.is_skip_sync_existing_shopify_product = False

    @api.model
    def default_get(self, fields):
        res = super(shopify_process_import_export, self).default_get(fields)
        if 'default_instance_id' in self._context:
            res.update({'instance_ids': [(6, 0, [self._context.get('default_instance_id')])]})
            shopify_instance = self._context.get('default_instance_id')
            shopify_instance = self.env['shopify.instance.ept'].search(
                [('id', '=', shopify_instance)], limit=1)
            to_date = datetime.now()
            from_date = shopify_instance.last_date_order_import
            export_stock_from = shopify_instance.shopify_last_date_update_stock or datetime.now() - timedelta(30)
            res.update({'orders_from_date': from_date, 'orders_to_date': to_date,
                        'export_stock_from':export_stock_from})
        elif 'instance_ids' in fields:
            instance_ids = self.env['shopify.instance.ept'].search([('state', '=', 'confirmed')])
            res.update({'instance_ids': [(6, 0, instance_ids.ids)]})
            to_date = datetime.now()
            from_date = instance_ids and instance_ids[0].last_date_order_import
            export_stock_from = instance_ids and instance_ids[0].shopify_last_date_update_stock or datetime.now() - timedelta(30)
            if instance_ids:
                res.update({'orders_from_date': str(from_date), 'orders_to_date': to_date,'export_stock_from':export_stock_from})
        return res

    @api.multi
    def execute(self):
        if self.is_import_orders:
            self.import_export_processes()
        if self.is_import_customer:
            self.import_customer()
        if self.sync_product_from_shopify:
            self.sync_products()
        if self.is_import_collection:
            self.import_collection()
        if self.is_export_products:
            self.export_products()
        if self.is_update_products:
            self.update_products()
        if self.is_update_price:
            self.update_price()
        if self.is_update_stock:
            self.update_stock_in_shopify()
        if self.is_export_collection:
            self.export_collection()
        if self.is_update_collection:
            self.update_collection()
        if self.is_update_order_status:
            self.update_order_status()
        if self.is_publish_products:
            self.publish_multiple_products()
        if self.is_publish_collection:
            self.publish_multiple_collection()
        if self.is_import_stock:
            self.import_stock()
        if self.is_update_images:
            self.update_product_images()
        if self.is_import_location:
            self.import_location()
        return True

    @api.multi
    def import_export_processes(self):
        sale_order_obj = self.env['sale.order']
        for instance in self.instance_ids:
            from_date = self.orders_from_date
            to_date = self.orders_to_date
            # current_date = datetime.strptime(
            #     datetime.now(pytz.timezone(self.env.user.tz)).strftime("%Y-%m-%d %H:%M-%S"),
            #     "%Y-%m-%d %H:%M-%S")
            # from_date, to_date = self.convert_date_into_users_timezone(from_date, to_date)
            # if to_date > current_date:
            #     raise Warning(_(
            #         "Date and Time should not be greater then current Date and Time"))
            if from_date > to_date:
                raise Warning(
                    _("From date should not be greater then To date"))
            instance.write({'last_date_order_import': to_date})
            sale_order_obj.import_shopify_orders(from_date, to_date, instance)
        return True

    @api.multi
    def convert_date_into_users_timezone(self, from_date, to_date):
        user_time_zone_offset = self.env.user.tz_offset
        timezone_operator = user_time_zone_offset[0]
        timezone_offset = int(user_time_zone_offset.split("+")[-1])
        timezone_minutes = 0
        timezone_hours = 0
        if timezone_offset == 0:
            pass
        elif math.floor(math.log10(timezone_offset)) + 1 == 1:
            timezone_minutes = timezone_offset
        elif math.floor(math.log10(timezone_offset)) + 1 == 2:
            timezone_minutes = timezone_offset
        elif math.floor(math.log10(timezone_offset)) + 1 == 3:
            timezone_hours = int(str(timezone_offset)[0])
            timezone_minutes = int(str(timezone_offset)[1:])
        elif math.floor(math.log10(timezone_offset)) + 1 == 4:
            if str(timezone_offset).endswith("00"):
                timezone_hours = int(str(timezone_offset)[0:2])
            else:
                timezone_hours = int(str(timezone_offset)[0:2])
                timezone_minutes = int(str(timezone_offset)[2:])

        if timezone_operator == '+':
            from_date += timedelta(hours=timezone_hours, minutes=timezone_minutes)
            to_date += timedelta(hours=timezone_hours, minutes=timezone_minutes)
        elif timezone_operator == '-':
            from_date -= timedelta(hours=timezone_hours, minutes=timezone_minutes)
            to_date -= timedelta(hours=timezone_hours, minutes=timezone_minutes)
        return from_date, to_date

    @api.multi
    def import_stock(self):
        shopify_product_tmpl_obj = self.env['shopify.product.template.ept']
        for instance in self.instance_ids:
            shopify_product_tmpl_obj.import_stock(instance)
        return True

    @api.multi
    def import_customer(self):
        res_partner_obj = self.env['res.partner']
        for instance in self.instance_ids:
            res_partner_obj.import_shopify_customers(instance)
        return True

    @api.multi
    def import_location(self):
        shopify_location_obj = self.env['shopify.location.ept']
        for instance in self.instance_ids:
            shopify_location_obj.import_shopify_locations(instance)
        return True

    @api.multi
    def update_order_status(self):
        sale_order_obj = self.env['sale.order']
        for instance in self.instance_ids:
            sale_order_obj.update_order_status(instance)
        return True

    @api.multi
    def update_stock_in_shopify(self):
        shopify_product_tmpl_obj = self.env['shopify.product.template.ept']
        product_obj = self.env['product.product']
        if self._context.get('process') == 'update_stock':
            product_tmpl_ids = self._context.get('active_ids')
            if product_tmpl_ids and len(product_tmpl_ids) > 80:
                raise Warning("Error:\n- System will not export stock more then 80 Products at a "
                              "time.\n- Please select only 80 product for export stock.")
            instances = self.env['shopify.instance.ept'].search([])
        else:
            product_tmpl_ids = []
            instances = self.instance_ids
        shopify_templates = False
        for instance in instances:
            if product_tmpl_ids:
                shopify_templates = shopify_product_tmpl_obj.search(
                    [('shopify_instance_id', '=', instance.id), ('id', 'in', product_tmpl_ids)])
                _logger.info(
                    "Exporting Stock by seleted products from shopify layer for instance - %s..." % (instance.name))
            else:
                _logger.info(
                    "Exporting Stock from Operations wizard for instance - %s.....It will take "
                    "those products which stock movement has done after this date (%s)" % (instance.name,self.export_stock_from))
                odoo_products = product_obj.get_products_based_on_movement_date(self.export_stock_from,
                                                                           instance.company_id)
                if odoo_products:
                    product_id_array = sorted(list(map(lambda x:x['product_id'], odoo_products)))
                    shopify_products = self.env['shopify.product.product.ept'].search(
                            [('shopify_instance_id', '=', instance.id),
                             ('exported_in_shopify', '=', True),
                             ('product_id', 'in', product_id_array)])
                    shopify_templates = shopify_products.mapped('shopify_template_id')
                else:
                    _logger.info("No products to export stock....for instance %s "%(instance.name))

            shopify_templates and shopify_product_tmpl_obj.update_stock_in_shopify(instance,shopify_templates)
        return True

    @api.multi
    def update_price(self):
        shopify_product_tmpl_obj = self.env['shopify.product.template.ept']
        if self._context.get('process') == 'update_price':
            product_tmpl_ids = self._context.get('active_ids')
            instances = self.env['shopify.instance.ept'].search([])
        else:
            product_tmpl_ids = []
            instances = self.instance_ids
        for instance in instances:
            if product_tmpl_ids:
                products = shopify_product_tmpl_obj.search(
                    [('shopify_instance_id', '=', instance.id), ('id', 'in', product_tmpl_ids)])
            else:
                products = shopify_product_tmpl_obj.search(
                    [('shopify_instance_id', '=', instance.id), ('exported_in_shopify', '=', True)])
            products and shopify_product_tmpl_obj.update_price_in_shopify(instance, products)
        return True

    @api.multi
    def check_products(self, products):
        if self.env['shopify.product.product.ept'].search(
                [('shopify_template_id', 'in', products.ids), ('default_code', '=', False)]):
            raise Warning("Default code is not set in some variants")
        return True

    @api.multi
    def filter_templates(self, products):
        filter_templates = []
        for template in products:
            if not self.env['shopify.product.product.ept'].search(
                    [('shopify_template_id', '=', template.id), ('default_code', '=', False)]):
                filter_templates.append(template)
        return filter_templates

    @api.multi
    def export_products(self):
        shopify_product_tmpl_obj = self.env['shopify.product.template.ept']
        instance_settings = {}
        config_settings = {}
        if self._context.get('process') == 'export_products':
            product_ids = self._context.get('active_ids')
            instances = self.env['shopify.instance.ept'].search([])
        else:
            product_ids = []
            instances = self.instance_ids
            for instance in instances:
                instance_settings.update({"instance_id": instance})
                if instance.is_set_price:
                    config_settings.update({"is_set_price": True})
                if instance.is_set_stock:
                    config_settings.update({"is_set_stock": True})
                if instance.is_set_image:
                    config_settings.update({"is_set_image": True})
                if instance.is_publish:
                    config_settings.update({"is_publish": True})
                instance_settings.update({"settings": config_settings})
        for instance in instances:
            if instance_settings:
                setting = instance_settings.get('settings')
                is_set_price = setting.get('is_set_price')
                is_set_stock = setting.get('is_set_stock')
                is_set_image = setting.get('is_set_image')
                is_publish = setting.get('is_publish')
            else:
                is_set_price = self.update_price_in_product
                is_set_stock = self.update_stock_in_product
                is_set_image = self.is_set_image
                is_publish = self.publish
            if product_ids:
                products = shopify_product_tmpl_obj.search(
                    [('shopify_instance_id', '=', instance.id), ('id', 'in', product_ids),
                     ('exported_in_shopify', '=', False)])
                products = self.filter_templates(products)
            else:
                products = shopify_product_tmpl_obj.search(
                    [('shopify_instance_id', '=', instance.id),
                     ('exported_in_shopify', '=', False)])
                self.check_products(products)
            products and shopify_product_tmpl_obj.export_products_in_shopify(instance, products,
                                                                             is_set_price,
                                                                             is_set_stock,
                                                                             is_publish,
                                                                             is_set_image)
        return True

    @api.multi
    def update_products(self):
        shopify_product_tmpl_obj = self.env['shopify.product.template.ept']
        if self._context.get('process') == 'update_products':
            product_ids = self._context.get('active_ids')
            instances = self.env['shopify.instance.ept'].search([])
        else:
            instances = self.instance_ids
            product_ids = []

        for instance in instances:
            if product_ids:
                products = shopify_product_tmpl_obj.search(
                    [('shopify_instance_id', '=', instance.id), ('id', 'in', product_ids),
                     ('exported_in_shopify', '=', True)])
            else:
                products = shopify_product_tmpl_obj.search(
                    [('shopify_instance_id', '=', instance.id), ('exported_in_shopify', '=', True)])
            products and shopify_product_tmpl_obj.update_products_in_shopify(instance, products)
        return True

    @api.multi
    def update_product_images(self):
        shopify_product_tmpl_obj = self.env['shopify.product.template.ept']

        if self._context.get('process') == 'update_images':
            product_ids = self._context.get('active_ids')
            instances = self.env['shopify.instance.ept'].search([])
        else:
            product_ids = []
            instances = self.instance_ids
        for instance in instances:
            if product_ids:
                products = shopify_product_tmpl_obj.search(
                    [('shopify_instance_id', '=', instance.id), ('id', 'in', product_ids),
                     ('exported_in_shopify', '=', True)])
            else:
                products = shopify_product_tmpl_obj.search(
                    [('shopify_instance_id', '=', instance.id), ('exported_in_shopify', '=', True)])
            for product in products:
                shopify_product_tmpl_obj.update_product_images(instance, shopify_template=product)
        return True

    @api.multi
    def update_payment(self):
        account_invoice_obj = self.env['account.invoice']
        invoices = self.invoice_ids
        sale_order_ids = []
        for invoice in invoices:
            sale_order_ids += invoice.sale_ids.ids
        account_invoice_obj.update_payment(sale_order_ids, invoices.ids)
        return True

    @api.multi
    def prepare_product_for_export(self):
        shopify_template_obj = self.env['shopify.product.template.ept']
        shopify_product_obj = self.env['shopify.product.product.ept']
        shopify_product_image_obj = self.env['shopify.product.image.ept']
        active_template_ids = self._context.get('active_ids', [])
        template_ids = self.env['product.template'].browse(active_template_ids)
        # odoo_templates = self.env['product.template'].search(
        #     [('id', 'in', template_ids), ('default_code', '!=', False)])
        # if not odoo_templates:
        #     raise Warning("Internel Reference (SKU) not set in selected products")
        odoo_template_ids = template_ids.filtered(lambda template:template.type == 'product')
        if not odoo_template_ids:
            raise Warning(_('It seems like selected products are not Storable Products.'))
        shopify_image = False
        is_shopify_variant = False
        for instance in self.instance_ids:
            for odoo_template in odoo_template_ids:
                gallery_image_keys = {}
                product_img_seq = 1
                if len(odoo_template.attribute_line_ids) > 3:
                    continue
                if len(odoo_template.product_variant_ids.ids) == 1 and not odoo_template.default_code:
                    continue
                shopify_template = shopify_template_obj.search(
                    [('shopify_instance_id', '=', instance.id),
                     ('product_tmpl_id', '=', odoo_template.id)])
                if not shopify_template:
                    shopify_template = shopify_template_obj.create(
                        {'shopify_instance_id': instance.id, 'product_tmpl_id': odoo_template.id,
                         'name': odoo_template.name, 'description': odoo_template.description_sale,
                         'shopify_product_category': odoo_template.categ_id.id})
                if odoo_template.image:
                    shopify_image = shopify_product_image_obj.search(
                        [('shopify_instance_id', '=', instance.id),
                         ('shopify_product_tmpl_id', '=', shopify_template.id)])
                    if not shopify_image:
                        template_image = shopify_product_image_obj.create(
                            {'position': product_img_seq,
                             'shopify_product_tmpl_id': shopify_template.id,
                             'shopify_instance_id': instance.id, 'image_id': odoo_template.image})
                        product_img_seq += 1
                        key = odoo_template.image and hashlib.md5(
                            odoo_template.image).hexdigest() or False
                        gallery_image_keys.update({key: template_image})
                if shopify_image:
                    last_image = list(shopify_image)
                    last_image_position = last_image[len(last_image) - 1:]
                    last_position = last_image_position[0].position
                    product_img_seq = last_position + 1
                sequence = 1
                for variant in odoo_template.product_variant_ids.filtered(lambda variant:variant.default_code != False):
                    shopify_variant = shopify_product_obj.search(
                        [('shopify_instance_id', '=', instance.id),
                         ('product_id', '=', variant.id)])
                    is_shopify_variant = False
                    if shopify_variant:
                        is_shopify_variant = True
                    if not shopify_variant:
                        shopify_variant = shopify_product_obj.create(
                            {'shopify_instance_id': instance.id, 'product_id': variant.id,
                             'shopify_template_id': shopify_template.id,
                             'default_code': variant.default_code, 'name': variant.name,
                             'sequence': sequence})
                    else:
                        shopify_variant.write({'sequence': sequence})
                    key = variant.image and hashlib.md5(variant.image).hexdigest() or False
                    if not key:
                        continue
                    if key in gallery_image_keys:
                        gallery_image_keys.get(key).write(
                            {'shopify_variant_ids': [(4, shopify_variant.id)]})
                        continue
                    else:
                        if not is_shopify_variant:
                            variant_image = shopify_product_image_obj.create(
                                {'position': product_img_seq,
                                 'shopify_product_tmpl_id': shopify_template.id,
                                 'shopify_instance_id': instance.id, 'image_id': variant.image,
                                 'shopify_variant_ids': [(4, shopify_variant.id)]})
                            product_img_seq += 1
                            gallery_image_keys.update({key: variant_image})
                        sequence = sequence + 1
        return True

    @api.multi
    def publish_multiple_products(self):
        shopify_template_obj = self.env['shopify.product.template.ept']
        if self._context.get('process') == 'publish_multiple_products':
            template_ids = self._context.get('active_ids', [])
            templates = shopify_template_obj.search(
                [('id', 'in', template_ids), ('exported_in_shopify', '=', True)])
        else:
            templates = shopify_template_obj.search([('exported_in_shopify', '=', True)])
        for template in templates:
            template.shopify_published()
        return True

    @api.multi
    def publish_multiple_collection(self):
        collection_obj = self.env['shopify.collection.ept']
        if self._context.get('process') == 'publish_multiple_collection':
            collection_ids = self._context.get('active_ids')
            collections = collection_obj.search(
                [('id', 'in', collection_ids), ('exported_in_shopify', '=', True)])
        else:
            collections = collection_obj.search([('exported_in_shopify', '=', True)])
        for collection in collections:
            collection.shopify_published()
        return True

    @api.multi
    def export_collection(self):
        collection_obj = self.env['shopify.collection.ept']
        if self._context.get('process') == 'create_collection':
            collection_ids = self._context.get('active_ids')
            instances = self.env['shopify.instance.ept'].search([])
        else:
            instances = self.instance_ids
            collection_ids = collection_obj.search([]).ids
        for instance in instances:
            collections = collection_obj.search(
                [('shopify_instance_id', '=', instance.id), ('id', 'in', collection_ids),
                 ('is_smart_collection', '=', False), ('exported_in_shopify', '=', False)])
            collections and collection_obj.export_custom_collection(instance, collections,
                                                                    self.publish_collection)
            collections = collection_obj.search(
                [('shopify_instance_id', '=', instance.id), ('id', 'in', collection_ids),
                 ('is_smart_collection', '=', True), ('exported_in_shopify', '=', False)])
            collections and collection_obj.export_smart_collection(instance, collections,
                                                                   self.publish_collection)
        return True

    @api.multi
    def update_collection(self):
        collection_obj = self.env['shopify.collection.ept']
        if self._context.get('process') == 'update_collection':
            collection_ids = self._context.get('active_ids')
            instances = self.env['shopify.instance.ept'].search([])
        else:
            instances = self.instance_ids
            collection_ids = collection_obj.search([]).ids
        for instance in instances:
            collections = collection_obj.search(
                [('shopify_instance_id', '=', instance.id), ('id', 'in', collection_ids),
                 ('is_smart_collection', '=', False), ('exported_in_shopify', '=', True)])
            collections and collection_obj.update_custom_collection(instance, collections)

            collections = collection_obj.search(
                [('shopify_instance_id', '=', instance.id), ('id', 'in', collection_ids),
                 ('is_smart_collection', '=', True), ('exported_in_shopify', '=', True)])
            collections and collection_obj.update_smart_collection(instance, collections)
        return True

    @api.multi
    def import_collection(self):
        collection_obj = self.env['shopify.collection.ept']
        for instance in self.instance_ids:
            collection_obj.import_collection(instance)
        return True

    @api.multi
    def sync_selective_products(self):
        active_ids = self._context.get('active_ids')
        shopify_template_obj = self.env['shopify.product.template.ept']
        for instance in self.instance_ids:
            shopify_templates = shopify_template_obj.search(
                [('id', 'in', active_ids), ('shopify_instance_id', '=', instance.id),
                 ('shopify_tmpl_id', '=', False)])
            if shopify_templates:
                raise Warning("You can only sync already exported products")
            shopify_templates = shopify_template_obj.search(
                [('id', 'in', active_ids), ('shopify_instance_id', '=', instance.id)])
            for shopify_template in shopify_templates:
                shopify_template_obj.sync_products(instance,
                                                   shopify_tmpl_id=shopify_template.shopify_tmpl_id,
                                                   sync_images_with_product=self.sync_images_with_product,
                                                   update_price=self.sync_price_with_product)
        return True

        # Modify by Haresh mori on date 18/05/2019 The Changes related to update template while sync products from shopify to odoo.

    @api.multi
    def sync_products(self):
        shopify_template_obj = self.env['shopify.product.template.ept']
        for instance in self.instance_ids:
            update_template = True
            if self.is_skip_sync_existing_shopify_product:
                update_template = False
            shopify_template_obj.sync_products(instance, update_price=self.update_price_in_product,
                                               sync_images_with_product=instance.sync_images_with_product,
                                               update_templates=update_template)
        return True
