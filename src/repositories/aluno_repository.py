import bcrypt
from bson import ObjectId
from entities.aluno import Aluno
from models.aluno_model import AlunoModel

class AlunoRepository:
    @staticmethod
    def _to_entity(model: AlunoModel) -> Aluno:
        return Aluno(
            id=str(model.id),
            name=model.name,
            email=model.email,
            password=model.password,
            plano=model.plano
        )

    def save(self, aluno: Aluno) -> Aluno:
        # Verifica se já existe um aluno com este email
        if AlunoModel.objects(email=aluno.email).first():
            raise ValueError(f"Já existe um aluno cadastrado com o email '{aluno.email}'")

        model = AlunoModel(
            name=aluno.name,
            email=aluno.email,
            password=bcrypt.hashpw(aluno.password.encode(), bcrypt.gensalt()).decode(),
            plano=aluno.plano
        )
        try:
            model.save()
            # Busca o modelo salvo para garantir que temos o ID
            saved_model = AlunoModel.objects(id=model.id).first()
            if saved_model is None:
                raise ValueError("Erro ao recuperar aluno após salvar")
            return self._to_entity(saved_model)
        except Exception as e:
            raise ValueError(f"Erro ao salvar aluno: {str(e)}")

    def find_all(self) -> list[Aluno]:

        return [self._to_entity(m) for m in AlunoModel.objects()]

    def find_by_name(self, name: str) -> Aluno:
        model = AlunoModel.objects(name=name).first()
        if not model:
            raise ValueError(f"Aluno com nome '{name}' não encontrado")
        return self._to_entity(model)

    def find_by_email(self, email: str) -> Aluno:
        model = AlunoModel.objects(email=email).first()
        if not model:
            raise ValueError(f"Aluno com email '{email}' não encontrado")
        return self._to_entity(model)
    
    def find_by_id(self, aluno_id: str) -> Aluno:
        try:
            oid = ObjectId(aluno_id)
        except Exception:
            raise ValueError("Aluno ID inválido")
        model = AlunoModel.objects.with_id(oid)
        if not model:
            raise ValueError("Aluno não encontrado")
        return self._to_entity(model)

    def update(self, name: str, updated_data: dict) -> Aluno:
        model = AlunoModel.objects(name=name).first()
        if not model:
            raise ValueError(f"Aluno com nome '{name}' não encontrado")

        for key, value in updated_data.items():
            if key == "password":
                value = bcrypt.hashpw(value.encode(), bcrypt.gensalt()).decode()
            if hasattr(model, key):
                setattr(model, key, value)
        model.save()
        return self._to_entity(model)

    def update_by_id(self, aluno_id: str, updated_data: dict) -> Aluno:
        try:
            oid = ObjectId(aluno_id)
        except Exception:
            raise ValueError("Aluno ID inválido")
            
        model = AlunoModel.objects(id=oid).first()
        if not model:
            raise ValueError("Aluno não encontrado")

        for key, value in updated_data.items():
            if key == "password":
                value = bcrypt.hashpw(value.encode(), bcrypt.gensalt()).decode()
            if hasattr(model, key):
                setattr(model, key, value)
        model.save()
        return self._to_entity(model)

    def delete(self, name: str) -> None:
        deleted_count = AlunoModel.objects(name=name).delete()
        if deleted_count == 0:
            raise ValueError(f"Aluno com nome '{name}' não encontrado")

    def delete_by_id(self, aluno_id: str) -> None:
        try:
            oid = ObjectId(aluno_id)
        except Exception:
            raise ValueError("Aluno ID inválido")
        
        deleted_count = AlunoModel.objects(id=oid).delete()
        if deleted_count == 0:
            raise ValueError("Aluno não encontrado")
