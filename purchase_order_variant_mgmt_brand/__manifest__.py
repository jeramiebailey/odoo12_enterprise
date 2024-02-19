{
    'name': 'Purchase Variant Manage Brand',
    'summary': 'Adds brand filter to purchase variant management wizard',
    'version': '12.0.1.0.0',
    'category': 'Sale',
    'author': 'JB',
    'license': 'AGPL-3',
    'depends': [
        'product_brand',
        'purchase_order_variant_mgmt',
    ],
    'data': [
        'wizard/purchase_manage_variant_view.xml',
    ],
    'installable': True,
}
