odoo.define('pos_workflow.pos_workflow', function (require) {
"use strict";

var core = require('web.core');
var models = require('point_of_sale.models');
var rpc = require('web.rpc');
var workflow_base = require('pos_workflow_base.pos_workflow_base');

var _t = core._t;


var _super_order = models.Order.prototype;
models.Order = models.Order.extend({
    initialize: function(attr, options) {
        var result = _super_order.initialize.apply(this, arguments);
        this.date_order = false;
        this.sale_order_name = false;
        this.purchase_order_name = false;
        this.partner_ref = false;
        this.notes = false;
        return result;
    },
});


workflow_base.POSWorkflowPopup.include({
    renderElement: function () {
        this._super();
        var self = this;
        var order = this.pos.get_order();

        if (document.getElementById("workflow-date")) {
            document.getElementById("workflow-date").valueAsDate = new Date()
        }

        if (order) {
            var order_workflow = this.pos.config.pos_workflow;
            var order_values = order.export_as_JSON();

            $('.print-create-sale-order-button').click(function (event) {
                event.preventDefault();
                $('.print-create-sale-order-button').unbind('click');

                order_values.client_order_ref = document.getElementById('workflow-partner-ref').value;
                order_values.note = document.getElementById('workflow-note').value;
                order.partner_ref = order_values.client_order_ref;
                order.notes = order_values.note;

                rpc.query({model: 'sale.order', method: 'create_pos_sale_order', args: [order_values, order_workflow]}, {timeout: 3000, shadow: true})
                    .then(function (sale_order) {
                       if (sale_order) {
                           var url = window.location.origin + "/web#id=" + sale_order.id + "&view_type=form&model=sale.order";
                           window.open(url, '_blank');
                           if (order) {
                               order.sale_order_name = sale_order.name;
                           }
                           self.gui.show_screen('receipt');
                       }
                    },
                    )
            })

            $('.create-sale-order-button').click(function (event) {
                event.preventDefault();
                $('.create-sale-order-button').unbind('click');

                order_values.client_order_ref = document.getElementById('workflow-partner-ref').value;
                order_values.note = document.getElementById('workflow-note').value;
                order.partner_ref = order_values.client_order_ref;
                order.notes = order_values.note;


                rpc.query({model: 'sale.order', method: 'create_pos_sale_order', args: [order_values, order_workflow]}, {timeout: 3000, shadow: true})
                    .then(function () {
                       if (sale_order) {
                           var url = window.location.origin + "/web#id=" + sale_order.id + "&view_type=form&model=sale.order";
                           window.open(url, '_blank');
                           if (order) {
                               order.finalize();
                           }
                       }
                    },
//                    function( type, err ){
//                        self.gui.show_popup('error', {
//                            'title': _t('Error: Could not save changes'),
//                            'body': _t('Your internet connection is probably down.'+err),
//                        });
//                    }
                    )





            })

            $('.print-create-purchase-order-button').click(function (event) {
                event.preventDefault();
                $('.print-create-purchase-order-button').unbind('click');

                order_values.partner_ref = document.getElementById('workflow-partner-ref').value;
                order_values.notes = document.getElementById('workflow-note').value;
                order.partner_ref = order_values.partner_ref;
                order.notes = order_values.notes;

                rpc.query({model: 'purchase.order', method: 'create_pos_purchase_order', args: [order_values, order_workflow]}, {timeout: 3000, shadow: true})
                    .then(function (purchase_order) {
                        if (purchase_order) {
                            var url = window.location.origin + "/web#id=" + purchase_order.id + "&view_type=form&model=purchase.order";
                            var new_window = window.open(url, '_blank');
                            if (order) {
                                order.purchase_order_name = purchase_order.name;
                            }
                            self.gui.show_screen('receipt');
                        }
                    }, function( type, err ){
                        self.gui.show_popup('error', {
                            'title': _t('Error: Could not save changes'),
                            'body': _t('Your internet connection is probably down.'+err),
                        });
                    })
            })

            $('.create-purchase-order-button').click(function (event) {
                event.preventDefault();
                $('.create-purchase-order-button').unbind('click');

                order_values.partner_ref = document.getElementById('workflow-partner-ref').value;
                order_values.notes = document.getElementById('workflow-note').value;
                order.partner_ref = order_values.partner_ref;
                order.notes = order_values.notes;

                rpc.query({model: 'purchase.order', method: 'create_pos_purchase_order', args: [order_values, order_workflow]}, {timeout: 3000, shadow: true})
                    .then(function (purchase_order) {
                        if (purchase_order) {
                            var url = window.location.origin + "/web#id=" + purchase_order.id + "&view_type=form&model=purchase.order";
                            var new_window = window.open(url, '_blank');
                            if (order) {
                                order.finalize();
                            }
                        }
                    }, function( type, err ){
                        self.gui.show_popup('error', {
                            'title': _t('Error: Could not save changes'),
                            'body': _t('Your internet connection is probably down.'+err),
                        });
                    })
            })

            $('.print-create-invoice-button').click(function (event) {
                event.preventDefault();
                $('.print-create-invoice-button').unbind('click');

                order_values.date_invoice = document.getElementById('workflow-date').value;
                order_values.partner_ref = document.getElementById('workflow-partner-ref').value;
                order_values.comment = document.getElementById('workflow-note').value;
                order.partner_ref = order_values.partner_ref;
                order.notes = order_values.comment;

                rpc.query({model: 'account.invoice', method: 'create_pos_invoice', args: [order_values, order_workflow]}, {timeout: 3000, shadow: true})
                    .then(function (invoice) {
                        if (invoice) {
                            var url = window.location.origin + "/web#id=" + invoice.id + "&view_type=form&model=account.invoice&action=" + invoice.action_id;
                            var new_window = window.open(url, '_blank');
                            if (order) {
                                order.date_order = invoice.date_invoice;
                            }
                            self.gui.show_screen('receipt');
                        }
                    })
            })

            $('.create-invoice-button').click(function (event) {
                event.preventDefault();
                $('.create-invoice-button').unbind('click');

                order_values.date_invoice = document.getElementById('workflow-date').value;
                order_values.partner_ref = document.getElementById('workflow-partner-ref').value;
                order_values.comment = document.getElementById('workflow-note').value;
                order.partner_ref = order_values.partner_ref;
                order.notes = order_values.comment;

                rpc.query({model: 'account.invoice', method: 'create_pos_invoice', args: [order_values, order_workflow]}, {timeout: 3000, shadow: true})
                    .then(function (invoice) {
                        if (invoice) {
                            var url = window.location.origin + "/web#id=" + invoice.id + "&view_type=form&model=account.invoice&action=" + invoice.action_id;
                            var new_window = window.open(url, '_blank');
                            if (order) {
                                order.finalize();
                            }
                        }
                    }, function( type, err ){
                        self.gui.show_popup('error', {
                            'title': _t('Error: Could not save changes'),
                            'body': _t('Your internet connection is probably down.'+err),
                        });
                    })
            })
        }
    }
});

})
