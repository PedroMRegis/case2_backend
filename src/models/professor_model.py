from mongoengine import Document, StringField

class ProfessorModel(Document):
    name = StringField(required=True)
    email = StringField(required=True, unique=True)
    password = StringField(required=True)
    idioma = StringField(required=True, choices=['ingles', 'espanhol'])
    trilha = StringField(required=True, choices=['financeiro', 'corporativo'])

