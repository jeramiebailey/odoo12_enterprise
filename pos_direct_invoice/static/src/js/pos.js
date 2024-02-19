odoo.define('pos_direct_invoice.pos', function (require) {
    "use strict";
    var core = require('web.core');
    var _t = core._t;
    var screens = require('point_of_sale.screens');
    screens.PaymentScreenWidget.include({
        finalize_validation: function () {
            var self = this;
            var order = this.pos.get_order();

            if (order.is_paid_with_cash() && this.pos.config.iface_cashdrawer) {

                this.pos.proxy.open_cashbox();
            }

            order.initialize_validation_date();
            order.finalized = true;
            var paymentlines = this.pos.get_order().get_paymentlines();
            var bool_cash_found = false;
            for (var item in paymentlines) {
                var jr_type = paymentlines[item].cashregister.journal.type;
                if (jr_type === 'cash') {
                    bool_cash_found = true;
                    break;
                }
            }
            if (order.is_to_invoice() || (this.pos.config.auto_invoice_cash && bool_cash_found)) {
                var invoiced = this.pos.push_and_invoice_order(order);
                this.invoicing = true;

                invoiced.fail(this._handleFailedPushForInvoice.bind(this, order, false));

                invoiced.done(function () {
                    self.invoicing = false;
                    self.gui.show_screen('receipt');
                });
            } else {
                this.pos.push_order(order);
                this.gui.show_screen('receipt');
            }

        },

    });

});
