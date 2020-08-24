odoo.define('sale_customer_warning.screens', function (require) {
"use strict";

var module = require('point_of_sale.models');
var screens = require('point_of_sale.screens');
var core = require('web.core');
var QWeb = core.qweb;
var _t = core._t;
var models = module.PosModel.prototype.models;

screens.ClientListScreenWidget.include({
    toggle_save_button: function(){
        this._super();
        if( this.new_client ){
            if( !this.old_client){
                if( this.new_client.company_type === 'person'){
                this.gui.show_popup('alert',{
                'title': _t('Warning'),
                'body':  _t('You have chosen an Individual Customer.'),
            });
                }
            }
        }
    },

});
});