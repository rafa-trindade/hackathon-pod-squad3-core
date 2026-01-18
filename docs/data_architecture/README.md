![header](../images/data_architecture/header_architecture.png)

Este documento detalha a arquitetura técnica da plataforma de dados, justificando a escolha das ferramentas para um cenário de execução em **Virtual Private Server (VPS)**. A solução foi desenhada como uma PoC de alta fidelidade, garantindo escalabilidade, governança pragmática e observabilidade nativa.

## 🛠️ Arquitetura Macro (Visão de Fluxo)

A arquitetura macro ilustra o ciclo de vida do dado, integrando governança e observabilidade em cada etapa do fluxo.

![Arquitetura Macro](../images/data_architecture/arquitetura_macro.png)

### Camadas de Fluxo e Governança Ativa
* **Ingestion & External Data:** Captura de fontes disjuntas com validação via **Contratos de Dados (Pandera)**, garantindo conformidade antes da persistência na camada Landing.
* **Data Processing (Medallion):** Implementação das camadas **Bronze, Silver e Gold** no MinIO (S3-Compatible). 
* **Engine de Processamento:** O **DuckDB** executa transformações SQL vetorizadas com alta eficiência em recursos limitados.
* **Data Observability:** Monitoramento automático de *Freshness*, Volume e Distribuição através de auditorias programáticas e logs de integridade.
* **Deliverables:** Entrega de modelos via **MLflow** e dashboards em **Streamlit**.


## 🛠️ Arquitetura Micro (Visão de Componentes)

O desenho micro detalha o isolamento e a orquestração dos serviços que sustentam as políticas de governança.

![Arquitetura Micro](../images/data_architecture/arquitetura_micro.png)

* **Orquestração (Apache Airflow):** Maestro responsável por garantir a idempotência e a ordem de execução das DAGs.
* **Isolamento (Docker):** Coexistência de serviços (MinIO, Postgres, Airflow) em containers, facilitando o setup e a portabilidade.
* **Data Warehouse (PostgreSQL + dbt):** Modelagem dimensional (Star Schema) para consumo analítico, com governança de transformações via dbt.


## 🧱 Matriz de Componentes e Diferenciais Estratégicos

| Componente | Papel na Arquitetura | Diferencial Estratégico (PoC) | Governança Aplicada |
|:---|:---|:---|:---|
| **MinIO** | **Data Lake S3** | **Cloud-Ready:** Migração transparente para ambientes de nuvem via S3-API. | **Imutabilidade:** Estratégia de `run_id` para reprocessabilidade total. |
| **DuckDB** | **Compute Engine** | Performance analítica local sem necessidade de clusters Spark. | **Partition Pruning:** Acelera consultas em até 90% via filtros `ano_mes`. |
| **dbt Core** | **Modelagem Analítica** | Governança de transformações com testes e linhagem automática. | **Documentação Viva:** Reflete o estado real do Warehouse no PostgreSQL. |
| **Pandera** | **Data Quality** | Validação de schema na ingestão (Data Contracts). | **Prevenção de Erros:** Bloqueia inconsistências na entrada do pipeline. |
| **MLflow** | **ML Lifecycle** | Versionamento e rastreio de modelos treinados (.pkl). | **Auditabilidade:** Rastreia qual versão do código gerou qual modelo. |


## 🚀 Estratégias de Engenharia e Confiabilidade

Esta PoC implementa pilares de **Data Reliability** que garantem a resiliência operacional na VPS:

1. **Governança via Código (Policy as Code):**
   * **Política de Retenção Ativa:** Limpeza automatizada post-write para evitar esgotamento de storage, mantendo apenas as `MAX_RUNS` necessárias para rollback imediato.
   * **Particionamento Hive:** Padronização da chave `ano_mes=YYYYMM` (BIGINT) auditada programaticamente para evitar *data drift* físico.

2. **Observabilidade Emergente:**
   * **Freshness & Integridade:** Uso da coluna técnica `ingestion_ts` e auditoria de partições para garantir que a estrutura física condiz com a cronologia dos dados.
   * **Saúde de Safra (Health Check):** Monitoramento de volumetria (regra 10%-90%) na Gold Pipeline, impedindo o processamento de cargas incompletas.
   * **Audit de Overlap:** Monitoramento da taxa de encontro de chaves entre camadas para garantir a riqueza de informação necessária à modelagem.

3. **Resiliência e Recuperação:**
   * **Idempotência:** O reprocessamento de um mesmo mês não gera duplicidade; a nova `run_id` substitui logicamente a anterior.
   * **Isolamento de Erros:** Como cada execução é encapsulada por um timestamp ISO, falhas na run atual não corrompem dados históricos estáveis.