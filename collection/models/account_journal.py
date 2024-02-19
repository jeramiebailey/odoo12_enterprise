
from odoo import fields, models


class AccountJournal(models.Model):
    _inherit = "account.journal"

    use_in_collections = fields.Boolean(
        string='Use in collections',
    )
