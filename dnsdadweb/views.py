from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest, HttpResponseServerError
from django.core.exceptions import ValidationError
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import requests
from .models import AppCredentials, AppCredentialsToken
from .models import SubscriptionPlan, UserSubscription
from api.models import Domain
import uuid
import secrets
import os
from django.conf import settings
from django.contrib import messages
from datetime import datetime,timedelta
from django.db.models import Count
from django.core.paginator import Paginator
from django.db.models import Q
import csv
import urllib.parse


def home(request):
    return render(request, 'home.html')

@login_required
def dashboard(request):
    app_credentials = AppCredentials.objects.filter(user_id=request.user.id)
    contxt = {
        'app_credentials' : app_credentials
    }
    return render(request, 'backend/dashboard.html', contxt)

@login_required
def appSettingCreate(request):
    
    app_credentials = AppCredentials.objects.filter(user_id=request.user.id)
    contxt = {
        'app_credentials' : app_credentials
    }

    return render(request, 'backend/app-settings.html', contxt)

@csrf_exempt
def ajaxPostDomain(request):
    if (request.method == 'POST'):
        var_provider_id = "exampleservice.domainconnect.org"
        var_service_id = "template1"
        var_domain_name = request.POST.get('domain')
        var_host_name = request.POST.get('host')
        var_params = []
        response_data = {}

        try:
            if(var_domain_name == ''):
                # result = Helpers.sum(10, 20)
                # response_data = {'message': f'Please enter a valid your domain {result}', 'status' : False}
                response_data = {'message': 'Please enter a valid your domain', 'status' : False}
                return JsonResponse(response_data)
            
            xhr = requests.get('https://dns.google/resolve?type=txt&name=_domainconnect.'+var_domain_name)
            
            if(xhr.status_code != 200 or xhr.json().get('Status') != 0):
                response_data = {'message': 'something went wrong please try again', 'status' : False}
            
            answerField = xhr.json().get('Answer', [])
            
            count = len(answerField)
            if(count == 0):
                if(xhr.json().get('Status') == 3 and xhr.status_code == 200):
                    varAuthorityType = xhr.json().get('Authority')[-1]['data']
                    # Split the string by whitespace
                    parts = varAuthorityType.split()
                    # Find and extract the substring
                    awsdns_hostmaster = next((part for part in parts if "amazon.com" in part), None)
                    if(awsdns_hostmaster == 'awsdns-hostmaster.amazon.com.'):
                        response_data = {
                            'message' : 'success',
                            "status" : True,
                            "url" : 'javascript::',
                            "domain" :var_domain_name,
                            "host" :var_host_name,
                            "provider_name" : 'Amazon Route 53',
                            "data" : 'javascript::'
                        }
                        return JsonResponse(response_data)
                    
                    hostinger_hostmaster = next((part for part in parts if "hostinger.com" in part), None)
                    if(hostinger_hostmaster == 'dns.hostinger.com.'):
                        response_data = {
                            'message' : 'success',
                            "status" : True,
                            "url" : 'javascript::',
                            "domain" :var_domain_name,
                            "host" :var_host_name,
                            "provider_name" : 'Hostinger',
                            "data" : 'javascript::'
                        }
                        return JsonResponse(response_data)

                    inmotion_hostmaster = next((part for part in parts if "inmotionhosting.com" in part), None)\
                    
                    if(inmotion_hostmaster == 'ns1.inmotionhosting.com.'):
                        response_data = {
                            'message' : 'success',
                            "status" : True,
                            "url" : 'javascript::',
                            "domain" :var_domain_name,
                            "host" :var_host_name,
                            "provider_name" : 'Inmotion Hosting',
                            "data" : 'javascript::'
                        }
                    return JsonResponse(response_data)

            if answerField:
                lastData = answerField[-1]['data']

            xhr2 = requests.get(f"https://{lastData}/v2/{var_domain_name}/settings")

            if(xhr2.status_code != 200):
                response_data = {'message': 'something went wrong please try again', 'status' : False}
            
            # Get the values using the xhr2 response
            urlAPI_value = xhr2.json().get('urlAPI', '')
            urlSyncUX_value = xhr2.json().get('urlSyncUX', '')
            providerName_value = xhr2.json().get('providerName', '')

            if(urlAPI_value == '' or urlSyncUX_value == '' or providerName_value == ''):
                response_data = {'message': 'something went wrong please try again', 'status' : False}
            
            xhr3 = requests.get(f"{urlAPI_value}/v2/domainTemplates/providers/{var_provider_id}/services/{var_service_id}")
            
            if(xhr3.status_code != 200):
                response_data = {'message': 'something went wrong please try again', 'status' : False}
            
            resUrl = f"{urlSyncUX_value}/v2/domainTemplates/providers/{var_provider_id}/services/{var_service_id}/apply?domain={var_domain_name}&host={var_host_name}"
        
            cUrl = f"{resUrl}&RANDOMTEXT=shm:0:{urllib.parse.quote(xhr3.json())}&IP=172.105.47.42"
            
            response_data = {
                'message' : 'success',
                "status" : True,
                "url" : resUrl,
                "domain" :var_domain_name,
                "host" :var_host_name,
                "provider_name" : providerName_value,
                "data" : xhr3.json(),
                'curl': cUrl
            }

            # Print the values
            # print("urlAPI:", urlAPI_value)
            # print("urlSyncUX:", urlSyncUX_value)
            # print("providerName:", providerName_value)
        except Exception as e:
            response_data = {'message': f"Unexpected error: {e}", 'status' : False}
        return JsonResponse(response_data)
    else:
        # The request is not an AJAX request
        return HttpResponseBadRequest('Bad Request: This endpoint requires an AJAX request')

@login_required
def appSettingStore(request):
    try:
        if request.method == 'POST':
            var_app_name = request.POST.get('app_name')
            var_app_uuid = uuid.uuid4().hex
            var_app_secrets = secrets.token_hex(32)
            
            app_save = AppCredentials(name=var_app_name, client_id=var_app_uuid, client_secret=var_app_secrets, user_id=request.user.id)
            app_save.save()
            
            response_data = {'message': 'Application added', 'status' : True}
            status_code = 200
        else:
            response_data = {'message': 'Invalid request method', 'status': False}
            status_code = 400
    except ValidationError as e:
        response_data = {'message': str(e), 'status': False}
        status_code = 400
    except Exception as e:
        response_data = {'message': 'Something went wrong: ' + str(e), 'status': False}
        status_code = 500

    return JsonResponse(response_data, status=status_code)

def appFileUpload(request):
    if (request.method == 'POST' and request.POST.get('app_key')):
        try:
            var_app_key = request.POST.get('app_key')
            app_profile = AppCredentials.objects.get(client_id=var_app_key)
        except AppCredentials.DoesNotExist:
            return JsonResponse({'status': False, 'message': 'User profile not found.'}, status=404)

        # the delet file
        if(request.FILES.get('app_image')):
            
            uploaded_file = request.FILES['app_image']

            # Update the image field with the new file
            random_filename = str(uuid.uuid4())
            
            # Get filename
            filename = uploaded_file.name
            
            # Get file size
            file_size = uploaded_file.size

            # Get file extension
            file_extension = filename.split('.')[-1].lower()
            
            # Rename the file
            new_filename = f"{random_filename}.{file_extension}"

            uploaded_file.name = new_filename

            allowed_extensions = ['png', 'jpg', 'jpeg', 'svg']
            
            if file_extension not in allowed_extensions:
                messages.error(request, 'File type not allowed.')
                return redirect('app.setting')

            if app_profile.app_image:
                old_image_path = os.path.join(settings.MEDIA_ROOT, str(app_profile.app_image))
                if os.path.exists(old_image_path):
                    os.remove(old_image_path)
            
            # Save the file to a specific location
            with open(os.path.join(settings.MEDIA+settings.APP_FILE_ROOT, new_filename), 'wb+') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)

            app_profile.app_image = settings.APP_FILE_ROOT+new_filename
        app_profile.redirect_uris = request.POST.get('app_redirect_url')
        app_profile.save()

        # image_url = request.build_absolute_uri(app_profile.app_image.url)

        return redirect('/app-setting')
        # return JsonResponse({'status': True, 'message': 'Profile image updated successfully.', 'data' : {
        #     'image_url' : image_url,
        #     'image_path' : app_profile.app_image.url
        # }})
    else:
        return JsonResponse({'status': False, 'message': 'invalid request method.'})

def appUpdateSecret(request):
    if (request.method == 'POST' and request.POST.get('app_secret') and request.POST.get('app_key')):
        try:
            var_app_key = request.POST.get('app_key')
            app_profile = AppCredentials.objects.get(client_id=var_app_key)
        except AppCredentials.DoesNotExist:
            return JsonResponse({'status': False, 'message': 'User profile not found.'}, status=404)
        var_app_secrets = secrets.token_hex(32)
        app_profile.client_secret = var_app_secrets
        app_profile.save()
    
        return JsonResponse({'status': True, 'message': 'Client secret updated successfully.', 'data' : {
            'client_secret' : app_profile.client_secret,
        }})
    else:
        return JsonResponse({'status': False, 'message': 'No image file provided or invalid request method.'})
    
@login_required
def billingCreate(request):
    return render(request, 'backend/billing.html')

@login_required
def dashboardDataTable(request):
    
    draw = int(request.GET.get('draw', 1)) 
    start = int(request.GET.get('start', 0))
    length = int(request.GET.get('length', 2))  
    category_value = request.GET.get('category')
    search_value = request.GET.get('search[value]', None)

    if category_value:
        queryset = Domain.objects.filter(application_id=category_value)

        if search_value:
            name_query = Q(name__icontains=search_value)
            provider__icontains = Q(provider__icontains=search_value)
            queryset = queryset.filter(name_query | provider__icontains)

        paginator = Paginator(queryset, length)
        page_number = (start // length) + 1
        page = paginator.get_page(page_number)
        
        data = list(page.object_list.values('name', 'provider', 'status')) 

        response = {
            'data': data,
            'draw': draw,
            'recordsFiltered': paginator.count,
            'recordsTotal': paginator.count,
            'search_value': search_value
        }

        return JsonResponse(response)
    else:
        return JsonResponse({'error': 'Category value not provided'}, status=400)

@login_required
def dashboardChart(request):
    category_value = request.POST.get('category')
    var_data_label = []
    var_data_data = []
    if category_value:
        queryset = Domain.objects.filter(application_id=category_value).values('provider').annotate(count=Count('provider'))
        if queryset.exists():
            for domain in queryset:
                var_data_label.append(domain['provider'])
                var_data_data.append(domain['count'])

            return JsonResponse({'pichart': {'label' : var_data_label, 'label_data' : var_data_data}, 'message': 'succes', 'status' : True})
        else:
            return JsonResponse({'pichart': [], 'message': 'data not found', 'status' : False})
    else:
        return JsonResponse({'error': 'Category value not provided'}, status=400)

@login_required
def planList(request):
    planList = SubscriptionPlan.objects.all()
    contxt = {
        'planList' : planList
    }
    return render(request, 'backend/plan.html', contxt)

@login_required
def planStore(request, plan_id):
    try:
            isPlan = SubscriptionPlan.objects.get(id=plan_id)
            if(isPlan and isPlan.id > 0):
                # Get the current date
                current_date = datetime.now()
                # Add a certain number of months
                number_of_months_to_add = isPlan.duration_months
                future_date = current_date + timedelta(days=number_of_months_to_add * 30)

                user_plan_save = UserSubscription(
                    plan_id = plan_id, 
                    start_date = current_date.date(),
                    end_date = future_date,
                    user_id = request.user.id,
                    )
                user_plan_save.save()

                return redirect('/plan')
            else:
                return render(request, 'backend/404.html')

            # response_data = {'message': 'Application added', 'status' : True,  'time': request.user.id}
            # status_code = 200
            # return JsonResponse(response_data, status=status_code)
    except Exception as e:
        return render(request, 'backend/404.html')
    

def export_csv(request):
    try:
        filename = f"{uuid.uuid4().hex}.csv"
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'

        writer = csv.writer(response)
        # Write header row
        writer.writerow(['Domain Name', 'Provider Name', 'Status'])

        app_id = request.GET.get('app', None)
        search_value = request.GET.get('query', None)

        if app_id:
            queryset = Domain.objects.filter(application_id=app_id)

            if search_value:
                name_query = Q(name__icontains=search_value)
                provider__icontains = Q(provider__icontains=search_value)
                queryset = queryset.filter(name_query | provider__icontains)
        
        if(queryset):
            for val in queryset:
                writer.writerow([val.name, val.provider, val.status])

        return response
    except Exception as e:
        return HttpResponseServerError("An error occurred while exporting the CSV file.")