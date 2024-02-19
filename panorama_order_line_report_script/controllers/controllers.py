# -*- coding: utf-8 -*-
from odoo import http

# class PanoramaOrderLineReportScript(http.Controller):
#     @http.route('/panorama_order_line_report_script/panorama_order_line_report_script/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/panorama_order_line_report_script/panorama_order_line_report_script/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('panorama_order_line_report_script.listing', {
#             'root': '/panorama_order_line_report_script/panorama_order_line_report_script',
#             'objects': http.request.env['panorama_order_line_report_script.panorama_order_line_report_script'].search([]),
#         })

#     @http.route('/panorama_order_line_report_script/panorama_order_line_report_script/objects/<model("panorama_order_line_report_script.panorama_order_line_report_script"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('panorama_order_line_report_script.object', {
#             'object': obj
#         })