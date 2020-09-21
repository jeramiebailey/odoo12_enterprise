# -*- coding: utf-8 -*-
from odoo import http

# class PanoramaOrderLineReport(http.Controller):
#     @http.route('/panorama_order_line_report/panorama_order_line_report/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/panorama_order_line_report/panorama_order_line_report/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('panorama_order_line_report.listing', {
#             'root': '/panorama_order_line_report/panorama_order_line_report',
#             'objects': http.request.env['panorama_order_line_report.panorama_order_line_report'].search([]),
#         })

#     @http.route('/panorama_order_line_report/panorama_order_line_report/objects/<model("panorama_order_line_report.panorama_order_line_report"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('panorama_order_line_report.object', {
#             'object': obj
#         })