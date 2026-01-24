# 📊 Qualidade de Dados: Tabela Score Bureau

## 1. Validação de Entrada (RAW)
* **Contrato:** `RawScore` (8 colunas)
* **O que testa:** Estrutura fixa das métricas de Score 01 e 02.

## 2. Qualidade e Agregação (GOLD)
* **Estratégia:** Fornecedora de Features (Não-Âncora)
* **O que testa:** 
    * **Métricas:** Volumetria, cardinalidade e unicidade no grão da ABT final.
    * **Persistência:** Disponibilidade de variáveis score para o treinamento do modelo.

### 🔍 Estudo de Cobertura
Acompanhando a base Cadastral, o Bureau foi mantido apenas como enriquecimento de features, sendo descartado como âncora pela baixa cobertura volumétrica frente aos dados de comportamento:

* **Estudo:** [Seleção de Target (Âncora)](../data_lineage/gold/labels_fpd-lineage.md)

---

### **Repositório Histórico (Data Lake)**
Todas as evidências acima, incluindo o **Master Pipeline Log** (registro técnico consolidado da execução), são persistidas no S3 de forma versionada para fins de rastreabilidade:
> `s3://lake/observability/reports/run_id={run_id}/`