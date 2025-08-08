from mongoengine import *

class AdminModel(Document):
    name = StringField(required=True)
    email = StringField(required=True, unique=True)
    password = StringField(required=True)
    
    # Campos opcionais para compatibilidade com dados antigos
    reset_pwd_token = StringField(default="")
    reset_pwd_token_sent_at = IntField(default=0)
    
    meta = {
        'strict': False  # Permite campos extras sem erro
    }