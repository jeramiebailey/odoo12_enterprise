
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    'name': 'Purchase Scheduled Date Mass Change',
    'summary': 'Purchase Scheduled Date Mass Change',
    'version': '12.0.1.0.0',
    'category': 'Purchase',
    'author': 'JB',
    'license': 'AGPL-3',
    'depends': [
        'purchase',
    ],
    'data': [
        'wizard/purchase_order_wizard_view.xml',
        'views/purchase_order_view.xml',
    ],
    'installable': True,
    'auto_install': False,
}
