from odoo import models, fields, api, _
import logging
import odoo.addons.decimal_precision as dp
from odoo.exceptions import UserError
from .. import shopify
from odoo.addons.shopify_ept.shopify.pyactiveresource.util import xml_to_dict
from datetime import datetime, timedelta
from odoo.addons.shopify_ept.shopify.resources import location
from dateutil import parser
import pytz

utc = pytz.utc
import time
_logger = logging.getLogger('======Shopify ===')


class sale_order(models.Model):
    _inherit = "sale.order"

    @api.one
    def _get_shopify_order_status(self):
        for order in self:
            flag = False
            for picking in order.picking_ids:
                if picking.state != 'cancel':
                    flag = True
                    break
            if not flag:
                continue
            if order.picking_ids:
                order.updated_in_shopify = True
            else:
                order.updated_in_shopify = False
            for picking in order.picking_ids:
                if picking.state == 'cancel':
                    continue
                if picking.picking_type_id.code != 'outgoing':
                    continue
                if not picking.updated_in_shopify:
                    order.updated_in_shopify = False
                    break

    @api.multi
    @api.depends('risk_ids')
    def _check_order(self):
        for order in self:
            flag = False
            for risk in order.risk_ids:
                if risk.recommendation != 'accept':
                    flag = True
                    break
            order.is_risky_order = flag

    def _search_order_ids(self, operator, value):
        query = """
                    select stock_picking.group_id from stock_picking
                    inner join stock_picking_type on stock_picking.picking_type_id=stock_picking_type.id
                    where coalesce(updated_in_shopify,False)=%s and stock_picking_type.code='%s' and state='%s'        
              """ % (False, 'outgoing', 'done')
        self._cr.execute(query)
        results = self._cr.fetchall()
        group_ids = []
        for result_tuple in results:
            group_ids.append(result_tuple[0])
        sale_ids = self.search([('procurement_group_id', 'in', group_ids)])
        return [('id', 'in', sale_ids.ids)]

    shopify_order_id = fields.Char("Shopify Order Ref")
    shopify_order_number = fields.Char("Shopify Order Number")
    shopify_reference_id = fields.Char("Shopify Reference")
    checkout_id = fields.Char("Checkout Id")
    auto_workflow_process_id = fields.Many2one("sale.workflow.process.ept", "Auto Workflow")
    updated_in_shopify = fields.Boolean("Updated In Shopify ?", compute=_get_shopify_order_status,
                                        search='_search_order_ids')
    shopify_instance_id = fields.Many2one("shopify.instance.ept", "Instance")
    closed_at_ept = fields.Datetime("Closed At")
    risk_ids = fields.One2many("shopify.order.risk", 'odoo_order_id', "Risks")
    is_risky_order = fields.Boolean("Risky Order ?", compute=_check_order, store=True)
    shopify_payment_gateway_id = fields.Many2one('shopify.payment.gateway',
                                                 string="Payment Gateway")
    shopify_location_id = fields.Char("Shopify Location Id")
    while_imoprt_order_shopify_status = fields.Char("Shopify Order Status",
                                                    help="Order Status While Import From Shopify")

    @api.multi
    def create_or_update_customer(self, vals, is_company=False, parent_id=False, type=False,
                                  instance=False):
        partner_obj = self.env['res.partner']
        if is_company:
            address = vals.get('default_address')
            if not address:
                address = vals

            customer_id = address.get('id') or address.get('customer_id')
            name = address.get('name') or "%s %s" % (vals.get('first_name'), vals.get('last_name'))
            company_name = address.get("company")
            email = vals.get('email')
            phone = address.get('phone')
            street = address.get('address1')
            city = address.get('city')

            partner_vals = {
                'name': name,
                'street': address.get('address1'),
                'street2': address.get('address2'),
                'city': address.get('city'),
                'state_code': address.get('province_code'),
                'state_name': address.get('province'),
                'country_code': address.get('country_code'),
                'country_name': address.get('country'),
                'phone': address.get('phone'),
                'email': vals.get('email'),
                'zip': address.get('zip'),
                'is_company': is_company,
            }

            partner_vals = partner_obj._prepare_partner_vals(partner_vals)
            if instance.shopify_property_account_payable_id:
                partner_vals.update(
                    {'property_account_payable_id': instance.shopify_property_account_payable_id.id,
                    })
            if instance.shopify_property_account_receivable_id:
                partner_vals.update(
                    {'property_account_receivable_id': instance.shopify_property_account_receivable_id.id})
            state_id = partner_vals.get('state_id')
            partner = partner_obj.search([('shopify_customer_id', '=', customer_id)], limit=1)
            domain = []
            if not partner:
                if vals.get('email'):
                    domain = [('email', '=', email)]
                elif phone:
                    domain = [('phone', '=', phone)]
                partner = partner_obj.search([('name', '=ilike', name), ('city', '=', city),
                                              ('street', '=', street), ('zip', '=', zip),
                                              ('state_id', '=', state_id)] + domain, limit=1,
                                             order="id desc")
            if partner:
                partner_vals.update({'property_payment_term_id': instance.payment_term_id.id,
                                     'company_name_ept': company_name})
                partner.write(partner_vals)
            else:
                partner_vals.update({'shopify_customer_id': customer_id,
                                     'property_payment_term_id': instance.payment_term_id.id,
                                     'property_product_pricelist': instance.pricelist_id.id,
                                     'property_account_position_id': instance.fiscal_position_id and instance.fiscal_position_id.id or False,
                                     'company_name_ept': company_name})
                partner = partner_obj.create(partner_vals)
            self._cr.commit()
            return partner
        else:
            company_name = vals.get("company")
            partner_vals = {
                'name': vals.get('name'),
                'street': vals.get('address1'),
                'street2': vals.get('address2'),
                'city': vals.get('city'),
                'state_code': vals.get('province_code'),
                'state_name': vals.get('province'),
                'country_code': vals.get('country_code'),
                'country_name': vals.get('country'),
                'phone': vals.get('phone'),
                'email': vals.get('email'),
                'zip': vals.get('zip'),
                'parent_id': parent_id,
                'type': type
            }
            partner_vals = partner_obj._prepare_partner_vals(partner_vals)
            if instance.shopify_property_account_payable_id:
                partner_vals.update(
                    {'property_account_payable_id': instance.shopify_property_account_payable_id.id,
                    })
            if instance.shopify_property_account_receivable_id:
                partner_vals.update(
                    {'property_account_receivable_id': instance.shopify_property_account_receivable_id.id})

            key_list = ['name', 'state_id', 'city', 'zip', 'street', 'street2', 'country_id']
            address = partner_obj._find_partner(partner_vals, key_list, [])
            if not address:
                partner_vals.update({'company_name_ept': company_name})
                address = partner_obj.create(partner_vals)
            self._cr.commit()
            return address

    @api.model
    def createAccountTax(self, value, price_included, company, title):
        accounttax_obj = self.env['account.tax']

        if price_included:
            name = '%s_(%s %s included)_%s' % (title, str(value), '%', company.name)
        else:
            name = '%s_(%s %s excluded)_%s' % (title, str(value), '%', company.name)

        accounttax_id = accounttax_obj.create(
            {'name': name, 'amount': float(value), 'type_tax_use': 'sale',
             'price_include': price_included, 'company_id': company.id})

        return accounttax_id

    @api.model
    def get_tax_id_ept(self, instance, order_line, tax_included):
        tax_id = []
        taxes = []
        for tax in order_line:
            rate = float(tax.get('rate', 0.0))
            rate = rate * 100
            if rate != 0.0:
                acctax_id = self.env['account.tax'].search(
                    [('price_include', '=', tax_included), ('type_tax_use', '=', 'sale'),
                     ('amount', '=', rate),
                     ('company_id', '=', instance.warehouse_id.company_id.id)], limit=1)
                if not acctax_id:
                    acctax_id = self.createAccountTax(rate, tax_included,
                                                      instance.warehouse_id.company_id,
                                                      tax.get('title'))
                    if acctax_id:
                        transaction_log_obj = self.env["shopify.transaction.log"]
                        message = """Tax was not found in ERP ||
                        Automatic Created Tax,%s ||
                        tax rate  %s ||
                        Company %s""" % (acctax_id.name, rate, instance.company_id.name)
                        transaction_log_obj.create(
                            {'message': message,
                             'mismatch_details': True,
                             'type': 'sales',
                             'shopify_instance_id': instance.id
                             })
                if acctax_id:
                    taxes.append(acctax_id.id)
        if taxes:
            tax_id = [(6, 0, taxes)]

        return tax_id

    @api.model
    def check_mismatch_details(self, lines, instance, order_number):
        transaction_log_obj = self.env["shopify.transaction.log"]
        odoo_product_obj = self.env['product.product']
        shopify_product_obj = self.env['shopify.product.product.ept']
        shopify_product_template_obj = self.env['shopify.product.template.ept']
        mismatch = False
        for line in lines:
            barcode = 0
            odoo_product = False
            shopify_variant = False
            if line.get('variant_id', None):
                shopify_variant = shopify_product_obj.search(
                    [('variant_id', '=', line.get('variant_id')),
                     ('shopify_instance_id', '=', instance.id)])
                if shopify_variant:
                    continue
                try:
                    shopify_variant = shopify.Variant().find(line.get('variant_id'))
                except:
                    shopify_variant = False
                    message = "Variant Id %s not found in shopify || default_code %s || order ref %s" % (
                        line.get('variant_id', None), line.get('sku'), order_number)
                    log = transaction_log_obj.search(
                        [('shopify_instance_id', '=', instance.id), ('message', '=', message)])
                    if not log:
                        transaction_log_obj.create(
                            {'message': message,
                             'mismatch_details': True,
                             'type': 'sales',
                             'shopify_instance_id': instance.id
                             })
                    else:
                        log.write({'message': message})

                if shopify_variant:
                    shopify_variant = shopify_variant.to_dict()
                    barcode = shopify_variant.get('barcode')
                else:
                    barcode = 0
            sku = line.get('sku')
            shopify_variant = barcode and shopify_product_obj.search(
                [('product_id.barcode', '=', barcode), ('shopify_instance_id', '=', instance.id)])
            if not shopify_variant:
                odoo_product = barcode and odoo_product_obj.search(
                    [('barcode', '=', barcode)]) or False
            if not odoo_product and not shopify_variant and sku:
                shopify_variant = sku and shopify_product_obj.search(
                    [('default_code', '=', sku), ('shopify_instance_id', '=', instance.id)])
                if not shopify_variant:
                    odoo_product = sku and odoo_product_obj.search([('default_code', '=', sku)])
            if not odoo_product:
                line_variant_id = line.get('variant_id', False)
                line_product_id = line.get('product_id', False)
                if line_product_id and line_variant_id:
                    odoo_product = False
                    shopify_product_template_obj.sync_products(instance,
                                                               shopify_tmpl_id=line_product_id)
                    odoo_product = odoo_product_obj.search([('default_code', '=', sku)], limit=1)
            if not shopify_variant and not odoo_product:
                message = "%s Product Code Not found for order %s" % (sku, order_number)
                log = transaction_log_obj.search(
                    [('shopify_instance_id', '=', instance.id), ('message', '=', message)])
                if not log:
                    transaction_log_obj.create(
                        {'message': message,
                         'mismatch_details': True,
                         'type': 'sales',
                         'shopify_instance_id': instance.id
                         })
                else:
                    log.write({'message': message})

                mismatch = True
                break
        return mismatch

    @api.model
    def create_sale_order_line(self, line, product, quantity, name, order_id, price,
                               order_response, is_shipping=False):
        sale_order_line_obj = self.env['sale.order.line']

        uom_id = product and product.uom_id and product.uom_id.id or False
        line_vals = {
            'product_id': product and product.ids[0] or False,
            'order_id': order_id.id,
            'company_id': order_id.company_id.id,
            'product_uom': uom_id,
            'name': name,
            'price_unit': price,
            'order_qty': quantity,
        }
        order_line_vals = sale_order_line_obj.create_sale_order_line_ept(line_vals)
        if order_id.shopify_instance_id.apply_tax_in_order == 'create_shopify_tax':
            taxes_included = order_response.get('taxes_included') or False
            tax_ids = []
            if line and line.get('tax_lines'):
                if line.get('taxable'):
                    # This is used for when the one product is taxable and another product is not
                    # taxable
                    tax_ids = self.shopify_get_tax_id_ept(order_id.shopify_instance_id, line.get('tax_lines'),
                                                          taxes_included)
                if is_shipping:
                    # In the Shopify store there is configuration regarding tax is applicable on shipping or not, if applicable then this use.
                    tax_ids = self.shopify_get_tax_id_ept(order_id.shopify_instance_id,
                                                          line.get('tax_lines'),
                                                          taxes_included)
            elif not line:
                if order_id.shopify_instance_id.add_discount_tax:
                    tax_ids = self.shopify_get_tax_id_ept(order_id.shopify_instance_id,
                                                          order_response.get('tax_lines'),
                                                          taxes_included)
            order_line_vals["tax_id"] = tax_ids

        else:
            if is_shipping and not line.get("tax_lines", []):
                order_line_vals["tax_id"] = []

        order_line_vals.update({
            'shopify_line_id': line.get('id'),
            'is_delivery': is_shipping
        })
        order_line = sale_order_line_obj.with_context({'round':False}).create(order_line_vals)
        return order_line

    @api.model
    def shopify_get_tax_id_ept(self, instance, tax_lines, tax_included):
        """This method used to search tax in Odoo.
            @param : self,instance,order_line,tax_included
            @return: tax_id
            @author: Haresh Mori @Emipro Technologies Pvt. Ltd on date 18/11/2019.
            Task Id : 157350
        """
        tax_id = []
        taxes = []
        for tax in tax_lines:
            rate = float(tax.get('rate', 0.0))
            rate = rate * 100
            if rate != 0.0:
                acctax_id = self.env['account.tax'].search(
                    [('price_include', '=', tax_included), ('type_tax_use', '=', 'sale'),
                     ('amount', '=', rate),
                     ('company_id', '=', instance.warehouse_id.company_id.id)], limit=1)
                if not acctax_id:
                    acctax_id = self.shopify_create_account_tax(instance, rate, tax_included,
                                                                instance.warehouse_id.company_id,
                                                                tax.get('title'))
                if acctax_id:
                    taxes.append(acctax_id.id)
        if taxes:
            tax_id = [(6, 0, taxes)]
        return tax_id

    @api.model
    def shopify_create_account_tax(self, instance, value, price_included, company, title):
        """This method used to create tax in Odoo when importing orders from Shopify to Odoo.
            @param : self, value, price_included, company, title
            @return: account_tax_id
            @author: Haresh Mori @Emipro Technologies Pvt. Ltd on date 18/11/2019.
            Task Id : 157350
        """
        account_tax_obj = self.env['account.tax']
        if price_included:
            name = '%s_(%s %s included)_%s' % (title, str(value), '%', company.name)
        else:
            name = '%s_(%s %s excluded)_%s' % (title, str(value), '%', company.name)

        account_tax_id = account_tax_obj.create(
            {'name': name, 'amount': float(value), 'type_tax_use': 'sale',
             'price_include': price_included, 'company_id': company.id})
        return account_tax_id

    @api.model
    def create_or_update_product(self, line, instance):
        shopify_product_tmpl_obj = self.env['shopify.product.template.ept']
        shopify_product_obj = self.env['shopify.product.product.ept']
        variant_id = line.get('variant_id')
        shopify_product = False
        if variant_id:
            shopify_product = shopify_product_obj.search(
                [('shopify_instance_id', '=', instance.id), ('variant_id', '=', variant_id)])
            if shopify_product:
                return shopify_product
            shopify_product = shopify_product_obj.search(
                [('shopify_instance_id', '=', instance.id), ('default_code', '=', line.get('sku'))])
            shopify_product and shopify_product.write({'variant_id': variant_id})
            if shopify_product:
                return shopify_product
            line_product_id = line.get('product_id')
            if line_product_id:
                shopify_product_tmpl_obj.sync_products(instance, shopify_tmpl_id=line_product_id,
                                                       update_templates=True)
            shopify_product = shopify_product_obj.search(
                [('shopify_instance_id', '=', instance.id), ('variant_id', '=', variant_id)])
        else:
            shopify_product = shopify_product_obj.search(
                [('shopify_instance_id', '=', instance.id), ('default_code', '=', line.get('sku'))])
            if shopify_product:
                return shopify_product
        return shopify_product

    @api.model
    def create_order(self, result, invoice_address, instance, partner, shipping_address,
                     pricelist_id, fiscal_position, payment_term):
        shopify_payment_gateway = False
        no_payment_gateway = False
        payment_term_id = False
        #       Added by Priya Pal
        #       For : If no payment gateway is found in result.get('gateway') then it default set no_payment_gateway as gateway.
        #       Guided By : Dhaval Bhalani Sir
        gateway = result.get('gateway', '') or "no_payment_gateway"
        if gateway:
            shopify_payment_gateway = self.env['shopify.payment.gateway'].search(
                [('code', '=', gateway), ('shopify_instance_id', '=', instance.id)], limit=1)
            if not shopify_payment_gateway:
                shopify_payment_gateway = self.env['shopify.payment.gateway'].create(
                    {'name': gateway, 'code': gateway, 'shopify_instance_id': instance.id})
        if not shopify_payment_gateway:
            no_payment_gateway = self.verify_order(instance, result)
            if not no_payment_gateway:
                transaction_log_obj = self.env["shopify.transaction.log"]
                message = "Payment Gateway not found for this order %s and financial status is %s" % (
                    result.get('name'), result.get('financial_status'))
                log = transaction_log_obj.search(
                    [('shopify_instance_id', '=', instance.id), ('message', '=', message)])
                if not log:
                    transaction_log_obj.create({'message': message,
                                                'mismatch_details': True,
                                                'type': 'sales', 'shopify_instance_id': instance.id
                                                })
                else:
                    log.write({'message': message})

                return False

        workflow = False
        if not no_payment_gateway and shopify_payment_gateway:
            workflow_config = self.env['sale.auto.workflow.configuration'].search(
                [('shopify_instance_id', '=', instance.id),
                 ('payment_gateway_id', '=', shopify_payment_gateway.id),
                 ('financial_status', '=', result.get('financial_status'))])
            workflow = workflow_config and workflow_config.auto_workflow_id or False
            if workflow_config:
                payment_term_id = workflow_config.payment_term_id and workflow_config.payment_term_id.id or False
                if not payment_term_id:
                    payment_term_id = instance.payment_term_id.id or False
                    if payment_term_id:
                        partner.write({'property_payment_term_id': payment_term_id})

        if not workflow and not no_payment_gateway:
            transaction_log_obj = self.env["shopify.transaction.log"]
            message = "Workflow Configuration not found for this order %s and payment gateway is %s and financial status is %s" % (
                result.get('name'), gateway, result.get('financial_status'))
            log = transaction_log_obj.search(
                [('shopify_instance_id', '=', instance.id), ('message', '=', message)])
            if not log:
                transaction_log_obj.create(
                    {'message': message,
                     'mismatch_details': True,
                     'type': 'sales', 'shopify_instance_id': instance.id
                     })

            else:
                log.write({'message': message})
            return False

            # This method call the prepared dictionary for the new sale order and return dictionary
        if result.get('created_at', False):
            order_date = result.get('created_at', False)
            date_order = parser.parse(order_date).astimezone(utc).strftime('%Y-%m-%d %H:%M:%S')
        else:
            date_order = time.strftime('%Y-%m-%d %H:%M:%S')
            date_order = str(date_order)
        ordervals = {
            'company_id': instance.company_id.id,
            'partner_id': partner.ids[0],
            'partner_invoice_id': invoice_address.ids[0],
            'partner_shipping_id': shipping_address.ids[0],
            'warehouse_id': instance.warehouse_id.id,
            'fiscal_position_id': fiscal_position and fiscal_position.id or False,
            'date_order': date_order,
            'state': 'draft',
            'pricelist_id': pricelist_id or instance.pricelist_id.id or False,
            'team_id': instance.section_id and instance.section_id.id or False,
        }
        ordervals = self.create_sales_order_vals_ept(ordervals)

        ordervals.update({
            'checkout_id': result.get('checkout_id'),
            'note': result.get('note'),
            'shopify_order_id': result.get('id'),
            'shopify_order_number': result.get('order_number'),
            'shopify_payment_gateway_id': shopify_payment_gateway and shopify_payment_gateway.id or False,
            'shopify_instance_id': instance.id,
            'global_channel_id': instance.global_channel_id and instance.global_channel_id.id or False,
            'while_imoprt_order_shopify_status': result.get('fulfillment_status'),
            'client_order_ref':result.get('name'),
        })
        # Add by Haresh Mori on Date 31_1_2019
        # Take changes for while order import use odoo default sequence base on configuration
        if not instance.is_use_default_sequence:
            if instance.order_prefix:
                name = "%s_%s" % (instance.order_prefix, result.get('name'))
            else:
                name = result.get('name')
            ordervals.update({'name': name})

        if workflow:
            ordervals.update({
                'picking_policy': workflow.picking_policy,
                'auto_workflow_process_id': workflow.id,
                'payment_term_id': payment_term_id and payment_term_id or payment_term or False,
                'invoice_policy': workflow.invoice_policy or False
            })
        order = self.create(ordervals)
        return order

    @api.model
    def verify_order(self, instance, order):
        payment_method = order.get("gateway", '')
        total = order.get("total_price", 0)

        if order.get('total_discounts', 0.0):
            discount = order.get('total_discounts', 0)

        if not payment_method and float(total) == 0 and float(discount) > 0:
            return True
        else:
            return False

    @api.model
    def check_fulfilled_or_not(self, result):
        fulfilled = True
        for line in result.get('line_items'):
            if not line.get('fulfillment_status'):
                fulfilled = False
                break
        return fulfilled

    @api.multi
    def list_all_orders(self, results):
        sum_order_list = []
        catch = ""
        while results:
            page_info = ""
            sum_order_list += results
            link = shopify.ShopifyResource.connection.response.headers.get('Link')
            if not link or not isinstance(link, str):
                return sum_order_list
            for page_link in link.split(','):
                if page_link.find('next') > 0:
                    page_info = page_link.split(';')[0].strip('<>').split('page_info=')[1]
                    try:
                        results = shopify.Order().find(limit=250, page_info=page_info)
                    except Exception as e:
                        if e.response.code == 429 and e.response.msg == "Too Many Requests":
                            time.sleep(5)
                            results = shopify.Order().find(limit=250, page_info=page_info)
                        else:
                            raise Warning(e)
            if catch == page_info:
                break
        return sum_order_list

    @api.model
    def auto_import_sale_order_ept(self, ctx={}):
        shopify_instance_obj = self.env['shopify.instance.ept']
        if not isinstance(ctx, dict) or not 'shopify_instance_id' in ctx:
            return True
        shopify_instance_id = ctx.get('shopify_instance_id', False)
        if shopify_instance_id:
            instance = shopify_instance_obj.search(
                [('id', '=', shopify_instance_id), ('state', '=', 'confirmed')])
            if not instance:
                return True
            from_date = instance and instance.last_date_order_import
            to_date = datetime.now()
            self.import_shopify_orders(from_date, to_date, instance)
        return True

    @api.model
    def import_shopify_orders(self, from_date, to_date, instance=False):
        order_risk_obj = self.env['shopify.order.risk']
        shopify_location_obj = self.env['shopify.location.ept']
        instances = []
        if not instance:
            instances = self.env['shopify.instance.ept'].search(
                [('order_auto_import', '=', True), ('state', '=', 'confirmed')])
        else:
            instances.append(instance)
        for instance in instances:
            # While changes primary location so base on instance it call location import
            shopify_location_obj.import_shopify_locations(instance)
            instance.connect_in_shopify()
            if not from_date:
                from_date = datetime.now() - timedelta(days=3)
            if not to_date:
                to_date = datetime.now()
            # from_date = datetime.strptime(pytz.utc.localize(from_date).astimezone(
            #         pytz.timezone(instance.shopify_store_time_zone[12:] or 'UTC')).strftime(
            #         '%Y-%m-%d %H:%M:%S'), "%Y-%m-%d %H:%M:%S")
            # to_date = datetime.strptime(pytz.utc.localize(to_date).astimezone(
            #         pytz.timezone(instance.shopify_store_time_zone[12:] or 'UTC')).strftime(
            #         '%Y-%m-%d %H:%M:%S'), "%Y-%m-%d %H:%M:%S")
            instance.last_date_order_import = to_date
            for status in instance.import_shopify_order_status_ids:
                shopify_fulfillment_status = status.status
                if shopify_fulfillment_status == 'any' or shopify_fulfillment_status == 'shipped':
                    try:
                        order_ids = shopify.Order().find(status='any',
                                                         fulfillment_status=shopify_fulfillment_status,
                                                         created_at_min=from_date,
                                                         created_at_max=to_date, limit=250)
                    except Exception as e:
                        raise Warning(e)
                    if len(order_ids) >= 50:
                        order_ids = self.list_all_orders(order_ids)
                else:
                    try:
                        order_ids = shopify.Order().find(
                            fulfillment_status=shopify_fulfillment_status, created_at_min=from_date,
                            created_at_max=to_date, limit=250)
                    except Exception as e:
                        raise Warning(e)
                    if len(order_ids) >= 50:
                        order_ids = self.list_all_orders(order_ids)

                import_order_ids = []
                transaction_log_obj = self.env["shopify.transaction.log"]
                _logger.info("Total len of import orders: {0} for instance:{1} ".format(len(order_ids),instance.name))
                for order_id in order_ids:
                    result = xml_to_dict(order_id.to_xml())
                    result = result.get('order')
                    _logger.info("START processing of order id: {0} and order number is: {""1}".format(result.get('id'),result.get('order_number')))
                    if self.search([('shopify_order_id', '=', result.get('id')),
                                    ('shopify_instance_id', '=', instance.id),
                                    ('shopify_order_number', '=', result.get('order_number'))]):
                        continue

                    if self.search([('shopify_instance_id', '=', instance.id),
                                    ('client_order_ref', '=', result.get('name'))]):
                        continue

                    partner = result.get('customer', {}) and self.create_or_update_customer(
                        result.get('customer', {}), True, False, False, instance) or False
                    if not partner:
                        message = "Customer Not Available In %s Order" % (
                            result.get('order_number'))
                        log = transaction_log_obj.search(
                            [('shopify_instance_id', '=', instance.id), ('message', '=', message)])
                        if not log:
                            transaction_log_obj.create(
                                {'message': message,
                                 'mismatch_details': True,
                                 'type': 'sales',
                                 'shopify_instance_id': instance.id
                                 })
                        else:
                            log.write({'message': message})
                        continue
                    shipping_address = result.get('shipping_address',
                                                  False) and self.create_or_update_customer(
                        result.get('shipping_address'), False, partner.id, 'delivery',
                        instance) or partner
                    invoice_address = result.get('billing_address',
                                                 False) and self.create_or_update_customer(
                        result.get('billing_address'), False, partner.id, 'invoice',
                        instance) or partner

                    lines = result.get('line_items')
                    if self.check_mismatch_details(lines, instance, result.get('order_number')):
                        continue

                    new_record = self.new({'partner_id': partner.id})
                    new_record.onchange_partner_id()
                    partner_result = self._convert_to_write(
                        {name: new_record[name] for name in new_record._cache})

                    fiscal_position = partner.property_account_position_id
                    pricelist_id = partner_result.get('pricelist_id', False)
                    payment_term = partner_result.get(
                        'payment_term_id') or instance.payment_term_id.id or False
                    shopify_location_id = result.get('location_id') or False
                    log = False
                    if not shopify_location_id:
                        shopify_location = shopify_location_obj.search(
                            [('is_primary_location', '=', True), ('instance_id', '=', instance.id)],
                            limit=1)
                    else:
                        shopify_location = shopify_location_obj.search(
                            [('shopify_location_id', '=', shopify_location_id),
                             ('instance_id', '=', instance.id)], limit=1)
                        shopify_location_warehouse = shopify_location.warehouse_id or False
                        if not shopify_location_warehouse:
                            message = "No Warehouse found for Import Order: %s in Shopify Location %s" % (
                                result.get('order_number'), shopify_location.name)
                            if not log:
                                transaction_log_obj.create(
                                    {'message': message,
                                     'mismatch_details': True,
                                     'type': 'sales',
                                     'shopify_instance_id': instance.id
                                     })
                            else:
                                log.write({'message': message})
                            continue
                    order = self.create_order(result, invoice_address, instance, partner,
                                              shipping_address, pricelist_id, fiscal_position,
                                              payment_term)
                    if not order:
                        continue
                    order.write({'shopify_location_id': shopify_location.shopify_location_id})
                    risk_result = shopify.OrderRisk().find(order_id=order_id.id)
                    flag = False
                    for line in lines:
                        shopify_product = self.create_or_update_product(line, instance)
                        if not shopify_product:
                            flag = True
                            break
                        product_url = shopify_product and shopify_product.producturl or False
                        if product_url:
                            line.update({'product_url': product_url})
                        product = shopify_product.product_id
                        self.create_sale_order_line(line, product, line.get('quantity'),
                                                    product.name, order, line.get('price'),
                                                    result)
                    if flag:
                        order.unlink()
                        continue
                    if not risk_result:
                        import_order_ids.append(order.id)
                    elif order_risk_obj.create_risk(risk_result, order):
                        import_order_ids.append(order.id)
                    total_discount = result.get('total_discounts', 0.0)
                    if float(total_discount) > 0.0:
                        self.create_sale_order_line({}, instance.discount_product_id, 1,
                                                    instance.discount_product_id.name, order,
                                                    float(total_discount) * -1, result)

                    product_template_obj = self.env['product.template']
                    for line in result.get('shipping_lines', []):
                        delivery_method = line.get('title')
                        if delivery_method:
                            carrier = self.env['delivery.carrier'].search(
                                [('shopify_code', '=', delivery_method)], limit=1)
                            if not carrier:
                                carrier = self.env['delivery.carrier'].search(
                                    ['|', ('name', '=', delivery_method),
                                     ('shopify_code', '=', delivery_method)], limit=1)
                            if not carrier:
                                carrier = self.env['delivery.carrier'].search(
                                    ['|', ('name', 'ilike', delivery_method),
                                     ('shopify_code', 'ilike', delivery_method)], limit=1)
                            if not carrier:
                                product_template = product_template_obj.search(
                                    [('name', '=', delivery_method), ('type', '=', 'service')],
                                    limit=1)
                                if not product_template:
                                    product_template = product_template_obj.create(
                                        {'name': delivery_method, 'type': 'service'})
                                carrier = self.env['delivery.carrier'].create(
                                    {'name': delivery_method, 'shopify_code': delivery_method,
                                     'partner_id': self.env.user.company_id.partner_id.id,
                                     'product_id': product_template.product_variant_ids[0].id})
                            order.write({'carrier_id': carrier.id})
                            if carrier.product_id:
                                shipping_product = carrier.product_id
                        self.create_sale_order_line(line, shipping_product, 1,
                                                    shipping_product and shipping_product.name or line.get(
                                                        'title'), order, line.get('price'), result,
                                                    is_shipping=True)
                if import_order_ids:
                    self.env['sale.workflow.process.ept'].with_context({'round':False}).auto_workflow_process(
                        ids=import_order_ids)
        return True

    @api.multi
    def action_invoice_create(self, grouped=False, final=False):
        if self.shopify_instance_id :
            return super(sale_order, self.with_context(round=False)).action_invoice_create(
                grouped=grouped, final=final)
        else :
            return super(sale_order, self).action_invoice_create(
                grouped=grouped, final=final)

    @api.model
    def closed_at(self, instances):
        for instance in instances:
            if not instance.auto_closed_order:
                continue
            warehouse_ids = self.env['shopify.location.ept'].search(
                [('instance_id', '=', instance.id)]).mapped('warehouse_id')
            if not warehouse_ids:
                warehouse_ids = instance.warehouse_id
            sales_orders = self.search([('warehouse_id', 'in', warehouse_ids.ids),
                                        ('shopify_order_id', '!=', False),
                                        ('shopify_instance_id', '=', instance.id),
                                        ('state', '=', 'done'), ('closed_at_ept', '=', False)],
                                       order='date_order')

            instance.connect_in_shopify()

            for sale_order in sales_orders:
                order = shopify.Order.find(sale_order.shopify_order_id)
                order.close()
                sale_order.write({'closed_at_ept': datetime.now()})
        return True

    @api.model
    def auto_update_order_status_ept(self, ctx={}):
        shopify_instance_obj = self.env['shopify.instance.ept']
        if not isinstance(ctx, dict) or not 'shopify_instance_id' in ctx:
            return True
        shopify_instance_id = ctx.get('shopify_instance_id', False)
        if shopify_instance_id:
            instance = shopify_instance_obj.search([('id', '=', shopify_instance_id)])
            self.update_order_status(instance)
        return True

    @api.model
    def update_order_status(self, instance):
        move_line_obj = self.env['stock.move.line']
        transaction_log_obj = self.env["shopify.transaction.log"]
        log = False
        instances = []
        if not instance:
            instances = self.env['shopify.instance.ept'].search(
                [('order_auto_import', '=', True), ('state', '=', 'confirmed')])
        else:
            instances.append(instance)
        for instance in instances:
            instance.connect_in_shopify()
            warehouse_ids = self.env['shopify.location.ept'].search(
                [('instance_id', '=', instance.id)]).mapped('warehouse_id')
            if not warehouse_ids:
                warehouse_ids = instance.warehouse_id
            sales_orders = self.search([('warehouse_id', 'in', warehouse_ids.ids),
                                        ('shopify_order_id', '!=', False),
                                        ('shopify_instance_id', '=', instance.id),
                                        ('updated_in_shopify', '=', False)], order='date_order')

            for sale_order in sales_orders:
                notify_customer = instance.notify_customer
                try:
                    order = shopify.Order.find(sale_order.shopify_order_id)
                except Exception as e:
                    if e.response.code == 429 and e.response.msg == "Too Many Requests":
                        time.sleep(5)
                        order = shopify.Order.find(sale_order.shopify_order_id)
                    else:
                        return Warning(e)
                        # Getting only those picking has state is done, Not updated in shopify and location destination id user is customer, Added By Prakash Makwana Dated on : 26, April 2019 and guided by Dhaval Sir.
                picking_ids = sale_order.picking_ids.filtered(lambda
                                                                  p: p.updated_in_shopify == False and p.state == 'done' and p.location_dest_id.usage == 'customer')
                for picking in picking_ids:
                    """Here We Take only done picking and  updated in shopify false"""
                    if picking.updated_in_shopify or picking.state != 'done':
                        continue

                    order_lines = picking.sale_id.order_line
                    if order_lines and order_lines.filtered(
                            lambda s: s.product_id.type != 'service' and s.shopify_line_id == False or ''):
                        transaction_log_obj.create(
                            {
                                'message': "Order status is not updated for order %s because shopify line id not found in this order." % picking.sale_id.name,
                                'mismatch_details': True,
                                'type': 'sales',
                                'shopify_instance_id': instance.id
                            })
                        continue

                    line_items = {}
                    list_of_tracking_number = []
                    tracking_numbers = []
                    carrier_name = picking.carrier_id and picking.carrier_id.shopify_code or ''
                    if not carrier_name:
                        carrier_name = picking.carrier_id and picking.carrier_id.name or ''
                    for move in picking.move_lines:
                        if move.sale_line_id and move.sale_line_id.shopify_line_id:
                            shopify_line_id = move.sale_line_id.shopify_line_id

                        """Create Package for the each parcel"""
                        move_line = move_line_obj.search(
                            [('move_id', '=', move.id), ('product_id', '=', move.product_id.id)],
                            limit=1)
                        tracking_no = False
                        if sale_order.shopify_instance_id.multiple_tracking_number:
                            if move_line.result_package_id.tracking_no:
                                tracking_no = move_line.result_package_id.tracking_no
                            if (move_line.package_id and move_line.package_id.tracking_no):
                                tracking_no = move_line.package_id.tracking_no
                        else:
                            tracking_no = picking.carrier_tracking_ref or False

                        tracking_no and list_of_tracking_number.append(tracking_no)
                        product_qty = move_line.qty_done or 0.0
                        product_qty = int(product_qty)
                        if shopify_line_id in line_items:
                            if 'tracking_no' in line_items.get(shopify_line_id):
                                quantity = line_items.get(shopify_line_id).get('quantity')
                                quantity = quantity + product_qty
                                line_items.get(shopify_line_id).update({'quantity': quantity})
                                if tracking_no not in line_items.get(shopify_line_id).get(
                                        'tracking_no'):
                                    line_items.get(shopify_line_id).get('tracking_no').append(
                                        tracking_no)
                            else:
                                line_items.get(shopify_line_id).update({'tracking_no': []})
                                line_items.get(shopify_line_id).update({'quantity': product_qty})
                                line_items.get(shopify_line_id).get('tracking_no').append(
                                    tracking_no)
                        else:
                            line_items.update({shopify_line_id: {}})
                            line_items.get(shopify_line_id).update({'tracking_no': []})
                            line_items.get(shopify_line_id).update({'quantity': product_qty})
                            line_items.get(shopify_line_id).get('tracking_no').append(tracking_no)

                    update_lines = []
                    for sale_line_id in line_items:
                        tracking_numbers += line_items.get(sale_line_id).get('tracking_no')
                        update_lines.append({'id': sale_line_id,
                                             'quantity': line_items.get(sale_line_id).get(
                                                 'quantity')})
                    if not update_lines:
                        message = "No lines found for update order status for %s" % (picking.name)
                        log = transaction_log_obj.search(
                            [('shopify_instance_id', '=', instance.id), ('message', '=', message)])
                        if not log:
                            transaction_log_obj.create(
                                {'message': message,
                                 'mismatch_details': True,
                                 'type': 'sales',
                                 'shopify_instance_id': instance.id
                                 })
                        else:
                            log.write({'message': message})
                        continue
                    try:
                        shopify_location_id = sale_order.shopify_location_id or False
                        if not shopify_location_id:
                            location_id = self.env['shopify.location.ept'].search(
                                [('is_primary_location', '=', True),
                                 ('instance_id', '=', instance.id)])
                            shopify_location_id = location_id.shopify_location_id or False
                            if not location_id:
                                message = "Primary Location not found for instance %s while Update order status" % (
                                    instance.name)
                                if not log:
                                    transaction_log_obj.create(
                                        {'message': message,
                                         'mismatch_details': True,
                                         'type': 'stock',
                                         'shopify_instance_id': instance.id
                                         })
                                else:
                                    log.write({'message': message})
                                continue
                        #                         new_fulfillment = shopify.Fulfillment({'order_id':order.id,'location_id':shopify_location_id,'tracking_numbers':list(set(tracking_numbers)),'tracking_company':carrier_name,'line_items':update_lines,'notify_customer':notify_customer})
                        try:
                            new_fulfillment = shopify.Fulfillment(
                                {'order_id': order.id, 'location_id': shopify_location_id,
                                 'tracking_numbers': list(set(tracking_numbers)),
                                 'tracking_company': carrier_name, 'line_items': update_lines,
                                 'notify_customer': notify_customer})

                        except Exception as e:
                            if e.response.code == 429 and e.response.msg == "Too Many Requests":
                                time.sleep(5)
                                new_fulfillment = shopify.Fulfillment(
                                    {'order_id': order.id, 'location_id': shopify_location_id,
                                     'tracking_numbers': list(set(tracking_numbers)),
                                     'tracking_company': carrier_name, 'line_items': update_lines,
                                     'notify_customer': notify_customer})
                        #                                 continue
                        try:
                            fulfillment_result = new_fulfillment.save()
                        except Exception as e:
                            if e.response.code == 429 and e.response.msg == "Too Many Requests":
                                time.sleep(5)
                                fulfillment_result = new_fulfillment.save()
                        if not fulfillment_result:
                            message = "Order(%s) status not updated due to some issue in fulfillment request/response:" % (
                                sale_order.name)
                            if not log:
                                transaction_log_obj.create(
                                    {'message': message,
                                     'mismatch_details': True,
                                     'type': 'stock',
                                     'shopify_instance_id': instance.id
                                     })
                            else:
                                log.write({'message': message})
                            continue
                    except Exception as e:
                        message = "%s" % (e)
                        if not log:
                            transaction_log_obj.create(
                                {'message': message,
                                 'mismatch_details': True,
                                 'type': 'stock',
                                 'shopify_instance_id': instance.id
                                 })
                        else:
                            log.write({'message': message})
                        continue
                    picking.write({'updated_in_shopify': True})
        self.closed_at(instances)
        return True

    @api.multi
    def update_carrier(self):
        instances = self.env['shopify.instance.ept'].search([('state', '=', 'confirmed')])
        for instance in instances:
            instance.connect_in_shopify()
            try:
                order_ids = shopify.Order().find()
            except Exception as e:
                raise Warning(e)
            if len(order_ids) >= 50:
                order_ids = self.list_all_orders(order_ids)
            for order_id in order_ids:
                result = xml_to_dict(order_id.to_xml())
                result = result.get('order')
                odoo_order = self.search([('shopify_order_id', '=', result.get('id')), (
                    'shopify_order_number', '=', result.get('order_number'))])
                if odoo_order:
                    for line in odoo_order.order_line:
                        if line.product_id.type == 'service':
                            shipping_product = instance.shipment_charge_product_id
                            for line in result.get('shipping_lines', []):
                                delivery_method = line.get('code')
                                if delivery_method:
                                    carrier = self.env['delivery.carrier'].search(
                                        ['|', ('name', '=', delivery_method),
                                         ('shopify_code', '=', delivery_method)])
                                    if not carrier:
                                        carrier = self.env['delivery.carrier'].create(
                                            {'name': delivery_method,
                                             'shopify_code': delivery_method,
                                             'partner_id': self.env.user.company_id.partner_id.id,
                                             'product_id': shipping_product.id})
                                    odoo_order.write({'carrier_id': carrier.id})
                                    odoo_order.picking_ids.write({'carrier_id': carrier.id})
            return True

    @api.multi
    def delivery_set(self):
        if self.shopify_order_id:
            raise UserError(
                _('You are not allow to change manually shipping charge in Shopify order.'))
        else:
            super(sale_order, self).delivery_set()


class sale_order_line(models.Model):
    _inherit = "sale.order.line"

    shopify_line_id = fields.Char("Shopify Line")

    @api.multi
    def unlink(self):
        """
        @author: Haresh Mori on date:3/05/2018
        """
        for record in self:
            if record.order_id.shopify_order_id:
                msg = _(
                    "You can not delete this line because this line is Shopify order line and we need Shopify line id while we are doing update order status")
                raise UserError(msg)
        return super(sale_order_line, self).unlink()


class import_shopify_order_status(models.Model):
    _name = "import.shopify.order.status"
    _description = 'Order Status'

    name = fields.Char("Name")
    status = fields.Char("Status")
