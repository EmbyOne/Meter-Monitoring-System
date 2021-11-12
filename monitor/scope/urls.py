from django.urls import path
from . import views

from .tasks import scheduler

urlpatterns = [
    path('api/', views.bigApiView)
]

scheduler.start()