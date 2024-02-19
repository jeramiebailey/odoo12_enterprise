
{
    'name': 'Partner Route',
    'summary': 'Add partner route',
    'version': '12.0.1.0.0',
    'category': 'Extra Tools',
    'author': 'JB',
    'license': 'AGPL-3',
    'depends': [
        'sale_crm',
    ],
    'data': [
        "security/ir.model.access.csv",
        "views/res_partner_route_view.xml",
        "views/res_partner_view.xml",
        "views/sale_order_view.xml",
        "views/crm_lead_view.xml",
    ],
    'installable': True,
    'auto_install': False,
}
