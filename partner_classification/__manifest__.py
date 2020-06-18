# Copyright 2015 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': 'Partner Classification',
    'summary': 'Add partner classification',
    'version': '12.0.1.0.0',
    'category': 'Extra Tools',
    'author': 'Eska',
    'website': 'http://www.eskayazilim.com.tr',
    'license': 'AGPL-3',
    'depends': [
        'contacts',
    ],
    'data': [
        "security/ir.model.access.csv",
        "views/res_partner_classification_view.xml",
        "views/res_partner_view.xml",
    ],
    'installable': True,
    'auto_install': False,
}
