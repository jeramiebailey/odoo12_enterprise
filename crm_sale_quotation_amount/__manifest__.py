# Copyright 2022 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    'name': 'CRM Sale Quotation Amount',
    'summary': 'Crm sale amount of quotation',
    'version': '12.0.1.0.0',
    'category': 'CRM',
    'author': 'Eska',
    'website': 'http://www.eskayazilim.com.tr',
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
