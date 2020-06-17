# Copyright 2019 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    'name': 'Panorama Purchase',
    'summary': 'Panorama Purchase Customizations',
    'version': '12.0.1.0.0',
    'category': 'Stock',
    'author': 'Eska',
    'website': 'http://www.eskayazilim.com.tr',
    'license': 'AGPL-3',
    'depends': [
        'purchase',
    ],
    'data': [
        'report/purchase_quotation_templates.xml',
        'views/purchase_order_view.xml',
    ],
    'installable': True,
    'auto_install': False,
}