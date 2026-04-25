---
id: levantamento de requisitos
title: Levantamento de Requisitos
---

# **06 - Levantamento de Requisitos e Caso de Uso**

**Sistema:** XXXX\*)

---

## **1. Identificação dos Stakeholders**

- **Aluno:** Aluno irá entrar e cadastrar sua atividade
- **Cordenação:** Irá avaliar e aprovar a atividade do aluno
- **Organização Acadêmica:** Junto com a coordenação, também é responsável por cadastrar atividades internas

---

### **2. Requisitos Funcionais**

- **Autenticação**: O sistema deve permitir login de usuários (Aluno, Coordenação, Organização Acadêmica).
- **Cadastro de atividade externa**: O sistema deve permitir ao aluno cadastrar atividades externas.
- **Anexo de comprovantes**: O sistema deve permitir ao aluno anexar comprovantes (PDF/imagem).
- **Visualizar atividades cadastradas**: O sistema deve permitir ao aluno visualizar atividades cadastradas.
- **Visualizar total de horas**: O sistema deve permitir ao aluno visualizar o total de horas acumuladas.
- **Visualizar progresso**: O sistema deve permitir ao aluno visualizar o progresso para obter todas as horas necessárias.
- **Validação de atividade externa**: O sistema deve permitir a coordenação validar ou rejeitar atividades externas.
- **Cadastro de atividade interna**: O sistema deve permitir a coordenação ou organização acadêmica cadastrar atividades internas.
- **Lançamento de horas**: O sistema deve lançar automaticamente as horas aos alunos participantes.

---

### **3. Requisitos Não Funcionais**

- **Armazenamento de arquivos**: O Sistema deve possuir a capacidade de armazenar arquivos pdf, imágens, etc.
- **O sistema deve ser seguro, protegendo os dados dos alunos**: O Sistema deve garantir a segurança dos dados do usuário.
- **Sistema deve estar disponível 24 horas por dia**: O sistema deve estar disponível indefinidamente, com os servidores abertos.
- **Interface deve ser fácil de usar** O Sistema deve possúir boa usabilidade.

---

### **4. Exemplo de Caso de Uso** (Exemplo)

#### UC01 – Realizar Login

Ator: Aluno/Coordenação/Organização Acadêmica

Descrição: Permite acesso ao sistema

Fluxo:

Usuário insere login e senha

Sistema valida credenciais

Sistema libera acesso

#### UC02 – Cadastrar Atividade Externa

Ator: Aluno

Fluxo:

Aluno acessa área de atividades

Preenche dados (tipo, carga horária, descrição)

Anexa comprovante

Envia solicitação

Sistema salva como “pendente”

#### UC03 – Validar Atividade Externa

Ator: Coordenação

Fluxo:

Admin acessa atividades pendentes

Analisa comprovante

Aprova ou rejeita

Sistema atualiza status

Sistema contabiliza horas (se aprovado)

#### UC04 – Consultar Horas

Ator: Aluno

Fluxo:

Aluno acessa dashboard

Sistema exibe:

Total de horas

Progresso

Lista de atividades

#### UC05 – Cadastrar Atividade Interna

Ator: Coordenação/Organização Acadêmica

Fluxo: Admin cria atividade

Admin cria atividade

Define carga horária

Associa alunos participantes

Sistema lança horas automaticamente

---

### Diagrama de Casos de Uso

Aqui está o diagrama de **Caso de Uso (UML)**:

[![Casos de Uso](../assets/Casos_de_Uso/Casos_de_uso.png)](../assets/Casos_de_Uso/Casos_de_uso.png)
