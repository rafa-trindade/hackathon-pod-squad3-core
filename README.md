## 🚀 Hackathon Pod Academy - Squad 3

Repositório de desenvolvimento, documentação e implementação da solução integrada de dados para o Hackathon da Pod Academy - Squad 3.

## 📚 Mapeamento de Documentação (Project Hub)

### 📅 Project Plan & Management
> 📁 [`docs/project_plan/*`](docs/project_plan/)  
> O projeto segue uma abordagem híbrida, onde o planejamento é regido por diretrizes de governança com execução gerenciada por ritos ágeis. Toda a documentação é versionada, servindo como suporte para auditorias e futuras migrações para ambiente de cloud pública.


### 🏗️ Data Architecture
> 📄 [`docs/data_architecture/`](docs/data_architecture/README.md)  
> Definição da stack moderna operando em VPS, utilizando Docker e Airflow para orquestração. Combina MinIO para storage Medallion (Cloud-Ready), DuckDB para processamento vetorial e PostgreSQL para o Data Warehouse, integrando modelagem via dbt, gestão de modelos com MLflow e entrega via Streamlit.


### 🏛️ Data Governance
> 📄 [`docs/data_governance/`](docs/data_governance/README.md)  
> Framework de governança pragmática que consolida os pilares de Observabilidade, Profiling e Qualidade através de *Policy as Code*. Garante a resiliência do ecossistema mediante versionamento de execuções, políticas de retenção para rollback imediato e eficiência de custos via particionamento físico (FinOps), convertendo definições estratégicas em ativos de dados auditáveis e de alta confiabilidade.


### 🧬 Data Lineage
> 📁 [`docs/data_lineage/*`](docs/data_lineage/)  
> Mapeamento da jornada do dado entre as camadas Medallion, garantindo padronização, tipagem forte e integridade técnica na camada Silver. Foca na rastreabilidade ponta a ponta e na otimização de performance através de particionamento físico e saneamento de metadados.


### 🧠 Feature Store & Book de Variáveis
> 📁 [`docs/data_modelling/*`](docs/data_modelling/)  
> Documentação técnica da Camada Gold com foco em inteligência de dados e Machine Learning. Consolida o Book de Variáveis com definições de negócio e lógicas de agregação, além do registro de Feature Engineering para treinamento de modelos.


### 🔍 Data Observability
> 📄 [`docs/data_observability/`](docs/data_observability/README.md)  
> Gestão da saúde dos dados através do monitoramento nativo de Freshness, Volume e Schema Drift. Utiliza metadados técnicos para auditoria, garantindo resiliência operacional com protocolos de rollback e diagnósticos preventivos de anomalias estatísticas.


### 📊 Data Profiling
> 📁 [`docs/data_profiling/*`](docs/data_profiling/)  
> Diagnóstico estatístico automatizado para monitoramento da saúde dos dados, cobrindo volumetria (MiB vs. Registros), cardinalidade e distribuição de valores. Utiliza scripts híbridos para análise de integridade, gerando evidências versionadas em Markdown para suporte à auditoria.


### ✅ Data Quality
> 📁 [`docs/data_quality/*`](docs/data_quality/)  
> Governança de contratos e validação de dados através de verificações estruturais e semânticas nas camadas Raw (Ingestão) e Silver. Implementa regras de negócio, unicidade e integridade tipológica integradas de forma programática aos scripts de transformação com suporte do Pandera.