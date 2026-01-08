# Relatório de Profiling: `bronze/recarga` - `20260108_191955`

### 📦 Volumetria: `bronze/recarga`
| diretorio      |   qtd_arquivos | registros   |   colunas |   tamanho_comprimido_mib |   tamanho_descomprimido_mib |
|:---------------|---------------:|:------------|----------:|-------------------------:|----------------------------:|
| ano_mes=202310 |              1 | 4.366.091   |        27 |                   106    |                      255.75 |
| ano_mes=202311 |              1 | 4.312.612   |        27 |                   105.97 |                      252.66 |
| ano_mes=202312 |              1 | 4.609.579   |        27 |                   112.5  |                      270.16 |
| ano_mes=202401 |              1 | 4.397.192   |        27 |                   109.22 |                      258    |
| ano_mes=202402 |              1 | 4.444.044   |        27 |                   110.16 |                      260.59 |
| ano_mes=202403 |              1 | 4.981.887   |        27 |                   120.27 |                      292.1  |
| ano_mes=202404 |              1 | 4.890.093   |        27 |                   119.38 |                      286.12 |
| ano_mes=202405 |              1 | 5.102.046   |        27 |                   123.92 |                      298.57 |
| ano_mes=202406 |              1 | 5.150.385   |        27 |                   127.02 |                      303.56 |
| ano_mes=202407 |              1 | 5.549.310   |        27 |                   135.57 |                      327.16 |
| ano_mes=202408 |              1 | 5.903.693   |        27 |                   142.5  |                      347.78 |
| ano_mes=202409 |              1 | 5.849.901   |        27 |                   141.74 |                      344.63 |
| ano_mes=202410 |              1 | 6.849.716   |        27 |                   163.66 |                      403.67 |
| ano_mes=202411 |              1 | 7.187.244   |        27 |                   172.91 |                      422.42 |
| ano_mes=202412 |              1 | 7.321.919   |        27 |                   176.65 |                      429.35 |
| ano_mes=202501 |              1 | 6.691.129   |        27 |                   163.55 |                      391.91 |
| ano_mes=202502 |              1 | 6.271.393   |        27 |                   155.84 |                      366.75 |
| ano_mes=202503 |              1 | 6.335.417   |        27 |                   156.38 |                      370.77 |
| TOTAL          |             18 | 100.213.651 |        27 |                  2443.24 |                     5881.96 |

---

### 🧬 Schema: `bronze/recarga`
| column_name           | column_type              | null   | key   | default   | extra   |
|:----------------------|:-------------------------|:-------|:------|:----------|:--------|
| num_cpf               | VARCHAR                  | YES    |       |           |         |
| dw_num_ntc            | VARCHAR                  | YES    |       |           |         |
| dw_num_cliente        | VARCHAR                  | YES    |       |           |         |
| dat_insercao_credito  | DATE                     | YES    |       |           |         |
| hor_insercao_credito  | VARCHAR                  | YES    |       |           |         |
| flag_sos              | BOOLEAN                  | YES    |       |           |         |
| cod_tecnologia_dw     | VARCHAR                  | YES    |       |           |         |
| cod_canal_aquisicao   | VARCHAR                  | YES    |       |           |         |
| cod_tipo_credito      | VARCHAR                  | YES    |       |           |         |
| cod_promocao          | VARCHAR                  | YES    |       |           |         |
| cod_plataforma_atu    | VARCHAR                  | YES    |       |           |         |
| cod_status_plataforma | VARCHAR                  | YES    |       |           |         |
| ind_metodo_pagamento  | VARCHAR                  | YES    |       |           |         |
| dw_plano_tarifacao    | VARCHAR                  | YES    |       |           |         |
| dw_tipo_recarga       | VARCHAR                  | YES    |       |           |         |
| dw_tipo_insercao      | VARCHAR                  | YES    |       |           |         |
| dw_forma_pagamento    | VARCHAR                  | YES    |       |           |         |
| dw_instituicao        | VARCHAR                  | YES    |       |           |         |
| cod_grupo_cartao      | VARCHAR                  | YES    |       |           |         |
| dsc_grupo_cartao_wpp  | VARCHAR                  | YES    |       |           |         |
| val_credito_inserido  | DOUBLE                   | YES    |       |           |         |
| val_bonus             | DOUBLE                   | YES    |       |           |         |
| val_real              | DOUBLE                   | YES    |       |           |         |
| valor_sos             | DOUBLE                   | YES    |       |           |         |
| ingestion_ts          | TIMESTAMP WITH TIME ZONE | YES    |       |           |         |
| ano_mes               | BIGINT                   | YES    |       |           |         |
| run_id                | VARCHAR                  | YES    |       |           |         |

---

### 📅 Range de Datas: `bronze/recarga`
#### Coluna: `dat_insercao_credito`
| min                        | max                        |
|:---------------------------|:---------------------------|
| 2023-10-01T00:00:00.000000 | 2025-03-31T00:00:00.000000 |

#### Coluna: `ingestion_ts`
| min                              | max                              |
|:---------------------------------|:---------------------------------|
| 2026-01-08 16:19:55.941150-03:00 | 2026-01-08 16:19:55.941150-03:00 |



---

### 📊 Estatísticas por Coluna: `bronze/recarga`
| coluna                |   distintos |    nulos |   duplicados | pct_nulos   | pct_duplicados   | cardinalidade   |
|:----------------------|------------:|---------:|-------------:|:------------|:-----------------|:----------------|
| num_cpf               |     3077601 |        0 |     97136050 | 0.0%        | 96.93%           | MEDIA           |
| dw_num_ntc            |     5211901 |        0 |     95001750 | 0.0%        | 94.8%            | ALTA            |
| dw_num_cliente        |     7607360 |        0 |     92606291 | 0.0%        | 92.41%           | ALTA            |
| dat_insercao_credito  |         548 |        0 |    100213103 | 0.0%        | 100.0%           | BAIXA           |
| hor_insercao_credito  |       86400 |        0 |    100127251 | 0.0%        | 99.91%           | BAIXA           |
| flag_sos              |           2 |        0 |    100213649 | 0.0%        | 100.0%           | BAIXA           |
| cod_tecnologia_dw     |           1 |        0 |    100213650 | 0.0%        | 100.0%           | BAIXA           |
| cod_canal_aquisicao   |         138 |        0 |    100213513 | 0.0%        | 100.0%           | BAIXA           |
| cod_tipo_credito      |           2 |        0 |    100213649 | 0.0%        | 100.0%           | BAIXA           |
| cod_promocao          |           1 |  2152012 |    100213650 | 2.15%       | 100.0%           | BAIXA           |
| cod_plataforma_atu    |          13 |        0 |    100213638 | 0.0%        | 100.0%           | BAIXA           |
| cod_status_plataforma |          17 |        0 |    100213634 | 0.0%        | 100.0%           | BAIXA           |
| ind_metodo_pagamento  |           2 |        0 |    100213649 | 0.0%        | 100.0%           | BAIXA           |
| dw_plano_tarifacao    |          97 |  2152012 |    100213554 | 2.15%       | 100.0%           | BAIXA           |
| dw_tipo_recarga       |           3 |  2152012 |    100213648 | 2.15%       | 100.0%           | BAIXA           |
| dw_tipo_insercao      |          11 |        0 |    100213640 | 0.0%        | 100.0%           | BAIXA           |
| dw_forma_pagamento    |           2 |        0 |    100213649 | 0.0%        | 100.0%           | BAIXA           |
| dw_instituicao        |         137 |        0 |    100213514 | 0.0%        | 100.0%           | BAIXA           |
| cod_grupo_cartao      |         250 |        0 |    100213401 | 0.0%        | 100.0%           | BAIXA           |
| dsc_grupo_cartao_wpp  |          23 |        0 |    100213628 | 0.0%        | 100.0%           | BAIXA           |
| val_credito_inserido  |        4609 |        0 |    100209042 | 0.0%        | 100.0%           | BAIXA           |
| val_bonus             |       75920 |        0 |    100137731 | 0.0%        | 99.92%           | BAIXA           |
| val_real              |       51832 |        0 |    100161819 | 0.0%        | 99.95%           | BAIXA           |
| valor_sos             |           5 | 93679237 |    100213646 | 93.48%      | 100.0%           | BAIXA           |
| ingestion_ts          |           1 |        0 |    100213650 | 0.0%        | 100.0%           | BAIXA           |
| ano_mes               |          18 |        0 |    100213633 | 0.0%        | 100.0%           | BAIXA           |
| run_id                |           1 |        0 |    100213650 | 0.0%        | 100.0%           | BAIXA           |

---

### 🔟 Distribuição de Valores (Top 10): `bronze/recarga`
#### Coluna: `num_cpf`

| valor       |   qtd |
|:------------|------:|
| XYT9U8X778W |  6703 |
| ZW797ZWZYT8 |  5608 |
| Z9WWUTT77XZ |  4878 |
| Z9YXUZYU7WX |  4873 |
| UUWUWZXX879 |  4755 |
| Z78YXX78YX7 |  4732 |
| XZNYZZNU7ZN |  4296 |
| X8YXWUN97XY |  4272 |
| ZX9YWXZT779 |  4253 |
| Z7ZWZ9XY7XW |  4081 |

#### Coluna: `dw_num_ntc`

|     valor |   qtd |
|----------:|------:|
| 648397569 |  3690 |
| 667413637 |  3377 |
| 652990493 |  3249 |
| 664947860 |  3212 |
| 739629381 |  2762 |
| 643133488 |  2687 |
| 748935078 |  2684 |
| 104291891 |  2683 |
| 590415338 |  2640 |
| 678572382 |  2614 |

#### Coluna: `dw_num_cliente`

|      valor |   qtd |
|-----------:|------:|
|         -2 | 18665 |
| 1139798979 |  3676 |
| 1164497165 |  3367 |
| 1145635585 |  3249 |
| 1161777754 |  3208 |
| 1403189723 |  2762 |
| 1415985368 |  2684 |
| 1189777104 |  2683 |
| 1053401384 |  2626 |
| 1178119367 |  2614 |

#### Coluna: `dat_insercao_credito`

| valor      |    qtd |
|:-----------|-------:|
| 2025-03-21 | 528198 |
| 2025-02-21 | 441769 |
| 2024-12-04 | 428262 |
| 2025-02-03 | 424966 |
| 2025-01-03 | 408187 |
| 2025-01-21 | 407850 |
| 2025-03-03 | 402542 |
| 2024-12-21 | 386298 |
| 2024-12-03 | 372600 |
| 2024-11-21 | 366077 |

#### Coluna: `hor_insercao_credito`

|   valor |   qtd |
|--------:|------:|
|   54211 |  9176 |
|   54204 |  9175 |
|   54207 |  9166 |
|   54209 |  9118 |
|   54208 |  9068 |
|   54212 |  9038 |
|   54203 |  9016 |
|   54210 |  8994 |
|   54205 |  8972 |
|   54206 |  8955 |

#### Coluna: `flag_sos`

| valor   |      qtd |
|:--------|---------:|
| false   | 93679237 |
| true    |  6534414 |

#### Coluna: `cod_tecnologia_dw`

| valor   |       qtd |
|:--------|----------:|
| GSM     | 100213651 |

#### Coluna: `cod_canal_aquisicao`

|   valor |      qtd |
|--------:|---------:|
|      -3 | 63971179 |
|      -2 |  7165424 |
|   16307 |  6667945 |
|   17627 |  2328698 |
|   17537 |  2249915 |
|   16357 |  1269216 |
|   16167 |  1100536 |
|   16187 |  1058023 |
|   15987 |  1042243 |
|   17621 |  1008240 |

#### Coluna: `cod_tipo_credito`

| valor   |       qtd |
|:--------|----------:|
| PE      | 100213634 |
| CV      |        17 |

#### Coluna: `cod_promocao`

| valor   |      qtd |
|:--------|---------:|
| -1      | 98061639 |
| NULL    |  2152012 |

#### Coluna: `cod_plataforma_atu`

| valor   |      qtd |
|:--------|---------:|
| PREPG   | 69182083 |
| AUTOC   | 26999142 |
| FLEXD   |  2076381 |
| CTLFC   |  1918277 |
| POSPG   |    34384 |
| MVNOD   |     2044 |
| POSRI   |      518 |
| POSTL   |      388 |
| POSBL   |      295 |
| PRECN   |       53 |

#### Coluna: `cod_status_plataforma`

| valor   |      qtd |
|:--------|---------:|
| A       | 95844056 |
| ZB1     |  4294201 |
| ZB2     |    35402 |
| -3      |    29945 |
| NDF     |     4841 |
| COL     |     2544 |
| PRE     |      718 |
| C       |      603 |
| ST      |      416 |
| U       |      298 |

#### Coluna: `ind_metodo_pagamento`

| valor   |       qtd |
|:--------|----------:|
| A       | 100213603 |
| M       |        48 |

#### Coluna: `dw_plano_tarifacao`

| valor   |      qtd |
|:--------|---------:|
| 541200  | 54703155 |
| 668900  | 13044915 |
| 607690  | 11176911 |
| 599100  |  8081156 |
| 369889  |  2929151 |
| NULL    |  2152012 |
| 567020  |  1911080 |
| 393401  |  1812407 |
| 606235  |  1048407 |
| 608480  |   963468 |

#### Coluna: `dw_tipo_recarga`

| valor   |      qtd |
|:--------|---------:|
| -2      | 93509722 |
| 2       |  4551844 |
| NULL    |  2152012 |
| 1       |       73 |

#### Coluna: `dw_tipo_insercao`

|   valor |      qtd |
|--------:|---------:|
|      -2 | 93509722 |
|       3 |  2784827 |
|      21 |  2736570 |
|      19 |   650651 |
|      99 |   531540 |
|      18 |      113 |
|      22 |       94 |
|       4 |       73 |
|       1 |       34 |
|      10 |       26 |

#### Coluna: `dw_forma_pagamento`

|   valor |      qtd |
|--------:|---------:|
|      -2 | 98061639 |
|      10 |  2152012 |

#### Coluna: `dw_instituicao`

|   valor |      qtd |
|--------:|---------:|
|      -1 | 63655482 |
|      -2 |  7574882 |
|   14433 |  6715184 |
|   14472 |  2317689 |
|   14475 |  2205879 |
|   14211 |  1283028 |
|   14427 |  1063639 |
|   14434 |  1047880 |
|   13934 |   969168 |
|   14452 |   932084 |

#### Coluna: `cod_grupo_cartao`

| valor   |      qtd |
|:--------|---------:|
| UB      | 11706356 |
| WT      | 10813756 |
| PY      |  8748579 |
| I8      |  6007706 |
| UD      |  5983895 |
| IW      |  4278141 |
| UC      |  4248697 |
| FW      |  3914541 |
| FV      |  3828598 |
| G6      |  3703976 |

#### Coluna: `dsc_grupo_cartao_wpp`

| valor        |      qtd |
|:-------------|---------:|
| NaoSeAplica  | 61563241 |
| Rec.Online   | 27752653 |
| AtivPromocao |  6007710 |
| -2           |  3601656 |
| ChipPre+R$30 |   662041 |
| ForcaZB2     |   531540 |
| ChipPre+R$25 |    94010 |
| Pl. Controle |      241 |
| PCT LDN ILIM |      227 |
| Pacote SMS   |      139 |

#### Coluna: `val_credito_inserido`

|   valor |      qtd |
|--------:|---------:|
|       0 | 63330263 |
|      20 | 12120732 |
|      30 |  6051484 |
|      25 |  4263034 |
|       5 |  3953991 |
|      15 |  2950537 |
|      10 |  2294908 |
|      35 |  1221326 |
|      40 |   702923 |
|      12 |   633111 |

#### Coluna: `val_bonus`

|   valor |      qtd |
|--------:|---------:|
|       0 | 48379780 |
|       1 | 11381611 |
|      -1 |  9846605 |
|   84300 |  5471647 |
|     390 |  3914551 |
|   10000 |  3784101 |
|   80500 |  2941259 |
|   42200 |  1482313 |
|      -2 |  1419799 |
|   21100 |  1332171 |

#### Coluna: `val_real`

|   valor |      qtd |
|--------:|---------:|
|       0 | 14163632 |
|      20 | 12222407 |
|       1 | 11911243 |
|      -1 | 10313575 |
|      30 |  6768581 |
|   84300 |  5471647 |
|       5 |  4450635 |
|      25 |  4375389 |
|     390 |  3914555 |
|   10000 |  3784101 |

#### Coluna: `valor_sos`

| valor   |      qtd |
|:--------|---------:|
| NULL    | 93679237 |
| 5.0     |  4092483 |
| 10.0    |  1629266 |
| 20.0    |   366642 |
| 15.0    |   324685 |
| 3.0     |   121338 |

#### Coluna: `ingestion_ts`

| valor                        |       qtd |
|:-----------------------------|----------:|
| 2026-01-08 16:19:55.94115-03 | 100213651 |

#### Coluna: `ano_mes`

|   valor |     qtd |
|--------:|--------:|
|  202412 | 7321919 |
|  202411 | 7187244 |
|  202410 | 6849716 |
|  202501 | 6691129 |
|  202503 | 6335417 |
|  202502 | 6271393 |
|  202408 | 5903693 |
|  202409 | 5849901 |
|  202407 | 5549310 |
|  202406 | 5150385 |

#### Coluna: `run_id`

|           valor |       qtd |
|----------------:|----------:|
| 20260108_191955 | 100213651 |



---

