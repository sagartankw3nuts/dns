
/*============ Header Function Start ============*/
 
 

jQuery(document).ready(function(){
	jQuery(".sidebar_menu .menu-item-has-children > a ").append('<span class="icon"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M8 10L12 14L16 10" stroke="currentcolor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"/></svg></span>');
	jQuery(".sidebar_menu .menu-item-has-children > a").on('click', function(e) {
		e.preventDefault();
		  jQuery(this).parent().children('ul').slideToggle(500);
		  jQuery(this).parent().siblings('li').find('ul').slideUp(500);
		  jQuery(this).parent().siblings('li').removeClass('active');
		  jQuery(this).parent().toggleClass('active');
		  e.stopPropagation();
	});

	/*Mobile Menu Start*/
	jQuery(".hamburger-icon").click(function() {
		'use strict';
		jQuery(this).toggleClass('active');
		jQuery('.sidebar').toggleClass('active-sidebar');
		jQuery('body').toggleClass('open_menu');
	});
	/*Mobile Menu End*/
});
/*============ Header Function End ============*/

function bluesticky()
{
	// First we get the viewport height and we multiple it by 1% to get a value for a vh unit
	let vh = window.innerHeight * 0.01;
	// Then we set the value in the --vh custom property to the root of the document
	document.documentElement.style.setProperty('--vh', `${vh}px`);
}

jQuery(window).on('load' ,function() {
	bluesticky();
});
jQuery(window).resize(function() {
	bluesticky();
});

var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
  return new bootstrap.Tooltip(tooltipTriggerEl)
})
	  
/*============ Slick-Slider Function End ============*/