# Copyright 2019 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': 'Purchase Order Total Quantity',
    'summary': 'Adds Total Quantity on Purchase Orders',
    'version': '12.0.1.0.0',
    'category': 'Purchase',
    'author': 'Eska',
    'website': 'http://www.eskayazilim.com.tr',
    'license': 'AGPL-3',
    'depends': [
        'purchase',
    ],
    'data': [
        'views/purchase_order_view.xml',
        'views/purchase_report_templates.xml',
    ],
    'installable': True,
}
