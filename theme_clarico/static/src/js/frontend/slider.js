//----------------------------------------------------
// Dynamic Product Slider Snippet
//----------------------------------------------------
odoo.define('website_slider.front_js', function (require) {
    'use strict';
    var sAnimations = require('website.content.snippets.animation');
    var ajax = require("web.ajax");
    var wSaleUtils = require('website_sale.utils');
    var sale = new sAnimations.registry.WebsiteSale();
    var wish = new sAnimations.registry.ProductWishlist();

    sAnimations.registry.js_slider_snippet = sAnimations.Class.extend({
        selector: ".js_slider_snippet",
        start: function () {
            this.redrow();
        },
        stop: function () {
            this.clean();
        },
        redrow: function (debug) {
            this.clean(debug);
            this.build(debug);
        },
        clean: function (debug) {
            this.$target.empty();
        },
        build: function (debug) {
	var self = this;
	var slider_id = self.$target.attr("data-slider-id");
         
	// Init wishlist function using wishlist class object also click as per base logic
	// base on click disable all data-product-product-id into page
	function slider_wishlist(){
		wish.willStart()
        $(self.$target).find(".o_add_wishlist").click(function (event) {
        event.stopImmediatePropagation();
        $(this).prop("disabled", true).addClass('disabled');
        var productId = parseInt( $(this).attr('data-product-product-id'), 10);
        $("[data-product-product-id='"+productId+"']").prop("disabled", true).addClass('disabled');
        if (productId && !_.contains(wish.wishlistProductIDs, productId)) {
	    self._rpc({
	        route: '/shop/wishlist/add',
	        params: {
	            	 product_id: productId,
	            	},
		          }).then(function () {
		        	  wish.wishlistProductIDs.push(productId);
		        	  wish._updateWishlistView();
		              wSaleUtils.animateClone($('#my_wish'), $(this).closest('form'), 25, 40);
		          }).fail(function () {
		             $(this).prop("disabled", false).removeClass('disabled');
		             var wproductId = parseInt( $(this).attr('data-product-product-id'), 10);
		             $("[data-product-product-id='"+wproductId+"']").prop("disabled", false).removeClass('disabled');
		          });
             }
        	})
    }  
    // init. carousel 
	function slider_carousel()
	{
		$(self.$target).find("#myCarousel_filter_product").each(function () {
				
                                var index = $(this).parents(".js_slider_snippet").index()
                                var id_val = $(this).parents(".js_slider_snippet").find(".js_filter_change.active").attr("data-id");
                                var self = $(this).attr("id", "myCarousel_filter_product" + index + "_" + id_val);
                                var f_slides = $(this).find(".carousel-item").length;
								
                                if (f_slides > 4) {
                                    $(this).find(".carousel-item").first().addClass("active");
                                    var s_id = $(self).attr("id");
                                    $(this).find(".carousel-control-prev").attr("data-target", "#" + s_id)
                                    $(this).find(".carousel-control-next").attr("data-target", "#" + s_id)                              
								}
	                            else {
                                    if(window.innerWidth <= 992 && window.innerWidth > 576) {
                                        if(f_slides > 2) {
                                            $(this).find(".carousel-item").first().addClass("active");
                                            $(self).attr("id");
                                            $(this).find(".carousel-control-prev").attr("data-target", "#" )
                                            $(this).find(".carousel-control-next").attr("data-target", "#" )    
                                        }
                                        else{
                                            $(this).find(".carousel-control-prev").css("display","none");
                                            $(this).find(".carousel-control-next").css("display","none");
                                            $(this).find(".carousel-item").addClass("active");
                                        }
                                        
                                    }
                                    else if(window.innerWidth <= 576) {
                                        if(f_slides > 1) {
                                            $(this).find(".carousel-inner").before('<div><a class="carousel-control-prev" data-target="#myCarousel_filter_product0_undefined" data-slide="prev"><i class="fa fa-chevron-left fa-lg text-muted"></i></a><a class="carousel-control-next" data-target="#myCarousel_filter_product0_undefined" data-slide="next"><i class="fa fa-chevron-right fa-lg text-muted"></i></a></div>')
                                            $(this).find(".carousel-item").first().addClass("active");
                                            
                                            $(this).find(".carousel-control-prev").attr("data-target", "#" )
                                            $(this).find(".carousel-control-next").attr("data-target", "#" )    
                                        }
                                        else{
                                            $(this).find(".carousel-control-prev").css("display","none");
                                            $(this).find(".carousel-control-next").css("display","none");
                                            $(this).find(".carousel-item").addClass("active");
                                        }
                                    }
                                    else {
                                        $(this).find(".carousel-control-prev").css("display","none");
                                        $(this).find(".carousel-control-next").css("display","none");
                                        $(this).find(".carousel-item").addClass("active");
                                    }                                    
                                }
                                
                                self.on('slide.bs.carousel', function (e) {
                                	var $e = $(e.relatedTarget);
                        		    var idx = $e.index();
                                    if(window.innerWidth <= 992){
                                        var itemsPerSlide = 2;    
                                    }
                                    else {
                        		      var itemsPerSlide = 4;
                        		    }
                                    var totalItems = self.find('.carousel-item').length;
                        		    if (idx >= totalItems-(itemsPerSlide-1)) {
                        		    	var it = itemsPerSlide - (totalItems - idx);
                        		        for (var i=0; i<it; i++) {
                        		            // append slides to end
                        		            if (e.direction=="left") {	            	
                        		            	self.find('.carousel-item').eq(i).appendTo(self.find('.carousel-inner'));
                        		            }
                        		            else {      		         
                        		            	self.find('.carousel-item').eq(0).appendTo(self.find('.carousel-inner'));
                        		            }
                        		        }
                        		    }
                        		});
							})
	}
	// Common filter click event within the current target
	// into it just append new filter data into data-container and if it already exist then 
	// toggle show / hide the filter data-container not request to server again { To optimize the performance }
	function slider_render(target)
	{
	$(target).find(".js_filter_change").click(function(){
        $('.cus_theme_loader_layout').removeClass('d-none');
        var filter_id = $(this).attr('data-id')
        $(target).find(".js_filter_change").removeClass('active')
        $(this).addClass('active')
        var current_filter=$(self.$target).find("div[filter-id='" + filter_id + "']");
        $(target).find(".js_filter_data").hide()
        if (current_filter.length ==1){
            $('.cus_theme_loader_layout').addClass('d-none');
            $('.cus_theme_loader_layout').addClass('hidden');
           current_filter.show()
        }
       else{
           		ajax.jsonRpc('/slider/render', 'call', {'slider_id': slider_id,'filter_id':filter_id}).then(function (data) {
	            	$('.cus_theme_loader_layout').addClass('d-none');
	            	$('.cus_theme_loader_layout').addClass('hidden');
					//$(self.$target).html(data);
	            	$(target).find(".js_data_container").append($(data).find(".js_filter_data"))
	            	$(target).find(".a-submit").click(function (event) {
	            		sale._onClickSubmit(event)
	            		})
		            	slider_wishlist()
		            	slider_carousel()
             	 })
         }
		})   
	}
	// on built snippent render the template of style as per configuration and call the common function
	// {Play with Logic} Logic : common method if not given then display first filter data other wise based on
	// argument display data on template
		ajax.jsonRpc('/slider/render', 'call', {'slider_id': slider_id}).then(function (data) {
			$(self.$target).html(data);
			$(self.$target).find(".js_filter_change").first().addClass( "active" );
	        slider_render($(self.$target))
	        $(self.$target).find(".a-submit").click(function (event) {
	        	sale._onClickSubmit(event)
	    		})
	    	slider_wishlist()
	    	slider_carousel()
	    	});
    }
    });
});
