# 🎯 Contexto de Negócio e Entendimento do Problema

Este documento detalha o desafio estratégico, os objetivos de negócio e o escopo técnico do projeto desenvolvido para o Hackathon PoD Academy Claro, focando na conversão sustentável de clientes da base Pré-paga para o Controle.

---

## 💼 Contexto e Problema de Negócio

A Claro busca expandir a base de clientes em planos controle de forma sustentável, equilibrando crescimento e gestão de risco. 

**O Desafio:** Identificar clientes pré-pagos que, caso migrados para o plano controle, apresentem menor probabilidade de inadimplência. Isso permite a priorização de ofertas, redução de risco financeiro e aumento da rentabilidade operacional.

---

## 🚀 Objetivo do Projeto

Desenvolver um **Modelo de Behavior** (visão unificada por CPF/cliente) para estimar o risco de inadimplência no contexto de migração **Pré → Controle**, entregando:

* **Score Individual:** Risco estimado por cliente.
* **Faixas de Risco:** Divisão em decis/bins para suporte à decisão operacional.
* **Recomendação de Política Inicial:** Definição de cortes e análise de *trade-offs* entre risco vs. massa de clientes.

### 📈 Valor para o Negócio

* **Aumento de Faturamento:** Melhor direcionamento da oferta de migração para perfis com maior sustentabilidade e maior LTV (*Lifetime Value*) esperado.
* **Redução de Custos:** Mitigação da inadimplência e menor desperdício de recursos em campanhas para perfis de alto risco.
* **Eficiência Operacional:** Decisão padronizada, explicável e baseada em dados, reduzindo o retrabalho manual.

---

## 📝 Escopo e Entregáveis

### ✅ Em escopo (Mínimo para Bancas) 
* **Plano de Execução** - Planejamento e entrega imediata.
* **Estudo de Público-Alvo** - EDA orientada a risco.
* **Books de Variáveis** - Documentação funcional das variáveis por domínio.
* **Modelo Baseline** - Métricas e primeira versão reprodutível.
* **Modelo Final (.pkl)** - Pipeline completo de treino e validação.
* **Plano de Monitoramento** - Métricas, drift, rotina e alertas.
* **Documentação de Engenharia** - Arquitetura, Lineage, Governança e Observabilidade.
* **Apresentação Final** - Storyline executiva e evidências técnicas.

### ❌ Fora de escopo
* **Ativação Produtiva** - Foco exclusivo em recomendação estratégica e prototipagem.
* **Dados Externos** - Enriquecimentos além dos dados de amostragem (tratados como *nice to have*).
* **Implementação de MLOps** - Foco limitado ao desenho técnico e plano de monitoramento.

---

## 4. Estado Atual do Projeto
*Status em 14/01/2026*

O projeto encontra-se com a fundação de dados consolidada, apresentando:
* **Infraestrutura:** Repositório versionado com profiling e EDA inicial.
* **Engenharia:** Ingestão via MinIO + DuckDB com suporte a S3.
* **Arquitetura Medallion:** Camadas **Raw**, **Bronze** e **Silver** estruturadas.
* **Domínios Processados:** Scripts Silver finalizados para os domínios de Atrasos, Pagamentos, Recargas, Telco, Score Bureau Móvel e Dados Cadastrais.