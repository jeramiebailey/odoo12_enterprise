# Copyright 2019 Bonainfo (www.bonainfo.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class BaseImport(models.TransientModel):
    _inherit = "base_import.import"

    @api.multi
    def do(self, fields, columns, options, dryrun=False):
        return super(
            BaseImport,
            self.with_context(dryrun=dryrun,
                              import_one2many=options.get(
                                  'import_one2many'))
        ).do(fields, columns, options, dryrun)

    @api.model
    def _convert_import_data(self, fields, options):
        data, fields = super(BaseImport, self)._convert_import_data(
            fields, options)
        if self._context.get('import_one2many'):
            parent_field = options.get('parent_field')
            parent_id = options.get('parent_id')
            if parent_field and parent_id:
                fields.append(parent_field)
                for row in data:
                    row.append(parent_id)
        return data, fields
