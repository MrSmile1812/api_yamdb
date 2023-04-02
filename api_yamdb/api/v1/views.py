import uuid
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from rest_framework.permissions import AllowAny

#from django.contrib.auth.tokens import default_token_generator

#from django.shortcuts import get_object_or_404

#from ..models import User_reg
from .serializers import CreateUserSerializer
from django.contrib.auth import get_user_model
User = get_user_model()


@api_view(['POST'])
@permission_classes([AllowAny])
def create_user(request):
    '''Создание нового пользователя'''
    serializer = CreateUserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data.get('username')
    email = serializer.validated_data.get('email')
    conformition_code = uuid.uuid4()
    if serializer.is_valid():
        user, created = User.objects.get_or_create(
            username=username,
            email=email,
            conformition_code=conformition_code
        )
        #plain_message = conformition_code
        send_mail(
            'Ваш код подтверждения',
            str(conformition_code),
            'from@example.com',  # Это поле "От кого"
            [email],  # Это поле "Кому" (можно указать список адресов)
            fail_silently=False, # Сообщать об ошибках («молчать ли об ошибках?»)
        )
        return Response(request.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

#token = default_token_generator.make_token(user)