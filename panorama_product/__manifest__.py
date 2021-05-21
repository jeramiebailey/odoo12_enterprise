# Copyright 2019 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    'name': 'Panorama Product',
    'summary': 'Panorama Product Customizations',
    'version': '12.0.3.0.0',
    'category': 'Product',
    'author': 'Eska',
    'website': 'http://www.eskayazilim.com.tr',
    'license': 'AGPL-3',
    'depends': [
        'stock',
        'product_variant_sale_price',
    ],
    'data': [
        'views/product_template_view.xml',
        'views/product_product_view.xml',
        'report/barcode_print_templates.xml',
    ],
    'installable': True,
    'auto_install': False,
}
