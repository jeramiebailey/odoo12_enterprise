# Copyright 2016-2018 Tecnativa - Pedro M. Baeza
# Copyright 2019 Eska
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Handle easily multiple variants on Purchase Orders',
    'summary': 'Handle the addition/removal of multiple variants from '
               'product template into the purchase order',
    'version': '12.0.1.0.0',
    'author': 'Eska,'
              'Odoo Community Association (OCA)',
    'category': 'Purchase',
    'license': 'AGPL-3',
    'website': 'https://www.eskayazilim.com.tr',
    'depends': [
        'purchase',
        'web_widget_x2many_2d_matrix',
    ],
    'demo': [],
    'data': [
        'wizard/purchase_manage_variant_view.xml',
        'views/purchase_order_view.xml',
    ],
    'installable': True,
}
