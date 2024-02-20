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


        var dataTable_ = $('#app_data').DataTable();
            dataTable_.destroy();

        new DataTable('#app_data', {
            ajax: {
                url: '/get_data',
                    type: 'GET',
                    data: {
                        'category': app_id
                    },
            },
            columns: [
                { data: 'name' },
                { data: 'provider' },
                { data: 'status' }
            ],
            processing: true,
            serverSide: true,
            // pageLength: 2, // Set the number of records per page to 2
            // lengthMenu: [ [2, 5, 10, -1], [2, 5, 10, "All"] ], 
        });
        console.log('app_id', app_id);
    }).trigger('change');

})
