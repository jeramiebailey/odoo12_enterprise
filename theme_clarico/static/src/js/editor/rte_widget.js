odoo.define('clarico_carousel.editor', function (require) {
"use strict";
var weContext = require('web_editor.context');
var v11_rte = require('web_editor.rte');

//--------------------------------------------------
// Emipro Ept Rte 
//-------------------------------------------------
 v11_rte.Class.include({ 
		
	_saveElement: function ($el, context, withLang) {
    	var tag = this._getEscapedElement($el).prop('outerHTML');
        var $tag = $(tag);
        $tag.find("[data-isemipro='true']").empty();
        tag = $tag[0].outerHTML;
        return this._rpc({
            model: 'ir.ui.view',
            method: 'save',
            args: [
                $el.data('oe-id'),
                tag,
                $el.data('oe-xpath') || null,
            ],
            context: withLang ? context : _.extend({}, context, {lang: undefined}),
        });
    },
	
	save : function (context) {
    var self = this;
    var $dirty = $('.o_dirty');
    $dirty
        .removeAttr('contentEditable')
        // https://github.com/odoo/odoo/commit/71b20a24c40ae9daa10076ab0fd656b043819cff#diff-1e7fea0c1a48e736046cf234118f95d4
        // remove class due to confict with destory method and as per odoo above commit ept-change.
        .removeClass('o_dirty oe_carlos_danger o_is_inline_editable note-air-editor note-editable');
    	var defs = _.map($dirty, function (el) {
        var $el = $(el);
        $el.find('[class]').filter(function () {
            if (!this.className.match(/\S/)) {
                this.removeAttribute('class');
            }
        });

        // TODO: Add a queue with concurrency limit in webclient
        // https://github.com/medikoo/deferred/blob/master/lib/ext/function/gate.js
        return self.saving_mutex.exec(function () {
            return self._saveElement($el, context || weContext.get())
            .then(function () {
                $el.removeClass('o_dirty');
            }, function (response) {
                // because ckeditor regenerates all the dom, we can't just
                // setup the popover here as everything will be destroyed by
                // the DOM regeneration. Add markings instead, and returns a
                // new rejection with all relevant info
                var id = _.uniqueId('carlos_danger_');
                $el.addClass('o_dirty oe_carlos_danger ' + id);
                var html = (response.data.exception_type === 'except_osv');
                if (html) {
                    var msg = $('<div/>', {text: response.data.message}).html();
                    var data = msg.substring(3, msg.length  -2).split(/', u'/);
                    response.data.message = '<b>' + data[0] + '</b>' + data[1];
                }
                $('.o_editable.' + id)
                    .removeClass(id)
                    .popover({
                        html: html,
                        trigger: 'hover',
                        content: response.data.message,
                        placement: 'auto top',
                    })
                    .popover('show');
            });
        });
    });
    return $.when.apply($, defs).then(function () {
        window.onbeforeunload = null;
    }, function (failed) {
        ret.cancel();
        ret.start();
    });
   
	}
});
});
