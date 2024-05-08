from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Vendor, PurchaseOrder

class APITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.vendor = Vendor.objects.create(name="Test Vendor", contact_details="Test Contact", address="Test Address", vendor_code="TEST001")
        self.purchase_order = PurchaseOrder.objects.create(po_number="PO01", vendor=self.vendor, order_date="2022-01-01", delivery_date="2022-01-15", items=["Item1", "Item2"], quantity=10, status="pending")

    def test_retrieve_all_vendors(self):
        response = self.client.get('/api/vendors/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_single_vendor(self):
        response = self.client.get(f'/api/vendors/{self.vendor.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.vendor.name)

    def test_retrieve_all_purchase_orders(self):
        response = self.client.get('/api/purchase_orders/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_single_purchase_order(self):
        response = self.client.get(f'/api/purchase_orders/{self.purchase_order.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['po_number'], self.purchase_order.po_number)

    def test_acknowledge_purchase_order(self):
        response = self.client.post(f'/api/purchase_orders/{self.purchase_order.id}/acknowledge/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('acknowledgment_date' in response.data)
