---
id: diagrama_de_casos de uso
title: Diagrama de Casos de Uso
---

## Diagrama de Classe a 1km de distância

@startuml
skinparam monochrome true
skinparam shadowing false
skinparam packageStyle rectangle

title Visão Conceitual do Banco de Dados (AAC IBMEC)

rectangle "Gestão de Usuários" {
    entity Aluno
    entity Coordenação
}

rectangle "Regras e Normativas" {
    entity EixoTematico
    entity TipoAtividade
}

rectangle "Operacional" {
    entity AtividadeComplementar
}

Aluno "1" -- "" AtividadeComplementar : submete >
EixoTematico "1" -- "" TipoAtividade : agrupa >
TipoAtividade "1" -- "" AtividadeComplementar : define limites para >
AtividadeComplementar "" -- "1" Coordenação : é analisada por >

@enduml
