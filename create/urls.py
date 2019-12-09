from django.urls import path

# from .views import select, create
from .views import create

app_name = 'create'
urlpatterns = [
    # path('select/', select, name='select'),
    path('create/', create, name='create')
]

