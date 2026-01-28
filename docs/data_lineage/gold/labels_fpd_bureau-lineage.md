## 📉 Visão Geral - `labels_fpd_bureau` (Gold Layer)

- **Entidade Principal:** Target de Modelagem de Expansão (Amplitude de Público)
- **Grão da Tabela (Unicidade):** `num_cpf, safra, prod`
- **Âncora de Seleção:** `silver/score_bureau_movel` (Foco em **Amplitude de Público**)
- **Chave de Particionamento:** `ano_mes` (Derivado da `safra`)

---

## 🎯 Estratégia de Seleção de Target (Âncora CMV)

Seguindo as recomendações da avaliação técnica, a âncora desta tabela foi migrada para a base de Bureau. Esta decisão visa eliminar distorções métricas causadas por produtos residenciais (NET/DTH) e focar no ecossistema onde o produto CMV é o único protagonista.

### 1. Estudo de Cobertura de Público-Alvo

#### 🔍 Análise Base Âncora: `score_bureau_movel`
- **Público Mandatório:** Clientes com Score de Bureau Móvel (CMV)
- **Total de CPFs únicos:** `2.565.985` (Execução 20260127)

| Comparado com         | Match %   | CPFs Encontrados   | Observação Técnica |
|:---------------------|:----------|:-------------------|:-------------------|
| `telco`              | 100.00%   | 2.565.985          | Cruzamento Integral |
| `dados_cadastrais`   | 100.00%   | 2.565.985          | Qualificação Cadastral |
| `recarga`            | 90.68%    | 2.326.835          | Densidade Transacional |
| `atraso`             | 77.11%    | 1.978.631          | Histórico de Risco |
| `pagamento`          | 71.84%    | 1.843.403          | Comportamento de Fatura |

---

### 🏆 Veredito Técnico: Transição para Âncora Bureau (Ativo de Expansão)

A transição para a base **BUREAU** é uma decisão de resposta da arquitetura para garantir a **Amplitude de Público** necessária para prospecção, mantendo o foco exclusivo no produto **CMV**.

**Justificativa Estratégica:**
1. **Amplitude de Público:** Elevamos a cardinalidade para **2.5M**, permitindo que o modelo aprenda padrões de mercado aberto.
2. **Isolamento de Risco:** Ao consumir o target da `silver/score_bureau_movel`, eliminamos o ruído estatístico de produtos residenciais (NET/DTH), estabilizando o FPD em **21.2%**.
3. **Fidelidade Nativa:** 100% de aderência ao público elegível pela solução de crédito móvel.

**📊 Comparativo de Estratégia:**

| Critério | Estratégia Antiga (Telco) | Estratégia Atual (CMV/Bureau) |
| :--- | :--- | :--- |
| **Foco de Público** | Amplo (Residencial + Móvel) | **Específico (Somente Móvel)** |
| **Aderência ao Bureau** | Indireta | **Nativa (100%)** |
| **Distorção de Métricas**| Risco Alto | **Mínimo / Controlado** |

---

## ✅ Data Lineage - `labels_fpd_bureau`

### 1. Visão Geral

| Item            | Valor                                 |
|-----------------|---------------------------------------|
| Origem Primária | `silver/score_bureau_movel`           |
| Origem Auxiliar | `silver/telco` (p/ flag_instalacao)   |
| Versionamento   | `run_id` (Isolamento de Execução)     |
| Particionamento | `ano_mes` (Coluna Técnica)            |

### 2. Fluxo de Transformação: SILVER → GOLD (TARGET BUREAU)

**Origem:** `s3://lake/silver/score_bureau_movel/**/*.parquet`  
**Destino:** `s3://lake/gold/labels_fpd_bureau/run_id={run_id}/ano_mes={YYYYMM}/*.parquet`

| Etapa | Processo | Descrição | Ações / Regras |
|------:|:---------|:----------|:---------------|
| 1 | **Fixação de Âncora** | Filtro de Público CMV | Seleção exclusiva de CPFs presentes na base de Bureau Móvel. |
| 2 | **Join Point-in-Time**| Enriquecimento Telco | Captura da `flag_instalacao` da base Telco Silver respeitando a safra. |
| 3 | **Saneamento Target** | Validação de `fpd` | Exclusão de registros com label de FPD nula ou inconsistente. |
| 4 | **Deduplicação** | Unicidade no Grão | `ROW_NUMBER` por `num_cpf, safra, prod` para garantir zero duplicatas. |
| 5 | **Auditoria** | Health Check | Emissão de relatório de volumetria e match percentual. |

---

### 3. Protocolo de Data Quality (Público CMV)

#### 📄 Evidência de Execução (Quality Report)
O log abaixo reflete a validação da volumetria expandida para o público CMV.

```text
📋 QUALITY REPORT - labels_fpd_bureau | RUN: 20260127_145520
----------------------------------------------------------------------------------
TESTE                         | STATUS     | OBSERVAÇÃO
----------------------------------------------------------------------------------
Unicidade no Grão             | PASS       | 0 duplicatas
Missing FPD Gold = 0          | PASS       | 0 nulos
----------------------------------------------------------------------------------
Distribuição Safra 202410     | PASS       | 16.2%
Distribuição Safra 202411     | PASS       | 17.3%
Distribuição Safra 202412     | PASS       | 16.9%
Distribuição Safra 202501     | PASS       | 17.2%
Distribuição Safra 202502     | PASS       | 15.9%
Distribuição Safra 202503     | PASS       | 16.6%
----------------------------------------------------------------------------------
Overlap dados_cadastrais      | PASS       | 100.00% de match
Overlap score_bureau_movel    | PASS       | 100.00% de match
Overlap atraso                | PASS       | 77.11% de match
Overlap Pagamento             | PASS       | 71.84% de match
Overlap Recarga               | PASS       | 90.68% de match
----------------------------------------------------------------------------------
Saneamento (Missing)          | INFO       | Descartados 1,161,410 registros (30.60%)
----------------------------------------------------------------------------------
```
> 🔗 **Acesse o log de auditoria:** [gold-labels_fpd_bureau-quality.log](../../../reports/observability/quality/pipeline/gold-labels_fpd_bureau-quality.log)

---

### 💡 Notas de Auditoria Técnica

1. **Expansão de Volumetria:** A migração para a âncora de Bureau consolidou a **Amplitude de Público** em **2.5M de CPFs**, garantindo significância estatística para cenários de novos clientes.
2. **Qualidade do Overlap:** O aumento do match de Pagamento (**71.84%**) e Atraso (**77.11%**) em relação à base Telco original sugere que o público que possui Score de Bureau é financeiramente mais ativo no ecossistema.
3. **Eficiência do Saneamento:** O descarte de **30.60%** dos registros na Etapa 1 refere-se a CPFs que não possuíam a label de FPD calculada ou que pertenciam a safras fora do período de observação homologado.
