## 🛡️ Visão Geral - `score_bureau_movel`

- **Entidade Principal:** Risco de Crédito do Cliente (`NUM_CPF` + `SCORE_`)
- **Grão da Tabela (Unicidade):** `NUM_CPF, SAFRA, PROD`
- **Chave de Particionamento:** `SAFRA` (Formato YYYYMM)

---

## 📥 Ingestão - `raw/score_bureau_movel`

- **Fonte:** Externa 
- **Frequência:** Sob demanda (Ingestão manual/Parquet)
- **Formato Original:** Parquet
- **Volume Médio:** ~12 MiB por carga (21 MiB descomprimido)

---

## ✅ Data Lineage - `score_bureau_movel`

### 1. Visão Geral

| Item            | Valor                                 |
|-----------------|---------------------------------------|
| Origem          | `raw/score_bureau_movel`              |
| Destino Bronze  | `bronze/score_bureau_movel`           |
| Destino Silver  | `silver/score_bureau_movel`           |
| Versionamento   | `run_id` (Isolamento de Execução)     |
| Particionamento | `ano_mes` (Coluna Técnica)            |

---

### 2. Lineage por Camada

#### 2.1 RAW → BRONZE

**Origem:** `s3://lake/raw/score_bureau_movel/*.parquet`  
**Destino:** `s3://lake/bronze/score_bureau_movel/run_id={run_id}/ano_mes={YYYYMM}/*.parquet`

| Etapa | Processo | Descrição | Ações / Regras | Resultado Esperado |
|------:|----------|-----------|----------------|-------------------|
| 1 | **Normalization (Lowercase)** | Padronização de nomenclatura | Conversão de todos os nomes de colunas para minúsculo para evitar conflitos de case-sensitivity. | Nomes uniformes e sem conflitos de *case-sensitivity*. |
| 2 | **Tipagem Forte** | Conversão de tipos via DuckDB | Aplicação de `CAST` para `DATE`, `INTEGER`, `DOUBLE` e `BOOLEAN` baseada no profiling da origem. | Dados tecnicamente íntegros para processamento. |
| 3 | **Observabilidade** | Enriquecimento de Metadados | Inclusão das colunas `ingestion_ts` e a organização por `run_id` no path do S3. | Rastreabilidade total de quando e como o dado foi carregado. |
| 4 | **Particionamento Técnico** | Geração da estrutura de pastas | Criação da coluna `ano_mes` baseada na `SAFRA` para habilitar o *Partition Pruning* e reduzir custos de scan. | Arquivos organizados fisicamente por `ano_mes=YYYYMM`. |

---

#### 2.2 BRONZE → SILVER 

**Origem:** `s3://lake/bronze/score_bureau_movel/*.parquet`  
**Destino:** `s3://lake/silver/score_bureau_movel/run_id={run_id}/ano_mes={YYYYMM}/*.parquet`

| Etapa | Processo | Descrição | Ações / Regras | Resultado Esperado |
|------:|:---------|:----------|:---------------|:-------------------|
| 1 | **Deduplicação** | Garantia de unicidade no lote de carga | Aplicação da regra de grão sobre os novos registros. | Dados reprocessados com unicidade absoluta. |
| 2 | **Normalização de Chaves** | Saneamento de identificadores | Conversão de *hashes* padrão ou valores fixos (vazios) para um padrão explícito de nulidade (`NULL`). | Chaves de relacionamento íntegras para operações de cruzamento (*JOIN*). |
| 3 | **Limpeza de Colunas** | Otimização do esquema (*Schema*) | Remoção de colunas 100% nulas ou sem valor analítico identificadas no diagnóstico de dados. | Base de dados mais leve, com redução de custos de leitura e armazenamento. |

![bucket](../images/data_lineage/bucket_score_bureau.png)

---

#### 2.2.1 🔍 Auditoria e Saneamento

**Grãos em Conformidade:** `num_cpf`, `safra`, `prod`

**Estatísticas de Processamento:**
* 📥 **Registros Iniciais (Bronze):** `1.290.526`
* 💎 **Registros Mantidos (Silver):** `1.290.526`
* ⚠️ **Registros Removidos (Duplicados):** `0` (**0.00%**)

**Otimização de Schema (Colunas Excluídas):**
* ✨ **Nenhuma coluna 100% nula encontrada:** Todas as colunas originais continham dados e foram preservadas.

---

#### 2.2.2 📁 Auditoria de Particionamento Físico (Hive)

Para garantir que a estratégia de particionamento no S3 está correta, foi executado um script de inspeção em lote na camada Silver. O objetivo é validar se o conteúdo interno da coluna de data corresponde exatamente à estrutura de pastas `ano_mes=YYYYMM` onde os arquivos Parquet estão armazenados.

> 🔗 **Acesse o log completo de auditoria:** [inspect_partition_*.log](../../reports/observability/integrity/)

**Evidência de Integridade:**

```text
📊 TABELA: SCORE_BUREAU_MOVEL
🆔 Run ID: 20260110_154703 | Coluna: safra
📅 Janela: 202410 a 202503
------------------------------------------------------------
  📁 202410:    203,828 linhas | Min: 2024-10-01 00:00:00 | Max: 2024-10-01 00:00:00 | ✅ OK
  📁 202411:    227,176 linhas | Min: 2024-11-01 00:00:00 | Max: 2024-11-01 00:00:00 | ✅ OK
  📁 202412:    227,985 linhas | Min: 2024-12-01 00:00:00 | Max: 2024-12-01 00:00:00 | ✅ OK
  📁 202501:    221,002 linhas | Min: 2025-01-01 00:00:00 | Max: 2025-01-01 00:00:00 | ✅ OK
  📁 202502:    203,139 linhas | Min: 2025-02-01 00:00:00 | Max: 2025-02-01 00:00:00 | ✅ OK
  📁 202503:    207,396 linhas | Min: 2025-03-01 00:00:00 | Max: 2025-03-01 00:00:00 | ✅ OK
```

**Principais Observações Técnicas:**
- **Consistência Temporal:** Confirmado que 100% dos registros possuem a coluna `safra` estritamente igual ao diretório de destino.
- **Volume Global:** O total processado e validado nesta run é de **1.290.526** registros.
- **Grão de Snapshot:** A base mantém a integridade de fotos mensais, com volumetria estável em torno de 215k registros por partição.

---

### 3. Observações Técnicas

- **Imutabilidade:** Nenhuma linha da camada *Raw* é descartada na *Bronze*; apenas os tipos são corrigidos e a nomenclatura é padronizada para garantir a fidelidade à origem.
- **Isolamento de Execuções:** O uso de `run_id` garante que reprocessamentos não causem duplicidade lógica, permitindo *rollbacks* seguros e isolamento de cargas via política de retenção.
- **Auditabilidade:** A coluna `ingestion_ts` registra o momento exato da transformação em cada camada, permitindo o monitoramento de latência e o rastreio da linhagem temporal do dado.
- **Escalabilidade e Custo:** O particionamento físico por `ano_mes` habilita o *Partition Pruning*, garantindo que consultas analíticas leiam apenas as frações necessárias do Lake, reduzindo o custo de scan.
- **Garantia de Unicidade:** A estratégia de deduplicação na *Silver* utiliza o grão técnico validado para assegurar que cada transação ou entidade seja representada de forma única, eliminando sobreposições do lote de carga.
- **Idempotência do Pipeline:** O processo é desenhado para ser idempotente; qualquer reprocessamento da mesma partição sob o mesmo contexto resultará no mesmo estado final, garantindo a consistência dos dados reprocessados.