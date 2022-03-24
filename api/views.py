import time
from django.utils.crypto import get_random_string
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .serializers import UserSerializer
from .models import User


class AuthorizationView(APIView):
    """Класс для авторизации и регистрации"""

    def post(self, request, *args, **kwargs):
        """Отправляет на сервер phone и invite_code(необязательно), в ответ получает authorization_code"""

        if {'phone'}.issubset(request.data):
            try:
                user = User.objects.get(phone=request.data['phone'])
            except ObjectDoesNotExist:
                user_serializer = UserSerializer(data=request.data)
                if user_serializer.is_valid():
                    if {'invite_code'}.issubset(request.data):
                        query_set = User.objects.filter(self_code=request.data['invite_code'])
                        if len(query_set) != 0:
                            user = user_serializer.save()
                            user.set_password(None)
                            user.authorization_code = get_random_string(4, allowed_chars='0123456789')
                            user.self_code = get_random_string(6,
                                                               allowed_chars='0123456789qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM')
                            user.invite_code = request.data['invite_code']
                            user.save()
                            return Response({'Status': True, 'authorization_code': user.authorization_code}, status=201)
                        else:
                            return Response({'Status': False, 'Errors': 'Неверный invite code'})
                    user = user_serializer.save()
                    user.set_password(None)
                    user.authorization_code = get_random_string(4, allowed_chars='0123456789')
                    user.self_code = get_random_string(6, allowed_chars='0123456789qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM')
                    user.save()
                    return Response({'Status': True, 'authorization_code': user.authorization_code}, status=201)
                else:
                    return Response({'Status': False, 'Errors': user_serializer.errors}, status=400)
            else:
                time.sleep(2)
                user.authorization_code = get_random_string(4, allowed_chars='0123456789')
                user.save()
                return Response({'phone': user.phone, 'authorization_code': user.authorization_code})
        return Response({'Status': False, 'Errors': 'Не указаны все необходимые аргументы'}, status=400)



class AuthorizationWithCodeView(APIView):
    """Авторизация с 4-х значным authorization_code"""

    def post(self, request, *args, **kwargs):
        if {'phone', 'authorization_code'}.issubset(request.data):
            try:
                user = User.objects.get(phone=request.data['phone'])
            except ObjectDoesNotExist:
                return Response({'Status': False, 'Errors': 'Пользователь не найден'}, status=404)
            else:
                if user.authorization_code == request.data['authorization_code'] and user.authorization_code != 'xxxx':
                    user.authorization_code = 'xxxx'
                    user.is_active = True
                    user.save()
                    token, created = Token.objects.get_or_create(user=user)
                    return Response({'Status': True, 'Token': token.key}, status=200)
                else:
                    return Response({'Status': False, 'Errors': 'Не верный код авторизации'}, status=400)
        return Response({'Status': False, 'Errors': 'Не указаны все необходимые аргументы'}, status=400)


class ProfileView(APIView):

    def get(self, request, *args, **kwargs):
        """Получение профиля пользователя"""
        if not request.user.is_authenticated:
            return Response({'Status': False, 'Errors': 'Пользователь не авторизован'}, status=401)
        user_profile = User.objects.get(id=request.user.id)
        serializer = UserSerializer(user_profile)
        invite_users = User.objects.filter(invite_code=user_profile.self_code)
        phone_numbers = [user.phone for user in invite_users]
        info = serializer.data
        info['invite_users'] = phone_numbers
        info.pop('authorization_code')
        return Response({'Status': True, 'Info': info}, status=200)

    def put(self, request, *args, **kwargs):
        """Добавление invite_code, если он не был указан при регистрации"""
        if not request.user.is_authenticated:
            return Response({'Status': False, 'Errors': 'Пользователь не авторизован'}, status=401)
        invite_code = request.data.get('invite_code')
        if invite_code:
            user = User.objects.get(id=request.user.id)
            if user.invite_code is None:
                query_set = User.objects.filter(self_code=request.data['invite_code']).exclude(id=request.user.id)
                if len(query_set) != 0:
                    user.invite_code = request.data['invite_code']
                    user.save()
                    return Response({'Status': True}, status=201)
                else:
                    return Response({'Status': False, 'Errors': 'invite_code не найден'}, status=404)
            else:
                return Response({'Status': False, 'Errors': 'вы уже вводили invite_code'}, status=400)
        return Response({'Status': False, 'Errors': 'Не указаны все необходимые аргументы'}, status=400)






