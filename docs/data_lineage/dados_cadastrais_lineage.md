## 📥 Ingestão - `raw/dados_cadastrais`

- **Fonte:** Externa  
- **Frequência:** Sob demanda (ingestão manual)
- **Formato:** Parquet (particionado)  
- **Volume médio:** ~75 MB por carga (105 MB descomprimido)
- **Chave técnica:** CPF (candidata)

---

## ✅ Data Lineage - `dados_cadastrais`

### 1. Visão Geral

| Item            | Valor                 |
|-----------------|-----------------------|
| Origem          | `dados_cadastrais`    |
| Domínio         | `clientes`            |
| Camadas         | Raw → Bronze → Silver |

---

### 2. Lineage por Camada

#### 2.1 RAW → BRONZE  

**Origem:** `raw/dados_cadastrais`  
**Destino:** `bronze/dados_cadastrais_*`

`raw/dados_cadastrais`
  → *normalização de colunas*
  → *normalização de tabelas*
  → *tipagem*
  → `bronze/dados_cadastrais_*`

| Etapa | Processo | Descrição | Ações / Regras | Resultado Esperado |
|------:|----------|-----------|----------------|-------------------|
| 1 | Normalização de colunas | Padronização técnica dos nomes e formatos das colunas | ex: Renomeação conforme *naming convention*; padronização de caixa; remoção de caracteres especiais | Colunas consistentes e legíveis |
| 2 | Normalização de tabelas | Padronização estrutural e nomenclatura técnica das tabelas de origem |  ex: Renomeação técnica das tabelas; alinhamento estrutural; preservação do significado original | Tabelas coerentes e padronizadas |
| 3 | Tipagem | Definição de tipos de dados adequados para cada coluna | ex: Conversão para tipos corretos (date, int, boolean etc.); validação de formatos | Dados tecnicamente consistentes |

---

#### 2.2 BRONZE → SILVER  

**Origem:** `bronze/dados_cadastrais_*`  
**Destino:** `silver/clientes`

`bronze/dados_cadastrais_*`
  → *consolidação de tabelas*
  → *deduplicação*
  → *aplicação de regras de negócio*
  → *definição de chaves semânticas*
  → `silver/clientes`

| Etapa | Processo | Descrição | Ações / Regras | Resultado Esperado |
|------:|----------|-----------|----------------|-------------------|
| 1 | Deduplicação | Eliminação de registros duplicados com base em critérios de unicidade de negócio | ex: CPF; priorizar registros ativos e mais recentes | Um único registro por cliente |
| 2 | Definição de chave técnica e chaves semânticas | Definição da chave de negócio que identifica unicamente o cliente | ex: CPF como chave; geração de hash estável quando necessário | Identificação única e consistente do cliente |

---

### 3. Observações

- RAW → BRONZE: apenas transformações técnicas, sem regras de negócio  
- BRONZE → SILVER: transformações semânticas e de negócio  
- Não há criação de surrogate keys nesta arquitetura (datalake)
- Nas camadas `RAW` e `SILVER` será realizada a **validação da qualidade dos dados**, utilizando **Pandera** para garantir conformidade com esquemas, tipos, regras de integridade e restrições de negócio
- A camada `SILVER` é a base de origem:
  - da camada `GOLD` do Data Lake (engenharia de atributos e ML)
  - da camada `SOURCE` do Data Warehouse (BI)