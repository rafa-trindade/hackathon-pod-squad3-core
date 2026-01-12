## 🚀 Hackathon Pod Academy - Squad 3

Repositório de desenvolvimento, documentação e implementação da solução integrada de dados para o Hackathon da Pod Academy - Squad 3.

## 📚 Mapeamento de Documentação (*Project Hub*)

### 📅 Gestão e Planejamento do Projeto
> 📁 [`docs/project_plan/*`](docs/project_plan/)  
> **Consolida** a visão estratégica e operacional do projeto, integrando o contexto de negócio, objetivos e plano de trabalho da Squad. **Define** o cronograma de entregas, as métricas de sucesso e as responsabilidades de cada frente sob uma abordagem híbrida de governança e agilidade.


### 🏗️ Data Architecture
> 📄 [`docs/data_architecture/`](docs/data_architecture/README.md)  
> **Define** a stack operada em VPS, utilizando Docker e Airflow para orquestração. **Combina** MinIO para storage Medallion (Cloud-Ready), DuckDB para processamento vetorial e PostgreSQL para o Data Warehouse, integrando modelagem via dbt, gestão de modelos com MLflow e entrega via Streamlit.


### 🏛️ Data Governance
> 📄 [`docs/data_governance/`](docs/data_governance/README.md)  
> **Estabelece** o framework de governança pragmática que consolida os pilares de Observabilidade, Profiling e Qualidade via *Policy as Code*. **Garante** a resiliência do ecossistema mediante versionamento de execuções (`run_id`), políticas de retenção para rollback imediato e eficiência de custos (FinOps).


### 🧬 Data Lineage
> 📁 [`docs/data_lineage/*`](docs/data_lineage/)  
> **Mapeia** a jornada do dado entre as camadas Medallion, garantindo padronização, tipagem forte e integridade técnica na camada Silver. **Foca** na rastreabilidade ponta a ponta e na otimização de performance através de particionamento físico e saneamento de metadados.
>
> * 📑 **Reports:** [`inspect_partition.log`](reports/observability/integrity/inspect_partition.log) - Validação física do particionamento e integridade dos caminhos de dados na camada Silver.


### 🧠 Feature Store & Book de Variáveis
> 📁 [`docs/data_modelling/*`](docs/data_modelling/)  
> **Apresenta** a documentação técnica da Camada Gold com foco em inteligência de dados e Machine Learning. **Consolida** o Book de Variáveis com definições de negócio e lógicas de agregação, além do registro de Feature Engineering para treinamento de modelos.


### 🔍 Data Observability
> 📄 [`docs/data_observability/`](docs/data_observability/README.md)  
> **Gerencia** a saúde dos dados através do monitoramento nativo de Freshness, Volume e Schema Drift. **Utiliza** metadados técnicos para auditoria, garantindo resiliência operacional com protocolos de rollback e diagnósticos preventivos de anomalias estatísticas. 
>
> * 📁 **Reports:** [`reports/observability/*`](reports/observability/) - Centraliza as evidências de integridade física (`integrity`), diagnósticos estatísticos (`profiling`) e relatórios de contratos de dados (`quality`).


### ✅ Data Quality (*Data Contracts*)
> 📁 [`docs/data_quality/*`](docs/data_quality/)  
> **Especifica** os contratos de dados e regras de negócio detalhadas para cada tabela nas camadas Bronze e Silver. **Define** critérios de integridade, servindo como a documentação técnica que orienta as validações programáticas via Pandera.
>
> * 📁 **Reports:** [`reports/observability/quality/*`](reports/observability/quality/) - Evidências de validação de contratos e conformidade de schemas.