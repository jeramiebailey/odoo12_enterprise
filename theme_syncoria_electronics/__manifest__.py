# -*- coding: utf-8 -*-
#################################################################################
# Author      : Syncoria Inc (<https://www.syncoria.com/>)
# Copyright(c): 2004-Present Syncoria Inc
# All Rights Reserved.
#
#
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#
#################################################################################

{
    'name': 'esync',
	'summary': 'eCommerce theme for electronics business',
	'description': 'Theme for Electronics Business',
	'category': 'Theme',
	'author': "Syncoria Inc.",
    'website': "https://www.syncoria.com",
    'company': 'Syncoria Inc.',
    'maintainer': 'Syncoria Inc.',
	'version': '12.0.1.0.0',
	'depends': ['website', 'website_theme_install', 'website_sale', 'website_sale_comparison', 'website_sale_wishlist'],
    'data': [
        'security/ir.model.access.csv',
        'data/data.xml',
        'views/templates.xml',
        'views/category_slide.xml',
        'views/inherit_template.xml',
        'views/snippets_bestsellers.xml',
        'views/snippets_brandblocks.xml',
        'views/snippets_topproduct.xml',
        'views/snippets_dealsweek.xml',
        'views/snippets_features.xml',
        'views/snippets_newsletter.xml',
        'views/snippets_info.xml',
        'views/recentlyviewed.xml',
        'views/snippets_specialoffers.xml',
        'views/snippets_topfeatures.xml',
        'views/syncoria_product_list.xml',
        'views/product.xml',
        'views/website_view.xml'
    ],
    'images': [
	    'static/description/banner.png',
        'static/description/theme_syncoria_electronics_screenshot.png',
	],
    'live_test_url': "http://esyncdemo.syncoria.com/",
	'price': 50,
    'currency': 'USD',
    'license': 'OPL-1',
    'support': "support@syncoria.com",
	'application': False,
	"installable": True,
    
}
