# -*- coding: utf-8 -*-
from odoo import http

# class PanoramaFixedToRefund(http.Controller):
#     @http.route('/panorama_fixed_to_refund/panorama_fixed_to_refund/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/panorama_fixed_to_refund/panorama_fixed_to_refund/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('panorama_fixed_to_refund.listing', {
#             'root': '/panorama_fixed_to_refund/panorama_fixed_to_refund',
#             'objects': http.request.env['panorama_fixed_to_refund.panorama_fixed_to_refund'].search([]),
#         })

#     @http.route('/panorama_fixed_to_refund/panorama_fixed_to_refund/objects/<model("panorama_fixed_to_refund.panorama_fixed_to_refund"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('panorama_fixed_to_refund.object', {
#             'object': obj
#         })