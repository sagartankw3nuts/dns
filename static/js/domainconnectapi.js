var temp_loader =`<div class="spinner-border text-light" role="status"><span class="visually-hidden"></span></div>`;
var domain_regex = /^(?!:\/\/)([A-Za-z0-9-]+\.)+[A-Za-z]{2,6}$/;

function ajaxErrorMsg(xhr) {
	$('.loader-div').html(null);
    if (xhr.status === 422) {
        $.each(xhr.responseJSON.errors, function (key, val) {
            console.error(val);
        });
    } else {
        console.error(xhr.statusText);
    }
}

function setLoading() {
	$('#2-btn-loader').hide();
	$('#2-btn-loader').text('Loading...');
	$('#2-btn-loader').attr('href', 'javascript:;');
	$('.analyze_blk').find('li').removeClass('active');
	document.getElementById("domainconnect").innerHTML ='';
}

function callbackfunc(url, domain, host, provider_name, data) {
	if (url) {
		$('.analyze_blk').find('li').addClass('active');
		url = url + '&RANDOMTEXT=shm:0:' + encodeURIComponent(data) + '&IP=172.105.47.42'
		document.getElementById("domainconnect").innerHTML = `<a href='javascript:;'>${provider_name}</a>`
		$('#2-btn-loader').show();
		$('#2-btn-loader').attr('href', url);
		$('#2-btn-loader').text(`Authorize with ${provider_name}`);
	} else {
		setTimeout(() => {
				$('.step_form_modal_step-2').removeClass('active').css('display', 'none');
				$('.step_form_modal_step-3').addClass('active').css('display', '');
			// $('.step_form_modal_step').removeClass('active');
			// $('.step_form_modal_step').css('display', 'none');
			// $('.step_form_modal_step-1').addClass('active').css('display', '');
			// $('.step_for_pagi li').removeClass('active');
			// $('.step_for_pagi li:first-child').addClass('active');
		}, 1000);
		$('#2-btn-loader').attr('href', 'javascript:;');
		// document.getElementById('domainconnect').innerHTML = "Domain does not support domain connect";
	}
}

$(document).keydown(function (event) {
    if (event.key === ' ' || event.keyCode === 32 || event.which === 32) {
		return false;
    }
});

$(document).ready(function () {
	$('#txt_domain_btn').click(function (event) {
		event.preventDefault();
		
		var txt_domain_obj = $('#txt_domain_name');
		txt_domain_obj.removeClass('form_error')
		var domain_val = txt_domain_obj.val();

		if(domain_val == '' || !domain_regex.test(domain_val)) {
			txt_domain_obj.addClass('form_error');

			$('.step_form_modal_step').removeClass('active');
			$('.step_form_modal_step').css('display', 'none');
			$('.step_form_modal_step-1').addClass('active').css('display', '');
			$('.step_for_pagi li').removeClass('active');
			$('.step_for_pagi li:first-child').addClass('active');
			return false
		}

		domain = document.getElementById('txt_domain_name').value;
		message = document.getElementById('message').value;
		host = document.getElementById('host').value;
		
		$.ajax({
			url: '/api-post-domain',
			type: 'POST',
            data: {
				'domain': domain,
				'message': message,
				'host': host,
			},
            dataType: 'json',
			cache: false,
            beforeSend: function() {
				$('.loader-div').html(temp_loader);
				setLoading();
			},
            success: function (res) {
				if(res.status == true) {
					$('.loader-div').html(null);
					$('#div_content_success').show();
					callbackfunc(res.url, res.domain, res.host, res.provider_name, res.data);
				} else if(res.status == false) {
					$('#div_content_error').show();
					callbackfunc("", "", "", "", "");
					console.log(res.message);
				}
			},
			error: function (xhr) {
				callbackfunc("", "", "", "", "");
				ajaxErrorMsg(xhr);
			}
		});
	});
	$('#btn_show_modal').click(function (event) {
		event.preventDefault();
		$('#txt_domain_name').val('');
		$('#txt_domain_name').removeClass('form_error');
		$('#seedemomodal').modal('show');
		
		$('.modal_main_step').css('display','block');

		$('.step_form_modal').css('display','none');
		
		$('.sent_modal_box').css('display','none');

		$('.step_for_pagi li').removeClass('active');
		$('.step_for_pagi li:first-child').addClass('active');
		
		$('#step-1').addClass('active').show();
		$('#step-2').removeClass('active').hide();
		$('#step-3').removeClass('active').hide();
		$('#step-4').removeClass('active').hide();
	});
});


$(document).ready(function () {
    $("#search_provider_name").on("input", function () {
        var filterValue = $(this).val().toLowerCase();
        $("#search_filter_list li").each(function () {
            var listItemText = $(this).attr('data-name').toLowerCase();
            if (listItemText.includes(filterValue)) {
                $(this).show();
            } else {
                $(this).hide();
            }
        });
    });
});