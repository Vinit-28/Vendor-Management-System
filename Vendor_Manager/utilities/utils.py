# Importing Dependencies #
from django.db.models import F, Sum, Q
import Vendor_Manager


# Calculating On-Time Delivery Rate #
def get_on_time_delivery_rate(vendor):
    print(f"\nCalculating the On-Time Delivery Rate for Vendor {vendor}.")
    try:
        completed_orders = Vendor_Manager.models.PurchaseOrdersModel.objects.filter(
            status__iexact='completed',
            vendor=vendor
        ).count()
        timely_completed_orders = Vendor_Manager.models.PurchaseOrdersModel.objects.filter(
            status__iexact='completed',
            vendor=vendor,
            delivery_date__isnull=False,
            delivery_date__lte=F('expected_delivery_date')
        ).count()
        print("Completed Orders:", completed_orders)
        print("Timely Completed Orders:", timely_completed_orders)
        on_time_delivery_rate = timely_completed_orders / completed_orders * 100
        on_time_delivery_rate = float("{:.2f}".format(on_time_delivery_rate))
    except Exception as err:
        print(f"Execption occurred: {err}")
        on_time_delivery_rate = 0
    print("On-Time Delivery Rate:", on_time_delivery_rate)
    return on_time_delivery_rate
    

# Calculating Quality Rating Average #
def get_quality_rating_avg(vendor):
    print(f"\nCalculating the Quality Rating Average for Vendor {vendor}.")
    try:
        completed_po = Vendor_Manager.models.PurchaseOrdersModel.objects.filter(
            status__iexact='completed',
            vendor=vendor,
            quality_rating__isnull=False
        )
        completed_po_count = completed_po.count()
        rating_sum = completed_po.aggregate(rating_sum=Sum('quality_rating'))['rating_sum']
        print("Completed Purchase Orders(Having Ratings) Count:", completed_po_count)
        print("Rating Sum:", rating_sum)
        quality_rating_avg = rating_sum / completed_po_count
    except Exception as err:
        print(f"Execption occurred: {err}")
        quality_rating_avg = 0
    print("Quality Rating Average:", quality_rating_avg)
    return quality_rating_avg


# Calculating Average Response Time #
def get_average_response_time(vendor):
    print(f"\nCalculating the Average Response Time for Vendor {vendor}.")
    try:
        ack_purchase_orders = Vendor_Manager.models.PurchaseOrdersModel.objects.filter(
            vendor=vendor,
            acknowledgment_date__isnull=False
        ).annotate(
            response_time=(F('acknowledgment_date') - F('issue_date'))
        )
        total_orders = ack_purchase_orders.count()
        response_time_sum = ack_purchase_orders.aggregate(
            response_time_sum=Sum('response_time')
        )['response_time_sum']
        print("Total Acknowledged Purchase Orders:", total_orders)
        print("Response Time Sum:", response_time_sum)
        average_response_time = (response_time_sum / total_orders).days
    except Exception as err:
        print(f"Execption occurred: {err}")
        average_response_time = 0
    print("Average Response Time:", average_response_time)
    return average_response_time


# Calculating Fulfillment Rate #
def get_fulfillment_rate(vendor):
    print(f"\nCalculating the Fulfillment Rate for Vendor {vendor}.")
    try:
        purchase_orders = Vendor_Manager.models.PurchaseOrdersModel.objects.filter(
            vendor=vendor
        )
        all_po_count = purchase_orders.count()
        completed_po_count = purchase_orders.filter(
            status__iexact='completed'
        ).count()
        print("Purchase Orders Count:", all_po_count)
        print("Completed Purchase Orders Count:", completed_po_count)
        fulfillment_rate = completed_po_count / all_po_count * 100
    except Exception as err:
        print(f"Execption occurred: {err}")
        fulfillment_rate = 0
    print("Fulfillment Rate:", fulfillment_rate)
    return fulfillment_rate


# Updating vendor profile with updated performance stats #
def update_vendor_profile(vendor, data):
    print("Updating vendor profile with updated performance stats.")
    serializer = Vendor_Manager.serializers.VendorProfileSerializer(vendor, data, partial=True)
    if serializer.is_valid():
        serializer.save()
        print("Vendor profile updated.")
    else:
        print("Errors:", serializer.errors)


# Adding performance record for the given vendor #
def add_performance_record(vendor, data):
    print(f"Adding performance record for the vendor {vendor}.")
    data['vendor'] = vendor.vendor_code
    serializer = Vendor_Manager.serializers.HistoricalPerformancesSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        print("Performance Record Added.")
    else:
        print("Errors:", serializer.errors)


# Updating Vendor Performance #
def update_vendor_performance(vendor, po_status_completed, po_status_updated, po_acknowledged):
    # Initializing default values #
    on_time_delivery_rate = vendor.on_time_delivery_rate
    quality_rating_avg = vendor.quality_rating_avg
    fulfillment_rate = vendor.fulfillment_rate
    average_response_time = vendor.average_response_time
    # Calculating Values #
    if po_status_completed:
        on_time_delivery_rate = get_on_time_delivery_rate(vendor) or on_time_delivery_rate
        quality_rating_avg = get_quality_rating_avg(vendor) or quality_rating_avg
    if po_status_updated:
        fulfillment_rate = get_fulfillment_rate(vendor) or fulfillment_rate
    if po_acknowledged:
        average_response_time = get_average_response_time(vendor) or average_response_time
    # Updating the Vendor Performance Details #
    data = {
        'on_time_delivery_rate': on_time_delivery_rate,
        'quality_rating_avg': quality_rating_avg,
        'fulfillment_rate': fulfillment_rate,
        'average_response_time': average_response_time
    }
    update_vendor_profile(vendor, data)
    add_performance_record(vendor, data)
