## 💰 Visão Geral - `pagamento`

- **Entidade Principal:** Pagamento do Cliente (`NUM_CPF` + `CONTRATO`)
- **Grão da Tabela (Unicidade):** `NUM_CPF, CONTRATO, SEQ_FATURA, NUM_SUB_SEQ_FATURA`
- **Chave de Relacionamento (Gold):** Sugestão: `NUM_CPF` (Identificador Único), `CONTRATO` (Vínculo de Produto), `DAT_STATUS_FATURA` (Eixo Temporal)
- **Chave de Particionamento:** `DAT_STATUS_FATURA` (Formato YYYYMM)

---

## 📥 Ingestão - `raw/pagamento`

- **Fonte:** Externa 
- **Frequência:** Sob demanda (Ingestão manual/Parquet)
- **Formato Original:** Parquet
- **Volume médio:** ~2115 MiB por carga (3677 MiB descomprimido)

---

## ✅ Data Lineage - `pagamento`

### 1. Visão Geral

| Item            | Valor                                 |
|-----------------|---------------------------------------|
| Origem          | `raw/pagamento`                       |
| Destino Bronze  | `bronze/pagamento`                    |
| Destino Silver  | `silver/pagamento`                    |
| Particionamento | `ano_mes` (Coluna Técnica)    |
| Versionamento   | `run_id` (Isolamento de Execução)     |

---

### 2. Lineage por Camada

#### 2.1 RAW → BRONZE

**Origem:** `s3://lake/raw/pagamento/*.parquet`  
**Destino:** `s3://lake/bronze/pagamento/run_id={run_id}/ano_mes={YYYYMM}/*.parquet`

- **Volume médio:** ~1757 MiB por carga (2943 MiB descomprimido)

| Etapa | Processo | Descrição | Ações / Regras | Resultado Esperado |
|------:|----------|-----------|----------------|-------------------|
| 1 | **Normalization (Lowercase)** | Padronização de nomenclatura | Conversão de todos os nomes de colunas para minúsculo para evitar conflitos de case-sensitivity. | Nomes uniformes e sem conflitos de *case-sensitivity*. |
| 2 | **Tipagem Forte** | Conversão de tipos via DuckDB | Aplicação de `CAST` para `DATE`, `INTEGER`, `DOUBLE` e `BOOLEAN` baseada no profiling da origem. | Dados tecnicamente íntegros para processamento. |
| 3 | **Observabilidade** | Enriquecimento de Metadados | Inclusão das colunas `ingestion_ts` e a organização por `run_id` no path do S3. | Rastreabilidade total de quando e como o dado foi carregado. |
| 4 | **Particionamento Técnico** | Geração da estrutura de pastas | Criação da coluna `ano_mes` baseada na `DAT_STATUS_FATURA` para habilitar o *Partition Pruning* e reduzir custos de scan. | Arquivos organizados fisicamente por `ano_mes=YYYYMM`. |

---

#### 2.2 BRONZE → SILVER

**Origem:** `s3://lake/bronze/pagamento/*.parquet`  
**Destino:** `s3://lake/silver/pagamento/run_id={run_id}/ano_mes={YYYYMM}/*.parquet`

- **Volume médio:** em desenvolvimento

| Etapa | Processo | Descrição | Ações / Regras | Resultado Esperado |
|------:|:---------|:----------|:---------------|:-------------------|
| 1 | **Deduplicação** | Garantia de unicidade no lote de carga | Aplicação da regra de grão sobre os novos registros. | Dados reprocessados com unicidade absoluta. |
| 2 | **Normalização de Chaves** | Saneamento de identificadores | Conversão de *hashes* padrão ou valores fixos (vazios) para um padrão explícito de nulidade (`NULL`). | Chaves de relacionamento íntegras para operações de cruzamento (*JOIN*). |
| 3 | **Limpeza de Colunas** | Otimização do esquema (*Schema*) | Remoção de colunas 100% nulas ou sem valor analítico identificadas no diagnóstico de dados. | Base de dados mais leve, com redução de custos de leitura e armazenamento. |

---

### 3. Observações Técnicas

- **Imutabilidade:** Nenhuma linha da camada *Raw* é descartada na *Bronze*; apenas os tipos são corrigidos e a nomenclatura é padronizada para garantir a fidelidade à origem.
- **Isolamento de Execuções:** O uso de `run_id` garante que reprocessamentos não causem duplicidade lógica, permitindo *rollbacks* seguros e isolamento de cargas via política de retenção.
- **Auditabilidade:** A coluna `ingestion_ts` registra o momento exato da transformação em cada camada, permitindo o monitoramento de latência e o rastreio da linhagem temporal do dado.
- **Escalabilidade e Custo:** O particionamento físico por `ano_mes` habilita o *Partition Pruning*, garantindo que consultas analíticas leiam apenas as frações necessárias do Lake, reduzindo drasticamente o custo de scan.
- **Preservação do Estado Atual:** A estratégia de deduplicação na *Silver* prioriza o registro mais recente (via data de atualização ou carimbo de tempo), garantindo que retificações e atualizações vindas da origem sejam refletidas corretamente sem gerar duplicidade.
- **Idempotência do Pipeline:** O processo é desenhado para ser idempotente; qualquer reprocessamento da mesma partição sob o mesmo contexto resultará no mesmo estado final, evitando a inflação artificial de métricas e valores.
- **Preservação do Grão:** O grão técnico na camada *Silver* é mantido em sua forma mais granular para permitir reconciliações detalhadas e garantir flexibilidade total para diferentes agregações na camada *Gold*.