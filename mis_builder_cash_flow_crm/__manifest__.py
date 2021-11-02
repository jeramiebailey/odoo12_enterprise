# Copyright 2021 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': 'Mis Builder Cash Flow CRM',
    'summary': 'Mis Builder Cash Flow CRM',
    'version': '12.0.1.0.0',
    'category': 'Reporting',
    'author': 'Eska',
    'website': 'http://www.eskayazilim.com.tr',
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
