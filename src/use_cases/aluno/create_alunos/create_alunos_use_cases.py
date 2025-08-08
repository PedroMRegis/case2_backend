from entities.aluno import Aluno
from repositories.aluno_repository import AlunoRepository
from use_cases.aluno.create_alunos.create_alunos_dto import CreateAlunoDTO

class CreateAlunoUseCases:
    def __init__(self, aluno_repository: AlunoRepository):
        self.aluno_repository = aluno_repository

    def execute(self, aluno_data: CreateAlunoDTO) -> Aluno:
        try:
            # Criar a entidade aluno
            aluno = Aluno(
                name=aluno_data.name,
                email=aluno_data.email,
                password=aluno_data.password,
                plano=aluno_data.plano
            )
            
            # Salvar no repositório
            saved_aluno = self.aluno_repository.save(aluno)
            return saved_aluno
            
        except ValueError as e:
            # Re-propagar erros de validação
            raise ValueError(str(e))
        except Exception as e:
            # Tratar outros erros
            raise Exception(f"Erro ao criar aluno: {str(e)}")
