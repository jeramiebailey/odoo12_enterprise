# Copyright 2021 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Panorama Pos',
    'summary': 'Panorama Accounting Customizations',
    'version': '12.0.1.0.0',
    'category': 'Point of Sale',
    'author': 'Eska',
    'website': 'http://www.eskayazilim.com.tr',
    'license': 'AGPL-3',
    'depends': [
        'point_of_sale',
    ],
    'qweb': [
        'static/src/xml/pos_templates.xml',
    ],
    'installable': True,
    'auto_install': True,
}
