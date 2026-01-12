# 🛠️ Abordagem da Solução: Técnicas, Ferramentas e Estratégias

Este documento detalha a stack tecnológica e as metodologias aplicadas no projeto, justificando as escolhas baseadas no cenário de execução em uma **VPS (Virtual Private Server)** atuando como uma **Prova de Conceito (PoC)** de uma plataforma de dados moderna, ponta a ponta e escalável.


## 1️⃣ Stack Tecnológica e Justificativas

### 1.1 Infraestrutura e Orquestração
* **Ferramenta:** `Docker & Docker Compose`
    * **Justificativa:** Base para o isolamento de serviços em containers. Garante que MinIO, Postgres e Airflow coexistam na VPS sem conflitos de dependências e com portabilidade garantida.
* **Ferramenta:** `Apache Airflow`
    * **Justificativa:** O "maestro" do projeto. Responsável pelo agendamento e monitoramento dos fluxos (DAGs), garantindo a ordem de execução desde a ingestão até a entrega dos modelos de ML.

### 1.2 Armazenamento e Data Lake (MinIO)
* **Ferramenta:** `MinIO (S3-Compatible)`
    * **Justificativa:** Implementa a **Arquitetura Medallion** (BRONZE, SILVER, GOLD) em um storage de objetos local. O diferencial é ser *Cloud-Ready*: o código escrito para o MinIO funciona nativamente no AWS S3 caso a PoC avance para nuvem pública.

### 1.3 Processamento e Qualidade
* **Ferramenta:** `DuckDB (Vectorized Query Engine)`
    * **Justificativa**: O "coração" do processamento. Por ser uma engine *in-process*, ele não requer um cluster pesado (como Spark), sendo extremamente eficiente em ambientes de VPS com recursos limitados de memória e CPU. Oferece performance de nível Spark para arquivos Parquet e CSV com a volumetria do nosso cenário.
* **Ferramenta:** `Python & Pandas`
    * **Justificativa**: Linguagem base para orquestração, automação de scripts de profiling e integração entre os componentes.
* **Ferramenta:** `Pandera`
    * **Justificativa**: Utilizado para **Contratos de Dados na Origem**. Garante que o dado que entra na camada Landing/Raw respeite o schema esperado, evitando o "efeito cascata" de erros nas camadas posteriores.

### 1.4 Transformação e Data Warehouse (Arquitetura Bônus)
* **Ferramenta:** `dbt (Data Build Tool) & PostgreSQL`
    * **Justificativa:** O dbt gerencia o ciclo de vida do SQL no PostgreSQL, organizando a transformação em camadas lógicas: `raw_schema`, `dw_staging`, `dw_core` (Star Schema) e `dw_marts`. Garante documentação e testes automatizados.

### 1.5 Ciência de Dados e Entrega
* **Ferramenta:** `MLflow`
    * **Justificativa:** Gerencia o ciclo de vida dos modelos de Machine Learning (Produção `.pkl`), permitindo rastrear experimentos, parâmetros e versões dos modelos treinados.
* **Ferramenta:** `Streamlit (Bônus)`
    * **Justificativa:** Transforma os dados modelados em **Decision Intelligence**, entregando dashboards interativos e aplicações analíticas diretamente para os stakeholders.


## 2️⃣ Estratégias de Engenharia Aplicadas

### 2.1. Escopo e Escalabilidade (Visão de Negócio)
A arquitetura foi pensada já considerando a **volumetria real da Claro** (capaz de crescer verticalmente independente de onde esteja hospedada). No entanto, a implementação atual e os processamentos estão dimensionados com base em um **dataset de "teste"** (nossa base de amostra).

Esta abordagem foi adotada para:
- Garantir a viabilidade técnica dentro dos recursos da VPS.
- Manter a simplicidade e agilidade durante o ciclo de desenvolvimento.
- Validar a lógica de governança antes do scale-up para o ambiente produtivo final.

---

### 2.2 Arquitetura Medallion & Star Schema
Organizamos o dado para dois propósitos distintos:
1. **No Lake (MinIO):** Foco em armazenamento eficiente, imutabilidade e histórico transacional.
2. **No DW (Postgres) (Bônus):** Modelagem dimensional (Fatos e Dimensões) otimizada para performance de BI e consumo por aplicações.

---

### 2.3 Estratégia de Particionamento & Run_ID
Adotamos o particionamento físico por `ano_mes=YYYYMM` associado ao metadado técnico `run_id`.
* **Benefício:** Permite o *Partition Pruning* no DuckDB (lê apenas o necessário) e isola execuções. Se um processo falha, o Airflow pode re-executar apenas aquela run específica sem afetar o histórico estável.

---

### 2.4 Política de Retenção Ativa
Utilitário de limpeza programática que gerencia o ciclo de vida das runs no storage.
* **Por que:** Como o MLflow e as camadas do Data Lake geram alto volume de arquivos, a retenção automática evita que o armazenamento da VPS se esgote, mantendo a resiliência operacional.


## 3️⃣ Estratégia de Modelagem

### 3.1 Princípios de Solução
* **Granularidade Única** - Visão consolidada por CPF/Cliente.
* **Temporalidade Controlada** - Features calculadas em janela anterior ao target para evitar vazamento de dados (*leakage*).
* **Reprocessamento Consistente** - Capacidade de recalcular a ABT por data de referência quando necessário.
* **Auditabilidade** - Variáveis versionadas e documentadas em Books de Variáveis.

---

### 3.2 ABT (Analytical Base Table) - Contrato para Modelagem
A ABT é construída a partir da camada Silver, agregando sinais por cliente com janelas temporais (ex: 30/60/90 dias).
**Domínios previstos (Mapeados à Silver):**
* Atrasos/Delinquência
* Pagamentos
* Recargas
* Uso Telco/Engajamento
* Bureau Móvel (Score Externo)
* Cadastro/Estabilidade

---

### 3.3 Definição do Target e Modelagem

O **Target (Inadimplência)** será formalizado no início da execução (Sprint 0), contemplando a definição operacional do evento, janela de performance (horizonte para observação), data de referência para features e corte temporal para validação.

* **Modelagem:** Inicia com um **Baseline rápido e reprodutível** para estabelecer referência, evoluindo de forma incremental via *Feature Engineering* e validação temporal. 

* **Entrega Operacional:** Disponibilização de score contínuo, faixas/decis com taxa de inadimplência por faixa e sugestão de política de corte (*trade-off* risco vs massa).


## 4️⃣ Diferencial da Solução e Escalabilidade
A arquitetura provada nesta PoC integra o que há de melhor no ecossistema de dados moderno. Embora rode hoje em uma VPS, a separação clara entre **Storage (MinIO)**, **Compute (DuckDB)** e **Modelagem (dbt)** permite que a solução escale horizontalmente para nuvens com esforço de migração próximo de zero, validando a viabilidade técnica e de governança do projeto.