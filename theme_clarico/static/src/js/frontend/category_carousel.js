//--------------------------------------------------------------------------
// Category Carousel
//--------------------------------------------------------------------------
odoo.define('category_carousel.frontend_js',function(require){
'use strict';
  var category_carousel_slider = require('website.content.snippets.animation');
  var ajax = require("web.ajax");
   	category_carousel_slider.registry.category_carousel_js = category_carousel_slider.Class.extend({
    selector : ".category_carousel_js",
    start: function(){
        this.redrow();
      },
      stop: function(){
        this.clean();
      },

      redrow: function(debug){
        this.clean(debug);
        this.build(debug);
      },

      clean:function(debug){
        this.$target.empty();
      },
      build: function(debug)
      {  
    	var self = this;
        var new1 = self.$target.attr("data-list-id");
        ajax.jsonRpc('/category/slider/data', 'call', {
		'product_list_id': new1
	}).then(function (data) {
	$(self.$target).html(data);
	
		if($(window).width() > 1200)
		{
				$("#myCarousel_filter_product").each(function(){
				
					  var index = $(this).parents(".js_snippet").index();				
					  var self=$(this).attr("id","myCarousel_filter_product" +index);
					  var f_slides=$(self).find(".carousel-item").length;
					if(f_slides>4)
					{		
						$(self).find(".carousel-item").first().addClass("active");
						
						$(self).find('.carousel-item').each(function(){ 
							  var next = $(this).next();
							  if (!next.length) {
								  next = $(this).siblings(':first');
							  }
							  next.children(':first-child').clone().appendTo($(this));
							  for (var i=0;i<2;i++) {
						  			next=next.next();
						  			if (!next.length) {
						  				next = $(this).siblings(':first');
						  			}
						  			next.children(':first-child').clone().appendTo($(this));
						  		}
						})
						var s_id = $(self).attr("id");
						$(self).find(".left.carousel-control").attr("href","#" + s_id)
						$(self).find(".right.carousel-control").attr("href","#" + s_id)
					}
					else
					{		
							$(self).find(".carousel-item").addClass("active");
					}
				
				})	 	
				$("#myCarousel_product").each(function(){
					
					  var index = $(this).parents(".js_snippet").index();				
					  var self=$(this).attr("id","myCarousel_product" +index);
					
					var f_slides=$(self).find(".carousel-item").length;
				    
					if(f_slides>4)
					{		
						$(self).find(".carousel-item").first().addClass("active");
						
						$(self).find('.carousel-item').each(function(){ 
							  var next = $(this).next();
							  if (!next.length) {
								  next = $(this).siblings(':first');
							  }
							  next.children(':first-child').clone().appendTo($(this));
							  for (var i=0;i<2;i++) {
						  			next=next.next();
						  			if (!next.length) {
						  				next = $(this).siblings(':first');
						  			}
						  			next.children(':first-child').clone().appendTo($(this));
						  		}
						})
						var s_id = $(self).attr("id");
						$(self).find(".left.carousel-control").attr("href","#" + s_id)
						$(self).find(".right.carousel-control").attr("href","#" + s_id)
					}
					else
					{		
							$(self).find(".carousel-item").addClass("active");
					}
				
				})	 	
		}
        });	 	
      }
  });
});
			
			
