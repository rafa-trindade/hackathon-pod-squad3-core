# 📖 Dicionário de Dados Silver: `recarga`

Este documento descreve a estrutura técnica e funcional da tabela de **Recarga** na camada Silver. Esta entidade detalha o histórico de inserção de créditos, bônus e o comportamento de consumo pré-pago e controle.

---

## 🛠️ Grão da Tabela (Unicidade)

O grão desta tabela é definido pela combinação das seguintes chaves, garantindo o rastreio individual de cada transação de crédito:
* `num_cpf` + `dat_insercao_credito` + `hor_insercao_credito`

---

## 🧬 Dicionário de Atributos

### 🔑 Chaves e Identificadores
| Variável | Tipo | Descrição |
| :--- | :--- | :--- |
| `num_cpf` | VARCHAR | **Coluna Mascarada (LGPD):** Identificador único do cliente (Hash). |
| `dw_num_cliente` | VARCHAR | Identificador numérico do cliente no Data Warehouse. |
| `dw_num_ntc` | VARCHAR | Identificador único da linha telefônica (NTC). |
| `dat_insercao_credito` | DATE | Data em que o crédito foi inserido no sistema. |
| `hor_insercao_credito` | BIGINT | Hora da transação em **segundos decorridos desde a meia-noite** (Padrão SAS). |

---

### 💰 Valores e Finanças
| Variável | Tipo | Descrição |
| :--- | :--- | :--- |
| `val_credito_inserido` | DOUBLE | Valor nominal do crédito principal adquirido. |
| `val_bonus` | DOUBLE | Valor de bônus concedido na transação. |
| `val_real` | DOUBLE | Valor monetário total processado na operação. |
| `valor_sos` | DOUBLE | Valor referente a créditos de emergência (SOS Recarga). |
| `flag_sos` | BOOLEAN | Indicador se a transação é uma recarga de emergência (SOS). |

---

### 🏢 Canais e Instituições
| Variável | Tipo | Descrição |
| :--- | :--- | :--- |
| `cod_canal_aquisicao` | VARCHAR | Código técnico do canal de venda. |
| `dsc_canal_aquisicao` | VARCHAR | Descrição do canal de aquisição (Ex: Online, EPAY). |
| `dw_instituicao` | VARCHAR | Identificador da instituição financeira ou parceiro. |
| `dsc_instituicao` | VARCHAR | Nome da instituição processadora da recarga. |
| `ind_metodo_pagamento` | VARCHAR | Indicador do método utilizado para o pagamento da recarga. |
| `dw_forma_pagamento` | VARCHAR | Identificador técnico da forma de pagamento. |
| `dsc_forma_pagamento` | VARCHAR | Descrição da forma de pagamento (Ex: Online, Cartão). |

---

### 📋 Planos e Promoções
| Variável | Tipo | Descrição |
| :--- | :--- | :--- |
| `dw_plano_tarifacao` | VARCHAR | Identificador técnico do plano tarifário. |
| `dsc_plano_tarifacao` | VARCHAR | Nome do plano tarifário (Ex: Prezão, Controle). |
| `cod_promocao` | VARCHAR | Código identificador de promoção aplicada. |
| `dsc_promocao` | VARCHAR | Descrição da promoção vinculada à recarga. |
| `dw_tipo_recarga` | VARCHAR | Identificador do tipo de recarga efetuada. |
| `dsc_tipo_recarga` | VARCHAR | Descrição do tipo (Ex: Principal, Adicional). |
| `cod_grupo_cartao` | VARCHAR | Código do grupo de segmentação de cartão/crédito. |
| `dsc_grupo_cartao_wpp` | VARCHAR | Descrição da segmentação do grupo para canais digitais. |

---

### 🛠️ Status e Tecnologia
| Variável | Tipo | Descrição |
| :--- | :--- | :--- |
| `cod_plataforma_atu` | VARCHAR | Código da plataforma tecnológica atual. |
| `dsc_plataforma_atu` | VARCHAR | Descrição da plataforma (Ex: Pré-pago, Controle). |
| `cod_status_plataforma` | VARCHAR | Código do status da linha na plataforma. |
| `dsc_status_plataforma` | VARCHAR | Descrição do status (Ex: Ativo, Expirado). |
| `cod_tecnologia_dw` | VARCHAR | Código da tecnologia de rede (Ex: GSM). |
| `dsc_tecnologia` | VARCHAR | Descrição da tecnologia de rede. |
| `dw_tipo_insercao` | VARCHAR | Código do método de inserção do crédito. |
| `dsc_tipo_insercao` | VARCHAR | Descrição do método de inserção (Ex: Virtual, Físico). |
| `cod_tipo_credito` | VARCHAR | Código do tipo de crédito (Ex: Online). |
| `dsc_tipo_credito` | VARCHAR | Descrição do tipo de crédito. |

---

### ⚙️ Metadados de Processamento
| Variável | Tipo | Descrição |
| :--- | :--- | :--- |
| `ingestion_ts` | TIMESTAMP | Data e hora exata do processamento na camada Silver. |
| `run_id` | BIGINT | Identificador único da execução da pipeline. |
| `ano_mes` | BIGINT | Partição física do dado no Data Lake (YYYYMM). |

---

> **Finalidade:** Estes atributos compõem o histórico transacional de recargas, permitindo o cálculo de métricas de recência, frequência e valor médio de crédito para a modelagem de propensão na camada Gold.