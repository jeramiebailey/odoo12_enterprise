from odoo import _, api, fields, models
from odoo.exceptions import UserError
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError
from datetime import datetime
import datetime
from odoo.exceptions import Warning


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    license_validity_date_notes = fields.Text(readonly=True, copy=False)
    check_license_validity_date_notes = fields.Boolean(copy=False)

    @api.multi
    @api.onchange('partner_id')
    def _check_license_validity_date_notes(self):
        for rec in self:
            if rec.partner_id.tobacco_license_validity_date:
                days_number = datetime.date.today() - rec.partner_id.tobacco_license_validity_date
                if days_number.days >= 30:
                    rec.license_validity_date_notes = "Attention your license validity date is expired"
                    rec.check_license_validity_date_notes = True
                    res = {'warning': {
                        'title': _('Warning'),
                        'message': _('Attention your license validity date is expired.'), }}
                    if res:
                        return res


                else:
                    date_of_expire = rec.partner_id.tobacco_license_validity_date + datetime.timedelta(days=30)
                    print("date_of_expire", date_of_expire)
                    rec.license_validity_date_notes = "Note that your license validity date till date " + str(
                        date_of_expire)
                    rec.check_license_validity_date_notes = False
                    res = {'warning': {
                        'title': _('Warning'),
                        'message': _('Note that your license validity date till date %s.') % (
                            date_of_expire)}}
                    if res:
                        return res
            else:
                rec.license_validity_date_notes = ""
                rec.check_license_validity_date_notes = False

    @api.multi
    def _prepare_invoice(self):
        res = super(SaleOrder, self)._prepare_invoice()
        print("invoice_valsinvoice_valsinvoice_valsinvoice_vals", res)
        res.update({'license_validity_date_notes': self.license_validity_date_notes,
                    'check_license_validity_date_notes': self.check_license_validity_date_notes,
                    })
        return res

class SaleAdvancePaymentInv(models.TransientModel):
    _inherit = "sale.advance.payment.inv"

    @api.multi
    def _create_invoice(self, order, so_line, amount):
        res = super(SaleAdvancePaymentInv, self)._create_invoice(order, so_line, amount)
        print("order, so_line, amount", res)
        res.update({'license_validity_date_notes': order.license_validity_date_notes,
                    'check_license_validity_date_notes': order.check_license_validity_date_notes,
                    })
        return res
