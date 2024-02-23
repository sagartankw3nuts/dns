$(document).ready(function(){

    var app_id = false;
    $('#evt_all_app_credentials_dashboard').change(function (e) { 
        e.preventDefault();

        app_id = $(this).val();

        // var _secret = $(this).find("option:selected").data("secret");
        var _key = $(this).find("option:selected").data("key");
        var _txt = $(this).find("option:selected").text();
        var _image_url = $(this).find("option:selected").data('image');
        var _webhook = $(this).find("option:selected").data('webhook');
        
        $('#shw_app_key').val(_key);
        // $('#shw_app_secret').text(_secret);

        ajaxChart(app_id)

        var dataTable_ = $('#app_data_table').DataTable();
            dataTable_.destroy();

        new DataTable('#app_data_table', {
            ajax: {
                url: '/dashboard-table',
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
            pageLength: 2,
            lengthChange: false,
            // searching: false,
            paging: true
        });
    }).trigger('change');

    $('#evt_export_all_domain').click(function (e) { 
        e.preventDefault();
        var search_val = $('input[type="search"]').val();
        var app_val = $('#evt_all_app_credentials_dashboard').val();
        
        var params = {
            query: search_val,
            app: app_val
        };
        var baseUrl = 'domian-export-csv/';
        var url = baseUrl + '?' + $.param(params);
        window.location.href = url;
    });

    $('#evt_key_cpy').click(function (e) { 
        e.preventDefault();
        var temp = $("<input>");
        $("body").append(temp);
        temp.val($('#shw_app_key').val()).select();
        document.execCommand("copy");
        temp.remove();
        toastr.success('Copy success');
    });
})

function ajaxChart(app_id) {
    $.ajax({
        type: "POST",
        url: '/dashboard-chart',
        data: {
            'category': app_id
        },
        dataType: 'json',
        cache: false,
        success: function (res) {
                initPieChart(res.pichart);
        },
        error: function (xhr) {
            ajaxErrorMsg(xhr);
        }
    });
}

function initPieChart(res_pichart) {
    const pichart_data_obj = {
        labels: res_pichart.label,
        datasets: [{
            data: res_pichart.label_data,
            backgroundColor: [
                // 'rgb(13, 110, 253, 1.0)',
                // 'rgb(13, 110, 253, 0.8)',
                // 'rgb(13, 110, 253, 0.6)',
                // 'rgb(13, 110, 253, 0.4)',
                // 'rgb(13, 110, 253, 0.8)',
            ],
            hoverOffset: 4
        }]
    };

    $('#div_pie_chart_deals').empty();

    var pieChartElement = document.createElement("canvas");
    pieChartElement.id = 'pie_chart_deals';
    $('#div_pie_chart_deals').html(pieChartElement);

    pie_chart = new Chart(document.getElementById('pie_chart_deals'), {
        type: 'pie',
        data: pichart_data_obj,
        options: {
            plugins: {
                responsive: true,
                // maintainAspectRatio: true,
                legend: {
                    position: 'bottom',
                },
            },
        }
    });

    pie_chart.canvas.parentNode.style.height = '400px';
    pie_chart.canvas.parentNode.style.width = '400px';
}