from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class LOG(models.Model):
    expression = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

