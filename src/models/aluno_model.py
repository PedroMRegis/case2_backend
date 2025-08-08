from mongoengine import Document, StringField

class AlunoModel(Document):
    name = StringField(required=True)
    email = StringField(required=True, unique=True)
    password = StringField(required=True)
    plano = StringField(required=True, choices=['individual', 'grupo'])
