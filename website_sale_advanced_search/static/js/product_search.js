odoo.define('website_sale_advanced_search.product_search', function (require) {
"use strict";
var ajax = require('web.ajax');
var core = require('web.core');
var session = require('web.session');
var base = require('web_editor.base');
var _t = core._t;
base.url_translations = '/website/translations';
var _t = core._t;
$(function() {
    $('.search-panel .dropdown-menu').find('a').click(function(e) {
		e.preventDefault();
		var param = $(this).attr("href").replace("#","");
		var concept = $(this).text();
		$('.search-panel span#search_concept').text(concept);
		$('.input-group #search_param').val(param);
	});

	$(document).on('input','.oe_search_box',function(e){
//	    window.location = window.location.href
//        var oldurl = (window.location.href.indexOf("?")===-1) ? "" : "";
//        window.location = oldurl + '?search=' + $(this).val();
        ajax.jsonRpc("/shop/search_advance", 'call', {
                'search': $(this).val(),
          }).then(function (data) {
                $('#product_list').html(data.return_url);
//                window.history.pushState({}, "", $(this).val());
            });
	});
    $(".oe_search_box").autocomplete({
        source: function(request, response) {
            $.ajax({
            url: "/shop/search",
            method: "POST",
            dataType: "json",
            data: { name: request.term, category: $('.input-group #search_param').val()},
            success: function( data ) {
                response( $.map( data, function( item ) {
                    return {
                        label: item.name,
                        value: item.name,
                        id: item.res_id,
                    }
                }));
            },
//            error: function (error) {
//               alert('error: ' + error);
//            }
            });
        },
        select:function(suggestion,term,item){
            window.location.href= "/shop/product/"+term.item.id
        },
        minLength: 1
    });
});
});