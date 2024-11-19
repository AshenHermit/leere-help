from django.http import HttpResponse, JsonResponse, HttpRequest
import jwt
from ..models import *

SECRET_KEYWORD = "dreammomentsparklesinmyeyespastelpinkfoxscintillatingfluffypawsreachflowerymomentreactlotusmagicsingingstarrydaytimearchperfectinsteadninesecondseversoftenough"

def get_authorized_user(request: HttpRequest):
    user = None
    try:
        auth_token = request.COOKIES.get("auth")
        token_data = jwt.decode(auth_token, SECRET_KEYWORD, algorithms=["HS256"])

        user = User.objects.get(login=token_data["login"])
        if not user: raise Exception("no such user")

        password = token_data["password"]
        if user.password != password: raise Exception("wrong password")

    except:
        raise Exception("not authorized")
    
    return user

def get_authorized_user_by_credentials(login, password):
    user = User.objects.get(login=login)
    if not user: raise Exception("no such user")
    if user.password != password: raise Exception("wrong password")

    return user

def generate_token_for_user(user:User):
    token = jwt.encode({"login": user.login, "password": user.password}, SECRET_KEYWORD, algorithm="HS256")
    return token
