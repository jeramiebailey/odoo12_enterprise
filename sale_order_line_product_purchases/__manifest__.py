# Copyright 2019 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': 'Sale Order Line Product Purchases',
    'summary': 'Adds Origin Purchases Of Products on Sale Orders Lines',
    'version': '12.0.1.0.0',
    'category': 'Sale',
    'author': 'Eska',
    'website': 'http://www.eskayazilim.com.tr',
    'license': 'AGPL-3',
    'depends': [
        'sale_purchase',
    ],
    'data': [
        'views/sale_order_view.xml',
    ],
    'installable': True,
}