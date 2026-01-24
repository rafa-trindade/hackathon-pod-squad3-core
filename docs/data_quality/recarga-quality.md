# 📲 Qualidade de Dados: Tabela Recarga

## 1. Validação de Entrada (RAW)
* **Contrato:** `RawRecarga` (24 colunas)
* **O que testa:** Estrutura e nomes das 24 colunas originais via Pandera.

## 2. Validação Dimensão e Saneamento (BRONZE/SILVER)
* **O que testa:** 
    * **Integridade:** Órfãos em 11 dimensões técnicas (Canais, Instituições, etc).
    * **Pareamento:** Tradução de 11 chaves para descrições amigáveis (Check de 'Não Informados').

## 3. Qualidade e Agregação (GOLD)
* **Estratégia:** Provedora de Features (Enriquecimento)
* **O que testa:** 
    * **Métricas:** Volumetria, cardinalidade e unicidade no grão da ABT final.
    * **Agregação:** Agregação de comportamento de recarga.

---

### **Repositório Histórico (Data Lake)**
Todas as evidências acima, incluindo o **Master Pipeline Log** (registro técnico consolidado da execução), são persistidas no S3 de forma versionada para fins de rastreabilidade:
> `s3://lake/observability/reports/run_id={run_id}/`