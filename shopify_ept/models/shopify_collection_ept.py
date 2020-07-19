from odoo import models, fields, api
import urllib
import base64
from .. import shopify
import time
from datetime import datetime


class shopify_collection_ept(models.Model):
    _name = "shopify.collection.ept"
    _description = 'Shopify Collection ept'

    @api.model
    def get_default_value(self):
        if self._context.get('process') == 'smart_collection':
            return True
        else:
            return False

    disjunctive = fields.Boolean("Disjunctive", default=False, help="If false, products must match all of the rules to be included in the collection. If true, products can only match one of the rules.")
    name = fields.Char("Title", required=True)
    body_html = fields.Html("Body")
    image_id = fields.Binary("Image")
    is_smart_collection = fields.Boolean("Boolean Collection", default=get_default_value)
    shopify_collection_id = fields.Char("Shopify Id", copy=False)
    published = fields.Boolean('Published', copy=False)
    exported_in_shopify = fields.Boolean("Exported In Shopify", copy=False)
    published_at = fields.Datetime("Published At", copy=False)
    sort_order = fields.Selection([('alpha-asc', 'Alphabetically, in ascending order (A - Z)'),
                                 ('alpha-desc', 'Alphabetically, in descending order (Z - A)'),
                                 ('best-selling', 'By best-selling products'),
                                 ('created', 'By date created, in ascending order (oldest - newest)'),
                                 ('created-desc', 'By date created, in descending order (newest - oldest)'),
                                 ('manual', 'Order created by the shop owner'),
                                 ('price-asc', 'By price, in ascending order (lowest - highest)'),
                                 ('price-desc', 'By price, in descending order (highest - lowest)')
                                 ])
    template_suffix = fields.Char("Template Suffix")
    created_at = fields.Datetime("Created At", copy=False)
    updated_at = fields.Datetime("Updated At", copy=False)
    handle = fields.Char("Handle")
    shopify_instance_id = fields.Many2one("shopify.instance.ept", 'Shopify Instance', required=True)
    shopify_template_ids = fields.Many2many("shopify.product.template.ept", "shopify_collet_tmpl_rel", "collect_id", "template_id", "Shopify Templates")
    rule_ids = fields.One2many("smart.collection.rules.ept", 'collection_id', "Rules")

    @api.multi  
    def shopify_unpublished(self):
        instance = self.shopify_instance_id
        instance.connect_in_shopify()
        if self.shopify_collection_id:
            if self.is_smart_collection:
                new_collection = shopify.SmartCollection.find(self.shopify_collection_id)
            else:
                new_collection = shopify.CustomCollection.find(self.shopify_collection_id)
            new_collection.id = self.shopify_collection_id
            new_collection.published = 'false'
            new_collection.published_at = None
            try:
                result = new_collection.save()
            except Exception as e:
                if e.response.code == 429 and e.response.msg == "Too Many Requests":
                    time.sleep(5)
                    result = new_collection.save()
            if result:
                result_dict = new_collection.to_dict()
                updated_at = result_dict.get('updated_at')
                self.write({'updated_at':updated_at, 'published_at':False, 'published':False})
        return True

    @api.multi
    def shopify_published(self):
        instance = self.shopify_instance_id
        instance.connect_in_shopify()
        if self.shopify_collection_id:
            if self.is_smart_collection:
                try:
                    new_collection = shopify.SmartCollection.find(self.shopify_collection_id)
                except Exception as e:
                    if e.response.code == 429 and e.response.msg == "Too Many Requests":
                        time.sleep(5)
                        new_collection = shopify.SmartCollection.find(self.shopify_collection_id)
                    else:
                        return Warning(e)
            else:
                try:
                    new_collection = shopify.CustomCollection.find(self.shopify_collection_id)
                except Exception as e:
                    if e.response.code == 429 and e.response.msg == "Too Many Requests":
                        time.sleep(5)
                        new_collection = shopify.CustomCollection.find(self.shopify_collection_id)
                    else:
                        return Warning(e)

            new_collection.published = 'true'
            new_collection.id = self.shopify_collection_id
            published_at = datetime.utcnow() 
            published_at = published_at.strftime("%Y-%m-%dT%H:%M:%S")
            new_collection.published_at = published_at
            try:
                result = new_collection.save()
            except Exception as e:
                if e.response.code == 429 and e.response.msg == "Too Many Requests":
                    time.sleep(5)
                    result = new_collection.save()
            if result:
                result_dict = new_collection.to_dict()
                updated_at = result_dict.get('updated_at')
                published_at = result_dict.get('published_at')
                self.write({'updated_at':updated_at, 'published_at':published_at, 'published':True})
        return True

    @api.multi
    def export_custom_collection(self, instance, collections, publish):
        instance.connect_in_shopify()
        for collection in collections:
            custom_collection = {}
            new_collection = shopify.CustomCollection()
            custom_collection.update({'title':collection.name})
            if collection.template_suffix:
                custom_collection.update({'template_suffix':collection.template_suffix or None})
            if collection.sort_order:
                custom_collection.update({'sort_order':collection.sort_order or None})
            if collection.body_html:
                custom_collection.update({'body_html':collection.body_html or None})
            if collection.image_id:
                custom_collection.update({'image':{'attachment':collection.image_id.decode('utf-8') or None}})            
            if not publish:
                custom_collection.update({'published':False})            
            collects = []
            for template in collection.shopify_template_ids:
                collects.append({'product_id':template.shopify_tmpl_id})
            custom_collection.update({'collects':collects})

            # new_collection.custom_collection=custom_collection
            res = new_collection.create(custom_collection)
            result = res.to_dict()   
            if result:
                collection_id = result.get('id') 
                published_at = result.get('published_at', False)
                updated_at = result.get('updated_at', False)
                handle = result.get('handle', False)
                collection.write({'handle':handle,
                                  'updated_at':updated_at,
                                  'published_at':published_at,
                                  'shopify_collection_id':collection_id,
                                  'exported_in_shopify':True,
                                  'published':publish
                                  })
        return True

    @api.model
    def get_already_exist_products(self, products):
        product_ids = []
        for product in products:
            product_ids.append(str(product.id))
        return product_ids

    @api.multi
    def update_custom_collection(self, instance, collections):
        instance.connect_in_shopify()
        for collection in collections:
            try:
                new_collection = shopify.CustomCollection().find(collection.shopify_collection_id)
            except Exception as e:
                if e.response.code == 429 and e.response.msg == "Too Many Requests":
                    time.sleep(5)
                    new_collection = shopify.CustomCollection().find(collection.shopify_collection_id)                
            if not new_collection:
                continue
            new_collection.title = collection.name
            if collection.template_suffix:
                new_collection.template_suffix = collection.template_suffix
            if collection.sort_order:
                new_collection.sort_order = collection.sort_order
            if collection.body_html:
                new_collection.body_html = collection.body_html

            if collection.image_id:
                new_collection.image = {'attachment':collection.image_id.decode('utf-8') or None}

            collects = []
            exist_templates = self.get_already_exist_products(new_collection.products())
            odoo_templates = []
            for template in collection.shopify_template_ids:
                odoo_templates.append(template.shopify_tmpl_id)
                if template.shopify_tmpl_id not in exist_templates:
                    collects.append({'product_id':template.shopify_tmpl_id})
            new_collection.collects = collects
            try:
                res = new_collection.save()
            except Exception as e:
                if e.response.code == 429 and e.response.msg == "Too Many Requests":
                    time.sleep(5)
                    res = new_collection.save()
            remove_templates = list(set(exist_templates) - set(odoo_templates))
            for template in remove_templates:
                if template not in odoo_templates:
                    new_collection.remove_product(shopify.Product().find(template))
            result = new_collection.to_dict()   
            if result:
                collection_id = result.get('id') 
                published_at = result.get('published_at', False)
                updated_at = result.get('updated_at', False)
                handle = result.get('handle', False)
                if published_at:
                    publish = True
                else:
                    publish = False
                collection.write({'handle':handle,
                                  'updated_at':updated_at,
                                  'published_at':published_at,
                                  'shopify_collection_id':collection_id,
                                  'exported_in_shopify':True,
                                  'published':publish
                                  })

    @api.multi
    def list_all_custom_collections(self, results):
        sum_collection_list = []
        catch = ""
        while results:
            page_info = ""
            sum_collection_list += results
            link = shopify.ShopifyResource.connection.response.headers.get('Link')
            if not link or not isinstance(link, str):
                return sum_collection_list
            for page_link in link.split(','):
                if page_link.find('next') > 0:
                    page_info = page_link.split(';')[0].strip('<>').split('page_info=')[1]
                    try:
                        results = shopify.CustomCollection().find(page_info=page_info, limit=250)
                    except Exception as e:
                        if e.response.code == 429 and e.response.msg == "Too Many Requests":
                            time.sleep(5)
                            results = shopify.CustomCollection().find(page_info=page_info, limit=250)
                        else:
                            raise Warning(e)
            if catch == page_info:
                break
        return sum_collection_list

    @api.multi
    def list_all_smart_collections(self, results):
        sum_collection_list = []
        catch = ""
        while results:
            page_info = ""
            sum_collection_list += results
            link = shopify.ShopifyResource.connection.response.headers.get('Link')
            if not link or not isinstance(link, str):
                return sum_collection_list
            for page_link in link.split(','):
                if page_link.find('next') > 0:
                    page_info = page_link.split(';')[0].strip('<>').split('page_info=')[1]
                    try:
                        results = shopify.SmartCollection().find(page_info=page_info, limit=250)
                    except Exception as e:
                        if e.response.code == 429 and e.response.msg == "Too Many Requests":
                            time.sleep(5)
                            results = shopify.SmartCollection().find(page_info=page_info, limit=250)
                        else:
                            raise Warning(e)
            if catch == page_info:
                break
        return sum_collection_list

    @api.multi
    def import_collection(self, instance):
        shopify_product_tmpl_obj = self.env['shopify.product.template.ept']
        transaction_log_obj = self.env["shopify.transaction.log"]
        smart_collection_rule_obj = self.env['smart.collection.rules.ept']

        instance.connect_in_shopify()
        try:
            collections = shopify.CustomCollection().find(limit=250)
        except Exception as e:
            if e.response.code == 429 and e.response.msg == "Too Many Requests":
                time.sleep(5)
                collections = shopify.CustomCollection().find(limit=250)
            else:
                raise Warning(e)
        if len(collections) >= 250:
            collections = self.list_all_custom_collections(collections)
        for collection in collections:
            result = collection.to_dict()
            collection_id = result.get('id')
            template_suffix = result.get('template_suffix')
            handle = result.get('handle')
            title = result.get('title')
            image = result.get('image', {}).get('src')
            body_html = result.get('body_html')
            created_at = result.get('created_at')
            updated_at = result.get('updated_at')
            published_at = result.get('published_at')
            sort_order = result.get('sort_order')
            img = False
            try:  
                (filename, header) = urllib.request.urlretrieve(image)
                with open(filename , 'rb') as f:
                    img = base64.b64encode(f.read())    
            except Exception:
                img = False
                pass
            if published_at:
                published = True
            else:
                published = False
            vals = {'template_suffix':template_suffix, 'handle':handle,
                                       'name':title, 'body_html':body_html,
                                       'created_at':created_at, 'updated_at':updated_at, 'sort_order':sort_order,
                                       'image_id':img, 'published':published, 'published_at':published_at, 'shopify_collection_id':collection_id,
                                       'shopify_instance_id':instance.id, 'exported_in_shopify':True
                                       }
            odoo_collection = self.search([('shopify_collection_id', '=', collection_id), ('shopify_instance_id', '=', instance.id)], limit=1)
            if odoo_collection:
                odoo_collection.write(vals)
            else:
                odoo_collection = self.create(vals)
            shopify_products = []
            for product in collection.products():
                shopify_product = shopify_product_tmpl_obj.search([('shopify_tmpl_id', '=', str(product.id)), ('shopify_instance_id', '=', instance.id)])
                if not shopify_product:
                    shopify_product_tmpl_obj.sync_products(instance, shopify_tmpl_id=str(product.id))
                    shopify_product = shopify_product_tmpl_obj.search([('shopify_tmpl_id', '=', str(product.id)), ('shopify_instance_id', '=', instance.id)])
                if not shopify_product:
                    message = "Product %s not found for a collection %s " % (product.id, collection_id)
                    log = transaction_log_obj.search([('shopify_instance_id', '=', instance.id), ('message', '=', message)])                    
                    if not log:
                        transaction_log_obj.create(
                                                    {'message':message,
                                                     'mismatch_details':True,
                                                     'type':'collection',
                                                     'shopify_instance_id':instance.id
                                                    })
                    else:
                        log.write({'message':message})
                else:
                    shopify_products.append(str(product.id))
            shopify_templates = shopify_product_tmpl_obj.search([('shopify_tmpl_id', 'in', shopify_products), ('shopify_instance_id', '=', instance.id)])
            odoo_collection.write({'shopify_template_ids':[(6, 0, shopify_templates.ids)]})
            self._cr.commit()

        try:
            smart_collections = shopify.SmartCollection().find(limit=250)
        except Exception as e:
            if e.response.code == 429 and e.response.msg == "Too Many Requests":
                time.sleep(5)
                smart_collections = shopify.SmartCollection().find(limit=250)
            else:
                raise Warning(e)
        if len(smart_collections) >= 250:
            smart_collections = self.list_all_smart_collections(smart_collections)
        for smart_collection in smart_collections:
            result = smart_collection.to_dict()
            collection_id = result.get('id')
            template_suffix = result.get('template_suffix')
            handle = result.get('handle')
            title = result.get('title')
            image = result.get('image', {}).get('src')
            body_html = result.get('body_html')
            created_at = result.get('created_at')
            updated_at = result.get('updated_at')
            published_at = result.get('published_at')
            sort_order = result.get('sort_order')
            rules = result.get('rules')
            total_shopify_rules = len(rules)
            disjunctive = result.get('disjunctive')
            img = False
            try:  
                (filename, header) = urllib.request.urlretrieve(image)
                with open(filename , 'rb') as f:
                    img = base64.b64encode(f.read())    
            except Exception:
                img = False
                pass
            if published_at:
                published = True
            else:
                published = False
            vals = {'template_suffix':template_suffix, 'handle':handle,
                                       'name':title, 'body_html':body_html,
                                       'created_at':created_at, 'updated_at':updated_at, 'sort_order':sort_order,
                                       'image_id':img, 'published':published, 'published_at':published_at, 'shopify_collection_id':collection_id,
                                       'shopify_instance_id':instance.id, 'exported_in_shopify':True, 'is_smart_collection':True, 'disjunctive':disjunctive,
                                       }
            odoo_collection = self.search([('shopify_collection_id', '=', collection_id), ('shopify_instance_id', '=', instance.id)], limit=1)            
            if not odoo_collection:
                odoo_collection = self.create(vals) 
            else:
                odoo_collection.write(vals)                
            mismatch = False
            
            if not len(odoo_collection.rule_ids.ids) == total_shopify_rules:
                mismatch = True
            if not mismatch:
                for rule in rules:
                    column_name = rule.get('column')
                    relation = rule.get('relation')
                    condition = rule.get('condition')                    
                    smart_collection_record = smart_collection_rule_obj.search([('column_name', '=', column_name), ('relation', '=', relation), ('condition', '=', condition), ('collection_id', '=', odoo_collection.id)])
                    if not smart_collection_record:
                        smart_collection_record = smart_collection_rule_obj.search([('column_name', '=', column_name), ('relation', '=', relation), ('collection_id', '=', odoo_collection.id)])
                        if smart_collection_record:
                            smart_collection_record.write({'condition':condition})
                        else:
                            mismatch = True
                            break                
            if mismatch:
                odoo_collection.rule_ids.unlink()
                for rule in rules:
                    column_name = rule.get('column')
                    relation = rule.get('relation')
                    condition = rule.get('condition')
                    smart_collection_rule_obj.create({'column_name':column_name, 'relation':relation, 'condition':condition, 'collection_id':odoo_collection.id})
            self._cr.commit()
        return True

    @api.multi
    def export_smart_collection(self, instance, collections, publish):
        instance.connect_in_shopify()
        for collection in collections:
            smart_collection = {}
            new_collection = shopify.SmartCollection()
            smart_collection.update({'title':collection.name})
            if collection.template_suffix:
                smart_collection.update({'template_suffix':collection.template_suffix or None})
            if collection.sort_order:
                smart_collection.update({'sort_order':collection.sort_order or None})
            if collection.body_html:
                smart_collection.update({'body_html':collection.body_html or None})
            if collection.image_id:
                smart_collection.update({'image':{'attachment':collection.image_id.decode('utf-8') or None}})            
            if not publish:
                smart_collection.update({'published':False})            
            smart_collection.update({'disjunctive':collection.disjunctive})            
            rules = []
            for rule in collection.rule_ids:
                rules.append({'column':rule.column_name, 'relation':rule.relation, 'condition':rule.condition})
            smart_collection.update({'rules':rules})

            # new_collection.custom_collection=custom_collection
            res = new_collection.create(smart_collection)
            if res.errors.errors:
                errors = ""
                for key, value in res.errors.errors.items():
                    errors += "\n%s : %s" % (key, value)
                message = "Collection - %s can not be exported.\nError from Shopify : %s " % (collection.name, errors)
                self.env["shopify.transaction.log"].create({"message":message,
                                                            "mismatch_details":True,
                                                            "type":"collection",
                                                            "shopify_instance_id":instance.id
                                                            })
                continue

            result = res.to_dict()
            if result.get('id'):
                collection_id = result.get('id') 
                published_at = result.get('published_at', False)
                updated_at = result.get('updated_at', False)
                handle = result.get('handle', False)
                collection.write({'handle':handle,
                                  'updated_at':updated_at,
                                  'published_at':published_at,
                                  'shopify_collection_id':collection_id,
                                  'exported_in_shopify':True,
                                  'published':publish
                                  })
        return True

    @api.multi
    def update_smart_collection(self, instance, collections):
        instance.connect_in_shopify()
        for collection in collections:
            try:
                new_collection = shopify.SmartCollection().find(collection.shopify_collection_id)
            except Exception as e:
                if e.response.code == 429 and e.response.msg == "Too Many Requests":
                    time.sleep(5)
                    new_collection = shopify.SmartCollection().find(collection.shopify_collection_id)

            if not new_collection:
                continue
            new_collection.title = collection.name
            if collection.template_suffix:
                new_collection.template_suffix = collection.template_suffix
            if collection.sort_order:
                new_collection.sort_order = collection.sort_order
            if collection.body_html:
                new_collection.body_html = collection.body_html

            if collection.image_id:
                new_collection.image = {'attachment':collection.image_id.decode('utf-8') or None}

            new_collection.disjunctive = collection.disjunctive and 'true' or 'false'
            rules = []
            for rule in collection.rule_ids:
                rules.append({'column':rule.column_name, 'relation':rule.relation, 'condition':rule.condition})
            new_collection.rules = rules
            try:
                new_collection.save()
            except Exception as e:
                if e.response.code == 429 and e.response.msg == "Too Many Requests":
                    time.sleep(5)
                    new_collection.save()
            result = new_collection.to_dict()   
            if result:
                collection_id = result.get('id') 
                published_at = result.get('published_at', False)
                if published_at:
                    publish = True
                else:
                    publish = False
                updated_at = result.get('updated_at', False)
                handle = result.get('handle', False)
                collection.write({'handle':handle,
                                  'updated_at':updated_at,
                                  'published_at':published_at,
                                  'shopify_collection_id':collection_id,
                                  'exported_in_shopify':True,
                                  'published':publish
                                  })


class smart_collection_rules_ept(models.Model):
    _name = "smart.collection.rules.ept"
    _description = 'Smart Collection Rules Ept'

    column_name = fields.Selection([('title', 'Product title'), ('type', 'Product type'),
                                  ('vendor', 'Product vendor'), ('variant_price', 'Product price'),
                                  ('tag', 'Product tag'), ('variant_compare_at_price', 'Compare at price'),
                                  ('variant_weight', 'Weight'), ('variant_inventory', 'Inventory stock'),
                                  ('variant_title', 'Variant Title')
                                  ], string="Collection", default='title')
    relation = fields.Selection([('equals', 'Equals'), ('not_equals', 'Not Equals'), ('greater_than', 'Is Greater Than'),
                               ('less_than', 'Is Less Than'), ('starts_with', 'Starts With'), ('ends_with', 'Ends With'),
                               ('contains', 'Contains'), ('not_contains', 'Not Contains')
                               ], string="Relation", default='equals')
    condition = fields.Char("Condition")
    collection_id = fields.Many2one("shopify.collection.ept", string="Collections")
