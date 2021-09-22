# Copyright 2018 Clonera
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'CRM Opportunity Partner Required',
    'summary': 'Require partner on Opportunity',
    'version': '12.0.1.0.0',
    'category': 'CRM',
    'author': 'Clonera',
    'website': 'http://www.clonera.net',
    'license': 'AGPL-3',
    'depends': [
       'crm',
    ],
    'data': [
        'views/crm_lead_view.xml',
    ],
    'installable': True,
}
