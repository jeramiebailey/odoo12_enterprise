{
    'name': 'POS Workflow Base',
    'version': '12.0.1.8',
    'summary': """POS Workflow Base""",
    'description': """
POS Workflow Base
=================

Base module for POS workflows, returns and import
""",
    'category': 'Hidden',
    'author': 'MAC5',
    'contributors': ['Michael Aldrin C. Villamar'],
    'website': 'https://apps.odoo.com/apps/modules/browse?author=MAC5',
    'depends': [
        'point_of_sale',
        'sale',
    ],
    'data': [
        'views/pos_config_views.xml',
        'views/pos_templates.xml',
    ],
    'demo': [],
    'qweb': ['static/src/xml/pos_workflow_base.xml'],
    'installable': True,
    'application': False,
    'auto_install': False,
}