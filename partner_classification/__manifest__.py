{
    'name': 'Partner Classification',
    'summary': 'Add partner classification',
    'version': '12.0.1.0.0',
    'category': 'Extra Tools',
    'author': 'JB',
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
