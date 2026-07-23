![header](docs/images/main/header_main.png)

## 🏆 Resultados & Destaques

<div style="display: flex; gap: 10px; align-items: center;">
  <a href="https://drive.google.com/file/d/1fkRzZ8OR5SYczzmBmLq7r0Wg7lajzqf0/view?usp=sharing">
        <img src="docs/images/main/hackathon-pod.png" width="100" alt="Selo Hackathon Pod">
  </a>
  <a href="https://drive.google.com/file/d/19crkCafWzhxnG6tdUh8jsb4D2X1Px2fZ/view?usp=sharing">
        <img src="docs/images/main/hackathon-pod-skills.png" width="100" alt="Selo Skills">
  </a>
</div>

---

Repositório de desenvolvimento, documentação e implementação técnica de solução integrada de dados para o Hackathon da Pod Academy - Squad 3. 

> Este repositório centraliza a engine de processamento, a implementação da arquitetura medalhão e a aplicação de governança ativa através de contratos de dados e observabilidade nativa.

---

### 🔗 Ecossistema Squad 3

* **Repositório 1 de 2 (Core):** [hackathon-pod-squad3-core](https://github.com/rafa-trindade/hackathon-pod-squad3-core) - _Engine de processamento, arquitetura medalhão e gestão de performance com governança de dados nativa._
* **Repositório 2 de 2 (Ops):** [hackathon-pod-squad3-ops](https://github.com/rafa-trindade/hackathon-pod-squad3-ops) - _Infraestrutura como código (IaC), orquestração de pipelines e estratégias de Cloud Readiness._

> 🔐 O Core define **o que** a arquitetura executa.  
> ⚙️ O Ops define **como e onde** ela é executada.

---

### 🔄 O Ciclo de Vida: Do *Core* ao *Ops*

A arquitetura separa a **engine de processamento** da **sustentação de infraestrutura**, aplicando estratégias de **Cloud Readiness** para garantir escalabilidade, governança nativa e alta disponibilidade:

> **Fase 1 (Core):**
> * **🧠 A Engine de Processamento:** Responsável pela lógica de negócio e transformação. Atua como o **Worker** que executa a arquitetura Medallion e garante a integridade dos dados através de processamento vetorial (DuckDB). É o motor de execução agnóstico à infraestrutura, onde residem os contratos de dados e as regras de qualidade.

---

> **Fase 2 (Ops):**
>* **🏗️ O Provisionamento (IaC):** O Ops entra em cena via **Terraform**, erguendo uma infraestrutura segura e resiliente na **OCI**. Através de **Instance Principals**, a VM ganha identidade própria, eliminando a necessidade de gerenciar chaves manuais e garantindo acesso nativo e seguro ao Object Storage.
>* **⚡ A Integração & Bootstrap:** No momento do deploy, o Ops realiza o bootstrap automatizado utilizando **Docker Compose**. O Airflow assume a responsabilidade de sincronizar os repositórios, enquanto o **Core é montado como um volume persistente dentro dos containers (Workers)**. Isso funde a lógica de negócio à capacidade de escala da nuvem, permitindo atualizações de inteligência e transformações sem a necessidade de redeploy da infraestrutura.
>* **🎼 A Orquestração (Airflow):** O **Apache Airflow** assume o papel de maestro. Ele gerencia as DAGs que executam desde a ingestão (Bridge para OCI Object Storage) até o acionamento dos módulos do Core para transformar dados brutos em insights na camada Gold, fechando o ciclo de entrega de ponta a ponta.
>
> ---
>
> 💡 **Nota de Decisão Arquitetural (Cloud Readiness):** 
> Embora a OCI ofereça serviços gerenciados como *OCI Container Instances* e *OKE (Kubernetes)*, optamos estrategicamente pela execução via **Docker Compose dentro de OCI Compute**. Esta decisão foi tomada para garantir a **Portabilidade Total (Cloud Readiness)**: a solução não possui "lock-in" com serviços proprietários de orquestração da nuvem, permitindo que todo o ecossistema (Airflow + Workers + Ingestão) seja migrado para qualquer provedor Cloud ou ambiente On-premises apenas movendo o arquivo de composição, mantendo a simplicidade operacional sem sacrificar o isolamento de processos.

---

## 📖 Navegação Técnica (Documentação e Artefatos)

### 📅 Gestão e Planejamento do Projeto
> 📁 [`docs/project_plan/*`](docs/project_plan/)  
> **Consolida** a visão estratégica e operacional do projeto, integrando o contexto de negócio, objetivos e plano de trabalho da Squad. **Define** o cronograma de entregas, as métricas de sucesso e as responsabilidades de cada frente sob uma abordagem híbrida de governança e agilidade.
>
> * 🚦 **GitHub Projects:** [`squad3-analytics`](https://github.com/users/rafa-trindade/projects/6) | [`squad3-engineering-core`](https://github.com/users/rafa-trindade/projects/4) | [`squad3-engineering-ops`](https://github.com/users/rafa-trindade/projects/8)
> * 📑 **Documentação:** [`Entendimento`](docs/project_plan/01-entendimento-problema.md) | [`Abordagem`](docs/project_plan/02-abordagem-tecnica.md) | [`Plano de Trabalho`](docs/project_plan/03-plano-trabalho.md) | [`Cronograma`](docs/project_plan/04-cronograma.md) | [`Riscos`](docs/project_plan/05-riscos-dependencias.md) | [`Métricas`](docs/project_plan/06-metricas-sucesso.md)

---

### 🏗️ Data Architecture
> 📁 [`docs/data_architecture/*`](docs/data_architecture/)  
> **Define** uma stack **Cloud-Ready** orquestrada em ambiente VPS via **Docker** e **Airflow**. **Implementa** MinIO para storage Medallion (S3-API), DuckDB para processamento vetorial e PostgreSQL para o Data Warehouse. **Garante** a entrega de valor via **Modelos (.pkl)** versionados e relatórios analíticos, com suporte a **DataViz (Streamlit)** e estratégia de migração nativa para **OCI**.
>
> * 📑 **Documentação:** [`Arquitetura Técnica (Macro & Micro)`](docs/data_architecture/README.md) | [`Estratégia de Migração (VPS → OCI)`](docs/data_architecture/oci-cloud-ready-strategy.md)

---

### 🏛️ Data Governance
> 📁 [`docs/data_governance/`](docs/data_governance/)  
> **Define** as políticas estruturais para um Data Lake confiável. **Aplica** *Policy as Code* para assegurar a reprocessabilidade total via imutabilidade por execução (`run_id`) e eficiência através de particionamento físico otimizado (`ano_mes`).
>
> * 📑 **Políticas:** [`Retenção`](docs/data_governance/politica-retencao.md) | [`Particionamento`](docs/data_governance/politica-particionamento.md) | [`Qualidade`](docs/data_governance/politica-qualidade.md)

---

### 🧬 Data Lineage
> 📁 [`docs/data_lineage/*`](docs/data_lineage/)  
> Mapeia a jornada completa dos dados sob a arquitetura **Medallion**, garantindo rastreabilidade técnica e governança temporal. A linhagem é validada através de auditorias de integridade e densidade de atributos, culminando na homologação das estratégias de **Expansão (Amplitude)** e **Controle (Densidade)** na camada Gold.
>
> * 📑 **Documentação Principal:** [`Estratégia de Pré-processamento e Baseline (Master Lineage)`](docs/data_lineage/README.md)
> * 📁 **Fluxo de Refino:** [`Refino Técnico (Bronze → Silver)`](docs/data_lineage/bronze_silver/)
> * 📁 **Estratégia Gold:** [`Amplitude e Densidade (Silver → Gold)`](docs/data_lineage/gold/)

---

### 📖 Data Dictionary
> 📁 [`docs/data_dictionary/*`](docs/data_dictionary/)  
> 📖 **Dicionário de Dados (Silver):** Guia de referência das tabelas após os processos de **curadoria, higienização e agregação** de atributos. Consolida a definição das variáveis, garantindo a compreensão clara do grão, das tipagens e da semântica técnica e de negócio de cada entidade.
>
> * 📑 **Dicionários:** [`Atraso`](docs/data_dictionary/atraso-dict.md) | [`Pagamento`](docs/data_dictionary/pagamento-dict.md) | [`Recarga`](docs/data_dictionary/recarga-dict.md) | [`Cadastro`](docs/data_dictionary/dados_cadastrais-dict.md) | [`Telco`](docs/data_dictionary/telco-dict.md) | [`Bureau`](docs/data_dictionary/score_bureau_movel-dict.md)


---

### 🧠 Feature Store & Book de Variáveis
> 📁 [`docs/data_modelling/*`](docs/data_modelling/)  
> **Apresenta** a documentação técnica da Camada Gold. **Consolida** os dicionários de dados organizados por domínios, servindo como o guia oficial para o treinamento e consumo de modelos de Machine Learning.
>
> * 📑 **Books de Variáveis:** [`Target (Labels)`](docs/data_modelling/target/) | [`Features`](docs/data_modelling/features/)

---

### 📊 Analytics & Statistical Modeling
> 📁 [`notebooks/*`](notebooks/) | 📁 [`models/*.pkl`](models/)  
> **Integra e Documenta** o ciclo de inteligência analítica desde a exploração até a modelagem. **Diagnostica** o perfil de risco do público-alvo e **materializa** algoritmos de Credit Scoring através de artefatos serializados (**`.pkl`**), provendo suporte técnico e estatístico para as decisões estratégicas de negócio.
>
> * 📑 **Estudo Público Alvo (EDA):** [`01_estudo_publico_alvo_cmv.ipynb`](notebooks/eda/01_estudo_publico_alvo_cmv.ipynb)
> * 📑 **Modelagem & Baseline Scorecard:** [`02_modelo_baseline_behavior.ipynb`](notebooks/modeling/02_modelo_baseline_behavior.ipynb)
> * 📦 **Model Registry (Artefatos):** [`behavior_baseline_woe_v1.pkl`](models/behavior_baseline_woe_v1.pkl) | [`behavior_baseline_simple_v1.pkl`](models/behavior_baseline_simple_v1.pkl)


---

### 🔍 Data Observability
> 📁 [`docs/data_observability/`](docs/data_observability/)  
> **Materializa** a observabilidade através de artefatos gerados em tempo de execução. Garante a governança e transparência do pipeline, mantendo registros históricos de integridade, qualidade e diagnósticos estatísticos para auditoria técnica.
>
> * 🌐 [`Painel de Observabilidade (Streamlit)`](http://137.131.205.67:8501/) - _Interface interativa para monitoramento de saúde dos dados e execução do pipeline em tempo real._
> * 📁 [`Relatórios de Observabilidade`](reports/observability/) - Centraliza as evidências de integridade física (`integrity`), diagnósticos estatísticos (`profiling`), relatórios de contratos de dados (`quality`) e análise de público (`eda`).

---

### ✅ Data Quality
> 📁 [`docs/data_quality/*`](docs/data_quality/)  
> **Especifica** os contratos de dados e regras de negócio detalhadas para cada tabela nas camadas Raw e Gold. **Define** critérios de integridade, servindo como a documentação técnica que orienta as validações.
>
> * 📑 [`Política de Qualidade`](docs/data_governance/politica-qualidade.md) - Diretrizes gerais e dimensões de qualidade.
> * 📁 [`Relatórios de Qualidade`](reports/observability/quality/) - Evidências de conformidade de schemas e logs de auditoria das pipelines.

---

### ⚙️ Setup e Reprodução da Solução
> 📁 [`docs/guides/*`](docs/guides/)  
> **Descreve** os protocolos para configuração do ambiente e reprodução integral da solução. **Define** os requisitos de infraestrutura necessários para o processamento vetorizado no DuckDB e **detalha** os passos para acionamento do orquestrador, garantindo a persistência dos logs e a sincronização automática da observabilidade com o Data Lake.
>
> * 📑 **Guia:** [`Guia de Execução da Pipeline`](docs/guides/pipeline_execution.md)