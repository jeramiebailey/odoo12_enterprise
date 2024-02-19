# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    'name': 'Panorama Account',
    'summary': 'Panorama Accounting Customizations',
    'version': '12.0.1.0.0',
    'category': 'Accounting',
    'author': 'JB',
    'license': 'AGPL-3',
    'depends': [
        'account',
        'partner_sales_permit_no',
        'partner_tobacco_license_no',
    ],
    'data': [
        'views/report_invoice.xml',
        'views/account_invoice_view.xml',
    ],
    'installable': True,
    'auto_install': False,
}
