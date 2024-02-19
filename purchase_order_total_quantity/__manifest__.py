{
    'name': 'Purchase Order Total Quantity',
    'summary': 'Adds Total Quantity on Purchase Orders',
    'version': '12.0.1.0.0',
    'category': 'Purchase',
    'author': 'JB',
    'license': 'AGPL-3',
    'depends': [
        'purchase',
    ],
    'data': [
        'views/purchase_order_view.xml',
        'views/purchase_report_templates.xml',
    ],
    'installable': True,
}
