from odoo import models, fields, api, _
from odoo.exceptions import Warning
from .. import shopify

class shopify_instance_ept(models.Model):
    _name = "shopify.instance.ept"
    _description = 'Shopify Instance Ept'

    name = fields.Char(size=120, string='Name', required=True)
    company_id = fields.Many2one('res.company', string='Company', required=True)
    warehouse_id = fields.Many2one('stock.warehouse', string='Warehouse')
    pricelist_id = fields.Many2one('product.pricelist', string='Pricelist')
    lang_id = fields.Many2one('res.lang', string='Language')
    order_prefix = fields.Char(size=10, string='Order Prefix')
    order_auto_import = fields.Boolean(string='Auto Order Import?')
    order_auto_update = fields.Boolean(string="Auto Order Update ?")
    stock_auto_export = fields.Boolean(string="Stock Auto Export?")
    import_stock = fields.Boolean(string="import_stock?")
    fiscal_position_id = fields.Many2one('account.fiscal.position', string='Fiscal Position')
    stock_field = fields.Many2one('ir.model.fields', string='Stock Field')
    country_id = fields.Many2one("res.country", "Country")
    api_key = fields.Char("API Key", required=True)
    password = fields.Char("Password", required=True)
    shared_secret = fields.Char("Secret Key", required=True)
    host = fields.Char("Host", required=True)
    shipment_charge_product_id = fields.Many2one("product.product", "Shipment Fee",
                                                 domain=[('type', '=', 'service')])
    section_id = fields.Many2one('crm.team', 'Sales Team')
    payment_term_id = fields.Many2one('account.payment.term', string='Payment Term')
    discount_product_id = fields.Many2one("product.product", "Discount",
                                          domain=[('type', '=', 'service')])
    apply_tax_in_order = fields.Selection([("odoo_tax", "Odoo Default Tax Behaviour"),
                                           ("create_shopify_tax", "Create new tax if not found")],
                                          default='create_shopify_tax', copy=False, help=""" For Shopify Orders :- \n
                    1) Odoo Default Tax Behaviour - The Taxes will be set based on Odoo's
                                 default functional behaviour i.e. based on Odoo's Tax and Fiscal Position configurations. \n
                    2) Create New Tax If Not Found - System will search the tax data received 
                    from Shopify in Odoo, will create a new one if it fails in finding it.""")
    invoice_tax_account_id = fields.Many2one('account.account', string='Invoice Tax Account')
    credit_tax_account_id = fields.Many2one('account.account', string='Credit Tax Account')
    add_discount_tax = fields.Boolean("Calculate Discount Tax", default=False)
    last_inventory_update_time = fields.Datetime("Last Inventory Update Time")
    auto_closed_order = fields.Boolean("Auto Closed Order", default=False)
    state = fields.Selection([('not_confirmed', 'Not Confirmed'), ('confirmed', 'Confirmed')],
                             default='not_confirmed')
    workflow_config_ids = fields.One2many("sale.auto.workflow.configuration", "shopify_instance_id",
                                          "Workflows")
    multiple_tracking_number = fields.Boolean(string='One order can have multiple Tracking Number',
                                              default=False)
    notify_customer = fields.Boolean("Notify Customer about Update Order Status?",
                                     help="If checked,Notify the customer via email about Update Order Status")
    notify_by_email_while_cancel_picking = fields.Boolean("Notify Customer about Cancel Picking?",
                                                          help="If checked,Notify the customer via email about Order Cancel")
    notify_by_email_while_refund = fields.Boolean("Notify Customer about Refund?",
                                                  help="If checked,Notify the customer via email about Refund")
    restock_in_shopify = fields.Boolean("Restock In Shopify ?",
                                        help="If checked,Restock In Shopify while refund")
    auto_import_product = fields.Boolean(string="Auto Create Product if not found?")
    sync_images_with_product = fields.Boolean("Sync Images?",
                                              help="Check if you want to import images along with products",
                                              default=False)
    # auto_import_stock=fields.Boolean(string="Auto Import Stock?")
    import_price = fields.Boolean(string="Import Price?")
    inventory_adjustment_id = fields.Many2one('stock.inventory', "Last Inventory")
    is_image_url = fields.Boolean("Is Image URL?",
                                  help="Check this if you use Images from URL\nKeep as it is if you use Product images")
    is_set_price = fields.Boolean(string="Set Price ?", default=False)
    is_set_stock = fields.Boolean(string="Set Stock ?", default=False)
    is_publish = fields.Boolean(string="Publish In Website ?", default=False)
    is_set_image = fields.Boolean(string="Set Image ?", default=False)
    last_date_order_import = fields.Datetime(string="Last Date of Import Order",
                                             help="Which from date to import shopify order from shopify")
    import_shopify_order_status_ids = fields.Many2many('import.shopify.order.status',
                                                       'shopify_instance_order_status_rel',
                                                       'instance_id', 'status_id',
                                                       "Import Order Status",
                                                       help="Selected status orders will be imported from Shopify")
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
    shopify_last_date_update_stock = fields.Datetime(string="Last Date of Stock Update",
                                                     help="it is used to store last update inventory stock date")

    def _count_all(self):
        for instance in self:
            instance.product_count = len(instance.product_ids)
            instance.sale_order_count = len(instance.sale_order_ids)
            instance.picking_count = len(instance.picking_ids)
            instance.invoice_count = len(instance.invoice_ids)
            instance.exported_product_count = len(instance.exported_product_ids)
            instance.ready_to_expor_product_count = len(instance.ready_to_expor_product_ids)
            instance.published_product_count = len(instance.published_product_ids)
            instance.unpublished_product_count = len(instance.unpublished_product_ids)
            instance.quotation_count = len(instance.quotation_ids)
            instance.order_count = len(instance.order_ids)
            instance.risk_order_count = len(instance.risk_order_ids)
            instance.confirmed_picking_count = len(instance.confirmed_picking_ids)
            instance.assigned_picking_count = len(instance.assigned_picking_ids)
            instance.partially_available_picking_count = len(
                    instance.partially_available_picking_ids)
            instance.done_picking_count = len(instance.done_picking_ids)
            instance.open_invoice_count = len(instance.open_invoice_ids)
            instance.paid_invoice_count = len(instance.paid_invoice_ids)
            instance.refund_invoice_count = len(instance.refund_invoice_ids)
            instance.shopify_custom_collection_count = len(instance.shopify_custom_collection_ids)
            instance.shopify_smart_collection_count = len(instance.shopify_smart_collection_ids)

    color = fields.Integer(string='Color Index')

    exported_product_ids = fields.One2many('shopify.product.template.ept', 'shopify_instance_id',
                                           domain=[('exported_in_shopify', '=', True)],
                                           string="Exported Product")
    exported_product_count = fields.Integer(compute='_count_all', string="Exported Products")

    ready_to_expor_product_ids = fields.One2many('shopify.product.template.ept',
                                                 'shopify_instance_id',
                                                 domain=[('exported_in_shopify', '=', False)],
                                                 string="Ready To Export")
    ready_to_expor_product_count = fields.Integer(compute='_count_all', string="Ready For Export")

    published_product_ids = fields.One2many('shopify.product.template.ept', 'shopify_instance_id',
                                            domain=[('website_published', '=', True)],
                                            string="Published")
    published_product_count = fields.Integer(compute='_count_all', string="Published Product")

    unpublished_product_ids = fields.One2many('shopify.product.template.ept', 'shopify_instance_id',
                                              domain=[('website_published', '=', False),
                                                      ('exported_in_shopify', '=', True)],
                                              string="Unpublished Products")
    unpublished_product_count = fields.Integer(compute='_count_all', string="#UnPublished Product")

    quotation_ids = fields.One2many('sale.order', 'shopify_instance_id',
                                    domain=[('state', 'in', ['draft', 'sent'])],
                                    string="Quotations")
    quotation_count = fields.Integer(compute='_count_all', string="Quotation")

    order_ids = fields.One2many('sale.order', 'shopify_instance_id',
                                domain=[('state', 'not in', ['draft', 'sent', 'cancel'])],
                                string="Sales Order")
    order_count = fields.Integer(compute='_count_all', string="Sales Orders")

    risk_order_ids = fields.One2many('sale.order', 'shopify_instance_id',
                                     domain=[('state', '=', 'draft'),
                                             ('is_risky_order', '!=', False)], string="Risky Order")
    risk_order_count = fields.Integer(compute='_count_all', string="Risky Orders")

    confirmed_picking_ids = fields.One2many('stock.picking', 'shopify_instance_id',
                                            domain=[('state', '=', 'confirmed')],
                                            string="Confirm Pickings")
    confirmed_picking_count = fields.Integer(compute='_count_all', string="Confirm Picking")
    assigned_picking_ids = fields.One2many('stock.picking', 'shopify_instance_id',
                                           domain=[('state', '=', 'assigned')],
                                           string="Assigned Picking")
    assigned_picking_count = fields.Integer(compute='_count_all', string="Assigned Pickings")
    partially_available_picking_ids = fields.One2many('stock.picking', 'shopify_instance_id',
                                                      domain=[
                                                          ('state', '=', 'partially_available')],
                                                      string="Partially Available Pickings")
    partially_available_picking_count = fields.Integer(compute='_count_all',
                                                       string="Partially Available Picking")
    done_picking_ids = fields.One2many('stock.picking', 'shopify_instance_id',
                                       domain=[('state', '=', 'done')], string="Done Pickings")
    done_picking_count = fields.Integer(compute='_count_all', string="Done Picking")

    open_invoice_ids = fields.One2many('account.invoice', 'shopify_instance_id',
                                       domain=[('state', '=', 'open'),
                                               ('type', '=', 'out_invoice')],
                                       string="Open Invoices")
    open_invoice_count = fields.Integer(compute='_count_all', string="Open Invoice")

    paid_invoice_ids = fields.One2many('account.invoice', 'shopify_instance_id',
                                       domain=[('state', '=', 'paid'),
                                               ('type', '=', 'out_invoice')],
                                       string="Paid Invoices")
    paid_invoice_count = fields.Integer(compute='_count_all', string="Paid Invoice")

    refund_invoice_ids = fields.One2many('account.invoice', 'shopify_instance_id',
                                         domain=[('type', '=', 'out_refund')],
                                         string="Refund Invoice")
    refund_invoice_count = fields.Integer(compute='_count_all', string="Refund Invoices")

    product_ids = fields.One2many('shopify.product.template.ept', 'shopify_instance_id',
                                  string="Products")
    product_count = fields.Integer(compute='_count_all', string="Product")

    sale_order_ids = fields.One2many('sale.order', 'shopify_instance_id', string="Orders")
    sale_order_count = fields.Integer(compute='_count_all', string="Sale Order Count")

    picking_ids = fields.One2many('stock.picking', 'shopify_instance_id', string="Pickings")
    picking_count = fields.Integer(compute='_count_all', string="Picking")

    invoice_ids = fields.One2many('account.invoice', 'shopify_instance_id', string="Invoices")
    invoice_count = fields.Integer(compute='_count_all', string="Invoice")

    shopify_custom_collection_ids = fields.One2many('shopify.collection.ept', 'shopify_instance_id',
                                                    domain=[('is_smart_collection', '=', False)],
                                                    string="Shopify Collection")
    shopify_custom_collection_count = fields.Integer(compute='_count_all',
                                                     string="Shopify Collections")
    shopify_smart_collection_ids = fields.One2many('shopify.collection.ept', 'shopify_instance_id',
                                                   domain=[('is_smart_collection', '=', True)],
                                                   string="Shopify Smart Collection")
    shopify_smart_collection_count = fields.Integer(compute='_count_all',
                                                    string="Shopify Smart Collections")

    global_channel_id = fields.Many2one('global.channel.ept', string="Global Channel")



    shopify_api_url = fields.Char(string="Payout API URL", default = 'admin/api/2019-04/shopify_payments/')
    transaction_line_ids = fields.One2many("shopify.payout.account.config.ept", "instance_id",
                                           string="Transaction Line")
    shopify_settlement_report_journal_id = fields.Many2one('account.journal',
                                                           string='Settlement Report Journal')
    payout_last_import_date = fields.Date(string="Payout last Import Date")
    shopify_activity_type_id = fields.Many2one('mail.activity.type',
                                               string="Activity Type")
    shopify_date_deadline = fields.Integer('Deadline lead days',
                                           help="its add number of  days in schedule activity deadline date ")

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
        raise Warning('Service working properly')

    @api.multi
    def reset_to_confirm(self):
        self.write({'state':'not_confirmed'})
        return True

    @api.multi
    def confirm(self):
        self.connect_in_shopify()
        try:
            shop_id = shopify.Shop.current()
        except Exception as e:
            raise Warning(e)
        self.write({'state':'confirmed'})
        self.env['shopify.location.ept'].import_shopify_locations(self)
        return True

    @api.model
    def connect_in_shopify(self):
        instance = self
        shop = instance.host.split("//")
        if len(shop) == 2:
            shop_url = shop[0] + "//" + instance.api_key + ":" + instance.password + "@" + shop[
                1] + "/admin/api/2020-01"
        else:
            shop_url = "https://" + instance.api_key + ":" + instance.password + "@" + shop[
                0] + "/admin/api/2020-01"
        shopify.ShopifyResource.set_site(shop_url)
        return True
