import base64

def encode_password(password: str)-> str:
    return base64.b64encode(password.encode()).decode()

def decode_token(token: str)-> str:
    return base64.b64decode(token).decode()