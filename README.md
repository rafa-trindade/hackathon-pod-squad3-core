# 🏗️ Squad 3 - Data Engineering

Repositório de desenvolvimento e experimentação de engenharia de dados para o hackathon da Pod Academy - Squad 3 

## 👥 Time de Engenharia

- **Frederico da Costa dos Santos**
- **Rafael Araujo Trindade**
- **Ronaldo Theodoro**

## 📚 Mapeamento da Documentação

### 🏗️ Data Architecture
📄 [`docs/data_architecture/`](docs/data_architecture/README.md)

Descreve a arquitetura técnica do projeto em execução:
- Componentes da stack (MinIO, DuckDB, Airflow, Pandera, Docker)
- Papéis e responsabilidades de cada serviço
- Integração entre ingestão, processamento e armazenamento

---

### 📘 Data Dictionary
📁 [`docs/data_dictionary/*`](docs/data_dictionary/)

Define o significado, tipagem e uso das colunas por camada:
- Dicionário técnico e semântico
- Padronização de nomenclatura
- Suporte a contratos de dados

---

### 🏛️ Data Governance
📄 [`docs/data_governance/`](docs/data_governance/README.md)

Centraliza as políticas e diretrizes do projeto e mapeia como a solução atende,
na prática, aos pilares de **Data Governance**.
- Política de retenção baseada em execuções técnicas (`run_id`)
- Definição de contratos gerais de qualidade de dados
- Estratégias seguras de reprocessamento e rollback
- Suporte nativo à auditoria, observabilidade e controle de custos
- Governança aplicada via código e automação

---

### 🧬 Data Lineage
📁 [`docs/data_lineage/*`](docs/data_lineage)

Documenta a rastreabilidade ponta a ponta dos dados:
- Origem dos dados
- Transformações por camada (Raw → Bronze → Silver → Gold)
- Separação entre transformações técnicas e semânticas

---

### 🔍 Data Observability
📄 [`docs/data_observability/`](docs/data_observability/README.md)

Mapeia como o projeto atende aos pilares de Data Observability:
- Freshness
- Volume
- Schema
- Distribution
- Lineage
- Quality
- Reliability e Reprocessamento

A observabilidade emerge como resultado das decisões de arquitetura e governança.

---

### 📊 Data Profiling
📁 [`docs/data_profiling/*`](docs/data_profiling/)

Apresenta análises exploratórias e estatísticas dos dados:
- Volume por camada
- Cardinalidade
- Distribuição de valores
- Percentual de nulos

Utilizado como base para qualidade e observabilidade.

> **Observação:** O profiling foi gerado por meio de um **script utilitário de EDA híbrido (Python + Jupyter Notebook)**, combinando automação e análise exploratória assistida, com geração de relatórios versionados para suporte às decisões de qualidade e modelagem.

---

### ✅ Data Quality
📁 [`docs/data_quality/*`](docs/data_quality/)

Documenta os **contratos de dados** do projeto:
- Regras estruturais (schema, tipos, obrigatoriedade)
- Regras semânticas (unicidade, elegibilidade, consistência)
- Validações aplicadas com Pandera

