from django.urls import path

from .views import index

app_name = 'top'
urlpatterns = [
    path('', index, name='index'),
]
