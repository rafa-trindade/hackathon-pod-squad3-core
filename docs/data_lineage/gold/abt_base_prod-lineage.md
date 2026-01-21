## 📉 Visão Geral - `abt_base_prod` (Gold Layer)

- **Entidade Principal:** Analytical Base Table (ABT) para Modelagem de Crédito.
- **Grão da Tabela (Unicidade):** `num_cpf, safra, prod`
- **Âncora de Seleção:** `gold/labels_fpd` (Ponto de Observação D+4)
- **Chave de Particionamento:** `ano_mes` (Derivado da `safra`)

---

## ⏳ Estratégia de Governança Temporal

Este documento define as diretrizes para a construção da Analytical Base Table (ABT) `abt_base_prod`. O foco é garantir a integridade estatística através do **Point-in-Time Join**, permitindo o uso de todo o histórico disponível nas camadas Silver sem causar **Data Leakage**.

### 1. Definição da Âncora Temporal (Safra)
A âncora é o "ponto de observação" que separa o passado (features) do futuro (target).

* **Ref_Date (Safra):** Definida pelo campo `safra`. Representa o primeiro dia do mês de ativação ou evento do cliente.
* **Ponto de Corte (Cutoff):** Para cada registro, o sistema isola o universo de dados. Apenas eventos com data **estritamente inferior** à `safra` são elegíveis para a criação de features.
* **Objetivo:** Garantir que o modelo seja treinado exatamente com as informações que estariam disponíveis no momento da decisão de crédito.

---

### 2. Janelas de Lookback e Agregações Históricas
Diferente de modelos limitados, esta ABT utiliza uma abordagem de **Mesa Farta**, explorando os 18 meses de histórico das tabelas transacionais (`silver/recarga`, `silver/pagamento`, `silver/atraso`). 

As features são agregadas de forma exaustiva (Min, Max, Avg, Sum) conforme a semântica de cada fonte:

| Janela | Escopo Técnico | Objetivo |
| :--- | :--- | :--- |
| **L30D, L60D, L90D** | Janelas móveis pré-safra. | Capturar volatilidade e tendências de curtíssimo prazo. |
| **Total Histórico** | Todo o período disponível ($T < safra$). | Capturar o *Lifetime Value* e comportamento acumulado do cliente (até 18 meses). |

**Campos de Referência para Filtro Temporal:**
* **Recarga:** `dat_insercao_credito`
* **Pagamento:** `dat_status_fatura`
* **Atraso:** `dat_referencia`

---

## ✅ Data Lineage - `abt_base_prod`

### 1. Visão Geral

| Item | Valor |
| :--- | :--- |
| **Origem Primária** | `gold/labels_fpd` (Âncora de Target) |
| **Fontes de Features** | `silver/telco`, `silver/dados_cadastrais`, `silver/score_bureau_movel`, `silver/recarga`, `silver/pagamento`, `silver/atraso` |
| **Versionamento** | `run_id` (Isolamento de Execução) |
| **Particionamento** | `ano_mes` (Coluna Técnica) |

### 2. Fluxo de Transformação: MULTI-SILVER → GOLD (ABT)

**Origem:** `s3://lake/silver/**/*` & `s3://lake/gold/labels_fpd/**/*`  
**Destino:** `s3://lake/gold/abt_base_prod/run_id={run_id}/ano_mes={YYYYMM}/*.parquet`

| Etapa | Processo | Descrição | Ações / Regras |
|------:|:---------|:----------|:---------------|
| 1 | **Fixação da Âncora** | Leitura da `labels_fpd` | Define os CPFs e as Safras que devem ser processadas (Target persistente). |
| 2 | **Agregação Transacional** | Lookback de 18 meses | Processamento de Recarga, Pagamento e Atraso aplicando a regra $T < Safra$. |
| 3 | **Join Point-in-Time** | Enriquecimento Snapshot | Cruzamento com Cadastral, Telco e Bureau garantindo a foto exata do momento da safra. |
| 4 | **Prefixagem de Features** | Rastreabilidade e DNA | Aplicação de prefixos técnicos (`cad_`, `tel_`, `bur_`, `rec_`, `pag_`, `atr_`) para identificar origem das colunas. |
| 5 | **Auditoria Técnica** | Profiling Exaustivo | Geração de diagnóstico com volumetria, cardinalidade de CPF, missings e detecção de outliers (3 Sigma). |

---

### 3. Governança de Features (Permissões de Entrada)

Para maximizar o poder preditivo, a ABT traz **todas as colunas** das fontes originais (Mesa Farta), respeitando as restrições de segurança:

#### ✅ O que ENTRA (Features Permitidas)
* **Prefixos `cad_`:** Atributos de `silver/dados_cadastrais` (ex: `cad_idade_cli`).
* **Prefixos `tel_`:** Atributos de `silver/telco` (ex: `tel_var_28`).
* **Prefixos `bur_`:** Atributos de `silver/score_bureau_movel` (ex: `bur_score_01`).
* **Prefixos `rec_`, `pag_`, `atr_`:** Métricas agregadas (Soma, Média, Máximo, Mínimo) do transacional.

#### ❌ O que NÃO PODE entrar (Vazamento / Leakage)
* **Target:** A coluna `fpd` (First Payment Default) é a variável resposta e nunca deve ser usada como entrada.
* **Eventos Contemporâneos:** Qualquer recarga ou pagamento ocorrido no mesmo dia ou após a data da `safra`.
* **Metadados:** Colunas como `ingestion_ts` ou `run_id` (devem ser ignoradas pelo modelo para evitar viés de infraestrutura).

---

### 4. Estrutura do Grão e Cardinalidade

O grão da ABT é definido pela chave composta: **`num_cpf` + `safra` + `prod`**.

* **Reuso de CPF:** Um mesmo `num_cpf` pode aparecer em safras diferentes ou produtos diferentes.
* **Isolamento Temporal:** Devido às regras de *Point-in-Time*, a linha de um CPF na `safra_202501` terá features diferentes da linha do mesmo CPF na `safra_202410`, pois o histórico acumulado disponível em cada janela de tempo é distinto.

```text
📋 RESUMO TÉCNICO ABT - abt_base_prod | ÚLTIMA EXECUÇÃO
----------------------------------------------------------------------------------
METRICA                       | VALOR
----------------------------------------------------------------------------------
Volume de Registros (N)       | 1.321.168
Cardinalidade (CPF)           | 1.272.095
Grão Definido                 | CPF + SAFRA + PROD
Unicidade (PK)                | SUCESSO
----------------------------------------------------------------------------------
```

> 🔗 **Acesse o log de auditoria:** [gold-abt_base_prod-quality.log](../../../reports/observability/quality/pipeline/gold-abt_base_prod-quality.log)

> 🔗 **Acesse o Profiling Detalhado:** [gold-labels_fpd-quality.md](../../../reports/observability/profiling/gold/gold-abt_base_prod-profiling.md)


---

### 💡 Notas de Auditoria Técnica

1. **Estratégia de Dados Completos:** Nenhuma informação foi descartada durante a criação desta tabela. Decidimos entregar todas as colunas disponíveis para que o modelo identifique sozinho quais são as informações mais importantes para prever o comportamento do cliente.
   
2. **Qualidade da Base:** Todos os clientes listados nesta tabela possuem informações de cadastro e de crédito (Bureau) preenchidas. Isso garante que não existam registros fantasmas, permitindo que o modelo analise o perfil completo de cada CPF.

3. **Monitoramento de Valores Extremos:** O sistema identifica automaticamente valores muito fora do comum (ex: rendas ou gastos desproporcionais). Esse alerta serve para que a equipe de análise decida se deve ajustar ou limitar esses valores antes de iniciar o treinamento do modelo, evitando distorções nos resultados.

4. **Garantia de Não Repetição:** Validamos que não existem linhas duplicadas para o mesmo cliente, no mesmo mês e para o mesmo produto. Isso confirma que cada linha da tabela representa um evento único e confiável para análise.

