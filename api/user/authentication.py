import jwt, datetime, uuid
from rest_framework import exceptions


def create_access_token(id):
    str_id = str(id)  
    return jwt.encode({
        'user_id': str_id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=3000),
        'iat': datetime.datetime.utcnow(),
    }, 'access_secret', algorithm='HS256')

def create_refresh_token(id):
    str_id = str(id)  
    return jwt.encode({
        'user_id': str_id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7),
        'iat': datetime.datetime.utcnow(),
    }, 'refresh_secret', algorithm='HS256')

def decode_access_token(token):
    try:
        payload = jwt.decode(token, 'access_secret', algorithms=['HS256'])
        return payload['user_id']  
    except jwt.ExpiredSignatureError:
        return exceptions.AuthenticationFailed('Token expired, login again')
    except jwt.InvalidTokenError:
        return exceptions.AuthenticationFailed('Invalid token')

def decode_refresh_token(token):
    try:
        payload = jwt.decode(token, 'refresh_secret', algorithms=['HS256'])
        return uuid.UUID(payload['user_id'])  
    except jwt.ExpiredSignatureError:
        raise exceptions.AuthenticationFailed('Token expired, login again')
    except jwt.InvalidTokenError:
        raise exceptions.AuthenticationFailed('Invalid token')
    

# def create_access_token(id):
#     return jwt.encode({
#         'user_id' : id,
#         'exp' : datetime.datetime.utcnow() + datetime.timedelta(seconds = 30),
#         'iat' : datetime.datetime.utcnow(),
#     }, 'access_secret', algorithm = 'HS256' )

# def decode_access_token(token):
#     try:
#         payload = jwt.decode(token, 'access_secret', algorithms = 'HS256')

#         return payload['user_id']
#     except:
#         raise exceptions.AuthenticationFailed('Unauthenticated')

# def create_refresh_token(id):
#     return jwt.encode({
#         'user_id' : id,
#         'exp' : datetime.datetime.utcnow() + datetime.timedelta(days=7),
#         'iat' : datetime.datetime.utcnow(),
#     }, 'refresh_secret', algorithm = 'HS256' )

# def decode_refresh_token(token):
#     try:
#         payload = jwt.decode(token, 'refresh_secret', algorithms = 'HS256')

#         return payload['user_id']
#     except:
#         raise exceptions.AuthenticationFailed('Unauthenticated')