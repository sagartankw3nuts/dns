from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from dnsdadweb.models import AppCredentials
from helpers import is_expired


class TokenMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        authorization_header = request.headers.get('Authorization')
        if authorization_header:
            try:
                token_type, token = authorization_header.split(' ')
                if (token_type.lower() == 'bearer' and token):
                    isToeknExist = AppCredentials.objects.filter(client_secret=token).first()
                    if(isToeknExist):
                            request.app_user_id = isToeknExist.user_id
                            request.app_login_id = isToeknExist.id
                            response = self.get_response(request)
                            response.status_code = 200
                            return response
                    else:
                        return JsonResponse({'error': 'Invalid token type'}, status=400)
                else:
                    return JsonResponse({'error': 'Invalid token type'}, status=400)
            except ValueError:
                return JsonResponse({'error': 'Invalid Authorization header format'}, status=400)
        else:
            if(request.path.startswith('/api/') == False):
                response = self.get_response(request)
                return response
            else:
                return JsonResponse({'error': 'Authorization header not found'}, status=400)
