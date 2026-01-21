# 📖 Book de Variáveis ABT - Camada Gold (`abt_base_prod`)

Este documento contém o dicionário completo de variáveis da Analytical Base Table (ABT). A estrutura segue o princípio de **Mesa Farta**, disponibilizando todas as features disponíveis nas camadas Silver com prefixos de origem e tratamento de janela temporal (Point-in-Time).

---

## 🛠️ Chaves Primárias e Identificadores (Grão)

| Variável | Tipo | Descrição |
| :--- | :--- | :--- |
| `num_cpf` | VARCHAR | Identificador único do cliente (Hash/Anonimizado). |
| `safra` | DATE | Data de referência da observação (Snapshot Date). |
| `prod` | VARCHAR | Código do produto associado ao registro. |
| `fpd` | BOOLEAN | **Target:** Indicador de inadimplência no primeiro pagamento. |
| `ano_mes` | BIGINT | Partição física no Data Lake (Formato YYYYMM). |

---

## 🧬 Mapeamento de Prefixos e Origens

| Prefixo | Tabela Origem (Silver) | Estratégia de Captura |
| :--- | :--- | :--- |
| `rec_` | `silver/recarga` | Agregações estatísticas sobre histórico de créditos. |
| `pag_` | `silver/pagamento` | Agregações estatísticas sobre liquidação de faturas. |
| `atr_` | `silver/atraso` | Agregações estatísticas sobre histórico de inadimplência. |
| `cad_` | `silver/dados_cadastrais` | Snapshot completo de atributos demográficos e cadastrais. |
| `tel_` | `silver/telco` | Snapshot completo de variáveis de rede e consumo móvel. |
| `bur_` | `silver/score_bureau_movel` | Snapshot completo de scores e bureaus externos. |

---

## 📊 Dicionário de Features Agregadas (Transacionais)

Diferente das bases cadastrais, estas variáveis são processadas via agregação para resumir o comportamento histórico de até 18 meses em uma única linha.

### 1. Comportamento de Recarga (`rec_`)
| Variável | Descrição |
| :--- | :--- |
| `rec_qtd_total` | Contagem total de recargas no histórico pré-safra. |
| `rec_vlr_total` | Soma financeira total de recargas no histórico. |
| `rec_vlr_avg` | Ticket médio das recargas realizadas. |
| `rec_vlr_min` | Valor da menor recarga identificada. |
| `rec_vlr_max` | Valor da maior recarga identificada. |
| `rec_dat_primeira` | Data da primeira recarga registrada no Lake para o cliente. |
| `rec_dat_ultima` | Data da recarga mais recente antes da data da safra. |
| `rec_qtd_canais_distintos` | Diversidade de canais de recarga utilizados (PDV, App, etc). |

### 2. Comportamento de Pagamento (`pag_`)
| Variável | Descrição |
| :--- | :--- |
| `pag_vlr_total` | Volume total pago em faturas no período de lookback. |
| `pag_vlr_avg` | Média ponderada dos pagamentos realizados. |
| `pag_vlr_min` | Menor pagamento registrado. |
| `pag_vlr_max` | Maior pagamento registrado. |
| `pag_qtd_faturas` | Total de faturas liquidadas no histórico. |
| `pag_qtd_vezes_com_juros` | Frequência de pagamentos que incluíram encargos por atraso. |

### 3. Perfil de Atraso e Risco (`atr_`)
| Variável | Descrição |
| :--- | :--- |
| `atr_vlr_max_hist` | Maior saldo em aberto (default) já registrado para o CPF. |
| `atr_vlr_acumulado_hist` | Soma de todos os valores que entraram em atraso no histórico. |
| `atr_qtd_faturas_atrasadas` | Quantidade de faturas distintas que apresentaram inadimplência. |
| `atr_dat_ultima_ref` | Data de referência do último registro de atraso antes da safra. |

---

## 🏛️ Variáveis de Snapshot (Cadastral, Telco e Bureau)

As colunas com prefixos `cad_`, `tel_` e `bur_` representam a totalidade das colunas disponíveis nas respectivas tabelas Silver. Elas são trazidas via snapshot **Point-in-Time**.

* **Exaustividade:** Se a tabela `silver/telco` possui 100 variáveis (`var_01` a `var_100`), a ABT conterá as 100 colunas renomeadas para `tel_var_01`, etc.
* **Finalidade:** Permitir que técnicas de *Feature Selection* (como SHAP ou Random Forest Importance) selecionem os melhores preditores sem viés humano na engenharia de dados.

---

## ⏳ Governança de Janelas (Lookback)

* **Regra de Ouro:** Todas as variáveis acima respeitam a condição `Data do Evento < Safra`.
* **Maturidade:** A base âncora é capturada em **D+4** para garantir que os dados transacionais de final de mês já estejam processados na camada Silver.
