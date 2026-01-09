## 📥 Ingestão - `raw/atraso`

- **Fonte:** Externa 
- **Frequência:** Sob demanda (Ingestão manual/Parquet)
- **Formato Original:** Parquet
- **Volume médio:** ~4307 MiB por carga (6358 MiB descomprimido)
- **Chave Técnica Composta:** [`num_cpf`, `dat_referencia`, `num_fatura_hash`, `contrato`] (candidatas)
- **Chave de Particionamento:** `DAT_REFERENCIA` (YYYYMM)

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

- **Volume médio:** ~3541 MiB por carga (5213 MiB descomprimido)

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

- **Volume médio:** ~

... em desenvolvimento

---

### 3. Observações Técnicas

- **Imutabilidade:** Nenhuma linha da Raw é descartada na Bronze; apenas os tipos são corrigidos e a nomenclatura é padronizada.
- **Isolamento de Runs:** O uso do `run_id` garante que reprocessamentos não causem duplicidade lógica, permitindo rollbacks seguros via política de retenção.
- **Auditabilidade:** A coluna `ingestion_ts` registra o momento exato da transformação, permitindo monitorar a latência do pipeline.
- **Escalabilidade:** O particionamento por `ano_mes` prepara a base para consultas analíticas de alta performance, lendo apenas as frações necessárias do Lake.