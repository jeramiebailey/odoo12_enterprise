# Copyright 2019 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    'name': 'Panorama Sale',
    'summary': 'Panorama Sale Customizations',
    'version': '12.0.1.0.0',
    'category': 'Stock',
    'author': 'Eska',
    'website': 'http://www.eskayazilim.com.tr',
    'license': 'AGPL-3',
    'depends': [
        'sale_enterprise',
        'base_county',
        'sale_margin',
        'sale_crm',
    ],
    'data': [
        'views/sale_order_view.xml',
        'report/sale_report_view.xml',
        'report/sale_report_templates.xml',
        'report/sale_pro_forma_invoice_grouped_templates.xml',
    ],
    'installable': True,
    'auto_install': False,
}
