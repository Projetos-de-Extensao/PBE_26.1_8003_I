# Projeto Back-End 

**Código da Disciplina**: IBM8936<br>

## Sobre 
Descreva o seu projeto em linhas gerais. 

## Instalação 
**Linguagens**: Python, Django<br>
**Tecnologias**: Github, Visual Studio Code<br>
 os pré-requisitos para rodar o seu projeto são UX, Engenharia de Dados, POO.

### Instalação e execução do subprojeto `AAC`

Siga estes passos para executar localmente o aplicativo AAC (subpasta `src/AAC`):

- Pré-requisitos:
	- Python 3.8+ instalado
	- Git (opcional)

1. Abra um terminal (PowerShell no Windows) e navegue até a pasta do subprojeto:

```powershell
cd src\AAC
```

2. Crie e ative um ambiente virtual e instale dependências:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

3. Crie e aplique migrações do banco de dados:

```powershell
python manage.py makemigrations
python manage.py migrate
```

4. (Opcional) Crie um superusuário para acessar o admin do Django:

```powershell
python manage.py createsuperuser
```

5. Inicie o servidor de desenvolvimento:

```powershell
python manage.py runserver
```

O sistema ficará disponível em `http://127.0.0.1:8000/`.

Dicas:
- Se usar Windows PowerShell e houver bloqueio de execução de scripts, rode `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser` como administrador.
- Para problemas de dependências remova o venv e crie novamente antes de reinstalar.
- Para deploy em produção, configure variáveis de ambiente, banco e servidor WSGI/ASGI adequadamente.

