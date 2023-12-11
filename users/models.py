from django.db import models

# Create your models here.
class UserModel(models.Model):
    user_name = models.CharField(max_length=256, primary_key=True)
    password = models.CharField(max_length=256, null=False, blank=False)
    name = models.CharField(max_length=256, null=False)