from django.contrib import admin
from .models import FinalAllShifts, FinalCounterShifts, FinalKitchenShifts, FinalPersonalShifts, FinalSmgShifts

# Register your models here.
admin.site.register(FinalAllShifts)
admin.site.register(FinalCounterShifts)
admin.site.register(FinalKitchenShifts)
admin.site.register(FinalPersonalShifts)
admin.site.register(FinalSmgShifts)
