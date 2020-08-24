# Copyright 2019 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': 'Sale Report Cost',
    'summary': 'Add cost to Sale report.',
    'version': '12.0.1.0.0',
    'category': 'Sales',
    'author': 'doaa',
    'depends': [
        'base','sale','sale_enterprise'
    ],
    'data': [
        'report/sale_report_view.xml',
    ],
    'installable': True,
    'auto_install': False,
}
