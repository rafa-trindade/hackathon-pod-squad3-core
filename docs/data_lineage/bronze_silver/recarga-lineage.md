## 📱 Visão Geral - `recarga`

- **Entidade Principal:** Linha do Cliente (`NUM_CPF` + `DW_NUM_NTC`)
- **Grão da Tabela (Unicidade):** `NUM_CPF, DW_NUM_NTC, DAT_INSERCAO_CREDITO, HOR_INSERCAO_CREDITO`
- **Chave de Particionamento:** `DAT_INSERCAO_CREDITO` (Formato YYYYMM)

---

## 📥 Ingestão - `raw/recarga`

- **Fonte:** Externa 
- **Frequência:** Sob demanda (Ingestão manual/Parquet)
- **Formato Original:** Parquet
- **Volume Médio:** ~3104 MiB por carga (5222 MiB descomprimido)

---

## ✅ Data Lineage - `recarga`

### 1. Visão Geral

| Item            | Valor                                 |
|-----------------|---------------------------------------|
| Origem          | `raw/recarga`                         |
| Destino Bronze  | `bronze/recarga`                      |
| Destino Silver  | `silver/recarga`                      |
| Versionamento   | `run_id` (Isolamento de Execução)     |
| Particionamento | `ano_mes` (Coluna Técnica)            |

---

### 2. Lineage por Camada

#### 2.1 RAW → BRONZE

**Origem:** `s3://lake/raw/recarga/*.parquet`  
**Destino:** `s3://lake/bronze/recarga/run_id={run_id}/ano_mes={YYYYMM}/*.parquet`

| Etapa | Processo | Descrição | Ações / Regras | Resultado Esperado |
|------:|----------|-----------|----------------|-------------------|
| 1 | **Normalization (Lowercase)** | Padronização de nomenclatura | Conversão de todos os nomes de colunas para minúsculo para evitar conflitos de case-sensitivity. | Nomes uniformes e sem conflitos de *case-sensitivity*. |
| 2 | **Tipagem Forte** | Conversão de tipos via DuckDB | Aplicação de `CAST` para `DATE`, `INTEGER`, `DOUBLE` e `BOOLEAN` baseada no profiling da origem. | Dados tecnicamente íntegros para processamento. |
| 3 | **Observabilidade** | Enriquecimento de Metadados | Inclusão das colunas `ingestion_ts` e a organização por `run_id` no path do S3. | Rastreabilidade total de quando e como o dado foi carregado. |
| 4 | **Particionamento Técnico** | Geração da estrutura de pastas | Criação da coluna `ano_mes` baseada na `DAT_INSERCAO_CREDITO` para habilitar o *Partition Pruning* e reduzir custos de scan. | Arquivos organizados fisicamente por `ano_mes=YYYYMM`. |

---

#### 2.1.1 🧩 Suporte: Processamento de Dimensões (`recarga_dim`)

Diferente das tabelas '''Fato''', as dimensões são tabelas de referência técnica com baixo volume e alta estabilidade. Por isso, seguem um fluxo de carga simplificado:

**Origem:** `s3://lake/raw/recarga_dim/*.csv`  
**Destino:** `s3://lake/bronze/recarga_dim/*.parquet`

| Regra Técnica | Descrição | Justificativa |
|:---|:---|:---|
| **Overwrite Total** | Os arquivos Parquet são sobrescritos a cada carga. | Dimensões são snapshots do estado atual do cadastro. |
| **Flat Structure** | Armazenamento em arquivos únicos (sem run_id/ano_mes). | Facilita o Join e reduz a complexidade de leitura na camada Silver. |
| **Saneamento de Strings** | Aplicação de `TRIM` e `LOWER` (exceto em chaves técnicas). | Garante que descrições fiquem padronizadas para visualização. |
| **Auditoria de Integridade** | Validação contra a ''Fato'' já na camada Bronze. | **O log da Bronze é um alerta de cadastro faltando**: identifica IDs na ''Fato'' sem par na dimensão. |

![bucket](../images/data_lineage/bucket_recarga_dim.png)

---

#### 2.2 BRONZE → SILVER 

**Origem:** `s3://lake/bronze/recarga/*.parquet`  
**Destino:** `s3://lake/silver/recarga/run_id={run_id}/ano_mes={YYYYMM}/*.parquet`

| Etapa | Processo | Descrição | Ações / Regras | Resultado Esperado |
|------:|:---------|:----------|:---------------|:-------------------|
| 1 | **Deduplicação** | Garantia de unicidade | Aplicação da regra de grão (`num_cpf`, `data`, `hora`). | Dados reprocessados com unicidade absoluta. |
| 2 | **Normalização de Chaves** | Saneamento de identificadores | Conversão de campos do grão para padrões técnicos. | Chaves íntegras para operações de cruzamento. |
| 3 | **Enriquecimento (JOINs)** | Agregação das 11 dimensões técnicas | Cruzamento com `recarga_dim` tratando códigos de sistema (-1) e garantindo match via cast. | Dataset legível com descrições de negócio integradas. |
| 4 | **Limpeza e Reordenação** | Otimização do esquema (*Schema*) | Remoção de colunas 100% nulas e posicionamento das descrições após suas respectivas chaves. | Base de dados organizada e otimizada para consumo analítico. |

![bucket](../images/data_lineage/bucket_recarga.png)

---

#### 2.2.1 🔍 Auditoria e Saneamento

**Grãos em Conformidade:** `num_cpf`, `dw_num_ntc`, `dat_insercao_credito`, `hor_insercao_credito`

**Estatísticas de Processamento:**
* 📥 **Registros Iniciais (Bronze):** `100.213.651`
* 💎 **Registros Mantidos (Silver):** `95.446.983`
* ⚠️ **Registros Removidos (Duplicados Reais):** `4.766.668` (**4.75%**)

---

#### 💡 Nota Arquitetural: Precisão Temporal e Unicidade por Linha
> A combinação da alta granularidade temporal (`hor_insercao_credito`) com o identificador da linha (`dw_num_ntc`) é o que garante a integridade desta entidade.
>
> * **Detalhe Técnico:** O valor da hora representa os segundos decorridos desde a meia-noite (Padrão SAS/Legacy) e é processado como **BIGINT**, permitindo distinguir transações simultâneas em linhas distintas de um mesmo titular.
> * **Impacto:** Esta estratégia permitiu identificar e remover **4.766.668 registros redundantes**, provenientes de possíveis falhas de *double ingestion* na origem, corrigindo um possível desvio de **4.7%** no faturamento total reportado.

---

**Otimização de Schema:**
* ✨ **Expansão de Atributos:** O dataset saltou de **27 para 38 colunas** após a agregação de dimensões.
* ✨ **Nenhuma coluna 100% nula encontrada:** Todas as colunas originais e agregadas foram preservadas.

---

#### 2.2.2 📁 Auditoria de Particionamento Físico (Hive)

Para garantir que a estratégia de particionamento no S3 está correta, foi executado um script de inspeção em lote na camada Silver. O objetivo é validar se o conteúdo interno da coluna de data corresponde exatamente à estrutura de pastas `ano_mes=YYYYMM` onde os arquivos Parquet estão armazenados.

> 🔗 **Acesse o log completo de auditoria:** [inspect_partition_*.log](../../reports/observability/integrity/)

**Evidência de Integridade:**

```text
📊 TABELA: RECARGA
🆔 Run ID: 20260110_152608 | Coluna: dat_insercao_credito
📅 Janela: 202310 a 202503
------------------------------------------------------------
  📁 202310:  4,182,629 linhas | Min: 2023-10-01 00:00:00 | Max: 2023-10-31 00:00:00 | ✅ OK
  📁 202311:  4,153,371 linhas | Min: 2023-11-01 00:00:00 | Max: 2023-11-30 00:00:00 | ✅ OK
  📁 202312:  4,440,690 linhas | Min: 2023-12-01 00:00:00 | Max: 2023-12-31 00:00:00 | ✅ OK
  📁 202401:  4,238,829 linhas | Min: 2024-01-01 00:00:00 | Max: 2024-01-31 00:00:00 | ✅ OK
  📁 202402:  4,254,204 linhas | Min: 2024-02-01 00:00:00 | Max: 2024-02-29 00:00:00 | ✅ OK
  📁 202403:  4,736,808 linhas | Min: 2024-03-01 00:00:00 | Max: 2024-03-31 00:00:00 | ✅ OK
  📁 202404:  4,641,082 linhas | Min: 2024-04-01 00:00:00 | Max: 2024-04-30 00:00:00 | ✅ OK
  📁 202405:  4,822,127 linhas | Min: 2024-05-01 00:00:00 | Max: 2024-05-31 00:00:00 | ✅ OK
  📁 202406:  4,886,421 linhas | Min: 2024-06-01 00:00:00 | Max: 2024-06-30 00:00:00 | ✅ OK
  📁 202407:  5,257,411 linhas | Min: 2024-07-01 00:00:00 | Max: 2024-07-31 00:00:00 | ✅ OK
  📁 202408:  5,557,900 linhas | Min: 2024-08-01 00:00:00 | Max: 2024-08-31 00:00:00 | ✅ OK
  📁 202409:  5,512,580 linhas | Min: 2024-09-01 00:00:00 | Max: 2024-09-30 00:00:00 | ✅ OK
  📁 202410:  6,480,407 linhas | Min: 2024-10-01 00:00:00 | Max: 2024-10-31 00:00:00 | ✅ OK
  📁 202411:  6,800,420 linhas | Min: 2024-11-01 00:00:00 | Max: 2024-11-30 00:00:00 | ✅ OK
  📁 202412:  6,927,326 linhas | Min: 2024-12-01 00:00:00 | Max: 2024-12-31 00:00:00 | ✅ OK
  📁 202501:  6,366,515 linhas | Min: 2025-01-01 00:00:00 | Max: 2025-01-31 00:00:00 | ✅ OK
  📁 202502:  6,030,903 linhas | Min: 2025-02-01 00:00:00 | Max: 2025-02-28 00:00:00 | ✅ OK
  📁 202503:  6,096,666 linhas | Min: 2025-03-01 00:00:00 | Max: 2025-03-31 00:00:00 | ✅ OK
```

**Principais Observações Técnicas:**
- **Consistência Temporal:** Confirmado que 100% dos registros possuem a coluna `dat_insercao_credito` estritamente dentro do intervalo do diretório de destino.
- **Volume Global:** O total processado e validado nesta run é de **95.386.289** registros.
- **Grão de Transação:** Esta tabela reflete a volumetria de transações diárias (com Min/Max cobrindo o mês completo), garantindo a correta agregação física por partição mensal.

---

#### 2.2.3 📋 Logs de Qualidade e Observabilidade

O pipeline implementa uma estratégia de validação em duas etapas, diferenciando a integridade referencial (cadastro) da cobertura analítica (enriquecimento).

> 🔗 **Acesse os logs:** [bronze-recarga_dim-quality.log](../../reports/observability/quality/pipeline/bronze-recarga_dim-quality.log) | [silver-recarga_agg-quality.log](../../reports/observability/quality/pipeline/silver-recarga_agg-quality.log)

**Diferenciação de Responsabilidades:**
* **Log da Bronze (Dimensões):** Atua como um **alerta de cadastro faltando**. Valida se a origem (CSV) possui todos os códigos que a transação ('Fato') está gerando.
* **Log da Silver (Agregação):** Atua como um **alerta de cobertura de dados**. Valida se o processo de Join conseguiu preencher as descrições ou se existem "gaps" de informação analítica.

**Evidência de Sucesso (Run 20260121_175800):**
* ✅ **Tratamento de Órfãos:** O código `-1` foi mapeado para "não mapeado (código -1)", reduzindo as falhas de cobertura em **98%** nas colunas de Promoção e Instituição.
* ✅ **Tipagem Forte:** O uso de `::VARCHAR` no Join de Status e Inserção garantiu 100% de match para códigos negativos que existiam no CSV.

---

### 3. Observações Técnicas

- **Imutabilidade:** Nenhuma linha da camada *Raw* é descartada na *Bronze*; apenas os tipos são corrigidos e a nomenclatura é padronizada para garantir a fidelidade à origem.
- **Isolamento de Execuções:** O uso de `run_id` garante que reprocessamentos não causem duplicidade lógica, permitindo *rollbacks* seguros e isolamento de cargas via política de retenção.
- **Auditabilidade:** A coluna `ingestion_ts` registra o momento exato da transformação em cada camada, permitindo o monitoramento de latência e o rastreio da linhagem temporal do dado.
- **Escalabilidade e Custo:** O particionamento físico por `ano_mes` habilita o *Partition Pruning*, garantindo que consultas analíticas leiam apenas as frações necessárias do Lake, reduzindo o custo de scan.
- **Garantia de Unicidade:** A estratégia de deduplicação na *Silver* utiliza o grão técnico validado para assegurar que cada transação ou entidade seja representada de forma única, eliminando sobreposições do lote de carga.
- **Idempotência do Pipeline:** O processo é desenhado para ser idempotente; qualquer reprocessamento da mesma partição sob o mesmo contexto resultará no mesmo estado final, garantindo a consistência dos dados reprocessados.