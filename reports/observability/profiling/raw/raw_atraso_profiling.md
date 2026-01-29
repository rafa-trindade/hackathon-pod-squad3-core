# Relatório de Profiling: `raw/atraso`

### 📦 Volumetria: `raw/atraso`
|   qtd_arquivos | registros   |   colunas |   tamanho_comprimido_mib |   tamanho_descomprimido_mib |
|---------------:|:------------|----------:|-------------------------:|----------------------------:|
|             10 | 31.611.316  |        50 |                  4307.73 |                      6358.9 |

---

### 🧬 Schema: `raw/atraso`
| column_name                  | column_type   | null   | key   | default   | extra   |
|:-----------------------------|:--------------|:-------|:------|:----------|:--------|
| NUM_CPF                      | VARCHAR       | YES    |       |           |         |
| DAT_REFERENCIA               | VARCHAR       | YES    |       |           |         |
| NUM_FATURA_HASH              | VARCHAR       | YES    |       |           |         |
| NUM_ENT_SEQ_FATURA           | VARCHAR       | YES    |       |           |         |
| CONTRATO                     | VARCHAR       | YES    |       |           |         |
| DW_UN_NEGOCIO                | VARCHAR       | YES    |       |           |         |
| DW_HIS_PONTO_VENDA_COMTA     | VARCHAR       | YES    |       |           |         |
| DW_NUM_CLIENTE               | VARCHAR       | YES    |       |           |         |
| DW_AREA                      | VARCHAR       | YES    |       |           |         |
| DW_CICLO                     | VARCHAR       | YES    |       |           |         |
| DW_TIPO_CLIENTE_CONTA        | VARCHAR       | YES    |       |           |         |
| DW_OFERTA                    | VARCHAR       | YES    |       |           |         |
| DW_FAIXA_AGING_FATURA        | VARCHAR       | YES    |       |           |         |
| DW_FAIXA_AGING_DIVIDA        | VARCHAR       | YES    |       |           |         |
| DW_FAIXA_TEMPO_BASE          | VARCHAR       | YES    |       |           |         |
| DW_FAIXA_AGING_PROX_FECH     | VARCHAR       | YES    |       |           |         |
| DW_TIPO_FATURAMENTO          | VARCHAR       | YES    |       |           |         |
| COD_PLATAFORMA               | VARCHAR       | YES    |       |           |         |
| DAT_CRIACAO_REGISTRO_TRANS   | VARCHAR       | YES    |       |           |         |
| DAT_ALTERACAO_REGISTRO_TRANS | VARCHAR       | YES    |       |           |         |
| DAT_CANCELAMENTO_FAT         | VARCHAR       | YES    |       |           |         |
| DAT_ORIGINAL_VCTO_FAT        | VARCHAR       | YES    |       |           |         |
| DAT_ALTERACAO_VCTO_FAT       | VARCHAR       | YES    |       |           |         |
| DAT_CRIACAO_FAT              | VARCHAR       | YES    |       |           |         |
| DAT_VENCIMENTO_FAT           | VARCHAR       | YES    |       |           |         |
| DAT_STATUS_FAT               | VARCHAR       | YES    |       |           |         |
| DAT_MIN_VENCIMENTO_FAT       | VARCHAR       | YES    |       |           |         |
| NUM_BILL_SEQ_FAT             | VARCHAR       | YES    |       |           |         |
| NUM_SEQ_ACORDO_FAT           | VARCHAR       | YES    |       |           |         |
| IND_ISENCAO_COB_FAT          | VARCHAR       | YES    |       |           |         |
| IND_WO                       | VARCHAR       | YES    |       |           |         |
| IND_PDD                      | VARCHAR       | YES    |       |           |         |
| IND_PCCR                     | VARCHAR       | YES    |       |           |         |
| IND_ACA                      | VARCHAR       | YES    |       |           |         |
| IND_PRIMEIRA_FAT             | VARCHAR       | YES    |       |           |         |
| IND_FRAUDE                   | VARCHAR       | YES    |       |           |         |
| VAL_FAT_LIQUIDO              | VARCHAR       | YES    |       |           |         |
| VAL_FAT_BRUTO                | VARCHAR       | YES    |       |           |         |
| VAL_FAT_CREDITO              | VARCHAR       | YES    |       |           |         |
| VAL_FAT_AJUSTE               | VARCHAR       | YES    |       |           |         |
| VAL_FAT_BRUTO_BC             | VARCHAR       | YES    |       |           |         |
| VAL_FAT_PAGAMENTO_BRUTO      | VARCHAR       | YES    |       |           |         |
| VAL_FAT_ABERTO               | VARCHAR       | YES    |       |           |         |
| VAL_FAT_ABERTO_LIQ           | VARCHAR       | YES    |       |           |         |
| VAL_MULTA_JUROS              | VARCHAR       | YES    |       |           |         |
| VAL_MULTA_CANCELAMENTO       | VARCHAR       | YES    |       |           |         |
| VAL_PARC_APARELHO_LIQ        | VARCHAR       | YES    |       |           |         |
| VAL_FAT_LIQ_JM_MC            | VARCHAR       | YES    |       |           |         |
| DAT_ATIVACAO_CONTA_CLI       | VARCHAR       | YES    |       |           |         |
| DAT_CRIACAO_DW               | VARCHAR       | YES    |       |           |         |

---

### 📅 Campos de Data: `raw/atraso`
#### ✅ Datas com tipagem (DATE / TIMESTAMP)
> ⚠️ Nenhuma coluna DATE ou TIMESTAMP encontrada.

#### ⚠️ Possíveis campos de data/hora sem tipagem (inferido pelo nome)

- `DAT_ALTERACAO_REGISTRO_TRANS`
- `DAT_ALTERACAO_VCTO_FAT`
- `DAT_ATIVACAO_CONTA_CLI`
- `DAT_CANCELAMENTO_FAT`
- `DAT_CRIACAO_DW`
- `DAT_CRIACAO_FAT`
- `DAT_CRIACAO_REGISTRO_TRANS`
- `DAT_MIN_VENCIMENTO_FAT`
- `DAT_ORIGINAL_VCTO_FAT`
- `DAT_REFERENCIA`
- `DAT_STATUS_FAT`
- `DAT_VENCIMENTO_FAT`


---

### 📊 Estatísticas por Coluna: `raw/atraso`
| coluna                       |   distintos |    nulos |   duplicados | pct_nulos   | pct_duplicados   | cardinalidade   |
|:-----------------------------|------------:|---------:|-------------:|:------------|:-----------------|:----------------|
| NUM_CPF                      |     2095944 |        0 |     29515372 | 0.0%        | 93.37%           | ALTA            |
| DAT_REFERENCIA               |          18 |        0 |     31611298 | 0.0%        | 100.0%           | BAIXA           |
| NUM_FATURA_HASH              |    15633144 |        0 |     15978172 | 0.0%        | 50.55%           | ALTA            |
| NUM_ENT_SEQ_FATURA           |        1183 |        0 |     31610133 | 0.0%        | 100.0%           | BAIXA           |
| CONTRATO                     |     2961912 |        0 |     28649404 | 0.0%        | 90.63%           | ALTA            |
| DW_UN_NEGOCIO                |          10 |        0 |     31611306 | 0.0%        | 100.0%           | BAIXA           |
| DW_HIS_PONTO_VENDA_COMTA     |       76810 |        0 |     31534506 | 0.0%        | 99.76%           | MEDIA           |
| DW_NUM_CLIENTE               |     3084554 |        0 |     28526762 | 0.0%        | 90.24%           | ALTA            |
| DW_AREA                      |          69 |        0 |     31611247 | 0.0%        | 100.0%           | BAIXA           |
| DW_CICLO                     |          47 |        0 |     31611269 | 0.0%        | 100.0%           | BAIXA           |
| DW_TIPO_CLIENTE_CONTA        |          35 |        0 |     31611281 | 0.0%        | 100.0%           | BAIXA           |
| DW_OFERTA                    |        1144 |        0 |     31610172 | 0.0%        | 100.0%           | BAIXA           |
| DW_FAIXA_AGING_FATURA        |          24 |        0 |     31611292 | 0.0%        | 100.0%           | BAIXA           |
| DW_FAIXA_AGING_DIVIDA        |          16 |        0 |     31611300 | 0.0%        | 100.0%           | BAIXA           |
| DW_FAIXA_TEMPO_BASE          |           7 |        0 |     31611309 | 0.0%        | 100.0%           | BAIXA           |
| DW_FAIXA_AGING_PROX_FECH     |          17 |        0 |     31611299 | 0.0%        | 100.0%           | BAIXA           |
| DW_TIPO_FATURAMENTO          |          27 |        0 |     31611289 | 0.0%        | 100.0%           | BAIXA           |
| COD_PLATAFORMA               |          14 |        0 |     31611302 | 0.0%        | 100.0%           | BAIXA           |
| DAT_CRIACAO_REGISTRO_TRANS   |     3133554 |        0 |     28477762 | 0.0%        | 90.09%           | ALTA            |
| DAT_ALTERACAO_REGISTRO_TRANS |     3407394 |      214 |     28203922 | 0.0%        | 89.22%           | ALTA            |
| DAT_CANCELAMENTO_FAT         |           0 | 31611316 |     31611316 | 100.0%      | 100.0%           | BAIXA           |
| DAT_ORIGINAL_VCTO_FAT        |        2317 |  1121787 |     31608999 | 3.55%       | 99.99%           | BAIXA           |
| DAT_ALTERACAO_VCTO_FAT       |         760 | 31523457 |     31610556 | 99.72%      | 100.0%           | BAIXA           |
| DAT_CRIACAO_FAT              |        2546 |        0 |     31608770 | 0.0%        | 99.99%           | BAIXA           |
| DAT_VENCIMENTO_FAT           |        2301 |        0 |     31609015 | 0.0%        | 99.99%           | BAIXA           |
| DAT_STATUS_FAT               |        2823 |  1075903 |     31608493 | 3.4%        | 99.99%           | BAIXA           |
| DAT_MIN_VENCIMENTO_FAT       |        1853 |        0 |     31609463 | 0.0%        | 99.99%           | BAIXA           |
| NUM_BILL_SEQ_FAT             |         256 |        0 |     31611060 | 0.0%        | 100.0%           | BAIXA           |
| NUM_SEQ_ACORDO_FAT           |          71 |        0 |     31611245 | 0.0%        | 100.0%           | BAIXA           |
| IND_ISENCAO_COB_FAT          |           4 |        0 |     31611312 | 0.0%        | 100.0%           | BAIXA           |
| IND_WO                       |           3 |        0 |     31611313 | 0.0%        | 100.0%           | BAIXA           |
| IND_PDD                      |           3 |        0 |     31611313 | 0.0%        | 100.0%           | BAIXA           |
| IND_PCCR                     |           4 |        0 |     31611312 | 0.0%        | 100.0%           | BAIXA           |
| IND_ACA                      |           3 |        0 |     31611313 | 0.0%        | 100.0%           | BAIXA           |
| IND_PRIMEIRA_FAT             |           2 |        0 |     31611314 | 0.0%        | 100.0%           | BAIXA           |
| IND_FRAUDE                   |           2 |        0 |     31611314 | 0.0%        | 100.0%           | BAIXA           |
| VAL_FAT_LIQUIDO              |       69378 |        0 |     31541938 | 0.0%        | 99.78%           | MEDIA           |
| VAL_FAT_BRUTO                |       78592 |        0 |     31532724 | 0.0%        | 99.75%           | MEDIA           |
| VAL_FAT_CREDITO              |       26236 |        0 |     31585080 | 0.0%        | 99.92%           | BAIXA           |
| VAL_FAT_AJUSTE               |        8581 |        0 |     31602735 | 0.0%        | 99.97%           | BAIXA           |
| VAL_FAT_BRUTO_BC             |       68671 |        0 |     31542645 | 0.0%        | 99.78%           | MEDIA           |
| VAL_FAT_PAGAMENTO_BRUTO      |       20777 |        0 |     31590539 | 0.0%        | 99.93%           | BAIXA           |
| VAL_FAT_ABERTO               |       70108 |        0 |     31541208 | 0.0%        | 99.78%           | MEDIA           |
| VAL_FAT_ABERTO_LIQ           |       69158 |        0 |     31542158 | 0.0%        | 99.78%           | MEDIA           |
| VAL_MULTA_JUROS              |        5403 |        0 |     31605913 | 0.0%        | 99.98%           | BAIXA           |
| VAL_MULTA_CANCELAMENTO       |       10668 |        0 |     31600648 | 0.0%        | 99.97%           | BAIXA           |
| VAL_PARC_APARELHO_LIQ        |         553 |        0 |     31610763 | 0.0%        | 100.0%           | BAIXA           |
| VAL_FAT_LIQ_JM_MC            |       66040 |        0 |     31545276 | 0.0%        | 99.79%           | MEDIA           |
| DAT_ATIVACAO_CONTA_CLI       |        7487 |        0 |     31603829 | 0.0%        | 99.98%           | BAIXA           |
| DAT_CRIACAO_DW               |      199410 |        0 |     31411906 | 0.0%        | 99.37%           | MEDIA           |

---

### 🔟 Distribuição de Valores (Top 10): `raw/atraso`
#### Coluna: `NUM_CPF`

| valor       |   qtd |
|:------------|------:|
| ZN98N87WNXX |  3584 |
| ZYTYXT8YXZ7 |  2952 |
| NY88TWWYW87 |  1970 |
| UNWTTZN88NU |  1890 |
| X7TYTTZW8YN |  1881 |
| X9U8NWN78N8 |  1844 |
| ZTNTN9UYTXX |  1418 |
| 9TZUTUT7TZZ |  1350 |
| Y8U7XYTU8T9 |  1233 |
| UWW97YYZ9ZU |  1103 |

#### Coluna: `DAT_REFERENCIA`

| valor              |     qtd |
|:-------------------|--------:|
| 01MAR2025:00:00:00 | 4394665 |
| 01FEB2025:00:00:00 | 3643289 |
| 01JAN2025:00:00:00 | 3018681 |
| 01DEC2024:00:00:00 | 2444916 |
| 01NOV2024:00:00:00 | 1883050 |
| 01OCT2024:00:00:00 | 1683363 |
| 01SEP2024:00:00:00 | 1510312 |
| 01AUG2024:00:00:00 | 1397247 |
| 01JUL2024:00:00:00 | 1318087 |
| 01DEC2023:00:00:00 | 1252111 |

#### Coluna: `NUM_FATURA_HASH`

| valor                                                            |     qtd |
|:-----------------------------------------------------------------|--------:|
| 5feceb66ffc86f38d952786c6d696c79c2dbc239dd4e91b46729d73a27fb57e9 | 1075903 |
| d62379c48ce480322c400adcbb1f59cf4196d4c627a6fae49c3ea53eeb2c7e6d |     126 |
| 0800dd401791559678cb955935325732500b31d51fed5f9af7af2b1c0a6075d3 |     108 |
| 2286794687ca5566d774c712d44c8672394f8ced25815023b1a5d37d9e7f56d6 |     108 |
| 065685ab18a3a1df24dfd9b22e165fdc8aaf8ff9b5308d2d90cf8d5c21dafb4b |     108 |
| 5e554a259c4ab7e7278f111ffd3cb1f4c650f5302aa6098883804eb7ae847f1a |     108 |
| b8b2bf7948343f22cd785bb1e707b7a696d8ecd5eee4d9c15a0671fbe80ae1ac |     108 |
| 1167a8f04367c7ce16c0b2196587507231add8b93ff8f0c03d1722f0c9e890f0 |     108 |
| e02f06436e1219eabeea7781d190542ed9b349c62ca3d00f04a33993dcf1fd7a |     108 |
| 029ea7d470f8de06cea55c9033d4f3966d10739aec333dd5cc88edfa9992b7de |     108 |

#### Coluna: `NUM_ENT_SEQ_FATURA`

|   valor |     qtd |
|--------:|--------:|
|       1 | 3622614 |
|       3 | 1798730 |
|       2 | 1744786 |
|       4 | 1430372 |
|       5 | 1001250 |
|       6 |  866619 |
|       7 |  694051 |
|       8 |  650143 |
|       9 |  541344 |
|      10 |  507448 |

#### Coluna: `CONTRATO`

|     valor |   qtd |
|----------:|------:|
| 832370173 |  3582 |
| 843837549 |  2952 |
| 827450936 |  1969 |
| 832040386 |  1890 |
| 822974440 |  1881 |
| 833912847 |  1837 |
| 846007545 |  1350 |
| 882711546 |  1233 |
| 851965102 |  1098 |
| 842432062 |  1098 |

#### Coluna: `DW_UN_NEGOCIO`

|   valor |     qtd |
|--------:|--------:|
|       5 | 5674372 |
|       1 | 4948185 |
|       3 | 4768595 |
|       4 | 4646757 |
|       6 | 2811457 |
|       2 | 2042652 |
|       9 | 1802755 |
|      10 | 1726876 |
|       8 | 1595073 |
|       7 | 1594594 |

#### Coluna: `DW_HIS_PONTO_VENDA_COMTA`

|    valor |     qtd |
|---------:|--------:|
|  9863292 | 1762903 |
|       -2 | 1349111 |
| 10428694 |  997120 |
|  9479205 |  996170 |
|  9980298 |  421378 |
|  1890100 |  364336 |
|   805397 |  359233 |
|       -3 |  345439 |
|  9987244 |  318925 |
| 10064668 |  310864 |

#### Coluna: `DW_NUM_CLIENTE`

|      valor |   qtd |
|-----------:|------:|
|  852163736 |  3582 |
|  937160046 |  2952 |
|  814166959 |  1969 |
|  699626807 |  1881 |
| 1207341177 |  1837 |
|  524092608 |  1422 |
| 1439218861 |  1365 |
|  947775947 |  1350 |
| 1170659040 |  1233 |
| 1146709793 |  1098 |

#### Coluna: `DW_AREA`

|   valor |     qtd |
|--------:|--------:|
|      36 | 4955241 |
|      -3 | 3544643 |
|       1 | 3524438 |
|      22 | 1219844 |
|      23 | 1091959 |
|      52 |  993495 |
|       7 |  922672 |
|       6 |  917979 |
|      19 |  844227 |
|      27 |  768378 |

#### Coluna: `DW_CICLO`

|   valor |     qtd |
|--------:|--------:|
|      29 | 1967108 |
|      61 | 1547850 |
|     101 | 1404525 |
|      65 | 1389746 |
|      74 | 1339012 |
|      77 | 1281125 |
|      28 | 1217233 |
|      25 | 1175556 |
|      66 | 1147670 |
|      75 | 1123173 |

#### Coluna: `DW_TIPO_CLIENTE_CONTA`

|   valor |      qtd |
|--------:|---------:|
|       6 | 21020227 |
|      52 |  4346840 |
|     367 |  2310244 |
|     792 |  1254105 |
|     293 |   802000 |
|     532 |   624647 |
|      -1 |   496599 |
|      31 |   329250 |
|     309 |   238014 |
|     822 |    67034 |

#### Coluna: `DW_OFERTA`

|   valor |     qtd |
|--------:|--------:|
|      -3 | 2252102 |
|      -2 | 1484945 |
|  160585 | 1479823 |
|  155057 | 1466190 |
|  159099 | 1316984 |
|  154953 | 1296950 |
|  159051 | 1274537 |
|  160733 | 1240211 |
|  159079 | 1183876 |
|  154968 | 1075260 |

#### Coluna: `DW_FAIXA_AGING_FATURA`

|   valor |      qtd |
|--------:|---------:|
|     277 | 17693100 |
|     278 |  6476688 |
|     279 |  2037163 |
|     280 |  1293182 |
|     281 |   849732 |
|     282 |   595868 |
|     283 |   436294 |
|     290 |   364942 |
|     292 |   325566 |
|     284 |   286518 |

#### Coluna: `DW_FAIXA_AGING_DIVIDA`

|   valor |      qtd |
|--------:|---------:|
|     261 | 15112702 |
|     262 |  7342787 |
|     263 |  2345438 |
|     264 |  1564580 |
|     265 |  1093425 |
|     266 |   833388 |
|     267 |   659050 |
|     274 |   520264 |
|     268 |   483738 |
|     269 |   375720 |

#### Coluna: `DW_FAIXA_TEMPO_BASE`

|   valor |      qtd |
|--------:|---------:|
|     356 | 12547987 |
|     352 |  5349573 |
|     355 |  5118869 |
|     354 |  4077334 |
|     353 |  4017582 |
|      -1 |   496599 |
|      -3 |     3372 |

#### Coluna: `DW_FAIXA_AGING_PROX_FECH`

|   valor |      qtd |
|--------:|---------:|
|     303 | 14018379 |
|     304 |  6681653 |
|     305 |  2291153 |
|     306 |  1504443 |
|     302 |  1457585 |
|     307 |  1060024 |
|     308 |   833517 |
|     309 |   628549 |
|     315 |   570893 |
|      -1 |   496599 |

#### Coluna: `DW_TIPO_FATURAMENTO`

|   valor |      qtd |
|--------:|---------:|
|   32529 | 24596826 |
|   32541 |  5723595 |
|   33523 |   519147 |
|   32534 |   252803 |
|   33541 |   117374 |
|   32542 |   109262 |
|   32548 |    85179 |
|   32543 |    67247 |
|   32556 |    55726 |
|   32569 |    38498 |

#### Coluna: `COD_PLATAFORMA`

| valor   |      qtd |
|:--------|---------:|
| AUTOC   | 17230902 |
| POSPG   | 10963007 |
| -2      |  2271850 |
| PREPG   |   748188 |
| POSBL   |   240839 |
| FLEXD   |    63540 |
| -3      |    46901 |
| CTLFC   |    42179 |
| POSTL   |     2470 |
| M2MS    |      930 |

#### Coluna: `DAT_CRIACAO_REGISTRO_TRANS`

| valor              |    qtd |
|:-------------------|-------:|
| 28SEP2023:00:00:00 | 102890 |
| 26NOV2023:00:00:00 |  95302 |
| 26SEP2023:00:00:00 |  94988 |
| 25OCT2023:00:00:00 |  94887 |
| 25NOV2023:00:00:00 |  91472 |
| 29SEP2023:00:00:00 |  88330 |
| 23NOV2023:00:00:00 |  83161 |
| 26OCT2023:00:00:00 |  83049 |
| 27OCT2023:00:00:00 |  79861 |
| 10NOV2023:00:00:00 |  77142 |

#### Coluna: `DAT_ALTERACAO_REGISTRO_TRANS`

| valor              |   qtd |
|:-------------------|------:|
| 28NOV2023:00:00:00 | 90100 |
| 10NOV2023:00:00:00 | 81464 |
| 25OCT2023:00:00:00 | 78276 |
| 26NOV2023:00:00:00 | 76114 |
| 23NOV2023:00:00:00 | 75654 |
| 25NOV2023:00:00:00 | 75279 |
| 22DEC2023:00:00:00 | 74914 |
| 22NOV2023:00:00:00 | 71565 |
| 09DEC2023:00:00:00 | 70050 |
| 26OCT2023:00:00:00 | 68987 |

#### Coluna: `DAT_CANCELAMENTO_FAT`

| valor   |      qtd |
|:--------|---------:|
|         | 31611316 |

#### Coluna: `DAT_ORIGINAL_VCTO_FAT`

| valor              |     qtd |
|:-------------------|--------:|
|                    | 1121787 |
| 15JAN2025:00:00:00 |  644505 |
| 10FEB2025:00:00:00 |  639876 |
| 15FEB2025:00:00:00 |  633685 |
| 10JAN2025:00:00:00 |  619734 |
| 10MAR2025:00:00:00 |  604634 |
| 15DEC2024:00:00:00 |  604212 |
| 15MAR2025:00:00:00 |  552868 |
| 10DEC2024:00:00:00 |  537212 |
| 15NOV2024:00:00:00 |  515760 |

#### Coluna: `DAT_ALTERACAO_VCTO_FAT`

| valor              |      qtd |
|:-------------------|---------:|
|                    | 31523457 |
| 14NOV2024:00:00:00 |    21087 |
| 22NOV2023:00:00:00 |     2520 |
| 12AUG2024:00:00:00 |     1666 |
| 10NOV2023:00:00:00 |     1238 |
| 12DEC2023:00:00:00 |     1137 |
| 27NOV2023:00:00:00 |      850 |
| 11OCT2023:00:00:00 |      840 |
| 13MAY2024:00:00:00 |      816 |
| 27AUG2018:00:00:00 |      810 |

#### Coluna: `DAT_CRIACAO_FAT`

| valor              |    qtd |
|:-------------------|-------:|
| 27FEB2025:00:00:00 | 535664 |
| 26NOV2024:00:00:00 | 430478 |
| 28JAN2025:00:00:00 | 430282 |
| 25DEC2024:00:00:00 | 428644 |
| 27DEC2024:00:00:00 | 398355 |
| 26FEB2025:00:00:00 | 390841 |
| 25JAN2025:00:00:00 | 383974 |
| 27NOV2024:00:00:00 | 339436 |
| 28DEC2024:00:00:00 | 316845 |
| 26OCT2024:00:00:00 | 315338 |

#### Coluna: `DAT_VENCIMENTO_FAT`

| valor              |    qtd |
|:-------------------|-------:|
| 10FEB2025:00:00:00 | 926196 |
| 10MAR2025:00:00:00 | 848971 |
| 15JAN2025:00:00:00 | 647428 |
| 17FEB2025:00:00:00 | 644302 |
| 10JAN2025:00:00:00 | 622295 |
| 16DEC2024:00:00:00 | 608559 |
| 17MAR2025:00:00:00 | 554254 |
| 10DEC2024:00:00:00 | 539820 |
| 18NOV2024:00:00:00 | 517653 |
| 12AUG2024:00:00:00 | 496002 |

#### Coluna: `DAT_STATUS_FAT`

| valor              |     qtd |
|:-------------------|--------:|
|                    | 1075903 |
| 27FEB2025:00:00:00 |  535067 |
| 28JAN2025:00:00:00 |  433158 |
| 25DEC2024:00:00:00 |  426693 |
| 26NOV2024:00:00:00 |  426590 |
| 27DEC2024:00:00:00 |  402503 |
| 26FEB2025:00:00:00 |  390467 |
| 25JAN2025:00:00:00 |  383531 |
| 27NOV2024:00:00:00 |  337232 |
| 28SEP2024:00:00:00 |  332855 |

#### Coluna: `DAT_MIN_VENCIMENTO_FAT`

| valor              |    qtd |
|:-------------------|-------:|
| 10FEB2025:00:00:00 | 877698 |
| 10MAR2025:00:00:00 | 710293 |
| 15JAN2025:00:00:00 | 621238 |
| 10JAN2025:00:00:00 | 610760 |
| 17FEB2025:00:00:00 | 596412 |
| 16DEC2024:00:00:00 | 579042 |
| 10DEC2024:00:00:00 | 520409 |
| 10JUN2024:00:00:00 | 509469 |
| 12AUG2024:00:00:00 | 506237 |
| 18NOV2024:00:00:00 | 484517 |

#### Coluna: `NUM_BILL_SEQ_FAT`

|   valor |     qtd |
|--------:|--------:|
|       1 | 4082744 |
|       2 | 2282121 |
|       3 | 2111113 |
|       4 | 1404737 |
|       5 |  956813 |
|       6 |  762806 |
|       7 |  704599 |
|       8 |  635146 |
|       9 |  590163 |
|      10 |  562407 |

#### Coluna: `NUM_SEQ_ACORDO_FAT`

|   valor |      qtd |
|--------:|---------:|
|      -2 | 27362822 |
|      -3 |  3572475 |
|       1 |   192679 |
|       2 |   113230 |
|       3 |    75216 |
|       4 |    53651 |
|       5 |    40730 |
|       6 |    32699 |
|       7 |    26156 |
|       8 |    22270 |

#### Coluna: `IND_ISENCAO_COB_FAT`

| valor   |      qtd |
|:--------|---------:|
| -2      | 28026258 |
| N       |  3580722 |
| Y       |     3442 |
| S       |      894 |

#### Coluna: `IND_WO`

| valor   |      qtd |
|:--------|---------:|
| R       | 29460247 |
| W       |  1654470 |
| -1      |   496599 |

#### Coluna: `IND_PDD`

| valor   |      qtd |
|:--------|---------:|
| N       | 28352241 |
| S       |  2762476 |
| -1      |   496599 |

#### Coluna: `IND_PCCR`

| valor   |      qtd |
|:--------|---------:|
| C       | 30233363 |
| W       |   880334 |
| -1      |   496599 |
| A       |     1020 |

#### Coluna: `IND_ACA`

| valor   |      qtd |
|:--------|---------:|
| N       | 31526541 |
| S       |    84612 |
| A       |      163 |

#### Coluna: `IND_PRIMEIRA_FAT`

| valor   |      qtd |
|:--------|---------:|
| N       | 27528572 |
| S       |  4082744 |

#### Coluna: `IND_FRAUDE`

| valor   |      qtd |
|:--------|---------:|
| N       | 31554040 |
| S       |    57276 |

#### Coluna: `VAL_FAT_LIQUIDO`

|   valor |    qtd |
|--------:|-------:|
|   34.8  | 664222 |
|    0    | 467711 |
|   54.9  | 440074 |
|   54.8  | 430210 |
|   29.8  | 374464 |
|   29.9  | 321551 |
|   34.9  | 276177 |
|   49.9  | 275673 |
|   49.8  | 251736 |
|    3.12 | 217100 |

#### Coluna: `VAL_FAT_BRUTO`

|   valor |    qtd |
|--------:|-------:|
|   54.9  | 376812 |
|   64.9  | 216671 |
|   34.9  | 161696 |
|   29.9  | 140989 |
|    5.59 | 126943 |
|    6.25 |  95534 |
|   54.22 |  85325 |
|   64.23 |  81540 |
|  105.86 |  74643 |
|    5.91 |  74342 |

#### Coluna: `VAL_FAT_CREDITO`

|   valor |      qtd |
|--------:|---------:|
|    0    | 11433827 |
|    4.32 |   253948 |
|    4.31 |   215136 |
|    4.34 |   196933 |
|    4.28 |   145584 |
|   12.92 |   139498 |
|    2.47 |   138570 |
|    8.66 |   134456 |
|    4.35 |   130058 |
|   49.09 |   124480 |

#### Coluna: `VAL_FAT_AJUSTE`

|   valor |      qtd |
|--------:|---------:|
|    0    | 31456117 |
|    0.01 |     6281 |
|    0.03 |     3595 |
|    0.04 |     3466 |
|    0.02 |     3389 |
|    0.05 |     2610 |
|    0.08 |     2455 |
|    0.06 |     2132 |
|   12.9  |     2006 |
|    4.99 |     1837 |

#### Coluna: `VAL_FAT_BRUTO_BC`

|   valor |    qtd |
|--------:|-------:|
|   34.8  | 663297 |
|   54.9  | 446296 |
|   54.8  | 431789 |
|   29.8  | 375735 |
|   29.9  | 333255 |
|   49.9  | 280431 |
|   34.9  | 278405 |
|   49.8  | 252489 |
|    3.12 | 217214 |
|   64.9  | 209822 |

#### Coluna: `VAL_FAT_PAGAMENTO_BRUTO`

|   valor |      qtd |
|--------:|---------:|
|    0    | 30830578 |
|    0.01 |    17790 |
|   20    |     8350 |
|    0.03 |     7614 |
|    0.04 |     7495 |
|    0.02 |     6640 |
|    0.05 |     6243 |
|    0.08 |     5863 |
|   30    |     5601 |
|    0.07 |     4997 |

#### Coluna: `VAL_FAT_ABERTO`

|   valor |    qtd |
|--------:|-------:|
|   34.8  | 661687 |
|   54.9  | 434382 |
|   54.8  | 426999 |
|   29.8  | 369322 |
|   29.9  | 323764 |
|   49.9  | 273328 |
|   34.9  | 272972 |
|   49.8  | 249415 |
|    3.12 | 217226 |
|   64.9  | 203130 |

#### Coluna: `VAL_FAT_ABERTO_LIQ`

|   valor |     qtd |
|--------:|--------:|
|    0    | 1617486 |
|   54.9  |  880527 |
|   34.8  |  661414 |
|   29.9  |  621158 |
|   34.9  |  590109 |
|   64.9  |  451093 |
|   54.8  |  428680 |
|   49.9  |  376634 |
|   29.8  |  371238 |
|   39.89 |  318124 |

#### Coluna: `VAL_MULTA_JUROS`

|   valor |      qtd |
|--------:|---------:|
|    0    | 19369833 |
|    0.13 |   193826 |
|    0.12 |   164311 |
|    0.14 |   149868 |
|    0.11 |   135495 |
|    0.09 |   134783 |
|    0.1  |   130038 |
|    0.08 |   122094 |
|    0.04 |   108261 |
|    0.15 |   104981 |

#### Coluna: `VAL_MULTA_CANCELAMENTO`

|   valor |      qtd |
|--------:|---------:|
|    0    | 31115884 |
|  110.47 |     2015 |
|  108.16 |     1900 |
|  105.86 |     1756 |
|    0.66 |     1749 |
|   93.37 |     1574 |
|   72.33 |     1558 |
|  107.78 |     1556 |
|   92.38 |     1508 |
|  108.93 |     1508 |

#### Coluna: `VAL_PARC_APARELHO_LIQ`

|    valor |      qtd |
|---------:|---------:|
|     0    | 31600434 |
|   134.37 |      252 |
|   127.97 |      224 |
|   148.58 |      224 |
|   181.58 |      210 |
|  2201.93 |      196 |
| 20046.8  |      180 |
|   605.75 |      165 |
|   126.56 |      164 |
|   207.41 |      161 |

#### Coluna: `VAL_FAT_LIQ_JM_MC`

|   valor |     qtd |
|--------:|--------:|
|    0    | 1616999 |
|   54.9  |  904411 |
|   34.8  |  664101 |
|   29.9  |  639614 |
|   34.9  |  601776 |
|   64.9  |  465884 |
|   54.8  |  432747 |
|   49.9  |  386686 |
|   29.8  |  377164 |
|   39.89 |  325328 |

#### Coluna: `DAT_ATIVACAO_CONTA_CLI`

| valor              |    qtd |
|:-------------------|-------:|
| 18OCT2021:00:00:00 | 150548 |
| 18JUL2021:00:00:00 | 120996 |
| 02OCT2024:00:00:00 | 107281 |
| 14OCT2024:00:00:00 |  99256 |
| 01OCT2024:00:00:00 |  99243 |
| 30OCT2024:00:00:00 |  98926 |
| 01NOV2024:00:00:00 |  98507 |
| 15OCT2024:00:00:00 |  97506 |
| 22JUL2021:00:00:00 |  96110 |
| 16OCT2024:00:00:00 |  94208 |

#### Coluna: `DAT_CRIACAO_DW`

| valor              |   qtd |
|:-------------------|------:|
| 04NOV2024:15:46:22 | 20417 |
| 04JAN2025:13:53:40 | 19978 |
| 04MAR2025:01:38:46 | 19544 |
| 04JAN2025:13:54:10 | 19142 |
| 04JAN2025:13:53:41 | 18916 |
| 04MAR2025:01:38:39 | 18707 |
| 04MAR2025:01:38:43 | 18318 |
| 04JAN2025:13:54:20 | 18087 |
| 04JAN2025:13:53:24 | 17828 |
| 04MAR2025:01:38:41 | 17672 |



---

### 📏 Comprimento de Strings: `raw/atraso`
#### Coluna: `NUM_CPF`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|        11 |        11 |        11 |

#### Coluna: `DAT_REFERENCIA`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|        18 |        18 |        18 |

#### Coluna: `NUM_FATURA_HASH`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|        64 |        64 |        64 |

#### Coluna: `NUM_ENT_SEQ_FATURA`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|         1 |      1.71 |         4 |

#### Coluna: `CONTRATO`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|         8 |         9 |         9 |

#### Coluna: `DW_UN_NEGOCIO`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|         1 |      1.05 |         2 |

#### Coluna: `DW_HIS_PONTO_VENDA_COMTA`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|         2 |      6.87 |         8 |

#### Coluna: `DW_NUM_CLIENTE`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|         9 |      9.94 |        10 |

#### Coluna: `DW_AREA`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|         1 |      1.78 |         2 |

#### Coluna: `DW_CICLO`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|         1 |         2 |         3 |

#### Coluna: `DW_TIPO_CLIENTE_CONTA`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|         1 |       1.5 |         3 |

#### Coluna: `DW_OFERTA`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|         2 |      5.53 |         6 |

#### Coluna: `DW_FAIXA_AGING_FATURA`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|         3 |         3 |         3 |

#### Coluna: `DW_FAIXA_AGING_DIVIDA`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|         3 |         3 |         3 |

#### Coluna: `DW_FAIXA_TEMPO_BASE`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|         2 |      2.98 |         3 |

#### Coluna: `DW_FAIXA_AGING_PROX_FECH`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|         2 |      2.98 |         3 |

#### Coluna: `DW_TIPO_FATURAMENTO`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|         5 |         5 |         5 |

#### Coluna: `COD_PLATAFORMA`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|         2 |      4.78 |         5 |

#### Coluna: `DAT_CRIACAO_REGISTRO_TRANS`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|        18 |        18 |        18 |

#### Coluna: `DAT_ALTERACAO_REGISTRO_TRANS`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|        18 |        18 |        18 |

#### Coluna: `DAT_CANCELAMENTO_FAT`
| min_len   | avg_len   | max_len   |
|:----------|:----------|:----------|
| NULL      | NULL      | NULL      |

#### Coluna: `DAT_ORIGINAL_VCTO_FAT`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|        18 |        18 |        18 |

#### Coluna: `DAT_ALTERACAO_VCTO_FAT`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|        18 |        18 |        18 |

#### Coluna: `DAT_CRIACAO_FAT`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|        18 |        18 |        18 |

#### Coluna: `DAT_VENCIMENTO_FAT`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|        18 |        18 |        18 |

#### Coluna: `DAT_STATUS_FAT`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|        18 |        18 |        18 |

#### Coluna: `DAT_MIN_VENCIMENTO_FAT`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|        18 |        18 |        18 |

#### Coluna: `NUM_BILL_SEQ_FAT`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|         1 |       1.6 |         3 |

#### Coluna: `NUM_SEQ_ACORDO_FAT`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|         1 |      1.98 |         2 |

#### Coluna: `IND_ISENCAO_COB_FAT`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|         1 |      1.89 |         2 |

#### Coluna: `IND_WO`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|         1 |      1.02 |         2 |

#### Coluna: `IND_PDD`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|         1 |      1.02 |         2 |

#### Coluna: `IND_PCCR`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|         1 |      1.02 |         2 |

#### Coluna: `IND_ACA`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|         1 |         1 |         1 |

#### Coluna: `IND_PRIMEIRA_FAT`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|         1 |         1 |         1 |

#### Coluna: `IND_FRAUDE`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|         1 |         1 |         1 |

#### Coluna: `VAL_FAT_LIQUIDO`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|         4 |      4.87 |        10 |

#### Coluna: `VAL_FAT_BRUTO`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|         4 |      4.95 |        10 |

#### Coluna: `VAL_FAT_CREDITO`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|         4 |      4.34 |         9 |

#### Coluna: `VAL_FAT_AJUSTE`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|         4 |         4 |         9 |

#### Coluna: `VAL_FAT_BRUTO_BC`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|         4 |      4.88 |        10 |

#### Coluna: `VAL_FAT_PAGAMENTO_BRUTO`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|         4 |      4.02 |         9 |

#### Coluna: `VAL_FAT_ABERTO`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|         4 |      4.88 |        10 |

#### Coluna: `VAL_FAT_ABERTO_LIQ`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|         4 |      4.86 |        10 |

#### Coluna: `VAL_MULTA_JUROS`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|         4 |         4 |         8 |

#### Coluna: `VAL_MULTA_CANCELAMENTO`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|         4 |      4.02 |         9 |

#### Coluna: `VAL_PARC_APARELHO_LIQ`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|         4 |         4 |        10 |

#### Coluna: `VAL_FAT_LIQ_JM_MC`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|         4 |      4.86 |        10 |

#### Coluna: `DAT_ATIVACAO_CONTA_CLI`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|        18 |        18 |        18 |

#### Coluna: `DAT_CRIACAO_DW`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|        18 |        18 |        18 |



---

