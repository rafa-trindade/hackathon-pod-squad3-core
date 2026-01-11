## 🚀 Hackathon Pod Academy - Squad 3

Repositório de desenvolvimento, documentação e implementação da solução integrada de dados para o Hackathon da Pod Academy - Squad 3.

## 📚 Mapeamento da Documentação

### 📅 Project Plan & Management
📁 [`docs/project_plan/*`](docs/project_plan/)

**Foco:** Planejamento Estratégico e Execução da PoC.
- **Entendimento do Problema:** Diagnóstico do desafio de negócio e objetivos centrais da solução.
- **Abordagem da Solução:** Definição das metodologias e estratégias para a viabilidade técnica da PoC.
- **Plano de Trabalho:** Distribuição de tarefas e responsabilidades entre os membros da Squad.
- **Cronograma Interno:** Mapeamento de etapas, marcos e prazos estimados para as entregas.
- **Riscos e Dependências:** Identificação de pontos críticos e planos de mitigação operacional.
- **Métricas de Sucesso:** Indicadores de performance para avaliação da qualidade e entrega de valor.

> O projeto segue uma abordagem híbrida, onde o planejamento é regido por diretrizes de governança e a execução diária é gerenciada por ritos ágeis. Toda a documentação é versionada, servindo como suporte para auditorias e futuras migrações para ambiente Cloud.

---

### 🏗️ Data Architecture
📄 [`docs/data_architecture/`](docs/data_architecture/README.md)

**Foco:** Infraestrutura e Stack Técnica.
- **Solução:** Desenho de arquitetura local e escalável com Docker, MinIO e DuckDB.
- **Engine:** Processamento analítico vetorizado com DuckDB e modelagem no PostgreSQL via dbt.
- **Qualidade:** Validação de schemas e contratos de dados na origem com Pandera.
- **Visualização:** Entrega de Data Apps analíticos integrados via Streamlit.

---

### 🏛️ Data Governance
📄 [`docs/data_governance/`](docs/data_governance/README.md)

**Foco:** Diretrizes, Políticas e Custos.
- **Retenção:** Gestão de ciclo de vida baseada em `run_id` (Rollback técnico).
- **Particionamento:** Estratégia de `ano_mes` para eficiência de processamento e custo.
- **Decisões:** Registro de escolhas arquiteturais aplicadas via código (Policy as Code).

---

### 🧬 Data Lineage
📁 [`docs/data_lineage/*`](docs/data_lineage/)

**Foco:** Rastreabilidade e Governança do Fluxo.
- **Rastreabilidade:** Mapeamento ponta a ponta da jornada do dado (Raw → Bronze → Silver → Gold).
- **Processamento Técnico:** Padronização de nomes, tipagem forte e enriquecimento de metadados na camada Bronze.
- **Integridade de Dados:** Deduplicação por grão técnico, tratamento de *hashes* inválidos e saneamento de chaves na Silver.
- **Otimização:** Particionamento físico por `ano_mes` e limpeza de colunas nulas para eficiência de custo e scan.

---

### 🧠 Feature Store & Book de Variáveis
📁 [`docs/data_modelling/*`](docs/data_modelling/)

**Foco:** Inteligência de Dados e Machine Learning (Camada Gold).
- **Book de Variáveis:** Documentação detalhada das variáveis preditivas, contendo definições de negócio, lógicas de agregação temporal e lógicas de cálculo.
- **Feature Engineering:** Registro das transformações construídas especificamente para o treinamento dos modelos.

---

### 🔍 Data Observability
📄 [`docs/data_observability/`](docs/data_observability/README.md)

**Foco:** Saúde e Confiabilidade da Ingestão ao Consumo.
- **Monitoramento:** Acompanhamento nativo de Freshness, Volume e Schema Drift sem ferramentas externas.
- **Previsibilidade:** Uso de metadados técnicos (`run_id`, `ingestion_ts`) para auditoria de atrasos e falhas.
- **Resiliência:** Protocolo de limpeza pós-sucesso e rollback imediato baseado na política de retenção.
- **Diagnóstico:** Identificação de anomalias estatísticas e desbalanceamento de partições via Profiling.

---

### 📊 Data Profiling
📁 [`docs/data_profiling/*`](docs/data_profiling/)

**Foco:** Diagnóstico Estatístico e Saúde dos Dados.
- **Relatórios:** Documentação automatizada de volumetria (MiB vs. Registros) e análise de Schema Drift.
- **Estatística:** Visão detalhada de cardinalidade, integridade de nulos e distribuição de valores (Top 10).
- **Método:** Execução via scripts híbridos (Python + Jupyter Notebook) com geração de evidências em Markdown versionadas para suporte à auditoria.

---

### ✅ Data Quality
📁 [`docs/data_quality/*`](docs/data_quality/)

**Foco:** Contratos e Validação.
- **Estrutural:** Tipagem e obrigatoriedade (Camada Bronze).
- **Semântico:** Regras de negócio, unicidade e elegibilidade (Camada Silver).
- **Execução:** Validações programáticas integradas aos scripts de transformação.