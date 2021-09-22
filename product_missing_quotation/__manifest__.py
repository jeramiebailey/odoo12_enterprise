# Copyright 2021 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    'name': 'Product Missing Quotation',
    'summary': 'Missing product quantity on quotation',
    'version': '12.0.1.0.0',
    'category': 'Project',
    'author': 'Eska',
    'website': 'http://www.eskayazilim.com.tr',
    'license': 'AGPL-3',
    'depends': [
        'product_missing_sale',
    ],
    'data': [
        'views/product_product_view.xml',
        'views/sale_order_line_view.xml',
    ],
    'installable': True,
    'auto_install': False,
}
