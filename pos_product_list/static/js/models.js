odoo.define("pos_product_list.models", function (require) {
    "use strict";
    
    var pos_model = require('point_of_sale.models');
    
    pos_model.load_fields("product.product",['qty_available','default_code','list_price']);
    

});