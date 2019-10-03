# Copyright 2019 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    'name': 'Partner Sales Permit Number',
    'summary': 'Partner Sales Permit Number',
    'version': '12.0.1.0.0',
    'category': 'Web',
    'author': 'Eska',
    'website': 'http://www.eskayazilim.com.tr',
    'license': 'AGPL-3',
    'depends': [
        'partner_identification',
    ],
    'data': [
        'data/res_partner_id_category_data.xml',
        'views/res_partner_view.xml'
    ],
    'installable': True,
}
