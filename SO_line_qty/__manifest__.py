
{
    'name': 'Sale Order Line Quantity',
    'version': '12.0.1.0.0',
    'category': 'Stock',
    'license': 'AGPL-3',
    'depends': [
        'sale','product_margin', 'sales_team', 'panorama_sale_margin_group',
    ],
    'data': [
        'views/stock_picking_view.xml',
    ],
    'installable': True,
}
