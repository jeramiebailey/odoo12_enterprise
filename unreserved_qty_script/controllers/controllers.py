# -*- coding: utf-8 -*-
from odoo import http

# class UnreservedQtyScript(http.Controller):
#     @http.route('/unreserved_qty_script/unreserved_qty_script/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/unreserved_qty_script/unreserved_qty_script/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('unreserved_qty_script.listing', {
#             'root': '/unreserved_qty_script/unreserved_qty_script',
#             'objects': http.request.env['unreserved_qty_script.unreserved_qty_script'].search([]),
#         })

#     @http.route('/unreserved_qty_script/unreserved_qty_script/objects/<model("unreserved_qty_script.unreserved_qty_script"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('unreserved_qty_script.object', {
#             'object': obj
#         })