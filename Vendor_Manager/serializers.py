# Importing Dependencies #
from rest_framework.serializers import ModelSerializer
from Vendor_Manager.models import VendorProfileModel, PurchaseOrdersModel, HistoricalPerformancesModel



# Vendor Profile Serializer #
class VendorProfileSerializer(ModelSerializer):
    class Meta:
        model = VendorProfileModel
        fields = '__all__'
    
    # Overriding the update function to avoid updating the primary key # 
    def update(self, instance, validated_data):
        validated_data.pop('vendor_code', None)
        return super().update(instance, validated_data)



# Purchase Order Serializer #
class PurchaseOrdersSerializer(ModelSerializer):
    class Meta:
        model = PurchaseOrdersModel
        fields = '__all__'
    
    # Overriding the update function to avoid updating the primary key # 
    def update(self, instance, validated_data):
        validated_data.pop('po_number', None)
        return super().update(instance, validated_data)