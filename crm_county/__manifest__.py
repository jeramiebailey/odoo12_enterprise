# Copyright 2021 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    'name': 'CRM County/Province',
    'summary': 'Adds county/province to CRM Lead',
    'version': '12.0.1.0.0',
    'category': 'Localization',
    'author': 'Eska',
    'website': 'http://www.eskayazilim.com.tr',
    'license': 'AGPL-3',
    'depends': [
        'crm',
    ],
    'data': [
        'views/crm_lead_view.xml',
    ],
    'installable': True,
    'auto_install': False,
}


