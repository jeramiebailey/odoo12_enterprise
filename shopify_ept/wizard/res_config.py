from odoo import models, fields, api, _
from odoo.exceptions import Warning
from .. import shopify
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

_intervalTypes = {
    'work_days':lambda interval:relativedelta(days=interval),
    'days':lambda interval:relativedelta(days=interval),
    'hours':lambda interval:relativedelta(hours=interval),
    'weeks':lambda interval:relativedelta(days=7 * interval),
    'months':lambda interval:relativedelta(months=interval),
    'minutes':lambda interval:relativedelta(minutes=interval),
}

class shopify_instance_config(models.TransientModel):
    _name = 'res.config.shopify.instance'
    _description = 'Res Config Shopify Instance'

    name = fields.Char("Instance Name")
    api_key = fields.Char("API Key", required=True)
    password = fields.Char("Password", required=True)
    shared_secret = fields.Char("Secret Key", required=True)
    host = fields.Char("Host", required=True)
    shopify_country_id = fields.Many2one('res.country', string="Country", required=True)
    is_image_url = fields.Boolean("Is Image URL?",
                                  help="Check this if you use Images from URL\nKeep as it is if you use Product images")
    apply_tax_in_order = fields.Selection(
            [("odoo_tax", "Odoo Default Tax Behaviour"), ("create_shopify_tax",
                                                          "Create new tax if not found")],
            copy=False,default='create_shopify_tax', help=""" For Shopify Orders :- \n
                    1) Odoo Default Tax Behaviour - The Taxes will be set based on Odoo's
                                 default functional behaviour i.e. based on Odoo's Tax and Fiscal Position configurations. \n
                    2) Create New Tax If Not Found - System will search the tax data received 
                    from Shopify in Odoo, will create a new one if it fails in finding it.""")
    invoice_tax_account_id = fields.Many2one('account.account', string='Invoice Tax '
                                                                       'Account')
    credit_tax_account_id = fields.Many2one('account.account', string='Credit Tax Account')

    @api.multi
    def test_shopify_connection(self):
        shop = self.host.split("//")
        if len(shop) == 2:
            shop_url = shop[0] + "//" + self.api_key + ":" + self.password + "@" + shop[
                1] + "/admin/api/2020-01"
        else:
            shop_url = "https://" + self.api_key + ":" + self.password + "@" + shop[0] + "/admin/api/2020-01"
        shopify.ShopifyResource.set_site(shop_url)
        try:
            shop_id = shopify.Shop.current()
        except Exception as e:
            raise Warning(e)

        shop_detail = shop_id.to_dict()
        shop_currency = shop_detail.get('currency')
        currency_obj = self.env['res.currency']
        currency_id = currency_obj.search([('name', '=', shop_currency)], limit=1)
        if not currency_id:
            currency_id = currency_obj.search(
                    [('name', '=', shop_currency), ('active', '=', False)], limit=1)
            currency_id.write({'active':True})
        if not currency_id:
            currency_id = self.env.user.currency_id
        warehouse_id = self.env['stock.warehouse'].search(
                [('company_id', '=', self.env.user.company_id.id)], limit=1)
        discount_product = self.env.ref('shopify_ept.product_product_id')
        account_term_id = self.env.ref('account.account_payment_term_immediate')
        pricelist_obj = self.env['product.pricelist']
        ir_model_obj = self.env['ir.model.fields']
        sale_team_obj = self.env['crm.team']
        global_channel_obj = self.env['global.channel.ept']
        res_lang_obj = self.env['res.lang']
        instance_obj = self.env['shopify.instance.ept']
        instance_id = instance_obj.search([('api_key', '=', self.api_key)], limit=1)
        if instance_id:
            raise Warning('This instance is already exist')
        res_lang_id = res_lang_obj.search([('code', '=', self.env.user.lang)], limit=1)
        global_channel_id = global_channel_obj.search([('name', '=', self.name)], limit=1)
        if not global_channel_id:
            global_channel_id = global_channel_obj.create({'name':self.name})
        sale_team_id = sale_team_obj.search(
                [('name', '=', self.name), ('user_id', '=', self.env.user.id)], limit=1)
        if not sale_team_id:
            sale_team_id = sale_team_obj.create({'name':self.name,
                                                 'user_id':self.env.user.id})
        stock_fields_id = ir_model_obj.search(
                [('model_id.model', '=', 'product.product'), ('name', '=', 'virtual_available')],
                limit=1)
        price_list_name = self.name + ' ' + 'PriceList'
        pricelist_id = pricelist_obj.search(
                [('name', '=', price_list_name), ('currency_id', '=', currency_id.id)], limit=1)
        if not pricelist_id:
            pricelist_id = pricelist_obj.create({'name':price_list_name,
                                                 'currency_id':currency_id.id
                                                 })
        import_shopify_order_status_obj = self.env['import.shopify.order.status']
        import_order_status = import_shopify_order_status_obj.search([('status', '=', 'unshipped')],
                                                                     limit=1)
        today = datetime.today()
        last_date_order_import = today + timedelta(days=-3)

        vals = {'name':self.name,
                'api_key':self.api_key,
                'password':self.password,
                'shared_secret':self.shared_secret,
                'host':self.host,
                'shopify_country_id':self.shopify_country_id.id,
                'company_id':self.env.user.company_id.id,
                'is_image_url':self.is_image_url,
                'warehouse_id':warehouse_id.id or False,
                # 'self.env.user.lang':True,
                'is_set_price':True,
                'is_set_stock':True,
                'is_set_image':True,
                'sync_images_with_product':True,
                'import_price':True,
                'add_discount_tax':True,
                'auto_closed_order':True,
                'notify_customer':True,
                'notify_by_email_while_cancel_picking':True,
                'notify_by_email_while_refund':True,
                'restock_in_shopify':True,
                'discount_product_id':discount_product.id or False,
                'pricelist_id':pricelist_id.id or False,
                'stock_field':stock_fields_id.id or False,
                'payment_term_id':account_term_id.id or False,
                'section_id':sale_team_id.id or False,
                'global_channel_id':global_channel_id.id or False,
                'lang_id':res_lang_id.id or False,
                'import_shopify_order_status_ids':[(6, 0, import_order_status.ids)],
                'last_date_order_import':last_date_order_import,
                'country_id':self.shopify_country_id.id,
                'apply_tax_in_order':self.apply_tax_in_order,
                'invoice_tax_account_id':self.invoice_tax_account_id.id if
                self.invoice_tax_account_id else False,
                'credit_tax_account_id':self.credit_tax_account_id.id if
                self.credit_tax_account_id else False,
                }
        shopify_instance_id = self.env['shopify.instance.ept'].create(vals)

        return {
            'type':'ir.actions.client',
            'tag':'reload',
        }

class ResConfigSettings(models.TransientModel):
    #    _name = 'shopify.config.settings'
    _inherit = 'res.config.settings'

    # @api.model
    # def _default_instance(self):
    #     instances = self.env['shopify.instance.ept'].search([])
    #     return instances and instances[0].id or False

    @api.model
    def create(self, vals):
        if not vals.get('company_id'):
            vals.update({'company_id':self.env.user.company_id.id})
        res = super(ResConfigSettings, self).create(vals)
        return res

    @api.model
    def _get_default_company(self):
        company_id = self.env.user._get_company()
        if not company_id:
            raise Warning(_('There is no default company for the current user!'))
        return company_id

    notify_customer = fields.Boolean("Notify Customer about Update Order Status?",
                                     help="If checked,Notify the customer via email about Update Order Status")
    notify_by_email_while_cancel_picking = fields.Boolean("Notify Customer about Cancel Picking?",
                                                          help="If checked,Notify the customer via email about Order Cancel")
    notify_by_email_while_refund = fields.Boolean("Notify Customer about Refund?",
                                                  help="If checked,Notify the customer via email about Refund")
    restock_in_shopify = fields.Boolean("Restock In Shopify ?",
                                        help="If checked,Restock In Shopify while refund")
    shopify_multiple_tracking_number = fields.Boolean(
            string='One order can have multiple Tracking Number ?', default=False)
    shopify_instance_id = fields.Many2one('shopify.instance.ept', 'Instance')
    shopify_warehouse_id = fields.Many2one('stock.warehouse', string="Warehouse")
    product_id = fields.Many2one('product.product', string="Product")
    # company_id = fields.Many2one('res.company',string='Company',default=_get_default_company,help="Orders and Invoices will be generated of this company.")
    shopify_company_id = fields.Many2one('res.company', string='Shopify Company',
                                         default=_get_default_company,
                                         help="Orders and Invoices will be generated of this company.")
    shopify_country_id = fields.Many2one('res.country', string="Country")
    shopify_lang_id = fields.Many2one('res.lang', string='Language')
    shopify_order_prefix = fields.Char(size=10, string='Order Prefix')
    add_discount_tax = fields.Boolean("Calculate Discount Tax", default=False)
    shopify_order_auto_import = fields.Boolean(string='Auto Order Import?')
    shopify_order_auto_update = fields.Boolean(string="Auto Update Order Status?")
    shopify_stock_auto_export = fields.Boolean(string="Stock Auto Export?")
    import_price = fields.Boolean(string="Import/Sync Price?", default=False)

    shopify_stock_field = fields.Many2one('ir.model.fields', string='Stock Field')

    shopify_pricelist_id = fields.Many2one('product.pricelist', string='Pricelist')
    shopify_payment_term_id = fields.Many2one('account.payment.term', string='Payment Term')

    shopify_discount_product_id = fields.Many2one("product.product", "Discount",
                                                  domain=[('type', '=', 'service')], required=False)

    shopify_fiscal_position_id = fields.Many2one('account.fiscal.position',
                                                 string='Fiscal Position')

    auto_closed_order = fields.Boolean("Auto Closed Order", Default=False)

    shopify_section_id = fields.Many2one('crm.team', 'Sales Team')
    shopify_global_channel_id = fields.Many2one('global.channel.ept', string="Global Channel")
    shopify_inventory_export_interval_number = fields.Integer('Export stock Interval Number',
                                                              help="Repeat every x.")
    shopify_inventory_export_interval_type = fields.Selection([('minutes', 'Minutes'),
                                                               ('hours', 'Hours'),
                                                               ('work_days', 'Work Days'),
                                                               ('days', 'Days'), ('weeks', 'Weeks'),
                                                               ('months', 'Months')],
                                                              'Export Stock Interval Unit')
    shopify_inventory_export_next_execution = fields.Datetime('Next Execution',
                                                              help='Next execution time')
    shopify_inventory_export_user_id = fields.Many2one('res.users', string="User", help='User',
                                                       default=lambda self:self.env.user)

    shopify_order_import_interval_number = fields.Integer('Import Order Interval Number',
                                                          help="Repeat every x.")
    shopify_order_import_interval_type = fields.Selection([('minutes', 'Minutes'),
                                                           ('hours', 'Hours'),
                                                           ('work_days', 'Work Days'),
                                                           ('days', 'Days'), ('weeks', 'Weeks'),
                                                           ('months', 'Months')],
                                                          'Import Order Interval Unit')
    shopify_order_import_next_execution = fields.Datetime('Next Execution Time',
                                                          help='Next execution time')
    shopify_order_import_user_id = fields.Many2one('res.users', string="Shopify Import User",
                                                   help='User', default=lambda self:self.env.user)

    shopify_order_update_interval_number = fields.Integer('Update Order Interval Number',
                                                          help="Repeat every x.")
    shopify_order_update_interval_type = fields.Selection([('minutes', 'Minutes'),
                                                           ('hours', 'Hours'),
                                                           ('work_days', 'Work Days'),
                                                           ('days', 'Days'), ('weeks', 'Weeks'),
                                                           ('months', 'Months')],
                                                          'Update Order Interval Unit')
    shopify_order_update_next_execution = fields.Datetime('Next Order Update Execution',
                                                          help='Next execution time')
    shopify_order_update_user_id = fields.Many2one('res.users', string="Shopify User", help='User',
                                                   default=lambda self:self.env.user)
    auto_import_product = fields.Boolean(string="Auto Create Product if not found?")
    sync_images_with_product = fields.Boolean("Import/Sync Images?",
                                              help="Check if you want to import images along with products",
                                              default=False)
    import_stock = fields.Boolean(string="Import Stock?")
    is_set_price = fields.Boolean(string="Set Price ?", default=False)
    is_set_stock = fields.Boolean(string="Set Stock ?", default=False)
    is_publish = fields.Boolean(string="Publish In Website ?", default=False)
    is_set_image = fields.Boolean(string="Set Image ?", default=False)
    import_shopify_order_status_ids = fields.Many2many('import.shopify.order.status',
                                                       'shopify_config_settings_order_status_rel',
                                                       'shopify_config_id', 'status_id',
                                                       "Import Order Status",
                                                       help="Select Order Status of the type of orders you want to import from Shopify.")
    last_date_order_import = fields.Datetime(string="Last Date of Import Order",
                                             help="Which from date to import shopify order from shopify")
    update_category_in_odoo_product = fields.Boolean(string="Update Category In Odoo Product ?")
    is_use_default_sequence = fields.Boolean("Use Odoo Default Sequence?",
                                             help="If checked,Then use default sequence of odoo for sale order create")
    # Account field
    shopify_property_account_payable_id = fields.Many2one('account.account',
                                                          string="Account Payable",
                                                          help='This account will be used instead of the default one as the payable account for the current partner')
    shopify_property_account_receivable_id = fields.Many2one('account.account',
                                                             string="Account Receivable",
                                                             help='This account will be used instead of the default one as the receivable account for the current partner')

    shopify_apply_tax_in_order = fields.Selection([("odoo_tax", "Odoo Default Tax Behaviour"),
                                                   ("create_shopify_tax","Create new tax if not found")],
                    copy=False, help=""" For Shopify Orders :- \n
                    1) Odoo Default Tax Behaviour - The Taxes will be set based on Odoo's
                                 default functional behaviour i.e. based on Odoo's Tax and Fiscal Position configurations. \n
                    2) Create New Tax If Not Found - System will search the tax data received 
                    from Shopify in Odoo, will create a new one if it fails in finding it.""")
    shopify_invoice_tax_account_id = fields.Many2one('account.account', string='Invoice Tax '
                                                                               'Account')
    shopify_credit_tax_account_id = fields.Many2one('account.account', string='Credit Tax Account')
    shopify_last_date_update_stock = fields.Datetime(string="Last Date of Stock Update",
                                                     help="it is used to store last update inventory stock date")

    shopify_settlement_report_journal_id = fields.Many2one('account.journal',string='Settlement Report Journal')

    shopify_auto_import_payout_report = fields.Boolean(string="Auto Import Payout Reports?")
    shopify_payout_import_interval_number = fields.Integer('Payout Import Interval Number', default=1,
                                                           help="Repeat every x.")
    shopify_payout_import_interval_type = fields.Selection([('minutes', 'Minutes'),
                                                            ('hours', 'Hours'), ('work_days', 'Work Days'),
                                                            ('days', 'Days'), ('weeks', 'Weeks'),
                                                            ('months', 'Months')], 'Payout Import Interval Unit')
    shopify_payout_import_next_execution = fields.Datetime('Payout Import Next Execution', help='Next execution time')
    shopify_payout_import_user_id = fields.Many2one('res.users', string="Payout Import User", help='User',
                                                    default=lambda self: self.env.user)

    shopify_auto_generate_bank_statement = fields.Boolean(string="Auto Generate Bank Statement?")
    shopify_auto_generate_bank_statement_interval_number = fields.Integer('Generate Bank Statement Interval Number',
                                                                          default=1,
                                                                          help="Repeat every x.")
    shopify_auto_generate_bank_statement_interval_type = fields.Selection([('minutes', 'Minutes'),
                                                                           ('hours', 'Hours'),
                                                                           ('work_days', 'Work Days'),
                                                                           ('days', 'Days'), ('weeks', 'Weeks'),
                                                                           ('months', 'Months')],
                                                                          'Generate Bank Statement Interval Unit')
    shopify_auto_generate_bank_statement_next_execution = fields.Datetime('Generate Bank Statement Next Execution',
                                                                          help='Next execution time')
    shopify_auto_generate_bank_statement_user_id = fields.Many2one('res.users', string="Generate Bank Statement User",
                                                                   help='User',
                                                                   default=lambda self: self.env.user)


    shopify_auto_process_bank_statement = fields.Boolean(string="Auto Process Bank Statement?")
    shopify_auto_process_bank_statement_interval_number = fields.Integer('Process Bank Statement Interval Number',
                                                                         default=1,
                                                                         help="Repeat every x.")
    shopify_auto_process_bank_statement_interval_type = fields.Selection([('minutes', 'Minutes'),
                                                                          ('hours', 'Hours'),
                                                                          ('work_days', 'Work Days'),
                                                                          ('days', 'Days'), ('weeks', 'Weeks'),
                                                                          ('months', 'Months')],
                                                                         'Process Bank Statement Interval Unit')
    shopify_auto_process_bank_statement_next_execution = fields.Datetime('Generate Bank Statement Next Execution',
                                                                         help='Next execution time')
    shopify_auto_process_bank_statement_user_id = fields.Many2one('res.users', string="Process Bank Statement User",
                                                                  help='User',
                                                                  default=lambda self: self.env.user)

    shopify_activity_type_id = fields.Many2one('mail.activity.type', string="Activity Type")
    shopify_date_deadline = fields.Integer('Deadline Lead Days',
                                           help="its add number of  days in schedule activity deadline date ")

    @api.onchange('shopify_instance_id')
    def onchange_shopify_instance_id(self):
        values = {}
        context = dict(self._context or {})
        instance = self.shopify_instance_id or False
        # self.company_id=instance and instance.company_id and instance.company_id.id or False
        if instance:
            self.shopify_company_id = instance.company_id and instance.company_id.id or False
            self.shopify_warehouse_id = instance.warehouse_id and instance.warehouse_id.id or False
            self.shopify_country_id = instance.country_id and instance.country_id.id or False
            self.shopify_lang_id = instance.lang_id and instance.lang_id.id or False
            self.shopify_order_prefix = instance.order_prefix and instance.order_prefix
            self.shopify_stock_field = instance.stock_field and instance.stock_field.id or False
            self.shopify_pricelist_id = instance.pricelist_id and instance.pricelist_id.id or False
            self.shopify_payment_term_id = instance.payment_term_id and instance.payment_term_id.id or False
            self.shopify_fiscal_position_id = instance.fiscal_position_id and instance.fiscal_position_id.id or False
            self.shopify_discount_product_id = instance.discount_product_id and instance.discount_product_id.id or False
            self.shopify_apply_tax_in_order = instance.apply_tax_in_order
            self.shopify_invoice_tax_account_id = instance.invoice_tax_account_id and \
                                                  instance.invoice_tax_account_id.id or False
            self.shopify_credit_tax_account_id = instance.credit_tax_account_id and \
                                                 instance.credit_tax_account_id.id or False
            self.add_discount_tax = instance.add_discount_tax
            self.shopify_order_auto_import = instance.order_auto_import
            self.shopify_stock_auto_export = instance.stock_auto_export
            self.import_stock = instance.import_stock
            # self.auto_import_stock=instance.auto_import_stock
            self.auto_closed_order = instance.auto_closed_order
            self.shopify_order_auto_update = instance.order_auto_update
            self.shopify_section_id = instance.section_id and instance.section_id.id or False
            self.shopify_multiple_tracking_number = instance.multiple_tracking_number or False
            self.notify_customer = instance.notify_customer or False
            self.notify_by_email_while_cancel_picking = instance.notify_by_email_while_cancel_picking or False
            self.notify_by_email_while_refund = instance.notify_by_email_while_refund or False
            self.restock_in_shopify = instance.restock_in_shopify or False
            self.auto_import_product = instance.auto_import_product or False
            self.sync_images_with_product = instance.sync_images_with_product or False
            self.import_price = instance.import_price or False
            self.is_set_price = instance.is_set_price or False
            self.is_set_stock = instance.is_set_stock or False
            self.is_publish = instance.is_publish or False
            self.is_set_image = instance.is_set_image or False
            self.shopify_global_channel_id = instance.global_channel_id or False
            self.import_shopify_order_status_ids = instance.import_shopify_order_status_ids.ids
            self.last_date_order_import = instance.last_date_order_import
            self.update_category_in_odoo_product = instance.update_category_in_odoo_product
            self.is_use_default_sequence = instance.is_use_default_sequence
            # Account Field
            self.shopify_property_account_payable_id = instance.shopify_property_account_payable_id and instance.shopify_property_account_payable_id.id or False
            self.shopify_property_account_receivable_id = instance.shopify_property_account_receivable_id and instance.shopify_property_account_receivable_id.id or False
            self.shopify_last_date_update_stock = instance.shopify_last_date_update_stock
            self.shopify_settlement_report_journal_id = instance.shopify_settlement_report_journal_id and instance.shopify_settlement_report_journal_id.id or False
            self.shopify_activity_type_id = instance.shopify_activity_type_id
            self.shopify_date_deadline = instance.shopify_date_deadline

        try:
            inventory_cron_exist = instance and self.env.ref(
                    'shopify_ept.ir_cron_auto_export_inventory_instance_%d' % (instance.id))
        except:
            inventory_cron_exist = False
        if inventory_cron_exist:
            self.shopify_inventory_export_interval_number = inventory_cron_exist.interval_number or False
            self.shopify_inventory_export_interval_type = inventory_cron_exist.interval_type or False
            self.shopify_inventory_export_next_execution = inventory_cron_exist.nextcall or False
            self.shopify_inventory_export_user_id = inventory_cron_exist.user_id.id or False

        try:
            shopify_order_import_cron_exist = instance and self.env.ref(
                    'shopify_ept.ir_cron_import_shopify_orders_instance_%d' % (instance.id))
        except:
            shopify_order_import_cron_exist = False
        if shopify_order_import_cron_exist:
            self.shopify_order_import_interval_number = shopify_order_import_cron_exist.interval_number or False
            self.shopify_order_import_interval_type = shopify_order_import_cron_exist.interval_type or False
            self.shopify_order_import_next_execution = shopify_order_import_cron_exist.nextcall or False
            self.shopify_order_import_user_id = shopify_order_import_cron_exist.user_id.id or False
        try:
            shopify_order_update_cron_exist = instance and self.env.ref(
                    'shopify_ept.ir_cron_auto_update_order_status_instance_%d' % (instance.id))
        except:
            shopify_order_update_cron_exist = False
        if shopify_order_update_cron_exist:
            self.shopify_order_update_interval_number = shopify_order_update_cron_exist.interval_number or False
            self.shopify_order_update_interval_type = shopify_order_update_cron_exist.interval_type or False
            self.shopify_order_update_next_execution = shopify_order_update_cron_exist.nextcall or False
            self.shopify_order_update_user_id = shopify_order_update_cron_exist.user_id.id or False


        try:
            payout_report_cron_exist = instance and self.env.ref(
                    'shopify_ept.ir_cron_auto_import_payout_report_instance_%d' % (instance.id))
        except:
            payout_report_cron_exist = False
        try:
            auto_generate_bank_statement_cron_exist = instance and self.env.ref(
                    'shopify_ept.ir_cron_auto_generate_bank_statement_instance_%d' % (instance.id))
        except:
            auto_generate_bank_statement_cron_exist = False
        try:
            auto_process_bank_statement_cron_exist = instance and self.env.ref(
                    'shopify_ept.ir_cron_auto_process_bank_statement_instance_%d' % (instance.id))
        except:
            auto_process_bank_statement_cron_exist = False

        if payout_report_cron_exist and payout_report_cron_exist.active:
            self.shopify_auto_import_payout_report = payout_report_cron_exist.active
            self.shopify_payout_import_interval_number = payout_report_cron_exist.interval_number or False
            self.shopify_payout_import_interval_type = payout_report_cron_exist.interval_type or False
            self.shopify_payout_import_next_execution = payout_report_cron_exist.nextcall or False
            self.shopify_payout_import_user_id = payout_report_cron_exist.user_id.id or False
        if auto_generate_bank_statement_cron_exist and auto_generate_bank_statement_cron_exist.active:
            self.shopify_auto_generate_bank_statement = auto_generate_bank_statement_cron_exist.active
            self.shopify_auto_generate_bank_statement_interval_number = auto_generate_bank_statement_cron_exist.interval_number or False
            self.shopify_auto_generate_bank_statement_interval_type = auto_generate_bank_statement_cron_exist.interval_type or False
            self.shopify_auto_generate_bank_statement_next_execution = auto_generate_bank_statement_cron_exist.nextcall or False
            self.shopify_auto_generate_bank_statement_user_id = auto_generate_bank_statement_cron_exist.user_id.id or False
        if auto_process_bank_statement_cron_exist and auto_process_bank_statement_cron_exist.active:
            self.shopify_auto_process_bank_statement = auto_process_bank_statement_cron_exist.active
            self.shopify_auto_process_bank_statement_interval_number = auto_process_bank_statement_cron_exist.interval_number or False
            self.shopify_auto_process_bank_statement_interval_type = auto_process_bank_statement_cron_exist.interval_type or False
            self.shopify_auto_process_bank_statement_next_execution = auto_process_bank_statement_cron_exist.nextcall or False
            self.shopify_auto_process_bank_statement_user_id = auto_process_bank_statement_cron_exist.user_id.id or False



    @api.multi
    def execute(self):
        instance = self.shopify_instance_id
        values = {}
        res = super(ResConfigSettings, self).execute()
        if instance:
            values['company_id'] = self.shopify_company_id and self.shopify_company_id.id or False
            values[
                'warehouse_id'] = self.shopify_warehouse_id and self.shopify_warehouse_id.id or False
            values['country_id'] = self.shopify_country_id and self.shopify_country_id.id or False
            values['lang_id'] = self.shopify_lang_id and self.shopify_lang_id.id or False
            values['order_prefix'] = self.shopify_order_prefix and self.shopify_order_prefix
            values[
                'stock_field'] = self.shopify_stock_field and self.shopify_stock_field.id or False
            values[
                'pricelist_id'] = self.shopify_pricelist_id and self.shopify_pricelist_id.id or False
            values[
                'payment_term_id'] = self.shopify_payment_term_id and self.shopify_payment_term_id.id or False
            values[
                'fiscal_position_id'] = self.shopify_fiscal_position_id and self.shopify_fiscal_position_id.id or False
            values['discount_product_id'] = self.shopify_discount_product_id.id or False
            values['apply_tax_in_order'] = self.shopify_apply_tax_in_order
            values['invoice_tax_account_id'] = self.shopify_invoice_tax_account_id and \
                                               self.shopify_invoice_tax_account_id.id or False
            values['credit_tax_account_id'] = self.shopify_credit_tax_account_id and \
                                              self.shopify_credit_tax_account_id.id or False
            values['add_discount_tax'] = self.add_discount_tax
            values['order_auto_import'] = self.shopify_order_auto_import
            values['stock_auto_export'] = self.shopify_stock_auto_export
            values['import_stock'] = self.import_stock
            # values['auto_import_stock']=self.auto_import_stock
            values['import_price'] = self.import_price
            values['auto_closed_order'] = self.auto_closed_order
            values['order_auto_update'] = self.shopify_order_auto_update
            values['section_id'] = self.shopify_section_id and self.shopify_section_id.id or False
            values['multiple_tracking_number'] = self.shopify_multiple_tracking_number
            values['notify_customer'] = self.notify_customer
            values[
                'notify_by_email_while_cancel_picking'] = self.notify_by_email_while_cancel_picking
            values['notify_by_email_while_refund'] = self.notify_by_email_while_refund
            values['restock_in_shopify'] = self.restock_in_shopify
            values['auto_import_product'] = self.auto_import_product or False
            values['sync_images_with_product'] = self.sync_images_with_product or False
            values['is_set_price'] = self.is_set_price or False
            values['is_set_stock'] = self.is_set_stock or False
            values['is_publish'] = self.is_publish or False
            values['is_set_image'] = self.is_set_image or False
            values[
                'global_channel_id'] = self.shopify_global_channel_id and self.shopify_global_channel_id.id or False
            values['import_shopify_order_status_ids'] = [
                (6, 0, self.import_shopify_order_status_ids.ids)]
            values['last_date_order_import'] = self.last_date_order_import
            values[
                'update_category_in_odoo_product'] = self.update_category_in_odoo_product or False
            values[
                'is_use_default_sequence'] = self.is_use_default_sequence and self.is_use_default_sequence
            # account Fields
            values[
                'shopify_property_account_payable_id'] = self.shopify_property_account_payable_id and self.shopify_property_account_payable_id.id or False
            values[
                'shopify_property_account_receivable_id'] = self.shopify_property_account_receivable_id and self.shopify_property_account_receivable_id.id or False
            values[
                'shopify_last_date_update_stock'] = self.shopify_last_date_update_stock

            """Get require value of payout report from instance
            @author: Deval Jagad (02/06/2020)
            Task Id : 163887"""
            #Start
            values['shopify_settlement_report_journal_id'] = self.shopify_settlement_report_journal_id and self.shopify_settlement_report_journal_id.id or False
            values['shopify_activity_type_id'] = self.shopify_activity_type_id and  self.shopify_activity_type_id.id or False
            values['shopify_date_deadline'] = self.shopify_date_deadline or False
            #End
            instance.write(values)
            self.setup_shopify_inventory_export_cron(instance)
            self.setup_shopify_order_import_cron(instance)
            self.setup_shopify_order_update_cron(instance)
            self.setup_shopify_payout_payout_cron(instance)
        return res

    @api.multi
    def setup_shopify_inventory_export_cron(self, instance):
        if self.shopify_stock_auto_export:
            try:
                cron_exist = self.env.ref(
                        'shopify_ept.ir_cron_auto_export_inventory_instance_%d' % (instance.id))
            except:
                cron_exist = False
            nextcall = datetime.now()
            nextcall += _intervalTypes[self.shopify_inventory_export_interval_type](
                    self.shopify_inventory_export_interval_number)
            vals = {'active':True,
                    'interval_number':self.shopify_inventory_export_interval_number,
                    'interval_type':self.shopify_inventory_export_interval_type,
                    'nextcall':self.shopify_inventory_export_next_execution or nextcall.strftime(
                            '%Y-%m-%d %H:%M:%S'),
                    'code':"model.auto_update_stock_ept(ctx={'shopify_instance_id':%d})" % (
                        instance.id),
                    'user_id':self.shopify_inventory_export_user_id and self.shopify_inventory_export_user_id.id}
            if cron_exist:
                vals.update({'name':cron_exist.name})
                cron_exist.write(vals)
            else:
                try:
                    export_stock_cron = self.env.ref('shopify_ept.ir_cron_auto_export_inventory')
                except:
                    export_stock_cron = False
                if not export_stock_cron:
                    raise Warning(
                            'Core settings of Shopify are deleted, please upgrade Shopify module to back this settings.')

                name = instance.name + ' : ' + export_stock_cron.name
                vals.update({'name':name})
                new_cron = export_stock_cron.copy(default=vals)
                self.env['ir.model.data'].create({'module':'shopify_ept',
                                                  'name':'ir_cron_auto_export_inventory_instance_%d' % (
                                                      instance.id),
                                                  'model':'ir.cron',
                                                  'res_id':new_cron.id,
                                                  'noupdate':True
                                                  })
        else:
            try:
                cron_exist = self.env.ref(
                        'shopify_ept.ir_cron_auto_export_inventory_instance_%d' % (instance.id))
            except:
                cron_exist = False
            if cron_exist:
                cron_exist.write({'active':False})
        return True

    @api.multi
    def setup_shopify_order_import_cron(self, instance):
        if self.shopify_order_auto_import:
            try:
                cron_exist = self.env.ref(
                        'shopify_ept.ir_cron_import_shopify_orders_instance_%d' % (instance.id))
            except:
                cron_exist = False
            nextcall = datetime.now()
            nextcall += _intervalTypes[self.shopify_order_import_interval_type](
                    self.shopify_order_import_interval_number)
            vals = {
                'active':True,
                'interval_number':self.shopify_order_import_interval_number,
                'interval_type':self.shopify_order_import_interval_type,
                'nextcall':self.shopify_order_import_next_execution or nextcall.strftime(
                        '%Y-%m-%d %H:%M:%S'),
                'code':"model.auto_import_sale_order_ept(ctx={'shopify_instance_id':%d})" % (
                    instance.id),
                'user_id':self.shopify_order_import_user_id and self.shopify_order_import_user_id.id}

            if cron_exist:
                vals.update({'name':cron_exist.name})
                cron_exist.write(vals)
            else:
                try:
                    import_order_cron = self.env.ref('shopify_ept.ir_cron_import_shopify_orders')
                except:
                    import_order_cron = False
                if not import_order_cron:
                    raise Warning(
                            'Core settings of Shopify are deleted, please upgrade Shopify module to back this settings.')

                name = instance.name + ' : ' + import_order_cron.name
                vals.update({'name':name})
                new_cron = import_order_cron.copy(default=vals)
                self.env['ir.model.data'].create({'module':'shopify_ept',
                                                  'name':'ir_cron_import_shopify_orders_instance_%d' % (
                                                      instance.id),
                                                  'model':'ir.cron',
                                                  'res_id':new_cron.id,
                                                  'noupdate':True
                                                  })
        else:
            try:
                cron_exist = self.env.ref(
                        'shopify_ept.ir_cron_import_shopify_orders_instance_%d' % (instance.id))
            except:
                cron_exist = False

            if cron_exist:
                cron_exist.write({'active':False})
        return True

    @api.multi
    def setup_shopify_order_update_cron(self, instance):
        if self.shopify_order_auto_update:
            try:
                cron_exist = self.env.ref(
                        'shopify_ept.ir_cron_auto_update_order_status_instance_%d' % (instance.id))
            except:
                cron_exist = False
            nextcall = datetime.now()
            nextcall += _intervalTypes[self.shopify_order_update_interval_type](
                    self.shopify_order_update_interval_number)
            vals = {'active':True,
                    'interval_number':self.shopify_order_update_interval_number,
                    'interval_type':self.shopify_order_update_interval_type,
                    'nextcall':self.shopify_order_update_next_execution or nextcall.strftime(
                            '%Y-%m-%d %H:%M:%S'),
                    'code':"model.auto_update_order_status_ept(ctx={'shopify_instance_id':%d})" % (
                        instance.id),
                    'user_id':self.shopify_order_update_user_id and self.shopify_order_update_user_id.id}

            if cron_exist:
                vals.update({'name':cron_exist.name})
                cron_exist.write(vals)
            else:
                try:
                    update_order_cron = self.env.ref('shopify_ept.ir_cron_auto_update_order_status')
                except:
                    update_order_cron = False
                if not update_order_cron:
                    raise Warning(
                            'Core settings of Shopify are deleted, please upgrade Shopify module to back this settings.')

                name = instance.name + ' : ' + update_order_cron.name
                vals.update({'name':name})
                new_cron = update_order_cron.copy(default=vals)
                self.env['ir.model.data'].create({'module':'shopify_ept',
                                                  'name':'ir_cron_auto_update_order_status_instance_%d' % (
                                                      instance.id),
                                                  'model':'ir.cron',
                                                  'res_id':new_cron.id,
                                                  'noupdate':True
                                                  })
        else:
            try:
                cron_exist = self.env.ref(
                        'shopify_ept.ir_cron_auto_update_order_status_instance_%d' % (instance.id))
            except:
                cron_exist = False
            if cron_exist:
                cron_exist.write({'active':False})
        return True

    @api.multi
    def setup_shopify_payout_auto_import_payout_report_cron(self, instance):
        """
        Author: Deval Jagad (02/06/2020)
        Task Id : 163887
        Func: this method use for the create import payout report instance wise cron or set active
        :param instance:use for shopify instance
        :return:True
        """
        try:
            cron_exist = self.env.ref(
                    'shopify_ept.ir_cron_auto_import_payout_report_instance_%d' % (instance.id))
        except:
            cron_exist = False
        nextcall = datetime.now()
        nextcall += _intervalTypes[self.shopify_payout_import_interval_type](
                self.shopify_payout_import_interval_number)
        vals = {'active': True,
                'interval_number': self.shopify_payout_import_interval_number,
                'interval_type': self.shopify_payout_import_interval_type,
                'nextcall': self.shopify_payout_import_next_execution or nextcall.strftime('%Y-%m-%d %H:%M:%S'),
                'code': "model.auto_import_payout_report(ctx={'shopify_instance_id':%d})" % (instance.id),
                'user_id': self.shopify_payout_import_user_id and self.shopify_payout_import_user_id.id}

        if cron_exist:
            vals.update({'name': cron_exist.name})
            cron_exist.write(vals)
        else:
            try:
                update_order_cron = self.env.ref('shopify_ept.ir_cron_auto_import_payout_report')
            except:
                update_order_cron = False
            if not update_order_cron:
                raise Warning(
                        'Core settings of Shopify are deleted, please upgrade Shopify module to back this settings.')

            name = instance.name + ' : ' + update_order_cron.name
            vals.update({'name': name})
            new_cron = update_order_cron.copy(default=vals)
            self.env['ir.model.data'].create({'module': 'shopify_ept',
                                              'name': 'ir_cron_auto_import_payout_report_instance_%d' % (
                                                  instance.id),
                                              'model': 'ir.cron',
                                              'res_id': new_cron.id,
                                              'noupdate': True
                                              })
        return True

    @api.multi
    def setup_shopify_payout_auto_generate_bank_statement_cron(self, instance):
        """
        Author: Deval Jagad (02/06/2020)
        Task Id : 163887
        Func: this method use for the create generate bank statement instance wise cron or set active
        :param instance: use for shopify instance
        :return: True
        """
        try:
            cron_exist = self.env.ref(
                    'shopify_ept.ir_cron_auto_generate_bank_statement_instance_%d' % (instance.id))
        except:
            cron_exist = False
        nextcall = datetime.now()
        nextcall += _intervalTypes[self.shopify_auto_generate_bank_statement_interval_type](
                self.shopify_auto_generate_bank_statement_interval_number)
        vals = {'active': True,
                'interval_number': self.shopify_auto_generate_bank_statement_interval_number,
                'interval_type': self.shopify_auto_generate_bank_statement_interval_type,
                'nextcall': self.shopify_auto_generate_bank_statement_next_execution or nextcall.strftime(
                        '%Y-%m-%d %H:%M:%S'),
                'code': "model.auto_generate_bank_statement(ctx={'shopify_instance_id':%d})" % (instance.id),
                'user_id': self.shopify_auto_generate_bank_statement_user_id and self.shopify_auto_generate_bank_statement_user_id.id}

        if cron_exist:
            vals.update({'name': cron_exist.name})
            cron_exist.write(vals)
        else:
            try:
                update_cron = self.env.ref('shopify_ept.ir_cron_auto_generate_bank_statement')
            except:
                update_cron = False
            if not update_cron:
                raise Warning(
                        'Core settings of Shopify are deleted, please upgrade Shopify module to back this settings.')

            name = instance.name + ' : ' + update_cron.name
            vals.update({'name': name})
            new_cron = update_cron.copy(default=vals)
            self.env['ir.model.data'].create({'module': 'shopify_ept',
                                              'name': 'ir_cron_auto_generate_bank_statement_instance_%d' % (
                                                  instance.id),
                                              'model': 'ir.cron',
                                              'res_id': new_cron.id,
                                              'noupdate': True
                                              })
        return True

    @api.multi
    def setup_shopify_payout_auto_process_bank_statement_cron(self, instance):
        """
        Author: Deval Jagad (02/06/2020)
        Task Id : 163887
        Func: this method use for the create process bank statement instance wise cron or set active
        :param instance: use for shopify instance
        :return: True
        """
        try:
            cron_exist = self.env.ref(
                    'shopify_ept.ir_cron_auto_process_bank_statement_instance_%d' % (instance.id))
        except:
            cron_exist = False
        nextcall = datetime.now()
        nextcall += _intervalTypes[self.shopify_auto_process_bank_statement_interval_type](
                self.shopify_auto_process_bank_statement_interval_number)
        vals = {'active': True,
                'interval_number': self.shopify_auto_process_bank_statement_interval_number,
                'interval_type': self.shopify_auto_process_bank_statement_interval_type,
                'nextcall': self.shopify_auto_process_bank_statement_next_execution or nextcall.strftime(
                        '%Y-%m-%d %H:%M:%S'),
                'code': "model.auto_process_bank_statement(ctx={'shopify_instance_id':%d})" % (instance.id),
                'user_id': self.shopify_auto_process_bank_statement_user_id and self.shopify_auto_process_bank_statement_user_id.id}
        if cron_exist:
            vals.update({'name': cron_exist.name})
            cron_exist.write(vals)
        else:
            try:
                update_cron = self.env.ref('shopify_ept.ir_cron_auto_process_bank_statement')
            except:
                update_cron = False
            if not update_cron:
                raise Warning(
                        'Core settings of Shopify are deleted, please upgrade Shopify module to back this settings.')

            name = instance.name + ' : ' + update_cron.name
            vals.update({'name': name})
            new_cron = update_cron.copy(default=vals)
            self.env['ir.model.data'].create({'module': 'shopify_ept',
                                              'name': 'ir_cron_auto_process_bank_statement_instance_%d' % (
                                                  instance.id),
                                              'model': 'ir.cron',
                                              'res_id': new_cron.id,
                                              'noupdate': True
                                              })
        return True

    @api.multi
    def setup_shopify_payout_payout_cron(self, instance):
        if self.shopify_auto_import_payout_report:
            self.setup_shopify_payout_auto_import_payout_report_cron(instance)
        else:
            try:
                cron_exist = self.env.ref(
                        'shopify_ept.ir_cron_auto_import_payout_report_instance_%d' % (instance.id))
            except:
                cron_exist = False
            if cron_exist:
                cron_exist.write({'active': False})
        if self.shopify_auto_generate_bank_statement:
            self.setup_shopify_payout_auto_generate_bank_statement_cron(instance)
        else:
            try:
                cron_exist = self.env.ref(
                        'shopify_ept.ir_cron_auto_generate_bank_statement_instance_%d' % (instance.id))
            except:
                cron_exist = False
            if cron_exist:
                cron_exist.write({'active': False})
        if self.shopify_auto_process_bank_statement:
            self.setup_shopify_payout_auto_process_bank_statement_cron(instance)
        else:
            try:
                cron_exist = self.env.ref(
                        'shopify_ept.ir_cron_auto_process_bank_statement_instance_%d' % (instance.id))
            except:
                cron_exist = False
            if cron_exist:
                cron_exist.write({'active': False})
        return True