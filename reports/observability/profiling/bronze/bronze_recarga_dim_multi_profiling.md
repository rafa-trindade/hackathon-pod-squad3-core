# Relatório de Profiling: `bronze/recarga_dim`

## 📄 Arquivo: `canal_aquisicao_credito.parquet`

#### 📦 Volumetria - `canal_aquisicao_credito.parquet`

| Arquivo | Registros | Colunas |
| :--- | :--- | :--- |
| canal_aquisicao_credito.parquet | 5.899 | 3 |


---

#### 🔍 Amostra de Dados (Head 20)  - `canal_aquisicao_credito.parquet`

|   cod_canal_aquisicao | dsc_canal_aquisicao        | cod_tipo_credito_aquisicao   |
|----------------------:|:---------------------------|:-----------------------------|
|                 14929 | ss/aa ebv - golfe telecom  | CV                           |
|                 14930 | ss/aa ebv - marajo comerci | CV                           |
|                 14931 | ss/aa concel               | CV                           |
|                 14932 | ss/aa virtual celulares    | CV                           |
|                 14933 | ss/aa portocel             | CV                           |
|                 14934 | ss/aa mv celulares         | CV                           |
|                 14935 | ss/aa falecom              | CV                           |
|                 14936 | ss/aa cell work            | CV                           |
|                 14937 | ss/aa ccv informatica      | CV                           |
|                 14938 | ss/aa eletro aurora        | CV                           |
|                 14939 | ss/aa ole celulares        | CV                           |
|                 14940 | ss/aa radio luz            | CV                           |
|                 14941 | ss/aa eskinao              | CV                           |
|                 14942 | ss/aa radio luz            | CV                           |
|                 14943 | ss/aa radio luz            | CV                           |
|                 14944 | ss/aa radio luz            | CV                           |
|                 14945 | ss/aa cpm celulares        | CV                           |
|                 14946 | ss/aa lusa celulares       | CV                           |
|                 14947 | ss/aa comercial bernardi   | CV                           |
|                 14948 | ss/aa clarocel             | CV                           |

---

#### 📊 Estatísticas e Tipagem  - `canal_aquisicao_credito.parquet`

| coluna                     | tipo    |   distintos |   nulos | pct_distintos   | pct_nulos   | cardinalidade   |
|:---------------------------|:--------|------------:|--------:|:----------------|:------------|:----------------|
| cod_canal_aquisicao        | VARCHAR |        5899 |       0 | 100.0%          | 0.0%        | ALTA            |
| dsc_canal_aquisicao        | VARCHAR |        4232 |       0 | 71.74%          | 0.0%        | ALTA            |
| cod_tipo_credito_aquisicao | VARCHAR |           3 |     294 | 0.05%           | 4.98%       | BAIXA           |

---

## 📄 Arquivo: `forma_pagamento.parquet`

#### 📦 Volumetria - `forma_pagamento.parquet`

| Arquivo | Registros | Colunas |
| :--- | :--- | :--- |
| forma_pagamento.parquet | 9 | 3 |


---

#### 🔍 Amostra de Dados (Head 20)  - `forma_pagamento.parquet`

|   dw_forma_pagamento | dsc_forma_pagamento   | desc_cod_forma_pagamento   |
|---------------------:|:----------------------|:---------------------------|
|                   -1 | não se aplica         | -1                         |
|                   -2 | não determinado       | -2                         |
|                   -3 | não informado         | -3                         |
|                   11 | credito de prepago    | CP                         |
|                   12 | debito direto         | DD                         |
|                   13 | pagamento manual      | MP                         |
|                   14 | arrecadacao bancaria  | PB                         |
|                   10 | pagamento online      | CA                         |
|                   15 | acordo de pagamento   | PA                         |

---

#### 📊 Estatísticas e Tipagem  - `forma_pagamento.parquet`

| coluna                   | tipo    |   distintos |   nulos | pct_distintos   | pct_nulos   | cardinalidade   |
|:-------------------------|:--------|------------:|--------:|:----------------|:------------|:----------------|
| dw_forma_pagamento       | VARCHAR |           9 |       0 | 100.0%          | 0.0%        | ALTA            |
| dsc_forma_pagamento      | VARCHAR |           9 |       0 | 100.0%          | 0.0%        | ALTA            |
| desc_cod_forma_pagamento | VARCHAR |           9 |       0 | 100.0%          | 0.0%        | ALTA            |

---

## 📄 Arquivo: `instituicao.parquet`

#### 📦 Volumetria - `instituicao.parquet`

| Arquivo | Registros | Colunas |
| :--- | :--- | :--- |
| instituicao.parquet | 550 | 5 |


---

#### 🔍 Amostra de Dados (Head 20)  - `instituicao.parquet`

|   dw_instituicao |   cod_instituicao | dsc_instituicao             |   cod_tipo_instituicao | dsc_tipo_instituicao   |
|-----------------:|------------------:|:----------------------------|-----------------------:|:-----------------------|
|            13926 |               416 | banco inter                 |                      1 | banco                  |
|            13927 |               490 | mwallet/bradesco            |                      1 | banco                  |
|            13928 |               514 | santander/c.bancario        |                      1 | banco                  |
|            13929 |                24 | cef/c.bancario              |                      1 | banco                  |
|            13930 |                69 | lemon bank                  |                      1 | banco                  |
|            13931 |                49 | tribanco                    |                      1 | banco                  |
|            13932 |                38 | santander-banespa           |                      1 | banco                  |
|            13933 |                33 | banrisul                    |                      1 | banco                  |
|            13934 |                25 | cef/banco                   |                      1 | banco                  |
|            13935 |                56 | hsbc                        |                      1 | banco                  |
|            13936 |                14 | ic/citibank                 |                      1 | banco                  |
|            13937 |                13 | nossa caixa                 |                      1 | banco                  |
|            13938 |                 8 | citibank                    |                      1 | banco                  |
|            13939 |                 7 | banco do brasil             |                      1 | banco                  |
|            13940 |                 4 | abn amro bank               |                      1 | banco                  |
|            13941 |                 3 | unibanco                    |                      1 | banco                  |
|            13942 |                 2 | itau                        |                      1 | banco                  |
|            13943 |                 1 | bradesco                    |                      1 | banco                  |
|            13944 |               425 | m4u controle facil boleto 3 |                      2 | venda direta           |
|            13945 |               424 | m4u controle facil boleto 2 |                      2 | venda direta           |

---

#### 📊 Estatísticas e Tipagem  - `instituicao.parquet`

| coluna               | tipo    |   distintos |   nulos | pct_distintos   | pct_nulos   | cardinalidade   |
|:---------------------|:--------|------------:|--------:|:----------------|:------------|:----------------|
| dw_instituicao       | VARCHAR |         550 |       0 | 100.0%          | 0.0%        | ALTA            |
| cod_instituicao      | VARCHAR |         550 |       0 | 100.0%          | 0.0%        | ALTA            |
| dsc_instituicao      | VARCHAR |         550 |       0 | 100.0%          | 0.0%        | ALTA            |
| cod_tipo_instituicao | VARCHAR |          11 |       0 | 2.0%            | 0.0%        | MEDIA           |
| dsc_tipo_instituicao | VARCHAR |          11 |       0 | 2.0%            | 0.0%        | MEDIA           |

---

## 📄 Arquivo: `plano_preco.parquet`

#### 📦 Volumetria - `plano_preco.parquet`

| Arquivo | Registros | Colunas |
| :--- | :--- | :--- |
| plano_preco.parquet | 293.743 | 18 |


---

#### 🔍 Amostra de Dados (Head 20)  - `plano_preco.parquet`

|   dw_plano_tarifacao |   cod_plano_preco | dsc_plano_tarifacao            |   cod_tipo_cliente |   dw_tipo_cliente | dat_efetivacao   | dsc_plano_preco_bi          |   dsc_grupo_plano_bi |   dsc_tipo_plano_bi | ind_amdocs_plat_pre   |   cod_tratamento_especial | num_franquia_minutos_bi   | num_franquia_reais_bi   | num_franquia_eventos_bi   | num_franquia_volume_bi   |   cod_plano_componente | dsc_plano_preco_unico_bi   | dsc_modalidade_plano   |
|---------------------:|------------------:|:-------------------------------|-------------------:|------------------:|:-----------------|:----------------------------|---------------------:|--------------------:|:----------------------|--------------------------:|:--------------------------|:------------------------|:--------------------------|:-------------------------|-----------------------:|:---------------------------|:-----------------------|
|               533477 |          50029231 | licitac?o marinha do brasil    |                 -1 |                -1 | NaT              | -3                          |                   -3 |                  -3 | a                     |                        -1 |                           |                         |                           |                          |               50029231 |                            |                        |
|               601796 |          50029231 | licitação marinha do brasil    |                 -1 |                -1 | NaT              | -3                          |                   -3 |                  -3 | a                     |                        -1 |                           |                         |                           |                          |               50029231 | -3                         |                        |
|               548887 |          50029231 | licitac?o marinha do brasil    |                 -1 |                -1 | NaT              | -3                          |                   -3 |                  -3 | a                     |                        -1 |                           |                         |                           |                          |               50029231 |                            |                        |
|               535237 |          50029231 | licitac?o marinha do brasil    |                 -1 |                -1 | NaT              | -3                          |                   -3 |                  -3 | a                     |                        -1 |                           |                         |                           |                          |               50029231 |                            |                        |
|               536107 |          50029231 | licitac?o marinha do brasil    |                 -1 |                -1 | NaT              | -3                          |                   -3 |                  -3 | a                     |                        -1 |                           |                         |                           |                          |               50029231 |                            |                        |
|               537347 |          50029231 | licitac?o marinha do brasil    |                 -1 |                -1 | NaT              | -3                          |                   -3 |                  -3 | a                     |                        -1 |                           |                         |                           |                          |               50029231 |                            |                        |
|               393144 |          50029231 | licitac?o marinha do brasil    |                 -1 |                -1 | NaT              | licitac?o                   |                   -3 |                  -3 | a                     |                        -1 |                           |                         |                           |                          |               50029231 | outros                     |                        |
|               554107 |          50029231 | licitac?o marinha do brasil    |                 -1 |                -1 | NaT              | -3                          |                   -3 |                  -3 | a                     |                        -1 |                           |                         |                           |                          |               50029231 |                            |                        |
|               538627 |          50029231 | licitac?o marinha do brasil    |                 -1 |                -1 | NaT              | -3                          |                   -3 |                  -3 | a                     |                        -1 |                           |                         |                           |                          |               50029231 |                            |                        |
|               547957 |          50029231 | licitac?o marinha do brasil    |                 -1 |                -1 | NaT              | -3                          |                   -3 |                  -3 | a                     |                        -1 |                           |                         |                           |                          |               50029231 |                            |                        |
|               545277 |          50029231 | licitac?o marinha do brasil    |                 -1 |                -1 | NaT              | -3                          |                   -3 |                  -3 | a                     |                        -1 |                           |                         |                           |                          |               50029231 |                            |                        |
|               539477 |          50029231 | licitac?o marinha do brasil    |                 -1 |                -1 | NaT              | -3                          |                   -3 |                  -3 | a                     |                        -1 |                           |                         |                           |                          |               50029231 |                            |                        |
|               540427 |          50029231 | licitac?o marinha do brasil    |                 -1 |                -1 | NaT              | -3                          |                   -3 |                  -3 | a                     |                        -1 |                           |                         |                           |                          |               50029231 |                            |                        |
|               550997 |          50029231 | licitac?o marinha do brasil    |                 -1 |                -1 | NaT              | -3                          |                   -3 |                  -3 | a                     |                        -1 |                           |                         |                           |                          |               50029231 |                            |                        |
|               523427 |          50029231 | licitac?o marinha do brasil    |                 -1 |                -1 | NaT              | licitac?o marinha do brasil |                   -3 |                  -3 | a                     |                        -1 |                           |                         |                           |                          |               50029231 | outros                     |                        |
|               532247 |          50029231 | licitac?o marinha do brasil    |                 -1 |                -1 | NaT              | -3                          |                   -3 |                  -3 | a                     |                        -1 |                           |                         |                           |                          |               50029231 |                            |                        |
|               549927 |          50029231 | licitac?o marinha do brasil    |                 -1 |                -1 | NaT              | -3                          |                   -3 |                  -3 | a                     |                        -1 |                           |                         |                           |                          |               50029231 |                            |                        |
|               546657 |          50029231 | licitac?o marinha do brasil    |                 -1 |                -1 | NaT              | -3                          |                   -3 |                  -3 | a                     |                        -1 |                           |                         |                           |                          |               50029231 |                            |                        |
|               696318 |          50029241 | licitacao min da educacao      |                 -1 |                -1 | NaT              | -3                          |                   -3 |                  -3 | a                     |                        -1 |                           |                         |                           |                          |               50029241 |                            |                        |
|               696319 |          50029251 | licitacao min des combate fome |                 -1 |                -1 | NaT              | -3                          |                   -3 |                  -3 | a                     |                        -1 |                           |                         |                           |                          |               50029251 |                            |                        |

---

#### 📊 Estatísticas e Tipagem  - `plano_preco.parquet`

| coluna                   | tipo    |   distintos |   nulos | pct_distintos   | pct_nulos   | cardinalidade   |
|:-------------------------|:--------|------------:|--------:|:----------------|:------------|:----------------|
| dw_plano_tarifacao       | VARCHAR |      293743 |       0 | 100.0%          | 0.0%        | ALTA            |
| cod_plano_preco          | VARCHAR |       13490 |       0 | 4.59%           | 0.0%        | MEDIA           |
| dsc_plano_tarifacao      | VARCHAR |       41929 |       0 | 14.27%          | 0.0%        | ALTA            |
| cod_tipo_cliente         | VARCHAR |           9 |       0 | 0.0%            | 0.0%        | BAIXA           |
| dw_tipo_cliente          | VARCHAR |          97 |       0 | 0.03%           | 0.0%        | BAIXA           |
| dat_efetivacao           | DATE    |           0 |  293743 | 0.0%            | 100.0%      | BAIXA           |
| dsc_plano_preco_bi       | VARCHAR |        2469 |       0 | 0.84%           | 0.0%        | MEDIA           |
| dsc_grupo_plano_bi       | VARCHAR |          30 |       0 | 0.01%           | 0.0%        | BAIXA           |
| dsc_tipo_plano_bi        | VARCHAR |           9 |       0 | 0.0%            | 0.0%        | BAIXA           |
| ind_amdocs_plat_pre      | VARCHAR |           3 |       0 | 0.0%            | 0.0%        | BAIXA           |
| cod_tratamento_especial  | VARCHAR |           4 |       0 | 0.0%            | 0.0%        | BAIXA           |
| num_franquia_minutos_bi  | VARCHAR |           0 |  293743 | 0.0%            | 100.0%      | BAIXA           |
| num_franquia_reais_bi    | VARCHAR |           0 |  293743 | 0.0%            | 100.0%      | BAIXA           |
| num_franquia_eventos_bi  | VARCHAR |           0 |  293743 | 0.0%            | 100.0%      | BAIXA           |
| num_franquia_volume_bi   | VARCHAR |           0 |  293743 | 0.0%            | 100.0%      | BAIXA           |
| cod_plano_componente     | VARCHAR |        6259 |  124730 | 2.13%           | 42.46%      | MEDIA           |
| dsc_plano_preco_unico_bi | VARCHAR |         100 |  110147 | 0.03%           | 37.5%       | BAIXA           |
| dsc_modalidade_plano     | VARCHAR |           0 |  293743 | 0.0%            | 100.0%      | BAIXA           |

---

## 📄 Arquivo: `plataforma.parquet`

#### 📦 Volumetria - `plataforma.parquet`

| Arquivo | Registros | Colunas |
| :--- | :--- | :--- |
| plataforma.parquet | 28 | 4 |


---

#### 🔍 Amostra de Dados (Head 20)  - `plataforma.parquet`

| cod_plataforma_atu   | dsc_plataforma_atu         | cod_grupo_plataforma   | dsc_grupo_plataforma   |
|:---------------------|:---------------------------|:-----------------------|:-----------------------|
| M2MS                 | machine to machine special | POSTL                  | telemetria             |
| MVNOD                | parceiros mvno digital     | MVNO                   | mvno digital           |
| POSTL                | telemetria                 | POSTL                  | telemetria             |
| POSDT                | pós pago deutsche telekom  | POSPG                  | telemetria             |
| FLEXD                | pré pago flex digital      | PREPG                  | pós pago               |
| MVNO                 | parceiros mvno             | MVNO                   | telemetria             |
| -1                   | não se aplica              | NA                     | outros                 |
| -2                   | não definido               | ND                     | outros                 |
| -3                   | não informado              | NI                     | outros                 |
| PREPG                | pré pago                   | PREPG                  | pré pago               |
| POSPG                | pós pago                   | POSPG                  | pós pago               |
| AUTOC                | controle                   | AUTOC                  | controle               |
| PRERO                | pré pago roaming           | PREPG                  | pré pago               |
| VROAM                | visitante nacional         | VROAM                  | outros                 |
| VRINT                | visitante internacional    | VRINT                  | outros                 |
| POSCM                | comunicação multimídia     | POSPG                  | pós pago               |
| POSFX                | nr fixo combo fixo         | POSPG                  | pós pago               |
| POSBL                | pós pago banda larga       | POSPG                  | pós pago               |
| CTLBL                | controle banda larga       | AUTOC                  | controle               |
| PREBL                | pré pago banda larga       | PREPG                  | pré pago               |

---

#### 📊 Estatísticas e Tipagem  - `plataforma.parquet`

| coluna               | tipo    |   distintos |   nulos | pct_distintos   | pct_nulos   | cardinalidade   |
|:---------------------|:--------|------------:|--------:|:----------------|:------------|:----------------|
| cod_plataforma_atu   | VARCHAR |          28 |       0 | 100.0%          | 0.0%        | ALTA            |
| dsc_plataforma_atu   | VARCHAR |          28 |       0 | 100.0%          | 0.0%        | ALTA            |
| cod_grupo_plataforma | VARCHAR |          13 |       0 | 46.43%          | 0.0%        | ALTA            |
| dsc_grupo_plataforma | VARCHAR |           6 |       1 | 21.43%          | 3.57%       | ALTA            |

---

## 📄 Arquivo: `promocao_credito.parquet`

#### 📦 Volumetria - `promocao_credito.parquet`

| Arquivo | Registros | Colunas |
| :--- | :--- | :--- |
| promocao_credito.parquet | 15 | 7 |


---

#### 🔍 Amostra de Dados (Head 20)  - `promocao_credito.parquet`

|   cod_promocao | dsc_promocao                                                                                         |   cod_prom_grupo_cartao | dsc_nome_promocao                | cod_tipo_promocao   |   val_promocao |   num_conta_dedicada |
|---------------:|:-----------------------------------------------------------------------------------------------------|------------------------:|:---------------------------------|:--------------------|---------------:|---------------------:|
|            317 | incentivo a adesão ao débito automático para claro controle                                          |                       1 | debau_01                         | INCENTIVO_DEBAU     |             50 |                    2 |
|            318 | incentivo à recarga, em todas as modalidades, para clientes pré-pago e claro controle, em que bônus  |                       2 | recarga turbinada                | RECARGA             |              0 |                    0 |
|            319 | incentivo à recarga em parceria com a visa para clientes pré-pago e claro controle, em que ganham bo |                       3 | acao claro visa                  | RECARGA             |              0 |                    0 |
|            320 | troca de portfolio com aumento de validade e ajuste nas descricoes de alguns voucher groups de merca |                       4 | troca de portfolio 19/08/2008    | RECARGA             |              0 |                    0 |
|            321 | diminui??o de validade nas recargas de 50 e 100 reais                                                |                       5 | altera??o de validades 50 e 100  | RECARGA             |              0 |                    0 |
|            367 | diminuic?o de validade nas recargas de 50 e 100 reais                                                |                       5 | alterac?o de validades 50 e 100  | RECARGA             |              0 |                    0 |
|            377 | diminuição de validade nas recargas de 50 e 100 reais                                                |                       5 | alteração de validades 50 e 100  | RECARGA             |              0 |                    0 |
|            322 | bônus para todas as recargas online e física de r$3 e r$5                                            |                       6 | recarga bonificada               | RECARGA             |              0 |                    0 |
|            327 | alteração da validade dos vgs para 30 dias (histórico pré-alteração)                                 |                       7 | anatel 632                       | RECARGA             |              0 |                    0 |
|            337 | concess?o de b?nus em conta dedicada para recargas de r$20, r$30, r$50 e r$100                       |                       8 | concess?o de cr?ditos adicionais | RECARGA             |              0 |                   67 |
|            368 | concess?o de bonus em conta dedicada para recargas de r$20, r$30, r$50 e r$100                       |                       8 | concess?o de creditos adicionais | RECARGA             |              0 |                   67 |
|            378 | concessão de bônus em conta dedicada para recargas de r$20, r$30, r$50 e r$100                       |                       8 | concessão de créditos adicionais | RECARGA             |              0 |                   67 |
|            347 | hist?rico de altera??es de caracter?sticas de voucher groups                                         |                      10 | hist?rico de altera??es          | RECARGA             |              0 |                    0 |
|            369 | historico de alterac?es de caracteristicas de voucher groups                                         |                      10 | historico de alterac?es          | RECARGA             |              0 |                    0 |
|            379 | histórico de alterações de características de voucher groups                                         |                      10 | histórico de alterações          | RECARGA             |              0 |                    0 |

---

#### 📊 Estatísticas e Tipagem  - `promocao_credito.parquet`

| coluna                | tipo    |   distintos |   nulos | pct_distintos   | pct_nulos   | cardinalidade   |
|:----------------------|:--------|------------:|--------:|:----------------|:------------|:----------------|
| cod_promocao          | VARCHAR |          15 |       0 | 100.0%          | 0.0%        | ALTA            |
| dsc_promocao          | VARCHAR |          15 |       0 | 100.0%          | 0.0%        | ALTA            |
| cod_prom_grupo_cartao | VARCHAR |           9 |       0 | 60.0%           | 0.0%        | ALTA            |
| dsc_nome_promocao     | VARCHAR |          15 |       0 | 100.0%          | 0.0%        | ALTA            |
| cod_tipo_promocao     | VARCHAR |           2 |       0 | 13.33%          | 0.0%        | ALTA            |
| val_promocao          | DOUBLE  |           2 |       0 | 13.33%          | 0.0%        | ALTA            |
| num_conta_dedicada    | VARCHAR |           3 |       0 | 20.0%           | 0.0%        | ALTA            |

---

## 📄 Arquivo: `status_plataforma.parquet`

#### 📦 Volumetria - `status_plataforma.parquet`

| Arquivo | Registros | Colunas |
| :--- | :--- | :--- |
| status_plataforma.parquet | 25 | 5 |


---

#### 🔍 Amostra de Dados (Head 20)  - `status_plataforma.parquet`

| cod_status_plataforma   | dsc_status_plataforma   | ind_ativo   | cod_status_plat_grp   | ind_sts_plat_grp_ativo   |
|:------------------------|:------------------------|:------------|:----------------------|:-------------------------|
| A                       | ativo                   | s           | A                     | s                        |
| ZB1                     | expirado 1              | s           | ZB1                   | s                        |
| PRE                     | pré-ativo               | n           | PRE                   | n                        |
| ZB2                     | expirado 2              | n           | ZB2                   | n                        |
| C                       | desconectado            | n           | C                     | n                        |
| FRD                     | bloqueio por fraude     | n           | C                     | n                        |
| COL                     | cooling                 | n           | C                     | n                        |
| NDF                     | status nao definido     | n           | ND                    | n                        |
| -3                      | nao informado           | n           | ND                    | n                        |
| -2                      | nao determinado         | n           | ND                    | n                        |
| ST                      | suspensão temporária    | s           | A                     | s                        |
| 4                       | inventario              | n           | C                     | n                        |
| 6                       | ativo                   | s           | A                     | s                        |
| 7                       | inativo                 | n           | C                     | n                        |
| 8                       | removido                | n           | C                     | n                        |
| 9                       | retirado                | n           | C                     | n                        |
| 10                      | teste pronto            | s           | A                     | s                        |
| 11                      | ativacao pronta         | s           | A                     | s                        |
| 12                      | trial                   | s           | A                     | s                        |
| 13                      | substituido             | n           | C                     | n                        |

---

#### 📊 Estatísticas e Tipagem  - `status_plataforma.parquet`

| coluna                 | tipo    |   distintos |   nulos | pct_distintos   | pct_nulos   | cardinalidade   |
|:-----------------------|:--------|------------:|--------:|:----------------|:------------|:----------------|
| cod_status_plataforma  | VARCHAR |          25 |       0 | 100.0%          | 0.0%        | ALTA            |
| dsc_status_plataforma  | VARCHAR |          24 |       0 | 96.0%           | 0.0%        | ALTA            |
| ind_ativo              | VARCHAR |           2 |       0 | 8.0%            | 0.0%        | ALTA            |
| cod_status_plat_grp    | VARCHAR |           6 |       0 | 24.0%           | 0.0%        | ALTA            |
| ind_sts_plat_grp_ativo | VARCHAR |           2 |       0 | 8.0%            | 0.0%        | ALTA            |

---

## 📄 Arquivo: `tecnologia.parquet`

#### 📦 Volumetria - `tecnologia.parquet`

| Arquivo | Registros | Colunas |
| :--- | :--- | :--- |
| tecnologia.parquet | 10 | 2 |


---

#### 🔍 Amostra de Dados (Head 20)  - `tecnologia.parquet`

| cod_tecnologia_dw   | dsc_tecnologia   |
|:--------------------|:-----------------|
| AMBOS               | 3g/gsm           |
| GSM                 | gsm              |
| NTDMA               | novo tdma        |
| TDMA                | tdma             |
| -1                  | na               |
| -2                  | nd               |
| -3                  | ni               |
| 3G                  | 3g               |
| 4G                  | 4g               |
| 5G                  | 5g               |

---

#### 📊 Estatísticas e Tipagem  - `tecnologia.parquet`

| coluna            | tipo    |   distintos |   nulos | pct_distintos   | pct_nulos   | cardinalidade   |
|:------------------|:--------|------------:|--------:|:----------------|:------------|:----------------|
| cod_tecnologia_dw | VARCHAR |          10 |       0 | 100.0%          | 0.0%        | ALTA            |
| dsc_tecnologia    | VARCHAR |          10 |       0 | 100.0%          | 0.0%        | ALTA            |

---

## 📄 Arquivo: `tipo_credito.parquet`

#### 📦 Volumetria - `tipo_credito.parquet`

| Arquivo | Registros | Colunas |
| :--- | :--- | :--- |
| tipo_credito.parquet | 12 | 2 |


---

#### 🔍 Amostra de Dados (Head 20)  - `tipo_credito.parquet`

| cod_tipo_credito   | dsc_tipo_credito         |
|:-------------------|:-------------------------|
| PE                 | online                   |
| -1                 | na                       |
| -2                 | nd                       |
| -3                 | ni                       |
| AU                 | autocontrole             |
| BO                 | bonus                    |
| CF                 | cartão físico            |
| CV                 | pin eletronico           |
| IO                 | ioio                     |
| OU                 | outros                   |
| TE                 | transferência eletrônica |
| TF                 | tef                      |

---

#### 📊 Estatísticas e Tipagem  - `tipo_credito.parquet`

| coluna           | tipo    |   distintos |   nulos | pct_distintos   | pct_nulos   | cardinalidade   |
|:-----------------|:--------|------------:|--------:|:----------------|:------------|:----------------|
| cod_tipo_credito | VARCHAR |          12 |       0 | 100.0%          | 0.0%        | ALTA            |
| dsc_tipo_credito | VARCHAR |          12 |       0 | 100.0%          | 0.0%        | ALTA            |

---

## 📄 Arquivo: `tipo_insercao.parquet`

#### 📦 Volumetria - `tipo_insercao.parquet`

| Arquivo | Registros | Colunas |
| :--- | :--- | :--- |
| tipo_insercao.parquet | 22 | 2 |


---

#### 🔍 Amostra de Dados (Head 20)  - `tipo_insercao.parquet`

|   dw_tipo_insercao | dsc_tipo_insercao                       |
|-------------------:|:----------------------------------------|
|                 -3 | não informado                           |
|                 -2 | não determinado                         |
|                 -1 | não se aplica                           |
|                  1 | pag. cartão físico                      |
|                  2 | pag. pin eletrônico                     |
|                  3 | pag. virtual                            |
|                  4 | franquia claro controle                 |
|                  5 | adicional claro controle-cartão físico  |
|                  6 | adicional claro controle-pin eletrônico |
|                  7 | adicional claro controle-virtual        |
|                  8 | claro transferência                     |
|                  9 | ajustes positivos                       |
|                 10 | pacote torpedo dacc                     |
|                 11 | claro bônus                             |
|                 12 | bônus ativação                          |
|                 13 | bônus recarga                           |
|                 14 | bônus acumulador 1                      |
|                 15 | bônus acumulador 2 e 3                  |
|                 16 | bônus dedicadas 1                       |
|                 17 | bônus dedicadas 2                       |

---

#### 📊 Estatísticas e Tipagem  - `tipo_insercao.parquet`

| coluna            | tipo    |   distintos |   nulos | pct_distintos   | pct_nulos   | cardinalidade   |
|:------------------|:--------|------------:|--------:|:----------------|:------------|:----------------|
| dw_tipo_insercao  | VARCHAR |          22 |       0 | 100.0%          | 0.0%        | ALTA            |
| dsc_tipo_insercao | VARCHAR |          22 |       0 | 100.0%          | 0.0%        | ALTA            |

---

## 📄 Arquivo: `tipo_recarga.parquet`

#### 📦 Volumetria - `tipo_recarga.parquet`

| Arquivo | Registros | Colunas |
| :--- | :--- | :--- |
| tipo_recarga.parquet | 5 | 2 |


---

#### 🔍 Amostra de Dados (Head 20)  - `tipo_recarga.parquet`

|   dw_tipo_recarga | dsc_tipo_recarga            |
|------------------:|:----------------------------|
|                -3 | não informado               |
|                -2 | não determinado             |
|                -1 | não se aplica               |
|                 1 | franquia do claro controle  |
|                 2 | adicional do claro controle |

---

#### 📊 Estatísticas e Tipagem  - `tipo_recarga.parquet`

| coluna           | tipo    |   distintos |   nulos | pct_distintos   | pct_nulos   | cardinalidade   |
|:-----------------|:--------|------------:|--------:|:----------------|:------------|:----------------|
| dw_tipo_recarga  | VARCHAR |           5 |       0 | 100.0%          | 0.0%        | ALTA            |
| dsc_tipo_recarga | VARCHAR |           5 |       0 | 100.0%          | 0.0%        | ALTA            |

---

