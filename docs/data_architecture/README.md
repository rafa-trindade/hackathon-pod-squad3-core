![header](../images/data_architecture/header_architecture.png)

Este documento detalha a arquitetura técnica da plataforma de dados, justificando a escolha das ferramentas para um cenário de execução em **Virtual Private Server (VPS)**. A solução foi desenhada como uma PoC de alta fidelidade, garantindo escalabilidade, portabilidade, governança pragmática e observabilidade nativa.

## 🛠️ Arquitetura Macro (Visão de Fluxo)

A arquitetura macro ilustra o fluxo end-to-end do dado, evidenciando como políticas de governança e mecanismos de observabilidade se materializam ao longo das etapas de ingestão, processamento e consumo.

![Arquitetura Macro](../images/data_architecture/arquitetura_macro.png)

### Camadas de Fluxo e Governança Ativa
* **Ingestion & External Data:** Captura de fontes com validação via **Contratos de Dados (Pandera)**, garantindo conformidade antes da persistência na camada Raw/Landing.
* **Data Processing (Medallion):** Implementação das camadas **Bronze, Silver e Gold** no MinIO (S3-Compatible). 
* **Engine de Processamento:** O **DuckDB** executa transformações SQL vetorizadas com alta eficiência em recursos limitados.
* **Data Observability:** Monitoramento automático de *Freshness*, Volumetria e Distribuição Estatística. Os logs de execução e relatórios técnicos são persistidos no Data Lake (S3) vinculados ao `run_id`, garantindo auditoria histórica e governança operacional.
* **Deliverables:** Entrega de modelo **.pkl**, relatórios de análise de público e dashboard analítico em **Streamlit** (escopo opcional).

## 🛠️ Arquitetura Micro (Visão de Componentes)

A arquitetura micro detalha os componentes da plataforma e seus mecanismos operacionais, evidenciando como armazenamento, isolamento, orquestração e controle de execução sustentam as políticas de governança, confiabilidade e reprodutibilidade.


![Arquitetura Micro](../images/data_architecture/arquitetura_micro.png)

* **Orquestração (Apache Airflow):** Maestro responsável por garantir a idempotência e a ordem de execução das DAGs.
   * **Identificação de Ciclo:** Nesta orquestração, um `run_id` exclusivo é gerado a cada execução. Isso garante que o dado processado e seus respectivos artefatos de observabilidade estejam deterministicamente vinculados à mesma janela de execução.
* **Isolamento (Docker):** Coexistência de serviços (MinIO, Postgres, Airflow) em containers, facilitando o setup e a portabilidade.
* **Data Lake (MinIO - S3 Compatible):** Camada de armazenamento central baseada no padrão Medallion (Bronze, Silver e Gold), com dados imutáveis por `run_id`.
    * **Fluxo de Evidências Técnicas:** O `run_id` atua como a chave mestra que vincula o processamento do dado aos buckets dedicados de **OBSERVABILITY** e **REPORTS**.
    * **Persistência de Artefatos:** Os artefatos de observabilidade são gerados localmente para consulta imediata e automaticamente persistidos no Data Lake a cada execução, garantindo um histórico imutável e auditável vinculado a cada processamento.
* **Data Warehouse (PostgreSQL + dbt):** Modelagem dimensional (Star Schema) para consumo analítico, com governança de transformações via dbt. *(escopo opcional)*
* **Camada Analítica & ML:**
  * **Jupyter Notebook:** Executado em ambiente isolado, consome dados da camada Gold para exploração, treino e validação de modelos, gerando artefatos analíticos e modelos versionados (.pkl).
  * **Streamlit:** Camada de visualização para consumo de KPIs e métricas a partir dos **Data Marts do Data Warehouse**. *(escopo opcional)*



## 🧱 Matriz de Componentes e Diferenciais Estratégicos

A matriz abaixo destaca apenas os componentes que representam decisões arquiteturais estratégicas da PoC, com impacto direto em governança, confiabilidade e observabilidade. Componentes de infraestrutura e orquestração são detalhados na Arquitetura Micro.

| Componente | Papel na Arquitetura | Diferencial Estratégico (PoC) | Governança Aplicada |
|:---|:---|:---|:---|
| **MinIO** | **Data Lake S3** | **Cloud-Ready:** Migração transparente para ambientes de nuvem via S3-API. | **Imutabilidade:** Estratégia de `run_id` para reprocessabilidade total. |
| **DuckDB** | **Compute Engine** | Performance analítica local sem necessidade de clusters Spark. | **Partition Pruning:** Acelera consultas em até 90% via filtros `ano_mes`. |
| **dbt Core** | **Modelagem Analítica** | Governança de transformações com testes e linhagem automática. | **Documentação Viva:** Reflete o estado real do Warehouse no PostgreSQL. |
| **Pandera** | **Data Quality** | Validação de schema na ingestão (Data Contracts). | **Prevenção de Erros:** Bloqueia inconsistências na entrada do pipeline. |
| **Jupyter Notebook** | **Experimentação & ML** | Treinamento interativo de modelos e feature engineering com baixo overhead operacional. | **Reprodutibilidade:** Notebooks versionados, seeds fixas e datasets imutáveis por `run_id`. |
| **Streamlit** | **Camada de Apresentação** | Exposição opcional de KPIs e métricas analíticas para stakeholders. | **Consumo Governado:** Acesso somente a Data Marts do Data Warehouse e artefatos de modelo versionados. |
| **Observability** | **Metadata Storage** | **Persistência de Artefatos:** Logs e reports gerados localmente são sincronizados com o S3. | **Histórico Imutável:** Garante um lastro auditável de saúde e qualidade vinculado a cada `run_id`. |

## 🚀 Estratégias de Engenharia e Confiabilidade

Esta PoC implementa pilares de **Data Reliability** que garantem a resiliência operacional na VPS:

1. **Governança via Código (Policy as Code):**
   * **Política de Retenção Ativa:** Limpeza automatizada post-write para evitar esgotamento de storage, mantendo apenas as `MAX_RUNS` necessárias para rollback imediato.
   * **Particionamento Hive:** Padronização da chave `ano_mes=YYYYMM` (BIGINT) auditada programaticamente para evitar *data drift* físico.

2. **Observabilidade Emergente:**
   * **Freshness & Integridade:** Uso da coluna técnica `ingestion_ts` e auditoria de partições para garantir que a estrutura física condiz com a cronologia dos dados.
   * **Saúde de Safra (Health Check):** Monitoramento de volumetria (regra 10%-90%) na Gold Pipeline, impedindo o processamento de cargas incompletas.
   * **Audit de Overlap:** Monitoramento da taxa de encontro de chaves entre camadas para garantir a riqueza de informação necessária à modelagem.
   * **Persistência de Evidências:** A arquitetura garante que todos os logs e relatórios técnicos sejam sincronizados com o S3 ao final de cada ciclo. Isso estabelece um lastro histórico permanente, permitindo auditorias retroativas e garantindo que nenhuma execução ocorra sem o seu respectivo registro de saúde e qualidade.

3. **Resiliência e Recuperação:**
   * **Idempotência:** O reprocessamento de um mesmo mês não gera duplicidade; a nova `run_id` substitui logicamente a anterior.
   * **Isolamento de Erros:** Como cada execução é encapsulada por um timestamp ISO, falhas na run atual não corrompem dados históricos estáveis.

<br>

> A arquitetura demonstra que observabilidade e governança não são camadas adicionais, mas propriedades emergentes de decisões corretas de engenharia.


## 📚 Documentação Complementar

### 🏛️ Data Governance
📑 **[Manual de Governança](../data_governance/README.md)**  
Diretrizes formais de governança aplicadas ao projeto.

---

### 🔍 Data Observability
📑 **[Manual de Observabilidade](../data_observability/README.md)**  
Referência das práticas de monitoramento e saúde do pipeline.

---

### ⚙️ Operação e Setup
📑 **[Guia de Execução do Projeto](../guides/pipeline_execution.md)** Protocolos de infraestrutura e passos para acionamento do pipeline.


