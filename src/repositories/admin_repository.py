import bcrypt
from bson import ObjectId
from entities.admin import Admin
from models.admin_model import AdminModel

class AdminRepository:

    @staticmethod
    def _to_entity(model: AdminModel) -> Admin:
        return Admin(
            id=str(model.id),
            name=model.name,
            email=model.email,
            password=model.password
        )

    def save(self, admin: Admin) -> Admin:
        model = AdminModel(
            name=admin.name,
            email=admin.email,
            password=bcrypt.hashpw(admin.password.encode(), bcrypt.gensalt()).decode(),
            reset_pwd_token="",  # Valor padrão para compatibilidade
            reset_pwd_token_sent_at=0  # Valor padrão para compatibilidade
        )
        try:
            model.save()
            # Busca o modelo salvo para garantir que temos o ID
            saved_model = AdminModel.objects(id=model.id).first()
            if saved_model is None:
                raise ValueError("Erro ao recuperar admin após salvar")
            return self._to_entity(saved_model)
        except Exception as e:
            raise ValueError(f"Erro ao salvar admin: {str(e)}")

    def find_all(self) -> list[Admin]:
        return [self._to_entity(m) for m in AdminModel.objects()]

    def find_by_name(self, name: str) -> Admin:
        model = AdminModel.objects(name=name).first()
        if not model:
            raise ValueError(f"Admin com nome '{name}' não encontrado")
        return self._to_entity(model)
    
    def find_by_email(self, email: str) -> Admin:
        model = AdminModel.objects(email=email).first()
        if not model:
            raise ValueError(f"Admin com email '{email}' não encontrado")
        return self._to_entity(model)
    
    def find_by_id(self, admin_id: str) -> Admin:
        try:
            oid = ObjectId(admin_id)
        except Exception:
            raise ValueError("Admin ID inválido")
        model = AdminModel.objects.with_id(oid)
        if not model:
            raise ValueError("Admin não encontrado")
        return self._to_entity(model)

    def update(self, name: str, updated_data: dict) -> Admin:
        model = AdminModel.objects(name=name).first()
        if not model:
            raise ValueError(f"Admin com nome '{name}' não encontrado")

        for key, value in updated_data.items():
            if key == "password":
                value = bcrypt.hashpw(value.encode(), bcrypt.gensalt()).decode()
            if hasattr(model, key):
                setattr(model, key, value)
        model.save()
        return self._to_entity(model)

    def delete_by_name(self, name: str) -> None:
        # Tenta deletar diretamente pelo campo `name`
        result = AdminModel.objects(name=name).delete()
        if result == 0:
            # nenhum registro removido → não encontrou ninguém com esse nome
            raise ValueError(f"Admin com nome '{name}' não encontrado")

    def delete_by_id(self, admin_id: str) -> None:
        try:
            oid = ObjectId(admin_id)
        except Exception:
            raise ValueError("Admin ID inválido")
        
        deleted_count = AdminModel.objects(id=oid).delete()
        if deleted_count == 0:
            raise ValueError("Admin não encontrado")
