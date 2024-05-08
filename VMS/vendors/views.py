from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from django.shortcuts import get_object_or_404
from .models import Vendor,PurchaseOrder,HistoricalPerformance
from .serializers import VendorSerializer,HistoricalPerformanceSerializer,PurchaseOrderSerializer

# vendors details
class VendorsAPIView(APIView):
    def post(self, request):
        serializer = VendorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        vendors = Vendor.objects.all()
        serializer = VendorSerializer(vendors, many=True)
        return Response(serializer.data)
    
vendors = VendorsAPIView.as_view()


class VendorOperationsAPIView(APIView):
    def get(self, request, vendor_id):
        vendor = get_object_or_404(Vendor, pk=vendor_id)
        serializer = VendorSerializer(vendor)
        return Response(serializer.data)
    def put(self, request, vendor_id):
        vendor = get_object_or_404(Vendor, pk=vendor_id)
        serializer = VendorSerializer(vendor, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request, vendor_id):
        vendor = get_object_or_404(Vendor, pk=vendor_id)
        vendor.delete()
        return Response({'message': 'Vendor deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
vendor_operations = VendorOperationsAPIView.as_view()


# Purchase Order Tracking
class PurchaseOrdersAPIView(APIView):
    def post(self, request):
        serializer = PurchaseOrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def get(self, request):
        purchase_orders = PurchaseOrder.objects.all()
        serializer = PurchaseOrderSerializer(purchase_orders, many=True)
        return Response(serializer.data)
    
purchase_orders = PurchaseOrdersAPIView.as_view()

class PurchaseOrderOperationsAPIView(APIView):
    def get(self, request, po_id):
        purchase_order = get_object_or_404(PurchaseOrder, pk=po_id)
        serializer = PurchaseOrderSerializer(purchase_order)
        return Response(serializer.data)
    def put(self, request, po_id):
        purchase_order = get_object_or_404(PurchaseOrder, pk=po_id)
        serializer = PurchaseOrderSerializer(purchase_order, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def put(self, request, po_id):
        # Retrieve the purchase order
        purchase_order = get_object_or_404(PurchaseOrder, pk=po_id)
        
        # Change the status to 'pending'
        purchase_order.status = 'pending'
      
        purchase_order.save()
        
        # Serialize and return the updated purchase order
        serializer = PurchaseOrderSerializer(purchase_order)
        return Response(serializer.data)
    def delete(self, request, po_id):
        purchase_order = get_object_or_404(PurchaseOrder, pk=po_id)
        purchase_order.delete()
        return Response({'message': 'Purchase order deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
purchase_order_operations = PurchaseOrderOperationsAPIView.as_view()

# Endpoint to acknowledge purchase order
class PurchaseOrderAcknowledgeAPIView(APIView):
    def post(self, request, po_id):
        purchase_order = get_object_or_404(PurchaseOrder, pk=po_id)
        purchase_order.status = 'completed'
        purchase_order.acknowledgment_date = timezone.now()
        purchase_order.save()
        # Include acknowledgment_date in the response data
        acknowledgment_date = purchase_order.acknowledgment_date.strftime("%Y-%m-%d %H:%M:%S") if purchase_order.acknowledgment_date else None
        response_data = {
            'message': 'Purchase order acknowledged successfully',
            'acknowledgment_date': acknowledgment_date
        }
        return Response(response_data, status=status.HTTP_200_OK)
purchase_order_acknowledge = PurchaseOrderAcknowledgeAPIView.as_view()

# Vendor Performance Evaluation
class RetrieveVendorPerformanceAPIView(APIView):
    def get(self, request, vendor_id):
        vendor = get_object_or_404(Vendor, pk=vendor_id)
        vendor_performance = {
            'on_time_delivery_rate': vendor.on_time_delivery_rate,
            'quality_rating': vendor.quality_rating_avg,
            'response_time': vendor.average_response_time,
            'fulfillment_rate': vendor.fulfillment_rate
        }
        return Response(vendor_performance)
retrieve_vp = RetrieveVendorPerformanceAPIView.as_view()



