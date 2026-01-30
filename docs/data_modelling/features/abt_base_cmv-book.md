# 📖 Book de Variáveis ABT CMV - Camada Gold (`abt_base_cmv`)

Este documento é o dicionário de referência da Analytical Base Table (ABT) focada no produto CMV. A estrutura segue o princípio de **Mesa Farta**, disponibilizando todas as features das camadas Silver prefixadas por origem e janela temporal, filtradas estritamente pelo público presente no Bureau.

---

## 🛡️ Protocolo de Uso e Anti-Leakage

* **Features Permitidas:** Prefixos `bur_`, `cad_`, `tel_`, `rec_`, `pag_`, `atr_`.
* **Target (Proibido no Treino):** Coluna `fpd`.
* **Identificadores (Chaves):** `num_cpf`, `safra`, `prod`, `ano_mes`.
* **Metadados (Ignorar):** `run_id`, `ingestion_ts`.

---

## 🛠️ Chaves Primárias e Identificadores (Grão)

| Variável | Tipo | Descrição |
| :--- | :--- | :--- |
| `num_cpf` | VARCHAR | Identificador único do cliente (Hash/Anonimizado). |
| `safra` | DATE | Data da geração do score no Bureau ( Snapshot Date). |
| `prod` | VARCHAR | Código do produto (Fixo em CMV para esta ABT). |
| `flag_instalacao` | VARCHAR | Tipo de instalação/origem do cliente (Enriquecimento Telco). |
| `fpd` | BOOLEAN | **Target:** Indicador de inadimplência no primeiro pagamento. |
| `ano_mes` | BIGINT | Partição física no Data Lake (Formato YYYYMM). |

---

## 🧬 Mapeamento de Prefixos e Origens

| Prefixo | Tabela Origem (Silver) | Estratégia de Captura |
| :--- | :--- | :--- |
| `bur_` | `silver/score_bureau_movel` | **Âncora Principal:** Snapshot completo de scores e bureaus externos CMV. |
| `cad_` | `silver/dados_cadastrais` | Snapshot completo de atributos demográficos e cadastrais. |
| `tel_` | `silver/telco` | Snapshot completo de variáveis de rede e consumo móvel. |
| `rec_` | `silver/recarga` | Agregações estatísticas sobre histórico de créditos. |
| `pag_` | `silver/pagamento` | AAgregações estatísticas sobre liquidação de faturas. |
| `atr_` | `silver/atraso` | Agregações estatísticas sobre histórico de inadimplência. |

---

## 🏛️ Variáveis de Snapshot (Bureau, Cadastro e Telco)

As colunas com prefixos `bur_`, `cad_` e `tel_` representam a totalidade das colunas disponíveis nas respectivas tabelas Silver, capturadas via **Point-in-Time Join** baseado na safra do Bureau.


* **Foco na Amplitude (CMV):** Diferente da ABT de Controle, os atributos `tel_` aqui incluídos referem-se ao público de **Expansão** (identificados via Bureau), garantindo que o modelo aprenda o padrão de risco do produto móvel mesmo em cenários de prospecção.
* **Finalidade:** Alimentar algoritmos de *Feature Selection* (ex: SHAP, Permutation Importance) para identificar os drivers de risco específicos do público CMV.

---

## 📊 Dicionário de Features Agregadas (Transacionais)

As variáveis transacionais são processadas para capturar a **velocidade** e a **tendência** do comportamento do cliente através de múltiplas janelas de observação (30, 60 e 90 dias) e o acumulado geral.

> 💡 **Legenda de Nomenclatura:** `{prefixo}_{métrica}_{janela}`
> * **`rec_vlr_avg_l60d`**: Valor médio de recarga nos últimos 60 dias pré-safra.

### 1. Comportamento de Recarga (`rec_`)
| Sufixo da Variável | Janelas Disponíveis | Tipo | Descrição |
| :--- | :--- | :--- | :--- |
| `_qtd_...` | l30d, l60d, l90d, **geral** | INTEGER | Quantidade de recargas no período. |
| `_vlr_total_...` | l30d, l60d, l90d, **geral** | DOUBLE | Soma financeira total das recargas no período. |
| `_vlr_avg_...` | l30d, l60d, l90d, **geral** | DOUBLE | Ticket médio das recargas no período. |
| `_vlr_min_...` | l30d, l60d, l90d, **geral** | DOUBLE | Valor da menor recarga identificada no período. |
| `_vlr_max_...` | l30d, l60d, l90d, **geral** | DOUBLE | Valor da maior recarga identificada no período. |
| `_vlr_std_...` | l30d, l60d, l90d, **geral** | DOUBLE | Desvio padrão dos valores de recarga no período (volatilidade). |
| `_vlr_coef_var_...` | l30d, l60d, l90d | DOUBLE | Coeficiente de variação dos valores de recarga no período. |
| `_ratio_qtd_l30d_l60d` | Comparativo | DOUBLE | Razão entre a quantidade de recargas nos últimos 30d vs 60d. |
| `_ratio_qtd_l60d_l90d` | Comparativo | DOUBLE | Razão entre a quantidade de recargas nos últimos 60d vs 90d. |
| `_ratio_vlr_l30d_l60d` | Comparativo | DOUBLE | Razão entre o valor total recarregado nos últimos 30d vs 60d. |
| `_ratio_vlr_l60d_l90d` | Comparativo | DOUBLE | Razão entre o valor total recarregado nos últimos 60d vs 90d. |
| `_flag_sem_recarga_...` | l30d, l60d, l90d | BOOLEAN | Indicador binário de ausência de recargas no período. |
| `_dat_primeira` | Histórico Total | DATE | Data da primeira recarga registrada (antiguidade). |
| `_dat_ultima` | Histórico Total | DATE | Data da última recarga registrada (recência). |
| `_dias_desde_primeira` | Histórico Total | INTEGER | Dias entre a primeira recarga e a data de referência. |
| `_dias_desde_ultima` | Histórico Total | INTEGER | Dias entre a última recarga e a data de referência. |
| `_qtd_canais_distintos` | Histórico Total | INTEGER | Diversidade de canais de recarga utilizados. |



### 2. Comportamento de Pagamento (`pag_`)
| Sufixo da Variável | Janelas Disponíveis | Tipo | Descrição |
| :--- | :--- | :--- | :--- |
| `_vlr_total_...` | l30d, l60d, l90d, **geral** | DOUBLE | Volume total pago em faturas no período. |
| `_vlr_avg_...` | l30d, l60d, l90d, **geral** | DOUBLE | Média dos pagamentos realizados no período. |
| `_vlr_min_...` | l30d, l60d, l90d, **geral** | DOUBLE | Menor valor pago em fatura no período. |
| `_vlr_max_...` | l30d, l60d, l90d, **geral** | DOUBLE | Maior valor pago em fatura no período. |
| `_vlr_std_...` | l30d, l60d, l90d | DOUBLE | Desvio padrão dos valores pagos no período. |
| `_qtd_faturas_...` | l30d, l60d, l90d, **geral** | INTEGER | Total de faturas liquidadas no período. |
| `_ticket_medio_...` | l30d, l60d, l90d, **geral** | DOUBLE | Valor médio pago por fatura no período. |
| `_share_faturas_com_juros_...` | l30d, l60d, l90d, **geral** | DOUBLE | Proporção de faturas pagas com juros ou multas no período. |
| `_flag_sem_pagamento_...` | l30d, l60d, l90d | BOOLEAN | Indicador binário de ausência de pagamentos no período. |
| `_qtd_vezes_com_juros` | Histórico Total | INTEGER | Frequência absoluta de pagamentos com encargos por atraso. |
| `_dias_desde_ultimo_pagamento` | Histórico Total | INTEGER | Dias desde o último pagamento registrado. |



### 3. Perfil de Atraso e Risco (`atr_`)
| Sufixo da Variável | Janelas Disponíveis | Tipo | Descrição |
| :--- | :--- | :--- | :--- |
| `_vlr_max_...` | l30d, l60d, l90d, **geral** | DOUBLE | Maior saldo em aberto registrado no período. |
| `_vlr_acumulado_...` | l30d, l60d, l90d, **geral** | DOUBLE | Soma de valores que entraram em atraso no período. |
| `_qtd_faturas_atrasadas_...` | l30d, l60d, l90d, **geral** | INTEGER | Quantidade de faturas inadimplentes no período. |
| `_ticket_medio_...` | l30d, l60d, l90d, **geral** | DOUBLE | Valor médio por fatura em atraso no período. |
| `_flag_atraso_...` | l30d, l60d, l90d | BOOLEAN | Indicador binário de ocorrência de atraso no período. |
| `_flag_recorrente_...` | l30d, l60d, l90d | BOOLEAN | Indicador de reincidência de atraso no período. |
| `_dat_ultima_ref` | Histórico Total | DATE | Data da última ocorrência de atraso registrada. |
| `_dias_desde_ultimo_atraso` | Histórico Total | INTEGER | Dias desde o último evento de atraso registrado. |

> 📐 **Nota Estatística**  
> As métricas de desvio padrão e coeficiente de variação são calculadas sobre a população observada em cada janela, sem aplicação de inferência estatística.

