# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) 2017-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# See LICENSE file for full copyright and licensing details.
# License URL : <https://store.webkul.com/license.html/>
##############################################################################


from odoo import _, api, fields, models
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _name = 'sale.order'
    _inherit = ['sale.order', 'barcodes.barcode_events_mixin']

    def on_barcode_scanned(self, barcode):
        product = self.env['product.product'].search(
            ['|',('barcode', '=', barcode),('default_code', '=', barcode)]
            , limit=1)
        if product:
            order_lines = self.order_line.filtered(
                lambda r: r.product_id == product)
            if order_lines:
                order_line = order_lines[0]
                qty = order_line.product_uom_qty
                order_line.product_uom_qty = qty + 1
            else:
                newId = self.order_line.new({
                    'product_id': product.id,
                    'product_uom_qty': 1,
                    'price_unit': product.lst_price
                })
                self.order_line += newId
                newId.product_id_change()
        else:
            raise UserError(
                _('Scanned barcode %s is not related to any product.') %
                barcode)

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def get_barcode_view_state(self):
        """ Return the initial state of the barcode view as a dict.
        """
        fields_to_read = self._get_picking_fields_to_read()
        pickings = self.read(fields_to_read)
        for picking in pickings:
            picking['move_line_ids'] = self.env['stock.move.line'].browse(picking.pop('move_line_ids')).read([
                'product_id',
                'location_id',
                'location_dest_id',
                'qty_done',
                'display_name',
                'product_uom_qty',
                'product_uom_id',
                'product_barcode',
                'owner_id',
                'lot_id',
                'lot_name',
                'package_id',
                'result_package_id',
                'dummy_id',
            ])
            for move_line_id in picking['move_line_ids']:
                move_line_id['product_id'] = self.env['product.product'].browse(move_line_id.pop('product_id')[0]).read([
                    'id',
                    'tracking',
                    'barcode',
                ])[0]
                move_line_id['location_id'] = self.env['stock.location'].browse(move_line_id.pop('location_id')[0]).read([
                    'id',
                    'display_name',
                ])[0]
                move_line_id['location_dest_id'] = self.env['stock.location'].browse(move_line_id.pop('location_dest_id')[0]).read([
                    'id',
                    'display_name',
                ])[0]
            picking['location_id'] = self.env['stock.location'].browse(picking.pop('location_id')[0]).read([
                'id',
                'display_name',
                'parent_path'
            ])[0]
            picking['location_dest_id'] = self.env['stock.location'].browse(picking.pop('location_dest_id')[0]).read([
                'id',
                'display_name',
                'parent_path'
            ])[0]
            picking['group_stock_multi_locations'] = self.env.user.has_group('stock.group_stock_multi_locations')
            picking['group_tracking_owner'] = self.env.user.has_group('stock.group_tracking_owner')
            picking['group_tracking_lot'] = self.env.user.has_group('stock.group_tracking_lot')
            picking['group_production_lot'] = self.env.user.has_group('stock.group_production_lot')
            picking['group_uom'] = self.env.user.has_group('uom.group_uom')
            picking['use_create_lots'] = self.env['stock.picking.type'].browse(picking['picking_type_id'][0]).use_create_lots
            picking['use_existing_lots'] = self.env['stock.picking.type'].browse(picking['picking_type_id'][0]).use_existing_lots
            picking['show_entire_packs'] = self.env['stock.picking.type'].browse(picking['picking_type_id'][0]).show_entire_packs
            picking['actionReportDeliverySlipId'] = self.env.ref('stock.action_report_delivery').id
            if self.env.user.company_id.nomenclature_id:
                picking['nomenclature_id'] = [self.env.user.company_id.nomenclature_id.id]
        return pickings