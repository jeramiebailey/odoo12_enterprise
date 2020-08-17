# -*- encoding: utf-8 -*-
{
    'name': 'Payment Info',
    'version': '12.0',
    'category': 'Account',
    'description': """
     Payment Info
    """,
    'summary': 'Employee Contract Sequence',
    'author': "ITSYS Doaa",
    'website': "http://www.itsyscorp.com",
    'images': ['static/description/icon.png'],
    'data': [

        'views/account_payment_view.xml',
    ],
    'depends': ['base', 'account'],
    'installable': True,
    'auto_install': False,
    'application': True,
    'WBS': 'ECUSA-21',

}
