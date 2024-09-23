from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.mainPage),
    path('host_select/', views.hostSelect),
    path('metrics_select/', views.MetricsSelect),
    path('report_gen/', views.reportGen),
]