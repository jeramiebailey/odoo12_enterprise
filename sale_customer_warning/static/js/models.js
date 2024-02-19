odoo.define("sale_customer_warning.models", function (require) {
    "use strict";
    
    var pos_model = require('point_of_sale.models');
    
    pos_model.load_fields("res.partner",['company_type']);
    

});