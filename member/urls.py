from django.urls import path

from .views import members_list, members_add, members_modify

app_name = 'member'
urlpatterns = [
    path('', members_list, name='list'),
    path('add/', members_add, name='add'),
    path('modify/<int:partner_number>/', members_modify, name='modify'),
]
