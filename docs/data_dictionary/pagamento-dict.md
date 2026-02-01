# 📖 Dicionário de Dados Silver: `pagamento`

Este documento descreve a estrutura técnica e funcional da tabela de **Pagamento** na camada Silver. Esta entidade detalha a liquidação financeira das faturas, métodos de recebimento e instâncias de pagamento.

---

## 🛠️ Grão da Tabela (Unicidade)

O grão desta tabela é definido pela combinação das seguintes chaves, garantindo o rastreio individual de cada evento de liquidação:
* `num_cpf` + `contrato` + `seq_fatura` + `num_sub_seq_fatura` + `num_credito_seq`

---

## 🧬 Dicionário de Atributos

### 🔑 Chaves e Identificadores
| Variável | Tipo | Descrição |
| :--- | :--- | :--- |
| `num_cpf` | VARCHAR | **Coluna Mascarada (LGPD):** Identificador único do cliente (Hash). |
| `dw_num_cliente` | VARCHAR | Identificador numérico do cliente no Data Warehouse. |
| `contrato` | VARCHAR | Identificador único do contrato ou assinatura. |
| `seq_fatura` | VARCHAR | Sequencial da fatura associada ao pagamento. |
| `num_sub_seq_fatura` | VARCHAR | Sequencial técnico de detalhamento da fatura. |
| `num_fatura_pagamento` | VARCHAR | Número identificador do documento de cobrança. |
| `num_credito_seq` | VARCHAR | Sequencial identificador do crédito gerado. |
| `num_parcela_pagamento` | VARCHAR | Número da parcela referente ao pagamento realizado. |

---

### 💰 Informações Financeiras e Valores
| Variável | Tipo | Descrição |
| :--- | :--- | :--- |
| `val_pagamento_fatura` | DOUBLE | Valor efetivamente pago pelo cliente na fatura. |
| `val_pagamento_item` | DOUBLE | Valor pago rateado por item da fatura. |
| `val_pagamento_credito` | DOUBLE | Valor do pagamento convertido em crédito sistêmico. |
| `val_original_pagamento` | DOUBLE | Valor original do lançamento antes de juros ou descontos. |
| `val_atual_pagamento` | DOUBLE | Valor atualizado do pagamento no momento da baixa. |
| `val_baixa_atividade` | DOUBLE | Valor total baixado no sistema financeiro. |
| `val_juros_multas_item` | DOUBLE | Valor de juros e multas inclusos no item pago. |
| `val_multa_equip_item` | DOUBLE | Valor de multa por equipamento incluído no item. |
| `val_multa_equip_total` | DOUBLE | Valor total de multas por equipamento na transação. |
| `val_multa_fid_item` | DOUBLE | Valor de multa por fidelidade (se houver). |
| `val_desconto_item` | DOUBLE | Valor de desconto aplicado ao item. |

---

### 💳 Métodos e Atributos de Pagamento
| Variável | Tipo | Descrição |
| :--- | :--- | :--- |
| `cod_forma_pagamento` | VARCHAR | Código da forma de pagamento (Ex: Boleto, Cartão). |
| `dw_forma_pagamento` | VARCHAR | Identificador técnico da forma de pagamento. |
| `cod_metodo_pagamento` | VARCHAR | Código do método de captura do pagamento. |
| `ind_metodo_pagamento` | VARCHAR | Indicador do método de pagamento utilizado. |
| `num_banco_pagamento` | VARCHAR | Código do banco recebedor. |
| `dw_banco` | VARCHAR | Identificador técnico do banco no DW. |
| `dsc_nome_banco_pagamento` | VARCHAR | Nome da instituição bancária processadora. |
| `num_agencia_pagamento` | VARCHAR | Número da agência onde o pagamento foi realizado. |
| `num_cc_pagamento` | VARCHAR | Número da conta corrente vinculada ao pagamento. |
| `num_agrupador_pagamento` | VARCHAR | Identificador de agrupamento de transações. |

---

### 📊 Status e Classificações Técnicas
| Variável | Tipo | Descrição |
| :--- | :--- | :--- |
| `ind_status_pagamento` | VARCHAR | Indicador do status (Ex: R - Recebido, P - Pendente). |
| `ind_status_fatura` | VARCHAR | Indicador de status da fatura após processamento. |
| `cod_tipo_pagamento` | VARCHAR | Código do tipo de pagamento (Ex: Online, Offline). |
| `dw_tipo_pagamento` | VARCHAR | Identificador técnico do tipo de pagamento. |
| `cod_tipo_fatura` | VARCHAR | Código do tipo de documento de cobrança. |
| `dw_tipo_fatura` | VARCHAR | Identificador técnico do tipo de fatura. |
| `cod_alocacao_credito` | VARCHAR | Código de alocação do crédito (Ex: PYM). |
| `ind_tipo_credito` | VARCHAR | Indicador do tipo de crédito gerado. |
| `cod_atividade` | VARCHAR | Código da atividade financeira vinculada. |
| `cod_razao_atividade` | VARCHAR | Código da razão do lançamento financeiro. |
| `dw_motivo_estorno` | VARCHAR | Identificador do motivo em caso de estorno. |
| `dw_un_negocio` | VARCHAR | Identificador da Unidade de Negócio. |
| `dw_area` | VARCHAR | Identificador da área regional vinculada. |

---

### 📅 Datas de Ciclo e Processamento
| Variável | Tipo | Descrição |
| :--- | :--- | :--- |
| `dat_baixa_atividade` | DATE | Data em que o pagamento foi baixado no sistema. |
| `dat_atividade_credito` | DATE | Data de competência do crédito financeiro. |
| `dat_status_fatura` | DATE | Data de atualização do status da fatura. |
| `dat_status_pagamento` | DATE | Data da última atualização de status do pagamento. |
| `dat_vencimento_credito` | DATE | Data prevista para o vencimento do crédito. |
| `dat_deposito_atividade` | DATE | Data do depósito financeiro da transação. |
| `dat_criacao_pagamento` | TIMESTAMP | Data e hora de criação do registro de pagamento. |
| `dat_criacao_atividade` | TIMESTAMP | Data e hora de criação da atividade financeira. |
| `dat_criacao_credito` | TIMESTAMP | Data e hora de geração do crédito. |
| `dat_atualizacao_pagamento` | TIMESTAMP | Data da última atualização sistêmica do pagamento. |
| `dat_atualizacao_atividade` | TIMESTAMP | Data da última atualização da atividade. |
| `dat_criacao_dw` | TIMESTAMP | Data de carga no Data Warehouse original. |

---

### ⚙️ Metadados do Sistema
| Variável | Tipo | Descrição |
| :--- | :--- | :--- |
| `cod_arquivo_pagamento` | VARCHAR | Identificador do arquivo de retorno bancário. |
| `seq_arquivo_pagamento` | VARCHAR | Sequencial do processamento do arquivo. |
| `cod_login_pagamento` | VARCHAR | Login do usuário/sistema que registrou o pagamento. |
| `cod_login_credito` | VARCHAR | Login do usuário/sistema que registrou o crédito. |
| `ingestion_ts` | TIMESTAMP | Data e hora exata do processamento na camada Silver. |
| `run_id` | BIGINT | Identificador único da execução da pipeline. |
| `ano_mes` | BIGINT | Partição física do dado no Data Lake (YYYYMM). |

---

> **Finalidade:** Estes atributos são essenciais para calcular o comportamento de pontualidade, ticket médio de pagamento e churn financeiro na camada Gold.