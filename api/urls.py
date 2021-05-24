from django.urls import path,include
from . import views
from rest_framework.routers import DefaultRouter

# router = DefaultRouter()

# router.register('task',views.TaskModelViewSet,basename='abcd')

urlpatterns = [
    path('', views.Index.as_view(),name='index'),
    path('logout', views.logOut.as_view(),name='logout'),
    path('task-list/', views.TaskList.as_view(),name='task-list'),
    path('api/task-detail/<int:pk>', views.TaskDetail.as_view(),name='task-detail'),
    # path('api/',include(router.urls)),
]
