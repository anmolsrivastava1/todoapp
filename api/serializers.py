from rest_framework import serializers
from .models import Task
from django.contrib.auth.models import User
from rest_framework.fields import CurrentUserDefault
# class UserSerializers(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields=['username']

class TaskSerializer(serializers.ModelSerializer):
    # person = UserSerializers()
    # url = serializers.HyperlinkedIdentityField(view_name="task-detail")
    person = serializers.HiddenField(default=serializers.CurrentUserDefault())
    task = serializers.CharField(style={'placeholder':'Task'})
    due_date = serializers.DateField(style={'placeholder':'Date','value':'date'})

    class Meta:
        model = Task
        fields='__all__'
        # ordering = ['-is_completed','due_date']

        # read_only_fields = ['person']

    # def save(self,usr):
    #     person = usr  # <= magic!
    #     task = self.validated_data['task']
    #     is_completed = self.validated_data['is_completed']
    #     due_date = self.validated_data['due_date']
