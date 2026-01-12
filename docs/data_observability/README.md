# 🔍 Data Observability - Mapeamento Prático do Projeto

Este documento mapeia como as práticas implementadas no projeto se consolidam nos pilares de **Data Observability**, demonstrando que a observabilidade é um **subproduto de boas decisões arquiteturais**.

## 🧱 Os 5 Pilares da Observabilidade no Projeto

Diferente da observabilidade de software (logs, métricas, traces), a observabilidade de dados foca na saúde do fluxo de informação.


### 1️⃣ Freshness & Integridade Física
**Como é atendido:**
- **Auditoria de Particionamento (Hive):** Validação programática (Audit) que garante que o conteúdo cronológico dos dados condiz com a estrutura de pastas `ano_mes=YYYYMM` no S3.
- **Rastreabilidade:** Cada diretório é encapsulado por um `run_id` (Timestamp ISO), permitindo identificar o "atraso" entre a origem e o Lake.
- **Metadado de Ingestão:** Uso da coluna técnica `ingestion_ts` em todos os registros para auditoria de tempo real de carga.

---

### 2️⃣ Volume & Tamanho
**Como é atendido:**
- **Cross-check de Volumetria:** A auditoria de partições realiza a contagem de registros por safra, garantindo que não houve perda de dados durante a fragmentação física na camada Silver.
- **Eficiência Física:** O profiling rastreia o tamanho comprimido (MiB) no S3, monitorando anomalias de armazenamento ou falhas de compressão.

---

### 3️⃣ Schema & Tipagem
**Como é atendido:**
- **Contratos de Tipagem:** A camada Bronze atua como o primeiro "Checkpoint de Schema", convertendo tipos SAS/String para tipos nativos DuckDB (Date, Double, BigInt).
- **Drift de Schema:** O uso de `DESCRIBE` nos relatórios de profiling permite detectar mudanças na estrutura da fonte entre diferentes runs.

---

### 4️⃣ Distribution (Perfil dos Dados)
**Como é atendido:**
- **Sanidade Estatística:** O profiling automatizado calcula cardinalidade, percentual de nulos e distribuição de valores (Top 10).
- **Detecção de Anomalias:** Facilita a identificação visual de "Skew" (desbalanceamento) nas partições `ano_mes`.

---

### 5️⃣ Lineage & Rastreabilidade
**Como é atendido:**
- **Mapeamento de Dependências:** Documentação explícita de como cada campo da RAW se transforma no campo da BRONZE e dai por diante.
- **Isolamento de Erros:** A estrutura de `run_id` permite que o Lineage seja "versionado" - sabemos exatamente qual código gerou qual dado.



## 🛠️ Implementação da Confiabilidade (Reliability)

A confiabilidade é garantida pelo **Protocolo de Limpeza Pós-Sucesso**:

1. **Idempotência:** O reprocessamento de um mesmo mês (`ano_mes`) não gera duplicidade, pois a nova `run_id` substitui logicamente a anterior.
2. **Capacidade de Rollback:** A Política de Retenção mantendo `MAX_RUNS > 1` é o nosso mecanismo de "Undo", permitindo reverter o Lake para um estado estável em segundos caso o pilar de Quality falhe.


## 📂 Evidências de Auditoria (Observability Reports)

A observabilidade é materializada através de artefatos técnicos gerados automaticamente e centralizados para consulta:

- **Integridade de Partições:** [`inspect_partition.log`](../../reports/observability/partitions/inspect_partition.log)
- **Qualidade de Dados (dbt/Pandera):** [`quality/*`](../../reports/observability/quality/)


## 🧠 Conclusão: Observabilidade como Resultado

Neste projeto, a observabilidade não é uma ferramenta instalada, mas uma **propriedade emergente** do sistema:

- **Se o pipeline roda, ele gera Logs (Freshness/Volume).**
- **Se o Profiling roda, ele gera Diagnósticos (Distribution/Schema).**
- **Se a Retenção funciona, ela garante a Resiliência (Reliability).**

A observabilidade emerge como resultado natural da união entre **Código, Governança e Arquitetura**.