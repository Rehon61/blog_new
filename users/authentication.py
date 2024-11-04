from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model
class EmailAuthBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        # Получаем модель пользователя Django
        user_model = get_user_model()
        try:
            # Ищем пользователя по email (в поле username в форме авторизации можно передать email)
            user = user_model.objects.get(email=username)
            # Проверяем правильность пароля
            if user.check_password(password):
                return user
        except user_model.DoesNotExist:
            return None
        except user_model.MultipleObjectsReturned:
            return None
    def get_user(self, user_id):
        """
        Метод для получения пользователя по его ID
        Используется Django для поддержания сессии пользователя
        """
        # Получаем модель пользователя Django
        user_model = get_user_model()
        try:
            # Ищем пользователя по первичному ключу
            return user_model.objects.get(pk=user_id)
        except user_model.DoesNotExist:
            return None
        except user_model.MultipleObjectsReturned:
            return None