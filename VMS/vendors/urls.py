from .views import *
from django.urls import path


urlpatterns = [ 
    #vendor
    path('vendors/', vendors, name='vendors'),
    path('vendors/<str:vendor_id>/', vendor_operations, name='vendor_operations'),
    #purchase orders
    path('purchase_orders/', purchase_orders, name='purchase_orders'),
    path('purchase_orders/<str:po_id>/', purchase_order_operations, name='purchase_order_operations'),
    
    #vendor performance
    path('vendors/<str:vendor_id>/performance/', retrieve_vp, name='retrieve_vendor_performance'),
]