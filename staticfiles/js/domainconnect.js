
function setLoading() {
	$('#2-btn-loader').text('Loading...');
	$('#2-btn-loader').attr('href', 'javascript:;');
	$('.analyze_blk').find('li').removeClass('active');
	document.getElementById("domainconnect").innerHTML ='';
}

function domain_connect(domain, host, data, providerId, serviceId, cb) {
    // Query for the _domainconnect TXT record
	setLoading();
    const xhr = new XMLHttpRequest();
    xhr.open('GET', 'https://dns.google/resolve?type=txt&name=_domainconnect.' + domain);
    xhr.responseType = "json";
    xhr.onerror = function(e) {
	cb('', domain, host, '', data);
	return;
    };
    xhr.onload = function(e) {

	if (!this.response || this.status != 200 || this.response['Status'] != 0) {
	    cb('', domain, host, '', data);
	    return;
	}

	len = this.response['Answer'].length;
	if (len === 0) {
	    cb('', domain, host, '', data);
	    return;
	}

	// Get the value of the TXT record
	d = this.response['Answer'][len-1]['data'];
	d = d.split('"').join('');
	console.log('ddddd', d);
	// Get the JSON for the settings
	xhr2 = new XMLHttpRequest();
	xhr2.open('GET', 'https://' + d + '/v2/' + domain + '/settings');
	xhr2.responseType = "json";
	xhr.onerror = function(e) {
	    cb('', domain, host, '', data);
	    return;
	};

	xhr2.onload = function(e) {
	    if (!this.response || this.status != 200) {
		cb('', domain, host, '', data);
	    }
	    
	    url_api = this.response['urlAPI'];
	    url_sync = this.response['urlSyncUX'];
	    dns_provider_name = this.response['providerName'];

	    // Verify our template is supported
	    xhr3 = new XMLHttpRequest()
	    xhr3.open('GET', url_api + '/v2/domainTemplates/providers/' + providerId + '/services/' + serviceId);
	    xhr3.onerror = function(e) {
		cb('', domain, host, '', data);
		return;
	    }
	    xhr3.onload = function(e) {
		if (!this.response || this.status != 200) {
		    cb('', domain, host, '', data);
		    return;
		}

		cb(url_sync + '/v2/domainTemplates/providers/' + providerId + '/services/' + serviceId + '/apply?domain=' + domain + '&host=' + host,
		 domain, host, dns_provider_name, data);
		return;
	    }
	    xhr3.send();
	}
	xhr2.send();
    };
    xhr.send();
}

function callbackfunc(url, domain, host, provider_name, data) {
	if (url) {
		console.log('data', data);
		$('.analyze_blk').find('li').addClass('active');
		url = url + '&RANDOMTEXT=shm:0:' + encodeURIComponent(data) + '&IP=132.148.166.208'
		document.getElementById("domainconnect").innerHTML = `<a href='javascript:;'>${provider_name}</a>`
		
		$('#2-btn-loader').attr('href', url);
		$('#2-btn-loader').text(`Authorize with ${provider_name}`);

		// document.getElementById("domainconnect").innerHTML = "Click to <a target=_new href='" + url + "'>configure</a> your domain with " + provider_name
	} else {
		setTimeout(() => {
			$('.step_form_modal_step').removeClass('active');
			$('.step_form_modal_step').css('display', 'none');
			$('.step_form_modal_step-1').addClass('active').css('display', '');
			$('.step_for_pagi li').removeClass('active');
			$('.step_for_pagi li:first-child').addClass('active');
		}, 2000);
		$('#2-btn-loader').attr('href', 'javascript:;');
		document.getElementById('domainconnect').innerHTML = "Domain does not support domain connect";
	}
}

$(document).ready(function () {
	$('#txt_domain_btn').click(function (event) {
		event.preventDefault();
		
		var txt_domain_obj = $('#txt_domain_name');
		var domain_val = txt_domain_obj.val();
			
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
				setLoading();
				$('#show_loader').show();
			},
			success: function (res) {
				$('#show_loader').hide();
				if(res.status == "true") {
					console.log(res.message);
					callbackfunc(res.url, res.domain, res.host, res.provider_name, res.data);
				} else if(res.status == "false") {
					callbackfunc("", "", "", "", "");
					console.log(res.message);
				}
				console.log('res', res);
			},
			error: function (xhr) {
				callbackfunc("", "", "", "", "");
				ajaxErrorMsg(xhr);
			}
		});
		// domain_connect(domain, host, message, 'exampleservice.domainconnect.org', 'template1', callbackfunc);
	});

	
	$('#btn_show_modal').click(function (event) {
		event.preventDefault();
		$('#txt_domain_name').val('');
		$('#seedemomodal').modal('show');
		$('.modal_main_step').css('display','block');
		$('.step_form_modal').css('display','none');
		$('.sent_modal_box').css('display','none');
	});
});

function ajaxErrorMsg(xhr) {
	if (xhr.status === 422) {
		$.each(xhr.responseJSON.errors, function (key, val) {
			console.error(val);
		});
	} else {
		console.error(xhr.statusText);
	}
}