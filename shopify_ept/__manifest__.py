{
    # App information
    'name': 'Shopify Odoo Connector',
    'version': '12.0.13',
    'category': 'Sales',
    'summary' : 'Shopify Odoo Connector helps you in integrating and managing your Shopify store with Odoo by providing the most useful features of Product and Order Synchronization.',
    'license': 'OPL-1',
    
    # Author
    'author': 'Emipro Technologies Pvt. Ltd.',
    'website': 'http://www.emiprotechnologies.com/',
    'maintainer': 'Emipro Technologies Pvt. Ltd.',
    
    # Dependencies
    'depends': ['auto_invoice_workflow_ept','common_connector_library'],
    
    # Views
    'init_xml': [],
    'data': [
             'security/group.xml',
             'security/ir.model.access.csv',
             'wizard/res_config_view.xml',
             'view/res_partner.xml',
             'view/sale_order.xml',
             'wizard/shopify_process_import_export_view.xml',
             'view/shopify_product_template_view.xml',
             'view/shopify_product_product_view.xml',
             'view/shopify_job_log.xml',
             'view/stock_quant_package_view.xml',
             'view/stock_picking_view.xml',
             'view/account_invoice_view.xml',
             'view/shopify_tags_view.xml',
             'view/ir_cron.xml',
             'wizard/shopify_cancel_order_wizard_view.xml',
             'view/shopify_collection_view.xml',             
             'view/web_templates.xml',
             'wizard/shopify_variants_reorder_view.xml',             
             'view/sale_workflow_config.xml',
             'view/shopify_product_image_view.xml',                                      
             'report/sale_report_view.xml',
             'view/shopify_instance_view.xml',
             'view/shopify_payment_gateway.xml',
             'view/shopify_location_ept.xml',
             'data/product_product_demo.xml',
             'wizard/shopify_refund_wizard_view.xml',
             'data/import_order_status.xml',
             'data/ir_sequence.xml',
             'view/shopify_payout_report_ept.xml',
             'wizard/shopify_payout_report.xml',
             ],
    'demo_xml': [],
    
    # Odoo Store Specific
    'images': ['static/description/shopify-odoo-cover.jpg'],
    
    'installable': True,
    'auto_install': False,
    'application' : True,
    'live_test_url' : 'https://www.emiprotechnologies.com/free-trial?app=shopify-ept&version=12&edition=enterprise',
    'price': 379.00,
    'currency': 'EUR',
}
