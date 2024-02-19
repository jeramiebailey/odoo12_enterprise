{
    # Theme information
    'name': 'Emipro Theme Base',
    'category': 'Base',
    'summary': 'Base module containing common libraries for all Emipro eCommerce themes.',
    'version': '12.0.0.24',
    'license': 'OPL-1',	
    'depends': [
        'website_theme_install',
        'website_sale_wishlist',
        'website_sale_comparison',
        'website_blog',        
    ],

    'data': [
		'data/score_cron.xml',
		'security/ir.model.access.csv',
	    'views/website_menu_view.xml',
	    'views/product_label_view.xml',
        'views/slider.xml',
        'views/slider_filter.xml',
        'views/slider_styles.xml',
        'views/product_pricelist_item.xml',
        'views/res_company_view.xml',
        'views/product_brand_ept.xml',
        'views/product_template.xml',
        'views/product_rule_view.xml',
        'views/product_attribute.xml',
        'views/website.xml',
	    'views/template.xml',
	'views/social_sharing.xml',
    ],

    #Odoo Store Specific
    'images': [
        'static/description/emipro_theme_base.jpg',
    ],

    # Author
    'author': 'Emipro Technologies Pvt. Ltd.',
    'website': 'https://www.emiprotechnologies.com',
    'maintainer': 'Emipro Technologies Pvt. Ltd.',

    # Technical
    'installable': True,
    'auto_install': False,
    'price': 9.00,
    'currency': 'EUR', 
}
