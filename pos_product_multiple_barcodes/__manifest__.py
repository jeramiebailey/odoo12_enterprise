
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    'name': 'POS Product Multiple Barcodes',
    'summary': 'POS Product Multiple Barcodes',
    'version': '12.0.1.0.0',
    'category': 'Point of Sale',
    'author': 'JB',
    'license': 'AGPL-3',
    'depends': [
        'point_of_sale',
        'product_multiple_barcodes',
    ],
    'data': [
        'views/assets.xml',
        'views/product_product_view.xml',
    ],
    'installable': True,
    'auto_install': False,
}
