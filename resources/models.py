from django.db import models
from django.utils import timezone
from account.models import User
# Create your models here.
class Resource(models.Model):
    class Meta:
        db_table = "CIT_RESOURCE_TABLE"
    file_id = models.CharField(max_length=500,unique=True)
    file = models.FileField()
    unitname = models.CharField(max_length=30,verbose_name="unit name",blank=True)
    year = models.CharField(max_length=30,verbose_name="year of unit",blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.CharField(max_length=30,verbose_name="course name",blank=True)
    date_added = models.DateTimeField(default=timezone.now)


