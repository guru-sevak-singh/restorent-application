from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.Restorent)
admin.site.register(models.Table)
admin.site.register(models.Floor)
admin.site.register(models.UserProfile)
admin.site.register(models.FoodCategory)
admin.site.register(models.FoodItem)
admin.site.register(models.Tax)
admin.site.register(models.Order)