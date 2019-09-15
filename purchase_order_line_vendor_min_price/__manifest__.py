# Copyright 2019 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    'name': 'Purchase Order Line Vendor Minimum Price',
    'summary': 'Show the minimum purchase price for this product from this vendor.',
    'version': '12.0.1.0.0',
    'category': 'Sale',
    'author': 'Eska',
    'website': 'http://www.eskayazilim.com.tr',
    'license': 'AGPL-3',
    'auto_install': False,
    'depends': [
        'purchase',
    ],
    'data': [
        'views/purchase_order_view.xml',
    ],
    'installable': True,
    'auto_install': False,
}

