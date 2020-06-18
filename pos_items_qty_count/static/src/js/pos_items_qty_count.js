odoo.define('pos.pos_items_qty_count', function (require) {
"use strict";
    
var PosModel = require('point_of_sale.models');
var Screens = require('point_of_sale.screens');
var SuperOrder = PosModel.Order;
var SuperOrderline = PosModel.Orderline.prototype;

    PosModel.Order = PosModel.Order.extend({
        initialize: function(attributes,options){
            this.items_count = 0;
            this.products_count = 0;
            SuperOrder.prototype.initialize.call(this, attributes, options);
        },
        get_items_count: function(Orderline){
            var count = 0;
            var is_old_line = false;
            if (Orderline != undefined && Orderline.quantity > 0)
                count = 1;
            this.orderlines.forEach(function(orderline){
                if (Orderline != undefined && orderline.cid == Orderline.cid)
                    is_old_line = true;
            });
            count = this.orderlines.length || count;
            if (!is_old_line && this.selected_orderline && Orderline != undefined && this.selected_orderline.cid != Orderline.cid && Orderline.quantity > 0)
                count += 1;
            this.items_count = count;
            return count
        },
        get_qty_count: function(Orderline){
            var count = 0;
            var is_old_line = false;
            if (Orderline != undefined && Orderline.quantity > 0 && this.orderlines.length == 0)
                count = Orderline.quantity;
            this.orderlines.forEach(function(orderline){
                count += orderline.quantity;
                if (Orderline != undefined && orderline.cid == Orderline.cid)
                    is_old_line = true;
            });
            if (!is_old_line && this.selected_orderline && Orderline != undefined && this.selected_orderline.cid != Orderline.cid && Orderline.quantity > 0)
                count += Orderline.quantity;
            this.products_count = count;
            return count
        },
        change_count_value: function(Orderline){
            this.items_count = this.get_items_count(Orderline);
            this.products_count = this.get_qty_count(Orderline);
            $('.items_count_value').text("Total Items: " + this.items_count);
            $('.products_count_value').text("Total Qty: " + this.products_count);
        },
    });
    
    PosModel.Orderline = PosModel.Orderline.extend({
        set_quantity: function(quantity){
            SuperOrderline.set_quantity.call(this,quantity);
            if(this.pos.get('selectedOrder') != null)
                this.order.change_count_value(this);
        }
    });

    Screens.OrderWidget.include({
        change_selected_order: function() {
            this._super();
            this.pos.get_order().change_count_value();
        }
    });
});