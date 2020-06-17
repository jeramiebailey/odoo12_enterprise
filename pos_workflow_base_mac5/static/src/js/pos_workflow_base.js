odoo.define('pos_workflow_base.pos_workflow_base', function (require) {
"use strict";

var core = require('web.core');
var DB = require('point_of_sale.DB');
var gui = require('point_of_sale.gui');
var models = require('point_of_sale.models');
var popups = require("point_of_sale.popups");
var rpc = require('web.rpc');
var screens = require('point_of_sale.screens');

var _t = core._t;


var _super_posmodel = models.PosModel.prototype;

var partner_index = _super_posmodel.models.map(function(e) { return e.model; }).indexOf('res.partner');
_super_posmodel.models.splice(partner_index, 1)

models.load_models({
        model: 'res.partner',
        fields: ['name', 'street', 'city', 'state_id', 'country_id', 'vat', 'phone', 'zip',
                 'mobile', 'email', 'barcode', 'write_date', 'property_account_position_id',
                 'property_product_pricelist', 'debit', 'credit', 'customer', 'supplier'],
        domain: [],
        loaded: function(self, partners) {
            var target_partners = [];
            var workflow = self.config ? self.config.pos_workflow : '';

            for(var i = 0; i < partners.length; i++){
                var partner = partners[i];
                if( (workflow.indexOf('purchase') >= 0 || workflow.indexOf('supplier') >= 0)
                        && partner.supplier ){
                    target_partners.push(partner);
                } else if( (workflow.indexOf('purchase') < 0 && workflow.indexOf('supplier') < 0)
                        && partner.customer ){
                    target_partners.push(partner);
                }
            }

            self.partners = target_partners;
            self.db.add_partners(target_partners);

            self.db.config = self.config;
        }
    }, {'after': 'pos.config'})


models.load_fields('product.product', ['standard_price', 'supplier_taxes_id', 'purchase_ok',
                                       'sale_ok', 'pos_customer_tax_ids', 'pos_supplier_tax_ids',
                                       'pos_sale_price_total', 'pos_cost_price_total',
                                       'uom_po_id', 'standard_price_computed'])


models.PosModel = models.PosModel.extend({
    load_new_partners: function(){
        var self = this;
        var def = new $.Deferred();
        var fields = _.find(this.models,function(model){ return model.model === 'res.partner'; }).fields;
        var workflow = this.config.pos_workflow;
        if( workflow.indexOf('purchase') >= 0 || workflow.indexOf('supplier') >= 0 ){
            var domain = [['supplier', '=', true], ['write_date', '>', this.db.get_partner_write_date()]];
        } else {
            var domain = [['customer', '=', true], ['write_date', '>', this.db.get_partner_write_date()]];
        }
        rpc.query({
                model: 'res.partner',
                method: 'search_read',
                args: [domain, fields],
            }, {
                timeout: 3000,
                shadow: true,
            })
            .then(function(partners){
                if (self.db.add_partners(partners)) {   // check if the partners we got were real updates
                    def.resolve();
                } else {
                    def.reject();
                }
            }, function(type,err){ def.reject(); });
        return def;
    },

    get_importobject: function() {
        var order = this.get_order();
        if (order) {
            return order.get_importobject();
        }
        return null;
    },
});


var _super_order = models.Order.prototype;
models.Order = models.Order.extend({
    initialize: function(attr, options) {
        var result = _super_order.initialize.apply(this, arguments);
        this.pos_workflow = this.pos.config.pos_workflow;
        return result;
    },

    get_importobject: function(){
        return null;
    },
});


DB.include({
    init: function( options ){
        this._super(options);
        this.config = false;
    },

    add_products: function( products ){
        if(!products instanceof Array){
            products = [products];
        }

        var target_products = [];
        var workflow = this.config ? this.config.pos_workflow : '';

        for( var i=0; i < products.length; i++ ){
            var product = products[i];
            if( (workflow.indexOf('purchase') >= 0 || workflow.indexOf('supplier') >= 0)
                    && product.purchase_ok ){
                if( this.config && this.config.use_pos_product_tax ){
                    if( this.config.display_pos_price_total ){
                        product.lst_price = product.pos_cost_price_total
                    } else {
                        product.lst_price = product.standard_price_computed;
                    }
                    if (product.pos_supplier_tax_ids === undefined || product.pos_supplier_tax_ids.length == 0) {
                        product.taxes_id = product.supplier_taxes_id;
                    } else {
                        product.taxes_id = product.pos_supplier_tax_ids;
                    }
                } else {
                    product.lst_price = product.standard_price_computed;
                    product.taxes_id = product.supplier_taxes_id;
                }
                product.uom_id = product.uom_po_id
                target_products.push(product);
            } else if( (workflow.indexOf('purchase') < 0 && workflow.indexOf('supplier') < 0)
                    && product.sale_ok ){
                if( this.config && this.config.use_pos_product_tax ){
                    if( this.config.display_pos_price_total ){
                        product.lst_price = product.pos_sale_price_total
                    }
                    if (product.pos_customer_tax_ids === undefined || product.pos_customer_tax_ids.length == 0) {
                        product.taxes_id = product.taxes_id;
                    } else {
                        product.taxes_id = product.pos_customer_tax_ids;
                    }
                }
                target_products.push(product);
            }
        }

        this._super(target_products);
    },
});


screens.ActionpadWidget.include({
    renderElement: function() {
        this._super();
        var self = this;
        this.$('.pos-workflow-popup').click(function() {
            self.gui.show_popup('pos_workflow', {});
        });
    }
});


screens.ClientListScreenWidget.include({
    toggle_save_button: function() {
        var workflow = this.pos.config.pos_workflow;
        if( workflow.indexOf('purchase') >= 0 || workflow.indexOf('supplier') >= 0 ){
            var $button = this.$('.button.next');
            if (this.editing_client) {
                $button.addClass('oe_hidden');
                return;
            } else if (this.new_client) {
                if (!this.old_client) {
                    $button.text(_t('Set Vendor'));
                } else {
                    $button.text(_t('Change Vendor'));
                }
            } else {
                $button.text(_t('Deselect Vendor'));
            }
            $button.toggleClass('oe_hidden', !this.has_client_changed());
        } else {
            this._super();
        }
    },

    save_client_details: function(partner) {
        var workflow = this.pos.config.pos_workflow;
        if( workflow.indexOf('purchase') >= 0 || workflow.indexOf('supplier') >= 0 ){
            var self = this;
            
            var fields = {};
            this.$('.client-details-contents .detail').each(function(idx,el){
                fields[el.name] = el.value || false;
            });

            if (!fields.name) {
                this.gui.show_popup('error',_t('A Vendor Name Is Required'));
                return;
            }
            
            if (this.uploaded_picture) {
                fields.image = this.uploaded_picture;
            }

            fields.id           = partner.id || false;
            fields.country_id   = fields.country_id || false;
            fields.customer = false;
            fields.supplier = true;

            if (fields.property_product_pricelist) {
                fields.property_product_pricelist = parseInt(fields.property_product_pricelist, 10);
            } else {
                fields.property_product_pricelist = false;
            }

            rpc.query({
                    model: 'res.partner',
                    method: 'create_from_ui',
                    args: [fields],
                })
                .then(function(partner_id){
                    self.saved_client_details(partner_id);
                },function(type,err){
                    self.gui.show_popup('error',{
                        'title': _t('Error: Could not Save Changes'),
                        'body': _t('Your Internet connection is probably down.'),
                    });
                });
        } else {
            this._super(partner);
        }
    },
});


var POSWorkflowPopup = popups.extend({
    template: 'POSWorkflowPopup',

    show: function () {
        this._super();
        var self = this;
        var order = this.pos.get_order();

        if (order) {
            var workflow = order.pos_workflow

            if (!order.get_client()) {
                if( workflow.indexOf('purchase') >= 0 || workflow.indexOf('supplier') >= 0 ){
                    this.gui.show_popup('error', {'title': _t("Warning"), 'body': _t("Please select a vendor first!")});
                } else {
                    this.gui.show_popup('error', {'title': _t("Warning"), 'body': _t("Please select a customer first!")});
                }
                return
            }
            if (order.orderlines.length == 0) {
                this.gui.show_popup('error', {'title': _t("Warning"), 'body': _t("Please add products first!")});
                return
            }
        }
    }
});
gui.define_popup({name: 'pos_workflow', widget: POSWorkflowPopup});


var POSImportListButton = screens.ActionButtonWidget.extend({
    template: 'POSImportListButton',
    button_click: function(){},
});

screens.define_action_button({
    'name': 'import_list',
    'widget': POSImportListButton,
    'condition': function() {
        return this.pos.config.pos_import !== false;
    },
});


return {
    POSWorkflowPopup: POSWorkflowPopup,
    POSImportListButton: POSImportListButton,
};

})
