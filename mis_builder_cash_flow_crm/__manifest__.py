
{
    'name': 'Mis Builder Cash Flow CRM',
    'summary': 'Mis Builder Cash Flow CRM',
    'version': '12.0.1.0.0',
    'category': 'Reporting',
    'author': 'JB',
    'license': 'AGPL-3',
    'depends': [
        'crm',
        'mis_builder_cash_flow',
    ],
    'data': [
        'views/crm_lead_view.xml',
        'views/mis_cash_flow_forecast_line_view.xml',
    ],
    'installable': True,
    'auto_install': True,
}
