# Copyright 2018 Clonera

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
