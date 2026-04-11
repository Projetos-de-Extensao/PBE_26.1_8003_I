---
id: prototipobaixa
title: Protótipo Baixa Fidelidade
---
## Introdução

<p align = "justify">
A construção do protótipo de alta fidelidade auxilia a equipe de desenvolvimento a encontrar um nível de detalhes abrangentes, extrair funcionalidades, testar usabilidade, e também fornece uma base para o gerenciamento do projeto pois com o protótipo é possível realizar estimativas de quanto tempo será necessário desempenhar em cada funcionalidade.
</p>

## Metodologia

<p align = "justify">
Iniciamos o projeto através dos levantamentos iniciais da equipe, após discussões a ferramenta Figma foi selecionada para produzir o protótipo de alta fidelidade com auxílio do Material Design Color Tool.
</p>

## Protótipo de Baixa Fidelidade

### Versão 1.0

# Tela de login

@startsalt
{+
  == Login - Sistema AAC IBMEC
  .
  Usuário (E-mail): | "exemplo@ibmec.edu.br  "
  Senha:            | "******* "
  .
  [  Entrar  ] | [ Esqueci a Senha ]
}
@endsalt


# Dashboard do aluno

@startsalt
{+
  == Dashboard: João Silva (Matrícula: 20240123)
  .
  {T
    Eixo Temático | Horas Obtidas | Mínimo Exigido | Status
    Ensino        | 40h           | 60h            | Em progresso
    Pesquisa      | 20h           | 40h            | Em progresso
    Extensão      | 50h           | 50h            | Concluído
    --            | --            | --             | --
    **Total** | **110h** | **150h** | **73%**
  }
  .
  [ + Cadastrar Nova Atividade ] | [ Gerar Relatório PDF ]
}
@endsalt

# Cadastro de atividades externas

@startsalt
{+
  == UC02 - Cadastrar Atividade Externa
  .
  Tipo de Atividade: | ^Cursos Livres / Idiomas^
  Carga Horária:     | "20 " (Horas)
  Data de Conclusão: | "10/04/2026"
  .
  Descrição da Atividade:
  {
    "Certificado de curso de Python Avançado realizado na plataforma Udemy."
  }
  .
  Comprovante (PDF/Imagem): | [ Selecionar Arquivo... ]
  .
  [  Cancelar  ] | [ Enviar para Validação ]
}
@endsalt