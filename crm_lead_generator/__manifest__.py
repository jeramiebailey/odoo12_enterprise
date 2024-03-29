
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    'name': 'Lead Generator',
    'summary': 'This module automatically generates leads by given schedule',
    'version': '12.0.1.0.0',
    'category': 'CRM',
    'author': 'JB',
    'license': 'AGPL-3',
    'depends': [
        'crm',
    ],
    'data': [
        'wizard/lead_generator_view.xml',
        'views/crm_view.xml',
        'views/res_partner_view.xml',
    ],
    'installable': True,
    'auto_install': False,
}
