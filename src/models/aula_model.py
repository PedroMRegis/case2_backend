from datetime import datetime
from mongoengine import Document, DateTimeField, StringField, ReferenceField, CASCADE
from models.aluno_model import AlunoModel
from models.professor_model import ProfessorModel

class AulaModel(Document):
    date = DateTimeField(required=True, default=datetime.now)
    status = StringField(required=True, choices=['agendada', 'concluida', 'cancelada'])
    professor = ReferenceField(ProfessorModel, required=True, reverse_delete_rule=CASCADE)
    aluno = ReferenceField(AlunoModel, required=True, reverse_delete_rule=CASCADE)
