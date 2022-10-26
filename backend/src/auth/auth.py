import json
from flask import request
from functools import wraps
from jose import jwt
from urllib.request import urlopen


AUTH0_DOMAIN = 'dev-5euegq86qhglqrz7.us.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'http://localhost:5000'


# AuthError Exception
class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


def get_token_from_authorization_header():
    authSplit = (request.headers.get('Authorization', None)).split()
    if not (request.headers.get('Authorization', None)):
        raise AuthError({
            'code': 'authorization header is missing',
            'description': 'Authorization header is missing for verifivation.'
        }, 401)

    if len(authSplit) == 1:
        raise AuthError({
            'code': 'authorization header is invalid',
            'description': 'Authorization token is not found.'
        }, 401)

    elif len(authSplit) > 2:
        raise AuthError({
            'code': 'authorization header is invalid',
            'description': 'Authorization header must be bearer token base on the format.'
        }, 401)

    elif authSplit[0].lower() != 'bearer':
        raise AuthError({
            'code': 'authorization header is invalid',
            'description': 'Authorization header must start with "Bearer" base on the format.'
        }, 401)

    print(authSplit[1])
    return authSplit[1]


def verify_decode_jwt(token):
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())
    unverified_header = jwt.get_unverified_header(token)
    rsa_key = {}
    if 'kid' not in unverified_header:
        raise AuthError({
            'code': 'authorization header is invalid',
            'description': 'Authorization malformed.'
        }, 401)

    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }
    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/'
            )

            return payload

        except jwt.ExpiredSignatureError:
            raise AuthError({
                'code': 'token is expired',
                'description': 'Token is expired.'
            }, 401)

        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'claims is not valid',
                'description': 'Incorrect claims.'
            }, 401)
        except Exception:
            raise AuthError({
                'code': 'authorization header is invalid',
                'description': 'Unable to parse authentication token.'
            }, 400)
    raise AuthError({
        'code': 'authorization header is invalid',
        'description': 'Unable to find the appropriate key.'
    }, 400)


def check_auth_access(access, payload):
    if 'permissions' not in payload:
        raise AuthError({
            'code': 'claims is not valid',
            'description': 'Access is not included in JWT.'
        }, 400)

    if access not in payload['permissions']:
        raise AuthError({
            'code': 'unauthorized',
            'description': 'Access not found.'
        }, 403)
    return True


def requires_auth(access=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            payload = verify_decode_jwt(get_token_from_authorization_header())
            check_auth_access(access, payload)
            return f(payload, *args, **kwargs)

        return wrapper
    return requires_auth_decorator
