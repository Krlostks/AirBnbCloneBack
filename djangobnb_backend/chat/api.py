from django.http import JsonResponse

from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.decorators import api_view, authentication_classes, permission_classes
 
from .models import Conversation, ConversationMessage
from .serializers import ConversationListSerializer, ConversationDetailSerializer, ConversationMessageSerializer

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

@api_view(['GET'])
def conversations_detail(request, pk):
     conversation = request.user.conversations.get(pk=pk)
 
     conversation_serializer = ConversationDetailSerializer(conversation, many=False)
     messages_serializer = ConversationMessageSerializer(conversation.messages.all(), many=True)
     
     return JsonResponse({
         'conversation': conversation_serializer.data,
         'messages': messages_serializer.data,
     }, safe=False)

@api_view(['GET'])
def conversations_start(request, user_id):
     conversations = Conversation.objects.filter(users__in=[user_id]).filter(users__in=[request.user.id])
 
     if conversations.count() > 0:
         conversation = conversations.first()
         
         return JsonResponse({'success': True, 'conversation_id': conversation.id})
     else:
         user = User.objects.get(pk=user_id)
         conversation = Conversation.objects.create()
         conversation.users.add(request.user)
         conversation.users.add(user)
 
         return JsonResponse({'success': True, 'conversation_id': conversation.id})