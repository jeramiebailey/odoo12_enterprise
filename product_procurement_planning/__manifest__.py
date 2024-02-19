
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    'name': 'Products Procurement Report',
    'summary': 'Report for Planning Procurements',
    'version': '12.0.1.0.0',
    'category': 'Project',
    'author': 'JB',
    'license': 'AGPL-3',
    'depends': [
        'product_missing_sale',
        'product_incoming_purchase',
    ],
    'data': [
         'views/product_product_view.xml',
    ],
    'installable': True,
    'auto_install': False,
}

