from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Task(models.Model):
    person = models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
    task = models.CharField(max_length=400,blank=False,null=False)
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField()
    def __str__(self):
        return self.task