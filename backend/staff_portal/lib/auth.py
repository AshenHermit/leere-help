from django.http import HttpResponse, JsonResponse, HttpRequest
import jwt
from ..models import *

SECRET_KEYWORD = "dreammomentsparklesinmyeyespastelpinkfoxscintillatingfluffypawsreachflowerymomentreactlotusmagicsingingstarrydaytimearchperfectinsteadninesecondseversoftenough"

def get_authorized_user(request: HttpRequest):
    """для полученя текущего пользователя для текущего запроса"""
    # по дефолту пусть user будет None
    user = None
    try:
        # получаем куки "auth", которая должна хранить токен
        auth_token = request.COOKIES.get("auth")
        # расшифровываем json токен с помощью jwt и получаем dict который зашифровали при авторизации
        token_data = jwt.decode(auth_token, SECRET_KEYWORD, algorithms=["HS256"])

        # получаем запись пользователя в бд, по логину из данных токена
        user = User.objects.get(login=token_data["login"])
        # кидаем ошибку если пользователь не найден
        if not user: raise Exception("no such user")

        # получаем из данных токена пароль
        password = token_data["password"]
        # проверяем соответствие пароля в токене к паролю из истинного пароля пользователя из бд 
        if user.password != password: raise Exception("wrong password")

    except:
        raise Exception("not authorized")
    
    # если все норм, возвращаем объект пользователя
    return user

def get_authorized_user_by_credentials(login, password):
    """для получения пользователя по логину + проверка пароля.  
    по сути работает как get_authorized_user, только эта функция читает не токен из куки, 
    а реквизиты для входа в аргументы функции"""

    # получаем пользователя по логину
    user = User.objects.get(login=login)
    # если пользователь не найден кидаем ошибку
    if not user: raise Exception("no such user")
    # проверяем пароль
    if user.password != password: raise Exception("wrong password")
    # если все хорошо возвращаем пользователя
    return user

def generate_token_for_user(user:User):
    """зашифровывает реквизиты для входа в аккаунт (логин пароль), получая на выходе токен"""
    token = jwt.encode({"login": user.login, "password": user.password}, SECRET_KEYWORD, algorithm="HS256")
    return token
