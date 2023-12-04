# Importing Dependencies #
from rest_framework.serializers import ModelSerializer
from Vendor_Manager.models import VendorProfileModel, PurchaseOrdersModel, HistoricalPerformancesModel



# Vendor Profile Serializer #
class VendorProfileSerializer(ModelSerializer):
    class Meta:
        model = VendorProfileModel
        fields = '__all__'



# Purchase Order Serializer #
class PurchaseOrdersSerializer(ModelSerializer):
    class Meta:
        model = PurchaseOrdersModel
        fields = '__all__'