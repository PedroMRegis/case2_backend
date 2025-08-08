from repositories.aula_repository import AulaRepository
from repositories.professor_repository import ProfessorRepository
from repositories.aluno_repository import AlunoRepository

class GetAulasProfessorUseCase:
    def __init__(self, aula_repository: AulaRepository, professor_repository: ProfessorRepository, aluno_repository: AlunoRepository):
        self.aula_repository = aula_repository
        self.professor_repository = professor_repository
        self.aluno_repository = aluno_repository

    def execute(self, professor_id: str) -> list[dict]:
        try:
            # Buscar todas as aulas
            all_aulas = self.aula_repository.find_all()
            
            # Debug: log do professor_id e aulas encontradas
            print(f"DEBUG: Buscando aulas para professor_id: {professor_id}")
            print(f"DEBUG: Total de aulas no sistema: {len(all_aulas)}")
            
            # Filtrar apenas as aulas do professor
            filtered_aulas = [aula for aula in all_aulas if aula.professor_id == professor_id]
            print(f"DEBUG: Aulas filtradas para o professor: {len(filtered_aulas)}")
            
            # Enriquecer dados com informações do aluno
            enriched_aulas = []
            for aula in filtered_aulas:
                print(f"DEBUG: Processando aula {aula.id} - professor_id: {aula.professor_id}, aluno_id: {aula.aluno_id}")
                
                try:
                    # Buscar dados do professor (para confirmar)
                    professor = self.professor_repository.find_by_id(aula.professor_id)
                    professor_name = professor.name
                    professor_idioma = professor.idioma
                    professor_trilha = professor.trilha
                except:
                    professor_name = "Professor não encontrado"
                    professor_idioma = "N/A"
                    professor_trilha = "N/A"
                
                try:
                    # Buscar dados do aluno
                    aluno = self.aluno_repository.find_by_id(aula.aluno_id)
                    aluno_name = aluno.name
                    aluno_email = aluno.email
                    aluno_plano = aluno.plano
                except:
                    aluno_name = "Aluno não encontrado"
                    aluno_email = "Email não disponível"
                    aluno_plano = "N/A"
                
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
                    "aluno_email": aluno_email,
                    "aluno_plano": aluno_plano
                })
            
            print(f"DEBUG: Retornando {len(enriched_aulas)} aulas enriquecidas")
            return enriched_aulas
            
        except Exception as e:
            print(f"DEBUG: Erro ao buscar aulas do professor: {str(e)}")
            raise ValueError(f"Erro ao buscar aulas do professor: {str(e)}")
