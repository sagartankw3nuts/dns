$(document).ready(function(){

    var app_id = false;
    $('#evt_all_app_credentials').change(function (e) { 
        e.preventDefault();

        app_id = $(this).val();

        var _secret = $(this).find("option:selected").data("secret");
        var _key = $(this).find("option:selected").data("key");
        var _txt = $(this).find("option:selected").text();
        var _image_url = $(this).find("option:selected").data('image');
        var _webhook = $(this).find("option:selected").data('webhook');
        
        $('#shw_app_key').val(_key);
        $('#shw_app_secret').text(_secret);

    }).trigger('change');

    console.log('app_id', app_id);
})
