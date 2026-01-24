# 📉 Qualidade de Dados: Tabela Atraso

## 1. Validação de Entrada (RAW)
* **Contrato:** `RawAtraso` (50 colunas)
* **O que testa:** Estrutura e nomes das 50 colunas originais via Pandera.

## 2. Validação Dimensão e Saneamento (BRONZE/SILVER)
* **O que testa:** 
    * **Integridade:** Órfãos na chave `dw_tipo_faturamento` (Check contra dimensão).
    * **Pareamento:** Tradução da chave para descrição `dsc_tipo_faturamento` (Check de 'Não Informados').

## 3. Qualidade e Agregação (GOLD)
* **Estratégia:** Provedora de Features (Enriquecimento)
* **O que testa:** 
    * **Métricas:** Volumetria, cardinalidade e unicidade no grão da ABT final.
    * **Agregação:** Agregação de comportamento de atraso.

---

### **Repositório Histórico (Data Lake)**
Todas as evidências acima, incluindo o **Master Pipeline Log** (registro técnico consolidado da execução), são persistidas no S3 de forma versionada para fins de rastreabilidade:
> `s3://lake/observability/reports/run_id={run_id}/`