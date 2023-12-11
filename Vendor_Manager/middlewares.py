# Importing Dependencies #
import jwt
from decouple import config
from django.conf import settings
from django.http import JsonResponse
from rest_framework.status import HTTP_400_BAD_REQUEST


# Custom Middleware for Authentication #
class Authenticator:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        unsecured_endpoints = getattr(settings, 'UNSECURED_ENDPOINTS', [])
        if request.path in unsecured_endpoints:
            return self.get_response(request)
        elif len(request.headers.get('Authorization', "").split(" ")) == 2:
            auth_header = request.headers.get('Authorization')
            bearer, token = auth_header.split(" ")
            res = self.isTokenValid(token)
            if res[0]:
                return self.get_response(request)
            else:
                return JsonResponse({
                    'message': res[1]
                }, status=HTTP_400_BAD_REQUEST)
        else:
            return JsonResponse({
                'message': 'Invalid Authorization Headers.'
            }, status=HTTP_400_BAD_REQUEST)


    # Validating the token #
    def isTokenValid(self, token):
        try:
            secret_key = config('JWT_SECRET_KEY')
            decoded_token = jwt.decode(token, secret_key, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return False, 'Token expired. Please re-authenticate.'
        except jwt.InvalidTokenError:
            return False, 'Invalid token. Authentication failed.'
        except jwt.DecodeError:
            return False, 'Decoding error.'
        return True, "Token Validated"