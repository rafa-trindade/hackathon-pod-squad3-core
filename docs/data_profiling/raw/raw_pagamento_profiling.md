# Relatório de Profiling: `raw/pagamento`

### 📦 Volumetria: `raw/pagamento`
|   qtd_arquivos | registros   |   colunas |   tamanho_comprimido_mib |   tamanho_descomprimido_mib |
|---------------:|:------------|----------:|-------------------------:|----------------------------:|
|             10 | 21.829.628  |        73 |                   2115.3 |                     3677.08 |

---

### 🧬 Schema: `raw/pagamento`
| column_name                  | column_type   | null   | key   | default   | extra   |
|:-----------------------------|:--------------|:-------|:------|:----------|:--------|
| NUM_CPF                      | VARCHAR       | YES    |       |           |         |
| DAT_STATUS_FATURA            | VARCHAR       | YES    |       |           |         |
| CONTRATO                     | VARCHAR       | YES    |       |           |         |
| SEQ_FATURA                   | VARCHAR       | YES    |       |           |         |
| NUM_SUB_SEQ_FATURA           | VARCHAR       | YES    |       |           |         |
| NUM_CREDITO_SEQ              | VARCHAR       | YES    |       |           |         |
| DW_TIPO_FATURA               | VARCHAR       | YES    |       |           |         |
| IND_STATUS_FATURA            | VARCHAR       | YES    |       |           |         |
| DW_NUM_CLIENTE               | VARCHAR       | YES    |       |           |         |
| DW_AREA                      | VARCHAR       | YES    |       |           |         |
| DW_UN_NEGOCIO                | VARCHAR       | YES    |       |           |         |
| DW_FORMA_PAGAMENTO           | VARCHAR       | YES    |       |           |         |
| VAL_PAGAMENTO_FATURA         | VARCHAR       | YES    |       |           |         |
| DAT_CRIACAO_DW               | VARCHAR       | YES    |       |           |         |
| DW_BANCO                     | VARCHAR       | YES    |       |           |         |
| DW_TIPO_PAGAMENTO            | VARCHAR       | YES    |       |           |         |
| NUM_BANCO_PAGAMENTO          | VARCHAR       | YES    |       |           |         |
| NUM_AGENCIA_PAGAMENTO        | VARCHAR       | YES    |       |           |         |
| NUM_CC_PAGAMENTO             | VARCHAR       | YES    |       |           |         |
| DW_MOTIVO_ESTORNO            | VARCHAR       | YES    |       |           |         |
| VAL_DESCONTO_ITEM            | VARCHAR       | YES    |       |           |         |
| VAL_PAGAMENTO_ITEM           | VARCHAR       | YES    |       |           |         |
| VAL_JUROS_MULTAS_ITEM        | VARCHAR       | YES    |       |           |         |
| VAL_MULTA_EQUIP_ITEM         | VARCHAR       | YES    |       |           |         |
| VAL_MULTA_EQUIP_TOTAL        | VARCHAR       | YES    |       |           |         |
| VAL_MULTA_FID_ITEM           | VARCHAR       | YES    |       |           |         |
| COD_ORIGEM_NETUNO            | VARCHAR       | YES    |       |           |         |
| COD_CONTA_ATIVIDADE          | VARCHAR       | YES    |       |           |         |
| SEQ_ENTIDADE_ATIVIDADE       | VARCHAR       | YES    |       |           |         |
| DAT_CRIACAO_ATIVIDADE        | VARCHAR       | YES    |       |           |         |
| DAT_ATUALIZACAO_ATIVIDADE    | VARCHAR       | YES    |       |           |         |
| COD_LOGIN_OPERADOR_ATIVIDADE | VARCHAR       | YES    |       |           |         |
| COD_ATIVIDADE                | VARCHAR       | YES    |       |           |         |
| COD_RAZAO_ATIVIDADE          | VARCHAR       | YES    |       |           |         |
| DAT_BAIXA_ATIVIDADE          | VARCHAR       | YES    |       |           |         |
| VAL_BAIXA_ATIVIDADE          | VARCHAR       | YES    |       |           |         |
| DAT_DEPOSITO_ATIVIDADE       | VARCHAR       | YES    |       |           |         |
| COD_FUNDO_ATIVIDADE          | VARCHAR       | YES    |       |           |         |
| COD_BANCO_ATIVIDADE          | VARCHAR       | YES    |       |           |         |
| NUM_CONTA_ATIVIDADE          | VARCHAR       | YES    |       |           |         |
| COD_AGENCIA_ATIVIDADE        | VARCHAR       | YES    |       |           |         |
| SEQ_ENTIDADE_PAGAMENTO       | VARCHAR       | YES    |       |           |         |
| DAT_CRIACAO_PAGAMENTO        | VARCHAR       | YES    |       |           |         |
| DAT_ATUALIZACAO_PAGAMENTO    | VARCHAR       | YES    |       |           |         |
| COD_LOGIN_PAGAMENTO          | VARCHAR       | YES    |       |           |         |
| COD_FORMA_PAGAMENTO          | VARCHAR       | YES    |       |           |         |
| VAL_ORIGINAL_PAGAMENTO       | VARCHAR       | YES    |       |           |         |
| NUM_FATURA_PAGAMENTO         | VARCHAR       | YES    |       |           |         |
| COD_TIPO_PAGAMENTO           | VARCHAR       | YES    |       |           |         |
| DSC_NOME_BANCO_PAGAMENTO     | VARCHAR       | YES    |       |           |         |
| SEQ_ARQUIVO_PAGAMENTO        | VARCHAR       | YES    |       |           |         |
| NUM_PARCELA_PAGAMENTO        | VARCHAR       | YES    |       |           |         |
| NUM_AGRUPADOR_PAGAMENTO      | VARCHAR       | YES    |       |           |         |
| DSC_PAGAMENTO                | VARCHAR       | YES    |       |           |         |
| VAL_ATUAL_PAGAMENTO          | VARCHAR       | YES    |       |           |         |
| COD_METODO_PAGAMENTO         | VARCHAR       | YES    |       |           |         |
| IND_STATUS_PAGAMENTO         | VARCHAR       | YES    |       |           |         |
| DAT_STATUS_PAGAMENTO         | VARCHAR       | YES    |       |           |         |
| COD_ARQUIVO_PAGAMENTO        | VARCHAR       | YES    |       |           |         |
| COD_NETUNO_PAGAMENTO         | VARCHAR       | YES    |       |           |         |
| DAT_CRIACAO_CREDITO          | VARCHAR       | YES    |       |           |         |
| DAT_ATUALIZACAO_CREDITO      | VARCHAR       | YES    |       |           |         |
| COD_LOGIN_CREDITO            | VARCHAR       | YES    |       |           |         |
| VAL_PAGAMENTO_CREDITO        | VARCHAR       | YES    |       |           |         |
| IND_TIPO_CREDITO             | VARCHAR       | YES    |       |           |         |
| SEQ_PAGAMENTO_CREDITO        | VARCHAR       | YES    |       |           |         |
| SEQ_FATURA_CREDITO           | VARCHAR       | YES    |       |           |         |
| COD_ALOCACAO_CREDITO         | VARCHAR       | YES    |       |           |         |
| COD_DESALOCACAO_CREDITO      | VARCHAR       | YES    |       |           |         |
| SEQ_ENTIDADE_CREDITO         | VARCHAR       | YES    |       |           |         |
| COD_TIPO_FATURA              | VARCHAR       | YES    |       |           |         |
| DAT_ATIVIDADE_CREDITO        | VARCHAR       | YES    |       |           |         |
| DAT_VENCIMENTO_CREDITO       | VARCHAR       | YES    |       |           |         |

---

### 📅 Campos de Data: `raw/pagamento`
#### ✅ Datas com tipagem (DATE / TIMESTAMP)
> ⚠️ Nenhuma coluna DATE ou TIMESTAMP encontrada.

#### ⚠️ Possíveis campos de data/hora sem tipagem (inferido pelo nome)

- `DAT_ATIVIDADE_CREDITO`
- `DAT_ATUALIZACAO_ATIVIDADE`
- `DAT_ATUALIZACAO_CREDITO`
- `DAT_ATUALIZACAO_PAGAMENTO`
- `DAT_BAIXA_ATIVIDADE`
- `DAT_CRIACAO_ATIVIDADE`
- `DAT_CRIACAO_CREDITO`
- `DAT_CRIACAO_DW`
- `DAT_CRIACAO_PAGAMENTO`
- `DAT_DEPOSITO_ATIVIDADE`
- `DAT_STATUS_FATURA`
- `DAT_STATUS_PAGAMENTO`
- `DAT_VENCIMENTO_CREDITO`


---

### 📊 Estatísticas por Coluna: `raw/pagamento`
| coluna                       |   distintos |    nulos |   duplicados | pct_nulos   | pct_duplicados   | cardinalidade   |
|:-----------------------------|------------:|---------:|-------------:|:------------|:-----------------|:----------------|
| NUM_CPF                      |     1930502 |        0 |     19899126 | 0.0%        | 91.16%           | ALTA            |
| DAT_STATUS_FATURA            |         548 |        0 |     21829080 | 0.0%        | 100.0%           | BAIXA           |
| CONTRATO                     |     2672803 |        0 |     19156825 | 0.0%        | 87.76%           | ALTA            |
| SEQ_FATURA                   |         258 |        0 |     21829370 | 0.0%        | 100.0%           | BAIXA           |
| NUM_SUB_SEQ_FATURA           |        1163 |        0 |     21828465 | 0.0%        | 99.99%           | BAIXA           |
| NUM_CREDITO_SEQ              |         363 |        0 |     21829265 | 0.0%        | 100.0%           | BAIXA           |
| DW_TIPO_FATURA               |          25 |        0 |     21829603 | 0.0%        | 100.0%           | BAIXA           |
| IND_STATUS_FATURA            |           2 |        0 |     21829626 | 0.0%        | 100.0%           | BAIXA           |
| DW_NUM_CLIENTE               |     2796110 |        0 |     19033518 | 0.0%        | 87.19%           | ALTA            |
| DW_AREA                      |          68 |        0 |     21829560 | 0.0%        | 100.0%           | BAIXA           |
| DW_UN_NEGOCIO                |          10 |        0 |     21829618 | 0.0%        | 100.0%           | BAIXA           |
| DW_FORMA_PAGAMENTO           |           4 |        0 |     21829624 | 0.0%        | 100.0%           | BAIXA           |
| VAL_PAGAMENTO_FATURA         |       66138 |        0 |     21763490 | 0.0%        | 99.7%            | MEDIA           |
| DAT_CRIACAO_DW               |       58092 |        0 |     21771536 | 0.0%        | 99.73%           | MEDIA           |
| DW_BANCO                     |          59 |        0 |     21829569 | 0.0%        | 100.0%           | BAIXA           |
| DW_TIPO_PAGAMENTO            |           4 |        0 |     21829624 | 0.0%        | 100.0%           | BAIXA           |
| NUM_BANCO_PAGAMENTO          |          41 |        0 |     21829587 | 0.0%        | 100.0%           | BAIXA           |
| NUM_AGENCIA_PAGAMENTO        |        9266 |        0 |     21820362 | 0.0%        | 99.96%           | BAIXA           |
| NUM_CC_PAGAMENTO             |      288970 |        0 |     21540658 | 0.0%        | 98.68%           | MEDIA           |
| DW_MOTIVO_ESTORNO            |           1 |        0 |     21829627 | 0.0%        | 100.0%           | BAIXA           |
| VAL_DESCONTO_ITEM            |           1 |        0 |     21829627 | 0.0%        | 100.0%           | BAIXA           |
| VAL_PAGAMENTO_ITEM           |       66138 |        0 |     21763490 | 0.0%        | 99.7%            | MEDIA           |
| VAL_JUROS_MULTAS_ITEM        |        5081 |        0 |     21824547 | 0.0%        | 99.98%           | BAIXA           |
| VAL_MULTA_EQUIP_ITEM         |        6801 |        0 |     21822827 | 0.0%        | 99.97%           | BAIXA           |
| VAL_MULTA_EQUIP_TOTAL        |        6801 |        0 |     21822827 | 0.0%        | 99.97%           | BAIXA           |
| VAL_MULTA_FID_ITEM           |           1 |        0 |     21829627 | 0.0%        | 100.0%           | BAIXA           |
| COD_ORIGEM_NETUNO            |      341773 | 13566081 |     21487855 | 62.15%      | 98.43%           | MEDIA           |
| COD_CONTA_ATIVIDADE          |     2663418 |  6118973 |     19166210 | 28.03%      | 87.8%            | ALTA            |
| SEQ_ENTIDADE_ATIVIDADE       |         357 |  6118973 |     21829271 | 28.03%      | 100.0%           | BAIXA           |
| DAT_CRIACAO_ATIVIDADE        |     6206923 |  6118973 |     15622705 | 28.03%      | 71.57%           | ALTA            |
| DAT_ATUALIZACAO_ATIVIDADE    |      394598 | 20730830 |     21435030 | 94.97%      | 98.19%           | MEDIA           |
| COD_LOGIN_OPERADOR_ATIVIDADE |         905 | 14215870 |     21828723 | 65.12%      | 100.0%           | BAIXA           |
| COD_ATIVIDADE                |           5 |  6118973 |     21829623 | 28.03%      | 100.0%           | BAIXA           |
| COD_RAZAO_ATIVIDADE          |           7 |  8446071 |     21829621 | 38.69%      | 100.0%           | BAIXA           |
| DAT_BAIXA_ATIVIDADE          |         350 |  6118973 |     21829278 | 28.03%      | 100.0%           | BAIXA           |
| VAL_BAIXA_ATIVIDADE          |       68454 |  6118973 |     21761174 | 28.03%      | 99.69%           | MEDIA           |
| DAT_DEPOSITO_ATIVIDADE       |         695 |  6118973 |     21828933 | 28.03%      | 100.0%           | BAIXA           |
| COD_FUNDO_ATIVIDADE          |        1478 | 21819036 |     21828150 | 99.95%      | 99.99%           | BAIXA           |
| COD_BANCO_ATIVIDADE          |          38 | 13732767 |     21829590 | 62.91%      | 100.0%           | BAIXA           |
| NUM_CONTA_ATIVIDADE          |      272210 | 19502508 |     21557418 | 89.34%      | 98.75%           | MEDIA           |
| COD_AGENCIA_ATIVIDADE        |        9236 | 15077146 |     21820392 | 69.07%      | 99.96%           | BAIXA           |
| SEQ_ENTIDADE_PAGAMENTO       |         357 |  6118973 |     21829271 | 28.03%      | 100.0%           | BAIXA           |
| DAT_CRIACAO_PAGAMENTO        |     6205107 |  6118973 |     15624521 | 28.03%      | 71.57%           | ALTA            |
| DAT_ATUALIZACAO_PAGAMENTO    |      185327 | 18882483 |     21644301 | 86.5%       | 99.15%           | MEDIA           |
| COD_LOGIN_PAGAMENTO          |         905 | 14539993 |     21828723 | 66.61%      | 100.0%           | BAIXA           |
| COD_FORMA_PAGAMENTO          |           4 |  6118973 |     21829624 | 28.03%      | 100.0%           | BAIXA           |
| VAL_ORIGINAL_PAGAMENTO       |       61749 |  6118973 |     21767879 | 28.03%      | 99.72%           | MEDIA           |
| NUM_FATURA_PAGAMENTO         |    11907562 |  6845630 |      9922066 | 31.36%      | 45.45%           | ALTA            |
| COD_TIPO_PAGAMENTO           |           5 |  6118973 |     21829623 | 28.03%      | 100.0%           | BAIXA           |
| DSC_NOME_BANCO_PAGAMENTO     |          83 |  6118973 |     21829545 | 28.03%      | 100.0%           | BAIXA           |
| SEQ_ARQUIVO_PAGAMENTO        |        6788 | 13775460 |     21822840 | 63.1%       | 99.97%           | BAIXA           |
| NUM_PARCELA_PAGAMENTO        |         652 | 21268211 |     21828976 | 97.43%      | 100.0%           | BAIXA           |
| NUM_AGRUPADOR_PAGAMENTO      |      317457 | 16102580 |     21512171 | 73.76%      | 98.55%           | MEDIA           |
| DSC_PAGAMENTO                |     1959588 | 18848477 |     19870040 | 86.34%      | 91.02%           | ALTA            |
| VAL_ATUAL_PAGAMENTO          |       64407 |  6118978 |     21765221 | 28.03%      | 99.7%            | MEDIA           |
| COD_METODO_PAGAMENTO         |           6 | 16297184 |     21829622 | 74.66%      | 100.0%           | BAIXA           |
| IND_STATUS_PAGAMENTO         |           4 |  8996090 |     21829624 | 41.21%      | 100.0%           | BAIXA           |
| DAT_STATUS_PAGAMENTO         |         367 |  6118973 |     21829261 | 28.03%      | 100.0%           | BAIXA           |
| COD_ARQUIVO_PAGAMENTO        |     2597204 | 18390641 |     19232424 | 84.25%      | 88.1%            | ALTA            |
| COD_NETUNO_PAGAMENTO         |           0 | 21829628 |     21829628 | 100.0%      | 100.0%           | BAIXA           |
| DAT_CRIACAO_CREDITO          |     6225621 |  6118973 |     15604007 | 28.03%      | 71.48%           | ALTA            |
| DAT_ATUALIZACAO_CREDITO      |           0 | 21829628 |     21829628 | 100.0%      | 100.0%           | BAIXA           |
| COD_LOGIN_CREDITO            |        1228 | 14223305 |     21828400 | 65.16%      | 99.99%           | BAIXA           |
| VAL_PAGAMENTO_CREDITO        |       57842 |  6118973 |     21771786 | 28.03%      | 99.74%           | MEDIA           |
| IND_TIPO_CREDITO             |           1 |  6118973 |     21829627 | 28.03%      | 100.0%           | BAIXA           |
| SEQ_PAGAMENTO_CREDITO        |         357 |  6118973 |     21829271 | 28.03%      | 100.0%           | BAIXA           |
| SEQ_FATURA_CREDITO           |        1111 |  6118973 |     21828517 | 28.03%      | 99.99%           | BAIXA           |
| COD_ALOCACAO_CREDITO         |           8 |  6118973 |     21829620 | 28.03%      | 100.0%           | BAIXA           |
| COD_DESALOCACAO_CREDITO      |           0 | 21829628 |     21829628 | 100.0%      | 100.0%           | BAIXA           |
| SEQ_ENTIDADE_CREDITO         |        5838 |  6118973 |     21823790 | 28.03%      | 99.97%           | BAIXA           |
| COD_TIPO_FATURA              |          27 |  6118973 |     21829601 | 28.03%      | 100.0%           | BAIXA           |
| DAT_ATIVIDADE_CREDITO        |         514 |  6118973 |     21829114 | 28.03%      | 100.0%           | BAIXA           |
| DAT_VENCIMENTO_CREDITO       |        1350 |  6118973 |     21828278 | 28.03%      | 99.99%           | BAIXA           |

---

### 🔟 Distribuição de Valores (Top 10): `raw/pagamento`
#### Coluna: `NUM_CPF`

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

#### Coluna: `DAT_STATUS_FATURA`

| valor              |    qtd |
|:-------------------|-------:|
| 11MAR2025:00:00:00 | 237845 |
| 06MAR2025:00:00:00 | 208120 |
| 11FEB2025:00:00:00 | 167344 |
| 06FEB2025:00:00:00 | 143259 |
| 10MAR2025:00:00:00 | 142721 |
| 18MAR2025:00:00:00 | 142504 |
| 21MAR2025:00:00:00 | 137487 |
| 07MAR2025:00:00:00 | 133100 |
| 07JAN2025:00:00:00 | 128795 |
| 18FEB2025:00:00:00 | 127701 |

#### Coluna: `CONTRATO`

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

#### Coluna: `SEQ_FATURA`

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

#### Coluna: `NUM_SUB_SEQ_FATURA`

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

#### Coluna: `NUM_CREDITO_SEQ`

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

#### Coluna: `DW_TIPO_FATURA`

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

#### Coluna: `IND_STATUS_FATURA`

| valor   |      qtd |
|:--------|---------:|
| C       | 21698270 |
| O       |   131358 |

#### Coluna: `DW_NUM_CLIENTE`

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

#### Coluna: `DW_AREA`

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

#### Coluna: `DW_UN_NEGOCIO`

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

#### Coluna: `DW_FORMA_PAGAMENTO`

|   valor |     qtd |
|--------:|--------:|
|      10 | 9381152 |
|      14 | 8636964 |
|      12 | 3422411 |
|      15 |  389101 |

#### Coluna: `VAL_PAGAMENTO_FATURA`

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

#### Coluna: `DAT_CRIACAO_DW`

| valor              |   qtd |
|:-------------------|------:|
| 23FEB2025:17:29:12 | 44444 |
| 03MAR2025:09:59:28 | 44035 |
| 24FEB2025:09:54:38 | 42553 |
| 09MAR2025:11:17:51 | 42038 |
| 15MAR2025:23:10:40 | 41664 |
| 09MAR2025:11:17:50 | 40929 |
| 09MAR2025:11:17:52 | 38850 |
| 11MAR2025:06:46:19 | 38813 |
| 16MAR2025:12:33:13 | 37978 |
| 15MAR2025:23:10:41 | 37733 |

#### Coluna: `DW_BANCO`

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

#### Coluna: `DW_TIPO_PAGAMENTO`

|   valor |     qtd |
|--------:|--------:|
|   30001 | 9381152 |
|   30007 | 8636964 |
|   30003 | 3422411 |
|   30006 |  389101 |

#### Coluna: `NUM_BANCO_PAGAMENTO`

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

#### Coluna: `NUM_AGENCIA_PAGAMENTO`

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

#### Coluna: `NUM_CC_PAGAMENTO`

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

#### Coluna: `DW_MOTIVO_ESTORNO`

|   valor |      qtd |
|--------:|---------:|
|      -3 | 21829628 |

#### Coluna: `VAL_DESCONTO_ITEM`

|   valor |      qtd |
|--------:|---------:|
|       0 | 21829628 |

#### Coluna: `VAL_PAGAMENTO_ITEM`

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

#### Coluna: `VAL_JUROS_MULTAS_ITEM`

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

#### Coluna: `VAL_MULTA_EQUIP_ITEM`

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

#### Coluna: `VAL_MULTA_EQUIP_TOTAL`

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

#### Coluna: `VAL_MULTA_FID_ITEM`

|   valor |      qtd |
|--------:|---------:|
|       0 | 21829628 |

#### Coluna: `COD_ORIGEM_NETUNO`

|           valor |      qtd |
|----------------:|---------:|
|                 | 13566081 |
| 848000000005490 |    32179 |
| 848000000004990 |    31102 |
| 848000000005989 |    25570 |
| 848000000003480 |    17215 |
| 848000000002990 |    16946 |
| 848000000005480 |    16459 |
| 848200000005490 |    16307 |
| 848000000003490 |    16286 |
| 848300000005490 |    16276 |

#### Coluna: `COD_CONTA_ATIVIDADE`

|     valor |     qtd |
|----------:|--------:|
|           | 6118973 |
| 966132196 |     258 |
| 103458506 |     214 |
| 104326334 |     208 |
| 206675794 |     194 |
| 148342547 |     180 |
| 143796530 |     179 |
| 142810442 |     159 |
| 147130148 |     154 |
| 159340518 |     150 |

#### Coluna: `SEQ_ENTIDADE_ATIVIDADE`

|   valor |     qtd |
|--------:|--------:|
|         | 6118973 |
|       1 | 2154176 |
|       2 | 1504746 |
|       3 | 1079994 |
|       4 |  680829 |
|       5 |  384912 |
|       6 |  251832 |
|       7 |  229466 |
|       8 |  220894 |
|       9 |  215866 |

#### Coluna: `DAT_CRIACAO_ATIVIDADE`

| valor              |     qtd |
|:-------------------|--------:|
|                    | 6118973 |
| 06MAR2025:14:36:18 |     250 |
| 06MAR2025:14:36:43 |     245 |
| 06MAR2025:14:36:07 |     241 |
| 21FEB2025:12:47:38 |     236 |
| 06MAR2025:14:36:36 |     235 |
| 21FEB2025:12:47:16 |     235 |
| 06MAR2025:14:36:11 |     234 |
| 21FEB2025:12:47:22 |     233 |
| 06MAR2025:14:36:38 |     232 |

#### Coluna: `DAT_ATUALIZACAO_ATIVIDADE`

| valor              |      qtd |
|:-------------------|---------:|
|                    | 20730830 |
| 18FEB2025:18:54:47 |      238 |
| 18FEB2025:18:54:52 |      225 |
| 18FEB2025:18:54:51 |      218 |
| 18FEB2025:18:54:50 |      204 |
| 18FEB2025:18:54:48 |      186 |
| 12MAR2025:04:19:30 |      182 |
| 18FEB2025:18:54:49 |      169 |
| 08JAN2025:03:40:08 |      167 |
| 08FEB2025:05:25:18 |      167 |

#### Coluna: `COD_LOGIN_OPERADOR_ATIVIDADE`

|    valor |      qtd |
|---------:|---------:|
|          | 14215870 |
|    60001 |  7585817 |
|    41002 |    12658 |
| 93257890 |      311 |
| 92546509 |      291 |
| 92597591 |      238 |
| 92531759 |      217 |
| 94146436 |      206 |
| 92344014 |      183 |
| 93278081 |      166 |

#### Coluna: `COD_ATIVIDADE`

| valor   |      qtd |
|:--------|---------:|
| PYM     | 15692484 |
|         |  6118973 |
| BCK     |    11401 |
| FNTT    |     6656 |
| FNTF    |      113 |
| RFNR    |        1 |

#### Coluna: `COD_RAZAO_ATIVIDADE`

| valor   |     qtd |
|:--------|--------:|
|         | 8446071 |
| CA      | 7251033 |
| PB      | 5848076 |
| PA      |  266277 |
| ECBBCK  |    7578 |
| FUND    |    6769 |
| ARAUBC  |    3823 |
| DOCDEV  |       1 |

#### Coluna: `DAT_BAIXA_ATIVIDADE`

| valor              |     qtd |
|:-------------------|--------:|
|                    | 6118973 |
| 11MAR2025:00:00:00 |  237845 |
| 06MAR2025:00:00:00 |  208120 |
| 11FEB2025:00:00:00 |  167344 |
| 06FEB2025:00:00:00 |  143259 |
| 10MAR2025:00:00:00 |  142721 |
| 18MAR2025:00:00:00 |  142504 |
| 21MAR2025:00:00:00 |  137487 |
| 07MAR2025:00:00:00 |  133100 |
| 07JAN2025:00:00:00 |  128795 |

#### Coluna: `VAL_BAIXA_ATIVIDADE`

|   valor |     qtd |
|--------:|--------:|
|         | 6118973 |
|   59.89 |  344023 |
|   34.8  |  336600 |
|   49.9  |  327761 |
|   54.9  |  319644 |
|   34.9  |  264599 |
|   29.8  |  248510 |
|   29.9  |  243820 |
|   54.8  |  208396 |
|   64.9  |  143522 |

#### Coluna: `DAT_DEPOSITO_ATIVIDADE`

| valor              |     qtd |
|:-------------------|--------:|
|                    | 6118973 |
| 10MAR2025:00:00:00 |  324945 |
| 10FEB2025:00:00:00 |  271932 |
| 05MAR2025:00:00:00 |  193490 |
| 17MAR2025:00:00:00 |  172723 |
| 10JAN2025:00:00:00 |  165489 |
| 20MAR2025:00:00:00 |  165082 |
| 17FEB2025:00:00:00 |  148657 |
| 20FEB2025:00:00:00 |  140404 |
| 10DEC2024:00:00:00 |  139575 |

#### Coluna: `COD_FUNDO_ATIVIDADE`

|     valor |      qtd |
|----------:|---------:|
|           | 21819036 |
| 127291234 |     1395 |
| 112486948 |     1029 |
| 870146020 |      834 |
| 102816296 |      454 |
| 835361356 |      402 |
| 208728872 |      255 |
| 745991108 |      237 |
| 772940148 |      136 |
| 106673111 |      119 |

#### Coluna: `COD_BANCO_ATIVIDADE`

| valor   |      qtd |
|:--------|---------:|
|         | 13732767 |
| NT1     |  1507770 |
| 104     |  1368072 |
| 341     |  1116136 |
| 237     |   855982 |
| 033     |   811600 |
| MPG     |   708060 |
| 001     |   597959 |
| 1044    |   189962 |
| 1043    |   157949 |

#### Coluna: `NUM_CONTA_ATIVIDADE`

|          valor |      qtd |
|---------------:|---------:|
|                | 19502508 |
| 00000090277515 |     6938 |
| 00000021631574 |     3328 |
| 00000091727328 |     2998 |
| 00000028847008 |      385 |
| 00000055984517 |      337 |
|     0086800760 |      320 |
|      010777005 |      282 |
|       05419859 |      260 |
|         126873 |      227 |

#### Coluna: `COD_AGENCIA_ATIVIDADE`

|   valor |      qtd |
|--------:|---------:|
|         | 15077146 |
|    0000 |  1595685 |
|    2370 |   113810 |
|    0001 |   107370 |
|    2271 |   101966 |
|    2371 |    60969 |
|    2372 |    57694 |
|    2373 |    52830 |
|    0105 |    25554 |
|    3880 |    18831 |

#### Coluna: `SEQ_ENTIDADE_PAGAMENTO`

|   valor |     qtd |
|--------:|--------:|
|         | 6118973 |
|       1 | 2154176 |
|       2 | 1504746 |
|       3 | 1079994 |
|       4 |  680829 |
|       5 |  384912 |
|       6 |  251832 |
|       7 |  229466 |
|       8 |  220894 |
|       9 |  215866 |

#### Coluna: `DAT_CRIACAO_PAGAMENTO`

| valor              |     qtd |
|:-------------------|--------:|
|                    | 6118973 |
| 06MAR2025:14:36:18 |     250 |
| 06MAR2025:14:36:43 |     245 |
| 06MAR2025:14:36:07 |     241 |
| 21FEB2025:12:47:38 |     236 |
| 21FEB2025:12:47:16 |     234 |
| 06MAR2025:14:36:11 |     234 |
| 21FEB2025:12:47:22 |     233 |
| 06MAR2025:14:36:36 |     233 |
| 06MAR2025:14:36:38 |     232 |

#### Coluna: `DAT_ATUALIZACAO_PAGAMENTO`

| valor              |      qtd |
|:-------------------|---------:|
|                    | 18882483 |
| 07MAR2025:04:06:31 |     2537 |
| 12MAR2025:04:06:33 |     2492 |
| 11MAR2025:05:27:34 |     2393 |
| 12MAR2025:04:06:32 |     2339 |
| 11MAR2025:05:27:36 |     2305 |
| 11MAR2025:05:27:33 |     2297 |
| 11MAR2025:05:27:37 |     2246 |
| 08MAR2025:05:30:28 |     2240 |
| 09JAN2025:04:46:10 |     2215 |

#### Coluna: `COD_LOGIN_PAGAMENTO`

|    valor |      qtd |
|---------:|---------:|
|          | 14539993 |
|    60001 |  7261693 |
|    41002 |    12658 |
| 93257890 |      311 |
| 92546509 |      291 |
| 92597591 |      238 |
| 92531759 |      217 |
| 94146436 |      206 |
| 92344014 |      183 |
| 93278081 |      166 |

#### Coluna: `COD_FORMA_PAGAMENTO`

| valor   |     qtd |
|:--------|--------:|
| CA      | 7251673 |
|         | 6118973 |
| PB      | 5865567 |
| DD      | 2327120 |
| PA      |  266295 |

#### Coluna: `VAL_ORIGINAL_PAGAMENTO`

|   valor |     qtd |
|--------:|--------:|
|         | 6118973 |
|   59.89 |  344023 |
|   34.8  |  336600 |
|   49.9  |  327761 |
|   54.9  |  319644 |
|   34.9  |  264601 |
|   29.8  |  248510 |
|   29.9  |  243820 |
|   54.8  |  208396 |
|   64.9  |  143522 |

#### Coluna: `NUM_FATURA_PAGAMENTO`

|        valor |     qtd |
|-------------:|--------:|
|              | 6845630 |
| 966132196123 |      24 |
| 966132196124 |      24 |
| 120004027064 |      22 |
| 966132196131 |      21 |
| 966132196132 |      21 |
| 966132196129 |      21 |
| 966132196127 |      21 |
| 966132196126 |      21 |
| 966132196128 |      21 |

#### Coluna: `COD_TIPO_PAGAMENTO`

| valor   |     qtd |
|:--------|--------:|
| O       | 7239233 |
|         | 6118973 |
| P       | 5769643 |
| D       | 2327120 |
| B       |  362219 |
| E       |   12440 |

#### Coluna: `DSC_NOME_BANCO_PAGAMENTO`

| valor    |     qtd |
|:---------|--------:|
| CPAY-PIX | 6192697 |
|          | 6118973 |
| NET1     | 2460975 |
| CEF      | 1730111 |
| ITAU     | 1116136 |
| BRADES   |  856068 |
| BANESPA  |  811601 |
| MULTI-PG |  708077 |
| BRASIL   |  598518 |
| GEVEN1P  |  189962 |

#### Coluna: `SEQ_ARQUIVO_PAGAMENTO`

|   valor |      qtd |
|--------:|---------:|
|         | 13775460 |
|    6340 |    61384 |
|    6285 |    51661 |
|    5298 |    41044 |
|    6156 |    36635 |
|    6296 |    34778 |
|    6328 |    31106 |
|    6852 |    30180 |
|    6211 |    28289 |
|    6274 |    27746 |

#### Coluna: `NUM_PARCELA_PAGAMENTO`

|   valor |      qtd |
|--------:|---------:|
|         | 21268211 |
|     458 |    10247 |
|     423 |     9539 |
|     463 |     7508 |
|     424 |     7253 |
|     457 |     6770 |
|     459 |     5903 |
|     464 |     5594 |
|     471 |     4898 |
|     394 |     4756 |

#### Coluna: `NUM_AGRUPADOR_PAGAMENTO`

|   valor |      qtd |
|--------:|---------:|
|         | 16102580 |
|       2 |     1797 |
|       1 |     1777 |
|       5 |     1624 |
|       4 |     1592 |
|       3 |     1554 |
|       6 |     1534 |
|       8 |     1481 |
|      11 |     1470 |
|       7 |     1451 |

#### Coluna: `DSC_PAGAMENTO`

| valor                                               |      qtd |
|:----------------------------------------------------|---------:|
|                                                     | 18848477 |
| Arquivo Rajada Sequencia: 21987, Registro: 00000067 |      143 |
| Arquivo Rajada Sequencia: 23862, Registro: 00000017 |      113 |
| Arquivo Rajada Sequencia: 24142, Registro: 00000031 |       96 |
| Arquivo Rajada Sequencia: 24395, Registro: 00000054 |       95 |
| Arquivo Rajada Sequencia: 11769, Registro: 00001397 |       93 |
| Arquivo Rajada Sequencia: 11769, Registro: 00001396 |       90 |
| Arquivo Rajada Sequencia: 11471, Registro: 00001477 |       89 |
| Arquivo Rajada Sequencia: 24762, Registro: 00000344 |       89 |
| Arquivo Rajada Sequencia: 24762, Registro: 00000437 |       88 |

#### Coluna: `VAL_ATUAL_PAGAMENTO`

|   valor |     qtd |
|--------:|--------:|
|         | 6118978 |
|   59.89 |  344023 |
|   34.8  |  336602 |
|   49.9  |  327761 |
|   54.9  |  319644 |
|   34.9  |  264599 |
|   29.8  |  248510 |
|   29.9  |  243827 |
|   54.8  |  208397 |
|   64.9  |  143522 |

#### Coluna: `COD_METODO_PAGAMENTO`

|   valor |      qtd |
|--------:|---------:|
|         | 16297184 |
|       1 |  1657841 |
|       3 |  1538749 |
|       5 |  1401465 |
|       4 |   647567 |
|       2 |   285169 |
|       6 |     1653 |

#### Coluna: `IND_STATUS_PAGAMENTO`

| valor   |     qtd |
|:--------|--------:|
| R       | 9478841 |
|         | 8996090 |
| C       | 2938458 |
| P       |  404814 |
| B       |   11425 |

#### Coluna: `DAT_STATUS_PAGAMENTO`

| valor              |     qtd |
|:-------------------|--------:|
|                    | 6118973 |
| 11MAR2025:00:00:00 |  274965 |
| 06MAR2025:00:00:00 |  204513 |
| 11FEB2025:00:00:00 |  180872 |
| 18MAR2025:00:00:00 |  151370 |
| 21MAR2025:00:00:00 |  146867 |
| 06FEB2025:00:00:00 |  144461 |
| 18FEB2025:00:00:00 |  134539 |
| 07MAR2025:00:00:00 |  134080 |
| 07JAN2025:00:00:00 |  131040 |

#### Coluna: `COD_ARQUIVO_PAGAMENTO`

| valor                |      qtd |
|:---------------------|---------:|
|                      | 18390641 |
| 6747200000000240924C |      148 |
| 1981200000000030624C |      142 |
| 4779200000000220824C |      128 |
| 2875200000000241024C |      127 |
| 5912200000000250624C |      122 |
| 6908200000000250724C |      122 |
| 1178200000000020524C |      117 |
| 4878200000000090125C |      111 |
| 8050091012345270125C |      109 |

#### Coluna: `COD_NETUNO_PAGAMENTO`

| valor   |      qtd |
|:--------|---------:|
|         | 21829628 |

#### Coluna: `DAT_CRIACAO_CREDITO`

| valor              |     qtd |
|:-------------------|--------:|
|                    | 6118973 |
| 06MAR2025:14:36:18 |     247 |
| 06MAR2025:14:36:07 |     242 |
| 21FEB2025:12:47:38 |     241 |
| 21FEB2025:12:47:22 |     240 |
| 06MAR2025:14:36:43 |     237 |
| 06MAR2025:14:36:11 |     236 |
| 21FEB2025:12:47:16 |     234 |
| 06MAR2025:14:36:36 |     233 |
| 06MAR2025:14:36:31 |     232 |

#### Coluna: `DAT_ATUALIZACAO_CREDITO`

| valor   |      qtd |
|:--------|---------:|
|         | 21829628 |

#### Coluna: `COD_LOGIN_CREDITO`

|    valor |      qtd |
|---------:|---------:|
|          | 14223305 |
|    60001 |  7576501 |
|    41002 |    12029 |
|    41003 |     1445 |
| 93257890 |      311 |
| 92546509 |      291 |
| 92597591 |      238 |
| 92531759 |      217 |
| 94146436 |      206 |
| 92344014 |      183 |

#### Coluna: `VAL_PAGAMENTO_CREDITO`

|   valor |     qtd |
|--------:|--------:|
|         | 6118973 |
|   34.8  |  336319 |
|   54.9  |  322706 |
|   34.9  |  265861 |
|   29.8  |  248568 |
|   29.9  |  244589 |
|   49.9  |  212998 |
|   54.8  |  208202 |
|    3.12 |  164469 |
|   64.9  |  144258 |

#### Coluna: `IND_TIPO_CREDITO`

| valor   |      qtd |
|:--------|---------:|
| P       | 15710655 |
|         |  6118973 |

#### Coluna: `SEQ_PAGAMENTO_CREDITO`

|   valor |     qtd |
|--------:|--------:|
|         | 6118973 |
|       1 | 2154176 |
|       2 | 1504746 |
|       3 | 1079994 |
|       4 |  680829 |
|       5 |  384912 |
|       6 |  251832 |
|       7 |  229466 |
|       8 |  220894 |
|       9 |  215866 |

#### Coluna: `SEQ_FATURA_CREDITO`

|   valor |     qtd |
|--------:|--------:|
|         | 6118973 |
|       1 | 1784745 |
|       2 | 1077354 |
|       3 | 1028928 |
|       4 |  771562 |
|       5 |  483752 |
|       6 |  364357 |
|       7 |  283689 |
|       8 |  270977 |
|       9 |  214614 |

#### Coluna: `COD_ALOCACAO_CREDITO`

| valor   |      qtd |
|:--------|---------:|
| PYM     | 14949068 |
|         |  6118973 |
| CRT     |   695700 |
| CRTW    |    49132 |
| CRF     |     6601 |
| FNTT    |     5505 |
| BCK     |     4086 |
| RFN     |      532 |
| FNTF    |       31 |

#### Coluna: `COD_DESALOCACAO_CREDITO`

| valor   |      qtd |
|:--------|---------:|
|         | 21829628 |

#### Coluna: `SEQ_ENTIDADE_CREDITO`

|   valor |     qtd |
|--------:|--------:|
|         | 6118973 |
|       1 | 1812152 |
|       2 | 1284694 |
|       3 |  909899 |
|       4 |  678526 |
|       5 |  426893 |
|       6 |  328812 |
|       7 |  252187 |
|       8 |  232996 |
|       9 |  186425 |

#### Coluna: `COD_TIPO_FATURA`

| valor   |      qtd |
|:--------|---------:|
| B       | 12251645 |
|         |  6118973 |
| 21      |  2871259 |
| PA      |   284316 |
| P1      |    73627 |
| T2      |    70352 |
| 15      |    54042 |
| FE      |    34081 |
| 31      |    32123 |
| 41      |    25651 |

#### Coluna: `DAT_ATIVIDADE_CREDITO`

| valor              |     qtd |
|:-------------------|--------:|
|                    | 6118973 |
| 11MAR2025:00:00:00 |  237682 |
| 06MAR2025:00:00:00 |  208768 |
| 11FEB2025:00:00:00 |  167407 |
| 06FEB2025:00:00:00 |  143415 |
| 10MAR2025:00:00:00 |  143156 |
| 18MAR2025:00:00:00 |  142276 |
| 21MAR2025:00:00:00 |  137340 |
| 07MAR2025:00:00:00 |  133017 |
| 07JAN2025:00:00:00 |  128867 |

#### Coluna: `DAT_VENCIMENTO_CREDITO`

| valor              |     qtd |
|:-------------------|--------:|
|                    | 6118973 |
| 10MAR2025:00:00:00 |  638118 |
| 10FEB2025:00:00:00 |  631527 |
| 17FEB2025:00:00:00 |  394098 |
| 10JAN2025:00:00:00 |  386952 |
| 20FEB2025:00:00:00 |  372923 |
| 17MAR2025:00:00:00 |  368492 |
| 15JAN2025:00:00:00 |  355307 |
| 20JAN2025:00:00:00 |  326015 |
| 20MAR2025:00:00:00 |  319366 |



---

### 📏 Comprimento de Strings: `raw/pagamento`
#### Coluna: `NUM_CPF`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|        11 |        11 |        11 |

#### Coluna: `DAT_STATUS_FATURA`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|        18 |        18 |        18 |

#### Coluna: `CONTRATO`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|         8 |         9 |         9 |

#### Coluna: `SEQ_FATURA`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|         1 |      1.68 |         3 |

#### Coluna: `NUM_SUB_SEQ_FATURA`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|         1 |       1.8 |         4 |

#### Coluna: `NUM_CREDITO_SEQ`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|         1 |      1.68 |         3 |

#### Coluna: `DW_TIPO_FATURA`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|         2 |      2.23 |         3 |

#### Coluna: `IND_STATUS_FATURA`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|         1 |         1 |         1 |

#### Coluna: `DW_NUM_CLIENTE`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|         9 |      9.92 |        10 |

#### Coluna: `DW_AREA`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|         1 |         2 |         2 |

#### Coluna: `DW_UN_NEGOCIO`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|         1 |      1.05 |         2 |

#### Coluna: `DW_FORMA_PAGAMENTO`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|         2 |         2 |         2 |

#### Coluna: `VAL_PAGAMENTO_FATURA`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|         1 |      4.63 |        10 |

#### Coluna: `DAT_CRIACAO_DW`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|        18 |        18 |        18 |

#### Coluna: `DW_BANCO`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|         2 |       2.7 |         4 |

#### Coluna: `DW_TIPO_PAGAMENTO`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|         5 |         5 |         5 |

#### Coluna: `NUM_BANCO_PAGAMENTO`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|         2 |      2.57 |         4 |

#### Coluna: `NUM_AGENCIA_PAGAMENTO`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|         1 |      2.91 |         4 |

#### Coluna: `NUM_CC_PAGAMENTO`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|         2 |      3.36 |        14 |

#### Coluna: `DW_MOTIVO_ESTORNO`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|         2 |         2 |         2 |

#### Coluna: `VAL_DESCONTO_ITEM`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|         1 |         1 |         1 |

#### Coluna: `VAL_PAGAMENTO_ITEM`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|         1 |      4.63 |        10 |

#### Coluna: `VAL_JUROS_MULTAS_ITEM`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|         1 |      2.07 |         9 |

#### Coluna: `VAL_MULTA_EQUIP_ITEM`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|         1 |      1.01 |         8 |

#### Coluna: `VAL_MULTA_EQUIP_TOTAL`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|         1 |      1.01 |         8 |

#### Coluna: `VAL_MULTA_FID_ITEM`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|         1 |         1 |         1 |

#### Coluna: `COD_ORIGEM_NETUNO`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|        15 |        15 |        15 |

#### Coluna: `COD_CONTA_ATIVIDADE`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|         9 |         9 |         9 |

#### Coluna: `SEQ_ENTIDADE_ATIVIDADE`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|         1 |      1.61 |         3 |

#### Coluna: `DAT_CRIACAO_ATIVIDADE`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|        18 |        18 |        18 |

#### Coluna: `DAT_ATUALIZACAO_ATIVIDADE`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|        18 |        18 |        18 |

#### Coluna: `COD_LOGIN_OPERADOR_ATIVIDADE`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|         5 |      5.01 |         8 |

#### Coluna: `COD_ATIVIDADE`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|         3 |         3 |         4 |

#### Coluna: `COD_RAZAO_ATIVIDADE`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|         2 |         2 |         6 |

#### Coluna: `DAT_BAIXA_ATIVIDADE`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|        18 |        18 |        18 |

#### Coluna: `VAL_BAIXA_ATIVIDADE`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|         1 |      4.91 |        10 |

#### Coluna: `DAT_DEPOSITO_ATIVIDADE`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|        18 |        18 |        18 |

#### Coluna: `COD_FUNDO_ATIVIDADE`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|         9 |         9 |         9 |

#### Coluna: `COD_BANCO_ATIVIDADE`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|         3 |      3.07 |         4 |

#### Coluna: `NUM_CONTA_ATIVIDADE`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|         2 |     10.67 |        14 |

#### Coluna: `COD_AGENCIA_ATIVIDADE`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|         1 |         4 |         4 |

#### Coluna: `SEQ_ENTIDADE_PAGAMENTO`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|         1 |      1.61 |         3 |

#### Coluna: `DAT_CRIACAO_PAGAMENTO`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|        18 |        18 |        18 |

#### Coluna: `DAT_ATUALIZACAO_PAGAMENTO`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|        18 |        18 |        18 |

#### Coluna: `COD_LOGIN_PAGAMENTO`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|         5 |      5.01 |         8 |

#### Coluna: `COD_FORMA_PAGAMENTO`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|         2 |         2 |         2 |

#### Coluna: `VAL_ORIGINAL_PAGAMENTO`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|         1 |      4.91 |        10 |

#### Coluna: `NUM_FATURA_PAGAMENTO`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|        12 |        12 |        12 |

#### Coluna: `COD_TIPO_PAGAMENTO`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|         1 |         1 |         1 |

#### Coluna: `DSC_NOME_BANCO_PAGAMENTO`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|         3 |       6.2 |         8 |

#### Coluna: `SEQ_ARQUIVO_PAGAMENTO`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|         2 |      3.96 |         5 |

#### Coluna: `NUM_PARCELA_PAGAMENTO`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|         2 |      3.11 |         4 |

#### Coluna: `NUM_AGRUPADOR_PAGAMENTO`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|         1 |      4.65 |         7 |

#### Coluna: `DSC_PAGAMENTO`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|        49 |        51 |        51 |

#### Coluna: `VAL_ATUAL_PAGAMENTO`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|         1 |      4.91 |        10 |

#### Coluna: `COD_METODO_PAGAMENTO`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|         1 |         1 |         1 |

#### Coluna: `IND_STATUS_PAGAMENTO`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|         1 |         1 |         1 |

#### Coluna: `DAT_STATUS_PAGAMENTO`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|        18 |        18 |        18 |

#### Coluna: `COD_ARQUIVO_PAGAMENTO`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|         1 |     12.66 |        23 |

#### Coluna: `COD_NETUNO_PAGAMENTO`
| min_len   | avg_len   | max_len   |
|:----------|:----------|:----------|
| NULL      | NULL      | NULL      |

#### Coluna: `DAT_CRIACAO_CREDITO`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|        18 |        18 |        18 |

#### Coluna: `DAT_ATUALIZACAO_CREDITO`
| min_len   | avg_len   | max_len   |
|:----------|:----------|:----------|
| NULL      | NULL      | NULL      |

#### Coluna: `COD_LOGIN_CREDITO`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|         5 |      5.01 |         8 |

#### Coluna: `VAL_PAGAMENTO_CREDITO`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|         1 |       4.6 |        10 |

#### Coluna: `IND_TIPO_CREDITO`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|         1 |         1 |         1 |

#### Coluna: `SEQ_PAGAMENTO_CREDITO`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|         1 |      1.61 |         3 |

#### Coluna: `SEQ_FATURA_CREDITO`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|         1 |      1.72 |         4 |

#### Coluna: `COD_ALOCACAO_CREDITO`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|         3 |         3 |         4 |

#### Coluna: `COD_DESALOCACAO_CREDITO`
| min_len   | avg_len   | max_len   |
|:----------|:----------|:----------|
| NULL      | NULL      | NULL      |

#### Coluna: `SEQ_ENTIDADE_CREDITO`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|         1 |      1.77 |         6 |

#### Coluna: `COD_TIPO_FATURA`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|         1 |      1.22 |         2 |

#### Coluna: `DAT_ATIVIDADE_CREDITO`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|        18 |        18 |        18 |

#### Coluna: `DAT_VENCIMENTO_CREDITO`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|        18 |        18 |        18 |



---

