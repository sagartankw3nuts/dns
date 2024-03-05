from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
import requests
from django.views.decorators.csrf import csrf_exempt
from .models import Domain

@csrf_exempt
def domainStore(request):
    if (request.method == 'POST'):
        var_provider_id = "exampleservice.domainconnect.org"
        var_service_id = "template1"
        var_domain_name = request.POST.get('domain')
        var_host_name = request.POST.get('host')
        var_params = []
        response_data = {}

        try:
            if(var_domain_name == ''):
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
                        domain_save = Domain(
                            name = var_domain_name,
                            provider = 'Amazon Route 53',
                            application_id = request.app_login_id
                        )
                        domain_save.save()
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
                        domain_save = Domain(
                            name = var_domain_name,
                            provider = 'Hostinger',
                            application_id = request.app_login_id
                        )
                        domain_save.save()
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
                        domain_save = Domain(
                            name = var_domain_name,
                            provider = 'Inmotion Hosting',
                            application_id = request.app_login_id
                        )
                        domain_save.save()
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

            print(urlAPI_value)
            print(urlSyncUX_value)
            print(providerName_value)

            if(urlAPI_value == '' or urlSyncUX_value == '' or providerName_value == ''):
                response_data = {'message': 'something went wrong please try again', 'status' : False}
            
            xhr3 = requests.get(f"{urlAPI_value}/v2/domainTemplates/providers/{var_provider_id}/services/{var_service_id}")
            
            if(xhr3.status_code != 200):
                response_data = {'message': 'something went wrong please try again', 'status' : False}
            
            resUrl = f"{urlSyncUX_value}/v2/domainTemplates/providers/{var_provider_id}/services/{var_service_id}/apply?domain={var_domain_name}&host={var_host_name}"
            
            response_data = {
                'message' : 'success',
                "status" : True,
                "url" : resUrl,
                "domain" :var_domain_name,
                "host" :var_host_name,
                "provider_name" : providerName_value,
                "data" : xhr3.json()
            }
            domain_save = Domain(
                name = var_domain_name,
                provider = providerName_value,
                application_id = request.app_login_id
            )
            domain_save.save()
        except Exception as e:
            response_data = {'message': f"Unexpected error: {e}", 'status' : False}
        return JsonResponse(response_data)
    else:
        return HttpResponseBadRequest('Bad Request: This endpoint requires an AJAX request')
    
@csrf_exempt
def meapp(request):
        var_domain_name = request.POST.get('domain')
        response_data = {'message': 'Please enter a valid your domain', 'status' : False}
        return JsonResponse(response_data)
