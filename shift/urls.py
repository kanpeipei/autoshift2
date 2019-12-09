from django.urls import path

from .views import shifts_list, shifts_write

app_name = 'shift'
urlpatterns = [
    path('', shifts_list, name='list'),
    path('write/<int:partner_number>/<int:year>/<int:month>/', shifts_write, name='write'),
]


