from django.shortcuts import render
from .serializers import DeviceSerializer
from rest_framework import generics, views
from rest_framework.permissions import IsAuthenticated
from .models import Device
from drf_spectacular.utils import extend_schema

# Create your views here.

class DeviceView(generics.CreateAPIView):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    
    
    def get_queryset(self):
        return Device.objects.filter(token=self.request.data.get('token'))

class DeviceDestroyView(generics.RetrieveDestroyAPIView):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
        

    def get_queryset(self):
        return Device.objects.filter(token=self.request.data.get('token'))

class DeviceDeactivateView(views.APIView):

    @extend_schema(
        request={
            'application/json': {
                'type': 'object',
                'properties': {
                    'token': {'type': 'string'},
                },
                'required': ['token']
            }
        },
        responses={200: DeviceSerializer}
    )
    def post(self, request):
        token = request.data.get('token')
        device = Device.objects.filter(token=token).first()
        if device:
            device.is_active = False
            device.save()
        return Response({'message': 'Device deactivated successfully'})
        