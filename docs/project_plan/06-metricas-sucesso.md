# 📊 Métricas de Sucesso e Avaliação

Este documento define os indicadores técnicos e de negócio utilizados para validar a eficácia do modelo de propensão e a saúde operacional da plataforma de dados.

---

## ⚙️ Métricas Técnicas (Model Performance)
Para garantir a capacidade preditiva e a estabilidade do modelo de Inadimplência, monitoramos:

* **Poder Discriminante** - ROC-AUC e KS/Gini para avaliar a separação entre "bons" e "maus" pagadores.
* **Ordenação de Risco** - Lift por faixa, garantindo que as faixas de maior score concentrem a maior taxa de inadimplência.
* **Estabilidade** - Monitoramento por safra para validar se o comportamento do modelo se mantém consistente ao longo do tempo.

---

## 💼 Métricas de Negócio (Business Impact)
Indicadores que traduzem a performance técnica em valor para a Claro:

* **Qualidade de Risco** - Inadimplência esperada por faixa de score.
* **Cobertura** - Percentual da massa elegível (clientes pré-pagos) mapeada pelo modelo.
* **Eficiência de Política** - Simulações de política de corte (ex: análise de impacto ao aprovar o Top X% de menor risco).

---

## 🛠️ Métricas de Plataforma (Data Health)
*Métricas geradas como subproduto da arquitetura de engenharia, governança e observabilidade:*

* **Observabilidade** - Monitoramento de **Freshness** (atualização), **Volume** e **Schema Drift**.
* **Qualidade** - Integridade técnica (**tipagem forte**) e semântica via **Pandera**.
* **Resiliência** - Disponibilidade de estados anteriores via **Versionamento de Execuções (`run_id`)**.
* **Eficiência de Custos** - Gestão do storage na VPS através da **Política de Retenção**.
* **Rastreabilidade** - Integridade da jornada do dado entre as camadas Medallion (**Data Lineage**).