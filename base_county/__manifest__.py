# Copyright 2021 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    'name': 'County/Province',
    'summary': 'Adds another administrative district under state',
    'version': '12.0.1.0.0',
    'category': 'Localization',
    'author': 'Eska',
    'website': 'http://www.eskayazilim.com.tr',
    'license': 'AGPL-3',
    'depends': [],
    'data': [
        'security/ir.model.access.csv',
        'views/res_company_view.xml',
        'views/res_partner_view.xml',
        'views/res_county_view.xml',
    ],
    'installable': True,
    'auto_install': False,
}
