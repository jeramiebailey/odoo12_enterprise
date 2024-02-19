# -*- coding: utf-8 -*-
from odoo import http

# class UniPharmaReturnCustomers(http.Controller):
#     @http.route('/uni_pharma_return_customers/uni_pharma_return_customers/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/uni_pharma_return_customers/uni_pharma_return_customers/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('uni_pharma_return_customers.listing', {
#             'root': '/uni_pharma_return_customers/uni_pharma_return_customers',
#             'objects': http.request.env['uni_pharma_return_customers.uni_pharma_return_customers'].search([]),
#         })

#     @http.route('/uni_pharma_return_customers/uni_pharma_return_customers/objects/<model("uni_pharma_return_customers.uni_pharma_return_customers"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('uni_pharma_return_customers.object', {
#             'object': obj
#         })