from django.http import JsonResponse

from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.decorators import api_view, authentication_classes, permission_classes
 
from .models import Conversation
from .serializers import ConversationListSerializer
from useraccount.models import User
 
 
@api_view(['GET'])
@authentication_classes([])  
@permission_classes([])  
def conversations_list(request):    
     try:
         token = request.META['HTTP_AUTHORIZATION'].split('Bearer ')[1]
         token = AccessToken(token)
         user_id = token.payload['user_id']
         user = User.objects.get(pk=user_id)         
     except Exception as e:
         user = None

     conversation = Conversation.objects.all()
     serializer = ConversationListSerializer(conversation, many=True)
     return JsonResponse({'data': serializer.data})