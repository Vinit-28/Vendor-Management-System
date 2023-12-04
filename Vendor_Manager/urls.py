# Importing Dependencies #
from django.urls import path
from Vendor_Manager.views import VendorProfileView, PurchaseOrdersView

# Defining URLs #
urlpatterns = [
    path('vendors/', VendorProfileView.as_view(), name='VendorProfile'),
    path('vendors/<vendor_id>/', VendorProfileView.as_view(), name='VendorProfile'),
    path('purchase_orders/', PurchaseOrdersView.as_view(), name='PurchaseOrders'),
    path('purchase_orders/<po_id>/', PurchaseOrdersView.as_view(), name='PurchaseOrders'),
]