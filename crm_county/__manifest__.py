
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    'name': 'CRM County/Province',
    'summary': 'Adds county/province to CRM Lead',
    'version': '12.0.1.0.0',
    'category': 'Localization',
    'author': 'JB',
    'license': 'AGPL-3',
    'depends': [
        'crm',
        'base_county',
    ],
    'data': [
        'views/crm_lead_view.xml',
    ],
    'installable': True,
    'auto_install': False,
}


