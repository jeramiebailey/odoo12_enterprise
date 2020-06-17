# Copyright 2019 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': 'Purchase Variant Invert Axis',
    'summary': 'Invert axis in purchase variant management wizard',
    'version': '12.0.1.0.0',
    'category': 'Sale',
    'author': 'Eska',
    'website': 'http://www.eskayazilim.com.tr',
    'license': 'AGPL-3',
    'depends': [
        'product_brand',
        'purchase_order_variant_mgmt',
    ],
    'data': [
        'wizard/purchase_manage_variant_view.xml',
    ],
    'installable': True,
}