# Importing Dependencies #
from django.db import models
from datetime import date, datetime



# Vendor Model #
class VendorProfileModel(models.Model):
    vendor_code = models.CharField(max_length=256, primary_key=True)
    name = models.CharField(max_length=256, null=True)
    contact_details = models.CharField(max_length=20, null=True)
    address = models.TextField()
    on_time_delivery_rate = models.FloatField(default=0)
    quality_rating_avg = models.FloatField(default=0)
    average_response_time = models.FloatField(default=0) # In Days #
    fulfillment_rate = models.FloatField(default=0)



# Purchase Order Model #
class PurchaseOrdersModel(models.Model):
    po_number = models.CharField(max_length=512, primary_key=True)
    vendor = models.ForeignKey(VendorProfileModel, on_delete=models.CASCADE)
    order_date = models.DateField(default=date.today)
    expected_delivery_date = models.DateField(null=False) # Extra Field -- useful is calculating "On Time Delivery Rate" #
    delivery_date = models.DateField(null=True)
    items = models.JSONField(null=False)
    quantity = models.IntegerField(null=False)
    status = models.CharField(max_length=32, default='pending', null=False)
    quality_rating = models.FloatField(null=True)
    issue_date = models.DateTimeField(null=False)
    acknowledgment_date = models.DateTimeField(null=True)



# Historical Performance Model #
class HistoricalPerformancesModel(models.Model):
    vendor = models.ForeignKey(VendorProfileModel, on_delete=models.CASCADE)
    date = models.DateTimeField(default=datetime.now)
    on_time_delivery_rate = models.FloatField(default=0)
    quality_rating_avg = models.FloatField(default=0)
    average_response_time = models.FloatField(default=0)
    fulfillment_rate = models.FloatField(default=0)