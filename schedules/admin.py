from django.contrib import admin

# Register your models here.
from .models import Crop, IrrigationMethod, SoilType, CropRelation, \
    Farmer,FarmerCropRelation, FarmerPumpRelation, \
    IrrigationTimeRate, Schedule, DayNightSchedule, \
    FarmerPowerRequirement
# Meta data and their relationships. Not for the application.
admin.site.register(Crop)
admin.site.register(IrrigationMethod)
admin.site.register(SoilType)
admin.site.register(CropRelation)
admin.site.register(IrrigationTimeRate)
# Farmer related. Need for the applications.
admin.site.register(Farmer)
admin.site.register(FarmerCropRelation)
admin.site.register(FarmerPumpRelation)
# Schedule related 
admin.site.register(Schedule)
admin.site.register(DayNightSchedule)
# Final calculations and relations for mobile app
admin.site.register(FarmerPowerRequirement)