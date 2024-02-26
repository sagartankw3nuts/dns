$(document).ready(function(){

    $('#evt_app_modal').click(function (e) { 
        e.preventDefault();
        $('#app_name').val(null);
        $('#addapplicationmodal').modal('show');
    });

    $('#app_form').submit(function (e) { 
        e.preventDefault();
        var isValid = true;
        var el_app_name = $('#app_name');
            el_app_name.removeClass('form_error');

        if(el_app_name.val().trim() === '') {
            el_app_name.addClass('form_error');
            isValid = false;
        }

        if (isValid) {
            var form_data = $(this).serialize();
            $.ajax({
                url: $(this).attr('action'),
                type: 'POST',
                data: form_data,
                dataType: 'json',
                cache: false,
                beforeSend: function() {
                },
                success: function (res) {
                    $('#addapplicationmodal').modal('hide');
                    if(res.status == true) {
                        toastr.success(res.message);
                    } else if(res.status == false) {
                        toastr.error(res.message);
                    }
                },
                error: function (xhr) {
                    ajaxErrorMsg(xhr);
                }
            });
        }
    });

    $('#evt_all_app_credentials').change(function (e) { 
        e.preventDefault();
        var _secret = $(this).find("option:selected").data("secret");
        var _key = $(this).find("option:selected").data("key");
        var _txt = $(this).find("option:selected").text();
        var _image_url = $(this).find("option:selected").data('image');
        var _webhook = $(this).find("option:selected").data('webhook');

        $('#shw_app_name').val(_txt);
        $('#shw_app_web_url').val(_webhook);
        $('#shw_app_key').val(_key);
        $('#shw_app_secret').text(_secret);
        $('#app_profile_image_url').attr('src', _image_url);

    }).trigger('change');

    $('.evt_file_upload__').on('change', function (e) {
        e.preventDefault();
        var form = $('#app_profile_form');
        var actionUrl = form.attr('action');
        var formData = new FormData($('#app_profile_form')[0]);
            formData.append('app_key', $('#shw_app_key').val());
            formData.append('app_redirect_url', $('#shw_app_web_url').val());

            $.ajax({
                type: "POST",
                url: actionUrl,
                data: formData,
                dataType: 'json',
                cache: false,
                processData: false,
                contentType: false,
                success: function (res) {
                    // $("input[type='file']").val('');
                    if (res.status == true) {
                        $('#app_profile_image_url').attr('src', res.data.image_url);
                        $('#evt_all_app_credentials').find("option:selected").attr("src", res.data.image_path);
                    } else {
                    }
                },
                error: function (xhr) {
                    // $("input[type='file']").val('');
                    ajaxErrorMsg(xhr);
                }
            });
    });

    $('#evt_change_app_secret').on('click', function (e) {
        e.preventDefault();
            formData = {'app_secret' : true, 'app_key':  $('#shw_app_key').val()};

            $.ajax({
                type: "POST",
                url: '/app-update-secret-ajax',
                data: formData,
                dataType: 'json',
                cache: false,
                success: function (res) {
                    if (res.status == true) {
                        toastr.success(res.message);
                        $('#shw_app_secret').text(res.data.client_secret);
                    } else {
                        toastr.error(res.message);
                    }
                },
                error: function (xhr) {
                    ajaxErrorMsg(xhr);
                }
            });
    });

    $('#cmd_app_save').on('click', function (e) {
        e.preventDefault();
        $('#app_form').submit();
    });

    $('#shw_app_secret_copy').click(function (e) { 
        e.preventDefault();
        var temp = $("<input>");
        $("body").append(temp);
        temp.val($('#shw_app_secret').text()).select();
        document.execCommand("copy");
        temp.remove();
        toastr.success('Copy success');
    });

    $('#shw_app_key_copy').click(function (e) { 
        e.preventDefault();
        var temp = $("<input>");
        $("body").append(temp);
        temp.val($('#shw_app_key').val()).select();
        document.execCommand("copy");
        temp.remove();
        toastr.success('Copy success');
    });
})

function ajaxErrorMsg(xhr) {
    if (xhr.status === 422) {
        $.each(xhr.responseJSON.errors, function (key, val) {
            console.error(val);
        });
    } else {
        console.error(xhr.statusText);
    }
}