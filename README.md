## 🚀 Hackathon Pod Academy - Squad 3

Repositório de desenvolvimento, documentação e implementação da solução integrada de dados para o Hackathon da Pod Academy - Squad 3.

## 📚 Mapeamento de Documentação (*Project Hub*)

### 📅 Gestão e Planejamento do Projeto
> 📁 [`docs/project_plan/*`](docs/project_plan/)  
> **Consolida** a visão estratégica e operacional do projeto, integrando o contexto de negócio, objetivos e plano de trabalho da Squad. **Define** o cronograma de entregas, as métricas de sucesso e as responsabilidades de cada frente sob uma abordagem híbrida de governança e agilidade.
>
> * 📑 **Documents:** [`Entendimento`](docs/project_plan/01-entendimento-problema.md) | [`Abordagem`](docs/project_plan/02-abordagem-tecnica.md) | [`Plano de Trabalho`](docs/project_plan/03-plano-trabalho.md) | [`Cronograma`](docs/project_plan/04-cronograma.md) | [`Riscos`](docs/project_plan/05-riscos-dependencias.md) | [`Métricas`](docs/project_plan/06-metricas-sucesso.md)

---

### 🏗️ Data Architecture
> 📄 [`docs/data_architecture/`](docs/data_architecture/README.md)  
> **Define** a stack operada em VPS, utilizando Docker e Airflow para orquestração. **Combina** MinIO para storage Medallion (Cloud-Ready), DuckDB para processamento vetorial e PostgreSQL para o Data Warehouse, integrando modelagem via dbt, gestão de modelos com MLflow e entrega via Streamlit.

---

### 🏛️ Data Governance
> 📄 [`docs/data_governance/`](docs/data_governance/README.md)  
> **Define** as políticas e diretrizes estruturais que garantem um Data Lake confiável e de baixo custo operacional. **Aplica** o conceito de *Policy as Code* para assegurar a reprocessabilidade total através de imutabilidade por execução (`run_id`) e eficiência via particionamento otimizado.
>
> * 📑 **Policies:** [`Retention`](docs/data_governance/politica-retencao.md) | [`Partitioning`](docs/data_governance/politica-particionamento.md) | [`Quality`](docs/data_governance/politica-qualidade.md)

---

### 🧬 Data Lineage
> 📁 [`docs/data_lineage/*`](docs/data_lineage/)  
> **Mapeia** a jornada do dado entre as camadas Medallion. **Garante** a rastreabilidade ponta a ponta, desde a ingestão técnica até a homologação das tabelas âncoras para modelagem na camada Gold.
>
> * 📑 **Lineage:** [`Raw -> Silver`](docs/data_lineage/) | [`Gold (Target & Features)`](docs/data_lineage/gold/)
> * 📑 **Reports:** [`Integrity`](reports/observability/integrity/) | [`Profiling`](reports/observability/profiling/)

---

### 🧠 Feature Store & Book de Variáveis
> 📁 [`docs/data_modelling/*`](docs/data_modelling/)  
> **Apresenta** a documentação técnica da Camada Gold. **Consolida** os dicionários de dados organizados por domínios, servindo como o guia oficial para o treinamento e consumo de modelos de Machine Learning.
>
> * 📑 **Books:** [`Target (Labels)`](docs/data_modelling/target/) | [`Feature Dictionary`](docs/data_modelling/features/)

---

### 🔍 Data Observability
> 📄 [`docs/data_observability/`](docs/data_observability/README.md)  
> **Gerencia** a saúde dos fluxos de dados através do monitoramento de *Freshness*, *Volume* e *Distribution*. **Garante** resiliência operacional através de protocolos de *Health Check* de safras e auditoria de *Overlap* para assegurar a riqueza de informação para Machine Learning.
>
> * 📁 [`Observability Reports`](reports/observability/) - Centraliza as evidências de integridade física (`integrity`), diagnósticos estatísticos (`profiling`) e relatórios de contratos de dados (`quality`).

---

### ✅ Data Quality (*Data Contracts*)
> 📁 [`docs/data_quality/*`](docs/data_quality/)  
> **Especifica** os contratos de dados e regras de negócio detalhadas para cada tabela nas camadas Bronze e Silver. **Define** critérios de integridade, servindo como a documentação técnica que orienta as validações programáticas via Pandera.
>
> * 📑 [`Quality Policy`](docs/data_governance/politica-qualidade.md) - Diretrizes gerais e dimensões de qualidade.
> * 📁 [`Quality Reports`](reports/observability/quality/) - Evidências de conformidade de schemas e logs de auditoria das pipelines.