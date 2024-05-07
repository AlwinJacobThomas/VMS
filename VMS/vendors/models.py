from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models.signals import post_save
from django.dispatch import receiver,Signal

# Create your models here.
class Vendor(models.Model):
    name = models.CharField(max_length=100)
    contact_details = models.TextField()
    address = models.TextField()
    vendor_code = models.CharField(max_length=100,unique=True,blank=True, null=True)
    on_time_delivery_rate = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(100.0)],null=True,blank=True)
    quality_rating_avg = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(5.0)],null=True,blank=True)
    average_response_time = models.FloatField(null=True,blank=True)
    fulfillment_rate = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(100.0)],null=True,blank=True)
    #for custom vendor code
    def save(self, *args, **kwargs):
        if not self.vendor_code:
            last_vendor = Vendor.objects.order_by('id').last()
            if last_vendor:
                last_vendor_id = int(last_vendor.vendor_code.split('VCODE')[-1]) + 1
                self.vendor_code = f'VCODE{last_vendor_id}'
            else:
                self.vendor_code = 'VCODE1'
        super().save(*args, **kwargs)
        
    def __str__(self):
        return self.name

class PurchaseOrder(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled'),
    ]

    po_number = models.CharField(max_length=100,unique=True,null=True,blank=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, null=True)
    order_date = models.DateTimeField()
    delivery_date = models.DateTimeField()
    items = models.JSONField()
    quantity = models.IntegerField(validators=[MinValueValidator(1)])
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    quality_rating = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(5.0)], null=True, blank=True)
    issue_date = models.DateTimeField(auto_now_add=True)
    acknowledgment_date = models.DateTimeField(null=True, blank=True)
    #for custom po number
    def save(self, *args, **kwargs):
        if not self.po_number:
            last_po = PurchaseOrder.objects.all().order_by('id').last()
            if last_po:
                last_po_number = int(last_po.po_number.split('PO')[-1]) + 1
                self.po_number = f'PO{last_po_number}'
            else:
                self.po_number = 'PO1'
        super().save(*args, **kwargs)
        
    def __str__(self):
        return self.po_number

class HistoricalPerformance(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    date = models.DateTimeField()
    on_time_delivery_rate = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(100.0)])
    quality_rating_avg = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(5.0)])
    average_response_time = models.FloatField()
    fulfillment_rate = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(100.0)])

    def __str__(self):
        return f"{self.vendor.name} - {self.date}"
    
# Signal handling function

@receiver(post_save, sender=PurchaseOrder)
def update_vendor_on_time_delivery_rate(sender, instance, created, **kwargs):
    if instance.status == 'completed':
        vendor = instance.vendor
        completed_orders = PurchaseOrder.objects.filter(vendor=vendor, status='completed')
        on_time_orders = completed_orders.filter(delivery_date__lte=instance.delivery_date)
        if completed_orders.count() > 0:
            on_time_delivery_rate = (on_time_orders.count() / completed_orders.count()) * 100
        else:
            on_time_delivery_rate = 0
        vendor.on_time_delivery_rate = on_time_delivery_rate
        vendor.save()
post_save.connect(update_vendor_on_time_delivery_rate, sender=PurchaseOrder)        