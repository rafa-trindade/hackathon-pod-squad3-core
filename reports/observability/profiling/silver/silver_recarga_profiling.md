# Relatório de Profiling: `silver/recarga` - `20260129`

### 🔑 Garantia de Unicidade: `silver/recarga`
- **Chave Técnica:** `num_cpf, dat_insercao_credito, hor_insercao_credito`
- **Tipo:** `COMPOSTA`

| coluna        |   distintos |   nulos |   duplicados | pct_nulos   | pct_duplicados   | cardinalidade   |
|:--------------|------------:|--------:|-------------:|:------------|:-----------------|:----------------|
| CHAVE_TECNICA |    95386289 |       0 |        60694 | 0.0%        | 0.06%            | ALTA            |

### 🚩 Diagnóstico e Observações Técnicas
* ⚠️ **Deduplicação Necessária:** Encontrados **60.694** (0.06%) duplicados reais.

---

### 📊 Schema e Estatísticas: `silver/recarga`
| column_name           | column_type              |   distintos |    nulos |   duplicados | pct_nulos   | pct_duplicados   | cardinalidade   |
|:----------------------|:-------------------------|------------:|---------:|-------------:|:------------|:-----------------|:----------------|
| num_cpf               | VARCHAR                  |     2746295 |        0 |     92700688 | 0.0%        | 97.12%           | MEDIA           |
| dw_num_ntc            | VARCHAR                  |     4144008 |        0 |     91302975 | 0.0%        | 95.66%           | MEDIA           |
| dat_insercao_credito  | DATE                     |         538 |        0 |     95446445 | 0.0%        | 100.0%           | BAIXA           |
| hor_insercao_credito  | BIGINT                   |       95082 |        0 |     95351901 | 0.0%        | 99.9%            | BAIXA           |
| cod_canal_aquisicao   | VARCHAR                  |         133 |        0 |     95446850 | 0.0%        | 100.0%           | BAIXA           |
| dsc_canal_aquisicao   | VARCHAR                  |         123 |        0 |     95446860 | 0.0%        | 100.0%           | BAIXA           |
| dw_forma_pagamento    | VARCHAR                  |           2 |        0 |     95446981 | 0.0%        | 100.0%           | BAIXA           |
| dsc_forma_pagamento   | VARCHAR                  |           2 |        0 |     95446981 | 0.0%        | 100.0%           | BAIXA           |
| dw_instituicao        | VARCHAR                  |         129 |        0 |     95446854 | 0.0%        | 100.0%           | BAIXA           |
| dsc_instituicao       | VARCHAR                  |         125 |        0 |     95446858 | 0.0%        | 100.0%           | BAIXA           |
| dw_plano_tarifacao    | VARCHAR                  |         104 |  2105750 |     95446879 | 2.21%       | 100.0%           | BAIXA           |
| dsc_plano_tarifacao   | VARCHAR                  |          79 |        0 |     95446904 | 0.0%        | 100.0%           | BAIXA           |
| cod_plataforma_atu    | VARCHAR                  |          13 |        0 |     95446970 | 0.0%        | 100.0%           | BAIXA           |
| dsc_plataforma_atu    | VARCHAR                  |          13 |        0 |     95446970 | 0.0%        | 100.0%           | BAIXA           |
| cod_promocao          | VARCHAR                  |           1 |  2105750 |     95446982 | 2.21%       | 100.0%           | BAIXA           |
| dsc_promocao          | VARCHAR                  |           2 |        0 |     95446981 | 0.0%        | 100.0%           | BAIXA           |
| cod_status_plataforma | VARCHAR                  |          17 |        0 |     95446966 | 0.0%        | 100.0%           | BAIXA           |
| dsc_status_plataforma | VARCHAR                  |           9 |        0 |     95446974 | 0.0%        | 100.0%           | BAIXA           |
| cod_tecnologia_dw     | VARCHAR                  |           1 |        0 |     95446982 | 0.0%        | 100.0%           | BAIXA           |
| dsc_tecnologia        | VARCHAR                  |           1 |        0 |     95446982 | 0.0%        | 100.0%           | BAIXA           |
| cod_tipo_credito      | VARCHAR                  |           2 |        0 |     95446981 | 0.0%        | 100.0%           | BAIXA           |
| dsc_tipo_credito      | VARCHAR                  |           2 |        0 |     95446981 | 0.0%        | 100.0%           | BAIXA           |
| dw_tipo_insercao      | VARCHAR                  |          11 |        0 |     95446972 | 0.0%        | 100.0%           | BAIXA           |
| dsc_tipo_insercao     | VARCHAR                  |           7 |        0 |     95446976 | 0.0%        | 100.0%           | BAIXA           |
| dw_tipo_recarga       | VARCHAR                  |           3 |  2105750 |     95446980 | 2.21%       | 100.0%           | BAIXA           |
| dsc_tipo_recarga      | VARCHAR                  |           4 |        0 |     95446979 | 0.0%        | 100.0%           | BAIXA           |
| cod_grupo_cartao      | VARCHAR                  |         240 |        0 |     95446743 | 0.0%        | 100.0%           | BAIXA           |
| dsc_grupo_cartao_wpp  | VARCHAR                  |          25 |        0 |     95446958 | 0.0%        | 100.0%           | BAIXA           |
| dw_num_cliente        | VARCHAR                  |     6245708 |        0 |     89201275 | 0.0%        | 93.46%           | ALTA            |
| flag_sos              | BOOLEAN                  |           2 |        0 |     95446981 | 0.0%        | 100.0%           | BAIXA           |
| ind_metodo_pagamento  | VARCHAR                  |           2 |        0 |     95446981 | 0.0%        | 100.0%           | BAIXA           |
| val_bonus             | DOUBLE                   |       65011 |        0 |     95381972 | 0.0%        | 99.93%           | BAIXA           |
| val_credito_inserido  | DOUBLE                   |        4613 |        0 |     95442370 | 0.0%        | 100.0%           | BAIXA           |
| val_real              | DOUBLE                   |       50763 |        0 |     95396220 | 0.0%        | 99.95%           | BAIXA           |
| valor_sos             | DOUBLE                   |           5 | 88912606 |     95446978 | 93.15%      | 100.0%           | BAIXA           |
| ingestion_ts          | TIMESTAMP WITH TIME ZONE |           1 |        0 |     95446982 | 0.0%        | 100.0%           | BAIXA           |
| run_id                | BIGINT                   |           1 |        0 |     95446982 | 0.0%        | 100.0%           | BAIXA           |
| ano_mes               | BIGINT                   |          20 |        0 |     95446963 | 0.0%        | 100.0%           | BAIXA           |

---

### 📦 Volumetria: `silver/recarga`
| diretorio      |   qtd_arquivos | registros   |   colunas |   tamanho_comprimido_mib |   tamanho_descomprimido_mib |
|:---------------|---------------:|:------------|----------:|-------------------------:|----------------------------:|
| ano_mes=202310 |              1 | 4.183.529   |        38 |                   114.44 |                      251.04 |
| ano_mes=202311 |              1 | 4.154.299   |        38 |                   114.7  |                      249.82 |
| ano_mes=202312 |              1 | 4.441.681   |        38 |                   121.11 |                      267.1  |
| ano_mes=202401 |              1 | 4.239.814   |        38 |                   116.75 |                      255.31 |
| ano_mes=202402 |              1 | 4.255.167   |        38 |                   118.27 |                      256.13 |
| ano_mes=202403 |              1 | 4.737.973   |        38 |                   129.47 |                      285.25 |
| ano_mes=202404 |              1 | 4.642.953   |        38 |                   126.75 |                      277.98 |
| ano_mes=202405 |              1 | 4.824.433   |        38 |                   131.5  |                      289.29 |
| ano_mes=202406 |              1 | 4.890.073   |        38 |                   133.62 |                      290.93 |
| ano_mes=202407 |              1 | 5.261.577   |        38 |                   144    |                      313.93 |
| ano_mes=202408 |              1 | 5.562.251   |        38 |                   150.88 |                      330.92 |
| ano_mes=202409 |              1 | 5.516.156   |        38 |                   149.91 |                      328.29 |
| ano_mes=202410 |              1 | 6.485.048   |        38 |                   172.1  |                      386.55 |
| ano_mes=202411 |              1 | 6.805.308   |        38 |                   181.59 |                      406.36 |
| ano_mes=202412 |              1 | 6.933.990   |        38 |                   183.82 |                      413.33 |
| ano_mes=202501 |              1 | 6.373.215   |        38 |                   168.75 |                      379.51 |
| ano_mes=202502 |              1 | 6.038.001   |        38 |                   159.69 |                      359.24 |
| ano_mes=202503 |              1 | 6.101.515   |        38 |                   160.26 |                      363.7  |
| TOTAL          |             18 | 95.446.983  |        38 |                  2577.63 |                     5704.65 |

---

### 📅 Range de Datas: `silver/recarga`
#### Coluna: `dat_insercao_credito`
| min                        | max                        |
|:---------------------------|:---------------------------|
| 2023-10-01T00:00:00.000000 | 2025-03-31T00:00:00.000000 |

#### Coluna: `ingestion_ts`
| min                              | max                              |
|:---------------------------------|:---------------------------------|
| 2026-01-29 01:44:41.030686-03:00 | 2026-01-29 01:44:41.030686-03:00 |



---

### 🔢 Range de Valores Numéricos: `silver/recarga`

#### Coluna: `hor_insercao_credito`
|   min |    max |   media |
|------:|-------:|--------:|
|     0 | 235959 |  108790 |

#### Coluna: `val_bonus`
|      min |   max |   media |
|---------:|------:|--------:|
| -87895.2 | 95500 | 10350.1 |

#### Coluna: `val_credito_inserido`
|   min |   max |   media |
|------:|------:|--------:|
|     0 | 25000 |    8.45 |

#### Coluna: `val_real`
|      min |   max |   media |
|---------:|------:|--------:|
| -87895.2 | 95500 | 10358.5 |

#### Coluna: `valor_sos`
|   min |   max |   media |
|------:|------:|--------:|
|     3 |    20 |    7.55 |



---

### 🔟 Distribuição de Valores (Top 10): `silver/recarga`
#### Coluna: `num_cpf`

| valor       |   qtd |
|:------------|------:|
| XYT9U8X778W |  3922 |
| ZW797ZWZYT8 |  3292 |
| Z9YXUZYU7WX |  2875 |
| Z9WWUTT77XZ |  2806 |
| UUWUWZXX879 |  2804 |
| Z78YXX78YX7 |  2747 |
| ZX9YWXZT779 |  2501 |
| XZNYZZNU7ZN |  2500 |
| X8YXWUN97XY |  2497 |
| XYYTXUWTTXU |  2456 |

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
| 763833967 |  1579 |
| 748935078 |  1562 |
| 104291891 |  1562 |

#### Coluna: `dat_insercao_credito`

| valor      |    qtd |
|:-----------|-------:|
| 2025-03-21 | 519941 |
| 2025-02-21 | 433010 |
| 2025-02-03 | 415436 |
| 2024-12-04 | 414221 |
| 2025-01-03 | 397080 |
| 2025-03-03 | 396452 |
| 2025-01-21 | 395683 |
| 2024-12-21 | 374368 |
| 2024-12-03 | 358450 |
| 2025-02-22 | 352665 |

#### Coluna: `hor_insercao_credito`

|   valor |   qtd |
|--------:|------:|
|   54211 |  9155 |
|   54204 |  9142 |
|   54207 |  9122 |
|   54209 |  9095 |
|   54208 |  9037 |
|   54212 |  9019 |
|   54203 |  8971 |
|   54210 |  8957 |
|   54205 |  8932 |
|   54206 |  8902 |

#### Coluna: `cod_canal_aquisicao`

|   valor |      qtd |
|--------:|---------:|
|      -3 | 60195293 |
|   16307 |  6667899 |
|      -2 |  6175355 |
|   17627 |  2328681 |
|   17537 |  2249874 |
|   16357 |  1269202 |
|   16167 |  1100520 |
|   16187 |  1057996 |
|   15987 |  1042127 |
|   17621 |  1008240 |

#### Coluna: `dsc_canal_aquisicao`

| valor                |      qtd |
|:---------------------|---------:|
| ni                   | 60195293 |
| epay campanhas       |  6667899 |
| nd                   |  6175355 |
| m4u/bemobi pix e 3ds |  2328681 |
| dbr                  |  2249874 |
| mercado pago         |  1269202 |
| rv 11                |  1100520 |
| rv 31 nac            |  1057996 |
| tendencia nac        |  1042127 |
| [rd] controle facil  |  1008240 |

#### Coluna: `dw_forma_pagamento`

|   valor |      qtd |
|--------:|---------:|
|      -2 | 93341233 |
|      10 |  2105750 |

#### Coluna: `dsc_forma_pagamento`

| valor            |      qtd |
|:-----------------|---------:|
| não determinado  | 93341233 |
| pagamento online |  2105750 |

#### Coluna: `dw_instituicao`

|   valor |      qtd |
|--------:|---------:|
|      -1 | 59879620 |
|   14433 |  6715137 |
|      -2 |  6584802 |
|   14472 |  2317671 |
|   14475 |  2205838 |
|   14211 |  1283014 |
|   14427 |  1063612 |
|   14434 |  1047755 |
|   13934 |   969156 |
|   14452 |   932084 |

#### Coluna: `dsc_instituicao`

| valor                   |      qtd |
|:------------------------|---------:|
| não mapeado (código -1) | 59879620 |
| não informado           |  6849477 |
| epay campanhas          |  6715137 |
| m4u/bemobi pix e 3ds    |  2317671 |
| dbr                     |  2205838 |
| mercado pago            |  1283014 |
| rv 31 nac               |  1063612 |
| dbr nac                 |  1047755 |
| cef/banco               |   969156 |
| [rd] controle facil     |   932084 |

#### Coluna: `dw_plano_tarifacao`

| valor   |      qtd |
|:--------|---------:|
| 541200  | 51416786 |
| 668900  | 13012350 |
| 607690  | 11058738 |
| 599100  |  7772454 |
| NULL    |  2105750 |
| 369889  |  2012412 |
| 567020  |  1908180 |
| 393401  |  1794419 |
| 606235  |  1034827 |
| 608480  |   962877 |

#### Coluna: `dsc_plano_tarifacao`

| valor                              |      qtd |
|:-----------------------------------|---------:|
| prezao diario                      | 59189240 |
| claro controle tradicional         | 13012350 |
| claro controle p                   | 11058738 |
| não informado                      |  2105750 |
| toda hora                          |  2012412 |
| claro controle conectado           |  1908180 |
| fala mais brasil por chamada bonus |  1794419 |
| pre pago jonava 1 - 15             |  1034827 |
| claro controle p - facil           |   962877 |
| pre pago jonava 16 - 30            |   553932 |

#### Coluna: `cod_plataforma_atu`

| valor   |      qtd |
|:--------|---------:|
| PREPG   | 64624116 |
| AUTOC   | 26833544 |
| FLEXD   |  2036824 |
| CTLFC   |  1915552 |
| POSPG   |    33641 |
| MVNOD   |     2012 |
| POSRI   |      511 |
| POSTL   |      368 |
| POSBL   |      280 |
| PRECN   |       53 |

#### Coluna: `dsc_plataforma_atu`

| valor                      |      qtd |
|:---------------------------|---------:|
| pré pago                   | 64624116 |
| controle                   | 26833544 |
| pré pago flex digital      |  2036824 |
| controle facil             |  1915552 |
| pós pago                   |    33641 |
| parceiros mvno digital     |     2012 |
| pós pago rio (apple watch) |      511 |
| telemetria                 |      368 |
| pós pago banda larga       |      280 |
| pré pago chip de nicho     |       53 |

#### Coluna: `cod_promocao`

| valor   |      qtd |
|:--------|---------:|
| -1      | 93341233 |
| NULL    |  2105750 |

#### Coluna: `dsc_promocao`

| valor                   |      qtd |
|:------------------------|---------:|
| não mapeado (código -1) | 93341233 |
| não informado           |  2105750 |

#### Coluna: `cod_status_plataforma`

| valor   |      qtd |
|:--------|---------:|
| A       | 91082403 |
| ZB1     |  4290259 |
| ZB2     |    35381 |
| -3      |    29383 |
| NDF     |     4487 |
| COL     |     2543 |
| PRE     |      674 |
| C       |      583 |
| ST      |      392 |
| U       |      287 |

#### Coluna: `dsc_status_plataforma`

| valor                |      qtd |
|:---------------------|---------:|
| ativo                | 91082403 |
| expirado 1           |  4290259 |
| expirado 2           |    35381 |
| nao informado        |    29383 |
| status nao definido  |     4487 |
| cooling              |     2543 |
| não informado        |      878 |
| pré-ativo            |      674 |
| desconectado         |      583 |
| suspensão temporária |      392 |

#### Coluna: `cod_tecnologia_dw`

| valor   |      qtd |
|:--------|---------:|
| GSM     | 95446983 |

#### Coluna: `dsc_tecnologia`

| valor   |      qtd |
|:--------|---------:|
| gsm     | 95446983 |

#### Coluna: `cod_tipo_credito`

| valor   |      qtd |
|:--------|---------:|
| PE      | 95446966 |
| CV      |       17 |

#### Coluna: `dsc_tipo_credito`

| valor          |      qtd |
|:---------------|---------:|
| online         | 95446966 |
| pin eletronico |       17 |

#### Coluna: `dw_tipo_insercao`

|   valor |      qtd |
|--------:|---------:|
|      -2 | 88790368 |
|       3 |  2738540 |
|      21 |  2736570 |
|      19 |   649733 |
|      99 |   531445 |
|      18 |      110 |
|      22 |       83 |
|       4 |       73 |
|       1 |       34 |
|      10 |       26 |

#### Coluna: `dsc_tipo_insercao`

| valor                                  |      qtd |
|:---------------------------------------|---------:|
| não determinado                        | 88790368 |
| não informado                          |  3268098 |
| pag. virtual                           |  2738540 |
| bônus dedicadas 4 e 5                  |   649733 |
| bônus dedicadas 3                      |      110 |
| franquia claro controle                |       73 |
| pag. cartão físico                     |       34 |
| pacote torpedo dacc                    |       26 |
| adicional claro controle-cartão físico |        1 |

#### Coluna: `dw_tipo_recarga`

| valor   |      qtd |
|:--------|---------:|
| -2      | 88790368 |
| 2       |  4550792 |
| NULL    |  2105750 |
| 1       |       73 |

#### Coluna: `dsc_tipo_recarga`

| valor                       |      qtd |
|:----------------------------|---------:|
| não determinado             | 88790368 |
| adicional do claro controle |  4550792 |
| não informado               |  2105750 |
| franquia do claro controle  |       73 |

#### Coluna: `cod_grupo_cartao`

| valor   |      qtd |
|:--------|---------:|
| UB      | 11706202 |
| WT      | 10796473 |
| PY      |  8741861 |
| I8      |  6003031 |
| UD      |  5983792 |
| UC      |  4248635 |
| IW      |  4193807 |
| -2      |  3552837 |
| G6      |  3532462 |
| AX      |  3276551 |

#### Coluna: `dsc_grupo_cartao_wpp`

| valor        |      qtd |
|:-------------|---------:|
| NaoSeAplica  | 57255463 |
| Rec.Online   | 27752145 |
| AtivPromocao |  6003035 |
| -2           |  3552837 |
| ForcaZB2     |   531445 |
| ChipPre+R$30 |   301218 |
| ChipPre+R$25 |    50054 |
| Pl. Controle |      241 |
| PCT LDN ILIM |      227 |
| Pacote SMS   |      136 |

#### Coluna: `dw_num_cliente`

|      valor |   qtd |
|-----------:|------:|
|         -2 | 13889 |
| 1139798979 |  2066 |
| 1145635585 |  1958 |
| 1389495657 |  1892 |
| 1164497165 |  1889 |
| 1161777754 |  1816 |
| 1403189723 |  1620 |
| 1437681817 |  1579 |
| 1415985368 |  1562 |
| 1189777104 |  1562 |

#### Coluna: `flag_sos`

| valor   |      qtd |
|:--------|---------:|
| false   | 88912606 |
| true    |  6534377 |

#### Coluna: `ind_metodo_pagamento`

| valor   |      qtd |
|:--------|---------:|
| A       | 95446935 |
| M       |       48 |

#### Coluna: `val_bonus`

|   valor |      qtd |
|--------:|---------:|
|       0 | 48157373 |
|       1 | 11301967 |
|      -1 |  9771253 |
|   84300 |  5467038 |
|   80500 |  2940985 |
|     390 |  2155428 |
|   10000 |  2030657 |
|   42200 |  1478498 |
|      -2 |  1418897 |
|   21100 |  1330043 |

#### Coluna: `val_credito_inserido`

|   valor |      qtd |
|--------:|---------:|
|       0 | 58970469 |
|      20 | 12120564 |
|      30 |  6051380 |
|      25 |  4262972 |
|       5 |  3953932 |
|      15 |  2950461 |
|      10 |  1890118 |
|      35 |  1221304 |
|      40 |   702896 |
|      12 |   633086 |

#### Coluna: `val_real`

|   valor |      qtd |
|--------:|---------:|
|       0 | 13941587 |
|      20 | 12221885 |
|       1 | 11831058 |
|      -1 | 10237775 |
|      30 |  6407290 |
|   84300 |  5467038 |
|       5 |  4431386 |
|      25 |  4331243 |
|   80500 |  3139419 |
|      15 |  3097175 |

#### Coluna: `valor_sos`

| valor   |      qtd |
|:--------|---------:|
| NULL    | 88912606 |
| 5.0     |  4092461 |
| 10.0    |  1629257 |
| 20.0    |   366639 |
| 15.0    |   324682 |
| 3.0     |   121338 |

#### Coluna: `ingestion_ts`

| valor                         |      qtd |
|:------------------------------|---------:|
| 2026-01-29 01:44:41.030686-03 | 95446983 |

#### Coluna: `run_id`

|    valor |      qtd |
|---------:|---------:|
| 20260129 | 95446983 |

#### Coluna: `ano_mes`

|   valor |     qtd |
|--------:|--------:|
|  202412 | 6933990 |
|  202411 | 6805308 |
|  202410 | 6485048 |
|  202501 | 6373215 |
|  202503 | 6101515 |
|  202502 | 6038001 |
|  202408 | 5562251 |
|  202409 | 5516156 |
|  202407 | 5261577 |
|  202406 | 4890073 |



---

