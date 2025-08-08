from bson import ObjectId
from entities.aula import Aula
from models.aula_model import AulaModel
from models.professor_model import ProfessorModel
from models.aluno_model import AlunoModel

class AulaRepository:

    @staticmethod
    def _to_entity(model: AulaModel) -> Aula:
        return Aula(
            id=str(model.id),
            date=model.date,
            status=model.status,
            professor_id=str(model.professor.id),
            aluno_id=str(model.aluno.id)
        )

    def save(self, aula: Aula) -> Aula:
        data = aula.model_dump()
        # 1) Validar existência de professor e aluno
        prof = ProfessorModel.objects.with_id(ObjectId(data["professor_id"]))
        if not prof:
            raise ValueError(f"Professor com ID '{data['professor_id']}' não encontrado")

        aluno = AlunoModel.objects.with_id(ObjectId(data["aluno_id"]))
        if not aluno:
            raise ValueError(f"Aluno com ID '{data['aluno_id']}' não encontrado")

        # 2) Verificar conflito de data/hora (por professor)
        conflict = AulaModel.objects(
            date=data["date"],
            professor=prof
        ).first()
        if conflict:
            raise ValueError("Já existe uma aula agendada para este professor nessa data e horário")

        # 3) Criar e salvar
        model = AulaModel(
            date=data["date"],
            status=data["status"],
            professor=prof,
            aluno=aluno
        )
        model.save()

        # 4) Retornar a entidade populada
        return self._to_entity(model)

    def find_all(self) -> list[Aula]:
        return [self._to_entity(m) for m in AulaModel.objects()]

    def find_by_id(self, aula_id: str) -> Aula:
        try:
            oid = ObjectId(aula_id)
        except Exception:
            raise ValueError("Aula ID inválido")
        model = AulaModel.objects.with_id(oid)
        if not model:
            raise ValueError("Aula não encontrada")
        return self._to_entity(model)
    
    def find_by_professor_id(self, professor_id: str) -> list[Aula]:
        try:
            oid = ObjectId(professor_id)
        except Exception:
            raise ValueError("Professor ID inválido")
        professor = ProfessorModel.objects.with_id(oid)
        if not professor:
            raise ValueError("Professor não encontrado")
        models = AulaModel.objects(professor=professor)
        return [self._to_entity(m) for m in models]

    def update(self, aula_id: str, updated_data: dict) -> Aula:
        model = self.find_by_id(aula_id)  # já retorna Aula entity, mas we need the model; adjust:
        # Fetch the raw model again
        raw = AulaModel.objects.with_id(ObjectId(aula_id))
        for key, value in updated_data.items():
            if hasattr(raw, key):
                setattr(raw, key, value)
        raw.save()
        return self._to_entity(raw)

    def delete(self, aula_id: str) -> None:
        model = AulaModel.objects.with_id(ObjectId(aula_id))
        if not model:
            raise ValueError("Aula não encontrada")
        model.delete()
