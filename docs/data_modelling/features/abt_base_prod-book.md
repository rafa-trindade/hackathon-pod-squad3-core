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
| `bur_` | `silver/score_bureau_movel` | Snapshot completo de scores e bureaus externos. |
| `cad_` | `silver/dados_cadastrais` | Snapshot completo de atributos demográficos e cadastrais. |
| `tel_` | `silver/telco` | Snapshot completo de variáveis de rede e consumo móvel. |
| `rec_` | `silver/recarga` | Agregações estatísticas sobre histórico de créditos. |
| `pag_` | `silver/pagamento` | Agregações estatísticas sobre liquidação de faturas. |
| `atr_` | `silver/atraso` | Agregações estatísticas sobre histórico de inadimplência. |

---

## 🏛️ Variáveis de Snapshot (Bureau, Cadastro e Telco)

As colunas com prefixos `bur_`, `cad_` e `tel_` representam a totalidade das colunas disponíveis nas respectivas tabelas Silver, capturadas via **Point-in-Time**.

* **Exaustividade:** Toda e qualquer variável presente na origem é prefixada e incluída na ABT (ex: `bur_score_01`, `cad_var_04`, `tel_var_28`).
* **Finalidade:** Alimentar algoritmos de *Feature Selection* sem viés humano na seleção inicial, garantindo que o modelo veja a "foto" do cliente no momento da safra.

---

## 📊 Dicionário de Features Agregadas (Transacionais)

As variáveis transacionais são processadas para capturar a **velocidade** e a **tendência** do comportamento do cliente através de múltiplas janelas de observação (30, 60 e 90 dias) e o acumulado geral.



### 1. Comportamento de Recarga (`rec_`)
| Sufixo da Variável | Janelas Disponíveis | Descrição |
| :--- | :--- | :--- |
| `_qtd_...` | l30d, l60d, l90d, **geral** | Quantidade de recargas no período. |
| `_vlr_total_...` | l30d, l60d, l90d, **geral** | Soma financeira total das recargas no período. |
| `_vlr_avg_...` | l30d, l60d, l90d, **geral** | Ticket médio das recargas no período. |
| `_vlr_min_...` | l30d, l60d, l90d, **geral** | Valor da menor recarga identificada no período. |
| `_vlr_max_...` | l30d, l60d, l90d, **geral** | Valor da maior recarga identificada no período. |
| `_dat_primeira/ultima`| Histórico Total | Datas dos eventos extremos (Antiguidade e Recência). |
| `_qtd_canais_distintos`| Histórico Total | Diversidade de canais de recarga utilizados. |

### 2. Comportamento de Pagamento (`pag_`)
| Sufixo da Variável | Janelas Disponíveis | Descrição |
| :--- | :--- | :--- |
| `_vlr_total_...` | l30d, l60d, l90d, **geral** | Volume total pago em faturas no período. |
| `_vlr_avg_...` | l30d, l60d, l90d, **geral** | Média dos pagamentos realizados no período. |
| `_vlr_min/max_...` | l30d, l60d, l90d, **geral** | Extremos de valores pagos no período. |
| `_qtd_faturas_...` | l30d, l60d, l90d, **geral** | Total de faturas liquidadas no período. |
| `_qtd_vezes_com_juros`| Histórico Total | Frequência de pagamentos com encargos por atraso. |

### 3. Perfil de Atraso e Risco (`atr_`)
| Sufixo da Variável | Janelas Disponíveis | Descrição |
| :--- | :--- | :--- |
| `_vlr_max_...` | l30d, l60d, l90d, **geral** | Maior saldo em aberto registrado no período. |
| `_vlr_acumulado_...` | l30d, l60d, l90d, **geral** | Soma de valores que entraram em atraso no período. |
| `_qtd_faturas_atr_...`| l30d, l60d, l90d, **geral** | Quantidade de faturas inadimplentes no período. |
| `_dat_ultima_ref` | Histórico Total | Data da última ocorrência de atraso registrada. |

---

## ⏳ Governança de Janelas (Lookback)

* **Regra de Ouro:** Todas as variáveis transacionais respeitam a condição `Data do Evento < Safra`.
* **Maturidade:** A base âncora é capturada em **D+4** para garantir a estabilidade dos dados transacionais da camada Silver antes da consolidação na Gold.



> 💡 **Como interpretar a nomenclatura das variáveis:**
> O padrão seguido é: `{prefixo}_{métrica}_{janela/tipo}`.
> - **`rec_vlr_avg_l60d`**: Valor médio de recarga nos últimos 60 dias pré-safra.
> - **`pag_vlr_total_geral`**: Soma total de pagamentos em todo o histórico (18 meses).
> - **`atr_vlr_max_hist_geral`**: Maior valor de atraso registrado em todo o histórico disponível.