# Transição

## Tutorial de Uso do Aplicativo AAC

### Visão geral

O aplicativo AAC (Atividades Acadêmicas Complementares) permite que alunos, coordenadores e organizações gerenciem, validem e acompanhem atividades complementares. Este tutorial descreve como preparar o ambiente, executar o sistema localmente e usar as funcionalidades básicas.

### Pré-requisitos

- Python 3.8+ instalado
- Git (opcional)

### Instalação e execução (Windows - PowerShell)

1. Abra o PowerShell e navegue até a pasta do projeto:

```powershell
cd c:\Users\mmpec\Downloads\PBE_26.1_8003_I\src\AAC
```

2. Crie e ative um ambiente virtual, instale dependências:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

3. Aplicar migrações e criar um superusuário (opcional para administração):

```powershell
python manage.py migrate
python manage.py createsuperuser
```

4. Iniciar o servidor de desenvolvimento:

```powershell
python manage.py runserver
```

O servidor ficará disponível em `http://127.0.0.1:8000/`.

### Configuração inicial

- Crie contas de teste para as funções principais: aluno, coordenador e organização.
- No painel admin (`/admin/`) você pode criar usuários, definir grupos/permissões e inspecionar modelos.

### Uso básico do sistema

- **Login:** Acesse a página de login e entre com as credenciais.
- **Dashboard do Aluno:** Após login como aluno, use o painel para visualizar atividades atribuídas, status e histórico.
- **Cadastrar atividade interna/externa:** Vá para as telas `cadastrar_atividade_interna` ou `cadastrar_atividade_externa`, preencha os dados e anexe comprovantes quando necessário.
- **Anexar comprovantes:** No formulário de cadastro, utilize o campo de upload para enviar arquivos de comprovação.
- **Validação/Fluxo do Coordenador:** O coordenador pode acessar o dashboard de validação, analisar submissões e alterar o status das atividades.

### Estrutura importante do projeto

- Código principal: `src/AAC/core/` (modelos, views, serializers, services)
- Gerenciamento do projeto Django: `src/AAC/manage.py`
- Dependências: `src/AAC/requirements.txt`

### Dicas e resolução de problemas

- Se houver erro de dependências, reveja `requirements.txt` e reinstale em um ambiente limpo.
- Se alterações em modelos não aparecerem, verifique acerto de migrações (`makemigrations` e `migrate`).
- Para ver logs detalhados, observe a saída do terminal onde o `runserver` foi iniciado.

