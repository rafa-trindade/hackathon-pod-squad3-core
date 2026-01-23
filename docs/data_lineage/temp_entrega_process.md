# 📖 Documentação de Data Lineage & Processamento de Dados
## Arquitetura Medallion (RAW → BRONZE → SILVER → GOLD)

Este documento consolida, em uma **visão única**, as **etapas de processamento de dados** aplicadas no Lakehouse, considerando tanto os **fluxos comuns** quanto as **variações específicas por entidade**, conforme definido na documentação técnica individual de cada domínio, disponível no repositório oficial de lineage.

> **Escopo:** transformação, organização e enriquecimento de dados  
> **Fora de escopo:** logs técnicos, métricas de execução e evidências operacionais detalhadas

## 🏗️ 1. Visão Global do Fluxo de Dados

Todas as entidades seguem o padrão arquitetural **Medallion (RAW → BRONZE → SILVER → GOLD)**, com responsabilidades bem definidas por camada.  

Esta visão representa o **fluxo lógico comum** do Lakehouse, independentemente de particularidades de implementação ou exceções controladas por tipo de dado.

![Arquitetura Micro](../images/data_architecture/arquitetura_micro.png)

| Camada | Papel no Pipeline |
|------|------------------|
| **RAW** | Persistência do dado original, sem transformação |
| **BRONZE** | Padronização técnica e organização física |
| **SILVER** | Qualidade, unicidade e enriquecimento |
| **GOLD** | Camada semântica para modelagem (ABTs e Labels ML-ready) |

Entidades contempladas neste fluxo:
- `atraso`
- `pagamento`
- `recarga`
- `dados_cadastrais`
- `score_bureau_movel`
- `telco`
- dimensões de suporte (`atraso_dim`, `recarga_dim`)

---

## 📥 2. Camada RAW - Ingestão

### Objetivo
Garantir a **preservação integral** dos dados recebidos das fontes, sem qualquer modificação estrutural ou semântica.

### Características
- Arquivos no formato original (`parquet` ou `csv`)
- Nenhuma deduplicação
- Nenhuma alteração de schema
- Fonte oficial para reprocessamentos

**Estrutura:**
```bash
s3://lake/raw/{entidade}/*
```

---

## 🥉 3. Processamento Global - RAW → BRONZE

Este estágio é **comum a todas as entidades de negócio** e tem como objetivo a **padronização técnica**, mantendo a imutabilidade dos dados.

**Origem:** `s3://lake/raw/{entidade}/*.parquet`  
**Destino:** `s3://lake/bronze/{entidade}/run_id={run_id}/ano_mes={YYYYMM}/*.parquet`

---

### 3.1 🔁 Etapas Comuns de Processamento (Todas as Entidades)

| Etapa | Processo | Descrição |
|----:|---------|-----------|
| 1 | **Normalization (Lowercase)** | Conversão de todos os nomes de colunas para minúsculo, eliminando ambiguidades de *case-sensitivity*. |
| 2 | **Tipagem Forte** | Aplicação de `CAST` explícito para tipos primitivos (`DATE`, `INTEGER`, `DOUBLE`, `BOOLEAN`) com base no profiling da origem. |
| 3 | **Metadados Técnicos** | Inclusão de colunas técnicas (`ingestion_ts`, `run_id`) para rastreabilidade e auditoria. |
| 4 | **Particionamento Técnico Global** | Criação da coluna técnica `ano_mes = YYYYMM`, derivada da data de referência principal da entidade, padronizando a organização física no Data Lake. |


---

### 3.2 🧩 Tratamento Diferenciado - Dimensões Técnicas

As tabelas dimensionais possuem comportamento distinto das tabelas 'Fato', pois representam **cadastros estáveis e de baixo volume**.

**Entidades:** `atraso_dim` `recarga_dim`

**Origens:** `s3://lake/raw/{dimensao}/*.csv`  
**Destinos:** `s3://lake/bronze/{dimensao}/*.parquet`

| Regra | Descrição | Justificativa |
|---|---|---|
| **Estrutura Flat** | Arquivo único, sem particionamento por data ou `run_id`. | Simplifica manutenção e JOINs laterais. |
| **Preservação de Case** | Manutenção do formato original das chaves. | Evita falhas de correspondência na Silver. |
| **Snapshot Técnico** | Representam o estado completo do cadastro. | Dimensões não são versionadas por execução. |

---

## 🥈 4. Processamento por Entidade - BRONZE → SILVER

Na camada Silver, os dados passam a atender **requisitos de qualidade, unicidade e semântica analítica**, respeitando o grão específico de cada entidade.

**Origem:** `s3://lake/bronze/{entidade}/**/*.parquet`  
**Destino:** `s3://lake/silver/{entidade}/run_id={run_id}/ano_mes={YYYYMM}/*.parquet`

---

### 4.1 🎯 Estratégia de Grão e Unicidade por Entidade


A deduplicação é aplicada **por lote de carga (`run_id`)**, com base no **grão lógico de negócio** definido por entidade.  
O particionamento físico por `ano_mes` é herdado da camada Bronze.

| Entidade | Grão Técnico (Unicidade) |
|---|---|
| **Atraso** | `num_cpf, contrato, dat_referencia, num_fatura_hash, num_ent_seq_fatura` |
| **Recarga** | `num_cpf, dat_insercao_credito, hor_insercao_credito` |
| **Pagamento** | `num_cpf, contrato, seq_fatura, num_sub_seq_fatura` |
| **Dados Cadastrais** | `num_cpf, safra, prod` |
| **Score Bureau** | `num_cpf, safra, prod` |
| **Telco** | `num_cpf, safra, prod` |

---

### 4.2 🔀 Regras de Transformação Específicas

Apesar do fluxo base ser comum, algumas entidades possuem **processamentos adicionais**.

#### A) Enriquecimento via Dimensões *(Aplicável a Atraso e Recarga)*

- JOIN com tabelas dimensionais técnicas
- Inclusão de descrições legíveis ao negócio
- Mapeamento de códigos inexistentes para valores padrão (ex: *"Não Mapeado"*)
- Preservação do grão original da 'Fato' (entidades de domínio com comportamento factual)

---

#### B) Saneamento e Higienização *(Todas as Entidades)*

- Normalização de hashes técnicos associados a valores nulos
- Padronização de identificadores inválidos
- Remoção de colunas sem valor analítico (100% nulas ou obsoletas)
- Reordenação lógica do schema para consumo analítico

---

## 🧱 5. Estrutura Física de Armazenamento (Padrão Hive)

A organização física segue o padrão Hive para garantir *partition pruning* e compatibilidade com motores analíticos:

```bash
s3://lake/
├── raw/
│   └── {entidade}/
├── bronze/
│   ├── {entidade}/
│   │   └── run_id=YYYYMMDD_HHMMSS/
│   │       └── ano_mes=YYYYMM/
│   │           └── data_0.parquet
│   └── {dimensao}/
│       └── dimensao.parquet
├── silver/
│   └── {entidade}/
│       └── run_id=YYYYMMDD_HHMMSS/
│           └── ano_mes=YYYYMM/
│               └── data_0.parquet
├── gold/
│   └── {entidade}/
│       └── run_id=YYYYMMDD_HHMMSS/
│           └── ano_mes=YYYYMM/
│               └── data_0.parquet          
```

---

## 🏁 6. Resultado da Camada SILVER

Ao final do processamento na camada Silver, todas as entidades apresentam:

- **Grão técnico garantido**
- **Unicidade validada**
- **Chaves normalizadas**
- **Schema otimizado**
- **Dados prontos para análises exploratórias, agregações controladas e estruturação de ativos na camada GOLD**

Este documento consolida a **visão oficial de processamento do Lake**, servindo como **referência única** para engenharia, governança e evolução contínua da arquitetura.

> 📌 **Contrato com a Camada GOLD**  
> As entidades na camada Silver representam a **fonte única e confiável** para a construção dos ativos analíticos da camada Gold.  
>  
> Nenhuma lógica de correção, enriquecimento temporal ou reinterpretação semântica é aplicada após este ponto.  
> Toda a inteligência estatística e analítica ocorre **exclusivamente na camada GOLD**, garantindo separação clara de responsabilidades.

---

## 🥇 7. Camada GOLD - Consumo Analítico e Modelagem

A camada **GOLD** representa a **materialização final dos dados para consumo analítico e Machine Learning**, sendo responsável por entregar **ativos semânticos, estatisticamente consistentes, versionados e auditáveis**, prontos para uso pela Squad de Modelagem.

Esta camada **não contém lógica de negócio transacional**, mas sim **estruturas analíticas consolidadas**, construídas a partir das entidades Silver, respeitando rigorosamente princípios de **governança temporal, integridade estatística e reprodutibilidade**.

📌 **Os ativos Gold são determinísticos por `run_id`, permitindo a reprodução exata de qualquer experimento histórico de Machine Learning.**

---

### 7.1 🎯 Objetivos da Camada GOLD
- Centralizar **targets oficiais** de modelagem
- Disponibilizar **Analytical Base Tables (ABTs)** padronizadas
- Garantir **consistência e comparabilidade entre experimentos de Machine Learning**
- Servir como **contrato único** entre Engenharia de Dados e Ciência de Dados

---

### 7.2 📦 Ativos GOLD Disponíveis

> -------- falta validar

| Ativo | Tipo | Finalidade |
|:-----|:-----|:-----------|
| `labels_fpd` | Target | Variável resposta oficial (First Payment Default) |
| `abt_base_prod` | ABT | Base analítica para treinamento e validação de modelos |

📘 **Dicionário de Variáveis (Feature Book)**  
A descrição detalhada das variáveis, incluindo definição semântica, domínio, regra de cálculo, janela temporal e origem Silver, está documentada em:

➡️ **[Book de Variáveis - `abt_base_prod`](../data_modelling/features/abt_base_prod-book.md)**

---

### 7.3 🧬 Princípios Técnicos Aplicados

Todos os ativos da camada GOLD obedecem aos seguintes princípios:

- **Grão analítico explícito e imutável**
- **Isolamento por execução (`run_id`)**
- **Particionamento temporal (`ano_mes`)**
- **Auditoria automática de qualidade**
- **Rastreabilidade completa até a Silver**
- **Prevenção ativa de Data Leakage**

---

### 7.4 🔀 Fluxo Lógico: SILVER → GOLD

```text
Silver (Entidades de Domínio)
        ↓
Definição de Âncora (Target)
        ↓
Governança Temporal (Point-in-Time)
        ↓
Agregações Históricas (Lookbacks)
        ↓
Join Controlado Multi-Silver
        ↓
Gold (Labels e ABTs ML-Ready)
```

> ⚠️ **Escopo desta documentação**  
> Este documento não detalha a lógica interna de construção dos ativos Gold, tais como:
>
> - Estratégias de Point-in-Time Join
> - Definição de janelas de lookback
> - Regras de anti-data leakage
> - Governança de features
> - Métricas estatísticas geradas
> - Auditorias específicas por ativo
>
>📌 Essas definições fazem parte da documentação dedicada de estruturação do modelo baseline, onde cada ativo Gold é descrito de forma aprofundada, incluindo decisões estatísticas e justificativas técnicas.

---

## 📚 Documentação Complementar

### 🏗️ Data Architecture
📑 **[Manual de Arquitetura de Dados](../data_architecture/README.md)**  
Descrição da arquitetura técnica da plataforma de dados, incluindo visão macro e micro, decisões de engenharia, escolha de tecnologias e seus impactos em escalabilidade, governança, confiabilidade e observabilidade.

---

### 🧬 Data Lineage
📑 **[Manual de Lineage](../data_lineage/README.md)**  
Documentação detalhada do fluxo de dados por entidade, incluindo origem, transformações e dependências entre camadas.

---

### 🏛️ Data Governance
📑 **[Manual de Governança](../data_governance/README.md)**  
Diretrizes formais de governança aplicadas ao projeto.

---

### 🔍 Data Observability
📑 **[Manual de Observabilidade](../data_observability/README.md)**  
Referência das práticas de monitoramento e saúde do pipeline.
