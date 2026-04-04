---
id: levantamento de requisitos
title: Levantamento de Requisitos
---

# **06 - Levantamento de Requisitos e Caso de Uso**

**Sistema:** XXXX\*)

---

## **1. Identificação dos Stakeholders**

- **Aluno:** Aluno irá entrar e cadastrar sua atividade
- **Cordenação:** Irá avaliar e aprovar a atividade do aluno...

---

### **2. Requisitos Funcionais**

- **Cadastro de atividades externas**: O Sistema deve permitir que o aluno envie documentos para comprovar atividades fora da instituição. - **Cadastro de atividades internas**: O Sistema deve automaticamente identificar atividades internas.
- **Visualização de Horas** : O aluno deve ter acesso total à quantidade de horas registradas no total em atividades externas e internas.
- **Classificar atividades por tipo**: O Sistema deve categorizar as atividade em diferentes eixos (curso, palestra, evento, etc.)
- **Fazer login de alunos e coordenação** O sistema deve permitir o login de usuários
- **Visualização de atividades cadastradas**: O Aluno deve ter acesso total à visualização das atividades registradas
-

### **3. Requisitos Não Funcionais**

- **Armazenamento de arquivos**: O Sistema deve possuir a capacidade de armazenar arquivos pdf, imágens, etc.
- **O sistema deve ser seguro, protegendo os dados dos alunos**: O Sistema deve garantir a segurança dos dados do usuário.
- **Sistema deve estar disponível 24 horas por dia**: O sistema deve estar disponível indefinidamente, com os servidores abertos.
- **Interface deve ser fácil de usar** O Sistema deve possúir boa usabilidade.

---

### **4. Exemplo de Caso de Uso** (Exemplo)

UC01 – Realizar Login

Ator: Aluno/Admin
Descrição: Permite acesso ao sistema

Fluxo:

Usuário insere login e senha
Sistema valida credenciais
Sistema libera acesso

UC02 – Cadastrar Atividade Externa

Ator: Aluno

Fluxo:

Aluno acessa área de atividades
Preenche dados (tipo, carga horária, descrição)
Anexa comprovante
Envia solicitação
Sistema salva como “pendente”

UC03 – Validar Atividade

Ator: Administrador

Fluxo:

Admin acessa atividades pendentes
Analisa comprovante
Aprova ou rejeita
Sistema atualiza status
Sistema contabiliza horas (se aprovado)

UC04 – Consultar Horas

Ator: Aluno

Fluxo:

Aluno acessa dashboard
Sistema exibe:
Total de horas
Progresso
Lista de atividades

UC05 – Cadastrar Atividade Interna

Ator: Administrador

Fluxo: Admin cria atividade

Admin cria atividade
Define carga horária
Associa alunos participantes
Sistema lança horas automaticamente

---

### Diagrama de Casos de Uso (Exemplo)

Aqui está o diagrama de **Caso de Uso (UML)** para o cenário de **"Cadastro de atividades externas"**, usando **PlantUML**:

### **Código PlantUML**:

@startuml Cadastro_Externo
left to right direction

actor "Aluno" as Aluno
entity "Sistema" as Sistema

rectangle "Sistema de Horas Complementares" {
usecase "UC02 - Cadastrar Atividade Externa" as UC02
}

Aluno --> UC02

note right of UC02
**Fluxo Principal:**

1. Aluno acessa área de atividades
2. Preenche dados (tipo, carga horária, descrição)
3. Anexa comprovante (PDF/Imagem)
4. Envia solicitação
5. Sistema valida e salva como "Pendente"
   end note

UC02 ..> Sistema : <<persistir dados>>
@enduml
