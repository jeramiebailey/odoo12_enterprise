# -*- coding: utf-8 -*-
#################################################################################
#
#   Copyright (c) 2016-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#   See LICENSE file for full copyright and licensing details.
#   License URL : <https://store.webkul.com/license.html/>
# 
#################################################################################
from odoo import api, fields,models

class PosConfig(models.Model):
	_inherit = 'pos.config'

	on_product_line = fields.Boolean('Add notes to individual orderlines', default=True)
	on_order = fields.Boolean('Add note to the complete order', default=True)
	receipt_order_note = fields.Boolean('Print notes on the receipt', default=True)
	note_keyword_limit = fields.Integer(string="Note Keywords Limit")
	set_note_keyword_limit = fields.Boolean()

class PosOrder(models.Model):
	_inherit = 'pos.order'

	@api.model
	def _order_fields(self,ui_order):
		fields_return = super(PosOrder,self)._order_fields(ui_order)
		fields_return.update({'note':ui_order.get('order_note','')})
		return fields_return

class PosOrderLine(models.Model):
	_inherit = 'pos.order.line'
	order_line_note = fields.Text('Extra Comments')

	@api.model
	def _order_line_fields(self, line, session_id=None):
		fields_return = super(PosOrderLine,self)._order_line_fields(line,session_id=None)
		fields_return[2].update({'order_line_note':line[2].get('order_line_note','')})
		return fields_return