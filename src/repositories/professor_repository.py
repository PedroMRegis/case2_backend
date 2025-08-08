import bcrypt
from bson import ObjectId
from entities.professor import Professor
from models.professor_model import ProfessorModel

class ProfessorRepository:
    @staticmethod
    def _to_entity(model: ProfessorModel) -> Professor:
        return Professor(
            id=str(model.id),
            name=model.name,
            email=model.email,
            password=model.password,
            idioma=model.idioma,
            trilha=model.trilha
        )

    def save(self, professor: Professor) -> Professor:
        model = ProfessorModel(
            name=professor.name,
            email=professor.email,
            password=bcrypt.hashpw(professor.password.encode(), bcrypt.gensalt()).decode(),
            idioma=professor.idioma,
            trilha=professor.trilha
        )
        try:
            model.save()
            # Busca o modelo salvo para garantir que temos o ID
            saved_model = ProfessorModel.objects(id=model.id).first()
            if saved_model is None:
                raise ValueError("Erro ao recuperar professor após salvar")
            return self._to_entity(saved_model)
        except Exception as e:
            raise ValueError(f"Erro ao salvar professor: {str(e)}")

    def find_all(self) -> list[Professor]:
        return [self._to_entity(m) for m in ProfessorModel.objects()]

    def find_by_name(self, name: str) -> Professor:
        m = ProfessorModel.objects(name=name).first()
        if not m:
            raise ValueError(f"Professor com name='{name}' não encontrado")
        return self._to_entity(m)
    
    def find_by_email(self, email: str) -> Professor:
        m = ProfessorModel.objects(email=email).first()
        if not m:
            raise ValueError(f"Professor com email='{email}' não encontrado")
        return self._to_entity(m)
    
    def find_by_id(self, professor_id: str) -> Professor:
        try:
            oid = ObjectId(professor_id)
        except Exception:
            raise ValueError("Professor ID inválido")
        m = ProfessorModel.objects.with_id(oid)
        if not m:
            raise ValueError("Professor não encontrado")
        return self._to_entity(m)

    def update_by_name(self, name: str, updated_data: dict) -> Professor:
        m = ProfessorModel.objects(name=name).first()
        if not m:
            raise ValueError(f"Professor com name='{name}' não encontrado")

        for key, value in updated_data.items():
            if key == "password":
                value = bcrypt.hashpw(value.encode(), bcrypt.gensalt()).decode()
            if hasattr(m, key):
                setattr(m, key, value)

        m.save()
        return self._to_entity(m)

    def delete_by_name(self, name: str) -> None:
        deleted_count = ProfessorModel.objects(name=name).delete()
        if deleted_count == 0:
            raise ValueError(f"Professor com name='{name}' não encontrado")

    def delete_by_id(self, professor_id: str) -> None:
        try:
            oid = ObjectId(professor_id)
        except Exception:
            raise ValueError("Professor ID inválido")
        
        deleted_count = ProfessorModel.objects(id=oid).delete()
        if deleted_count == 0:
            raise ValueError("Professor não encontrado")

    def update_by_id(self, professor_id: str, updated_data: dict) -> Professor:
        try:
            oid = ObjectId(professor_id)
        except Exception:
            raise ValueError("Professor ID inválido")
            
        model = ProfessorModel.objects(id=oid).first()
        if not model:
            raise ValueError("Professor não encontrado")

        for key, value in updated_data.items():
            if key == "password":
                value = bcrypt.hashpw(value.encode(), bcrypt.gensalt()).decode()
            if hasattr(model, key):
                setattr(model, key, value)
        model.save()
        return self._to_entity(model)
