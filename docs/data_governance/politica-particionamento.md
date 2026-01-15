# 🧭 Política de Particionamento no Data Lake

**Objetivo:** Documentar o padrão de particionamento e a estratégia de organização temporal adotada na camada Bronze, visando otimizar a performance de leitura, previsibilidade de armazenamento e suporte à modelagem nas camadas posteriores.


## 1. Visão Geral

Para garantir uma arquitetura escalável e eficiente, foi definido um padrão de particionamento único baseado em colunas temporais explícitas. Este eixo temporal permite a leitura seletiva (Partition Pruning), essencial para o processamento de grandes volumes (ex: base de pagamentos com +20M de registros).

Os dados são classificados em duas categorias de ingestão:
- **Snapshots Mensais:** Visões estáticas de posição em uma data de corte.
- **Eventos:** Registros transacionais capturados no momento da ocorrência.


### 1.1 Matriz de Particionamento: Camada Bronze

| Base | Tipo de Dado | Coluna de Referência (Física) | Coluna Técnica (Partição) | Padrão de Diretório | Exemplo de Caminho |
|:---|:---|:---|:---|:---|:---|
| **atraso** | Snapshot | `dat_referencia` | `ano_mes` | `ano_mes=YYYYMM` | `ano_mes=202501` |
| **pagamento** | Evento | `dat_status_fatura` | `ano_mes` | `ano_mes=YYYYMM` | `ano_mes=202501` |
| **recarga** | Evento | `dat_insercao_credito` | `ano_mes` | `ano_mes=YYYYMM` | `ano_mes=202503` |
| **dados_cadastrais** | Snapshot | `safra` | `ano_mes` | `ano_mes=YYYYMM` | `ano_mes=202501` |
| **score_bureau_movel**| Snapshot | `safra` | `ano_mes` | `ano_mes=YYYYMM` | `ano_mes=202501` |
| **telco** | Snapshot | `safra` | `ano_mes` | `ano_mes=YYYYMM` | `ano_mes=202501` |

---

### 1.2 Decisões Técnicas Fundamentais

* **Particionamento Virtual (Hive):** A coluna técnica `ano_mes` é utilizada exclusivamente para a criação da estrutura de pastas no S3. Ela é removida do corpo do arquivo Parquet para evitar redundância, sendo "reconstruída" em tempo de execução pelos motores de consulta (DuckDB).
* **Tipagem Numérica:** A partição `ano_mes` é tratada como `BIGINT` (formato `YYYYMM`). Isso garante ordenação natural e consultas de intervalo (`BETWEEN`) mais performáticas do que strings.
* **Preservação da Data Real:** A coluna de referência original (ex: `dat_status_fatura`) é sempre mantida dentro do arquivo Parquet com tipagem `DATE` ou `TIMESTAMP`, garantindo a precisão do evento.

---

### 1.3 Mecanismo de Auditoria e Integridade

Para garantir o cumprimento desta política e a saúde dos dados para modelagem, o sistema utiliza um protocolo híbrido de **Inspeção e Observabilidade**:

* **Auditoria Técnica de Partição:** Script `inspect_partition_*.py` que realiza o *cross-check* entre a estrutura física (`ano_mes=YYYYMM`) e os dados lógicos, emitindo alerta de `⚠️ DIVERGENTE` em caso de *data leakage*.
* **Observabilidade de Pipeline (Quality Report):** Auditoria automática executada no processamento da Gold, validando:
    * **Integridade no Grão:** Unicidade e tratamento de missings.
    * **Saúde de Safra:** Representatividade volumétrica (regra 10%-90%).
    * **Overlap de Camadas:** Percentual de match entre Gold e as tabelas Silver (âncora de modelagem).
* **Relatórios de Execução:** 
    * Detalhes técnicos de integridade: [`reports/observability/integrity/`](../../reports/observability/integrity/).
    * Auditoria de safra e overlap (Quality Report): [`reports/observability/quality/pipeline/`](../../reports/observability/quality/pipeline/).

## 2. Fluxo entre Camadas

* **Bronze:** Dados organizados por `ano_mes`, refletindo a granularidade da fonte. É a "Fonte da Verdade" particionada.
* **Silver:** Realiza o saneamento e padronização. Além de respeitar o particionamento da Bronze, a Silver é o alvo principal da **Auditoria de Integridade**, garantindo que a limpeza dos dados não corrompeu a distribuição temporal das safras.
* **Gold (Labels & Features):** Camada final de modelagem. Além de respeitar o particionamento, a Gold executa o **Audit de Overlap**, garantindo a riqueza de informação entre as janelas temporais da Silver e os targets selecionados.

## 3. Governança e Retenção

Para cada partição `ano_mes`, o sistema mantém um controle de `run_id` (timestamp da execução). A política de retenção padrão é configurada para manter as execuções mais recentes, permitindo o *rollback* imediato. A trilha de auditoria dessas execuções é centralizada no diretório de [Observabilidade](../../reports/observability/).

---

**Observações Finais:** Este padrão reflete as escolhas técnicas para este ecossistema específico, priorizando a simplicidade da estrutura de diretórios em nível único e a performance de motores SQL modernos.