/* Copyright (c) 2016-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>) */
/* See LICENSE file for full copyright and licensing details. */
/* License URL : <https://store.webkul.com/license.html/> */
odoo.define('pos_order_notes.pos_order_notes', function (require) {
"use strict";
    var pos_model = require('point_of_sale.models');
    var screens = require('point_of_sale.screens');
    var PopupWidget = require('point_of_sale.popups');
    var SuperPaymentScreen = screens.ProductScreenWidget.prototype;
    var gui = require('point_of_sale.gui');
    var SuperOrder = pos_model.Order;
    var SuperOrderline = pos_model.Orderline;

    screens.PaymentScreenWidget.include({
        show: function(){
            var self = this;
            self._super();
            $('#order_note').on('focus',function(){
                $('body').off('keypress', self.keyboard_handler);
                $('body').off('keydown', self.keyboard_keydown_handler);
            });
            $('#order_note').on('focusout',function(){
                $('body').keypress(self.keyboard_handler);
                $('body').keydown(self.keyboard_keydown_handler);
            });
        }
    });

    var WkAlertPopup = PopupWidget.extend({
        template: 'WkAlertPopup',
    });
    gui.define_popup({ name: 'wk_alert_popup', widget: WkAlertPopup });

    pos_model.Order = pos_model.Order.extend({
        get_order_note: function(){
            return $("#order_note").val();
        },
        export_as_JSON: function() {
            var self = this;
            var loaded=SuperOrder.prototype.export_as_JSON.call(this);
            loaded.order_note=self.get_order_note();  
            return loaded;
        },
    });
    
    pos_model.Orderline = pos_model.Orderline.extend({            
        initialize: function(attr,options){
            this.order_line_note='';
            SuperOrderline.prototype.initialize.call(this,attr,options);
        },
        export_for_printing: function(){
            var dict = SuperOrderline.prototype.export_for_printing.call(this);
            dict.order_line_note = this.order_line_note;
            return dict;
        },
        get_order_line_comment: function(){
            var self = this;        
            return self.order_line_note;
        },
        export_as_JSON: function() {
            var self = this;
            var loaded=SuperOrderline.prototype.export_as_JSON.call(this);
            loaded.order_line_note=self.get_order_line_comment();  
            return loaded;
        }
    });

    screens.ProductScreenWidget.include({
        show: function(){
            this._super();
            this.product_categories_widget.reset_category();
            this.numpad.state.reset();
            var self = this;
            var text_limit = this.pos.config.note_keyword_limit;
            var is_text_limit = this.pos.config.set_note_keyword_limit;
            this.$('#add_note').click(function()
            {
                if(typeof(self.pos.get_order().get_selected_orderline())=='object')
                {
                    self.gui.show_popup('textarea',{
                        title: "Add note",
                        value: self.pos.get_order().get_selected_orderline().order_line_note,
                        confirm: function(note){
                            self.$('ul.orderlines li.selected ul div#extra_comments').text(note);
                            self.pos.get_order().get_selected_orderline().order_line_note=note;
                        }
                    });                    
                    $("textarea").css({"width":"92%","height":"56%","resize":"none"});
                    if(text_limit && is_text_limit)
                        $("textarea").attr('maxlength',text_limit.toString());
                }
                else
                    self.pos.gui.show_popup('wk_alert_popup',{
                        'title':'No Selected Order Line',
                        'body':'Please add/select an orderline'
                    });
            });
        }
    });
});    