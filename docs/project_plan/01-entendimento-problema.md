# 🎯 Contexto de Negócio e Entendimento do Problema

Este documento detalha o desafio estratégico, os objetivos de negócio e o escopo técnico do projeto desenvolvido para o Hackathon PoD Academy Claro, focando na conversão sustentável de clientes da base Pré-paga para o Controle.


## 1️⃣ Contexto e Problema de Negócio

A Claro busca expandir a base de clientes em planos controle de forma sustentável, equilibrando crescimento e gestão de risco. 

**O Desafio:** Identificar clientes pré-pagos que, caso migrados para o plano controle, apresentem menor probabilidade de inadimplência. Isso permite a priorização de ofertas, redução de risco financeiro e aumento da rentabilidade operacional.


## 2️⃣ Objetivo do Projeto

Desenvolver um **Modelo de Behavior** (visão unificada por CPF/cliente) para estimar o risco de inadimplência no contexto de migração **Pré → Controle**, entregando:

* **Score Individual:** Risco estimado por cliente.
* **Faixas de Risco:** Divisão em decis/bins para suporte à decisão operacional.
* **Recomendação de Política Inicial:** Definição de cortes e análise de *trade-offs* entre risco vs. massa de clientes.


### 📈 Valor para o Negócio

* **Aumento de Faturamento:** Melhor direcionamento da oferta de migração para perfis com maior sustentabilidade e maior LTV (*Lifetime Value*) esperado.
* **Redução de Custos:** Mitigação da inadimplência e menor desperdício de recursos em campanhas para perfis de alto risco.
* **Eficiência Operacional:** Decisão padronizada, explicável e baseada em dados, reduzindo o retrabalho manual.