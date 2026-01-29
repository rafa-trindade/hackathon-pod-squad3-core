## 👤 Visão Geral - `dados_cadastrais`

- **Entidade Principal:** Cliente (`NUM_CPF`)
- **Grão da Tabela (Unicidade):** `NUM_CPF, SAFRA, PROD`
- **Chave de Particionamento:** `SAFRA` (Formato YYYYMM)

---

## 📥 Ingestão - `raw/dados_cadastrais`

- **Fonte:** Externa 
- **Frequência:** Sob demanda (Ingestão manual/Parquet)
- **Formato Original:** Parquet
- **Volume Médio:** ~74 MiB por carga (105 MiB descomprimido)

---

## ✅ Data Lineage - `dados_cadastrais`

### 1. Visão Geral

| Item            | Valor                                 |
|-----------------|---------------------------------------|
| Origem          | `raw/dados_cadastrais`                |
| Destino Bronze  | `bronze/dados_cadastrais`             |
| Destino Silver  | `silver/dados_cadastrais`             |
| Versionamento   | `run_id` (Isolamento de Execução)     |
| Particionamento | `ano_mes` (Coluna Técnica)            |

---

### 2. Lineage por Camada

#### 2.1 RAW → BRONZE

**Origem:** `s3://lake/raw/dados_cadastrais/*.parquet`  
**Destino:** `s3://lake/bronze/dados_cadastrais/run_id={run_id}/ano_mes={YYYYMM}/*.parquet`

| Etapa | Processo | Descrição | Ações / Regras | Resultado Esperado |
|------:|----------|-----------|----------------|-------------------|
| 1 | **Normalization (Lowercase)** | Padronização de nomenclatura | Conversão de todos os nomes de colunas para minúsculo para evitar conflitos de case-sensitivity. | Nomes uniformes e sem conflitos de *case-sensitivity*. |
| 2 | **Tipagem Forte** | Conversão de tipos via DuckDB | Aplicação de `CAST` para `DATE`, `INTEGER`, `DOUBLE` e `BOOLEAN` baseada no profiling da origem. | Dados tecnicamente íntegros para processamento. |
| 3 | **Observabilidade** | Enriquecimento de Metadados | Inclusão das colunas `ingestion_ts` e a organização por `run_id` no path do S3. | Rastreabilidade total de quando e como o dado foi carregado. |
| 4 | **Particionamento Técnico** | Geração da estrutura de pastas | Criação da coluna `ano_mes` baseada na `SAFRA` para habilitar o *Partition Pruning* e reduzir custos de scan. | Arquivos organizados fisicamente por `ano_mes=YYYYMM`. |

---

#### 2.2 BRONZE → SILVER 

**Origem:** `s3://lake/bronze/dados_cadastrais/*.parquet`  
**Destino:** `s3://lake/silver/dados_cadastrais/run_id={run_id}/ano_mes={YYYYMM}/*.parquet`

| Etapa | Processo | Descrição | Ações / Regras | Resultado Esperado |
|------:|:---------|:----------|:---------------|:-------------------|
| 1 | **Deduplicação** | Garantia de unicidade no lote de carga | Aplicação da regra de grão sobre os novos registros. | Dados reprocessados com unicidade absoluta. |
| 2 | **Normalização de Chaves** | Saneamento de identificadores | Conversão de *hashes* padrão ou valores fixos (vazios) para um padrão explícito de nulidade (`NULL`). | Chaves de relacionamento íntegras para operações de cruzamento (*JOIN*). |
| 3 | **Limpeza de Colunas** | Otimização do esquema (*Schema*) | Remoção de colunas 100% nulas ou sem valor analítico identificadas no diagnóstico de dados. | Base de dados mais leve, com redução de custos de leitura e armazenamento. |

![bucket](../images/data_lineage/bucket_dados_cadastrais.png)

---

#### 2.2.1 🔍 Auditoria e Saneamento

**Grãos em Conformidade:** `num_cpf`, `safra`, `prod`

**Estatísticas de Processamento:**
* 📥 **Registros Iniciais (Bronze):** `3.900.378`
* 💎 **Registros Mantidos (Silver):** `3.900.378`
* ⚠️ **Registros Removidos (Duplicados):** `0` (**0.00%**)

**Otimização de Schema (Colunas Excluídas):**
* ✨ **Nenhuma coluna 100% nula encontrada:** Todas as colunas originais continham dados e foram preservadas.

---

#### 2.2.2 📁 Auditoria de Particionamento Físico (Hive)

Para garantir que a estratégia de particionamento no S3 está correta, foi executado um script de inspeção em lote na camada Silver. O objetivo é validar se o conteúdo interno da coluna de data corresponde exatamente à estrutura de pastas `ano_mes=YYYYMM` onde os arquivos Parquet estão armazenados.

> 🔗 **Acesse o log completo de auditoria:** [inspect_partition_*.log](../../reports/observability/integrity/)

**Evidência de Integridade:**

```text
📊 TABELA: DADOS_CADASTRAIS
🆔 Run ID: 20260110_150431 | Coluna: safra
📅 Janela: 202410 a 202503
------------------------------------------------------------
  📁 202410:    653,586 linhas | Min: 2024-10-01 00:00:00 | Max: 2024-10-01 00:00:00 | ✅ OK
  📁 202411:    665,737 linhas | Min: 2024-11-01 00:00:00 | Max: 2024-11-01 00:00:00 | ✅ OK
  📁 202412:    646,037 linhas | Min: 2024-12-01 00:00:00 | Max: 2024-12-01 00:00:00 | ✅ OK
  📁 202501:    667,227 linhas | Min: 2025-01-01 00:00:00 | Max: 2025-01-01 00:00:00 | ✅ OK
  📁 202502:    619,961 linhas | Min: 2025-02-01 00:00:00 | Max: 2025-02-01 00:00:00 | ✅ OK
  📁 202503:    647,830 linhas | Min: 2025-03-01 00:00:00 | Max: 2025-03-01 00:00:00 | ✅ OK
```

**Principais Observações Técnicas:**
- **Consistência Temporal:** Confirmado que 100% dos registros possuem a coluna `safra` estritamente igual ao diretório de destino.
- **Volume Global:** O total processado e validado nesta run é de **3.900.378** registros.
- **Grão de Snapshot:** A base mantém a integridade de fotos mensais, com volumetria estável em torno de 650k registros por partição.

---

### 3. Observações Técnicas

- **Imutabilidade:** Nenhuma linha da camada *Raw* é descartada na *Bronze*; apenas os tipos são corrigidos e a nomenclatura é padronizada para garantir a fidelidade à origem.
- **Isolamento de Execuções:** O uso de `run_id` garante que reprocessamentos não causem duplicidade lógica, permitindo *rollbacks* seguros e isolamento de cargas via política de retenção.
- **Auditabilidade:** A coluna `ingestion_ts` registra o momento exato da transformação em cada camada, permitindo o monitoramento de latência e o rastreio da linhagem temporal do dado.
- **Escalabilidade e Custo:** O particionamento físico por `ano_mes` habilita o *Partition Pruning*, garantindo que consultas analíticas leiam apenas as frações necessárias do Lake, reduzindo o custo de scan.
- **Garantia de Unicidade:** A estratégia de deduplicação na *Silver* utiliza o grão técnico validado para assegurar que cada transação ou entidade seja representada de forma única, eliminando sobreposições do lote de carga.
- **Idempotência do Pipeline:** O processo é desenhado para ser idempotente; qualquer reprocessamento da mesma partição sob o mesmo contexto resultará no mesmo estado final, garantindo a consistência dos dados reprocessados.