# Relatório de Profiling: `bronze/pagamento` - `20260108_204106`

### 🔑 Garantia de Unicidade: `bronze/pagamento`
- **Chave Técnica:** `num_cpf, contrato, seq_fatura, num_sub_seq_fatura`
- **Tipo:** `COMPOSTA`

| coluna        |   distintos |   nulos |   duplicados | pct_nulos   | pct_duplicados   | cardinalidade   |
|:--------------|------------:|--------:|-------------:|:------------|:-----------------|:----------------|
| CHAVE_TECNICA |    23283525 |       0 |            0 | 0.0%        | 0.0%             | ALTA            |

### 🚩 Diagnóstico e Observações Técnicas
* ✅ **Sucesso:** A chave técnica parece ser única para este conjunto de dados (estimativa estatística).
* 👻 **Otimização de Schema:** Colunas 100% nulas ou zeradas detectadas em análises anteriores devem ser avaliadas para exclusão na Silver.

---



---

### 📦 Volumetria: `bronze/pagamento`
| diretorio      |   qtd_arquivos | registros   |   colunas |   tamanho_comprimido_mib |   tamanho_descomprimido_mib |
|:---------------|---------------:|:------------|----------:|-------------------------:|----------------------------:|
| ano_mes=202310 |              1 | 869.793     |        76 |                    32.15 |                       60.91 |
| ano_mes=202311 |              1 | 869.501     |        76 |                    31.92 |                       60.03 |
| ano_mes=202312 |              1 | 929.072     |        76 |                    34.14 |                       64.82 |
| ano_mes=202401 |              1 | 923.529     |        76 |                    34.33 |                       64.97 |
| ano_mes=202402 |              1 | 943.835     |        76 |                    34.59 |                       64.76 |
| ano_mes=202403 |              1 | 984.772     |        76 |                    36.61 |                       68.86 |
| ano_mes=202404 |              1 | 1.002.252   |        76 |                    66.82 |                      111.16 |
| ano_mes=202405 |              1 | 1.043.511   |        76 |                   103.94 |                      172.21 |
| ano_mes=202406 |              1 | 1.012.756   |        76 |                   101.03 |                      165.82 |
| ano_mes=202407 |              1 | 1.068.676   |        76 |                   107.35 |                      176.95 |
| ano_mes=202408 |              1 | 1.074.927   |        76 |                   107.64 |                      177.17 |
| ano_mes=202409 |              1 | 1.050.711   |        76 |                   104.99 |                      171.21 |
| ano_mes=202410 |              1 | 1.112.563   |        76 |                   109.9  |                      181.52 |
| ano_mes=202411 |              1 | 1.189.482   |        76 |                   117.39 |                      192.1  |
| ano_mes=202412 |              1 | 1.501.147   |        76 |                   145.53 |                      239.32 |
| ano_mes=202501 |              1 | 1.771.821   |        76 |                   170.14 |                      279.84 |
| ano_mes=202502 |              1 | 2.015.493   |        76 |                   190.46 |                      314.27 |
| ano_mes=202503 |              1 | 2.465.787   |        76 |                   230.21 |                      382.21 |
| TOTAL          |             18 | 21.829.628  |        76 |                  1759.13 |                     2948.11 |

---

### 🧬 Schema: `bronze/pagamento`
| column_name                  | column_type              | null   | key   | default   | extra   |
|:-----------------------------|:-------------------------|:-------|:------|:----------|:--------|
| num_cpf                      | VARCHAR                  | YES    |       |           |         |
| dat_status_fatura            | DATE                     | YES    |       |           |         |
| contrato                     | VARCHAR                  | YES    |       |           |         |
| dw_num_cliente               | VARCHAR                  | YES    |       |           |         |
| num_fatura_pagamento         | VARCHAR                  | YES    |       |           |         |
| dat_criacao_dw               | TIMESTAMP                | YES    |       |           |         |
| dat_criacao_atividade        | TIMESTAMP                | YES    |       |           |         |
| dat_atualizacao_atividade    | TIMESTAMP                | YES    |       |           |         |
| dat_baixa_atividade          | DATE                     | YES    |       |           |         |
| dat_deposito_atividade       | DATE                     | YES    |       |           |         |
| dat_criacao_pagamento        | TIMESTAMP                | YES    |       |           |         |
| dat_atualizacao_pagamento    | TIMESTAMP                | YES    |       |           |         |
| dat_status_pagamento         | DATE                     | YES    |       |           |         |
| dat_criacao_credito          | TIMESTAMP                | YES    |       |           |         |
| dat_atualizacao_credito      | TIMESTAMP                | YES    |       |           |         |
| dat_atividade_credito        | DATE                     | YES    |       |           |         |
| dat_vencimento_credito       | DATE                     | YES    |       |           |         |
| val_pagamento_fatura         | DOUBLE                   | YES    |       |           |         |
| val_desconto_item            | DOUBLE                   | YES    |       |           |         |
| val_pagamento_item           | DOUBLE                   | YES    |       |           |         |
| val_juros_multas_item        | DOUBLE                   | YES    |       |           |         |
| val_multa_equip_item         | DOUBLE                   | YES    |       |           |         |
| val_multa_equip_total        | DOUBLE                   | YES    |       |           |         |
| val_multa_fid_item           | DOUBLE                   | YES    |       |           |         |
| val_baixa_atividade          | DOUBLE                   | YES    |       |           |         |
| val_original_pagamento       | DOUBLE                   | YES    |       |           |         |
| val_atual_pagamento          | DOUBLE                   | YES    |       |           |         |
| val_pagamento_credito        | DOUBLE                   | YES    |       |           |         |
| seq_fatura                   | VARCHAR                  | YES    |       |           |         |
| num_sub_seq_fatura           | VARCHAR                  | YES    |       |           |         |
| num_credito_seq              | VARCHAR                  | YES    |       |           |         |
| dw_tipo_fatura               | VARCHAR                  | YES    |       |           |         |
| ind_status_fatura            | VARCHAR                  | YES    |       |           |         |
| dw_area                      | VARCHAR                  | YES    |       |           |         |
| dw_un_negocio                | VARCHAR                  | YES    |       |           |         |
| dw_forma_pagamento           | VARCHAR                  | YES    |       |           |         |
| dw_banco                     | VARCHAR                  | YES    |       |           |         |
| dw_tipo_pagamento            | VARCHAR                  | YES    |       |           |         |
| num_banco_pagamento          | VARCHAR                  | YES    |       |           |         |
| num_agencia_pagamento        | VARCHAR                  | YES    |       |           |         |
| num_cc_pagamento             | VARCHAR                  | YES    |       |           |         |
| dw_motivo_estorno            | VARCHAR                  | YES    |       |           |         |
| cod_origem_netuno            | VARCHAR                  | YES    |       |           |         |
| cod_conta_atividade          | VARCHAR                  | YES    |       |           |         |
| seq_entidade_atividade       | VARCHAR                  | YES    |       |           |         |
| cod_login_operador_atividade | VARCHAR                  | YES    |       |           |         |
| cod_atividade                | VARCHAR                  | YES    |       |           |         |
| cod_razao_atividade          | VARCHAR                  | YES    |       |           |         |
| cod_fundo_atividade          | VARCHAR                  | YES    |       |           |         |
| cod_banco_atividade          | VARCHAR                  | YES    |       |           |         |
| num_conta_atividade          | VARCHAR                  | YES    |       |           |         |
| cod_agencia_atividade        | VARCHAR                  | YES    |       |           |         |
| seq_entidade_pagamento       | VARCHAR                  | YES    |       |           |         |
| cod_login_pagamento          | VARCHAR                  | YES    |       |           |         |
| cod_forma_pagamento          | VARCHAR                  | YES    |       |           |         |
| cod_tipo_pagamento           | VARCHAR                  | YES    |       |           |         |
| dsc_nome_banco_pagamento     | VARCHAR                  | YES    |       |           |         |
| seq_arquivo_pagamento        | VARCHAR                  | YES    |       |           |         |
| num_parcela_pagamento        | VARCHAR                  | YES    |       |           |         |
| num_agrupador_pagamento      | VARCHAR                  | YES    |       |           |         |
| dsc_pagamento                | VARCHAR                  | YES    |       |           |         |
| cod_metodo_pagamento         | VARCHAR                  | YES    |       |           |         |
| ind_status_pagamento         | VARCHAR                  | YES    |       |           |         |
| cod_arquivo_pagamento        | VARCHAR                  | YES    |       |           |         |
| cod_netuno_pagamento         | VARCHAR                  | YES    |       |           |         |
| cod_login_credito            | VARCHAR                  | YES    |       |           |         |
| ind_tipo_credito             | VARCHAR                  | YES    |       |           |         |
| seq_pagamento_credito        | VARCHAR                  | YES    |       |           |         |
| seq_fatura_credito           | VARCHAR                  | YES    |       |           |         |
| cod_alocacao_credito         | VARCHAR                  | YES    |       |           |         |
| cod_desalocacao_credito      | VARCHAR                  | YES    |       |           |         |
| seq_entidade_credito         | VARCHAR                  | YES    |       |           |         |
| cod_tipo_fatura              | VARCHAR                  | YES    |       |           |         |
| ingestion_ts                 | TIMESTAMP WITH TIME ZONE | YES    |       |           |         |
| ano_mes                      | BIGINT                   | YES    |       |           |         |
| run_id                       | VARCHAR                  | YES    |       |           |         |

---

### 📅 Range de Datas: `bronze/pagamento`
#### Coluna: `dat_status_fatura`
| min                        | max                        |
|:---------------------------|:---------------------------|
| 2023-10-01T00:00:00.000000 | 2025-03-31T00:00:00.000000 |

#### Coluna: `dat_criacao_dw`
| min                        | max                        |
|:---------------------------|:---------------------------|
| 2023-10-05T02:22:07.000000 | 2025-04-03T09:59:52.000000 |

#### Coluna: `dat_criacao_atividade`
| min                        | max                        |
|:---------------------------|:---------------------------|
| 2024-04-16T02:00:07.000000 | 2025-04-01T01:00:49.000000 |

#### Coluna: `dat_atualizacao_atividade`
| min                        | max                        |
|:---------------------------|:---------------------------|
| 2024-04-16T06:44:08.000000 | 2025-04-02T05:08:18.000000 |

#### Coluna: `dat_baixa_atividade`
| min                        | max                        |
|:---------------------------|:---------------------------|
| 2024-04-16T00:00:00.000000 | 2025-03-31T00:00:00.000000 |

#### Coluna: `dat_deposito_atividade`
| min                        | max                        |
|:---------------------------|:---------------------------|
| 2005-03-20T00:00:00.000000 | 2025-03-31T00:00:00.000000 |

#### Coluna: `dat_criacao_pagamento`
| min                        | max                        |
|:---------------------------|:---------------------------|
| 2017-09-13T22:05:41.000000 | 2025-04-01T01:00:49.000000 |

#### Coluna: `dat_atualizacao_pagamento`
| min                        | max                        |
|:---------------------------|:---------------------------|
| 2024-04-16T08:25:15.000000 | 2025-04-02T12:07:58.000000 |

#### Coluna: `dat_status_pagamento`
| min                        | max                        |
|:---------------------------|:---------------------------|
| 2021-08-18T00:00:00.000000 | 2025-04-02T00:00:00.000000 |

#### Coluna: `dat_criacao_credito`
| min                        | max                        |
|:---------------------------|:---------------------------|
| 2017-09-13T22:05:41.000000 | 2025-04-02T11:17:08.000000 |

#### Coluna: `dat_atualizacao_credito`
| min   | max   |
|:------|:------|
| NaT   | NaT   |

#### Coluna: `dat_atividade_credito`
| min                        | max                        |
|:---------------------------|:---------------------------|
| 2017-09-13T00:00:00.000000 | 2025-04-02T00:00:00.000000 |

#### Coluna: `dat_vencimento_credito`
| min                        | max                        |
|:---------------------------|:---------------------------|
| 2011-09-20T00:00:00.000000 | 2025-05-05T00:00:00.000000 |

#### Coluna: `ingestion_ts`
| min                              | max                              |
|:---------------------------------|:---------------------------------|
| 2026-01-08 17:41:06.467416-03:00 | 2026-01-08 17:41:06.467416-03:00 |



---

### 🔢 Range de Valores Numéricos: `bronze/pagamento`

#### Coluna: `val_pagamento_fatura`
|   min |         max |   media |
|------:|------------:|--------:|
|  0.01 | 3.40652e+06 |   61.26 |

#### Coluna: `val_desconto_item`
|   min |   max |   media |
|------:|------:|--------:|
|     0 |     0 |       0 |

#### Coluna: `val_pagamento_item`
|   min |         max |   media |
|------:|------------:|--------:|
|  0.01 | 3.40652e+06 |   61.26 |

#### Coluna: `val_juros_multas_item`
|   min |    max |   media |
|------:|-------:|--------:|
|     0 | 103521 |    0.59 |

#### Coluna: `val_multa_equip_item`
|   min |     max |   media |
|------:|--------:|--------:|
|     0 | 56186.4 |    0.33 |

#### Coluna: `val_multa_equip_total`
|   min |     max |   media |
|------:|--------:|--------:|
|     0 | 56186.4 |    0.33 |

#### Coluna: `val_multa_fid_item`
|   min |   max |   media |
|------:|------:|--------:|
|     0 |     0 |       0 |

#### Coluna: `val_baixa_atividade`
|      min |         max |   media |
|---------:|------------:|--------:|
| -16803.5 | 3.40734e+06 |   97.52 |

#### Coluna: `val_original_pagamento`
|   min |         max |   media |
|------:|------------:|--------:|
|  0.01 | 6.28174e+06 |  1184.7 |

#### Coluna: `val_atual_pagamento`
|   min |         max |   media |
|------:|------------:|--------:|
|  0.01 | 3.40734e+06 |   98.05 |

#### Coluna: `val_pagamento_credito`
|   min |         max |   media |
|------:|------------:|--------:|
|  0.01 | 3.40649e+06 |   58.02 |



---

### 📊 Estatísticas por Coluna: `bronze/pagamento`
| coluna                       |   distintos |    nulos |   duplicados | pct_nulos   | pct_duplicados   | cardinalidade   |
|:-----------------------------|------------:|---------:|-------------:|:------------|:-----------------|:----------------|
| num_cpf                      |     1930320 |        0 |     19899308 | 0.0%        | 91.16%           | ALTA            |
| dat_status_fatura            |         538 |        0 |     21829090 | 0.0%        | 100.0%           | BAIXA           |
| contrato                     |     2304298 |        0 |     19525330 | 0.0%        | 89.44%           | ALTA            |
| dw_num_cliente               |     2954149 |        0 |     18875479 | 0.0%        | 86.47%           | ALTA            |
| num_fatura_pagamento         |    12888878 |  6845630 |      8940750 | 31.36%      | 40.96%           | ALTA            |
| dat_criacao_dw               |       49276 |        0 |     21780352 | 0.0%        | 99.77%           | MEDIA           |
| dat_criacao_atividade        |     6572610 |  6118973 |     15257018 | 28.03%      | 69.89%           | ALTA            |
| dat_atualizacao_atividade    |      392769 | 20730830 |     21436859 | 94.97%      | 98.2%            | MEDIA           |
| dat_baixa_atividade          |         382 |  6118973 |     21829246 | 28.03%      | 100.0%           | BAIXA           |
| dat_deposito_atividade       |         756 |  6118973 |     21828872 | 28.03%      | 100.0%           | BAIXA           |
| dat_criacao_pagamento        |     6572610 |  6118973 |     15257018 | 28.03%      | 69.89%           | ALTA            |
| dat_atualizacao_pagamento    |      153177 | 18882483 |     21676451 | 86.5%       | 99.3%            | MEDIA           |
| dat_status_pagamento         |         397 |  6118973 |     21829231 | 28.03%      | 100.0%           | BAIXA           |
| dat_criacao_credito          |     6657349 |  6118973 |     15172279 | 28.03%      | 69.5%            | ALTA            |
| dat_atualizacao_credito      |           0 | 21829628 |     21829628 | 100.0%      | 100.0%           | BAIXA           |
| dat_atividade_credito        |         508 |  6118973 |     21829120 | 28.03%      | 100.0%           | BAIXA           |
| dat_vencimento_credito       |        1420 |  6118973 |     21828208 | 28.03%      | 99.99%           | BAIXA           |
| val_pagamento_fatura         |       59667 |        0 |     21769961 | 0.0%        | 99.73%           | MEDIA           |
| val_desconto_item            |           1 |        0 |     21829627 | 0.0%        | 100.0%           | BAIXA           |
| val_pagamento_item           |       59667 |        0 |     21769961 | 0.0%        | 99.73%           | MEDIA           |
| val_juros_multas_item        |        3886 |        0 |     21825742 | 0.0%        | 99.98%           | BAIXA           |
| val_multa_equip_item         |        6123 |        0 |     21823505 | 0.0%        | 99.97%           | BAIXA           |
| val_multa_equip_total        |        6123 |        0 |     21823505 | 0.0%        | 99.97%           | BAIXA           |
| val_multa_fid_item           |           1 |        0 |     21829627 | 0.0%        | 100.0%           | BAIXA           |
| val_baixa_atividade          |       70406 |  6118973 |     21759222 | 28.03%      | 99.68%           | MEDIA           |
| val_original_pagamento       |       63233 |  6118973 |     21766395 | 28.03%      | 99.71%           | MEDIA           |
| val_atual_pagamento          |       68805 |  6118978 |     21760823 | 28.03%      | 99.68%           | MEDIA           |
| val_pagamento_credito        |       55384 |  6118973 |     21774244 | 28.03%      | 99.75%           | MEDIA           |
| seq_fatura                   |         251 |        0 |     21829377 | 0.0%        | 100.0%           | BAIXA           |
| num_sub_seq_fatura           |        1333 |        0 |     21828295 | 0.0%        | 99.99%           | BAIXA           |
| num_credito_seq              |         321 |        0 |     21829307 | 0.0%        | 100.0%           | BAIXA           |
| dw_tipo_fatura               |          24 |        0 |     21829604 | 0.0%        | 100.0%           | BAIXA           |
| ind_status_fatura            |           2 |        0 |     21829626 | 0.0%        | 100.0%           | BAIXA           |
| dw_area                      |          71 |        0 |     21829557 | 0.0%        | 100.0%           | BAIXA           |
| dw_un_negocio                |          10 |        0 |     21829618 | 0.0%        | 100.0%           | BAIXA           |
| dw_forma_pagamento           |           4 |        0 |     21829624 | 0.0%        | 100.0%           | BAIXA           |
| dw_banco                     |          55 |        0 |     21829573 | 0.0%        | 100.0%           | BAIXA           |
| dw_tipo_pagamento            |           4 |        0 |     21829624 | 0.0%        | 100.0%           | BAIXA           |
| num_banco_pagamento          |          39 |        0 |     21829589 | 0.0%        | 100.0%           | BAIXA           |
| num_agencia_pagamento        |        9154 |        0 |     21820474 | 0.0%        | 99.96%           | BAIXA           |
| num_cc_pagamento             |      325591 |        0 |     21504037 | 0.0%        | 98.51%           | MEDIA           |
| dw_motivo_estorno            |           1 |        0 |     21829627 | 0.0%        | 100.0%           | BAIXA           |
| cod_origem_netuno            |      419749 | 13566081 |     21409879 | 62.15%      | 98.08%           | MEDIA           |
| cod_conta_atividade          |     2730825 |  6118973 |     19098803 | 28.03%      | 87.49%           | ALTA            |
| seq_entidade_atividade       |         313 |  6118973 |     21829315 | 28.03%      | 100.0%           | BAIXA           |
| cod_login_operador_atividade |         971 | 14215870 |     21828657 | 65.12%      | 100.0%           | BAIXA           |
| cod_atividade                |           5 |  6118973 |     21829623 | 28.03%      | 100.0%           | BAIXA           |
| cod_razao_atividade          |           6 |  8446071 |     21829622 | 38.69%      | 100.0%           | BAIXA           |
| cod_fundo_atividade          |        1601 | 21819036 |     21828027 | 99.95%      | 99.99%           | BAIXA           |
| cod_banco_atividade          |          37 | 13732767 |     21829591 | 62.91%      | 100.0%           | BAIXA           |
| num_conta_atividade          |      293957 | 19502508 |     21535671 | 89.34%      | 98.65%           | MEDIA           |
| cod_agencia_atividade        |        9154 | 15077146 |     21820474 | 69.07%      | 99.96%           | BAIXA           |
| seq_entidade_pagamento       |         313 |  6118973 |     21829315 | 28.03%      | 100.0%           | BAIXA           |
| cod_login_pagamento          |         971 | 14539993 |     21828657 | 66.61%      | 100.0%           | BAIXA           |
| cod_forma_pagamento          |           4 |  6118973 |     21829624 | 28.03%      | 100.0%           | BAIXA           |
| cod_tipo_pagamento           |           5 |  6118973 |     21829623 | 28.03%      | 100.0%           | BAIXA           |
| dsc_nome_banco_pagamento     |          78 |  6118973 |     21829550 | 28.03%      | 100.0%           | BAIXA           |
| seq_arquivo_pagamento        |        6533 | 13775460 |     21823095 | 63.1%       | 99.97%           | BAIXA           |
| num_parcela_pagamento        |         601 | 21268211 |     21829027 | 97.43%      | 100.0%           | BAIXA           |
| num_agrupador_pagamento      |      338523 | 16102580 |     21491105 | 73.76%      | 98.45%           | MEDIA           |
| dsc_pagamento                |     2141789 | 18848477 |     19687839 | 86.34%      | 90.19%           | ALTA            |
| cod_metodo_pagamento         |           6 | 16297184 |     21829622 | 74.66%      | 100.0%           | BAIXA           |
| ind_status_pagamento         |           4 |  8996090 |     21829624 | 41.21%      | 100.0%           | BAIXA           |
| cod_arquivo_pagamento        |     2230500 | 18390641 |     19599128 | 84.25%      | 89.78%           | ALTA            |
| cod_netuno_pagamento         |           0 | 21829628 |     21829628 | 100.0%      | 100.0%           | BAIXA           |
| cod_login_credito            |        1179 | 14223305 |     21828449 | 65.16%      | 99.99%           | BAIXA           |
| ind_tipo_credito             |           1 |  6118973 |     21829627 | 28.03%      | 100.0%           | BAIXA           |
| seq_pagamento_credito        |         313 |  6118973 |     21829315 | 28.03%      | 100.0%           | BAIXA           |
| seq_fatura_credito           |        1245 |  6118973 |     21828383 | 28.03%      | 99.99%           | BAIXA           |
| cod_alocacao_credito         |           9 |  6118973 |     21829619 | 28.03%      | 100.0%           | BAIXA           |
| cod_desalocacao_credito      |           0 | 21829628 |     21829628 | 100.0%      | 100.0%           | BAIXA           |
| seq_entidade_credito         |        7916 |  6118973 |     21821712 | 28.03%      | 99.96%           | BAIXA           |
| cod_tipo_fatura              |          32 |  6118973 |     21829596 | 28.03%      | 100.0%           | BAIXA           |
| ingestion_ts                 |           1 |        0 |     21829627 | 0.0%        | 100.0%           | BAIXA           |
| ano_mes                      |          20 |        0 |     21829608 | 0.0%        | 100.0%           | BAIXA           |
| run_id                       |           1 |        0 |     21829627 | 0.0%        | 100.0%           | BAIXA           |

---

### 🔟 Distribuição de Valores (Top 10): `bronze/pagamento`
#### Coluna: `num_cpf`

| valor       |   qtd |
|:------------|------:|
| W8XY7ZUX88Y |   565 |
| YNZZZ9NZ8N7 |   524 |
| UWUUUYUX8Y8 |   467 |
| 78W79997YZU |   438 |
| NTTNTN9ZXXZ |   428 |
| NZTNN8X9W9Y |   363 |
| WZY8NUWT888 |   356 |
| ZUUZXTNT8ZZ |   354 |
| U8UTUYYYYZZ |   348 |
| ZW88NWYZYZZ |   344 |

#### Coluna: `dat_status_fatura`

| valor      |    qtd |
|:-----------|-------:|
| 2025-03-11 | 237845 |
| 2025-03-06 | 208120 |
| 2025-02-11 | 167344 |
| 2025-02-06 | 143259 |
| 2025-03-10 | 142721 |
| 2025-03-18 | 142504 |
| 2025-03-21 | 137487 |
| 2025-03-07 | 133100 |
| 2025-01-07 | 128795 |
| 2025-02-18 | 127701 |

#### Coluna: `contrato`

|     valor |   qtd |
|----------:|------:|
| 842432062 |   506 |
| 820476782 |   405 |
| 841649816 |   338 |
| 870385565 |   267 |
| 883412299 |   257 |
| 830274393 |   247 |
| 882702353 |   246 |
| 883290298 |   242 |
| 883078334 |   240 |
| 833863447 |   234 |

#### Coluna: `dw_num_cliente`

|      valor |   qtd |
|-----------:|------:|
|  929754533 |   506 |
| 1088708129 |   405 |
|  964129025 |   390 |
| 1164649466 |   308 |
| 1107929393 |   267 |
| 1173358512 |   257 |
| 1135100019 |   247 |
| 1170649847 |   246 |
| 1410997515 |   242 |
| 1171695031 |   240 |

#### Coluna: `num_fatura_pagamento`

| valor        |     qtd |
|:-------------|--------:|
| NULL         | 6845630 |
| 966132196123 |      24 |
| 966132196124 |      24 |
| 120004027064 |      22 |
| 913625840147 |      21 |
| 966132196122 |      21 |
| 966132196132 |      21 |
| 966132196127 |      21 |
| 966132196130 |      21 |
| 966132196128 |      21 |

#### Coluna: `dat_criacao_dw`

| valor               |   qtd |
|:--------------------|------:|
| 2025-02-23 17:29:12 | 44444 |
| 2025-03-03 09:59:28 | 44035 |
| 2025-02-24 09:54:38 | 42553 |
| 2025-03-09 11:17:51 | 42038 |
| 2025-03-15 23:10:40 | 41664 |
| 2025-03-09 11:17:50 | 40929 |
| 2025-03-09 11:17:52 | 38850 |
| 2025-03-11 06:46:19 | 38813 |
| 2025-03-16 12:33:13 | 37978 |
| 2025-03-15 23:10:41 | 37733 |

#### Coluna: `dat_criacao_atividade`

| valor               |     qtd |
|:--------------------|--------:|
| NULL                | 6118973 |
| 2025-03-06 14:36:18 |     250 |
| 2025-03-06 14:36:43 |     245 |
| 2025-03-06 14:36:07 |     241 |
| 2025-02-21 12:47:38 |     236 |
| 2025-03-06 14:36:36 |     235 |
| 2025-02-21 12:47:16 |     235 |
| 2025-03-06 14:36:11 |     234 |
| 2025-02-21 12:47:22 |     233 |
| 2025-03-06 14:36:38 |     232 |

#### Coluna: `dat_atualizacao_atividade`

| valor               |      qtd |
|:--------------------|---------:|
| NULL                | 20730830 |
| 2025-02-18 18:54:47 |      238 |
| 2025-02-18 18:54:52 |      225 |
| 2025-02-18 18:54:51 |      218 |
| 2025-02-18 18:54:50 |      204 |
| 2025-02-18 18:54:48 |      186 |
| 2025-03-12 04:19:30 |      182 |
| 2025-02-18 18:54:49 |      169 |
| 2025-02-08 05:25:18 |      167 |
| 2025-01-08 03:40:08 |      167 |

#### Coluna: `dat_baixa_atividade`

| valor      |     qtd |
|:-----------|--------:|
| NULL       | 6118973 |
| 2025-03-11 |  237845 |
| 2025-03-06 |  208120 |
| 2025-02-11 |  167344 |
| 2025-02-06 |  143259 |
| 2025-03-10 |  142721 |
| 2025-03-18 |  142504 |
| 2025-03-21 |  137487 |
| 2025-03-07 |  133100 |
| 2025-01-07 |  128795 |

#### Coluna: `dat_deposito_atividade`

| valor      |     qtd |
|:-----------|--------:|
| NULL       | 6118973 |
| 2025-03-10 |  324945 |
| 2025-02-10 |  271932 |
| 2025-03-05 |  193490 |
| 2025-03-17 |  172723 |
| 2025-01-10 |  165489 |
| 2025-03-20 |  165082 |
| 2025-02-17 |  148657 |
| 2025-02-20 |  140404 |
| 2024-12-10 |  139575 |

#### Coluna: `dat_criacao_pagamento`

| valor               |     qtd |
|:--------------------|--------:|
| NULL                | 6118973 |
| 2025-03-06 14:36:18 |     250 |
| 2025-03-06 14:36:43 |     245 |
| 2025-03-06 14:36:07 |     241 |
| 2025-02-21 12:47:38 |     236 |
| 2025-03-06 14:36:11 |     234 |
| 2025-02-21 12:47:16 |     234 |
| 2025-02-21 12:47:22 |     233 |
| 2025-03-06 14:36:36 |     233 |
| 2025-03-06 14:36:38 |     232 |

#### Coluna: `dat_atualizacao_pagamento`

| valor               |      qtd |
|:--------------------|---------:|
| NULL                | 18882483 |
| 2025-03-07 04:06:31 |     2537 |
| 2025-03-12 04:06:33 |     2492 |
| 2025-03-11 05:27:34 |     2393 |
| 2025-03-12 04:06:32 |     2339 |
| 2025-03-11 05:27:36 |     2305 |
| 2025-03-11 05:27:33 |     2297 |
| 2025-03-11 05:27:37 |     2246 |
| 2025-03-08 05:30:28 |     2240 |
| 2025-01-09 04:46:10 |     2215 |

#### Coluna: `dat_status_pagamento`

| valor      |     qtd |
|:-----------|--------:|
| NULL       | 6118973 |
| 2025-03-11 |  274965 |
| 2025-03-06 |  204513 |
| 2025-02-11 |  180872 |
| 2025-03-18 |  151370 |
| 2025-03-21 |  146867 |
| 2025-02-06 |  144461 |
| 2025-02-18 |  134539 |
| 2025-03-07 |  134080 |
| 2025-01-07 |  131040 |

#### Coluna: `dat_criacao_credito`

| valor               |     qtd |
|:--------------------|--------:|
| NULL                | 6118973 |
| 2025-03-06 14:36:18 |     247 |
| 2025-03-06 14:36:07 |     242 |
| 2025-02-21 12:47:38 |     241 |
| 2025-02-21 12:47:22 |     240 |
| 2025-03-06 14:36:43 |     237 |
| 2025-03-06 14:36:11 |     236 |
| 2025-02-21 12:47:16 |     234 |
| 2025-03-06 14:36:36 |     233 |
| 2025-03-06 14:36:31 |     232 |

#### Coluna: `dat_atualizacao_credito`

| valor   |      qtd |
|:--------|---------:|
| NULL    | 21829628 |

#### Coluna: `dat_atividade_credito`

| valor      |     qtd |
|:-----------|--------:|
| NULL       | 6118973 |
| 2025-03-11 |  237682 |
| 2025-03-06 |  208768 |
| 2025-02-11 |  167407 |
| 2025-02-06 |  143415 |
| 2025-03-10 |  143156 |
| 2025-03-18 |  142276 |
| 2025-03-21 |  137340 |
| 2025-03-07 |  133017 |
| 2025-01-07 |  128867 |

#### Coluna: `dat_vencimento_credito`

| valor      |     qtd |
|:-----------|--------:|
| NULL       | 6118973 |
| 2025-03-10 |  638118 |
| 2025-02-10 |  631527 |
| 2025-02-17 |  394098 |
| 2025-01-10 |  386952 |
| 2025-02-20 |  372923 |
| 2025-03-17 |  368492 |
| 2025-01-15 |  355307 |
| 2025-01-20 |  326015 |
| 2025-03-20 |  319366 |

#### Coluna: `val_pagamento_fatura`

|   valor |    qtd |
|--------:|-------:|
|   54.9  | 399940 |
|   29.9  | 357074 |
|   34.8  | 344505 |
|   34.9  | 299099 |
|   49.9  | 279331 |
|   29.8  | 276180 |
|   54.8  | 229557 |
|   64.9  | 192516 |
|   39.89 | 173593 |
|   59.89 | 172415 |

#### Coluna: `val_desconto_item`

|   valor |      qtd |
|--------:|---------:|
|       0 | 21829628 |

#### Coluna: `val_pagamento_item`

|   valor |    qtd |
|--------:|-------:|
|   54.9  | 399940 |
|   29.9  | 357074 |
|   34.8  | 344505 |
|   34.9  | 299099 |
|   49.9  | 279331 |
|   29.8  | 276180 |
|   54.8  | 229557 |
|   64.9  | 192516 |
|   39.89 | 173593 |
|   59.89 | 172415 |

#### Coluna: `val_juros_multas_item`

|   valor |      qtd |
|--------:|---------:|
|    0    | 13750268 |
|    0.13 |   128581 |
|    0.12 |   117043 |
|    0.09 |   103430 |
|    0.14 |    98282 |
|    0.1  |    98134 |
|    0.11 |    97317 |
|    0.08 |    95645 |
|    0.04 |    89815 |
|    0.05 |    74874 |

#### Coluna: `val_multa_equip_item`

|   valor |      qtd |
|--------:|---------:|
|    0    | 21790426 |
|    0.66 |      302 |
|    1.31 |       97 |
|    3.28 |       92 |
|    2.62 |       91 |
|    2.29 |       87 |
|    1.97 |       84 |
|  120    |       83 |
|    1.64 |       83 |
|   18.36 |       82 |

#### Coluna: `val_multa_equip_total`

|   valor |      qtd |
|--------:|---------:|
|    0    | 21790426 |
|    0.66 |      302 |
|    1.31 |       97 |
|    3.28 |       92 |
|    2.62 |       91 |
|    2.29 |       87 |
|    1.97 |       84 |
|    1.64 |       83 |
|  120    |       83 |
|   18.36 |       82 |

#### Coluna: `val_multa_fid_item`

|   valor |      qtd |
|--------:|---------:|
|       0 | 21829628 |

#### Coluna: `val_baixa_atividade`

| valor   |     qtd |
|:--------|--------:|
| NULL    | 6118973 |
| 59.89   |  344023 |
| 34.8    |  336600 |
| 49.9    |  327761 |
| 54.9    |  319644 |
| 34.9    |  264599 |
| 29.8    |  248510 |
| 29.9    |  243820 |
| 54.8    |  208396 |
| 64.9    |  143522 |

#### Coluna: `val_original_pagamento`

| valor   |     qtd |
|:--------|--------:|
| NULL    | 6118973 |
| 59.89   |  344023 |
| 34.8    |  336600 |
| 49.9    |  327761 |
| 54.9    |  319644 |
| 34.9    |  264601 |
| 29.8    |  248510 |
| 29.9    |  243820 |
| 54.8    |  208396 |
| 64.9    |  143522 |

#### Coluna: `val_atual_pagamento`

| valor   |     qtd |
|:--------|--------:|
| NULL    | 6118978 |
| 59.89   |  344023 |
| 34.8    |  336602 |
| 49.9    |  327761 |
| 54.9    |  319644 |
| 34.9    |  264599 |
| 29.8    |  248510 |
| 29.9    |  243827 |
| 54.8    |  208397 |
| 64.9    |  143522 |

#### Coluna: `val_pagamento_credito`

| valor   |     qtd |
|:--------|--------:|
| NULL    | 6118973 |
| 34.8    |  336319 |
| 54.9    |  322706 |
| 34.9    |  265861 |
| 29.8    |  248568 |
| 29.9    |  244589 |
| 49.9    |  212998 |
| 54.8    |  208202 |
| 3.12    |  164469 |
| 64.9    |  144258 |

#### Coluna: `seq_fatura`

|   valor |     qtd |
|--------:|--------:|
|       1 | 2176546 |
|       2 | 1522821 |
|       3 | 1308555 |
|       4 |  903376 |
|       5 |  551241 |
|       6 |  379194 |
|       7 |  356303 |
|       8 |  347241 |
|       9 |  342493 |
|      10 |  341171 |

#### Coluna: `num_sub_seq_fatura`

|   valor |     qtd |
|--------:|--------:|
|       1 | 1911132 |
|       2 | 1199278 |
|       3 | 1148202 |
|       4 |  885761 |
|       5 |  593181 |
|       6 |  470040 |
|       7 |  385753 |
|       8 |  371062 |
|       9 |  312043 |
|      10 |  301058 |

#### Coluna: `num_credito_seq`

|   valor |     qtd |
|--------:|--------:|
|       1 | 2309402 |
|       2 | 1655035 |
|       3 | 1222941 |
|       4 |  818495 |
|       5 |  516009 |
|       6 |  377296 |
|       7 |  349161 |
|       8 |  336307 |
|       9 |  332150 |
|      10 |  329832 |

#### Coluna: `dw_tipo_fatura`

|   valor |      qtd |
|--------:|---------:|
|      -2 | 16852336 |
|     118 |  4113913 |
|     146 |   421135 |
|     137 |   107972 |
|     184 |   102420 |
|     117 |    84804 |
|     122 |    49514 |
|     124 |    39634 |
|     167 |    39199 |
|     116 |     8888 |

#### Coluna: `ind_status_fatura`

| valor   |      qtd |
|:--------|---------:|
| C       | 21698270 |
| O       |   131358 |

#### Coluna: `dw_area`

|   valor |      qtd |
|--------:|---------:|
|      -3 | 21454950 |
|      36 |    81382 |
|       1 |    54267 |
|      22 |    17263 |
|       6 |    13406 |
|      23 |    12557 |
|      52 |    12254 |
|      19 |    12125 |
|       7 |    11359 |
|      27 |     7617 |

#### Coluna: `dw_un_negocio`

|   valor |     qtd |
|--------:|--------:|
|       5 | 4392679 |
|       1 | 3416370 |
|       4 | 3312100 |
|       3 | 3096565 |
|       6 | 1777115 |
|       2 | 1409424 |
|       9 | 1245037 |
|       7 | 1163137 |
|      10 | 1036162 |
|       8 |  981039 |

#### Coluna: `dw_forma_pagamento`

|   valor |     qtd |
|--------:|--------:|
|      10 | 9381152 |
|      14 | 8636964 |
|      12 | 3422411 |
|      15 |  389101 |

#### Coluna: `dw_banco`

|   valor |      qtd |
|--------:|---------:|
|      -3 | 14175380 |
|    1368 |  1953004 |
|    1396 |  1644497 |
|    1376 |  1279853 |
|    1694 |  1120685 |
|    1341 |   924342 |
|    1630 |   131060 |
|    1950 |   115930 |
|    1979 |   100190 |
|    1364 |    80760 |

#### Coluna: `dw_tipo_pagamento`

|   valor |     qtd |
|--------:|--------:|
|   30001 | 9381152 |
|   30007 | 8636964 |
|   30003 | 3422411 |
|   30006 |  389101 |

#### Coluna: `num_banco_pagamento`

| valor   |     qtd |
|:--------|--------:|
| -3      | 9958986 |
| NT1     | 2067404 |
| 104     | 2056889 |
| 341     | 1672774 |
| 237     | 1312912 |
| 033     | 1190262 |
| MPG     | 1075007 |
| 001     |  937011 |
| 1044    |  191053 |
| 1043    |  159254 |

#### Coluna: `num_agencia_pagamento`

|   valor |      qtd |
|--------:|---------:|
|      -3 | 11858983 |
|    0000 |  2187845 |
|    2370 |   183248 |
|    0001 |   154962 |
|    2271 |   119988 |
|    2371 |    99921 |
|    2372 |    97271 |
|    2373 |    84583 |
|    0105 |    66351 |
|    3880 |    30065 |

#### Coluna: `num_cc_pagamento`

|          valor |      qtd |
|---------------:|---------:|
|             -3 | 18407246 |
| 00000090277515 |    10188 |
| 00000021631574 |     4569 |
| 00000091727328 |     2998 |
| 00000028847008 |     1107 |
| 00000055984517 |      597 |
|       05419859 |      382 |
|       04369939 |      359 |
|      010777005 |      350 |
| 00000000023884 |      345 |

#### Coluna: `dw_motivo_estorno`

|   valor |      qtd |
|--------:|---------:|
|      -3 | 21829628 |

#### Coluna: `cod_origem_netuno`

| valor           |      qtd |
|:----------------|---------:|
| NULL            | 13566081 |
| 848000000005490 |    32179 |
| 848000000004990 |    31102 |
| 848000000005989 |    25570 |
| 848000000003480 |    17215 |
| 848000000002990 |    16946 |
| 848000000005480 |    16459 |
| 848200000005490 |    16307 |
| 848000000003490 |    16286 |
| 848300000005490 |    16276 |

#### Coluna: `cod_conta_atividade`

| valor     |     qtd |
|:----------|--------:|
| NULL      | 6118973 |
| 966132196 |     258 |
| 103458506 |     214 |
| 104326334 |     208 |
| 206675794 |     194 |
| 148342547 |     180 |
| 143796530 |     179 |
| 142810442 |     159 |
| 147130148 |     154 |
| 159340518 |     150 |

#### Coluna: `seq_entidade_atividade`

| valor   |     qtd |
|:--------|--------:|
| NULL    | 6118973 |
| 1       | 2154176 |
| 2       | 1504746 |
| 3       | 1079994 |
| 4       |  680829 |
| 5       |  384912 |
| 6       |  251832 |
| 7       |  229466 |
| 8       |  220894 |
| 9       |  215866 |

#### Coluna: `cod_login_operador_atividade`

| valor    |      qtd |
|:---------|---------:|
| NULL     | 14215870 |
| 60001    |  7585817 |
| 41002    |    12658 |
| 93257890 |      311 |
| 92546509 |      291 |
| 92597591 |      238 |
| 92531759 |      217 |
| 94146436 |      206 |
| 92344014 |      183 |
| 93278081 |      166 |

#### Coluna: `cod_atividade`

| valor   |      qtd |
|:--------|---------:|
| PYM     | 15692484 |
| NULL    |  6118973 |
| BCK     |    11401 |
| FNTT    |     6656 |
| FNTF    |      113 |
| RFNR    |        1 |

#### Coluna: `cod_razao_atividade`

| valor   |     qtd |
|:--------|--------:|
| NULL    | 8446071 |
| CA      | 7251033 |
| PB      | 5848076 |
| PA      |  266277 |
| ECBBCK  |    7578 |
| FUND    |    6769 |
| ARAUBC  |    3823 |
| DOCDEV  |       1 |

#### Coluna: `cod_fundo_atividade`

| valor     |      qtd |
|:----------|---------:|
| NULL      | 21819036 |
| 127291234 |     1395 |
| 112486948 |     1029 |
| 870146020 |      834 |
| 102816296 |      454 |
| 835361356 |      402 |
| 208728872 |      255 |
| 745991108 |      237 |
| 772940148 |      136 |
| 106673111 |      119 |

#### Coluna: `cod_banco_atividade`

| valor   |      qtd |
|:--------|---------:|
| NULL    | 13732767 |
| NT1     |  1507770 |
| 104     |  1368072 |
| 341     |  1116136 |
| 237     |   855982 |
| 033     |   811600 |
| MPG     |   708060 |
| 001     |   597959 |
| 1044    |   189962 |
| 1043    |   157949 |

#### Coluna: `num_conta_atividade`

| valor          |      qtd |
|:---------------|---------:|
| NULL           | 19502508 |
| 00000090277515 |     6938 |
| 00000021631574 |     3328 |
| 00000091727328 |     2998 |
| 00000028847008 |      385 |
| 00000055984517 |      337 |
| 0086800760     |      320 |
| 010777005      |      282 |
| 05419859       |      260 |
| 126873         |      227 |

#### Coluna: `cod_agencia_atividade`

| valor   |      qtd |
|:--------|---------:|
| NULL    | 15077146 |
| 0000    |  1595685 |
| 2370    |   113810 |
| 0001    |   107370 |
| 2271    |   101966 |
| 2371    |    60969 |
| 2372    |    57694 |
| 2373    |    52830 |
| 0105    |    25554 |
| 3880    |    18831 |

#### Coluna: `seq_entidade_pagamento`

| valor   |     qtd |
|:--------|--------:|
| NULL    | 6118973 |
| 1       | 2154176 |
| 2       | 1504746 |
| 3       | 1079994 |
| 4       |  680829 |
| 5       |  384912 |
| 6       |  251832 |
| 7       |  229466 |
| 8       |  220894 |
| 9       |  215866 |

#### Coluna: `cod_login_pagamento`

| valor    |      qtd |
|:---------|---------:|
| NULL     | 14539993 |
| 60001    |  7261693 |
| 41002    |    12658 |
| 93257890 |      311 |
| 92546509 |      291 |
| 92597591 |      238 |
| 92531759 |      217 |
| 94146436 |      206 |
| 92344014 |      183 |
| 93278081 |      166 |

#### Coluna: `cod_forma_pagamento`

| valor   |     qtd |
|:--------|--------:|
| CA      | 7251673 |
| NULL    | 6118973 |
| PB      | 5865567 |
| DD      | 2327120 |
| PA      |  266295 |

#### Coluna: `cod_tipo_pagamento`

| valor   |     qtd |
|:--------|--------:|
| O       | 7239233 |
| NULL    | 6118973 |
| P       | 5769643 |
| D       | 2327120 |
| B       |  362219 |
| E       |   12440 |

#### Coluna: `dsc_nome_banco_pagamento`

| valor    |     qtd |
|:---------|--------:|
| CPAY-PIX | 6192697 |
| NULL     | 6118973 |
| NET1     | 2460975 |
| CEF      | 1730111 |
| ITAU     | 1116136 |
| BRADES   |  856068 |
| BANESPA  |  811601 |
| MULTI-PG |  708077 |
| BRASIL   |  598518 |
| GEVEN1P  |  189962 |

#### Coluna: `seq_arquivo_pagamento`

| valor   |      qtd |
|:--------|---------:|
| NULL    | 13775460 |
| 6340    |    61384 |
| 6285    |    51661 |
| 5298    |    41044 |
| 6156    |    36635 |
| 6296    |    34778 |
| 6328    |    31106 |
| 6852    |    30180 |
| 6211    |    28289 |
| 6274    |    27746 |

#### Coluna: `num_parcela_pagamento`

| valor   |      qtd |
|:--------|---------:|
| NULL    | 21268211 |
| 458     |    10247 |
| 423     |     9539 |
| 463     |     7508 |
| 424     |     7253 |
| 457     |     6770 |
| 459     |     5903 |
| 464     |     5594 |
| 471     |     4898 |
| 394     |     4756 |

#### Coluna: `num_agrupador_pagamento`

| valor   |      qtd |
|:--------|---------:|
| NULL    | 16102580 |
| 2       |     1797 |
| 1       |     1777 |
| 5       |     1624 |
| 4       |     1592 |
| 3       |     1554 |
| 6       |     1534 |
| 8       |     1481 |
| 11      |     1470 |
| 7       |     1451 |

#### Coluna: `dsc_pagamento`

| valor                                               |      qtd |
|:----------------------------------------------------|---------:|
| NULL                                                | 18848477 |
| Arquivo Rajada Sequencia: 21987, Registro: 00000067 |      143 |
| Arquivo Rajada Sequencia: 23862, Registro: 00000017 |      113 |
| Arquivo Rajada Sequencia: 24142, Registro: 00000031 |       96 |
| Arquivo Rajada Sequencia: 24395, Registro: 00000054 |       95 |
| Arquivo Rajada Sequencia: 11769, Registro: 00001397 |       93 |
| Arquivo Rajada Sequencia: 11769, Registro: 00001396 |       90 |
| Arquivo Rajada Sequencia: 11471, Registro: 00001477 |       89 |
| Arquivo Rajada Sequencia: 24762, Registro: 00000344 |       89 |
| Arquivo Rajada Sequencia: 24762, Registro: 00000437 |       88 |

#### Coluna: `cod_metodo_pagamento`

| valor   |      qtd |
|:--------|---------:|
| NULL    | 16297184 |
| 1       |  1657841 |
| 3       |  1538749 |
| 5       |  1401465 |
| 4       |   647567 |
| 2       |   285169 |
| 6       |     1653 |

#### Coluna: `ind_status_pagamento`

| valor   |     qtd |
|:--------|--------:|
| R       | 9478841 |
| NULL    | 8996090 |
| C       | 2938458 |
| P       |  404814 |
| B       |   11425 |

#### Coluna: `cod_arquivo_pagamento`

| valor                |      qtd |
|:---------------------|---------:|
| NULL                 | 18390641 |
| 6747200000000240924C |      148 |
| 1981200000000030624C |      142 |
| 4779200000000220824C |      128 |
| 2875200000000241024C |      127 |
| 6908200000000250724C |      122 |
| 5912200000000250624C |      122 |
| 1178200000000020524C |      117 |
| 4878200000000090125C |      111 |
| 8050091012345270125C |      109 |

#### Coluna: `cod_netuno_pagamento`

| valor   |      qtd |
|:--------|---------:|
| NULL    | 21829628 |

#### Coluna: `cod_login_credito`

| valor    |      qtd |
|:---------|---------:|
| NULL     | 14223305 |
| 60001    |  7576501 |
| 41002    |    12029 |
| 41003    |     1445 |
| 93257890 |      311 |
| 92546509 |      291 |
| 92597591 |      238 |
| 92531759 |      217 |
| 94146436 |      206 |
| 92344014 |      183 |

#### Coluna: `ind_tipo_credito`

| valor   |      qtd |
|:--------|---------:|
| P       | 15710655 |
| NULL    |  6118973 |

#### Coluna: `seq_pagamento_credito`

| valor   |     qtd |
|:--------|--------:|
| NULL    | 6118973 |
| 1       | 2154176 |
| 2       | 1504746 |
| 3       | 1079994 |
| 4       |  680829 |
| 5       |  384912 |
| 6       |  251832 |
| 7       |  229466 |
| 8       |  220894 |
| 9       |  215866 |

#### Coluna: `seq_fatura_credito`

| valor   |     qtd |
|:--------|--------:|
| NULL    | 6118973 |
| 1       | 1784745 |
| 2       | 1077354 |
| 3       | 1028928 |
| 4       |  771562 |
| 5       |  483752 |
| 6       |  364357 |
| 7       |  283689 |
| 8       |  270977 |
| 9       |  214614 |

#### Coluna: `cod_alocacao_credito`

| valor   |      qtd |
|:--------|---------:|
| PYM     | 14949068 |
| NULL    |  6118973 |
| CRT     |   695700 |
| CRTW    |    49132 |
| CRF     |     6601 |
| FNTT    |     5505 |
| BCK     |     4086 |
| RFN     |      532 |
| FNTF    |       31 |

#### Coluna: `cod_desalocacao_credito`

| valor   |      qtd |
|:--------|---------:|
| NULL    | 21829628 |

#### Coluna: `seq_entidade_credito`

| valor   |     qtd |
|:--------|--------:|
| NULL    | 6118973 |
| 1       | 1812152 |
| 2       | 1284694 |
| 3       |  909899 |
| 4       |  678526 |
| 5       |  426893 |
| 6       |  328812 |
| 7       |  252187 |
| 8       |  232996 |
| 9       |  186425 |

#### Coluna: `cod_tipo_fatura`

| valor   |      qtd |
|:--------|---------:|
| B       | 12251645 |
| NULL    |  6118973 |
| 21      |  2871259 |
| PA      |   284316 |
| P1      |    73627 |
| T2      |    70352 |
| 15      |    54042 |
| FE      |    34081 |
| 31      |    32123 |
| 41      |    25651 |

#### Coluna: `ingestion_ts`

| valor                         |      qtd |
|:------------------------------|---------:|
| 2026-01-08 17:41:06.467416-03 | 21829628 |

#### Coluna: `ano_mes`

|   valor |     qtd |
|--------:|--------:|
|  202503 | 2465787 |
|  202502 | 2015493 |
|  202501 | 1771821 |
|  202412 | 1501147 |
|  202411 | 1189482 |
|  202410 | 1112563 |
|  202408 | 1074927 |
|  202407 | 1068676 |
|  202409 | 1050711 |
|  202405 | 1043511 |

#### Coluna: `run_id`

|           valor |      qtd |
|----------------:|---------:|
| 20260108_204106 | 21829628 |



---

