from rest_framework.serializers import ModelSerializer
from users.models import UserModel



class UserModelSerializer(ModelSerializer):
    class Meta:
        model = UserModel
        fields = '__all__'