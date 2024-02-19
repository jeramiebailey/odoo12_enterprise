
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    'name': 'Products Incoming',
    'summary': 'Incoming Products',
    'version': '12.0.1.0.0',
    'category': 'Project',
    'author': 'JB',
    'license': 'AGPL-3',
    'depends': [
         'purchase_order_archive',
    ],
    'data': [
         'views/product_product_view.xml',
         'views/purchase_order_line_view.xml',
    ],
    'installable': True,
    'auto_install': False,
}

