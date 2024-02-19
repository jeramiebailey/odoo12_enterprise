
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    'name': 'Panorama CRM',
    'summary': 'Panorama CRM',
    'version': '12.0.1.0.0',
    'category': 'CRM',
    'author': 'JB',
    'license': 'AGPL-3',
    'depends': [
        'sale_crm',
        'sale_order_archive',
    ],
    'data': [
        'views/sale_order_view.xml',
        'views/crm_lead_views.xml',
    ],
    'installable': True,
    'auto_install': False,
}
