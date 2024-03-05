
/*============ Header Function Start ============*/
 
 

jQuery(document).ready(function(){
	jQuery(".lifestyle-menu-toggler").click(function(){
		jQuery(this).toggleClass("active");
		jQuery(".lifestyle-header-navbar").slideToggle(300);
	});
});
/*============ Header Function End ============*/

/*============ Slick-Slider Function Start ============*/
 

jQuery(document).ready(function(){
	 
	 
	
 

	jQuery('.how_it_slider').owlCarousel({
		loop:true,
		margin:0,
		smartSpeed:800,
		autoplay:true,
		autoplayTimeout:5000,
		nav:false,
		dots:false,
		responsive:{
			0:{
				items:1
			},
			992:{
				items:2
			},
			1000:{
				items:3
			}
		}
	});


	jQuery(".modal_main_step .w3n_btn_wrp a").click(function(e){
		e.stopPropagation();
		e.preventDefault();
		jQuery(this).parents('.modal_main_step').next('.step_form_modal').show();
		jQuery(this).parents('.modal_main_step').hide();
	});

	jQuery(".step_form_modal_step-1 .w3n_btn_wrp .w3n_btn").click(function(e){
		e.stopPropagation();
		e.preventDefault();
		jQuery(this).parents('.step_form_modal_step-1').next('.step_form_modal_step-2').show();
		jQuery('.step_form_modal_step-2').addClass('active');
		jQuery(this).parents('.step_form_modal_step-1').hide();
		jQuery('.step_form_modal_step-1').removeClass('active');
		jQuery('.step_for_pagi li.active').removeClass('active').next().addClass('active');
	});

	/* jQuery(".step_form_modal_step-2 .w3n_btn_wrp .w3n_btn").click(function(e){
		e.stopPropagation();
		e.preventDefault();
		jQuery(this).parents('.step_form_modal_step-2').next('.step_form_modal_step-3').show();
		jQuery('.step_form_modal_step-3').addClass('active');
		jQuery(this).parents('.step_form_modal_step-2').hide();
		jQuery('.step_form_modal_step-2').removeClass('active');
		jQuery('.step_for_pagi li.active').removeClass('active').next().addClass('active');
	}); */
	
	jQuery(".search_filter_list li a").click(function(e){
		e.stopPropagation();
		e.preventDefault();
		jQuery(this).parents('.step_form_modal_step-3').next('.step_form_modal_step-4').show();
		jQuery('.step_form_modal_step-4').addClass('active');
		jQuery(this).parents('.step_form_modal_step-3').hide();
		jQuery('.step_form_modal_step-3').removeClass('active');
		jQuery('.step_for_pagi li.active').removeClass('active').next().addClass('active');
	});
	jQuery(".step_form_modal_step-4 .w3n_btn_wrp .w3n_btn").click(function(e){
		e.stopPropagation();
		e.preventDefault();
		jQuery(this).parents('.step_form_modal').next('.sent_modal_box').show();
		jQuery(this).parents('.step_form_modal').hide();
	});

	jQuery(".see_record_btn a").click(function(e){
		e.stopPropagation();
		e.preventDefault();
		jQuery(this).parents('.sent_modal_box').prev('.step_form_modal').show();
		jQuery(this).parents('.sent_modal_box').hide();
	});
	jQuery(".step_back a").click(function(e){
		e.stopPropagation();
		e.preventDefault();
		
		$('#txt_domain_btn').text('Continue');

		// console.log("jQuery('.step_form_modal_step-1')" , jQuery('.step_form_modal_step-1').show())
		// console.log("jQuery('.step_form_modal_step-2')" , jQuery('.step_form_modal_step-2').show())
		// console.log("jQuery('.step_form_modal_step-3')" , jQuery('.step_form_modal_step-3').show())
		// console.log("jQuery('.step_form_modal_step-4')" , jQuery('.step_form_modal_step-4').show())
		if(jQuery('.step_form_modal_step-1').hasClass('active')){
			jQuery(this).parents('.step_form_modal').prev('.modal_main_step').show();
			jQuery(this).parents('.step_form_modal').hide();
		}
		if(jQuery('.step_form_modal_step-2').hasClass('active')){
			jQuery('.step_form_modal_step-1').show();
			jQuery('.step_form_modal_step-1').addClass('active');
			jQuery('.step_form_modal_step-2').hide();
			jQuery('.step_form_modal_step-2').removeClass('active');
			jQuery('.step_for_pagi li.active').removeClass('active').prev().addClass('active');
		}
		else if(jQuery('.step_form_modal_step-3').hasClass('active')){
			/*jQuery('.step_form_modal_step-2').show();
			jQuery('.step_form_modal_step-2').addClass('active');
			jQuery('.step_form_modal_step-3').hide();
			jQuery('.step_form_modal_step-3').removeClass('active');
			jQuery('.step_for_pagi li.active').removeClass('active').prev().addClass('active');*/
			jQuery('.step_form_modal_step-1').show();
			jQuery('.step_form_modal_step-1').addClass('active');
			jQuery('.step_form_modal_step-2').hide();
			jQuery('.step_form_modal_step-2').removeClass('active');
			jQuery('.step_form_modal_step-3').hide();
			jQuery('.step_form_modal_step-3').removeClass('active');
			jQuery('.step_for_pagi li.active').removeClass('active').prev().addClass('active');
		}
		else if(jQuery('.step_form_modal_step-4').hasClass('active')){
			jQuery('.step_form_modal_step-3').show();
			jQuery('.step_form_modal_step-3').addClass('active');
			jQuery('.step_form_modal_step-4').hide();
			jQuery('.step_form_modal_step-4').removeClass('active');
			jQuery('.step_for_pagi li.active').removeClass('active').prev().addClass('active');
		}
	});
});
/*============ Slick-Slider Function End ============*/