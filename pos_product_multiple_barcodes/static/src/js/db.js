odoo.define('pos_product_multiple_barcodes.DB', function(require) {
'use strict';

var DB = require('point_of_sale.DB');
var models = require('point_of_sale.models');

models.load_fields("product.product", "barcode_ids_str");

DB.include({
    add_products: function( products ){
        this._super.apply(this, arguments);
        for( var i=0; i < products.length; i++ ){
            var product = products[i];
            var barcodes = product.barcode_ids_str;
            var barcode_ids = [];
            if(barcodes){
                barcode_ids = barcodes.split(',')
                for( var i=0; i < barcode_ids.length; i++ ){
                    var barcode = barcode_ids[i];
                    this.product_by_id[product.id] = product;
                    if (barcode){
                        this.product_by_barcode[barcode] = product;
                    }
                }
            }
        }
    }
})
})