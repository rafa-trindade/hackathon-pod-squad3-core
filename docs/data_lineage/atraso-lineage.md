## 📉 Visão Geral - `atraso`

- **Entidade Principal:** Fatura do Cliente (`NUM_CPF` + `CONTRATO`)
- **Grão da Tabela (Unicidade):** `NUM_CPF, CONTRATO, DAT_REFERENCIA, NUM_FATURA_HASH, NUM_ENT_SEQ_FATURA`
- **Sugestão Chave de Relacionamento (Gold):** `NUM_CPF` (Identificador Único), `CONTRATO` (Vínculo de Produto), `DAT_REFERENCIA` (Eixo Temporal)
- **Chave de Particionamento:** `DAT_REFERENCIA` (Formato YYYYMM)

---

## 📥 Ingestão - `raw/atraso`

- **Fonte:** Externa 
- **Frequência:** Sob demanda (Ingestão manual/Parquet)
- **Formato Original:** Parquet
- **Volume Médio:** ~4307 MiB por carga (6358 MiB descomprimido)

---

## ✅ Data Lineage - `atraso`

### 1. Visão Geral

| Item            | Valor                                 |
|-----------------|---------------------------------------|
| Origem          | `raw/atraso`                |
| Destino Bronze  | `bronze/atraso`             |
| Destino Silver  | `silver/atraso`             |
| Particionamento | `ano_mes` (Coluna Técnica)            |
| Versionamento   | `run_id` (Isolamento de Execução)     |

---

### 2. Lineage por Camada

#### 2.1 RAW → BRONZE

**Origem:** `s3://lake/raw/atraso/*.parquet`  
**Destino:** `s3://lake/bronze/atraso/run_id={run_id}/ano_mes={YYYYMM}/*.parquet`

| Etapa | Processo | Descrição | Ações / Regras | Resultado Esperado |
|------:|----------|-----------|----------------|-------------------|
| 1 | **Normalization (Lowercase)** | Padronização de nomenclatura | Conversão de todos os nomes de colunas para minúsculo para evitar conflitos de case-sensitivity. | Nomes uniformes e sem conflitos de *case-sensitivity*. |
| 2 | **Tipagem Forte** | Conversão de tipos via DuckDB | Aplicação de `CAST` para `DATE`, `INTEGER`, `DOUBLE` e `BOOLEAN` baseada no profiling da origem. | Dados tecnicamente íntegros para processamento. |
| 3 | **Observabilidade** | Enriquecimento de Metadados | Inclusão das colunas `ingestion_ts` e a organização por `run_id` no path do S3. | Rastreabilidade total de quando e como o dado foi carregado. |
| 4 | **Particionamento Técnico** | Geração da estrutura de pastas | Criação da coluna `ano_mes` baseada na `DAT_REFERENCIA` para habilitar o *Partition Pruning* e reduzir custos de scan. | Arquivos organizados fisicamente por `ano_mes=YYYYMM`. |

---

#### 2.2 BRONZE → SILVER 

**Origem:** `s3://lake/bronze/atraso/*.parquet`  
**Destino:** `s3://lake/silver/atraso/run_id={run_id}/ano_mes={YYYYMM}/*.parquet`

| Etapa | Processo | Descrição | Ações / Regras | Resultado Esperado |
|------:|:---------|:----------|:---------------|:-------------------|
| 1 | **Deduplicação** | Garantia de unicidade no lote de carga | Aplicação da regra de grão sobre os novos registros. | Dados reprocessados com unicidade absoluta. |
| 2 | **Normalização de Chaves** | Saneamento de identificadores | Conversão de *hashes* padrão ou valores fixos (vazios) para um padrão explícito de nulidade (`NULL`). | Chaves de relacionamento íntegras para operações de cruzamento (*JOIN*). |
| 3 | **Limpeza de Colunas** | Otimização do esquema (*Schema*) | Remoção de colunas 100% nulas ou sem valor analítico identificadas no diagnóstico de dados. | Base de dados mais leve, com redução de custos de leitura e armazenamento. |

---

#### 2.2.1 🔍 Auditoria e Saneamento

**Grãos em Conformidade:** `num_cpf`, `contrato`, `dat_referencia`, `num_fatura_hash`, `num_ent_seq_fatura`

**Estatísticas de Processamento:**
* 📥 **Registros Iniciais (Bronze):** `31.611.316`
* 💎 **Registros Mantidos (Silver):** `31.611.219`
* ⚠️ **Registros Removidos (Duplicados):** `97` (**< 0.01%**)

**Otimização de Schema (Colunas Excluídas):**
* ✂️ **Colunas 100% Nulas Removidas:** `dat_cancelamento_fat`.

**Notas de Saneamento:**
* 🛠️ **Saneamento de Identificadores:** A coluna `num_fatura_hash` teve 1.075.903 registros normalizados.
* 🔍 **Blacklist de Hash:** O valor técnico `5feceb66ffc86f38d952786c6d696c79c2dbc239dd4e91b46729d73a27fb57e9` (hash de valor nulo) foi detectado e convertido para o padrão `'0'`.

---

#### 2.2.2 📁 Auditoria de Particionamento Físico (Hive)

Para garantir que a estratégia de particionamento no S3 está correta, foi executado um script de inspeção em lote na camada Silver. O objetivo é validar se o conteúdo interno da coluna de data corresponde exatamente à estrutura de pastas `ano_mes=YYYYMM` onde os arquivos Parquet estão armazenados.

> 🔗 **Acesse o log completo de auditoria:** [inspect_partition.log](../../reports/observability/integrity/inspect_partition.log)

**Evidência de Integridade:**

```text
================================================================================
🕵️  AUDITORIA DE PARTIÇÕES SILVER - 2026-01-12 13:13:29
📂 Arquivo de Log: reports/observability/integrity/inspect_partition.log
================================================================================

📊 TABELA: ATRASO
🆔 Run ID: 20260110_145918 | Coluna: dat_referencia
📅 Janela: 202310 a 202503
------------------------------------------------------------
  📁 202310:  1,173,205 linhas | Min: 2023-10-01 00:00:00 | Max: 2023-10-01 00:00:00 | ✅ OK
  📁 202311:  1,152,922 linhas | Min: 2023-11-01 00:00:00 | Max: 2023-11-01 00:00:00 | ✅ OK
  📁 202312:  1,252,111 linhas | Min: 2023-12-01 00:00:00 | Max: 2023-12-01 00:00:00 | ✅ OK
  📁 202401:  1,026,478 linhas | Min: 2024-01-01 00:00:00 | Max: 2024-01-01 00:00:00 | ✅ OK
  📁 202402:  1,055,098 linhas | Min: 2024-02-01 00:00:00 | Max: 2024-02-01 00:00:00 | ✅ OK
  📁 202403:  1,074,593 linhas | Min: 2024-03-01 00:00:00 | Max: 2024-03-01 00:00:00 | ✅ OK
  📁 202404:  1,160,777 linhas | Min: 2024-04-01 00:00:00 | Max: 2024-04-01 00:00:00 | ✅ OK
  📁 202405:  1,196,731 linhas | Min: 2024-05-01 00:00:00 | Max: 2024-05-01 00:00:00 | ✅ OK
  📁 202406:  1,225,694 linhas | Min: 2024-06-01 00:00:00 | Max: 2024-06-01 00:00:00 | ✅ OK
  📁 202407:  1,318,087 linhas | Min: 2024-07-01 00:00:00 | Max: 2024-07-01 00:00:00 | ✅ OK
  📁 202408:  1,397,247 linhas | Min: 2024-08-01 00:00:00 | Max: 2024-08-01 00:00:00 | ✅ OK
  📁 202409:  1,510,312 linhas | Min: 2024-09-01 00:00:00 | Max: 2024-09-01 00:00:00 | ✅ OK
  📁 202410:  1,683,363 linhas | Min: 2024-10-01 00:00:00 | Max: 2024-10-01 00:00:00 | ✅ OK
  📁 202411:  1,883,050 linhas | Min: 2024-11-01 00:00:00 | Max: 2024-11-01 00:00:00 | ✅ OK
  📁 202412:  2,444,916 linhas | Min: 2024-12-01 00:00:00 | Max: 2024-12-01 00:00:00 | ✅ OK
  📁 202501:  3,018,681 linhas | Min: 2025-01-01 00:00:00 | Max: 2025-01-01 00:00:00 | ✅ OK
  📁 202502:  3,643,289 linhas | Min: 2025-02-01 00:00:00 | Max: 2025-02-01 00:00:00 | ✅ OK
  📁 202503:  4,394,665 linhas | Min: 2025-03-01 00:00:00 | Max: 2025-03-01 00:00:00 | ✅ OK
```

**Principais Observações Técnicas:**
- **Consistência Temporal:** Confirmado que 100% dos registros possuem a coluna `dat_referencia` estritamente igual ao diretório de destino.
- **Volume Global:** O total processado e validado nesta run é de **31.611.219** registros.
- **Grão de Snapshot:** A base mantém a integridade de fotos mensais com data de referência sempre no dia 01, mantendo a integridade do particionamento mensal.

---

### 3. Observações Técnicas

- **Imutabilidade:** Nenhuma linha da camada *Raw* é descartada na *Bronze*; apenas os tipos são corrigidos e a nomenclatura é padronizada para garantir a fidelidade à origem.
- **Isolamento de Execuções:** O uso de `run_id` garante que reprocessamentos não causem duplicidade lógica, permitindo *rollbacks* seguros e isolamento de cargas via política de retenção.
- **Auditabilidade:** A coluna `ingestion_ts` registra o momento exato da transformação em cada camada, permitindo o monitoramento de latência e o rastreio da linhagem temporal do dado.
- **Escalabilidade e Custo:** O particionamento físico por `ano_mes` habilita o *Partition Pruning*, garantindo que consultas analíticas leiam apenas as frações necessárias do Lake, reduzindo o custo de scan.
- **Garantia de Unicidade:** A estratégia de deduplicação na *Silver* utiliza o grão técnico validado para assegurar que cada transação ou entidade seja representada de forma única, eliminando sobreposições do lote de carga.
- **Idempotência do Pipeline:** O processo é desenhado para ser idempotente; qualquer reprocessamento da mesma partição sob o mesmo contexto resultará no mesmo estado final, garantindo a consistência dos dados reprocessados.