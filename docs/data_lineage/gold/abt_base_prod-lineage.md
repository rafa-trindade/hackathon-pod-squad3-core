## 📉 Visão Geral - `abt_base_prod` (Gold Layer)

- **Entidade Principal:** Analytical Base Table (ABT) de Controle (Baseline).
- **Grão da Tabela (Unicidade):** `num_cpf, safra, prod`
- **Âncora de Seleção:** `gold/labels_fpd` (Responsável pela **Densidade Transacional**)
- **Chave de Particionamento:** `ano_mes` (Derivado da `safra`)

---

## ⏳ Estratégia de Governança Temporal

Este documento define as diretrizes para a construção da ABT de Controle `abt_base_prod`. Além do rigor temporal (**Point-in-Time Join**), este ativo atua como o **Padrão de Ouro** do projeto, garantindo que o modelo seja calibrado com o máximo de preenchimento de atributos internos (99.9% de densidade em variáveis `tel_`).

### 1. Definição da Âncora Temporal (Safra)
A âncora é o "ponto de observação" que separa o passado (features) do futuro (target).

* **Ref_Date (Safra):** Definida pelo campo `safra`. Representa o primeiro dia do mês de ativação ou evento do cliente.
* **Ponto de Corte (Cutoff):** Para cada registro, o sistema isola o universo de dados. Apenas eventos com data **estritamente inferior** à `safra` são elegíveis para a criação de features.
* **Objetivo:** Garantir que o modelo seja treinado exatamente com as informações que estariam disponíveis no momento da decisão de crédito.

---

### 2. Janelas de Lookback e Agregações Históricas
Esta ABT utiliza uma abordagem de **Mesa Farta**. Para cada métrica estatística (Soma, Média, Mínimo, Máximo e Contagem), geramos colunas específicas para quatro horizontes temporais distintos, permitindo ao modelo identificar variações de comportamento (tendência e velocidade).

| Janela | Escopo Técnico | Objetivo |
| :--- | :--- | :--- |
| **L30D** | $T >= Safra - 30$ | Comportamento imediato e volatilidade de curtíssimo prazo. |
| **L60D** | $T >= Safra - 60$ | Estabilidade de consumo e detecção de tendências recentes. |
| **L90D** | $T >= Safra - 90$ | Visão consolidada do último trimestre (Padrão de Crédito). |
| **Geral** | Todo o período ($T < Safra$) | Perfil acumulado e *Lifetime Value* (até 18 meses). |

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
| **Fontes de Features** | `silver/score_bureau_movel`, `silver/dados_cadastrais`, `silver/telco`, `silver/recarga`, `silver/pagamento`, `silver/atraso` |
| **Versionamento** | `run_id` (Isolamento de Execução) |
| **Particionamento** | `ano_mes` (Coluna Técnica) |

### 2. Fluxo de Transformação: MULTI-SILVER → GOLD (ABT)

**Origem:** `s3://lake/silver/**/*` e `s3://lake/gold/labels_fpd/**/*`  
**Destino:** `s3://lake/gold/abt_base_prod/run_id={run_id}/ano_mes={YYYYMM}/*.parquet`

| Etapa | Processo | Descrição | Ações / Regras |
|------:|:---------|:----------|:---------------|
| 1 | **Fixação da Âncora** | Leitura da `labels_fpd` | Define os CPFs e as Safras que devem ser processadas (Target persistente). |
| 2 | **Agregação Transacional** | Multi-Window Stats | Processamento de Recarga, Pagamento e Atraso com janelas 30, 60, 90 e Geral. |
| 3 | **Join Point-in-Time** | Enriquecimento Snapshot | Cruzamento na ordem **Bureau > Cadastro > Telco** garantindo a foto exata da safra. |
| 4 | **Prefixagem de Features** | Rastreabilidade e DNA | Aplicação de prefixos técnicos (`bur_`, `cad_`, `tel_`, `rec_`, `pag_`, `atr_`). |
| 5 | **Auditoria Técnica** | Profiling Exaustivo | Geração de diagnóstico com volumetria, cardinalidade, missings e outliers (3 Sigma). |

---

### 3. Governança de Features (Permissões de Entrada)

Para maximizar o poder preditivo, a ABT traz **todas as colunas** das fontes originais, respeitando as restrições de segurança:

#### ✅ O que ENTRA (Features Permitidas)
* **Prefixos `bur_`, `cad_`, `tel_`:** Atributos brutos capturados no snapshot da safra.
* **Prefixos `rec_`, `pag_`, `atr_`:** Matriz completa de estatísticas replicada para cada janela temporal (`_l30d`, `_l60d`, `_l90d` e `_geral`).

#### ❌ O que NÃO PODE entrar (Vazamento / Leakage)
* **Target:** A coluna `fpd` é a variável resposta e nunca deve ser usada como entrada do modelo.
* **Eventos Contemporâneos:** Qualquer evento ocorrido no mesmo dia ou após a data da `safra`.
* **Metadados:** Colunas de infraestrutura (`ingestion_ts`, `run_id`) devem ser ignoradas no treino.

---

### 4. Estrutura do Grão e Cardinalidade

O grão da ABT é definido pela chave composta: **`num_cpf` + `safra` + `prod`**.



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

> 🔗 **Acesse o Profiling Detalhado:** [gold-abt_base_prod-profiling.md](../../../reports/observability/profiling/gold/gold-abt_base_prod-profiling.md)


---

### 💡 Notas de Auditoria Técnica

1. **Estratégia de Dados Completos:** Nenhuma informação foi descartada durante a criação desta tabela. Decidimos entregar todas as colunas disponíveis para que o modelo identifique sozinho quais são as informações mais importantes para prever o comportamento do cliente (Abordagem *Mesa Farta*).
   
2. **Qualidade da Base (Padrão de Ouro):** O profiling confirma que **99.9% dos registros** possuem informações transacionais completas. Isso garante a calibração do modelo em um ambiente de máxima fidelidade de atributos.

3. **Monitoramento de Valores Extremos:** O sistema identifica automaticamente valores muito fora do comum (Outliers) através do método de 3 Sigmas ($\mu \pm 3\sigma$). Esse alerta serve para que a equipe de modelagem decida por ajustes de *Capping* antes de iniciar o treinamento, evitando distorções.

4. **Garantia de Não Repetição:** Validamos que não existem linhas duplicadas para o mesmo cliente, na mesma safra e para o mesmo produto. Isso confirma que cada linha da tabela representa um evento único e confiável.

5. **Densidade Temporal (Multi-Window):** Esta ABT entrega a "velocidade" do cliente. Ao comparar janelas curtas (30d, 60d, 90d) com o histórico longo (_geral), o modelo consegue identificar automaticamente sinais de melhora ou deterioração financeira antes da ocorrência do default.

6. **Organização e Mix de Produtos:** A estrutura foi desenhada para permitir o **Isolamento de Risco**, facilitando a identificação de disparidades de FPD entre o produto móvel (CMV) e produtos residenciais (NET/DTH), conforme detectado no diagnóstico de governança.