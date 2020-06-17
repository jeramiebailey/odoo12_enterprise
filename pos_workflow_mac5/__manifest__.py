{
    'name': 'POS Workflows',
    'version': '12.0.1.9.2',
    'summary': """Create POS Order, Sales Order, Delivery Order,
                  Purchase Order, Customer Invoice & Vendor Bill""",
    'description': """
POS Workflows
=============

Features
--------
* Create POS Order
* Create Sales Quotation
* Create Sales Order
* Create Sales Order, Waiting Delivery & Posted Invoice
* Create Sales Order, Done Delivery & Posted Invoice
* Create Purchase Quotation
* Create Purchase Order
* Create Purchase Order, Waiting Reception & Posted Invoice
* Create Purchase Order, Done Reception & Posted Invoice
* Create Customer Invoice
* Create Validated Customer Invoice
* Create Vendor Bill
* Create Validated Vendor Bill


Keywords: Odoo POS Sales Quotation, Odoo POS Sales Order, Odoo POS Sale Quotation,
Odoo POS Sale Order, Odoo POS Create Sales Quotation, Odoo POS Create Sales Order,
Odoo Create POS Sale Quotation, Odoo POS Create Sale Order, Odoo POS Purchase Quotation,
Odoo POS Purchase Order, Odoo POS Create Purchase Quotation, Odoo POS Create Purchase Order,
Odoo POS Invoice, Odoo POS Customer Invoice, Odoo POS Create Customer Invoice,
Odoo POS Vendor Bill, Odoo POS Create Vendor Bill, Odoo POS Supplier Invoice,
Odoo POS Create Supplier Invoice
""",
    'category': 'Point of Sale',
    'author': 'MAC5',
    'contributors': ['Michael Aldrin C. Villamar'],
    'website': 'https://apps.odoo.com/apps/modules/browse?author=MAC5',
    'depends': [
        'pos_workflow_base_mac5',
        'purchase',
        'sale_stock',
    ],
    'data': ['views/pos_templates.xml'],
    'demo': [],
    'qweb': ['static/src/xml/pos_workflow.xml'],
    'installable': True,
    'application': False,
    'auto_install': False,
    'images': ['static/description/pos_sale_quotation2.png'],
    'price': 149.99,
    'currency': 'EUR',
    'support': 'macvillamar@live.com',
    'license': 'OPL-1',
}
