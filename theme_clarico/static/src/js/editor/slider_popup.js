//--------------------------------------------------------------------------
// Product Slider and Category Popup
//--------------------------------------------------------------------------
odoo.define('website_slider.editor', function (require) {
'use strict';

var core = require('web.core');
var rpc = require('web.rpc');
var weContext = require('web_editor.context');
var options = require('web_editor.snippets.options');
var wUtils = require('website.utils');
var _t = core._t;
var snippets_slider_common = options.Class.extend({
    popup_template_id: "snippets_list",
    popup_title: _t("Add Slider"),
    select_snippet_list: function (previewMode, value) {
        var self = this;
        var def = wUtils.prompt({
            'id': this.popup_template_id,
            'window_title': this.popup_title,
            'select': _t("Product"),
            'init': function (field) {
                return rpc.query({
                        model: 'slider',
                        method: 'name_search',
                        args: ['', [['website_id','in',[false,parseInt($("html").attr("data-website-id"))]]]],
                        context: weContext.get(),
                    });
            },
        });
        def.then(function (slider_id) {
        var currentdate = new Date();
        self.$target.attr("data-slider-id", slider_id);
        self.$target.attr("data-date-time", currentdate);

	});
        return def;
    },	
    onBuilt: function () {
        var self = this;
        this._super();
        this.select_snippet_list('click').fail(function () {
            self.getParent()._onRemoveClick($.Event( "click" ));
        });
    },
});
options.registry.product_list_slider = snippets_slider_common.extend({
    cleanForSave: function () {
        this.$target.addClass("hidden");
    },
});
});
