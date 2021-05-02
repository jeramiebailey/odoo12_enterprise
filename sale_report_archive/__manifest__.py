# Copyright 2021 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': 'Sale Report Archive',
    'summary': 'Adds Active Field on Sale Report',
    'version': '12.0.1.0.0',
    'category': 'Stock',
    'author': 'Eska',
    'website': 'http://www.eskayazilim.com.tr',
    'license': 'AGPL-3',
    'depends': [
        'sale_order_archive',
    ],
    'data': [
        'report/sale_report_view.xml',
    ],
    'installable': True,
}
