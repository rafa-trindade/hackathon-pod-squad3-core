# 📅 Cronograma e Planejamento de Entregas

Este documento detalha os marcos oficiais, o planejamento tático da Sprint 0 e a estratégia de mitigação de riscos para garantir o sucesso da PoC no Hackathon Claro.


## 1️⃣ Marcos Oficiais do Projeto

| Data | Marco / Entrega |
| :--- | :--- |
| **14/01/2026** | Entrega do Plano de Execução |
| **15/01/2026** | Checkpoint: Ciência de Dados |
| **20/01/2026** | Checkpoint: Engenharia de Dados |
| **03/02/2026** | Banca de Qualificação |
| **05/03/2026** | Banca Final |


## 2️⃣ Sprint 0 - Planejamento Imediato (Até 14/01)

Foco em travar escopo, decisões-base e consolidação do Plano de Execução.

| Dia | Frentes de Trabalho | Saída Esperada (DoD) |
| :--- | :--- | :--- |
| **D0 (11/01)** | **Analytics:** Métricas de sucesso, estrutura do Estudo de Público-Alvo e checklist de qualidade nas Silvers.<br><br>**DS:** Definição do target, granularidade CPF e proposta de janelas; desenho da ABT. | **Pager:** Objetivos, rascunho do target, granularidade, janelas e entregáveis. |
| **D1 (12/01)** | **Analytics:** Relatório de qualidade/cobertura (CPF, duplicidade, missing críticos, ranges).<br><br>**DS:** Estratégia de validação (split temporal), baseline planejado e features por domínio. | **Plano preenchido:** Seções de abordagem, métricas, dependências e riscos. |
| **D2 (13/01)** | **Analytics:** Backlog com épicos/histórias, owners e cadência de comunicação.<br><br>**DS:** Lista priorizada de features, critérios de aceite (baseline/final) e plano de evidências. | **Versão Review:** Plano disponível para o time de documentação adequar. |
| **D3 (14/01)** | **Squad:** Consolidação final de todas as frentes. | **Entrega Formal:** Plano finalizado com entendimento, cronograma e riscos. |


## 3️⃣ Evolução das Entregas

### 3.1 Até a Qualificação (15/01 → 03/02)
* **15/01:** Aprovação de Target/ABT + Baseline encaminhado + Primeiros insights de EDA.
* **20/01:** Validação do contrato **Silver → ABT** e definição da estratégia de reprocessamento.
* **03/02:** **Entrega Final da Fase:** Estudo de Público-Alvo + Books + Baseline + Documentação inicial + Arquitetura.

---

### 3.2 Até a Banca Final (04/02 → 05/03)
* **Modelagem:** Modelo final (.pkl), faixas de risco e recomendação de política inicial.
* **Observabilidade:** Plano de monitoramento completo.
* **Engenharia:** Documentação técnica consolidada e Storyline da apresentação final.


## 4️⃣ Governança e Cerimônias
* **Daily:** Reuniões curtas (10–15 min) para alinhamento de impedimentos.
* **Checkpoint Interno:** 2x por semana para validação de evidências (EDA, ABT, Modelagem, Books).
* **Revisão Pré-Banca:** Checklist de consistência entre premissas, números e narrativa.


## 5️⃣ Escopo e Entregáveis

### ✅ Em escopo (Mínimo para Bancas) 
* **Plano de Execução** - Planejamento e entrega imediata.
* **Estudo de Público-Alvo** - EDA orientada a risco.
* **Books de Variáveis** - Documentação funcional das variáveis por domínio.
* **Modelo Baseline** - Métricas e primeira versão reprodutível.
* **Modelo Final (.pkl)** - Pipeline completo de treino e validação.
* **Plano de Monitoramento** - Métricas, drift, rotina e alertas.
* **Documentação de Engenharia** - Arquitetura, Lineage, Governança e Observabilidade.
* **Apresentação Final** - Storyline executiva e evidências técnicas.

---

### ❌ Fora de escopo
* **Ativação Produtiva** - Foco exclusivo em recomendação estratégica e prototipagem.
* **Dados Externos** - Enriquecimentos além dos dados de amostragem (tratados como *nice to have*).
* **Implementação de MLOps** - Foco limitado ao desenho técnico e plano de monitoramento.


## 6️⃣ Estado Atual do Projeto
> *Status em 14/01/2026*

O projeto encontra-se com a fundação de dados consolidada, apresentando:
* **Infraestrutura:** Repositório versionado com profiling e EDA inicial.
* **Engenharia:** Ingestão via MinIO + DuckDB com suporte a S3.
* **Arquitetura Medallion:** Camadas **Raw**, **Bronze** e **Silver** estruturadas.
* **Domínios Processados:** Scripts Silver finalizados para os domínios de Atrasos, Pagamentos, Recargas, Telco, Score Bureau Móvel e Dados Cadastrais.