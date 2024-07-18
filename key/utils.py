import secrets
import uuid

def gen_key():
    key = f'{secrets.token_hex(16)}-{str(uuid.uuid4())}'
    return key
