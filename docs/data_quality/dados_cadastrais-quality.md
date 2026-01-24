# 👤 Qualidade de Dados: Tabela Dados Cadastrais

## 1. Validação de Entrada (RAW)
* **Contrato:** `raw_dados_cadastrais_schema` (33 colunas)
* **O que testa:** Estrutura fixa e range dinâmico (`var_02` a `var_25`).

## 2. Qualidade e Agregação (GOLD)
* **Estratégia:** Provedora de Features (Enriquecimento)
* **O que testa:** 
    * **Métricas:** Volumetria, cardinalidade e unicidade no grão da ABT final.
    * **Persistência:** Disponibilidade de variáveis cadastrais para o treinamento do modelo.

### 🔍 Estudo de Cobertura
Embora possua o maior volume absoluto (`3.590.459` CPFs), a base cadastral foi descartada como âncora devido à baixa densidade de cobertura no ecossistema:

* **Estudo:** [Seleção de Target (Âncora)](../data_lineage/gold/labels_fpd-lineage.md)

---

### **Repositório Histórico (Data Lake)**
Todas as evidências acima, incluindo o **Master Pipeline Log** (registro técnico consolidado da execução), são persistidas no S3 de forma versionada para fins de rastreabilidade:
> `s3://lake/observability/reports/run_id={run_id}/`