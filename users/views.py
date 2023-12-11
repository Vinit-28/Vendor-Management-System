from rest_framework.views import APIView
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR
from rest_framework.response import Response
from users.models import UserModel
from users.serializers import UserModelSerializer
import bcrypt
from users.utilities import generate_token


# User Registration API #
class UserRegistration(APIView):
    def post(self, request):
        response = dict()
        status = HTTP_200_OK
        try:
            data = request.data.dict()
            data['password'] = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            serializer = UserModelSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                response['message'] = 'User Registration Sucessfull.'
            else:
                status = HTTP_400_BAD_REQUEST
                errors = serializer.errors
                response['message'] = errors
        except Exception as err:
            response['message'] = err
            status = HTTP_500_INTERNAL_SERVER_ERROR
        return Response(response, status=status)


# User Login API #
class LoginView(APIView):
    def post(self, request):
        response = dict()
        status = HTTP_200_OK
        try:
            data = request.data.dict()
            res = UserModel.objects.filter(pk=data['user_name'])
            if len(res) == 1:
                user = res[0]
                if bcrypt.checkpw(data['password'].encode('utf-8'), user.password.encode('utf-8')):
                    response['message'] = "Login Successfull"
                    response['token'] = generate_token(data['user_name'])
                else:
                    response['message'] = "Invalid Password"
            else:
                response['message'] = "Invalid Username"
        except Exception as err:
            response['message'] = err
            status = HTTP_500_INTERNAL_SERVER_ERROR
        return Response(response, status=status)