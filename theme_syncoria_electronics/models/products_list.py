
# -*- coding: utf-8 -*-
###############################################################################
#    License, author and contributors information in:                         #
#    __manifest__.py file at the root folder of this module.                  #
###############################################################################

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class SyncoriaProductList(models.Model):
    _name = 'syncoria.product.list'
    _description = u'Theme Product Lists'

    _rec_name = 'name'
    _order = 'sequence,name ASC'

    name = fields.Char(required=True, copy=False)
    sequence = fields.Integer(default=0)

    line_ids = fields.One2many(
        comodel_name='syncoria.product.list.line',
        inverse_name='list_id',
    )


class SyncoriaProductListLine(models.Model):
    _name = 'syncoria.product.list.line'
    _description = u'Theme Product List Items'

    _rec_name = 'product_id'
    _order = 'sequence,product_id ASC'

    sequence = fields.Integer(default=0)
    list_id = fields.Many2one(
        string=u'List',
        comodel_name='syncoria.product.list',
        ondelete='cascade'
    )
    product_id = fields.Many2one(
        string=u'Product',
        comodel_name='product.template',
        ondelete='set null',
        required=True
    )
