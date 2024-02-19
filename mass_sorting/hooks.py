# Copyright 2016 Serpent Consulting Services Pvt. Ltd. (support@serpentcs.com)

from odoo.api import Environment, SUPERUSER_ID


def uninstall_hook(cr, registry):
    """Delete the actions that were created with mass_sorting when
    the module is uninstalled"""
    env = Environment(cr, SUPERUSER_ID, {})
    env['ir.actions.act_window'].search([
        ('res_model', '=', 'mass.sort.wizard')
    ]).unlink()
    return True
