## 💰 Visão Geral - `pagamento`

- **Entidade Principal:** Pagamento do Cliente (`NUM_CPF` + `CONTRATO`)
- **Grão da Tabela (Unicidade):** `NUM_CPF, CONTRATO, SEQ_FATURA, NUM_SUB_SEQ_FATURA`
- **Sugestão Chave de Relacionamento (Gold):** `NUM_CPF` (Identificador Único), `CONTRATO` (Vínculo de Produto), `DAT_STATUS_FATURA` (Eixo Temporal)
- **Chave de Particionamento:** `DAT_STATUS_FATURA` (Formato YYYYMM)

---

## 📥 Ingestão - `raw/pagamento`

- **Fonte:** Externa 
- **Frequência:** Sob demanda (Ingestão manual/Parquet)
- **Formato Original:** Parquet
- **Volume Médio:** ~2115 MiB por carga (3677 MiB descomprimido)

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

| Etapa | Processo | Descrição | Ações / Regras | Resultado Esperado |
|------:|:---------|:----------|:---------------|:-------------------|
| 1 | **Deduplicação** | Garantia de unicidade no lote de carga | Aplicação da regra de grão sobre os novos registros. | Dados reprocessados com unicidade absoluta. |
| 2 | **Normalização de Chaves** | Saneamento de identificadores | Conversão de *hashes* padrão ou valores fixos (vazios) para um padrão explícito de nulidade (`NULL`). | Chaves de relacionamento íntegras para operações de cruzamento (*JOIN*). |
| 3 | **Limpeza de Colunas** | Otimização do esquema (*Schema*) | Remoção de colunas 100% nulas ou sem valor analítico identificadas no diagnóstico de dados. | Base de dados mais leve, com redução de custos de leitura e armazenamento. |

---

#### 2.2.1 🔍 Auditoria e Saneamento

**Grãos em Conformidade:** `num_cpf`, `contrato`, `seq_fatura`, `num_sub_seq_fatura`

**Estatísticas de Processamento:**
* 📥 **Registros Iniciais (Bronze):** `21.829.628`
* 💎 **Registros Mantidos (Silver):** `21.567.614`
* ⚠️ **Registros Removidos (Duplicados):** `262.014` (**1.20%**)

**Otimização de Schema (Colunas Excluídas):**
* ✂️ **Colunas 100% Nulas Removidas:** `dat_atualizacao_credito`, `cod_netuno_pagamento`, `cod_desalocacao_credito`.

---

#### 2.2.2 📁 Auditoria de Particionamento Físico (Hive)

Para garantir que a estratégia de particionamento no S3 está correta, foi executado um script de inspeção em lote na camada Silver. O objetivo é validar se o conteúdo interno da coluna de data corresponde exatamente à estrutura de pastas `ano_mes=YYYYMM` onde os arquivos Parquet estão armazenados.

> 🔗 **Acesse o log completo de auditoria:** [inspect_partition.log](../../reports/observability/partitions/inspect_partition.log)

**Evidência de Integridade:**

```text
📊 TABELA: PAGAMENTO
🆔 Run ID: 20260110_150652 | Coluna: dat_status_fatura
📅 Janela: 202310 a 202503
------------------------------------------------------------
  📁 202310:    857,209 linhas | Min: 2023-10-01 00:00:00 | Max: 2023-10-31 00:00:00 | ✅ OK
  📁 202311:    857,908 linhas | Min: 2023-11-01 00:00:00 | Max: 2023-11-30 00:00:00 | ✅ OK
  📁 202312:    916,573 linhas | Min: 2023-12-01 00:00:00 | Max: 2023-12-31 00:00:00 | ✅ OK
  📁 202401:    912,618 linhas | Min: 2024-01-01 00:00:00 | Max: 2024-01-31 00:00:00 | ✅ OK
  📁 202402:    912,381 linhas | Min: 2024-02-01 00:00:00 | Max: 2024-02-29 00:00:00 | ✅ OK
  📁 202403:    967,967 linhas | Min: 2024-03-01 00:00:00 | Max: 2024-03-31 00:00:00 | ✅ OK
  📁 202404:    991,859 linhas | Min: 2024-04-01 00:00:00 | Max: 2024-04-30 00:00:00 | ✅ OK
  📁 202405:  1,029,769 linhas | Min: 2024-05-01 00:00:00 | Max: 2024-05-31 00:00:00 | ✅ OK
  📁 202406:    998,124 linhas | Min: 2024-06-01 00:00:00 | Max: 2024-06-30 00:00:00 | ✅ OK
  📁 202407:  1,057,102 linhas | Min: 2024-07-01 00:00:00 | Max: 2024-07-31 00:00:00 | ✅ OK
  📁 202408:  1,062,456 linhas | Min: 2024-08-01 00:00:00 | Max: 2024-08-31 00:00:00 | ✅ OK
  📁 202409:  1,039,259 linhas | Min: 2024-09-01 00:00:00 | Max: 2024-09-30 00:00:00 | ✅ OK
  📁 202410:  1,097,942 linhas | Min: 2024-10-01 00:00:00 | Max: 2024-10-31 00:00:00 | ✅ OK
  📁 202411:  1,177,502 linhas | Min: 2024-11-01 00:00:00 | Max: 2024-11-30 00:00:00 | ✅ OK
  📁 202412:  1,489,889 linhas | Min: 2024-12-01 00:00:00 | Max: 2024-12-31 00:00:00 | ✅ OK
  📁 202501:  1,755,588 linhas | Min: 2025-01-01 00:00:00 | Max: 2025-01-31 00:00:00 | ✅ OK
  📁 202502:  2,001,239 linhas | Min: 2025-02-01 00:00:00 | Max: 2025-02-28 00:00:00 | ✅ OK
  📁 202503:  2,442,229 linhas | Min: 2025-03-01 00:00:00 | Max: 2025-03-31 00:00:00 | ✅ OK
```

**Principais Observações Técnicas:**
- **Consistência Temporal:** Confirmado que 100% dos registros possuem a coluna `dat_status_fatura` estritamente dentro do intervalo do diretório de destino.
- **Volume Global:** O total processado e validado nesta run é de **21.567.614** registros.
- **Grão de Transação:** A base mantém a integridade de fotos mensais, apresentando variação diária dentro do mês (Min/Max cobrem o mês completo), mantendo a integridade do particionamento mensal.

---

### 3. Observações Técnicas

- **Imutabilidade:** Nenhuma linha da camada *Raw* é descartada na *Bronze*; apenas os tipos são corrigidos e a nomenclatura é padronizada para garantir a fidelidade à origem.
- **Isolamento de Execuções:** O uso de `run_id` garante que reprocessamentos não causem duplicidade lógica, permitindo *rollbacks* seguros e isolamento de cargas via política de retenção.
- **Auditabilidade:** A coluna `ingestion_ts` registra o momento exato da transformação em cada camada, permitindo o monitoramento de latência e o rastreio da linhagem temporal do dado.
- **Escalabilidade e Custo:** O particionamento físico por `ano_mes` habilita o *Partition Pruning*, garantindo que consultas analíticas leiam apenas as frações necessárias do Lake, reduzindo o custo de scan.
- **Garantia de Unicidade:** A estratégia de deduplicação na *Silver* utiliza o grão técnico validado para assegurar que cada transação ou entidade seja representada de forma única, eliminando sobreposições do lote de carga.
- **Idempotência do Pipeline:** O processo é desenhado para ser idempotente; qualquer reprocessamento da mesma partição sob o mesmo contexto resultará no mesmo estado final, garantindo a consistência dos dados reprocessados.liações detalhadas e garantir flexibilidade total para diferentes agregações na camada *Gold*.