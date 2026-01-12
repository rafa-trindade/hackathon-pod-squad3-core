# 📋 Plano de Trabalho: Divisão de Tarefas e Responsabilidades

Este documento detalha a metodologia de gestão do projeto e a distribuição de responsabilidades entre os membros da Squad, visando garantir agilidade, governança e entregas incrementais na Prova de Conceito (PoC).


## ⚡ Agilidade e Planejamento

### Metodologia Híbrida
O planejamento do projeto foi estruturado combinando as boas práticas do **PMBOK** (garantindo governança, controle de escopo, riscos e custos) com **Metodologias Ágeis**, priorizando entregas incrementais e adaptação contínua. Esta abordagem permite o controle rigoroso de prazos e recursos em paralelo com a flexibilidade para pivotar estratégias de processamento conforme a análise dos dados.

---

### Gestão do Fluxo (Kanban)
A gestão das atividades é realizada por meio de quadros Kanban no **GitHub Projects**, integrando planejamento, execução e versionamento em um único ecossistema. Para garantir a especialização técnica e a fluidez das entregas, dividimos a gestão em dois projetos distintos:

* **Data & Analytics - Squad 3:** Focado no ciclo de vida da ciência de dados e modelos de ML.
* **Data Engineering - Squad 3:** Focado na infraestrutura de processamento, orquestração e sustentação do Data Lake.

O uso desses quadros possibilita:
* Controle visual detalhado das tarefas (*To Do, In Progress, Done*).
* Monitoramento preciso de **Milestones do Projeto**, como a finalização de camadas específicas ou deploy de modelos.
* Identificação de dependências críticas entre engenharia e analytics.

---

![Quadro GitHub Projects](../images/project.png)


## 👥 Organização da Squad e Responsabilidades

A equipe é composta por 10 especialistas, organizados em frentes de trabalho com entregáveis claros para as bancas de qualificação e final.

### ⚙️ Engenharia de Dados (Data Engineering)
* **Foco:** Construção e manutenção da infraestrutura de dados.
* **Responsabilidades:** Ingestão de dados no **MinIO**, desenvolvimento de pipelines com **DuckDB**, orquestração via **Airflow** e implementação de políticas de retenção e particionamento.
* **Interfaces Críticas:** Garante a consistência de chaves, temporalidade, disponibilidade e estabilidade das tabelas para as frentes de Analytics e Data Science.

---

### 🧠 Ciência de Dados (Data Science)
* **Foco:** Inteligência de dados e modelagem preditiva.
* **Responsabilidades:** 
    * Definição formal do target, janelas (feature/performance) e validação temporal.
    * Especificação e construção da **ABT (Analytical Base Table)**.
    * Baseline e evolução até o modelo final (.pkl) com pipeline reprodutível.
    * Tradução de métricas em decisão operacional (faixas, corte e simulações).
    * Plano de monitoramento (performance, drift e gatilhos de retraining).
* **Entregáveis:** Modelo Baseline (Banca de Qualificação), Modelo Final e Plano de Monitoramento (Banca Final).

---

### 📈 Análise de Dados (Analytics)
* **Foco:** Tradução de dados em insights de negócio e Storytelling.
* **Responsabilidades:** 
    * Estudo de Público-Alvo: perfil, segmentações, qualidade, outliers e vieses.
    * Definição das métricas de sucesso (técnicas e de negócio).
    * Liderança dos **Books de Variáveis** (significado, regra e interpretação).
    * Storytelling e consolidação de impacto com insights acionáveis por faixa.
* **Entregáveis:** Estudo de Público-Alvo (Qualificação), Books de Variáveis (coautoria) e seções de métricas, riscos e governança.

---

### 🏛️ Documentação e Governança
* **Foco:** Manutenção do conhecimento, conformidade técnica e narrativa.
* **Responsabilidades:** 
    * Mapeamento de Lineage e documentação técnica (Profiling/Dicionário).
    * Garantia da aplicação das políticas de governança via código.
    * Padronização de narrativa e consistência dos materiais para as bancas.
* **Interfaces Críticas:** Apoio na redação técnica e consistência entre o que é processado e o que é documentado.


## 🔗 Interfaces e Dependências
Para o sucesso da PoC, estabelecemos protocolos de colaboração entre as frentes:

> **Engenharia ↔️ Documentação:** Sincronização técnica para o mapeamento de metadados, linhagem e políticas de governança. A Engenharia produz sua própria documentação garantindo que a documentação central reflita com precisão o que foi implementado via código.  
> **Engenharia ↔️ Science/Analytics:** Alinhamento sobre janelas temporais e regras de reprocessamento para garantir que a ABT (Analytical Base Table) reflita a realidade dos dados na camada Silver.  
> **Science ↔️ Documentação:** Padronização das métricas e lógicas de variáveis nos Books de Variáveis para garantir a auditabilidade dos experimentos e resultados.  
> **Analytics ↔️ Squad:** Consolidação dos resultados técnicos em uma storyline executiva e visual para a apresentação final estratégica.