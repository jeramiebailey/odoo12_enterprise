import time
from odoo import models,fields,api
from .. import shopify
from odoo.addons.shopify_ept.shopify.pyactiveresource.util import xml_to_dict

class res_partner(models.Model):
    _inherit="res.partner"
    
    company_name_ept=fields.Char("Company Of Name")
    shopify_customer_id=fields.Char("Shopify Cutstomer Id")

    @api.multi
    def list_all_customer(self,results):
        sum_cust_list = []
        catch = ""
        while results:
            page_info = ""
            sum_cust_list += results
            link = shopify.ShopifyResource.connection.response.headers.get('Link')
            if not link or not isinstance(link, str):
                return sum_cust_list
            for page_link in link.split(','):
                if page_link.find('next') > 0:
                    page_info = page_link.split(';')[0].strip('<>').split('page_info=')[1]
                    try:
                        results = shopify.Customer().search(page_info=page_info, limit=250)
                    except Exception as e:
                        if e.response.code == 429 and e.response.msg == "Too Many Requests":
                            time.sleep(5)
                            results = shopify.Customer().search(page_info=page_info, limit=250)
                        else:
                            raise Warning(e)
            if catch == page_info:
                break
        return sum_cust_list

    @api.model    
    def import_shopify_customers(self,instance=False):
        instances=[]
        instances.append(instance)
        sale_order_obj=self.env['sale.order']        
        for instance in instances:
            instance.connect_in_shopify()
            try:
                customer_ids = shopify.Customer().search(limit=250)
            except Exception as e:
                raise Warning(e)
            if len(customer_ids)>=250:
                customer_ids=self.list_all_customer(customer_ids)
            for customer_id in customer_ids:
                result=xml_to_dict(customer_id.to_xml())
                partner=result.get('customer',{}) and sale_order_obj.create_or_update_customer(result.get('customer',{}),True,False,False,instance) or False
        return True     
                 