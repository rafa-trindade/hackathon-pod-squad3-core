# 🏛️ Relatório de Diagnóstico Integrado de Target

## 🚀 PARTE 1: TESTE DE COBERTURA DE ECOSSISTEMA (SILVER LAYER)

### 🔍 Análise Base Âncora: `TELCO`
- **Total de CPFs únicos na base:** `1.272.095`

| Comparado com        | Match %   | CPFs Encontrados   |
|:---------------------|:----------|:-------------------|
| `atraso`             | 74.74%    | 950.731            |
| `pagamento`          | 68.16%    | 867.035            |
| `recarga`            | 99.78%    | 1.269.268          |
| `score_bureau_movel` | 100.00%   | 1.272.095          |
| `dados_cadastrais`   | 100.00%   | 1.272.095          |

### 🔍 Análise Base Âncora: `DADOS_CADASTRAIS`
- **Total de CPFs únicos na base:** `3.590.459`

| Comparado com        | Match %   | CPFs Encontrados   |
|:---------------------|:----------|:-------------------|
| `atraso`             | 58.38%    | 2.095.944          |
| `pagamento`          | 53.77%    | 1.930.502          |
| `recarga`            | 85.72%    | 3.077.601          |
| `score_bureau_movel` | 35.43%    | 1.272.095          |
| `telco`              | 35.43%    | 1.272.095          |

### 🔍 Análise Base Âncora: `SCORE_BUREAU_MOVEL`
- **Total de CPFs únicos na base:** `1.272.095`

| Comparado com      | Match %   | CPFs Encontrados   |
|:-------------------|:----------|:-------------------|
| `atraso`           | 74.74%    | 950.731            |
| `pagamento`        | 68.16%    | 867.035            |
| `recarga`          | 99.78%    | 1.269.268          |
| `dados_cadastrais` | 100.00%   | 1.272.095          |
| `telco`            | 100.00%   | 1.272.095          |

## 📑 DIAGNÓSTICO DE SELEÇÃO PARA CONFRONTO
> 1. **DESCARTE DADOS_CADASTRAIS:** Apesar do volume (3.5M), apresenta apenas 35% de match. A adoção como âncora resultaria em 65% de 'Sparsity' (nulos) na variável alvo.
> 2. **ELEGIBILIDADE TELCO vs BUREAU:** Ambas apresentam consistência volumétrica absoluta. O confronto visa validar a integridade semântica da Label entre as fontes.

## ⚖️ PARTE 2: CONFRONTO DE LABELS (TELCO vs BUREAU)

### 📊 [RESULTADOS DO CONFRONTO]
- **Total de CPFs na interseção:** `1.406.564`
- ✅ **Labels idênticas:** `1.337.421` (95.08%)
- 🆘 **Nulos Telco recuperados pelo Bureau:** `46.868` (3.33%)
- ⚠️ **Divergências de valor (Conflito):** `22.275` (1.58%)

### 📈 [ESTATÍSTICAS DO TARGET]
- **Bad Rate na Telco:** `23.52%`
- **Bad Rate no Bureau:** `24.51%`

## 🎯 ESTRATÉGIAS DE SELEÇÃO DE TARGET
### 🛡️ OPÇÃO A: FOCO EM INTEGRIDADE (AUDITORIA)
- **Veredito:** **❌ NÃO RECOMENDADO**
- **Premissa:** Rigidez Analítica (Divergência < 1%).
- **Lógica:** Soberania do dado primário da Telco sobre fontes externas.

### 🚀 OPÇÃO B: FOCO EM VOLUMETRIA (MÁXIMA PERFORMANCE)
- **Veredito:** **✅ RECOMENDADO**
- **Premissa:** Expansão de Base Amostral (Divergência < 2%).
- **Ganhos:** Recuperação de `46.868` registros para incremento de performance.

### 💡 RECOMENDAÇÃO FINAL
> Com **1.58%** de divergência, a melhor escolha técnica é: **BUREAU (OPÇÃO B)**

### 💼 OBSERVAÇÃO DE NEGÓCIO PARA VALIDAR
Pode ser que o Bureau só gere score para clientes que tiveram uma proposta efetivada. Com isso, os nulos na Telco podem ser clientes que nem chegaram a gerar um registro no Bureau, como em casos de vendas canceladas no carrinho. Neste cenário, a base **TELCO** é mais fiel a realidade.

---


#### 2.2.2 📁 Auditoria de Particionamento Físico (Hive)

Para garantir que a estratégia de particionamento no S3 está correta, foi executado um script de inspeção em lote na camada Silver. O objetivo é validar se o conteúdo interno da coluna de data corresponde exatamente à estrutura de pastas `ano_mes=YYYYMM` onde os arquivos Parquet estão armazenados.

> 🔗 **Acesse o log completo de auditoria:** [inspect_partition_gold.log](../../reports/observability/integrity/inspect_partition_gold.log)
