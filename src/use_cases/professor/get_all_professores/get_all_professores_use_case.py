from repositories.professor_repository import ProfessorRepository
from entities.professor import Professor

class GetAllProfessoresUseCase:
    def __init__(self, professor_repository: ProfessorRepository):
        self.professor_repository = professor_repository

    def execute(self, user_id: str, user_type: str) -> list[dict]:
        try:
            # Buscar todos os professores
            all_professores = self.professor_repository.find_all()
            
            # Retornar dados estruturados
            professores_data = []
            for professor in all_professores:
                professores_data.append({
                    "id": professor.id,
                    "name": professor.name,
                    "email": professor.email,
                    "idioma": professor.idioma,
                    "trilha": professor.trilha
                })
            
            return professores_data
            
        except Exception as e:
            raise ValueError(f"Erro ao buscar professores: {str(e)}")
