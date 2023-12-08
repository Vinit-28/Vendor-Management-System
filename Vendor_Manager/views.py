# Importing Dependencies #
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from Vendor_Manager.serializers import VendorProfileSerializer, PurchaseOrdersSerializer
from Vendor_Manager.models import VendorProfileModel, PurchaseOrdersModel, HistoricalPerformancesModel


# Vendor Profile APIs #
class VendorProfileView(APIView):

    # Get to get the Vendor Profile(s) #
    def get(self, request, vendor_id=None):
        response = dict()
        response_status = status.HTTP_200_OK
        if vendor_id is None:
            vendor_profiles = VendorProfileModel.objects.all()
            serializer = VendorProfileSerializer(vendor_profiles, many=True)
            response['status'] = 'Success'
            response['Vendor Profiles'] = serializer.data
        else:
            try:
                vendor_profile = VendorProfileModel.objects.get(vendor_code=vendor_id)
                serializer = VendorProfileSerializer(vendor_profile)
                response['status'] = 'Success'
                response['Vendor Profile'] = serializer.data
            except ObjectDoesNotExist as err:
                response_status = status.HTTP_400_BAD_REQUEST
                response['status'] = 'Failed'
                response['Errors'] = {
                    'message': [f'No Vendor with Vendor Id "{vendor_id}".']
                }
        return Response(response, status=response_status)
    

    # Post to create the Vendor Profile #
    def post(self, request):
        response = dict()
        response_status = status.HTTP_200_OK
        try:
            serializer = VendorProfileSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                response['status'] = 'Success'
                response['message'] = 'Vendor Profile Saved.'
            else:
                response['status'] = 'Failed'
                response['Errors'] = serializer.errors
        except Exception as err:
            response_status = status.HTTP_500_INTERNAL_SERVER_ERROR
            response['status'] = 'Failed'
            response['Errors'] = {
                'message': [f"{err}."]
            }
        return Response(response, status=response_status)


    # Put to update the Vendor Profile #
    def put(self, request, vendor_id):
        response = dict()
        response_status = status.HTTP_200_OK
        try:
            vendor_profile = VendorProfileModel.objects.get(vendor_code=vendor_id)
            serializer = VendorProfileSerializer(vendor_profile, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                response['status'] = 'Success'
                response['message'] = 'Vendor Profile Updated Successfully.'
                response['Vendor Profile'] = serializer.data
            else:
                response['status'] = 'Failed'
                response['Errors'] = serializer.errors
        except ObjectDoesNotExist as err:
            response_status = status.HTTP_400_BAD_REQUEST
            response['status'] = 'Failed'
            response['Errors'] = {
                'message': [f'No Vendor with Vendor Id "{vendor_id}".']
            }
        except Exception as err:
            response_status = status.HTTP_500_INTERNAL_SERVER_ERROR
            response['status'] = 'Failed'
            response['Errors'] = {
                'message': [f"{err}."]
            }
        return Response(response, status=response_status)


    # Delete to delete the Vendor Profile #
    def delete(self, request, vendor_id):
        response = dict()
        response_status = status.HTTP_200_OK
        try:
            vendor_profile = VendorProfileModel.objects.get(vendor_code=vendor_id)
            serializer = VendorProfileSerializer(vendor_profile)
            vendor_profile_json = serializer.data
            vendor_profile.delete()
            response['status'] = 'Success'
            response['message'] = 'Vendor Profile Deleted Successfully.'
            response['Vendor Profile'] = vendor_profile_json
        except ObjectDoesNotExist as err:
            response_status = status.HTTP_400_BAD_REQUEST
            response['status'] = 'Failed'
            response['Errors'] = {
                'message': [f'No Vendor with Vendor Id "{vendor_id}".']
            }
        except Exception as err:
            response_status = status.HTTP_500_INTERNAL_SERVER_ERROR
            response['status'] = 'Failed'
            response['Errors'] = {
                'message': [f"{err}."]
            }
        return Response(response, status=response_status)




# Purchase Orders APIs #
class PurchaseOrdersView(APIView):

    # Get to get the Purchase Order(s) #
    def get(self, request, po_id=None):
        response = dict()
        response_status = status.HTTP_200_OK
        if po_id is None:
            purchase_orders = PurchaseOrdersModel.objects.all()
            serializer = PurchaseOrdersSerializer(purchase_orders, many=True)
            response['status'] = 'Success'
            response['Purchase Orders'] = serializer.data
        else:
            try:
                purchase_order = PurchaseOrdersModel.objects.get(po_number=po_id)
                serializer = PurchaseOrdersSerializer(purchase_order)
                response['status'] = 'Success'
                response['Purchase Order'] = serializer.data
            except ObjectDoesNotExist as err:
                response_status = status.HTTP_400_BAD_REQUEST
                response['status'] = 'Failed'
                response['Errors'] = {
                    'message': [f'No Purchase Order with Purchar Order Id "{po_id}".']
                }
        return Response(response, status=response_status)
    

    # Post to create the Purchase Order #
    def post(self, request):
        response = dict()
        response_status = status.HTTP_200_OK
        try:
            vendor_id = request.data.get('vendor')
            vendor = VendorProfileModel.objects.get(pk=vendor_id) # Will raise the exception if vendor doesn't exist #
            serializer = PurchaseOrdersSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                response['status'] = 'Success'
                response['message'] = 'Purchase Order Saved.'
            else:
                response['status'] = 'Failed'
                response['Errors'] = serializer.errors
        except ObjectDoesNotExist as err:
            response_status = status.HTTP_400_BAD_REQUEST
            response['status'] = 'Failed'
            response['Errors'] = {
                'message': [f"Please provide a valid vendor id."]
            }
        except Exception as err:
            response_status = status.HTTP_500_INTERNAL_SERVER_ERROR
            response['status'] = 'Failed'
            response['Errors'] = {
                'message': [f"{err}."]
            }
        return Response(response, status=response_status)


    # Put to update the Purchase Order #
    def put(self, request, po_id):
        response = dict()
        response_status = status.HTTP_200_OK
        try:
            purchase_order = PurchaseOrdersModel.objects.get(pk=po_id)
            vendor_id = request.data.get('vendor')
            vendor = VendorProfileModel.objects.get(pk=vendor_id) if vendor_id else purchase_order.vendor # VAlidating the whether the new/updated vendor exists or not #
            serializer = PurchaseOrdersSerializer(purchase_order, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                response['status'] = 'Success'
                response['message'] = 'Purchase Order Updated Successfully.'
                response['Purchase Order'] = serializer.data
            else:
                response['status'] = 'Failed'
                response['Errors'] = serializer.errors
        except ObjectDoesNotExist as err:
            response_status = status.HTTP_400_BAD_REQUEST
            response['status'] = 'Failed'
            response['Errors'] = {
                'message': [f'Invalid purchase order id or vendor id.']
            }
        except Exception as err:
            response_status = status.HTTP_500_INTERNAL_SERVER_ERROR
            response['status'] = 'Failed'
            response['Errors'] = {
                'message': [f"{err}."]
            }
        return Response(response, status=response_status)


    # Delete to delete the Purchase Order #
    def delete(self, request, po_id):
        response = dict()
        response_status = status.HTTP_200_OK
        try:
            purchase_order = PurchaseOrdersModel.objects.get(pk=po_id)
            serializer = PurchaseOrdersSerializer(purchase_order)
            purchase_order_json = serializer.data
            purchase_order.delete()
            response['status'] = 'Success'
            response['message'] = 'Purchase Order Deleted Successfully.'
            response['Purchase Order'] = purchase_order_json
        except ObjectDoesNotExist as err:
            response_status = status.HTTP_400_BAD_REQUEST
            response['status'] = 'Failed'
            response['Errors'] = {
                'message': [f'No purchase order with id {po_id}.']
            }
        except Exception as err:
            response_status = status.HTTP_500_INTERNAL_SERVER_ERROR
            response['status'] = 'Failed'
            response['Errors'] = {
                'message': [f"{err}."]
            }
        return Response(response, status=response_status)