from django.http import JsonResponse
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from .models import Property
from .serializers import PropertiesDetailSerializer
from .forms import PropertyForm
 
@api_view(['GET'])
@authentication_classes([])  
@permission_classes([])  
def properties_detail(request, property_id):
     try:
         property = Property.objects.get(id=property_id)  
     except Property.DoesNotExist:
         return JsonResponse({'error': 'Property not found'}, status=404)
 
     serializer = PropertiesDetailSerializer(property) 
 
     return JsonResponse({
         'data': serializer.data
     })

@api_view(['GET'])
@authentication_classes([]) 
@permission_classes([])  
def properties_list(request):
    properties = Property.objects.all()  
    serializer = PropertiesDetailSerializer(properties, many=True)  
    return JsonResponse({'data': serializer.data})

@api_view(['POST', 'FILES'])
def create_property(request):
     form = PropertyForm(request.POST, request.FILES)
 
     if form.is_valid():
         property = form.save(commit=False)
         property.landlord = request.user
         property.save()
 
         return JsonResponse({'success': True})
     else:
         print('error', form.errors, form.non_field_errors)
         return JsonResponse({'errors': form.errors.as_json()}, status=400)