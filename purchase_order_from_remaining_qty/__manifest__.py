# Copyright 2020 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': 'Purchase Order From Remaining',
    'summary': 'Create backorders from purchase remaining quantities',
    'version': '12.0.1.0.0',
    'category': 'Purchase',
    'author': 'Eska',
    'website': 'http://www.eskayazilim.com.tr',
    'license': 'AGPL-3',
    'depends': [
        'purchase_stock',
    ],
    'data': [
        'wizard/purchase_order_from_remaining_qty.xml',
        'views/purchase_order_view.xml',
    ],
    'installable': True,
}
