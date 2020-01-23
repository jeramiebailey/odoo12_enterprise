# Copyright 2019 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    'name': 'Panorama Stock',
    'summary': 'Panorama Stock Customizations',
    'version': '12.0.1.0.0',
    'category': 'Stock',
    'author': 'Eska',
    'website': 'http://www.eskayazilim.com.tr',
    'license': 'AGPL-3',
    'depends': [
        'stock',
    ],
    'data': [
        'views/stock_picking_view.xml',
        'report/report_deliveryslip.xml',
        'report/report_stockpicking_operations.xml',
    ],
    'installable': True,
    'auto_install': False,
}
