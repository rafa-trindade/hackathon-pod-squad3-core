# Relatório de Profiling: `raw/dados_cadastrais`

### 📦 Volumetria: `raw/dados_cadastrais`
|   qtd_arquivos | registros   |   colunas |   tamanho_comprimido_mib |   tamanho_descomprimido_mib |
|---------------:|:------------|----------:|-------------------------:|----------------------------:|
|              1 | 3.900.378   |        33 |                    74.68 |                      105.86 |

---

### 🧬 Schema: `raw/dados_cadastrais`
| column_name      | column_type   | null   | key   | default   | extra   |
|:-----------------|:--------------|:-------|:------|:----------|:--------|
| NUM_CPF          | VARCHAR       | YES    |       |           |         |
| SAFRA            | VARCHAR       | YES    |       |           |         |
| FLAG_INSTALACAO  | VARCHAR       | YES    |       |           |         |
| FPD              | VARCHAR       | YES    |       |           |         |
| PROD             | VARCHAR       | YES    |       |           |         |
| flag_mig2        | VARCHAR       | YES    |       |           |         |
| STATUSRF         | VARCHAR       | YES    |       |           |         |
| DATADENASCIMENTO | VARCHAR       | YES    |       |           |         |
| var_03           | VARCHAR       | YES    |       |           |         |
| var_02           | VARCHAR       | YES    |       |           |         |
| var_04           | VARCHAR       | YES    |       |           |         |
| var_05           | VARCHAR       | YES    |       |           |         |
| var_06           | VARCHAR       | YES    |       |           |         |
| var_07           | VARCHAR       | YES    |       |           |         |
| var_08           | VARCHAR       | YES    |       |           |         |
| var_09           | VARCHAR       | YES    |       |           |         |
| var_10           | VARCHAR       | YES    |       |           |         |
| var_11           | VARCHAR       | YES    |       |           |         |
| var_12           | VARCHAR       | YES    |       |           |         |
| var_13           | VARCHAR       | YES    |       |           |         |
| var_14           | VARCHAR       | YES    |       |           |         |
| var_15           | VARCHAR       | YES    |       |           |         |
| var_16           | VARCHAR       | YES    |       |           |         |
| var_17           | VARCHAR       | YES    |       |           |         |
| var_18           | VARCHAR       | YES    |       |           |         |
| var_19           | VARCHAR       | YES    |       |           |         |
| var_20           | VARCHAR       | YES    |       |           |         |
| var_21           | VARCHAR       | YES    |       |           |         |
| var_22           | VARCHAR       | YES    |       |           |         |
| var_23           | VARCHAR       | YES    |       |           |         |
| var_24           | VARCHAR       | YES    |       |           |         |
| var_25           | VARCHAR       | YES    |       |           |         |
| CEP_3_digitos    | VARCHAR       | YES    |       |           |         |

---

### 📅 Campos de Data: `raw/dados_cadastrais`
#### ✅ Datas com tipagem (DATE / TIMESTAMP)
> ⚠️ Nenhuma coluna DATE ou TIMESTAMP encontrada.

#### ⚠️ Possíveis campos de data/hora sem tipagem (inferido pelo nome)

- `DATADENASCIMENTO`
- `SAFRA`


---

### 📊 Estatísticas por Coluna: `raw/dados_cadastrais`
| coluna           |   distintos |   nulos |   duplicados | pct_nulos   | pct_duplicados   | cardinalidade   |
|:-----------------|------------:|--------:|-------------:|:------------|:-----------------|:----------------|
| NUM_CPF          |     3590459 |       0 |       309919 | 0.0%        | 7.95%            | ALTA            |
| SAFRA            |           6 |       0 |      3900372 | 0.0%        | 100.0%           | BAIXA           |
| FLAG_INSTALACAO  |           2 |       0 |      3900376 | 0.0%        | 100.0%           | BAIXA           |
| FPD              |           2 | 1203757 |      3900376 | 30.86%      | 100.0%           | BAIXA           |
| PROD             |           3 |       0 |      3900375 | 0.0%        | 100.0%           | BAIXA           |
| flag_mig2        |           3 | 1266478 |      3900375 | 32.47%      | 100.0%           | BAIXA           |
| STATUSRF         |           6 |   15154 |      3900372 | 0.39%       | 100.0%           | BAIXA           |
| DATADENASCIMENTO |       30046 |   16831 |      3870332 | 0.43%       | 99.23%           | MEDIA           |
| var_03           |         100 |  269970 |      3900278 | 6.92%       | 100.0%           | BAIXA           |
| var_02           |        2130 | 3685278 |      3898248 | 94.49%      | 99.95%           | BAIXA           |
| var_04           |           6 |   15154 |      3900372 | 0.39%       | 100.0%           | BAIXA           |
| var_05           |          10 |  196424 |      3900368 | 5.04%       | 100.0%           | BAIXA           |
| var_06           |           1 | 3157126 |      3900377 | 80.94%      | 100.0%           | BAIXA           |
| var_07           |      225525 | 3250748 |      3674853 | 83.34%      | 94.22%           | ALTA            |
| var_08           |          53 | 3157325 |      3900325 | 80.95%      | 100.0%           | BAIXA           |
| var_09           |          17 | 2223690 |      3900361 | 57.01%      | 100.0%           | BAIXA           |
| var_10           |        3320 | 3838163 |      3897058 | 98.4%       | 99.91%           | BAIXA           |
| var_11           |       16030 | 3842389 |      3884348 | 98.51%      | 99.59%           | MEDIA           |
| var_12           |       15469 | 1490335 |      3884909 | 38.21%      | 99.6%            | MEDIA           |
| var_13           |        1502 | 3314097 |      3898876 | 84.97%      | 99.96%           | BAIXA           |
| var_14           |          49 | 3533608 |      3900329 | 90.6%       | 100.0%           | BAIXA           |
| var_15           |          27 | 3315375 |      3900351 | 85.0%       | 100.0%           | BAIXA           |
| var_16           |        1513 | 3315375 |      3898865 | 85.0%       | 99.96%           | BAIXA           |
| var_17           |          20 | 3315375 |      3900358 | 85.0%       | 100.0%           | BAIXA           |
| var_18           |           1 | 3157126 |      3900377 | 80.94%      | 100.0%           | BAIXA           |
| var_19           |           1 | 2223690 |      3900377 | 57.01%      | 100.0%           | BAIXA           |
| var_20           |           1 | 3827574 |      3900377 | 98.13%      | 100.0%           | BAIXA           |
| var_21           |           1 | 1490335 |      3900377 | 38.21%      | 100.0%           | BAIXA           |
| var_22           |           1 | 3533608 |      3900377 | 90.6%       | 100.0%           | BAIXA           |
| var_23           |           1 | 3315375 |      3900377 | 85.0%       | 100.0%           | BAIXA           |
| var_24           |           2 | 1490335 |      3900376 | 38.21%      | 100.0%           | BAIXA           |
| var_25           |          63 |  467469 |      3900315 | 11.99%      | 100.0%           | BAIXA           |
| CEP_3_digitos    |         922 |  292051 |      3899456 | 7.49%       | 99.98%           | BAIXA           |

---

### 🔟 Distribuição de Valores (Top 10): `raw/dados_cadastrais`
#### Coluna: `NUM_CPF`

| valor       |   qtd |
|:------------|------:|
| ZX77YX8WNWN |     6 |
| ZZTZ799U79T |     6 |
| 7X7NZ79YWU9 |     6 |
| WXZY8TNZ7XZ |     6 |
| U8Z9ZZ8N8XZ |     6 |
| 888W78UZYYT |     6 |
| WW7NWZ9Y8ZW |     6 |
| Y77ZYUXU8NW |     6 |
| ZZZZZZZX7T9 |     6 |
| XX9Z8T8YUZT |     6 |

#### Coluna: `SAFRA`

|   valor |    qtd |
|--------:|-------:|
|  202501 | 667227 |
|  202411 | 665737 |
|  202410 | 653586 |
|  202503 | 647830 |
|  202412 | 646037 |
|  202502 | 619961 |

#### Coluna: `FLAG_INSTALACAO`

|   valor |     qtd |
|--------:|--------:|
|       1 | 2696621 |
|       0 | 1203757 |

#### Coluna: `FPD`

|   valor |     qtd |
|--------:|--------:|
|       0 | 2122991 |
|         | 1203757 |
|       1 |  573630 |

#### Coluna: `PROD`

| valor   |     qtd |
|:--------|--------:|
| CMV     | 3795310 |
| NET     |   89968 |
| DTH     |   15100 |

#### Coluna: `flag_mig2`

| valor     |     qtd |
|:----------|--------:|
| Aquisição | 1338888 |
| PRE       | 1290526 |
|           | 1266478 |
| FLEX      |    4486 |

#### Coluna: `STATUSRF`

| valor                     |     qtd |
|:--------------------------|--------:|
| REGULAR                   | 3848697 |
| PENDENTE DE REGULARIZACAO |   31217 |
|                           |   15154 |
| SUSPENSA                  |    2689 |
| TITULAR FALECIDO          |    2398 |
| CANCELADA                 |     222 |
| NULA                      |       1 |

#### Coluna: `DATADENASCIMENTO`

| valor      |   qtd |
|:-----------|------:|
|            | 16831 |
| 10/05/1982 |   355 |
| 10/06/1981 |   349 |
| 05/06/1981 |   348 |
| 20/09/1985 |   346 |
| 10/03/1988 |   345 |
| 12/10/1989 |   345 |
| 08/06/1982 |   344 |
| 06/06/1988 |   343 |
| 29/06/1981 |   342 |

#### Coluna: `var_03`

|   valor |     qtd |
|--------:|--------:|
|      33 | 1191647 |
|         |  269970 |
|       1 |  262689 |
|       3 |  166238 |
|      50 |  106736 |
|      17 |  101647 |
|       5 |   95371 |
|      13 |   91389 |
|     100 |   86508 |
|       2 |   78405 |

#### Coluna: `var_02`

|   valor |     qtd |
|--------:|--------:|
|         | 3685278 |
|  521110 |   12045 |
|  514320 |    8907 |
|  411005 |    8399 |
|  411010 |    7749 |
|  717020 |    6600 |
|  421125 |    5261 |
|  784205 |    4974 |
|  715210 |    4010 |
|  782510 |    3360 |

#### Coluna: `var_04`

|   valor |     qtd |
|--------:|--------:|
|       0 | 3468813 |
|       1 |  247171 |
|       2 |   99910 |
|       3 |   39738 |
|       4 |   16063 |
|         |   15154 |
|       5 |   13529 |

#### Coluna: `var_05`

|   valor |     qtd |
|--------:|--------:|
|       1 | 1655206 |
|       2 | 1359629 |
|       3 |  307874 |
|         |  196424 |
|       4 |  188285 |
|       5 |  103836 |
|       6 |   30620 |
|       7 |   26920 |
|       9 |   16284 |
|       8 |   14557 |

#### Coluna: `var_06`

|   valor |     qtd |
|--------:|--------:|
|         | 3157126 |
|       1 |  743252 |

#### Coluna: `var_07`

|   valor |     qtd |
|--------:|--------:|
|         | 3250748 |
|     954 |   83144 |
|    1045 |   50191 |
|  121200 |   28765 |
|     945 |   12120 |
|   67800 |   11636 |
|       0 |    9781 |
|   54500 |    9596 |
|   51000 |    8837 |
|   62200 |    8313 |

#### Coluna: `var_08`

|   valor |     qtd |
|--------:|--------:|
|         | 3157325 |
|      31 |  253786 |
|      21 |   91866 |
|      42 |   81520 |
|      80 |   76612 |
|      41 |   75112 |
|      87 |   44430 |
|      91 |   38391 |
|      32 |   33996 |
|      88 |   25364 |

#### Coluna: `var_09`

|   valor |     qtd |
|--------:|--------:|
|         | 2223690 |
|       9 |  955897 |
|       8 |  238946 |
|       5 |  161096 |
|       7 |  141786 |
|       6 |   63012 |
|       4 |   47280 |
|       3 |   25347 |
|       2 |   22189 |
|       1 |   20892 |

#### Coluna: `var_10`

| valor                            |     qtd |
|:---------------------------------|--------:|
|                                  | 3838163 |
| SOLDADORECRUTA                   |    5820 |
| SOLDADO                          |    2722 |
| PROFESSOR DO MAGISTERIO SUPERIOR |    1678 |
| CABO ENGAJADO                    |    1495 |
| TERCEIROSARGENTO                 |    1452 |
| PROFESSOR EDUCACAO BASICA II     |    1372 |
| PROFESSOR                        |    1359 |
| PROFESSOR EDUCACAO BASICA I      |    1067 |
| PROFESSOR DE EDUCACAO BASICA     |     997 |

#### Coluna: `var_11`

|   valor |     qtd |
|--------:|--------:|
|         | 3842389 |
|    0    |    9354 |
|  642    |    2311 |
| 1567.5  |    2003 |
|  769    |    1883 |
|  630.1  |    1378 |
| 1747.5  |     633 |
| 2467.5  |     609 |
| 2546.46 |     450 |
| 3774.72 |     376 |

#### Coluna: `var_12`

| valor      |     qtd |
|:-----------|--------:|
|            | 1490335 |
| 01/04/2019 |    8950 |
| 01/10/2019 |    8702 |
| 03/02/2020 |    8565 |
| 01/08/2019 |    8511 |
| 01/02/2019 |    8440 |
| 01/03/2016 |    7802 |
| 01/11/2019 |    7800 |
| 01/02/2017 |    7560 |
| 01/07/2019 |    7498 |

#### Coluna: `var_13`

| valor      |     qtd |
|:-----------|--------:|
|            | 3314097 |
| 31/12/2021 |    6321 |
| 31/12/2018 |    3686 |
| 3112       |    2865 |
| 3006       |    2132 |
| 3011       |    2100 |
| 3004       |    1776 |
| 28/02/2021 |    1744 |
| 3009       |    1674 |
| 3107       |    1613 |

#### Coluna: `var_14`

|   valor |     qtd |
|--------:|--------:|
|         | 3533608 |
|       1 |  325447 |
|       2 |   29525 |
|       3 |    6999 |
|       4 |    2402 |
|       5 |     998 |
|       6 |     533 |
|       7 |     268 |
|       8 |     192 |
|       9 |      93 |

#### Coluna: `var_15`

| valor   |     qtd |
|:--------|--------:|
|         | 3315375 |
| SP      |  105971 |
| RJ      |   79019 |
| BA      |   59037 |
| PE      |   40782 |
| MG      |   36463 |
| PA      |   25427 |
| CE      |   23910 |
| RS      |   23749 |
| GO      |   22887 |

#### Coluna: `var_16`

|   valor |     qtd |
|--------:|--------:|
|         | 3315375 |
|     600 |   90590 |
|     650 |   60965 |
|     750 |   44625 |
|     800 |   29551 |
|     700 |   29479 |
|     440 |   18002 |
|     490 |   16845 |
|     100 |   13943 |
|     325 |   12890 |

#### Coluna: `var_17`

|   valor |     qtd |
|--------:|--------:|
|         | 3315375 |
|  202311 |  243745 |
|  202406 |  233841 |
|  202111 |   79236 |
|  202403 |   12524 |
|  202002 |    5925 |
|  202110 |    3454 |
|  202012 |    3431 |
|  202107 |    1345 |
|  202008 |     524 |

#### Coluna: `var_18`

| valor      |     qtd |
|:-----------|--------:|
|            | 3157126 |
| APOSENTADO |  743252 |

#### Coluna: `var_19`

| valor    |     qtd |
|:---------|--------:|
|          | 2223690 |
| AUX_EMRG | 1676688 |

#### Coluna: `var_20`

| valor     |     qtd |
|:----------|--------:|
|           | 3827574 |
| FUNC_PUBL |   72804 |

#### Coluna: `var_21`

| valor        |     qtd |
|:-------------|--------:|
| FUNC_PRIVADO | 2410043 |
|              | 1490335 |

#### Coluna: `var_22`

| valor        |     qtd |
|:-------------|--------:|
|              | 3533608 |
| EMPR/DIRETOR |  366770 |

#### Coluna: `var_23`

| valor         |     qtd |
|:--------------|--------:|
|               | 3315375 |
| BOLSA_FAMILIA |  585003 |

#### Coluna: `var_24`

| valor      |     qtd |
|:-----------|--------:|
| ADMITIDO   | 1823762 |
|            | 1490335 |
| DISPENSADO |  586281 |

#### Coluna: `var_25`

| valor                               |    qtd |
|:------------------------------------|-------:|
| FUNC_PRIVADO                        | 945989 |
| AUX_EMRG FUNC_PRIVADO               | 535967 |
|                                     | 467469 |
| AUX_EMRG                            | 371795 |
| APOSENTADO FUNC_PRIVADO             | 268762 |
| AUX_EMRG BOLSA_FAMILIA              | 226240 |
| APOSENTADO                          | 198573 |
| AUX_EMRG FUNC_PRIVADO BOLSA_FAMILIA | 169432 |
| FUNC_PRIVADO EMPR/DIRETOR           |  97468 |
| AUX_EMRG FUNC_PRIVADO EMPR/DIRETOR  |  91963 |

#### Coluna: `CEP_3_digitos`

|   valor |    qtd |
|--------:|-------:|
|         | 292051 |
|     690 |  64987 |
|     130 |  31737 |
|     291 |  30344 |
|     768 |  28723 |
|     650 |  28152 |
|     134 |  26167 |
|     790 |  25500 |
|     230 |  24723 |
|     227 |  24184 |



---

### 📏 Comprimento de Strings: `raw/dados_cadastrais`
#### Coluna: `NUM_CPF`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|        11 |        11 |        11 |

#### Coluna: `SAFRA`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|         6 |         6 |         6 |

#### Coluna: `FLAG_INSTALACAO`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|         1 |         1 |         1 |

#### Coluna: `FPD`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|         1 |         1 |         1 |

#### Coluna: `PROD`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|         3 |         3 |         3 |

#### Coluna: `flag_mig2`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|         3 |      6.05 |         9 |

#### Coluna: `STATUSRF`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|         4 |      7.15 |        25 |

#### Coluna: `DATADENASCIMENTO`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|        10 |        10 |        10 |

#### Coluna: `var_03`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|         1 |      1.78 |         3 |

#### Coluna: `var_02`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|         1 |      5.99 |         6 |

#### Coluna: `var_04`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|         1 |         1 |         1 |

#### Coluna: `var_05`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|         1 |         1 |         2 |

#### Coluna: `var_06`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|         1 |         1 |         1 |

#### Coluna: `var_07`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|         1 |       5.2 |         8 |

#### Coluna: `var_08`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|         1 |         2 |         2 |

#### Coluna: `var_09`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|         1 |         1 |         2 |

#### Coluna: `var_10`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|         2 |     20.18 |       162 |

#### Coluna: `var_11`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|         1 |      5.49 |         8 |

#### Coluna: `var_12`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|        10 |        10 |        10 |

#### Coluna: `var_13`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|         4 |      8.51 |        10 |

#### Coluna: `var_14`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|         1 |         1 |         3 |

#### Coluna: `var_15`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|         2 |         2 |         2 |

#### Coluna: `var_16`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|         2 |      3.02 |         4 |

#### Coluna: `var_17`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|         6 |         6 |         6 |

#### Coluna: `var_18`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|        10 |        10 |        10 |

#### Coluna: `var_19`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|         8 |         8 |         8 |

#### Coluna: `var_20`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|         9 |         9 |         9 |

#### Coluna: `var_21`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|        12 |        12 |        12 |

#### Coluna: `var_22`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|        12 |        12 |        12 |

#### Coluna: `var_23`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|        13 |        13 |        13 |

#### Coluna: `var_24`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|         8 |      8.49 |        10 |

#### Coluna: `var_25`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|         8 |     18.89 |        69 |

#### Coluna: `CEP_3_digitos`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|         3 |         3 |         3 |



---

