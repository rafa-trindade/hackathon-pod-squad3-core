# 📡 Qualidade de Dados: Tabela Telco

## 1. Validação de Entrada (RAW)
* **Contrato:** `raw_telco_schema` (74 colunas)
* **O que testa:** Estrutura fixa e range dinâmico (`var_26` a `var_93`).

## 2. Qualidade e Agregação (GOLD)
* **Estratégia:** **Âncora do Ecossistema Selecionada**
* **O que testa:** 
    * **Target Audit:** Unicidade e ausência de nulos na label `fpd`.
    * **Métricas:** Volumetria, cardinalidade e distribuição por safra.

### 🔍 Estudo de Cobertura
A base **TELCO** foi selecionada como a âncora do projeto por apresentar a maior densidade de informações cruzadas, garantindo maior poder preditivo (KS) para o modelo.

* **Estudo:** [Seleção de Target (Âncora)](../data_lineage/gold/labels_fpd-lineage.md)

---

### **Repositório Histórico (Data Lake)**
Todas as evidências acima, incluindo o **Master Pipeline Log** (registro técnico consolidado da execução), são persistidas no S3 de forma versionada para fins de rastreabilidade:
> `s3://lake/observability/reports/run_id={run_id}/`