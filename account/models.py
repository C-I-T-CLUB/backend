from django.db import models
from django.utils import timezone

# Create your models here.
class User(models.Model):
    class Meta:
        db_table = "CIT_USER_TABLE"
    user_id = models.CharField(max_length=500,unique=True)
    firstname = models.CharField(max_length=30,verbose_name="Firstname",blank=True)
    lastname = models.CharField(max_length=30,verbose_name="Lastname",blank=True)
    email = models.EmailField(max_length=90, unique=True,verbose_name="Email")
    user_phone = models.CharField(max_length=15, unique=True, null=True, verbose_name="Telephone number")
    user_gender = models.CharField(max_length=15, verbose_name="Gender")
    user_password = models.TextField(max_length=200,verbose_name="Password")
    date_added = models.DateTimeField(default=timezone.now)
    role = models.TextField(max_length=50,verbose_name="User role",default="user")
    password_reset_code = models.TextField(max_length=20,verbose_name="Reset Code",default="")

