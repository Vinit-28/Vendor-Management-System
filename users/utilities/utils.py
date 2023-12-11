# Importing Dependencies #
import jwt
from decouple import config
from datetime import datetime, timedelta


# Generating JWT Token #
def generate_token(user_name):
    payload = {
        'user_name': str(user_name),
        'exp': int((datetime.now() + timedelta(hours=1)).timestamp())
    }
    secret_key = config('JWT_SECRET_KEY')
    token = jwt.encode(payload, secret_key, algorithm='HS256')
    return token
