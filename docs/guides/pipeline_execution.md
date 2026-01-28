# ▶️ Guia de Execução da Pipeline de Dados

Este documento descreve os **pré-requisitos técnicos**, **configuração do ambiente** e o **passo a passo para execução da pipeline de dados** do Lakehouse, cobrindo desde a camada **RAW** até **GOLD**, incluindo **qualidade, profiling, inspeções e transformações**.


## 🖥️ Requisitos de Infraestrutura (Recomendado)

Para garantir **performance**, **estabilidade** e **reprodutibilidade**, recomenda-se o seguinte ambiente:

- **Sistema Operacional:** Linux (Ubuntu 22.04+ ou similar)
- **CPU:** ≥ **6 vCPUs** (ou Cores físicos)
- **Memória RAM:** ≥ **12 GB**
- **Armazenamento:** ≥ **100 GB SSD** (Preferencialmente **NVMe**)


### 🔍 Justificativa Técnica

1. **Paralelismo DuckDB:** O motor analítico está configurado para operar com **5 threads paralelas**. A disponibilidade de 6 vCPUs permite que o processamento de dados ocorra em capacidade máxima, mantendo 1 núcleo livre para operações de sistema e I/O.
2. **Gerenciamento de Memória:** O DuckDB está configurado com limite de **6 GB de RAM**. A especificação de 12 GB no host garante estabilidade para o Sistema Operacional e permite que o Linux utilize o excedente para cache de arquivos, acelerando o I/O.
3. **Operações Vetorizadas:** O DuckDB se beneficia da baixa latência de I/O (SSD/NVMe) para acelerar joins e agregações complexas nas camadas Silver e Gold.
4. **Ambiente Unix:** A orquestração utiliza **Shell Script (Bash)** e comandos nativos para gestão de logs e permissões.


## 🐍 Configuração do Ambiente

### 1. Dependências
Certifique-se de estar utilizando `python >= 3.10`. 

Na raiz do projeto, execute:
```bash
pip install -r requirements.txt
```
> 💡 Recomenda-se o uso de virtualenv para isolamento do ambiente.

---

### 2. Variáveis de Ambiente

O projeto utiliza um arquivo `.env` para gerenciar credenciais sensíveis (S3/MinIO). 

- **Solicite as credenciais** de acesso ao administrador do Lake.
- **Configure o arquivo:** Na raiz do projeto, renomeie o arquivo de exemplo e preencha com as chaves recebidas:
```bash
cp .env.example .env
```


## ▶️ Execução da Pipeline

### 1. Conceder permissão de execução:

```bash
chmod +x bin/run_pipeline.sh
```

---

### 2. Iniciar processamento:

```text
bin/run_pipeline.sh
```

## 🧾 Logs e Observabilidade

### Logs Locais
A cada execução, um log detalhado é gerado em: 
`bin/reports/pipeline_run_YYYYMMDD.log`

O log registra o status de cada etapa (`PROCESS`, `SUCCESS`, `ERROR`) e a duração exata de cada step.

---

### Persistência no Data Lake
Ao final da execução, todos os relatórios de qualidade, profiling e o próprio log de execução são automaticamente sincronizados com o S3 para fins de auditoria e governança:

> `s3://lake/observability/reports/run_id=YYYYMMDD/`


## 🛡️ Nota de Confiabilidade (Reliability)

- **Idempotência:** A pipeline pode ser reexecutada para a mesma safra; a geração de uma nova `run_id` garantirá a unicidade técnica e evitará conflitos de dados.
- **Fail-Fast:** Em caso de erro em qualquer etapa (ex: falha em um contrato de dados Pandera ou erro de script), a execução é interrompida imediatamente para evitar a propagação de dados inconsistentes para as camadas seguintes.


## ✅ Resultado Esperado

Ao final de uma execução bem-sucedida, o ambiente apresentará:
- **Camadas Medallion:** Bronze, Silver e Gold atualizadas no S3.
- **Evidências Técnicas:** Relatórios de Profiling e Integridade gerados e atualizados.
- **Governança:** Master Log persistido no Lake (S3) vinculado ao `run_id` da execução.