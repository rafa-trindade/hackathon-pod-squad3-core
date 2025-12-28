# 🔍 Data Observability - Mapeamento Prático do Projeto

Este documento mapeia como as práticas implementadas no projeto
se encaixam nos pilares clássicos de **Data Observability**.

O objetivo é demonstrar que observabilidade não depende de ferramentas específicas,
mas de **boas decisões arquiteturais, técnicas e operacionais**.

---

## 📊 O que é Data Observability

Data Observability é a capacidade de responder, de forma rápida e confiável, às perguntas:

- Os dados chegaram?
- Estão completos?
- Estão corretos?
- Mudaram de comportamento?
- De onde vieram?
- Onde estão sendo usados?
- Posso reprocessar?

---

## 🧱 Pilares Clássicos de Data Observability

1. Freshness (Atualização)
2. Volume
3. Schema
4. Distribution
5. Lineage
6. Quality
7. Reliability / Reprocessamento

---

## 🗺️ Mapeamento do Projeto por Pilar

### 1️⃣ Freshness (Atualização)

**Como é atendido:**
- Cada execução gera um `run_id` com timestamp
- A estrutura por runs permite identificar facilmente a última carga
- Logs explícitos indicam início, sucesso e falha de cada execução
- Freshness não é SLA de negócio, é sinal técnico

**Onde está documentado / implementado:**
- `data_lineage/dados_cadastrais_lineage`
- `data_governance/politica_retencao.md`
- Scripts de ingestão e transformação


---

### 2️⃣ Volume

**Como é atendido:**
- Contagem de linhas após cada transformação
- Registro explícito do volume processado por run
- Profiling documentado por camada

**Onde está documentado / implementado:**
- `data_profiling/`
- Logs de pipeline

---

### 3️⃣ Schema

**Como é atendido:**
- Normalização técnica na camada BRONZE
- Tipagem explícita de colunas
- Dicionário de dados por camada

**Onde está documentado / implementado:**
- `data_dictionary/`
- `data_profiling/`

---

### 4️⃣ Distribution (Distribuição dos Dados)

**Como é atendido:**
- Análises de cardinalidade
- Percentual de nulos
- Distribuição de valores documentada

**Onde está documentado / implementado:**
- `data_profiling/`
- Scripts de profiling

---

### 5️⃣ Lineage

**Como é atendido:**
- Lineage explícito por dataset
- Separação clara entre transformações técnicas e de negócio
- Documentação por camada

**Onde está documentado / implementado:**
- `data_lineage/`

---

### 6️⃣ Quality

**Como é atendido:**
- Validação de regras estruturais na camada RAW e semânticas na SILVER
- Definição clara de critérios de unicidade e elegibilidade
- Validações com Pandera

**Onde está documentado / implementado:**
- `data_governance/politica_qualidade` regra geral
- `data_quality/` - documentação dos contratos por base
- Scripts de quality

---

### 7️⃣ Reliability e Reprocessamento

**Como é atendido:**
- Retenção baseada em runs técnicas
- Limpeza executada apenas após sucesso
- Preservação de runs anteriores para rollback
- Reprocessamento idempotente
- Retenção por run substitui versionamento tradicional

**Onde está documentado / implementado:**
- `data_governance/politica_retencao.md`
- Script utilitário de pipeline `lake_retention.py`

---

## 🧠 Conclusão

Este projeto implementa Data Observability de forma **nativa**, sem dependência
de ferramentas externas, através de:

- Arquitetura bem definida
- Separação clara de responsabilidades
- Documentação consistente
- Automação operacional
- Governança aplicada via código

A observabilidade emerge como **resultado natural** das decisões de engenharia.
