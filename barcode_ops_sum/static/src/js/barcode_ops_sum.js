odoo.define('barcode_ops_sum.barcode_ops_sum', function (require) {
    var core = require('web.core');
    var LinesWidget = require('stock_barcode.LinesWidget');
    var QWeb = core.qweb;
    var _t = core._t
    console.log('Called?1')
    LinesWidget.include({
        _renderLines: function () {
            this._super();
             var $header = this.$el.filter('.o_barcode_lines_header');
            var product_uom_qty=0;
            var done_qty=0;
            for (var y in this.page.lines){
              product_uom_qty+=parseFloat(this.page.lines[y].product_uom_qty);
              done_qty+=parseFloat(this.page.lines[y].qty_done);
            }
            $header.append("<span>"+done_qty+"</span>/<span>"+product_uom_qty+"</span>")
        },
    });

});
