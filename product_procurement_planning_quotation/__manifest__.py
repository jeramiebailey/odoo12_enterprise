
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    'name': 'Products Procurement Report Quotation',
    'summary': 'Report for Planning Procurements Quotation',
    'version': '12.0.1.0.0',
    'category': 'Project',
    'author': 'JB',
    'license': 'AGPL-3',
    'depends': [
        'product_missing_quotation',
        'product_procurement_planning',
    ],
    'data': [
         'views/product_product_view.xml',
    ],
    'installable': True,
    'auto_install': False,
}
