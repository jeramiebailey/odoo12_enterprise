
import odoo.addons.decimal_precision as dp
from odoo import api, models, fields


class StockManageVariant(models.TransientModel):
    _name = 'inventory.manage.variant'
    _description = 'Add or modify variants on stock inventory lines'

    product_tmpl_id = fields.Many2one(
        comodel_name='product.template', string="Template", required=True)
    variant_line_ids = fields.Many2many(
        comodel_name='inventory.manage.variant.line', string="Variant Lines")

    def _get_product_variant(self, value_x, value_y):
        """Filter the corresponding product for provided values."""
        self.ensure_one()
        values = value_x
        if value_y:
            values += value_y
        return self.product_tmpl_id.product_variant_ids.filtered(
            lambda x: not (values - x.attribute_value_ids)
        )[:1]

    @api.onchange('product_tmpl_id')
    def _onchange_product_tmpl_id(self):
        self.variant_line_ids = [(6, 0, [])]
        template = self.product_tmpl_id
        context = self.env.context
        record = self.env[context['active_model']].browse(
            context['active_id'])
        if context['active_model'] == 'stock.inventory.line':
            inventory = record.inventory_id
        else:
            inventory = record
        attr_lines = template.attribute_line_ids.filtered(
            lambda x: x.attribute_id.create_variant != 'no_variant'
        )
        num_attrs = len(attr_lines)
        if not template or not num_attrs or num_attrs > 2:
            return
        line_x = attr_lines[0]
        line_y = False if num_attrs == 1 else attr_lines[1]
        lines = []
        for value_x in line_x.value_ids:
            for value_y in line_y and line_y.value_ids or [False]:
                product = self._get_product_variant(value_x, value_y)
                if not product:
                    continue
                inventory_line = inventory.line_ids.filtered(
                    lambda x: x.product_id == product
                )[:1]
                lines.append((0, 0, {
                    'value_x': value_x,
                    'value_y': value_y,
                    'product_qty': inventory_line.product_qty,
                }))
        self.variant_line_ids = lines

    @api.multi
    def button_transfer_to_picking(self):
        context = self.env.context
        record = self.env[context['active_model']].browse(context['active_id'])
        if context['active_model'] == 'stock.inventory.line':
            inventory = record.inventory_id
        else:
            inventory = record
        InventoryLine = self.env['stock.inventory.line']
        lines2unlink = InventoryLine
        for line in self.variant_line_ids:
            product = self._get_product_variant(line.value_x, line.value_y)
            inventory_line = inventory.line_ids.filtered(
                lambda x: x.product_id == product
            )
            if inventory_line:
                if not line.product_qty:
                    # Done this way because there's a side effect removing here
                    lines2unlink |= inventory_line
                else:
                    inventory_line.product_qty = line.product_qty
            elif line.product_qty:
                vals = InventoryLine.default_get(InventoryLine._fields.keys())
                vals.update({
                    'product_id': product.id,
                    'product_uom': product.uom_id,
                    'product_qty': line.product_qty,
                    'inventory_id': inventory.id,
                    'location_id': inventory.location_id,
                })
                inventory_line = InventoryLine.new(vals)
                inventory_line.with_context(
                    partner_id=inventory.partner_id.id
                )._onchange_product()
                stock_inventory_vals = inventory_line._convert_to_write(
                    inventory_line._cache)
                inventory.line_ids.browse().create(stock_inventory_vals)
        lines2unlink.unlink()


class StockManageVariantLine(models.TransientModel):
    _name = 'inventory.manage.variant.line'
    _description = 'Define variants quantities on stock picking lines'

    value_x = fields.Many2one(comodel_name='product.attribute.value')
    value_y = fields.Many2one(comodel_name='product.attribute.value')
    product_qty = fields.Float(
        string="Quantity", digits=dp.get_precision('Product UoS'))
