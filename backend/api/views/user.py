from .api import res, api, P
from django.db.models import F, Count
from ..models import User
from ..serializer import SimpleSerializer, AccountSerializer
from argon2 import PasswordHasher
import jwt, os

SECRET = os.getenv('DJANGO_SECRET_KEY')

@api(
    name="회원가입",
    method='POST',
    params=[
        P('username', t='string', desc='아이디'),
        P('nickname', t='string', desc='닉네임'),
        P('password', t='string', desc='비밀번호'),
    ],
    response=AccountSerializer,
    errors={
        1: '알 수 없는 에러',
        2: '이미 존재하는 아이디',
    }
)
def register(req, username:str, nickname:str, password:str):
    if User.objects.filter(username=username).count() > 0:
        return res(code=2, msg='이미 존재하는 아이디')
    user = User(
        username=username,
        nickname=nickname,
        password=PasswordHasher().hash(password),
        booka=True
    )
    user.save()
    return res(AccountSerializer({
            'token': jwt.encode({'username': user.username, 'id': user.id}, SECRET, algorithm='HS256').decode('utf-8'),
            'is_first': True,
            'nickname': user.nickname,
        }).data)

@api(
    name="로그인",
    method='POST',
    params=[
        P('username', t='string', desc='아이디'),
        P('password', t='string', desc='비밀번호'),
    ],
    response=AccountSerializer,
    errors={
        1: '알 수 없는 에러',
        2: '존재하지 않는 아이디',
        3: '비밀번호 일치하지 않음'
    }
)
def login(req, username:str, password:str):
    if User.objects.filter(username=username).count() == 0:
        return res(code=2, msg='존재하지 않는 아이디')
    user = User.objects.get(username=username)
    try:
        PasswordHasher().verify(user.password, password)
    except:
        return res(code=3, msg='비밀번호 일치하지 않음')
    try:
        return res(AccountSerializer({
            'token': jwt.encode({'username': user.username, 'id': user.id}, SECRET, algorithm='HS256').decode('utf-8'),
            'is_first': user.reviews.count() == 0,
            'nickname': user.nickname,
        }).data)
    except Exception as e:
        print(e)
        return res(code=1)
