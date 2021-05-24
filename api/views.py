from django.shortcuts import render,redirect
from .models import Task
from .serializers import TaskSerializer
from rest_framework import generics,viewsets
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication,BasicAuthentication
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from django.contrib.auth import authenticate, login, logout
from rest_framework import status
from django.core.mail import send_mail
from datetime import date
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from decouple import config

reminder=[]

class Index(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    
    def get(self, request, format=None):
        print(request.user)
        try:
            print(request.user.first_name)
            return redirect('task-list')
        except:
            pass
        task = Task.objects.filter(due_date=date.today(),is_completed=False)
        print(reminder)
        if date.today() not in reminder:
            reminder.clear()
            reminder.append(date.today())
            for t in task:
                if t.due_date==date.today():
                    person = t.person
                    send_mail(
                        'Reminder from the todo list',
                        "Your task "+t.task+" 's due date is today..",
                        'bing.chandl3r@gmail.com',
                        [t.person.email],
                        fail_silently=False,
                    )
            print(reminder)        
        return Response(template_name='index.html')


    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request,username=username,password=password)
        print(user)
        if user is None:
            messages.error(request,"Invalid Username or Password")
            return redirect('index')
        login(request,user)
        return redirect('task-list')

class logOut(APIView):
    def get(self, request):
        logout(request)
        return redirect('index')

class TaskList(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    # authentication_classes = [ BasicAuthentication]
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = TaskSerializer()
        tasks = request.user.task_set.all().order_by('is_completed','due_date')
        return Response({'serializer':serializer,'tasks':tasks},template_name='dashboard.html')

    def post(self, request):
        serializer = TaskSerializer(data=request.data, context={'request': self.request})
        if serializer.is_valid():
            serializer.save()
            
        else:
            print(serializer.error_messages)
        return redirect('task-list')


class TaskDetail(APIView):
    def get_object(self, pk):
        try:
            return Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        task = self.get_object(pk)
        serializer = TaskSerializer(task)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        task = self.get_object(pk)
        serializer = TaskSerializer(task, data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            print(serializer.errors)
        return JsonResponse({'errors':serializer.errors, 'status':status.HTTP_400_BAD_REQUEST})

    def delete(self, request, pk, format=None):
        task = self.get_object(pk)
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# class TaskModelViewSet(viewsets.ModelViewSet):
#     queryset = Task.objects.all()
#     serializer_class = TaskSerializer
