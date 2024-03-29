# Copyright (C) 2016-Today GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)

from odoo import fields, models


class TransientModelLine(models.TransientModel):
    _name = 'mass.sort.wizard.line'

    sequence = fields.Integer(string='Sequence', required=True, default=1)

    wizard_id = fields.Many2one(
        comodel_name='mass.sort.wizard', string='Wizard')

    field_id = fields.Many2one(
        comodel_name='ir.model.fields', string='Field', required=True,
        domain="[('model', '=', parent.one2many_model)]")

    desc = fields.Boolean('Inverse Order')
