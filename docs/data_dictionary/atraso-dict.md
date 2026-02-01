# 📖 Dicionário de Dados Silver: `atraso`

Este documento descreve a estrutura técnica e funcional da tabela de **Atraso** na camada Silver. Esta entidade consolida o histórico de faturas e saldos em aberto por cliente e contrato.

---

## 🛠️ Grão da Tabela (Unicidade)

O grão desta tabela é definido pela combinação das seguintes chaves, garantindo que cada evento de fatura seja único no tempo:
* `num_cpf` + `contrato` + `dat_referencia` + `num_fatura_hash` + `num_ent_seq_fatura`

---

## 🧬 Dicionário de Atributos

### 🔑 Chaves e Identificadores
| Variável | Tipo | Descrição |
| :--- | :--- | :--- |
| `num_cpf` | VARCHAR | **Coluna Mascarada (LGPD):** Identificador único do cliente (Hash). |
| `dw_num_cliente` | VARCHAR | Identificador numérico do cliente no Data Warehouse. |
| `contrato` | VARCHAR | Identificador único do contrato ou assinatura. |
| `dat_referencia` | DATE | Data de referência do mês da observação (Snapshot). |
| `num_fatura_hash` | VARCHAR | **Coluna Mascarada (LGPD):** Identificador único da fatura (Hash). |
| `num_ent_seq_fatura` | VARCHAR | Sequencial técnico de entrada do registro no sistema. |

---

### 💰 Informações Financeiras (Saldos e Valores)
| Variável | Tipo | Descrição |
| :--- | :--- | :--- |
| `val_fat_aberto` | DOUBLE | Valor total que permanece em aberto (inadimplente). |
| `val_fat_aberto_liq` | DOUBLE | Valor líquido em aberto após ajustes e deduções. |
| `val_fat_liquido` | DOUBLE | Valor líquido total da fatura. |
| `val_fat_bruto` | DOUBLE | Valor total bruto da fatura sem descontos. |
| `val_fat_bruto_bc` | DOUBLE | Valor bruto base de cálculo. |
| `val_fat_credito` | DOUBLE | Valor de créditos aplicados à fatura. |
| `val_fat_ajuste` | DOUBLE | Valor de ajustes manuais ou sistêmicos na fatura. |
| `val_fat_liq_jm_mc` | DOUBLE | Valor líquido considerando juros, multas e mora. |
| `val_fat_pagamento_bruto` | DOUBLE | Valor total bruto já pago referente a esta fatura. |
| `val_multa_juros` | DOUBLE | Valor de encargos e multas incidentes pelo atraso. |
| `val_multa_cancelamento` | DOUBLE | Valor de multa aplicada por cancelamento de contrato. |
| `val_parc_aparelho_liq` | DOUBLE | Valor líquido de parcelamento de aparelhos, se houver. |

---

### 📊 Classificação e Status de Negócio
| Variável | Tipo | Descrição |
| :--- | :--- | :--- |
| `dsc_tipo_faturamento` | VARCHAR | Descrição da natureza do faturamento (Ex: Mensalidade, Multa). |
| `dw_tipo_faturamento` | VARCHAR | Código técnico do tipo de faturamento. |
| `cod_plataforma` | VARCHAR | Código do sistema de origem do faturamento (Ex: AUTOC, POSPG). |
| `ind_fraude` | VARCHAR | Indicador de identificação de suspeita de fraude. |
| `ind_aca` | VARCHAR | Indicador de ação de cobrança aplicada. |
| `ind_pccr` | VARCHAR | Indicador de perfil de recuperação de crédito. |
| `ind_pdd` | VARCHAR | Indicador de Provisão para Devedores Duvidosos. |
| `ind_wo` | VARCHAR | Indicador de Write-off (perda contábil reconhecida). |
| `ind_primeira_fat` | VARCHAR | Flag indicando se é a primeira fatura do cliente. |
| `ind_isencao_cob_fat` | VARCHAR | Indicador de isenção de cobrança de fatura. |

---

### ⏳ Temporalidade e Envelhecimento (Aging)
| Variável | Tipo | Descrição |
| :--- | :--- | :--- |
| `dw_faixa_aging_divida` | VARCHAR | Faixa de atraso consolidada da dívida do cliente. |
| `dw_faixa_aging_fatura` | VARCHAR | Faixa de atraso específica desta fatura. |
| `dw_faixa_aging_prox_fech` | VARCHAR | Projeção de faixa de atraso para o próximo fechamento. |
| `dw_faixa_tempo_base` | VARCHAR | Faixa de tempo de permanência do cliente na base. |
| `dw_ciclo` | VARCHAR | Código do ciclo de faturamento do cliente. |
| `num_bill_seq_fat` | VARCHAR | Número sequencial de cobrança da fatura. |
| `num_seq_acordo_fat` | VARCHAR | Sequencial de acordo de parcelamento vinculado. |
| `dw_area` | VARCHAR | Código da área geográfica/regional do contrato. |
| `dw_his_ponto_venda_comta`| VARCHAR | Histórico do ponto de venda onde a conta foi aberta. |
| `dw_oferta` | VARCHAR | Identificador da oferta comercial vinculada ao contrato. |
| `dw_tipo_cliente_conta` | VARCHAR | Classificação do tipo de conta do cliente. |
| `dw_un_negocio` | VARCHAR | Identificador da Unidade de Negócio. |

---

### 📅 Datas de Ciclo e Sistema
| Variável | Tipo | Descrição |
| :--- | :--- | :--- |
| `dat_vencimento_fat` | DATE | Data de vencimento atual da fatura. |
| `dat_original_vcto_fat` | DATE | Data de vencimento original (antes de prorrogações). |
| `dat_min_vencimento_fat` | DATE | Data mínima de vencimento registrada para o documento. |
| `dat_alteracao_vcto_fat` | DATE | Data da última alteração no vencimento da fatura. |
| `dat_ativacao_conta_cli` | DATE | Data de ativação do cliente na base histórica. |
| `dat_criacao_fat` | TIMESTAMP | Data e hora da geração da fatura no sistema. |
| `dat_status_fat` | TIMESTAMP | Data da última atualização de status do documento. |
| `dat_criacao_dw` | TIMESTAMP | Data de carga do registro no Data Warehouse original. |
| `dat_criacao_registro_trans`| TIMESTAMP | Data de criação do registro transacional na origem. |
| `dat_alteracao_registro_trans`| TIMESTAMP | Data da última alteração do registro na origem. |

---

### ⚙️ Metadados de Processamento
| Variável | Tipo | Descrição |
| :--- | :--- | :--- |
| `ingestion_ts` | TIMESTAMP | Data e hora exata do processamento na camada Silver. |
| `run_id` | BIGINT | Identificador único da execução da pipeline. |
| `ano_mes` | BIGINT | Partição física do dado no Data Lake (YYYYMM). |

---

> **Finalidade:** Estes atributos são as fontes oficiais para o cálculo de Recência, Frequência e Valor (RFV) de inadimplência, além de servirem para análises de safra e envelhecimento de dívida na camada Gold.