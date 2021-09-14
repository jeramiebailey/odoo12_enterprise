# Copyright 2021 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': 'Stock Inventory Product Variants',
    'summary': 'Manage product variants',
    'version': '12.0.1.0.0',
    'category': 'Product',
    'author': 'Eska',
    'website': 'http://www.eskayazilim.com.tr',
    'license': 'AGPL-3',
    'depends': [
        'stock',
        'web_widget_x2many_2d_matrix',
    ],
    'data': [
        'wizard/stock_manage_variant_view.xml',
        "views/stock_inventory_view.xml",
    ],
    'installable': True,
    'auto_install': False,
}
