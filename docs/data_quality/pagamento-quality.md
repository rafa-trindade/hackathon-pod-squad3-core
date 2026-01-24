# 💳 Qualidade de Dados: Tabela Pagamento

## 1. Validação de Entrada (RAW)
* **Contrato:** `RawPagamento` (73 colunas)
* **O que testa:** Estrutura e nomes das 73 colunas originais via Pandera.

## 2. Qualidade e Agregação (GOLD)
* **Estratégia:** Provedora de Features (Enriquecimento)
* **O que testa:** 
    * **Métricas:** Volumetria, cardinalidade e unicidade no grão da ABT final.
    * **Agregação:** Agregação de comportamento de pagamento.

---

### **Repositório Histórico (Data Lake)**
Todas as evidências acima, incluindo o **Master Pipeline Log** (registro técnico consolidado da execução), são persistidas no S3 de forma versionada para fins de rastreabilidade:
> `s3://lake/observability/reports/run_id={run_id}/`