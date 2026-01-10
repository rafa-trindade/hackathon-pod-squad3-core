# 📋 Plano de Trabalho: Divisão de Tarefas e Responsabilidades

Este documento detalha a metodologia de gestão do projeto e a distribuição de responsabilidades entre os membros da Squad, visando garantir agilidade, governança e entregas incrementais na Prova de Conceito (PoC).

---

## Agilidade e Planejamento

### Metodologia Híbrida
O planejamento do projeto foi estruturado combinando as boas práticas do **PMBOK** (garantindo governança, controle de escopo, riscos e custos) com **Metodologias Ágeis**, priorizando entregas incrementais e adaptação contínua.

Essa abordagem híbrida permite:
* **Controle Executivo:** Gestão rigorosa de prazos e recursos.
* **Flexibilidade Técnica:** Capacidade de pivotar estratégias de processamento conforme a análise dos dados.

### Gestão do Fluxo (Kanban)
A gestão das atividades é realizada por meio de um **Quadro Kanban**, utilizado para organizar o fluxo de trabalho desde a concepção até a implementação final. O quadro foi implementado utilizando o **GitHub Projects**, integrando planejamento, execução e versionamento do código.

O Kanban possibilita:
* Controle visual das tarefas (*To Do, In Progress, Done*).
* Monitoramento dos **Milestones do Projeto** (ex: Finalização da camada Silver).

![Quadro GitHub Projects](../images/project.png)

---

## 👥 Organização da Squad e Responsabilidades

A equipe é composta por 10 especialistas, organizados para garantir a fluidez do dado desde a origem até o consumo final.

### ⚙️ Engenharia de Dados (3 Membros)
* **Foco:** Construção e manutenção da infraestrutura de dados.
* **Responsabilidades:** Ingestão de dados no **MinIO**, desenvolvimento de pipelines no **DuckDB**, orquestração via **Airflow** e implementação de políticas de retenção e particionamento.

### 🧠 Ciência de Dados (3 Membros)
* **Foco:** Inteligência de dados e modelagem preditiva.
* **Responsabilidades:** Feature Engineering na camada Gold, treinamento de modelos, versionamento de experimentos via **MLflow** e entrega de arquivos de produção (`.pkl`).

### 📈 Análise de Dados (2 Membros)
* **Foco:** Tradução de dados em insights de negócio.
* **Responsabilidades:** Criação de dashboards interativos via **Streamlit**, exploração de dados (EDA) e validação dos modelos lógicos no **PostgreSQL/dbt**.

### 📝 Documentação e Governança (2 Membros)
* **Foco:** Manutenção do conhecimento e conformidade.
* **Responsabilidades:** Mapeamento de Lineage, documentação técnica (Profiling/Data Dictionary), gestão da Wiki do projeto e garantia de que as políticas de governança estão sendo aplicadas via código.