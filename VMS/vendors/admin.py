from django.contrib import admin
from .models import HistoricalPerformance,PurchaseOrder,Vendor
# Register your models here.
admin.site.register(HistoricalPerformance)
admin.site.register(Vendor)
admin.site.register(PurchaseOrder)