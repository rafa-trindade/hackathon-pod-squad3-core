# Relatório de Profiling: `raw/recarga`

### 📦 Volumetria: `raw/recarga`
|   qtd_arquivos | registros   |   colunas |   tamanho_comprimido_mib |   tamanho_descomprimido_mib |
|---------------:|:------------|----------:|-------------------------:|----------------------------:|
|             10 | 100.213.651 |        24 |                  3104.31 |                     5222.09 |

---


### 🧬 Schema: `raw/recarga`
| column_name           | column_type   | null   | key   | default   | extra   |
|:----------------------|:--------------|:-------|:------|:----------|:--------|
| NUM_CPF               | VARCHAR       | YES    |       |           |         |
| DW_NUM_NTC            | VARCHAR       | YES    |       |           |         |
| DAT_INSERCAO_CREDITO  | VARCHAR       | YES    |       |           |         |
| HOR_INSERCAO_CREDITO  | VARCHAR       | YES    |       |           |         |
| DW_NUM_CLIENTE        | VARCHAR       | YES    |       |           |         |
| COD_TECNOLOGIA_DW     | VARCHAR       | YES    |       |           |         |
| COD_CANAL_AQUISICAO   | VARCHAR       | YES    |       |           |         |
| COD_TIPO_CREDITO      | VARCHAR       | YES    |       |           |         |
| COD_PROMOCAO          | VARCHAR       | YES    |       |           |         |
| VAL_CREDITO_INSERIDO  | VARCHAR       | YES    |       |           |         |
| VAL_BONUS             | VARCHAR       | YES    |       |           |         |
| VAL_REAL              | VARCHAR       | YES    |       |           |         |
| COD_PLATAFORMA_ATU    | VARCHAR       | YES    |       |           |         |
| COD_STATUS_PLATAFORMA | VARCHAR       | YES    |       |           |         |
| IND_METODO_PAGAMENTO  | VARCHAR       | YES    |       |           |         |
| DW_PLANO_TARIFACAO    | VARCHAR       | YES    |       |           |         |
| DW_TIPO_RECARGA       | VARCHAR       | YES    |       |           |         |
| DW_TIPO_INSERCAO      | VARCHAR       | YES    |       |           |         |
| DW_FORMA_PAGAMENTO    | VARCHAR       | YES    |       |           |         |
| DW_INSTITUICAO        | VARCHAR       | YES    |       |           |         |
| COD_GRUPO_CARTAO      | VARCHAR       | YES    |       |           |         |
| DSC_GRUPO_CARTAO_WPP  | VARCHAR       | YES    |       |           |         |
| FLAG_SOS              | VARCHAR       | YES    |       |           |         |
| VALOR_SOS             | VARCHAR       | YES    |       |           |         |

---

### 📅 Campos de Data: `raw/recarga`
#### ✅ Datas com tipagem (DATE / TIMESTAMP)
> ⚠️ Nenhuma coluna DATE ou TIMESTAMP encontrada.

#### ⚠️ Possíveis campos de data/hora sem tipagem (inferido pelo nome)

- `DAT_INSERCAO_CREDITO`
- `HOR_INSERCAO_CREDITO`


---

### 📊 Estatísticas por Coluna: `raw/recarga`
| coluna                |   distintos |    nulos |   duplicados | pct_nulos   | pct_duplicados   | cardinalidade   |
|:----------------------|------------:|---------:|-------------:|:------------|:-----------------|:----------------|
| NUM_CPF               |     3077601 |        0 |     97136050 | 0.0%        | 96.93%           | MEDIA           |
| DW_NUM_NTC            |     5211901 |        0 |     95001750 | 0.0%        | 94.8%            | ALTA            |
| DAT_INSERCAO_CREDITO  |         548 |        0 |    100213103 | 0.0%        | 100.0%           | BAIXA           |
| HOR_INSERCAO_CREDITO  |       86400 |        0 |    100127251 | 0.0%        | 99.91%           | BAIXA           |
| DW_NUM_CLIENTE        |     7607360 |        0 |     92606291 | 0.0%        | 92.41%           | ALTA            |
| COD_TECNOLOGIA_DW     |           1 |        0 |    100213650 | 0.0%        | 100.0%           | BAIXA           |
| COD_CANAL_AQUISICAO   |         138 |        0 |    100213513 | 0.0%        | 100.0%           | BAIXA           |
| COD_TIPO_CREDITO      |           2 |        0 |    100213649 | 0.0%        | 100.0%           | BAIXA           |
| COD_PROMOCAO          |           1 |  2152012 |    100213650 | 2.15%       | 100.0%           | BAIXA           |
| VAL_CREDITO_INSERIDO  |        4626 |        0 |    100209025 | 0.0%        | 100.0%           | BAIXA           |
| VAL_BONUS             |       75925 |        0 |    100137726 | 0.0%        | 99.92%           | BAIXA           |
| VAL_REAL              |       51845 |        0 |    100161806 | 0.0%        | 99.95%           | BAIXA           |
| COD_PLATAFORMA_ATU    |          13 |        0 |    100213638 | 0.0%        | 100.0%           | BAIXA           |
| COD_STATUS_PLATAFORMA |          17 |        0 |    100213634 | 0.0%        | 100.0%           | BAIXA           |
| IND_METODO_PAGAMENTO  |           2 |        0 |    100213649 | 0.0%        | 100.0%           | BAIXA           |
| DW_PLANO_TARIFACAO    |          97 |  2152012 |    100213554 | 2.15%       | 100.0%           | BAIXA           |
| DW_TIPO_RECARGA       |           3 |  2152012 |    100213648 | 2.15%       | 100.0%           | BAIXA           |
| DW_TIPO_INSERCAO      |          11 |        0 |    100213640 | 0.0%        | 100.0%           | BAIXA           |
| DW_FORMA_PAGAMENTO    |           2 |        0 |    100213649 | 0.0%        | 100.0%           | BAIXA           |
| DW_INSTITUICAO        |         137 |        0 |    100213514 | 0.0%        | 100.0%           | BAIXA           |
| COD_GRUPO_CARTAO      |         250 |        0 |    100213401 | 0.0%        | 100.0%           | BAIXA           |
| DSC_GRUPO_CARTAO_WPP  |          23 |        0 |    100213628 | 0.0%        | 100.0%           | BAIXA           |
| FLAG_SOS              |           2 |        0 |    100213649 | 0.0%        | 100.0%           | BAIXA           |
| VALOR_SOS             |           5 | 93679237 |    100213646 | 93.48%      | 100.0%           | BAIXA           |

---

### 🔟 Distribuição de Valores (Top 10): `raw/recarga`
#### Coluna: `NUM_CPF`

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

#### Coluna: `DW_NUM_NTC`

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

#### Coluna: `DAT_INSERCAO_CREDITO`

| valor              |    qtd |
|:-------------------|-------:|
| 21MAR2025:00:00:00 | 528198 |
| 21FEB2025:00:00:00 | 441769 |
| 04DEC2024:00:00:00 | 428262 |
| 03FEB2025:00:00:00 | 424966 |
| 03JAN2025:00:00:00 | 408187 |
| 21JAN2025:00:00:00 | 407850 |
| 03MAR2025:00:00:00 | 402542 |
| 21DEC2024:00:00:00 | 386298 |
| 03DEC2024:00:00:00 | 372600 |
| 21NOV2024:00:00:00 | 366077 |

#### Coluna: `HOR_INSERCAO_CREDITO`

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

#### Coluna: `DW_NUM_CLIENTE`

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

#### Coluna: `COD_TECNOLOGIA_DW`

| valor   |       qtd |
|:--------|----------:|
| GSM     | 100213651 |

#### Coluna: `COD_CANAL_AQUISICAO`

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

#### Coluna: `COD_TIPO_CREDITO`

| valor   |       qtd |
|:--------|----------:|
| PE      | 100213634 |
| CV      |        17 |

#### Coluna: `COD_PROMOCAO`

|   valor |      qtd |
|--------:|---------:|
|      -1 | 98061639 |
|         |  2152012 |

#### Coluna: `VAL_CREDITO_INSERIDO`

|   valor |      qtd |
|--------:|---------:|
|       0 | 61496530 |
|      20 | 12049955 |
|      30 |  5998131 |
|      25 |  4251971 |
|       5 |  3953519 |
|      15 |  2934362 |
|      10 |  2294876 |
|       0 |  1833733 |
|      35 |  1192585 |
|      12 |   633109 |

#### Coluna: `VAL_BONUS`

|   valor |      qtd |
|--------:|---------:|
|       0 | 46229965 |
|       1 | 11381611 |
|      -1 |  9846605 |
|   84300 |  5471647 |
|     390 |  3914551 |
|   10000 |  3784101 |
|   80500 |  2941259 |
|       0 |  2149815 |
|   42200 |  1482313 |
|      -2 |  1419799 |

#### Coluna: `VAL_REAL`

|   valor |      qtd |
|--------:|---------:|
|       0 | 12327702 |
|      20 | 12151630 |
|       1 | 11911243 |
|      -1 | 10313575 |
|      30 |  6715228 |
|   84300 |  5471647 |
|       5 |  4450635 |
|      25 |  4364326 |
|     390 |  3914555 |
|   10000 |  3784101 |

#### Coluna: `COD_PLATAFORMA_ATU`

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

#### Coluna: `COD_STATUS_PLATAFORMA`

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

#### Coluna: `IND_METODO_PAGAMENTO`

| valor   |       qtd |
|:--------|----------:|
| A       | 100213603 |
| M       |        48 |

#### Coluna: `DW_PLANO_TARIFACAO`

|   valor |      qtd |
|--------:|---------:|
|  541200 | 54703155 |
|  668900 | 13044915 |
|  607690 | 11176911 |
|  599100 |  8081156 |
|  369889 |  2929151 |
|         |  2152012 |
|  567020 |  1911080 |
|  393401 |  1812407 |
|  606235 |  1048407 |
|  608480 |   963468 |

#### Coluna: `DW_TIPO_RECARGA`

|   valor |      qtd |
|--------:|---------:|
|      -2 | 93509722 |
|       2 |  4551844 |
|         |  2152012 |
|       1 |       73 |

#### Coluna: `DW_TIPO_INSERCAO`

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

#### Coluna: `DW_FORMA_PAGAMENTO`

|   valor |      qtd |
|--------:|---------:|
|      -2 | 98061639 |
|      10 |  2152012 |

#### Coluna: `DW_INSTITUICAO`

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

#### Coluna: `COD_GRUPO_CARTAO`

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

#### Coluna: `DSC_GRUPO_CARTAO_WPP`

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

#### Coluna: `FLAG_SOS`

|   valor |      qtd |
|--------:|---------:|
|       0 | 93679237 |
|       1 |  6534414 |

#### Coluna: `VALOR_SOS`

|   valor |      qtd |
|--------:|---------:|
|         | 93679237 |
|       5 |  4092483 |
|      10 |  1629266 |
|      20 |   366642 |
|      15 |   324685 |
|       3 |   121338 |



---

### 📏 Comprimento de Strings: `raw/recarga`
#### Coluna: `NUM_CPF`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|        11 |        11 |        11 |

#### Coluna: `DW_NUM_NTC`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|         8 |         9 |         9 |

#### Coluna: `DAT_INSERCAO_CREDITO`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|        18 |        18 |        18 |

#### Coluna: `HOR_INSERCAO_CREDITO`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|         1 |      5.49 |         6 |

#### Coluna: `DW_NUM_CLIENTE`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|         2 |      9.92 |        10 |

#### Coluna: `COD_TECNOLOGIA_DW`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|         3 |         3 |         3 |

#### Coluna: `COD_CANAL_AQUISICAO`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|         2 |      2.79 |         5 |

#### Coluna: `COD_TIPO_CREDITO`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|         2 |         2 |         2 |

#### Coluna: `COD_PROMOCAO`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|         2 |         2 |         2 |

#### Coluna: `VAL_CREDITO_INSERIDO`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|         1 |      4.26 |         8 |

#### Coluna: `VAL_BONUS`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|         1 |      4.92 |         9 |

#### Coluna: `VAL_REAL`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|         1 |       5.2 |         9 |

#### Coluna: `COD_PLATAFORMA_ATU`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|         4 |         5 |         5 |

#### Coluna: `COD_STATUS_PLATAFORMA`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|         1 |      1.09 |         3 |

#### Coluna: `IND_METODO_PAGAMENTO`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|         1 |         1 |         1 |

#### Coluna: `DW_PLANO_TARIFACAO`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|         6 |         6 |         6 |

#### Coluna: `DW_TIPO_RECARGA`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|         1 |      1.95 |         2 |

#### Coluna: `DW_TIPO_INSERCAO`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|         1 |      1.97 |         2 |

#### Coluna: `DW_FORMA_PAGAMENTO`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|         2 |         2 |         2 |

#### Coluna: `DW_INSTITUICAO`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|         2 |      2.87 |         5 |

#### Coluna: `COD_GRUPO_CARTAO`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|         2 |         2 |         2 |

#### Coluna: `DSC_GRUPO_CARTAO_WPP`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|         2 |     10.45 |        12 |

#### Coluna: `FLAG_SOS`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|         1 |         1 |         1 |

#### Coluna: `VALOR_SOS`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|         1 |      1.36 |         2 |



---

