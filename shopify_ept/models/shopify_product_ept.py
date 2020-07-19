from odoo import models, fields, api, _
import odoo.addons.decimal_precision  as dp
from .. import shopify
import urllib
import base64
import time
from datetime import datetime, timedelta
import hashlib
import csv
import logging

_logger = logging.getLogger('shopify_process===(Emipro)===')

class product_attribute(models.Model):
    _inherit = "product.attribute"
    shopify_name = fields.Char("Shopify Name")

class product_category(models.Model):
    _inherit = "product.category"
    is_shopify_product_cat = fields.Boolean('Is Shopify Product Category')

class shopify_product_template_ept(models.Model):
    _name = "shopify.product.template.ept"
    _description = 'Shopify Product Template Ept'

    @api.multi
    @api.depends('shopify_product_ids.exported_in_shopify', 'shopify_product_ids.variant_id')
    def get_total_sync_variants(self):
        shopify_product_obj = self.env['shopify.product.product.ept']
        for template in self:
            variants = shopify_product_obj.search(
                    [('id', 'in', template.shopify_product_ids.ids),
                     ('exported_in_shopify', '=', True),
                     ('variant_id', '!=', False)])
            template.total_sync_variants = len(variants.ids)

    name = fields.Char("Name")
    shopify_instance_id = fields.Many2one("shopify.instance.ept", "Instance", required=1)
    product_tmpl_id = fields.Many2one("product.template", "Product Template", required=1)
    shopify_tmpl_id = fields.Char("Shopify Tmpl Id")
    exported_in_shopify = fields.Boolean("Exported In Shopify")
    shopify_product_ids = fields.One2many("shopify.product.product.ept", "shopify_template_id",
                                          "Products")
    template_suffix = fields.Char("Template Suffix")
    created_at = fields.Datetime("Created At")
    updated_at = fields.Datetime("Updated At")
    published_at = fields.Datetime("Publish at")
    inventory_management = fields.Selection(
            [('shopify', 'Shopify tracks this product Inventory'),
             ('Dont track Inventory', 'Dont track Inventory')],
            default='shopify')
    check_product_stock = fields.Boolean("Sale out of stock products ?", default=False)
    taxable = fields.Boolean("Taxable", default=True)
    fulfillment_service = fields.Selection(
            [('manual', 'Manual'), ('shopify', 'shopify'), ('gift_card', 'Gift Card')],
            default='manual')
    website_published = fields.Boolean('Available in the website', copy=False)
    tag_ids = fields.Many2many("shopify.tags", "shopify_tags_rel", "product_tmpl_id", "tag_id",
                               "Tags")
    description = fields.Html("Description")
    total_variants_in_shopify = fields.Integer("Total Shopify Varaints", default=0)
    total_sync_variants = fields.Integer("Total Sync Variants", compute="get_total_sync_variants",
                                         store=True)
    shopify_gallery_image_ids = fields.One2many('shopify.product.image.ept',
                                                'shopify_product_tmpl_id',
                                                'Gallery Images')
    shopify_product_category = fields.Many2one("product.category", "Product Category")

    @api.multi
    def reorder_variants(self):
        res = self.env.ref('shopify_ept.view_shopify_reorder_variants_wizard')
        action = {
            'name':'Reorder Variants',
            'view_type':'form',
            'view_mode':'form',
            'view_id':res.ids,
            'res_model':'shopify.variant.reorder.ept',
            'context':self._context,
            'type':'ir.actions.act_window',
            'nodestroy':True,
            'target':'new',
        }
        return action

    @api.multi
    def list_all_products(self, results):
        sum_product_list = []
        catch = ""
        while results:
            page_info = ""
            sum_product_list += results
            link = shopify.ShopifyResource.connection.response.headers.get('Link')
            if not link or not isinstance(link, str):
                return sum_product_list
            for page_link in link.split(','):
                if page_link.find('next') > 0:
                    page_info = page_link.split(';')[0].strip('<>').split('page_info=')[1]
                    try:
                        results = shopify.Product().find(page_info=page_info, limit=250)
                    except Exception as e:
                        if e.response.code == 429 and e.response.msg == "Too Many Requests":
                            time.sleep(5)
                            results = shopify.Product().find(page_info=page_info, limit=250)
                        else:
                            raise Warning(e)
            if catch == page_info:
                break
        return sum_product_list

    @api.multi
    def set_variant_sku(self, result, product_template, instance):
        product_attribute_obj = self.env['product.attribute']
        product_attribute_value_obj = self.env['product.attribute.value']
        odoo_product_obj = self.env['product.product']

        for variation in result.get('variants'):
            sku = variation.get('sku')
            price = variation.get('price')
            barcode = variation.get('barcode') or False
            if barcode and barcode.__eq__("false"):
                barcode = False
            attribute_value_ids = []
            domain = []
            odoo_product = False
            variation_attributes = []
            option_name = []
            for options in result.get('options'):
                attrib_name = options.get('name')
                attrib_name and option_name.append(attrib_name)

            option1 = variation.get('option1', False)
            option2 = variation.get('option2', False)
            option3 = variation.get('option3', False)
            if option1 and (option_name and option_name[0]):
                variation_attributes.append({"name":option_name[0], "option":option1})
            if option2 and (option_name and option_name[1]):
                variation_attributes.append({"name":option_name[1], "option":option2})
            if option3 and (option_name and option_name[2]):
                variation_attributes.append({"name":option_name[2], "option":option3})

            for variation_attribute in variation_attributes:
                attribute_val = variation_attribute.get('option')
                attribute_name = variation_attribute.get('name')
                product_attribute = product_attribute_obj.search(
                        [('name', '=ilike', attribute_name)], limit=1)
                if product_attribute:
                    product_attribute_value = product_attribute_value_obj.search(
                            [('attribute_id', '=', product_attribute.id),
                             ('name', '=', attribute_val)], limit=1)
                    product_attribute_value and attribute_value_ids.append(
                            product_attribute_value.id)

            for attribute_value_id in attribute_value_ids:
                tpl = ('attribute_value_ids', '=', attribute_value_id)
                domain.append(tpl)
            domain and domain.append(('product_tmpl_id', '=', product_template.id))
            if domain:
                odoo_product = odoo_product_obj.search(domain)
            odoo_product and odoo_product.write({'default_code':sku})
            if barcode:
                odoo_product and odoo_product.write({'barcode':barcode})
            if price and instance.import_price:
                if instance.pricelist_id.currency_id.id == product_template.company_id.currency_id.id:
                    odoo_product and odoo_product.write({'list_price':price.replace(",", ".")})
                else:
                    instance_currency = instance.pricelist_id.currency_id
                    product_company_currency = product_template.company_id.currency_id
                    amount = instance_currency.compute(float(price), product_company_currency)
                    odoo_product and odoo_product.write({'list_price':amount})
        return True

    @api.multi
    def create_variant_product(self, result, instance, price, product_category):
        product_attribute_obj = self.env['product.attribute']
        product_attribute_value_obj = self.env['product.attribute.value']
        product_template_obj = self.env['product.template']

        template_title = result.get('title', '')
        attrib_line_vals = []

        for attrib in result.get('options'):
            attrib_name = attrib.get('name')
            attrib_values = attrib.get('values')
            attribute = product_attribute_obj.search([('name', '=ilike', attrib_name)], limit=1)
            if not attribute:
                attribute = product_attribute_obj.create({'name':attrib_name})
            attr_val_ids = []

            for attrib_vals in attrib_values:
                attrib_value = product_attribute_value_obj.search(
                        [('attribute_id', '=', attribute.id), ('name', '=', attrib_vals)], limit=1)
                if not attrib_value:
                    attrib_value = product_attribute_value_obj.with_context(active_id=False).create(
                            {'attribute_id':attribute.id, 'name':attrib_vals})
                attr_val_ids.append(attrib_value.id)

            if attr_val_ids:
                attribute_line_ids_data = [0, False,
                                           {'attribute_id':attribute.id,
                                            'value_ids':[[6, False, attr_val_ids]]}]
                attrib_line_vals.append(attribute_line_ids_data)
        if attrib_line_vals:
            product_template = product_template_obj.create({'name':template_title,
                                                            'type':'product',
                                                            'attribute_line_ids':attrib_line_vals,
                                                            'description_sale':result.get(
                                                                    'description', ''),
                                                            'categ_id':product_category.id
                                                            })
            if instance.import_price:
                if instance.pricelist_id.currency_id.id == product_template.company_id.currency_id.id:
                    product_template.write({'list_price':price.replace(",", ".")})
                else:
                    instance_currency = instance.pricelist_id.currency_id
                    product_company_currency = product_template.company_id.currency_id
                    amount = instance_currency.compute(float(price), product_company_currency)
                    product_template.write({'list_price':amount})

            self.set_variant_sku(result, product_template, instance)
        else:
            return False
        return True

    @api.multi
    def is_product_importable(self, result, instance, odoo_product, shopify_product):
        shopify_skus = []
        shopify_barcodes = []
        odoo_skus = []
        odoo_barcodes = []
        product_sku_barcodes = []
        odoo_product_obj = self.env['product.product']
        variants = result.get('variants')
        template_title = result.get('title', '')
        template_id = result.get('id', '')
        product_count = len(variants)
        importable = True
        message = ""

        if not odoo_product and not shopify_product:
            for variantion in variants:
                sku = variantion.get("sku") or False
                barcode = variantion.get('barcode', '') or False
                sku and shopify_skus.append(sku)
                barcode and shopify_barcodes.append(barcode)
                product_sku_barcodes.append(
                        {"name":template_title, "sku":sku or '', "barcode":barcode or ''})
                if barcode:
                    odoo_product = odoo_product_obj.search([("barcode", "=", barcode)], limit=1)
                if not odoo_product and sku:
                    odoo_product = odoo_product_obj.search([("default_code", "=", sku)], limit=1)
                if odoo_product and odoo_product.product_tmpl_id.product_variant_count > 1:
                    message = "Total number of variants in shopify and odoo are not match or all the SKU(s) are not match or all the Barcode(s) are not match for Product: %s and ID: %s." % (
                        template_title, template_id)
                    importable = False
                    return importable, message
            for product_sku_barcode in product_sku_barcodes:
                sku = product_sku_barcode.get("sku") or False
                barcode = product_sku_barcode.get("barcode") or False
                if not sku and not barcode:
                    message = "All SKU(s) or Barcode(s) are not set in Product: %s and ID: %s." % (
                        template_title, template_id)
                    if product_count == 1:
                        message = "SKU or Barcode is not set in Product: %s and ID: %s." % (
                            template_title, template_id)
                    importable = False
                    return importable, message
            total_shopify_sku = len(set(shopify_skus))
            if not len(shopify_skus) == total_shopify_sku:
                message = "Duplicate SKU found in Product: %s and ID: %s." % (
                    template_title, template_id)
                importable = False
                return importable, message
            total_shopify_barcodes = len(set(shopify_barcodes))
            if not len(shopify_barcodes) == total_shopify_barcodes:
                message = "Duplicate barcode found in Product: %s and ID: %s." % (
                    template_title, template_id)
                importable = False
                return importable, message

        if odoo_product:
            odoo_template = odoo_product.product_tmpl_id
            if not (product_count == 1 and odoo_template.product_variant_count == 1):
                if product_count == odoo_template.product_variant_count:
                    for shopify_prdct, odoo_prdct in zip(result.get('variants'),
                                                         odoo_template.product_variant_ids):
                        sku = shopify_prdct.get('sku') or False
                        barcode = shopify_prdct.get('barcode', '') or False
                        sku and shopify_skus.append(sku)
                        barcode and shopify_barcodes.append(barcode)
                        product_sku_barcodes.append(
                                {"name":template_title, "sku":sku or '', "barcode":barcode or ''})
                        odoo_prdct and odoo_prdct.default_code and odoo_skus.append(
                                odoo_prdct.default_code)
                        odoo_prdct and odoo_prdct.barcode and odoo_barcodes.append(
                                odoo_prdct.barcode)

                    shopify_skus = list(filter(lambda x:len(x) > 0, shopify_skus))
                    odoo_skus = list(filter(lambda x:len(x) > 0, odoo_skus))
                    shopify_barcodes = list(filter(lambda x:len(x) > 0, shopify_barcodes))
                    odoo_barcodes = list(filter(lambda x:len(x) > 0, odoo_barcodes))

                    for product_sku_barcode in product_sku_barcodes:
                        sku = product_sku_barcode.get("sku") or False
                        barcode = product_sku_barcode.get("barcode") or False
                        if not sku and not barcode:
                            message = "All SKU(s) or Barcode(s) are not set in Product: %s and ID: %s." % (
                                template_title, template_id)
                            importable = False
                            return importable, message

                    total_shopify_sku = len(set(shopify_skus))
                    if not len(shopify_skus) == total_shopify_sku:
                        message = "Duplicate SKU found in Product: %s and ID: %s." % (
                            template_title, template_id)
                        importable = False
                        return importable, message
                    total_shopify_barcodes = len(set(shopify_barcodes))
                    if not len(shopify_barcodes) == total_shopify_barcodes:
                        message = "Duplicate barcode found in Product: %s and ID: %s." % (
                            template_title, template_id)
                        importable = False
                        return importable, message

                    for sku in shopify_skus:
                        if sku not in odoo_skus:
                            message = "SKU not found in Odoo for Product: %s and SKU: %s." % (
                                template_title, sku)
                            importable = False
                            return importable, message
                    for barcode in shopify_barcodes:
                        if barcode not in odoo_barcodes:
                            message = "Barcode not found in Odoo for Product: %s and Barcode: %s." % (
                                template_title, barcode)
                            importable = False
                            return importable, message
                else:
                    message = "All SKU(s) or Barcode(s) not as per Odoo product in Product: %s and ID: %s." % (
                        template_title, template_id)
                    if product_count == 1:
                        message = "Product: %s and ID: %s is simple product in shopify but Odoo has it product as variant." % (
                            template_title, template_id)
                    importable = False
                    return importable, message

        if shopify_product:
            shopify_skus = []
            shopify_barcodes = []
            product_sku_variants = []
            for variantion in variants:
                variant_id = variantion.get("id") or False
                sku = variantion.get("sku") or False
                barcode = variantion.get('barcode', '') or False
                sku and shopify_skus.append(sku)
                barcode and shopify_barcodes.append(barcode)
                product_sku_barcodes.append(
                        {"name":template_title, "sku":sku or '', "barcode":barcode or ''})
                product_sku_variants.append(
                        {"variant_id":variant_id, "name":template_title, "sku":sku or '',
                         "barcode":barcode or ''})

            # Add by Haresh Mori
            # For Extra variant
            odoo_products = False
            odoo_products = []
            if shopify_product and len(
                    product_sku_barcodes) != shopify_product.shopify_template_id.total_variants_in_shopify:
                for product_sku_barcode in product_sku_barcodes:
                    odoo_product = odoo_product_obj.search(
                            [("default_code", "=", product_sku_barcode.get("sku"))],
                            limit=1) or False
                    if odoo_product:
                        odoo_products.append(odoo_product)

                        # Added by Priya Pal
            # For same variant id
            if shopify_product.product_id.product_tmpl_id.product_variant_count != len(
                    product_sku_barcodes):
                shopify_product_obj = self.env['shopify.product.product.ept']
                for product_sku_variant in product_sku_variants:
                    shopify_product = shopify_product_obj.search(
                            [("variant_id", "=", product_sku_variant.get("variant_id"))],
                            limit=1) or False
                    if shopify_product:
                        message = "Product with Variant ID: %s Already link in odoo product for Product: %s and ID: %s." % (
                            shopify_product.variant_id, template_title, template_id)
                        importable = False
                        return importable, message

            #             if shopify_product and odoo_products and len(product_sku_barcodes) != len(odoo_products):
            # #                 message = "Same SKU(s) or Barcode(s) Already exists in another product in Odoo for Product: %s and ID: %s." % (
            # #                 template_title, template_id)
            #                 message = "Product with same Variant Id Already exists in same product in Odoo for Product: %s and ID: %s." % (
            #                 template_title, template_id,)
            #                 importable = False
            #                 return importable, message

            total_shopify_sku = len(set(shopify_skus))
            if not len(shopify_skus) == total_shopify_sku:
                message = "Duplicate SKU found in Product %s and ID: %s." % (
                    template_title, template_id)
                importable = False
                return importable, message
            total_shopify_barcodes = len(set(shopify_barcodes))
            if not len(shopify_barcodes) == total_shopify_barcodes:
                message = "Duplicate Barcode found in Product %s and ID: %s." % (
                    template_title, template_id)
                importable = False
                return importable, message

        return importable, message

    @api.multi
    def sync_product_images(self, instance, shopify_template=False, image_response=False):
        shopify_product_img = self.env['shopify.product.image.ept']
        shopify_product_obj = self.env['shopify.product.product.ept']
        if not image_response:
            instance.connect_in_shopify()
            try:
                images = shopify.Image().find(product_id=shopify_template.shopify_tmpl_id)
            except Exception as e:
                if e.response.code == 429 and e.response.msg == "Too Many Requests":
                    time.sleep(5)
                    images = shopify.Image().find(product_id=shopify_template.shopify_tmpl_id)
                else:
                    raise Warning(e)
            image_response = [image.to_dict() for image in images]
        for image in image_response:
            shopify_image_id = False
            if image.get('src'):
                variant_ids = image.get('variant_ids')
                shopify_image_id = image.get('id')
                shopify_variants = shopify_product_obj.search(
                        [('shopify_instance_id', '=', instance.id),
                         ('variant_id', 'in', variant_ids)])
                shopify_variants.write({'shopify_image_id':shopify_image_id})
                odoo_product_ids = variant_ids and [shopify_variant.product_id for shopify_variant
                                                    in
                                                    shopify_variants] or []
                shopify_product_ids = variant_ids and [
                    (6, 0, [shopify_variant.id for shopify_variant in shopify_variants])]
                shopify_gallery_image = shopify_product_img.search(
                        [('shopify_product_tmpl_id', '=', shopify_template.id),
                         ('shopify_image_id', '=', shopify_image_id)], limit=1)
                if not instance.is_image_url:
                    try:
                        (filename, header) = urllib.request.urlretrieve(image.get('src'))
                        with open(filename, 'rb') as f:
                            img = base64.b64encode(f.read())
                    except Exception:
                        continue
                    for products in odoo_product_ids:
                        products.write({'image':img})
                    if shopify_gallery_image:
                        shopify_gallery_image.write(
                                {'position':image.get('position'), 'height':image.get('height'),
                                 'width':image.get('width'), 'image_id':img,
                                 'shopify_variant_ids':shopify_product_ids and shopify_product_ids})
                    else:
                        shopify_gallery_image = shopify_product_img.search(
                                [('shopify_product_tmpl_id', '=', shopify_template.id),
                                 ('position', '=', image.get('position'))], limit=1)
                        if shopify_gallery_image:
                            shopify_gallery_image.write(
                                    {'position':image.get('position'), 'height':image.get('height'),
                                     'width':image.get('width'), 'image_id':img,
                                     'shopify_variant_ids':shopify_product_ids and shopify_product_ids})
                        else:
                            shopify_product_img.create(
                                    {'shopify_product_tmpl_id':shopify_template.id,
                                     'shopify_instance_id':instance.id,
                                     'image_id':img, 'shopify_image_id':image.get('id'),
                                     'position':image.get('position'),
                                     'height':image.get('height'), 'width':image.get('width'),
                                     'shopify_variant_ids':shopify_product_ids and shopify_product_ids})
                    if image.get('position') == 1:
                        shopify_template.product_tmpl_id.write({'image':img})
                else:
                    if shopify_gallery_image:
                        shopify_gallery_image.write(
                                {'position':image.get('position'), 'height':image.get('height'),
                                 'width':image.get('width'),
                                 'shopify_variant_ids':shopify_product_ids and shopify_product_ids})
                    else:
                        shopify_product_img.create(
                                {'shopify_product_tmpl_id':shopify_template.id,
                                 'shopify_instance_id':instance.id,
                                 'url':image.get('src'), 'shopify_image_id':image.get('id'),
                                 'position':image.get('position'), 'height':image.get('height'),
                                 'width':image.get('width'),
                                 'shopify_variant_ids':shopify_product_ids and shopify_product_ids})
        return True

    @api.multi
    def sync_products(self, instance, sync_images_with_product=False, shopify_tmpl_id=False,
                      update_price=False,
                      update_templates=True):
        shopify_product_obj = self.env['shopify.product.product.ept']
        transaction_log_obj = self.env["shopify.transaction.log"]
        odoo_product_obj = self.env['product.product']
        product_template_obj = self.env['product.template']
        product_category_obj = self.env['product.category']
        instance.connect_in_shopify()
        if shopify_tmpl_id:
            try:
                results = [shopify.Product().find(shopify_tmpl_id)]
            except Exception as e:
                if e.response.code == 429 and e.response.msg == "Too Many Requests":
                    time.sleep(5)
                    results = [shopify.Product().find(shopify_tmpl_id)]
        else:
            results = shopify.Product().find(limit=250)
            if len(results) >= 250:
                results = self.list_all_products(results)
        for response_template in results:
            response_template = response_template.to_dict()
            template_title = response_template.get('title')
            created_at = response_template.get('created_at')
            body_html = response_template.get('body_html')
            updated_at = response_template.get('updated_at')
            tags = response_template.get('tags')
            product_type = response_template.get('product_type')
            published_at = response_template.get('published_at')
            shopify_tmpl_id = response_template.get('id')
            shopify_template = self.search(
                    [('shopify_tmpl_id', '=', shopify_tmpl_id),
                     ('shopify_instance_id', '=', instance.id)])
            if shopify_template and not update_templates:
                continue
            updated_template = False
            variant_sequence = 1
            onetime_call = False
            is_importable_checked = False
            for variant in response_template.get('variants'):
                odoo_product = False
                shopify_variant = False
                barcode = variant.get('barcode', '') or False
                weight = variant.get('weight')
                sku = variant.get('sku', '')
                title = variant.get('title')
                price = variant.get('price').replace(",", ".")
                inventory_policy = variant.get('inventory_policy')
                inventory_management = variant.get('inventory_management')
                fulfillment_service = variant.get('fulfillment_service')
                taxable = variant.get('taxable')
                variant_id = variant.get('id')
                inventory_item_id = variant.get('inventory_item_id')
                shopify_variant = shopify_product_obj.search(
                        [('variant_id', '=', variant_id),
                         ('shopify_instance_id', '=', instance.id)], limit=1)
                if not shopify_variant and barcode:
                    shopify_variant = shopify_product_obj.search(
                            [('product_id.barcode', '=', barcode),
                             ('shopify_instance_id', '=', instance.id)], limit=1)
                if not shopify_variant and barcode:
                    odoo_product = odoo_product_obj.search([('barcode', '=', barcode)], limit=1)
                if not odoo_product and not shopify_variant and sku:
                    shopify_variant = shopify_product_obj.search(
                            [('default_code', '=', sku), ('shopify_instance_id', '=', instance.id)],
                            limit=1)
                    if not shopify_variant and sku:
                        odoo_product = odoo_product_obj.search([('default_code', '=', sku)],
                                                               limit=1)
                product_category = product_category_obj.search([('name', '=', product_type),
                                                                ('is_shopify_product_cat', '=',
                                                                 True)])
                if not product_category:
                    product_category = product_category_obj.create(
                            {'name':product_type, 'is_shopify_product_cat':True})

                is_importable = True
                message = ""
                if not is_importable_checked:
                    is_importable, message = self.is_product_importable(response_template, instance,
                                                                        odoo_product,
                                                                        shopify_variant)
                    log = transaction_log_obj.search([("message", "=", message)], limit=1)
                    if not is_importable:
                        if not log:
                            transaction_log_obj.create(
                                    {'message':message,
                                     'mismatch_details':True,
                                     'type':'product',
                                     'shopify_instance_id':instance.id})
                        else:
                            log.write({'message':message})
                        break

                    else:
                        is_importable_checked = True

                if not odoo_product and not shopify_variant:
                    if instance.auto_import_product:
                        if not onetime_call:
                            if len(response_template.get('variants')) > 1:
                                self.create_variant_product(response_template, instance, price,
                                                            product_category)
                            else:
                                if sku or barcode:
                                    new_templ_obj = product_template_obj.create(
                                            {'name':template_title,
                                             'default_code':sku or '',
                                             'barcode':barcode or '',
                                             'type':'product',
                                             'categ_id':product_category.id
                                             })
                                    if instance.import_price:
                                        if instance.pricelist_id.currency_id.id == new_templ_obj.company_id.currency_id.id:
                                            new_templ_obj.write(
                                                    {'list_price':price.replace(",", ".")})
                                        else:
                                            instance_currency = instance.pricelist_id.currency_id
                                            product_company_currency = new_templ_obj.company_id.currency_id
                                            amount = instance_currency.compute(float(price),
                                                                               product_company_currency)
                                            new_templ_obj.write({'list_price':amount})
                                else:
                                    message = "Product %s and ID: %s has nither set barcode nor sku." % (
                                        template_title, response_template.get('id'))
                                    log = transaction_log_obj.search(
                                            [('shopify_instance_id', '=', instance.id),
                                             ('message', '=', message)])
                                    if not log:
                                        transaction_log_obj.create(
                                                {'message':message,
                                                 'mismatch_details':True,
                                                 'type':'product',
                                                 'shopify_instance_id':instance.id
                                                 })
                                    else:
                                        log.write({'message':message})

                                    continue
                            odoo_product = odoo_product_obj.search([('default_code', '=', sku)],
                                                                   limit=1)
                            if not odoo_product:
                                odoo_product = odoo_product_obj.search([('barcode', '=', barcode)],
                                                                       limit=1)
                            onetime_call = True
                            if not odoo_product:
                                message = "Attribute(s) are not set properly in Product: %s." % (
                                    template_title)
                                transaction_log_obj.create(
                                        {'message':message,
                                         'mismatch_details':True,
                                         'type':'product',
                                         'shopify_instance_id':instance.id})
                                break
                    else:
                        message = "%s Product Not found for barcode %s and sku %s" % (
                            template_title, barcode, sku)
                        log = transaction_log_obj.search(
                                [('shopify_instance_id', '=', instance.id),
                                 ('message', '=', message)])
                        if not log:
                            transaction_log_obj.create(
                                    {'message':message,
                                     'mismatch_details':True,
                                     'type':'product',
                                     'shopify_instance_id':instance.id
                                     })
                        else:
                            log.write({'message':message})

                        continue
                if not shopify_variant:
                    vals = {}
                    if not shopify_template:
                        if inventory_policy == 'continue':
                            vals.update({'check_product_stock':True})
                        if inventory_management == 'shopify':
                            vals.update({'inventory_management':'shopify'})
                        else:
                            vals.update({'inventory_management':'Dont track Inventory'})

                        shopify_template = self.search(
                                [('product_tmpl_id', '=', odoo_product.product_tmpl_id.id),
                                 ('shopify_instance_id', '=', instance.id)])
                        vals.update(
                                {'product_tmpl_id':odoo_product.product_tmpl_id.id,
                                 'shopify_instance_id':instance.id,
                                 'name':template_title,
                                 'shopify_tmpl_id':shopify_tmpl_id,
                                 'fulfillment_service':fulfillment_service,
                                 'taxable':taxable,
                                 'created_at':created_at,
                                 'updated_at':updated_at,
                                 'description':body_html,
                                 'published_at':published_at,
                                 'website_published':published_at and True or False,
                                 'exported_in_shopify':True,
                                 'total_variants_in_shopify':len(response_template.get('variants'))
                                 })

                        shopify_tag_obj = self.env['shopify.tags']
                        list_of_tags = []
                        sequence = 1
                        for tag in tags.split(','):
                            if not len(tag) > 0:
                                continue
                            shopify_tag = shopify_tag_obj.search([('name', '=', tag)], limit=1)
                            sequence = shopify_tag and shopify_tag.sequence or 0
                            if not shopify_tag:
                                sequence = sequence + 1
                                shopify_tag = shopify_tag_obj.create(
                                        {'name':tag, 'sequence':sequence})
                            list_of_tags.append(shopify_tag.id)
                        vals.update({'tag_ids':[(6, 0, list_of_tags)]})

                        shopify_template = self.create(vals)
                        shopify_template.write({'shopify_product_category':product_category.id})
                        if instance.update_category_in_odoo_product:
                            shopify_template.product_tmpl_id.write({'categ_id':product_category.id})
                    vals = {}
                    vals.update({'product_id':odoo_product.id,
                                 'default_code':sku, 'name':title,
                                 'variant_id':variant_id,
                                 'shopify_template_id':shopify_template.id,
                                 'shopify_instance_id':instance.id,
                                 'created_at':created_at,
                                 'updated_at':updated_at,
                                 'exported_in_shopify':True,
                                 'sequence':variant_sequence,
                                 'inventory_item_id':inventory_item_id
                                 })

                    shopify_product_obj.create(vals)
                    variant_sequence = variant_sequence + 1
                    if update_price:
                        odoo_product.write({'list_price':price.replace(",", ".")})
                else:
                    if not updated_template:
                        vals = {}
                        vals.update(
                                {'name':template_title, 'fulfillment_service':fulfillment_service,
                                 'taxable':taxable, 'created_at':created_at,
                                 'updated_at':updated_at,
                                 'exported_in_shopify':True, 'shopify_tmpl_id':shopify_tmpl_id,
                                 'description':body_html,
                                 'total_variants_in_shopify':len(response_template.get('variants'))
                                 })
                        if published_at:
                            vals.update({'website_published':True})
                        updated_template = True

                        shopify_tag_obj = self.env['shopify.tags']
                        list_of_tags = []
                        sequence = 1
                        for tag in tags.split(','):
                            if not len(tag) > 0:
                                continue
                            shopify_tag = shopify_tag_obj.search([('name', '=', tag)], limit=1)
                            sequence = shopify_tag and shopify_tag.sequence or 0
                            if not shopify_tag:
                                sequence = sequence + 1
                                shopify_tag = shopify_tag_obj.create(
                                        {'name':tag, 'sequence':sequence})
                            list_of_tags.append(shopify_tag.id)
                        vals.update({'tag_ids':[(6, 0, list_of_tags)]})

                        if not shopify_template:
                            shopify_template = shopify_variant.shopify_template_id

                        shopify_template.write(vals)
                        shopify_template.write({'shopify_product_category':product_category.id})
                        if instance.update_category_in_odoo_product:
                            shopify_template.product_tmpl_id.write({'categ_id':product_category.id})
                    tmpl_vals = {}
                    vals = {}
                    if inventory_policy == 'continue':
                        vals.update({'check_product_stock':'continue'})
                        tmpl_vals.update({'check_product_stock':True})
                    else:
                        vals.update({'check_product_stock':'deny'})
                        tmpl_vals.update({'check_product_stock':False})
                    if inventory_management == 'shopify':
                        vals.update({'inventory_management':'shopify'})
                        tmpl_vals.update({'inventory_management':'shopify'})
                    else:
                        vals.update({'inventory_management':'Dont track Inventory'})
                        tmpl_vals.update({'inventory_management':'Dont track Inventory'})
                    vals.update({
                        'default_code':sku,
                        'variant_id':variant_id,
                        'shopify_template_id':shopify_template.id,
                        'shopify_instance_id':instance.id,
                        'created_at':created_at,
                        'updated_at':updated_at,
                        'exported_in_shopify':True,
                        'sequence':variant_sequence,
                        'inventory_item_id':inventory_item_id
                    })
                    shopify_variant.write(vals)
                    shopify_variant.shopify_template_id.write(tmpl_vals)
                    variant_sequence = variant_sequence + 1
                if shopify_variant:
                    odoo_product = shopify_variant.product_id
                if instance.import_price and odoo_product:
                    pricelist_item = self.env['product.pricelist.item'].search(
                            [('pricelist_id', '=', instance.pricelist_id.id),
                             ('product_id', '=', odoo_product.id)], limit=1)
                    if not pricelist_item:
                        instance.pricelist_id.write({
                            'item_ids':[(0, 0, {
                                'applied_on':'0_product_variant',
                                'product_id':odoo_product.id,
                                'compute_price':'fixed',
                                'fixed_price':price})]
                        })
                    else:
                        pricelist_item.write({'fixed_price':price})
                # proudct_list = instance.pricelist_id.item_ids.mapped('product_id').ids
                # if odoo_product and odoo_product.id not in proudct_list and instance.import_price:
                #     instance.pricelist_id.write({
                #         'item_ids': [(0, 0, {
                #             'applied_on': '0_product_variant',
                #             'product_id': odoo_product.id,
                #             'compute_price': 'fixed',
                #             'fixed_price': price})]
                #     })

            if sync_images_with_product and shopify_template:
                self.sync_product_images(instance, shopify_template=shopify_template,
                                         image_response=response_template.get('images', {}))
            self._cr.commit()
        return True

    #     @api.multi
    #     def get_stock(self, shopify_product, warehouse_id, stock_type='virtual_available'):
    #         product = self.env['product.product'].with_context(warehouse=warehouse_id).browse(shopify_product.product_id.id)
    #         actual_stock = getattr(product, stock_type)
    #         if actual_stock >= 1.00:
    #             if shopify_product.fix_stock_type == 'fix':
    #                 if shopify_product.fix_stock_value >= actual_stock:
    #                     return actual_stock
    #                 else:
    #                     return shopify_product.fix_stock_value
    #
    #             elif shopify_product.fix_stock_type == 'percentage':
    #                 quantity = int((actual_stock * shopify_product.fix_stock_value) / 100.0)
    #                 if quantity >= actual_stock:
    #                     return actual_stock
    #                 else:
    #                     return quantity
    #         return actual_stock

    @api.model
    def auto_update_stock_ept(self, ctx={}):
        product_obj = self.env['product.product']
        shopify_instance_obj = self.env['shopify.instance.ept']
        if not isinstance(ctx, dict) or not 'shopify_instance_id' in ctx:
            return True
        shopify_instance_id = ctx.get('shopify_instance_id', False)
        shopify_templates = False
        if shopify_instance_id:
            instance = shopify_instance_obj.search([('id', '=', shopify_instance_id)])
            if instance.shopify_last_date_update_stock:
                last_date_update_stock = instance.shopify_last_date_update_stock
            else:
                last_date_update_stock = datetime.now() - timedelta(30)
            _logger.info(
                    "Exporting Stock from Auto cron job for instance - %s.....It will take "
                    "those products which stock movement has done after this date (%s)" % (
                        instance.name, last_date_update_stock))
            odoo_products = product_obj.get_products_based_on_movement_date(last_date_update_stock,
                                                                            instance.company_id)
            if odoo_products:
                product_id_array = sorted(list(map(lambda x:x['product_id'], odoo_products)))
                shopify_products = self.env['shopify.product.product.ept'].search(
                        [('shopify_instance_id', '=', instance.id),
                         ('exported_in_shopify', '=', True),
                         ('product_id', 'in', product_id_array)])
                shopify_templates = shopify_products.mapped('shopify_template_id')
                if not shopify_templates:
                    _logger.info("No products to export stock....for instance %s " % (instance.name))
            else:
                _logger.info("No products to export stock....for instance %s " % (instance.name))

            shopify_templates and self.update_stock_in_shopify(instance=instance,
                                                               products=shopify_templates,
                                                               is_process_from_auto_cron=True)
        return True

    @api.model
    def update_stock_in_shopify(self, instance=False, products=False,
                                is_process_from_auto_cron=False):
        product_obj = self.env['product.product']
        transaction_log_obj = self.env['shopify.transaction.log']
        instances = []
        if not instance:
            instances = self.env['shopify.instance.ept'].search(
                    [('stock_auto_export', '=', True), ('state', '=', 'confirmed')])
        else:
            instances.append(instance)
        log = False
        for instance in instances:
            #             location_ids = instance.warehouse_id.lot_stock_id.child_ids.ids
            #             location_ids.append(instance.warehouse_id.lot_stock_id.id)
            #             if not products:
            #                 shopify_products = self.search(
            #                     [('shopify_instance_id', '=', instance.id), ('exported_in_shopify', '=', True)])
            #             else:
            #                 shopify_products = self.search(
            #                     [('shopify_instance_id', '=', instance.id), ('exported_in_shopify', '=', True),
            #                      ('id', 'in', products.ids)])
            shopify_products = products
            _logger.info(
                "Total Shopify template for export stock === (%s)" % (len(shopify_products)))
            instance.connect_in_shopify()

            location_ids = self.env['shopify.location.ept'].search(
                    [('legacy', '=', False), ('instance_id', '=', instance.id)])
            if not location_ids:
                message = "Location not found for instance %s while update stock" % (instance.name)
                log = transaction_log_obj.search(
                        [('shopify_instance_id', '=', instance.id), ('message', '=', message)])
                if not log:
                    transaction_log_obj.create(
                            {'message':message,
                             'mismatch_details':True,
                             'type':'stock',
                             'shopify_instance_id':instance.id
                             })

                else:
                    log.write({'message':message})

                continue

            for location_id in location_ids:
                shopify_location_warehouse = location_id.warehouse_id or False
                if not shopify_location_warehouse:
                    message = "No Warehouse found for Import Stock in Shopify Location: %s" % (
                        location_id.name)
                    if not log:
                        transaction_log_obj.create(
                                {'message':message,
                                 'mismatch_details':True,
                                 'type':'stock',
                                 'shopify_instance_id':instance.id
                                 })
                    else:
                        log.write({'message':message})

                    continue

                for template in shopify_products:
                    # try:
                    #     new_product = shopify.Product().find(template.shopify_tmpl_id)
                    # except Exception as e:
                    #     if e.response.code == 429 and e.response.msg == "Too Many Requests":
                    #         time.sleep(5)
                    #         new_product = shopify.Product().find(template.shopify_tmpl_id)
                    #     else:
                    #         message = "Template %s not found in shopify When update Stock" % (template.shopify_tmpl_id)
                    #         log = transaction_log_obj.search(
                    #             [('shopify_instance_id', '=', instance.id), ('message', '=', message)])
                    #         if not log:
                    #             transaction_log_obj.create(
                    #                 {'message': message,
                    #                  'mismatch_details': True,
                    #                  'type': 'stock',
                    #                  'shopify_instance_id': instance.id
                    #                  })
                    #
                    #         else:
                    #             log.write({'message': message})
                    #
                    #         continue
                    #
                    # new_product.id = template.shopify_tmpl_id
                    variants = []
                    info = {}
                    for variant in template.shopify_product_ids:
                        if variant.variant_id and variant.product_id.type == 'product':
                            if not variant.inventory_item_id:
                                message = "Inventory Item Id not found for variant %s with id %s for instance %s while Update stock" % (
                                    variant.name, variant.variant_id, instance.name)
                                log = transaction_log_obj.search(
                                        [('shopify_instance_id', '=', instance.id),
                                         ('message', '=', message)])
                                if not log:
                                    transaction_log_obj.create(
                                            {'message':message,
                                             'mismatch_details':True,
                                             'type':'stock',
                                             'shopify_instance_id':instance.id
                                             })

                                else:
                                    log.write({'message':message})

                                continue

                            quantity = product_obj.get_stock_ept(variant.product_id,
                                                                 location_id.warehouse_id.id,
                                                                 variant.fix_stock_type,
                                                                 variant.fix_stock_value,
                                                                 instance.stock_field.name)
                            try:
                                _logger.info(" Start Request Shopify product => (%s) Odoo product => (%s) and qty for export stock is (%s)" % (variant.name, variant.product_id.name, quantity))
                                shopify.InventoryLevel.set(location_id.shopify_location_id,
                                                           variant.inventory_item_id,
                                                           int(quantity))
                                _logger.info(
                                    " End Request Shopify product => (%s) Odoo product => (%s) and "
                                    "qty for export stock is (%s)" % (
                                    variant.name, variant.product_id.name, quantity))
                            except Exception as e:
                                _logger.info(
                                    " Exception for time out Shopify product => (%s) Odoo product "
                                    "=> (%s) and "
                                    "qty for export stock is (%s)" % (
                                    variant.name, variant.product_id.name, quantity))
                                if e.response.code == 429 and e.response.msg == "Too Many Requests":
                                    time.sleep(5)
                                    shopify.InventoryLevel.set(location_id.shopify_location_id,
                                                               variant.inventory_item_id,
                                                               int(quantity))
                                    continue
                                else:
                                    message = "Error while Update stock for variant %s with id %s for instance %s\nError: %s" % (
                                        variant.name, variant.variant_id, instance.name,
                                        str(e.response.code) + " " + e.response.msg)
                                    log = transaction_log_obj.search(
                                            [('shopify_instance_id', '=', instance.id),
                                             ('message', '=', message)])
                                    if not log:
                                        transaction_log_obj.create(
                                                {'message':message,
                                                 'mismatch_details':True,
                                                 'type':'stock',
                                                 'shopify_instance_id':instance.id
                                                 })

                                    else:
                                        log.write({'message':message})

                                    continue
                    if not products:
                        instance.write({'last_inventory_update_time':datetime.now()})
            if is_process_from_auto_cron:
                instance.write({'shopify_last_date_update_stock':datetime.now()})
        return True

    @api.model
    def update_price_in_shopify(self, instance, products):
        transaction_log_obj = self.env['shopify.transaction.log']
        instance.connect_in_shopify()

        if not products:
            shopify_products = self.search(
                    [('shopify_instance_id', '=', instance.id), ('exported_in_shopify', '=', True)])
        else:
            shopify_products = self.search(
                    [('shopify_instance_id', '=', instance.id), ('exported_in_shopify', '=', True),
                     ('id', 'in', products.ids)])

        for template in shopify_products:
            try:
                new_product = shopify.Product().find(template.shopify_tmpl_id)
            except Exception as e:
                if e.response.code == 429 and e.response.msg == "Too Many Requests":
                    time.sleep(5)
                    new_product = shopify.Product().find(template.shopify_tmpl_id)
                else:
                    message = "Template %s not found in shopify When update Price" % (
                        template.shopify_tmpl_id)
                    log = transaction_log_obj.search(
                            [('shopify_instance_id', '=', instance.id), ('message', '=', message)])
                    if not log:
                        transaction_log_obj.create(
                                {'message':message,
                                 'mismatch_details':True,
                                 'type':'price',
                                 'shopify_instance_id':instance.id
                                 })
                    else:
                        log.write({'message':message})

                    continue

            new_product.id = template.shopify_tmpl_id
            variants = []
            for variant in template.shopify_product_ids:
                info = {}
                price = instance.pricelist_id.get_product_price(variant.product_id, 1.0,
                                                                partner=False,
                                                                uom_id=variant.product_id.uom_id.id)
                variant.variant_id and info.update({'id':variant.variant_id, 'price':price})
                variants.append(info)
            new_product.variants = variants
            try:
                new_product.save()
            except Exception as e:
                if e.response.code == 429 and e.response.msg == "Too Many Requests":
                    time.sleep(5)
                    new_product.save()
        return True

    @api.multi
    def shopify_unpublished(self):
        instance = self.shopify_instance_id
        instance.connect_in_shopify()
        if self.shopify_tmpl_id:
            new_product = shopify.Product.find(self.shopify_tmpl_id)
            if new_product:
                new_product.id = self.shopify_tmpl_id
                new_product.published = 'false'
                new_product.published_at = None
                try:
                    result = new_product.save()
                except Exception as e:
                    if e.response.code == 429 and e.response.msg == "Too Many Requests":
                        time.sleep(5)
                        result = new_product.save()
                if result:
                    result_dict = new_product.to_dict()
                    updated_at = result_dict.get('updated_at')
                    published_at = result_dict.get('published_at')
                    self.write({'updated_at':updated_at, 'published_at':False,
                                'website_published':False})
        return True

    @api.multi
    def shopify_published(self):
        transaction_log_obj = self.env['shopify.transaction.log']
        instance = self.shopify_instance_id
        instance.connect_in_shopify()
        if self.shopify_tmpl_id:
            try:
                new_product = shopify.Product.find(self.shopify_tmpl_id)
                if new_product:
                    new_product.published = 'true'
                    new_product.id = self.shopify_tmpl_id
                    published_at = datetime.utcnow()
                    published_at = published_at.strftime("%Y-%m-%dT%H:%M:%S")
                    new_product.published_at = published_at
                    try:
                        result = new_product.save()
                    except Exception as e:
                        if e.response.code == 429 and e.response.msg == "Too Many Requests":
                            time.sleep(5)
                            result = new_product.save()
                    if result:
                        result_dict = new_product.to_dict()
                        updated_at = result_dict.get('updated_at')
                        published_at = result_dict.get('published_at')
                        self.write({'updated_at':updated_at, 'published_at':published_at,
                                    'website_published':True})
            except:
                message = "Template %s not found in shopify When Publish" % (self.shopify_tmpl_id)
                log = transaction_log_obj.search(
                        [('shopify_instance_id', '=', instance.id), ('message', '=', message)])
                if not log:
                    transaction_log_obj.create({'message':message,
                                                'mismatch_details':True,
                                                'type':'product',
                                                'shopify_instance_id':instance.id
                                                })
                else:
                    log.write({'message':message})

        return True

    @api.onchange("product_tmpl_id")
    def on_change_product(self):
        for record in self:
            record.name = record.product_tmpl_id.name

    @api.model
    def update_products_in_shopify(self, instance, templates):
        transaction_log_obj = self.env['shopify.transaction.log']
        instance.connect_in_shopify()

        for template in templates:
            try:
                new_product = shopify.Product().find(template.shopify_tmpl_id)
            except Exception as e:
                if e.response.code == 429 and e.response.msg == "Too Many Requests":
                    time.sleep(5)
                    new_product = shopify.Product().find(template.shopify_tmpl_id)

                else:
                    message = "Template %s not found in shopify When update Product" % (
                        template.shopify_tmpl_id)
                    log = transaction_log_obj.search(
                            [('shopify_instance_id', '=', instance.id), ('message', '=', message)])
                    if not log:
                        transaction_log_obj.create(
                                {'message':message,
                                 'mismatch_details':True,
                                 'type':'product',
                                 'shopify_instance_id':instance.id
                                 })

                    else:
                        log.write({'message':message})

                    continue

            new_product.id = template.shopify_tmpl_id
            if template.description:
                new_product.body_html = template.description
            if template.product_tmpl_id.seller_ids:
                new_product.vendor = template.product_tmpl_id.seller_ids[0].display_name
            # Take Changes for Shopify_category
            # Haresh Mori
            new_product.product_type = template.shopify_product_category.name

            tags = [tag.name for tag in template.tag_ids]
            new_product.tags = ",".join(tags)
            if template.template_suffix:
                new_product.template_suffix = template.template_suffix
            # commeted code by Maulik Barad on date 12/03/2020
            # because this method used for basic details.
            # This code is removing images in shopify as only passing the main image.
            # images = []
            # image_position = 1
            # images_with_position = {}
            # for variant in template.shopify_product_ids:
            #     if variant.product_id.image:
            #         key = hashlib.md5(variant.product_id.image).hexdigest()
            #         if not key in images_with_position:
            #             images_with_position.update({key: image_position})
            #             image_position = image_position + 1
            #
            # image_with_position = []
            # exist_images = []
            # for variant in template.shopify_product_ids:
            #     image_info = {}
            #     if variant.product_id.image:
            #         key = hashlib.md5(variant.product_id.image).hexdigest()
            #         if key not in exist_images:
            #             image_info.update({'attachment': variant.product_id.image.decode('utf-8'),
            #                                'position': images_with_position.get(key)})
            #             exist_images.append(key)
            #             images.append(image_info)
            #         image_with_position.append({'position': images_with_position.get(key), 'variant': variant})
            # if images:
            #     new_product.images = images

            new_product.title = template.name
            variants = []
            info = {}
            for variant in template.shopify_product_ids:
                if variant.variant_id:
                    info = {'id':variant.variant_id}
                else:
                    info = {}
                if variant.product_id.barcode:
                    info.update({
                        'barcode':variant.product_id.barcode
                    })

                if template.fulfillment_service == 'manual':
                    info.update({
                        'fulfillment_service':'manual'
                    })
                info.update({
                    'grams':int(variant.product_id.weight * 1000),
                    'weight':(variant.product_id.weight),
                    'weight_unit':'kg',
                })
                if variant.check_product_stock == 'parent_product':
                    if template.inventory_management == 'shopify':
                        info.update({'inventory_management':'shopify'})
                    else:
                        info.update({'inventory_management':None})
                elif variant.inventory_management == 'shopify':
                    info.update({'inventory_management':'shopify'})
                else:
                    info.update({'inventory_management':None})

                if variant.check_product_stock == 'parent_product':
                    if template.check_product_stock:
                        info.update({'inventory_policy':'continue'})
                    else:
                        info.update({'inventory_policy':'deny'})
                elif variant.check_product_stock == 'continue':
                    info.update({
                        'inventory_policy':'continue'
                    })
                else:
                    info.update({
                        'inventory_policy':'deny'
                    })
                info.update({
                    'requires_shipping':'true', 'sku':variant.default_code,
                    'taxable':template.taxable and 'true' or 'false',
                    'title':variant.name,
                })
                option_index = 0
                option_index_value = ['option1', 'option2', 'option3']
                attribute_value_obj = self.env['product.attribute.value']
                att_values = attribute_value_obj.search(
                        [('id', 'in', variant.product_id.attribute_value_ids.ids)],
                        order="attribute_id")
                for att_value in att_values:
                    info.update({option_index_value[option_index]:att_value.name})
                    option_index = option_index + 1
                    if option_index > 2:
                        break
                variants.append(info)
            new_product.variants = variants
            variants = []
            attribute_position = 1
            for attribute_line in template.product_tmpl_id.attribute_line_ids:
                info = {}
                attribute = attribute_line.attribute_id
                values = []
                value_ids = attribute_line.value_ids.ids
                for variant in template.shopify_product_ids:
                    for value in variant.product_id.attribute_value_ids:
                        if value.id in value_ids and value.id not in values:
                            values.append(value.id)
                value_names = []
                for value in self.env['product.attribute.value'].browse(values):
                    value_names.append(value.name)
                for value in attribute_line.value_ids:
                    if value.id not in values:
                        value_names.append(value.name)

                info.update({'name':attribute.shopify_name or attribute.name, 'values':value_names,
                             'position':attribute_position})
                variants.append(info)
                attribute_position = attribute_position + 1
                if attribute_position > 3:
                    break
            if variants:
                new_product.options = variants
            try:
                result = new_product.save()
            except Exception as e:
                if e.response.code == 429 and e.response.msg == "Too Many Requests":
                    time.sleep(5)
                    result = new_product.save()
            if result:
                result_dict = new_product.to_dict()
                created_at = result_dict.get('created_at')
                updated_at = result_dict.get('updated_at')
                published_at = result_dict.get('published_at')
                tmpl_id = result_dict.get('id')
                template.write({'created_at':created_at, 'updated_at':updated_at,
                                'published_at':published_at,
                                'shopify_tmpl_id':tmpl_id,
                                'exported_in_shopify':True,
                                'total_variants_in_shopify':len(result_dict.get('variants'))

                                })
                for variant_dict in result_dict.get('variants'):
                    updated_at = variant_dict.get('updated_at')
                    created_at = variant_dict.get('created_at')
                    variant_id = variant_dict.get('id')
                    sku = variant_dict.get('sku')
                    shopify_variant = self.env['shopify.product.product.ept'].search(
                            [('default_code', '=', sku), ('shopify_instance_id', '=', instance.id)])
                    shopify_variant and shopify_variant.write({
                        'variant_id':variant_id,
                        'updated_at':updated_at,
                        'created_at':created_at,
                        'exported_in_shopify':True
                    })
                # for image in image_with_position:
                #     for image_line in result_dict.get('images'):
                #         if image.get('position') == image_line.get('position'):
                #             image.get('variant').write({'shopify_image_id': image_line.get('id')})

                variants = []
                info = {}
                for variant in template.shopify_product_ids:
                    if variant.variant_id:
                        if variant.shopify_image_id:
                            info = {}
                            info.update(
                                    {'id':variant.variant_id, 'image_id':variant.shopify_image_id})
                            variants.append(info)
                new_product.id = template.shopify_tmpl_id
                new_product.variants = variants
                try:
                    new_product.save()
                except Exception as e:
                    if e.response.code == 429 and e.response.msg == "Too Many Requests":
                        time.sleep(5)
                        new_product.save()
        return True

    @api.multi
    def update_product_images(self, instance, shopify_template=False):
        if not shopify_template:
            return False
        instance.connect_in_shopify()
        for image in shopify_template.shopify_gallery_image_ids:
            if not image.image_id and not instance.is_image_url:
                continue
            shopify_image = False
            if image.shopify_image_id:
                try:
                    shopify_images = shopify.Image().find(
                            product_id=shopify_template.shopify_tmpl_id)
                except Exception as e:
                    if e.response.code == 429 and e.response.msg == "Too Many Requests":
                        time.sleep(5)
                        shopify_images = shopify.Image().find(
                                product_id=shopify_template.shopify_tmpl_id)
                if not shopify_images:
                    continue
                for shop_image in shopify_images:
                    if int(image.shopify_image_id) == shop_image.id:
                        shopify_image = shop_image
                        break
            else:
                shopify_image = shopify.Image()
            if not shopify_image:
                continue
            shopify_image.position = image.position
            shopify_image.product_id = shopify_template.shopify_tmpl_id
            shopify_image.variant_ids = [int(variant_id.variant_id) for variant_id in
                                         image.shopify_variant_ids]
            if instance.is_image_url:
                shopify_image.src = image.url
            else:
                shopify_image.attachment = image.image_id.decode('utf-8')
            if image.height > 0:
                shopify_image.height = image.height
            if image.width > 0:
                shopify_image.width = image.width
            try:
                result = shopify_image.save()
            except Exception as e:
                if e.response.code == 429 and e.response.msg == "Too Many Requests":
                    time.sleep(5)
                    result = shopify_image.save()
            if result:
                if instance.is_image_url:
                    image.url = shopify_image.src
                image.shopify_image_id = shopify_image.id
                image.height = shopify_image.height
                image.width = shopify_image.width
        return True

    @api.model
    def export_products_in_shopify(self, instance, templates, update_price, update_stock, publish,
                                   update_image):
        instance.connect_in_shopify()
        product_obj = product_obj = self.env['product.product']
        for template in templates:
            new_product = shopify.Product()
            if template.description:
                new_product.body_html = template.description
            if template.product_tmpl_id.seller_ids:
                new_product.vendor = template.product_tmpl_id.seller_ids[0].display_name
            new_product.product_type = template.shopify_product_category.name
            new_product.tags = [tag.name for tag in template.tag_ids]
            if template.template_suffix:
                new_product.template_suffix = template.template_suffix
            new_product.published = publish and 'true' or 'false'
            new_product.title = template.name
            variants = []
            info = {}
            for variant in template.shopify_product_ids:
                info = {}
                if variant.product_id.barcode:
                    info.update({'barcode':variant.product_id.barcode})
                if update_stock:
                    quantity = product_obj.get_stock_ept(variant.product_id,
                                                         instance.warehouse_id.id,
                                                         variant.fix_stock_type,
                                                         variant.fix_stock_value,
                                                         instance.stock_field.name)
                    info.update({'inventory_quantity':int(quantity)})
                if update_price:
                    price = instance.pricelist_id.get_product_price(variant.product_id, 1.0,
                                                                    partner=False,
                                                                    uom_id=variant.product_id.uom_id.id)
                    info.update({'price':float(price)})
                if template.fulfillment_service == 'manual':
                    info.update({'fulfillment_service':'manual'})
                info.update({
                    'grams':int(variant.product_id.weight * 1000),
                    'weight':(variant.product_id.weight),
                    'weight_unit':'kg',
                })
                if variant.check_product_stock == 'parent_product':
                    if template.inventory_management == 'shopify':
                        info.update({'inventory_management':'shopify'})
                    else:
                        info.update({'inventory_management':None})
                elif variant.inventory_management == 'shopify':
                    info.update({'inventory_management':'shopify'})
                else:
                    info.update({'inventory_management':None})

                if variant.check_product_stock == 'parent_product':
                    if template.check_product_stock:
                        info.update({'inventory_policy':'continue'})
                    else:
                        info.update({'inventory_policy':'deny'})
                elif variant.check_product_stock == 'continue':
                    info.update({
                        'inventory_policy':'continue'
                    })
                else:
                    info.update({
                        'inventory_policy':'deny'
                    })

                info.update({
                    'requires_shipping':'true', 'sku':variant.default_code,
                    'taxable':template.taxable and 'true' or 'false',
                    'title':variant.name,
                })
                option_index = 0
                option_index_value = ['option1', 'option2', 'option3']
                attribute_value_obj = self.env['product.attribute.value']
                att_values = attribute_value_obj.search(
                        [('id', 'in', variant.product_id.attribute_value_ids.ids)],
                        order="attribute_id")
                for att_value in att_values:
                    info.update({option_index_value[option_index]:att_value.name})
                    option_index = option_index + 1
                    if option_index > 2:
                        break
                variants.append(info)
            new_product.variants = variants
            variants = []
            attribute_position = 1
            product_attribute_line_obj = self.env['product.template.attribute.line']
            product_attribute_lines = product_attribute_line_obj.search(
                    [('id', 'in', template.product_tmpl_id.attribute_line_ids.ids)],
                    order="attribute_id")
            for attribute_line in product_attribute_lines:
                info = {}
                attribute = attribute_line.attribute_id
                values = []
                value_ids = attribute_line.value_ids.ids
                for variant in template.shopify_product_ids:
                    for value in variant.product_id.attribute_value_ids:
                        if value.id in value_ids and value.id not in values:
                            values.append(value.id)
                value_names = []
                for value in self.env['product.attribute.value'].browse(values):
                    value_names.append(value.name)
                for value in attribute_line.value_ids:
                    if value.id not in values:
                        value_names.append(value.name)

                info.update({'name':attribute.shopify_name or attribute.name, 'values':value_names,
                             'position':attribute_position})
                variants.append(info)
                attribute_position = attribute_position + 1
                if attribute_position > 3:
                    break
            new_product.options = variants
            try:
                result = new_product.save()
            except Exception as e:
                if e.response.code == 429 and e.response.msg == "Too Many Requests":
                    time.sleep(5)
                    result = new_product.save()
            if result:
                result_dict = new_product.to_dict()
                created_at = result_dict.get('created_at')
                updated_at = result_dict.get('updated_at')
                published_at = result_dict.get('published_at')
                tmpl_id = result_dict.get('id')
                template.write({'created_at':created_at, 'updated_at':updated_at,
                                'published_at':published_at,
                                'shopify_tmpl_id':tmpl_id,
                                'exported_in_shopify':True,
                                'total_variants_in_shopify':len(result_dict.get('variants'))
                                })
                for variant_dict in result_dict.get('variants'):
                    updated_at = variant_dict.get('updated_at')
                    created_at = variant_dict.get('created_at')
                    inventory_item_id = variant_dict.get('inventory_item_id')
                    variant_id = variant_dict.get('id')
                    sku = variant_dict.get('sku')
                    shopify_variant = self.env['shopify.product.product.ept'].search(
                            [('default_code', '=', sku), ('shopify_instance_id', '=', instance.id)])
                    shopify_variant and shopify_variant.write({
                        'variant_id':variant_id,
                        'updated_at':updated_at,
                        'created_at':created_at,
                        'inventory_item_id':inventory_item_id,
                        'exported_in_shopify':True
                    })
                variants = []
                info = {}
                for variant in template.shopify_product_ids:
                    if variant.variant_id:
                        if variant.shopify_image_id:
                            info = {}
                            info.update(
                                    {'id':variant.variant_id, 'image_id':variant.shopify_image_id})
                            variants.append(info)
                new_product.id = template.shopify_tmpl_id
                new_product.variants = variants
                try:
                    new_product.save()
                except Exception as e:
                    if e.response.code == 429 and e.response.msg == "Too Many Requests":
                        time.sleep(5)
                        new_product.save()
                if new_product and update_image:
                    self.update_product_images(instance, shopify_template=template)
            self._cr.commit()
        return True

    @api.model
    def import_stock(self, instance):
        transaction_log_obj = self.env['shopify.transaction.log']
        stock_inventory_line_obj = self.env["stock.inventory.line"]
        templates = self.search(
                [('shopify_instance_id', '=', instance.id), ('exported_in_shopify', '=', True)])
        invetory_adjustments = self.env['stock.inventory'].search(
                [('is_shopify_product_adjustment', '=', True), ('state', '!=', 'done')])
        inventory_id = False
        log = False
        for invetory_adjustment in invetory_adjustments:
            if not invetory_adjustment.state == 'cancel':
                invetory_adjustment.action_cancel_draft()
                invetory_adjustment.write({'state':'cancel'})
        if templates:
            instance.connect_in_shopify()
            location_ids = self.env['shopify.location.ept'].search(
                    [('legacy', '=', False), ('instance_id', '=', instance.id)])
            if not location_ids:
                message = "Location not found for instance %s while Import stock" % (instance.name)
                log = transaction_log_obj.search(
                        [('shopify_instance_id', '=', instance.id), ('message', '=', message)])
                if not log:
                    transaction_log_obj.create(
                            {'message':message,
                             'mismatch_details':True,
                             'type':'stock',
                             'shopify_instance_id':instance.id
                             })

                else:
                    log.write({'message':message})

                return False
            for location_id in location_ids:
                shopify_location_warehouse = location_id.warehouse_id or False
                if not shopify_location_warehouse:
                    message = "No Warehouse found for Import Stock in Shopify Location: %s" % (
                        location_id.name)
                    if not log:
                        transaction_log_obj.create(
                                {'message':message,
                                 'mismatch_details':True,
                                 'type':'stock',
                                 'shopify_instance_id':instance.id
                                 })
                    else:
                        log.write({'message':message})

                    continue
                inventory_id = self.env['stock.inventory'].create({
                    'name':'Inventory For Instance %s And Shopify Location %s' % (
                        (instance.name) + ' ' + datetime.now().strftime('%d-%m-%Y'),
                        location_id.name),
                    'location_id':location_id.warehouse_id.lot_stock_id.id,
                    'filter':'partial',
                    'is_shopify_product_adjustment':True
                })
                inventory_id.action_start()
                shopify_template_ids = []
                for template in templates:
                    shopify_template_ids.append(template.shopify_tmpl_id)
                shopify_template_ids = shopify_template_ids and ','.join(
                        shopify_template_ids) or False
                if not shopify_template_ids:
                    return False

                try:
                    inventory_levels = shopify.InventoryLevel.find(
                            location_ids=location_id.shopify_location_id)
                except Exception as e:
                    if e.response.code == 429 and e.response.msg == "Too Many Requests":
                        time.sleep(5)
                        inventory_levels = shopify.InventoryLevel.find(
                                location_ids=location_id.shopify_location_id)
                        continue
                    else:
                        #                 except Exception as e:
                        message = "Error while import stock for instance %s\nError: %s" % (
                            instance.name, str(e.response.code) + " " + e.response.msg)
                        log = transaction_log_obj.search(
                                [('shopify_instance_id', '=', instance.id),
                                 ('message', '=', message)])
                        if not log:
                            transaction_log_obj.create(
                                    {'message':message,
                                     'mismatch_details':True,
                                     'type':'stock',
                                     'shopify_instance_id':instance.id
                                     })

                        else:
                            log.write({'message':message})

                    return False

                if len(inventory_levels) >= 50:
                    inventory_levels = self.list_all_inventory(inventory_levels)

                for inventory_level in inventory_levels:
                    inventory_level = inventory_level.to_dict()
                    inventory_item_id = inventory_level.get('inventory_item_id')
                    qty = inventory_level.get('available')
                    shopify_product = self.env['shopify.product.product.ept'].search(
                            [('inventory_item_id', '=', inventory_item_id),
                             ('exported_in_shopify', '=', True),
                             ('shopify_instance_id', '=', instance.id)], limit=1)
                    if shopify_product:
                        stock_inventory_line_obj.create(
                                {"inventory_id":inventory_id.id,
                                 "product_id":shopify_product.product_id.id,
                                 "location_id":inventory_id.location_id.id, "product_qty":qty})
        if inventory_id:
            if inventory_id.line_ids:
                instance.inventory_adjustment_id = inventory_id.id
            else:
                inventory_id.unlink()
        return True

    def list_all_inventory(self, results):
        sum_inventory_list = []
        catch = ""
        while results:
            page_info = ""
            sum_inventory_list += results
            link = shopify.ShopifyResource.connection.response.headers.get('Link')
            if not link or not isinstance(link, str):
                return sum_inventory_list
            for page_link in link.split(','):
                if page_link.find('next') > 0:
                    page_info = page_link.split(';')[0].strip('<>').split('page_info=')[1]
                    try:
                        results = shopify.InventoryLevel.find(page_info=page_info, limit=250)
                    except Exception as e:
                        if e.response.code == 429 and e.response.msg == "Too Many Requests":
                            time.sleep(5)
                            results = shopify.InventoryLevel.find(page_info=page_info, limit=250)
                        else:
                            raise Warning(e)
            if catch == page_info:
                break
        return sum_inventory_list

    @api.model
    def auto_import_stock_ept(self):
        shopify_instance_objs = self.env['shopify.instance.ept'].search(
                [('state', '=', 'confirmed'), ('auto_import_stock', '=', True)])
        if shopify_instance_objs:
            for shopify_instance_obj in shopify_instance_objs:
                self.import_stock(instance=shopify_instance_obj)
        return True

class shopify_product_product_ept(models.Model):
    _name = "shopify.product.product.ept"
    _description = 'Shopify Product Product Ept'
    _order = 'sequence'

    producturl = fields.Text("Product URL")
    sequence = fields.Integer("Position", default=1)
    name = fields.Char("Title")
    shopify_instance_id = fields.Many2one("shopify.instance.ept", "Instance", required=1)
    default_code = fields.Char("Default Code")
    product_id = fields.Many2one("product.product", "Product", required=1)
    shopify_template_id = fields.Many2one("shopify.product.template.ept", "Shopify Template",
                                          required=1,
                                          ondelete="cascade")
    exported_in_shopify = fields.Boolean("Exported In Shopify")
    variant_id = fields.Char("Variant Id")
    fix_stock_type = fields.Selection([('fix', 'Fix'), ('percentage', 'Percentage')],
                                      string='Fix Stock Type')
    fix_stock_value = fields.Float(string='Fix Stock Value', digits=dp.get_precision("Product UoS"))
    created_at = fields.Datetime("Created At")
    updated_at = fields.Datetime("Updated At")
    shopify_image_id = fields.Char("Shopify Image Id")
    inventory_item_id = fields.Char("Inventory Item Id")
    # Added_by_Haresh Mori 31/01/2019
    check_product_stock = fields.Selection(
            [('continue', 'Allow'), ('deny', 'Denied'),
             ('parent_product', 'Set as a Product Template')],
            default='parent_product',
            help='If true than customers are allowed to place an order for the product variant when it is out of stock.')
    inventory_management = fields.Selection(
            [('shopify', 'Shopify tracks this product Inventory'),
             ('Dont track Inventory', 'Dont track Inventory'),
             ('parent_product', 'Set as a Product Template')],
            default='parent_product',
            help="If you select 'Shopify tracks this product Inventory' than shopify tracks this product inventory.if select 'Dont track Inventory' then after we can not update product stock from odoo")

class shopify_tags(models.Model):
    _name = "shopify.tags"
    _description = 'Shopify Tags'

    name = fields.Char("Name", required=1)
    sequence = fields.Integer("Sequence", required=1)

# class product_product(models.Model):
#     _inherit="product.product"
#     
#     @api.multi
#     def create_product_ept(self):
#         not_found=[]
#         for line in csv.reader(open('/tmp/product.csv','rb'),delimiter=',', quotechar='"'):      
#             self.create({'name':line[0],'default_code':line[1]})
#         return True
