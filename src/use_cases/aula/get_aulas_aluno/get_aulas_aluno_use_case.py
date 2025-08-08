from repositories.aula_repository import AulaRepository
from repositories.professor_repository import ProfessorRepository
from repositories.aluno_repository import AlunoRepository

class GetAulasAlunoUseCase:
    def __init__(self, aula_repository: AulaRepository, professor_repository: ProfessorRepository, aluno_repository: AlunoRepository):
        self.aula_repository = aula_repository
        self.professor_repository = professor_repository
        self.aluno_repository = aluno_repository

    def execute(self, aluno_id: str) -> list[dict]:
        try:
            # Buscar todas as aulas
            all_aulas = self.aula_repository.find_all()
            
            # Filtrar apenas as aulas do aluno
            filtered_aulas = [aula for aula in all_aulas if aula.aluno_id == aluno_id]
            
            # Enriquecer dados com informações do professor
            enriched_aulas = []
            for aula in filtered_aulas:
                try:
                    # Buscar dados do professor
                    professor = self.professor_repository.find_by_id(aula.professor_id)
                    professor_name = professor.name
                    professor_idioma = professor.idioma
                    professor_trilha = professor.trilha
                except:
                    professor_name = "Professor não encontrado"
                    professor_idioma = "N/A"
                    professor_trilha = "N/A"
                
                try:
                    # Buscar dados do aluno (para confirmar)
                    aluno = self.aluno_repository.find_by_id(aula.aluno_id)
                    aluno_name = aluno.name
                    aluno_email = aluno.email
                except:
                    aluno_name = "Aluno não encontrado"
                    aluno_email = "Email não disponível"
                
                enriched_aulas.append({
                    "id": aula.id,
                    "date": aula.date,
                    "status": aula.status,
                    "professor_id": aula.professor_id,
                    "professor_name": professor_name,
                    "professor_idioma": professor_idioma,
                    "professor_trilha": professor_trilha,
                    "aluno_id": aula.aluno_id,
                    "aluno_name": aluno_name,
                    "aluno_email": aluno_email
                })
            
            return enriched_aulas
            
        except Exception as e:
            raise ValueError(f"Erro ao buscar aulas do aluno: {str(e)}")
