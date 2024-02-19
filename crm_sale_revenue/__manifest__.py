
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    'name': 'CRM Sale Revenue',
    'summary': 'Crm lead actual sale revenue',
    'version': '12.0.1.0.0',
    'category': 'CRM',
    'author': 'JB',
    'license': 'AGPL-3',
    'depends': [
        'sale_crm',
    ],
    'data': [
        'views/crm_lead_view.xml',
    ],
    'installable': True,
    'auto_install': False,
}
