## 📉 Visão Geral - `abt_base_cmv` (Gold Layer)

- **Entidade Principal:** Analytical Base Table (ABT) de Expansão (Amplitude de Público).
- **Grão da Tabela (Unicidade):** `num_cpf, safra, prod`
- **Âncora de Seleção:** `gold/labels_fpd_bureau` (Foco em **Amplitude e Cobertura**)
- **Chave de Particionamento:** `ano_mes` (Derivado da `safra`)

---

## ⏳ Estratégia de Governança Temporal

Este documento define as diretrizes para a construção da ABT de Expansão `abt_base_cmv`. Esta arquitetura assume a **responsabilidade técnica** de isolar o público de **CMV**, garantindo a **amplitude de público** necessária para prospecção (2.6M de registros) sem a interferência de risco de produtos residenciais (NET/DTH).

### 1. Definição da Âncora Temporal (Safra)
A âncora é o "ponto de observação" que separa o passado (features) do futuro (target).

* **Ref_Date (Safra):** Definida pelo campo `safra`. Representa o primeiro dia do mês em que o Bureau gerou o score para o cliente.
* **Ponto de Corte (Cutoff):** Para cada registro, o sistema isola o universo de dados. Apenas eventos com data **estritamente inferior** à `safra` são elegíveis para a criação de features.
* **Filtro de Público:** Diferente da versão genérica, esta ABT utiliza a `labels_fpd_bureau` como filtro mandatório, garantindo integridade estatística para o produto CMV.

---

### 2. Janelas de Lookback e Agregações Históricas
Esta ABT utiliza uma abordagem de **Mesa Farta**. Geramos métricas estatísticas (Soma, Média, Mínimo, Máximo e Contagem) para quatro horizontes temporais distintos, permitindo ao modelo identificar variações de comportamento (tendência e velocidade).

| Janela | Escopo Técnico | Objetivo |
| :--- | :--- | :--- |
| **L30D** | $T >= Safra - 30$ | Comportamento imediato e volatilidade de curtíssimo prazo. |
| **L60D** | $T >= Safra - 60$ | Estabilidade de consumo e detecção de tendências recentes. |
| **L90D** | $T >= Safra - 90$ | Visão consolidada do último trimestre (Padrão de Crédito). |
| **Geral** | Todo o período ($T < Safra$) | Perfil acumulado e *Lifetime Value* (até 18 meses). |

---

## ✅ Data Lineage - `abt_base_cmv`

### 1. Visão Geral

| Item | Valor |
| :--- | :--- |
| **Origem Primária** | `gold/labels_fpd_bureau` (Âncora de Target CMV) |
| **Fontes de Features** | `silver/score_bureau_movel`, `silver/dados_cadastrais`, `silver/telco`, `silver/recarga`, `silver/pagamento`, `silver/atraso` |
| **Feature Especial** | `flag_instalacao` (Puxada da Telco via Point-in-Time Join) |
| **Particionamento** | `ano_mes` (Coluna Técnica para Performance) |

### 2. Fluxo de Transformação: MULTI-SILVER → GOLD (ABT CMV)

**Origem:** `s3://lake/silver/**/*` e `s3://lake/gold/labels_fpd_bureau/**/*`  
**Destino:** `s3://lake/gold/abt_base_cmv/run_id={run_id}/ano_mes={YYYYMM}/*.parquet`

| Etapa | Processo | Descrição | Ações / Regras |
|------:|:---------|:----------|:---------------|
| 1 | **Fixação da Âncora Bureau** | Leitura da `labels_fpd_bureau` | Define estritamente o público CMV conforme diretriz técnica. |
| 2 | **Agregação Transacional** | Multi-Window Stats | Processamento de Recarga, Pagamento e Atraso sincronizados com a Safra Bureau. |
| 3 | **Join Point-in-Time** | Enriquecimento Snapshot | Cruzamento **Bureau > Cadastro > Telco** garantindo a foto exata da safra. |
| 4 | **Prefixagem de Features** | Rastreabilidade e DNA | Aplicação de prefixos técnicos (`bur_`, `cad_`, `tel_`, `rec_`, `pag_`, `atr_`). |
| 5 | **Auditoria de Público** | Profiling Exaustivo | Validação de que 100% da base pertence ao universo CMV/Bureau. |

---

### 3. Governança de Features (Permissões de Entrada)

#### ✅ O que ENTRA (Features Permitidas)
* **Identificadores Core:** `num_cpf`, `safra`, `prod`, `fpd`, `flag_instalacao`.
* **Atributos de Bureau:** Score 1, Score 2 e variáveis de comportamento móvel capturadas na safra.
* **Prefixos `rec_`, `pag_`, `atr_`:** Matriz completa de estatísticas transacionais pré-safra.

#### ❌ O que NÃO PODE entrar (Vazamento / Viés)
* **Outros Produtos:** Dados exclusivos de DTH/NET (evitando distorção de métricas).
* **Target:** A coluna `fpd` nunca deve ser usada como entrada do modelo.
* **Variáveis Contemporâneas:** Qualquer dado gerado no dia ou após a data da `safra`.

---

### 4. Estrutura do Grão e Cardinalidade

O grão da ABT é definido pela chave composta: **`num_cpf` + `safra` + `prod`**.

```text
📋 RESUMO TÉCNICO ABT - abt_base_cmv | ORIENTAÇÃO TÉCNICA APLICADA
----------------------------------------------------------------------------------
METRICA                       | VALOR (Execução 20260127_153240)
----------------------------------------------------------------------------------
Variáveis (Features)          | 207 colunas
Volume de Registros (N)       | 2.633.900
Cardinalidade (CPF)           | 2.565.985
Grão Definido                 | CPF + SAFRA + PROD (CMV Only)
Unicidade (PK)                | SUCESSO
Status Enriquecimento         | 100% com flag_instalacao
----------------------------------------------------------------------------------
```

> 🔗 **Acesse o log de auditoria:** [gold-abt_base_cmv-quality.log](../../../reports/observability/quality/pipeline/gold-abt_base_cmv-quality.log)
> 🔗 **Acesse o Profiling Detalhado:** [gold-abt_base_cmv-profiling.md](../../../reports/observability/profiling/gold/gold-abt_base_cmv-profiling.md)

---

### 💡 Notas de Auditoria Técnica

1. **Amplitude de Público:** Esta ABT foi construída para garantir a máxima cobertura de mercado. O público é 100% alinhado à `silver/score_bureau_movel`, eliminando o ruído estatístico de produtos residenciais. Com a volumetria de **2.6M de registros**, garantimos a **capacidade de generalização** do modelo para novos clientes.

2. **Densidade de Features:** O dataset foi expandido para **207 colunas**, cobrindo todo o espectro de bureaus, cadastro e comportamento transacional, mantendo o prefixo de origem para rastreabilidade total.

3. **Enriquecimento Estratégico:** A coluna `flag_instalacao` foi incorporada com sucesso, permitindo segmentações de origem sem a necessidade de importar a base cadastral completa de outros produtos.

4. **Garantia de Point-in-Time:** O uso de f-strings e variáveis de ambiente no pipeline DuckDB garante que a âncora `labels_fpd_bureau` seja a única fonte de verdade para CPFs e datas em todo o fluxo de agregação.

5. **Organização de Colunas (DNA do Ativo):** Estrutura otimizada para consumo analítico: `CHAVES/TARGET` > `ESTATÍSTICAS AGG (rec_, pag_, atr_)` > `BUREAU` > `CADASTRO` > `TELCO` > `METADADOS`.