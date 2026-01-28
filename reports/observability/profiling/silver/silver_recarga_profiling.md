# Relatório de Profiling: `silver/recarga` - `20260128`

### 🔑 Garantia de Unicidade: `silver/recarga`
- **Chave Técnica:** `num_cpf, dat_insercao_credito, hor_insercao_credito`
- **Tipo:** `COMPOSTA`

| coluna        |   distintos |   nulos |   duplicados | pct_nulos   | pct_duplicados   | cardinalidade   |
|:--------------|------------:|--------:|-------------:|:------------|:-----------------|:----------------|
| CHAVE_TECNICA |    95386289 |       0 |            0 | 0.0%        | 0.0%             | MÁXIMA          |

### 🚩 Diagnóstico e Observações Técnicas
* ✅ **Sucesso:** Unicidade Garantida. O grão da tabela está preservado.


---

### 📊 Schema e Estatísticas: `silver/recarga`
| column_name           | column_type              |   distintos |    nulos |   duplicados | pct_nulos   | pct_duplicados   | cardinalidade   |
|:----------------------|:-------------------------|------------:|---------:|-------------:|:------------|:-----------------|:----------------|
| num_cpf               | VARCHAR                  |     2746295 |        0 |     92639994 | 0.0%        | 97.12%           | MEDIA           |
| dat_insercao_credito  | DATE                     |         538 |        0 |     95385751 | 0.0%        | 100.0%           | BAIXA           |
| hor_insercao_credito  | VARCHAR                  |       86309 |        0 |     95299980 | 0.0%        | 99.91%           | BAIXA           |
| cod_canal_aquisicao   | VARCHAR                  |         133 |        0 |     95386156 | 0.0%        | 100.0%           | BAIXA           |
| dsc_canal_aquisicao   | VARCHAR                  |         123 |        0 |     95386166 | 0.0%        | 100.0%           | BAIXA           |
| dw_forma_pagamento    | VARCHAR                  |           2 |        0 |     95386287 | 0.0%        | 100.0%           | BAIXA           |
| dsc_forma_pagamento   | VARCHAR                  |           2 |        0 |     95386287 | 0.0%        | 100.0%           | BAIXA           |
| dw_instituicao        | VARCHAR                  |         129 |        0 |     95386160 | 0.0%        | 100.0%           | BAIXA           |
| dsc_instituicao       | VARCHAR                  |         125 |        0 |     95386164 | 0.0%        | 100.0%           | BAIXA           |
| dw_plano_tarifacao    | VARCHAR                  |         104 |  2105707 |     95386185 | 2.21%       | 100.0%           | BAIXA           |
| dsc_plano_tarifacao   | VARCHAR                  |          79 |        0 |     95386210 | 0.0%        | 100.0%           | BAIXA           |
| cod_plataforma_atu    | VARCHAR                  |          13 |        0 |     95386276 | 0.0%        | 100.0%           | BAIXA           |
| dsc_plataforma_atu    | VARCHAR                  |          13 |        0 |     95386276 | 0.0%        | 100.0%           | BAIXA           |
| cod_promocao          | VARCHAR                  |           1 |  2105707 |     95386288 | 2.21%       | 100.0%           | BAIXA           |
| dsc_promocao          | VARCHAR                  |           2 |        0 |     95386287 | 0.0%        | 100.0%           | BAIXA           |
| cod_status_plataforma | VARCHAR                  |          17 |        0 |     95386272 | 0.0%        | 100.0%           | BAIXA           |
| dsc_status_plataforma | VARCHAR                  |           9 |        0 |     95386280 | 0.0%        | 100.0%           | BAIXA           |
| cod_tecnologia_dw     | VARCHAR                  |           1 |        0 |     95386288 | 0.0%        | 100.0%           | BAIXA           |
| dsc_tecnologia        | VARCHAR                  |           1 |        0 |     95386288 | 0.0%        | 100.0%           | BAIXA           |
| cod_tipo_credito      | VARCHAR                  |           2 |        0 |     95386287 | 0.0%        | 100.0%           | BAIXA           |
| dsc_tipo_credito      | VARCHAR                  |           2 |        0 |     95386287 | 0.0%        | 100.0%           | BAIXA           |
| dw_tipo_insercao      | VARCHAR                  |          11 |        0 |     95386278 | 0.0%        | 100.0%           | BAIXA           |
| dsc_tipo_insercao     | VARCHAR                  |           7 |        0 |     95386282 | 0.0%        | 100.0%           | BAIXA           |
| dw_tipo_recarga       | VARCHAR                  |           3 |  2105707 |     95386286 | 2.21%       | 100.0%           | BAIXA           |
| dsc_tipo_recarga      | VARCHAR                  |           4 |        0 |     95386285 | 0.0%        | 100.0%           | BAIXA           |
| cod_grupo_cartao      | VARCHAR                  |         240 |        0 |     95386049 | 0.0%        | 100.0%           | BAIXA           |
| dsc_grupo_cartao_wpp  | VARCHAR                  |          25 |        0 |     95386264 | 0.0%        | 100.0%           | BAIXA           |
| dw_num_cliente        | VARCHAR                  |     6245708 |        0 |     89140581 | 0.0%        | 93.45%           | ALTA            |
| dw_num_ntc            | VARCHAR                  |     4144008 |        0 |     91242281 | 0.0%        | 95.66%           | MEDIA           |
| flag_sos              | BOOLEAN                  |           2 |        0 |     95386287 | 0.0%        | 100.0%           | BAIXA           |
| ind_metodo_pagamento  | VARCHAR                  |           2 |        0 |     95386287 | 0.0%        | 100.0%           | BAIXA           |
| val_bonus             | DOUBLE                   |       65011 |        0 |     95321278 | 0.0%        | 99.93%           | BAIXA           |
| val_credito_inserido  | DOUBLE                   |        4613 |        0 |     95381676 | 0.0%        | 100.0%           | BAIXA           |
| val_real              | DOUBLE                   |       50763 |        0 |     95335526 | 0.0%        | 99.95%           | BAIXA           |
| valor_sos             | DOUBLE                   |           5 | 88851918 |     95386284 | 93.15%      | 100.0%           | BAIXA           |
| ingestion_ts          | TIMESTAMP WITH TIME ZONE |           1 |        0 |     95386288 | 0.0%        | 100.0%           | BAIXA           |
| run_id                | BIGINT                   |           1 |        0 |     95386288 | 0.0%        | 100.0%           | BAIXA           |
| ano_mes               | BIGINT                   |          20 |        0 |     95386269 | 0.0%        | 100.0%           | BAIXA           |

---

### 📦 Volumetria: `silver/recarga`
| diretorio      |   qtd_arquivos | registros   |   colunas |   tamanho_comprimido_mib |   tamanho_descomprimido_mib |
|:---------------|---------------:|:------------|----------:|-------------------------:|----------------------------:|
| ano_mes=202310 |              1 | 4.182.629   |        38 |                   119.17 |                      257.19 |
| ano_mes=202311 |              1 | 4.153.371   |        38 |                   118.12 |                      255.74 |
| ano_mes=202312 |              1 | 4.440.690   |        38 |                   125.19 |                      273.45 |
| ano_mes=202401 |              1 | 4.238.829   |        38 |                   120.58 |                      261.4  |
| ano_mes=202402 |              1 | 4.254.204   |        38 |                   122.36 |                      262.29 |
| ano_mes=202403 |              1 | 4.736.808   |        38 |                   133.55 |                      291.89 |
| ano_mes=202404 |              1 | 4.641.082   |        38 |                   131.32 |                      284.55 |
| ano_mes=202405 |              1 | 4.822.127   |        38 |                   136.7  |                      296.16 |
| ano_mes=202406 |              1 | 4.886.421   |        38 |                   138.28 |                      297.82 |
| ano_mes=202407 |              1 | 5.257.411   |        38 |                   148.51 |                      321.3  |
| ano_mes=202408 |              1 | 5.557.900   |        38 |                   155.75 |                      338.77 |
| ano_mes=202409 |              1 | 5.512.580   |        38 |                   155.31 |                      336.11 |
| ano_mes=202410 |              1 | 6.480.407   |        38 |                   177.97 |                      395.87 |
| ano_mes=202411 |              1 | 6.800.420   |        38 |                   187.55 |                      415.97 |
| ano_mes=202412 |              1 | 6.927.326   |        38 |                   190.46 |                      422.58 |
| ano_mes=202501 |              1 | 6.366.515   |        38 |                   174.64 |                      387.88 |
| ano_mes=202502 |              1 | 6.030.903   |        38 |                   164.52 |                      366.6  |
| ano_mes=202503 |              1 | 6.096.666   |        38 |                   166.24 |                      371.69 |
| TOTAL          |             18 | 95.386.289  |        38 |                  2666.21 |                     5837.24 |

---

### 📅 Range de Datas: `silver/recarga`
#### Coluna: `dat_insercao_credito`
| min                        | max                        |
|:---------------------------|:---------------------------|
| 2023-10-01T00:00:00.000000 | 2025-03-31T00:00:00.000000 |

#### Coluna: `ingestion_ts`
| min                              | max                              |
|:---------------------------------|:---------------------------------|
| 2026-01-28 00:48:31.596268-03:00 | 2026-01-28 00:48:31.596268-03:00 |



---

### 🔢 Range de Valores Numéricos: `silver/recarga`

#### Coluna: `val_bonus`
|      min |   max |   media |
|---------:|------:|--------:|
| -87895.2 | 95500 | 10348.5 |

#### Coluna: `val_credito_inserido`
|   min |   max |   media |
|------:|------:|--------:|
|     0 | 25000 |    8.45 |

#### Coluna: `val_real`
|      min |   max |   media |
|---------:|------:|--------:|
| -87895.2 | 95500 | 10356.9 |

#### Coluna: `valor_sos`
|   min |   max |   media |
|------:|------:|--------:|
|     3 |    20 |    7.55 |



---

### 🔟 Distribuição de Valores (Top 10): `silver/recarga`
#### Coluna: `num_cpf`

| valor       |   qtd |
|:------------|------:|
| XYT9U8X778W |  3919 |
| ZW797ZWZYT8 |  3286 |
| Z9YXUZYU7WX |  2874 |
| UUWUWZXX879 |  2801 |
| Z9WWUTT77XZ |  2801 |
| Z78YXX78YX7 |  2742 |
| ZX9YWXZT779 |  2501 |
| XZNYZZNU7ZN |  2500 |
| X8YXWUN97XY |  2497 |
| XYYTXUWTTXU |  2449 |

#### Coluna: `dat_insercao_credito`

| valor      |    qtd |
|:-----------|-------:|
| 2025-03-21 | 519168 |
| 2025-02-21 | 431136 |
| 2025-02-03 | 415207 |
| 2024-12-04 | 414133 |
| 2025-01-03 | 395958 |
| 2025-03-03 | 395640 |
| 2025-01-21 | 394274 |
| 2024-12-21 | 373517 |
| 2024-12-03 | 357827 |
| 2024-11-21 | 351538 |

#### Coluna: `hor_insercao_credito`

|   valor |   qtd |
|--------:|------:|
|   54211 |  9152 |
|   54204 |  9139 |
|   54207 |  9118 |
|   54209 |  9086 |
|   54208 |  9034 |
|   54212 |  9015 |
|   54203 |  8963 |
|   54210 |  8956 |
|   54205 |  8928 |
|   54206 |  8900 |

#### Coluna: `cod_canal_aquisicao`

|   valor |      qtd |
|--------:|---------:|
|      -3 | 60138304 |
|   16307 |  6667847 |
|      -2 |  6174230 |
|   17627 |  2328661 |
|   17537 |  2249859 |
|   16357 |  1269188 |
|   16167 |  1100500 |
|   16187 |  1057920 |
|   15987 |  1040955 |
|   17621 |  1007970 |

#### Coluna: `dsc_canal_aquisicao`

| valor                |      qtd |
|:---------------------|---------:|
| ni                   | 60138304 |
| epay campanhas       |  6667847 |
| nd                   |  6174230 |
| m4u/bemobi pix e 3ds |  2328661 |
| dbr                  |  2249859 |
| mercado pago         |  1269188 |
| rv 11                |  1100500 |
| rv 31 nac            |  1057920 |
| tendencia nac        |  1040955 |
| [rd] controle facil  |  1007970 |

#### Coluna: `dw_forma_pagamento`

|   valor |      qtd |
|--------:|---------:|
|      -2 | 93280582 |
|      10 |  2105707 |

#### Coluna: `dsc_forma_pagamento`

| valor            |      qtd |
|:-----------------|---------:|
| não determinado  | 93280582 |
| pagamento online |  2105707 |

#### Coluna: `dw_instituicao`

|   valor |      qtd |
|--------:|---------:|
|      -1 | 59822642 |
|   14433 |  6715082 |
|      -2 |  6583660 |
|   14472 |  2317653 |
|   14475 |  2205825 |
|   14211 |  1282998 |
|   14427 |  1063535 |
|   14434 |  1046580 |
|   13934 |   969148 |
|   14452 |   931821 |

#### Coluna: `dsc_instituicao`

| valor                   |      qtd |
|:------------------------|---------:|
| não mapeado (código -1) | 59822642 |
| não informado           |  6848337 |
| epay campanhas          |  6715082 |
| m4u/bemobi pix e 3ds    |  2317653 |
| dbr                     |  2205825 |
| mercado pago            |  1282998 |
| rv 31 nac               |  1063535 |
| dbr nac                 |  1046580 |
| cef/banco               |   969148 |
| [rd] controle facil     |   931821 |

#### Coluna: `dw_plano_tarifacao`

| valor   |      qtd |
|:--------|---------:|
| 541200  | 51407948 |
| 668900  | 12991511 |
| 607690  | 11035912 |
| 599100  |  7770371 |
| NULL    |  2105707 |
| 369889  |  2012002 |
| 567020  |  1904858 |
| 393401  |  1794019 |
| 606235  |  1034675 |
| 608480  |   962603 |

#### Coluna: `dsc_plano_tarifacao`

| valor                              |      qtd |
|:-----------------------------------|---------:|
| prezao diario                      | 59178319 |
| claro controle tradicional         | 12991511 |
| claro controle p                   | 11035912 |
| não informado                      |  2105707 |
| toda hora                          |  2012002 |
| claro controle conectado           |  1904858 |
| fala mais brasil por chamada bonus |  1794019 |
| pre pago jonava 1 - 15             |  1034675 |
| claro controle p - facil           |   962603 |
| pre pago jonava 16 - 30            |   553861 |

#### Coluna: `cod_plataforma_atu`

| valor   |      qtd |
|:--------|---------:|
| PREPG   | 64612093 |
| AUTOC   | 26785417 |
| FLEXD   |  2036784 |
| CTLFC   |  1915084 |
| POSPG   |    33606 |
| MVNOD   |     2012 |
| POSRI   |      510 |
| POSTL   |      368 |
| POSBL   |      280 |
| PRECN   |       53 |

#### Coluna: `dsc_plataforma_atu`

| valor                      |      qtd |
|:---------------------------|---------:|
| pré pago                   | 64612093 |
| controle                   | 26785417 |
| pré pago flex digital      |  2036784 |
| controle facil             |  1915084 |
| pós pago                   |    33606 |
| parceiros mvno digital     |     2012 |
| pós pago rio (apple watch) |      510 |
| telemetria                 |      368 |
| pós pago banda larga       |      280 |
| pré pago chip de nicho     |       53 |

#### Coluna: `cod_promocao`

| valor   |      qtd |
|:--------|---------:|
| -1      | 93280582 |
| NULL    |  2105707 |

#### Coluna: `dsc_promocao`

| valor                   |      qtd |
|:------------------------|---------:|
| não mapeado (código -1) | 93280582 |
| não informado           |  2105707 |

#### Coluna: `cod_status_plataforma`

| valor   |      qtd |
|:--------|---------:|
| A       | 91023397 |
| ZB1     |  4288738 |
| ZB2     |    35379 |
| -3      |    29219 |
| NDF     |     4487 |
| COL     |     2543 |
| PRE     |      673 |
| C       |      583 |
| ST      |      392 |
| U       |      287 |

#### Coluna: `dsc_status_plataforma`

| valor                |      qtd |
|:---------------------|---------:|
| ativo                | 91023397 |
| expirado 1           |  4288738 |
| expirado 2           |    35379 |
| nao informado        |    29219 |
| status nao definido  |     4487 |
| cooling              |     2543 |
| não informado        |      878 |
| pré-ativo            |      673 |
| desconectado         |      583 |
| suspensão temporária |      392 |

#### Coluna: `cod_tecnologia_dw`

| valor   |      qtd |
|:--------|---------:|
| GSM     | 95386289 |

#### Coluna: `dsc_tecnologia`

| valor   |      qtd |
|:--------|---------:|
| gsm     | 95386289 |

#### Coluna: `cod_tipo_credito`

| valor   |      qtd |
|:--------|---------:|
| PE      | 95386272 |
| CV      |       17 |

#### Coluna: `dsc_tipo_credito`

| valor          |      qtd |
|:---------------|---------:|
| online         | 95386272 |
| pin eletronico |       17 |

#### Coluna: `dw_tipo_insercao`

|   valor |      qtd |
|--------:|---------:|
|      -2 | 88731521 |
|       3 |  2738212 |
|      21 |  2735071 |
|      19 |   649720 |
|      99 |   531436 |
|      18 |      110 |
|      22 |       85 |
|       4 |       73 |
|       1 |       34 |
|      10 |       26 |

#### Coluna: `dsc_tipo_insercao`

| valor                                  |      qtd |
|:---------------------------------------|---------:|
| não determinado                        | 88731521 |
| não informado                          |  3266592 |
| pag. virtual                           |  2738212 |
| bônus dedicadas 4 e 5                  |   649720 |
| bônus dedicadas 3                      |      110 |
| franquia claro controle                |       73 |
| pag. cartão físico                     |       34 |
| pacote torpedo dacc                    |       26 |
| adicional claro controle-cartão físico |        1 |

#### Coluna: `dw_tipo_recarga`

| valor   |      qtd |
|:--------|---------:|
| -2      | 88731521 |
| 2       |  4548988 |
| NULL    |  2105707 |
| 1       |       73 |

#### Coluna: `dsc_tipo_recarga`

| valor                       |      qtd |
|:----------------------------|---------:|
| não determinado             | 88731521 |
| adicional do claro controle |  4548988 |
| não informado               |  2105707 |
| franquia do claro controle  |       73 |

#### Coluna: `cod_grupo_cartao`

| valor   |      qtd |
|:--------|---------:|
| UB      | 11705731 |
| WT      | 10777098 |
| PY      |  8736231 |
| I8      |  6002870 |
| UD      |  5983272 |
| UC      |  4248260 |
| IW      |  4187872 |
| -2      |  3551826 |
| G6      |  3531570 |
| AX      |  3276547 |

#### Coluna: `dsc_grupo_cartao_wpp`

| valor        |      qtd |
|:-------------|---------:|
| NaoSeAplica  | 57197348 |
| Rec.Online   | 27749988 |
| AtivPromocao |  6002874 |
| -2           |  3551826 |
| ForcaZB2     |   531436 |
| ChipPre+R$30 |   301565 |
| ChipPre+R$25 |    50465 |
| Pl. Controle |      241 |
| PCT LDN ILIM |      226 |
| Pacote SMS   |      136 |

#### Coluna: `dw_num_cliente`

|      valor |   qtd |
|-----------:|------:|
|         -2 | 13884 |
| 1139798979 |  2066 |
| 1145635585 |  1958 |
| 1389495657 |  1892 |
| 1164497165 |  1889 |
| 1161777754 |  1816 |
| 1403189723 |  1620 |
| 1437681817 |  1577 |
| 1189777104 |  1562 |
| 1415985368 |  1562 |

#### Coluna: `dw_num_ntc`

|     valor |   qtd |
|----------:|------:|
| 648397569 |  2080 |
| 652990493 |  1958 |
| 667413637 |  1896 |
| 729697471 |  1892 |
| 664947860 |  1820 |
| 739629381 |  1620 |
| 643133488 |  1612 |
| 763833967 |  1577 |
| 104291891 |  1562 |
| 748935078 |  1562 |

#### Coluna: `flag_sos`

| valor   |      qtd |
|:--------|---------:|
| false   | 88851918 |
| true    |  6534371 |

#### Coluna: `ind_metodo_pagamento`

| valor   |      qtd |
|:--------|---------:|
| A       | 95386241 |
| M       |       48 |

#### Coluna: `val_bonus`

|   valor |      qtd |
|--------:|---------:|
|       0 | 48152380 |
|       1 | 11280733 |
|      -1 |  9752422 |
|   84300 |  5462847 |
|   80500 |  2937448 |
|     390 |  2154750 |
|   10000 |  2030574 |
|   42200 |  1477772 |
|      -2 |  1418882 |
|   21100 |  1329618 |

#### Coluna: `val_credito_inserido`

|   valor |      qtd |
|--------:|---------:|
|       0 | 58911649 |
|      20 | 12120095 |
|      30 |  6050849 |
|      25 |  4262597 |
|       5 |  3953930 |
|      15 |  2950056 |
|      10 |  1890872 |
|      35 |  1221265 |
|      40 |   702861 |
|      12 |   632801 |

#### Coluna: `val_real`

|   valor |      qtd |
|--------:|---------:|
|       0 | 13938770 |
|      20 | 12221397 |
|       1 | 11809660 |
|      -1 | 10218793 |
|      30 |  6407102 |
|   84300 |  5462847 |
|       5 |  4431362 |
|      25 |  4331232 |
|   80500 |  3135835 |
|      15 |  3096652 |

#### Coluna: `valor_sos`

| valor   |      qtd |
|:--------|---------:|
| NULL    | 88851918 |
| 5.0     |  4092460 |
| 10.0    |  1629253 |
| 20.0    |   366640 |
| 15.0    |   324681 |
| 3.0     |   121337 |

#### Coluna: `ingestion_ts`

| valor                         |      qtd |
|:------------------------------|---------:|
| 2026-01-28 00:48:31.596268-03 | 95386289 |

#### Coluna: `run_id`

|    valor |      qtd |
|---------:|---------:|
| 20260128 | 95386289 |

#### Coluna: `ano_mes`

|   valor |     qtd |
|--------:|--------:|
|  202412 | 6927326 |
|  202411 | 6800420 |
|  202410 | 6480407 |
|  202501 | 6366515 |
|  202503 | 6096666 |
|  202502 | 6030903 |
|  202408 | 5557900 |
|  202409 | 5512580 |
|  202407 | 5257411 |
|  202406 | 4886421 |



---

