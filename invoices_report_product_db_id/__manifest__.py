# Copyright 2016 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': 'Invoices Report Product db Id',
    'summary': 'Account Invoice Report Product Id in db',
    'version': '12.0.1.0.0',
    'category': 'Accounting',
    'author': 'doaa',
    'website': 'http://www.eskayazilim.com.tr',
    'license': 'AGPL-3',
    'depends': [
        'account',
    ],
    'data': [
        'report/account_invoice_report_view.xml',
    ],
    'installable': True,
    'auto_install': True,
}
