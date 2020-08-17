# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

{
    'name' : "create Purchase from Sales Order",
    'version' : "13.0.0.1",
    'category' : "Purchases",
    'summary': 'This apps helps to Covert Purchase order from Sales Order',
    'description' : """create Purchase from Sales Order

     """,
    'author' : "Said yahia",
    'wbs'  : "ECUSA-20",
    'depends'  : [ 'base','sale_management','purchase'],
    'data'     : [
                    'views/inherit_sale_order_view.xml',
            ],      
    'installable' : True,
    'application' :  False,
}
