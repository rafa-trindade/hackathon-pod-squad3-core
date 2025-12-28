## 🏗️ squad3-data-engineering

Repositório de desenvolvimento e experimentação de engenharia de dados para o hackathon da Pod Academy - Squad 3 

## 👥 Time de Engenharia

- **Frederico da Costa dos Santos**
- **Rafael Araujo Trindade**
- **Ronaldo Theodoro**

## 📚 Mapeamento da Documentação

A documentação do projeto está organizada por **domínios clássicos de engenharia de dados**,
permitindo fácil navegação, auditoria e apresentação técnica.

### 🏗️ Data Architecture
📁 `docs/data_architecture/`

Descreve a arquitetura técnica do projeto em execução:
- Componentes da stack (MinIO, DuckDB, Airflow, Pandera, Docker)
- Papéis e responsabilidades de cada serviço
- Integração entre ingestão, processamento e armazenamento

---

### 📘 Data Dictionary
📁 `docs/data_dictionary/`

Define o significado, tipagem e uso das colunas por camada:
- Dicionário técnico e semântico
- Padronização de nomenclatura
- Suporte a contratos de dados

---

### 🏛️ Data Governance
📁 `docs/data_governance/`

Centraliza as políticas e diretrizes do projeto e mapeia como a solução atende,
na prática, aos pilares de **Data Governance**.
- Política de retenção baseada em execuções técnicas (`run_id`)
- Definição de contratos gerais de qualidade de dados
- Estratégias seguras de reprocessamento e rollback
- Suporte nativo à auditoria, observabilidade e controle de custos
- Governança aplicada via código e automação

---

### 🧬 Data Lineage
📁 `docs/data_lineage/`

Documenta a rastreabilidade ponta a ponta dos dados:
- Origem dos dados
- Transformações por camada (Raw → Bronze → Silver → Gold)
- Separação entre transformações técnicas e semânticas

---

### 🔍 Data Observability
📁 `docs/data_observability/`

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
📁 `docs/data_profiling/`

Apresenta análises exploratórias e estatísticas dos dados:
- Volume por camada
- Cardinalidade
- Distribuição de valores
- Percentual de nulos

Utilizado como base para qualidade e observabilidade.

---

### ✅ Data Quality
📁 `docs/data_quality/`

Documenta os **contratos de dados** do projeto:
- Regras estruturais (schema, tipos, obrigatoriedade)
- Regras semânticas (unicidade, elegibilidade, consistência)
- Validações aplicadas com Pandera

---

## 🎯 Princípios do Projeto

- Simplicidade operacional
- Governança pragmática
- Observabilidade nativa
- Reprocessamento como regra
- Engenharia orientada a dados, não a ferramentas