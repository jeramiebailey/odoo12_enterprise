# Copyright 2019 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': 'Stock Picking Total Quantity',
    'summary': 'Adds Total Quantity on Stock Picking',
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
        'views/report_deliveryslip.xml',
    ],
    'installable': True,
}
