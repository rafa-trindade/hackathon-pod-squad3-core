# Relatório de Profiling: `raw/recarga_dim`



## 📄 Arquivo: `BI_DIM_CANAL_AQUISICAO_CREDITO.csv`

#### 📦 Volumetria - `BI_DIM_CANAL_AQUISICAO_CREDITO.csv`

| Arquivo | Registros | Colunas |
| :--- | :--- | :--- |
| BI_DIM_CANAL_AQUISICAO_CREDITO.csv | 5.899 | 12 |


---

#### 🔍 Amostra de Dados (Head 5)  - `BI_DIM_CANAL_AQUISICAO_CREDITO.csv`

|   COD_CANAL_AQUISICAO | DSC_CANAL_AQUISICAO        |   COD_SISTEMA_DW | DAT_ATUALIZACAO_DW   | DAT_CRIACAO_DW     |   COD_CANAL_AQUISICAO_BI |   DSC_CANAL_AQUISICAO_BI |   COD_AGENTE_CREDITO | DAT_EXPIRACAO_DW   | COD_TIPO_CREDITO   | COD_TIPO_INSTITUICAO   | DSC_TIPO_INSTITUICAO   |
|----------------------:|:---------------------------|-----------------:|:---------------------|:-------------------|-------------------------:|-------------------------:|---------------------:|:-------------------|:-------------------|:-----------------------|:-----------------------|
|                 14929 | SS/AA EBV - GOLFE TELECOM  |               21 | 08JUL2020:08:22:50   | 16APR2015:22:19:21 |                       -3 |                       -3 |                 8210 | 08JUL2020:00:00:00 | CV                 | <NA>                   |                        |
|                 14930 | SS/AA EBV - MARAJO COMERCI |               21 | 08JUL2020:08:22:50   | 16APR2015:22:19:21 |                       -3 |                       -3 |                 8211 | 08JUL2020:00:00:00 | CV                 | <NA>                   |                        |
|                 14931 | SS/AA CONCEL               |               21 | 08JUL2020:08:22:50   | 16APR2015:22:19:21 |                       -3 |                       -3 |                 8212 | 08JUL2020:00:00:00 | CV                 | <NA>                   |                        |
|                 14932 | SS/AA VIRTUAL CELULARES    |               21 | 08JUL2020:08:22:50   | 16APR2015:22:19:21 |                       -3 |                       -3 |                 8213 | 08JUL2020:00:00:00 | CV                 | <NA>                   |                        |
|                 14933 | SS/AA PORTOCEL             |               21 | 08JUL2020:08:22:50   | 16APR2015:22:19:21 |                       -3 |                       -3 |                 8214 | 08JUL2020:00:00:00 | CV                 | <NA>                   |                        |

---

#### 📊 Estatísticas e Tipagem  - `BI_DIM_CANAL_AQUISICAO_CREDITO.csv`

| coluna                 | tipo    |   distintos |   nulos | pct_distintos   | pct_nulos   | cardinalidade   |
|:-----------------------|:--------|------------:|--------:|:----------------|:------------|:----------------|
| COD_CANAL_AQUISICAO    | BIGINT  |        5899 |       0 | 100.0%          | 0.0%        | ALTA            |
| DSC_CANAL_AQUISICAO    | VARCHAR |        4243 |       0 | 71.93%          | 0.0%        | ALTA            |
| COD_SISTEMA_DW         | BIGINT  |           9 |       0 | 0.15%           | 0.0%        | MEDIA           |
| DAT_ATUALIZACAO_DW     | VARCHAR |          79 |       0 | 1.34%           | 0.0%        | MEDIA           |
| DAT_CRIACAO_DW         | VARCHAR |         321 |       0 | 5.44%           | 0.0%        | ALTA            |
| COD_CANAL_AQUISICAO_BI | BIGINT  |          17 |       0 | 0.29%           | 0.0%        | MEDIA           |
| DSC_CANAL_AQUISICAO_BI | VARCHAR |          19 |       0 | 0.32%           | 0.0%        | MEDIA           |
| COD_AGENTE_CREDITO     | VARCHAR |        5105 |     294 | 86.54%          | 4.98%       | ALTA            |
| DAT_EXPIRACAO_DW       | VARCHAR |          32 |     990 | 0.54%           | 16.78%      | MEDIA           |
| COD_TIPO_CREDITO       | VARCHAR |           3 |     294 | 0.05%           | 4.98%       | BAIXA           |
| COD_TIPO_INSTITUICAO   | BIGINT  |          11 |    5268 | 0.19%           | 89.3%       | MEDIA           |
| DSC_TIPO_INSTITUICAO   | VARCHAR |          13 |    5268 | 0.22%           | 89.3%       | MEDIA           |

---

#### 📏 Extremos (Min/Max)  - `BI_DIM_CANAL_AQUISICAO_CREDITO.csv`

| coluna                 |   minimo |   maximo |
|:-----------------------|---------:|---------:|
| COD_CANAL_AQUISICAO    |       -3 |    17708 |
| COD_SISTEMA_DW         |       -3 |       21 |
| COD_CANAL_AQUISICAO_BI |       -3 |       16 |
| COD_TIPO_INSTITUICAO   |        1 |       13 |


---



## 📄 Arquivo: `BI_DIM_FORMA_PAGAMENTO.csv`

#### 📦 Volumetria - `BI_DIM_FORMA_PAGAMENTO.csv`

| Arquivo | Registros | Colunas |
| :--- | :--- | :--- |
| BI_DIM_FORMA_PAGAMENTO.csv | 9 | 5 |


---

#### 🔍 Amostra de Dados (Head 5)  - `BI_DIM_FORMA_PAGAMENTO.csv`

|   DW_FORMA_PAGAMENTO | COD_FORMA_PAGAMENTO   | DSC_FORMA_PAGAMENTO   | DAT_CRIACAO_DW     | DAT_EXPIRACAO_DW   |
|---------------------:|:----------------------|:----------------------|:-------------------|:-------------------|
|                   -1 | -1                    | Não se Aplica         | 21FEB2008:17:11:28 |                    |
|                   -2 | -2                    | Não Determinado       | 21FEB2008:17:11:29 |                    |
|                   -3 | -3                    | Não Informado         | 21FEB2008:17:11:29 |                    |
|                   11 | CP                    | Credito de PrePago    | 15FEB2008:11:27:40 |                    |
|                   12 | DD                    | Debito Direto         | 15FEB2008:11:27:40 |                    |

---

#### 📊 Estatísticas e Tipagem  - `BI_DIM_FORMA_PAGAMENTO.csv`

| coluna              | tipo    |   distintos |   nulos | pct_distintos   | pct_nulos   | cardinalidade   |
|:--------------------|:--------|------------:|--------:|:----------------|:------------|:----------------|
| DW_FORMA_PAGAMENTO  | BIGINT  |           9 |       0 | 100.0%          | 0.0%        | ALTA            |
| COD_FORMA_PAGAMENTO | VARCHAR |           9 |       0 | 100.0%          | 0.0%        | ALTA            |
| DSC_FORMA_PAGAMENTO | VARCHAR |           9 |       0 | 100.0%          | 0.0%        | ALTA            |
| DAT_CRIACAO_DW      | VARCHAR |           4 |       0 | 44.44%          | 0.0%        | ALTA            |
| DAT_EXPIRACAO_DW    | VARCHAR |           0 |       9 | 0.0%            | 100.0%      | BAIXA           |

---

#### 📏 Extremos (Min/Max)  - `BI_DIM_FORMA_PAGAMENTO.csv`

| coluna             |   minimo |   maximo |
|:-------------------|---------:|---------:|
| DW_FORMA_PAGAMENTO |       -3 |       15 |


---



## 📄 Arquivo: `BI_DIM_INSTITUICAO.csv`

#### 📦 Volumetria - `BI_DIM_INSTITUICAO.csv`

| Arquivo | Registros | Colunas |
| :--- | :--- | :--- |
| BI_DIM_INSTITUICAO.csv | 550 | 9 |


---

#### 🔍 Amostra de Dados (Head 5)  - `BI_DIM_INSTITUICAO.csv`

|   DW_INSTITUICAO |   COD_INSTITUICAO | DSC_INSTITUICAO      |   COD_TIPO_INSTITUICAO | DSC_TIPO_INSTITUICAO   |   COD_SISTEMA_DW | DAT_EXPIRACAO_DW   | DAT_CRIACAO_DW     |   COD_AGENTE |
|-----------------:|------------------:|:---------------------|-----------------------:|:-----------------------|-----------------:|:-------------------|:-------------------|-------------:|
|            13926 |               416 | Banco Inter          |                      1 | Banco                  |               21 |                    | 26AUG2021:00:18:55 |         5416 |
|            13927 |               490 | MWallet/Bradesco     |                      1 | Banco                  |               21 |                    | 26AUG2021:00:18:55 |         5490 |
|            13928 |               514 | Santander/C.Bancario |                      1 | Banco                  |               21 |                    | 26AUG2021:00:18:55 |         5514 |
|            13929 |                24 | CEF/C.Bancario       |                      1 | Banco                  |               21 |                    | 26AUG2021:00:18:55 |         5024 |
|            13930 |                69 | Lemon Bank           |                      1 | Banco                  |               21 |                    | 26AUG2021:00:18:55 |         5069 |

---

#### 📊 Estatísticas e Tipagem  - `BI_DIM_INSTITUICAO.csv`

| coluna               | tipo    |   distintos |   nulos | pct_distintos   | pct_nulos   | cardinalidade   |
|:---------------------|:--------|------------:|--------:|:----------------|:------------|:----------------|
| DW_INSTITUICAO       | BIGINT  |         550 |       0 | 100.0%          | 0.0%        | ALTA            |
| COD_INSTITUICAO      | BIGINT  |         550 |       0 | 100.0%          | 0.0%        | ALTA            |
| DSC_INSTITUICAO      | VARCHAR |         550 |       0 | 100.0%          | 0.0%        | ALTA            |
| COD_TIPO_INSTITUICAO | BIGINT  |          11 |       0 | 2.0%            | 0.0%        | MEDIA           |
| DSC_TIPO_INSTITUICAO | VARCHAR |          11 |       0 | 2.0%            | 0.0%        | MEDIA           |
| COD_SISTEMA_DW       | BIGINT  |           1 |       0 | 0.18%           | 0.0%        | MEDIA           |
| DAT_EXPIRACAO_DW     | VARCHAR |           0 |     550 | 0.0%            | 100.0%      | BAIXA           |
| DAT_CRIACAO_DW       | VARCHAR |           2 |       0 | 0.36%           | 0.0%        | MEDIA           |
| COD_AGENTE           | BIGINT  |         550 |       0 | 100.0%          | 0.0%        | ALTA            |

---

#### 📏 Extremos (Min/Max)  - `BI_DIM_INSTITUICAO.csv`

| coluna               |   minimo |   maximo |
|:---------------------|---------:|---------:|
| DW_INSTITUICAO       |    13926 |    14477 |
| COD_INSTITUICAO      |        1 |      558 |
| COD_TIPO_INSTITUICAO |        1 |       13 |
| COD_SISTEMA_DW       |       21 |       21 |
| COD_AGENTE           |     5001 |     5558 |


---



## 📄 Arquivo: `BI_DIM_PLANO_PRECO.csv`

#### 📦 Volumetria - `BI_DIM_PLANO_PRECO.csv`

| Arquivo | Registros | Colunas |
| :--- | :--- | :--- |
| BI_DIM_PLANO_PRECO.csv | 293.743 | 25 |


---

#### 🔍 Amostra de Dados (Head 5)  - `BI_DIM_PLANO_PRECO.csv`

|   DW_PLANO |   COD_PLANO_PRECO | DSC_PLANO_PRECO             |   COD_TIPO_CLIENTE |   COD_SUB_TIPO_CLIENTE |   DW_TIPO_CLIENTE | DAT_EFETIVACAO     | DAT_EXPIRACAO   |   DSC_PLANO_PRECO_BI |   DSC_GRUPO_PLANO_BI |   DSC_TIPO_PLANO_BI | IND_AMDOCS_PLAT_PRE   |   COD_TRATAMENTO_ESPECIAL |   COD_SISTEMA_DW |   COD_TECNOLOGIA_DW | DAT_EXPIRACAO_DW   | DAT_ATUALIZACAO_DW   | DAT_CRIACAO_DW     | NUM_FRANQUIA_MINUTOS_BI   | NUM_FRANQUIA_REAIS_BI   | NUM_FRANQUIA_EVENTOS_BI   | NUM_FRANQUIA_VOLUME_BI   |   COD_PLANO_COMPONENTE |   DSC_PLANO_PRECO_UNICO_BI | DSC_MODALIDADE_PLANO   |
|-----------:|------------------:|:----------------------------|-------------------:|-----------------------:|------------------:|:-------------------|:----------------|---------------------:|---------------------:|--------------------:|:----------------------|--------------------------:|-----------------:|--------------------:|:-------------------|:---------------------|:-------------------|:--------------------------|:------------------------|:--------------------------|:-------------------------|-----------------------:|---------------------------:|:-----------------------|
|     533477 |          50029231 | Licitac?o Marinha do Brasil |                 -1 |                     -1 |                -1 | 13OCT2017:23:18:06 |                 |                   -3 |                   -3 |                  -3 | A                     |                        -1 |               35 |                  -3 | 20NOV2017:00:00:00 | 20NOV2017:00:15:25   | 22AUG2017:00:15:10 |                           |                         |                           |                          |               50029231 |                            |                        |
|     601796 |          50029231 | Licitação Marinha do Brasil |                 -1 |                     -1 |                -1 | 20FEB2025:17:52:41 |                 |                   -3 |                   -3 |                  -3 | A                     |                        -1 |               35 |                  -3 | 06APR2025:00:00:00 | 06APR2025:01:51:48   | 08FEB2022:04:43:05 |                           |                         |                           |                          |               50029231 |                         -3 |                        |
|     548887 |          50029231 | Licitac?o Marinha do Brasil |                 -1 |                     -1 |                -1 | 12MAY2019:12:23:52 |                 |                   -3 |                   -3 |                  -3 | A                     |                        -1 |               35 |                  -3 | 16JUN2019:00:00:00 | 16JUN2019:00:29:37   | 27MAY2019:00:33:52 |                           |                         |                           |                          |               50029231 |                            |                        |
|     535237 |          50029231 | Licitac?o Marinha do Brasil |                 -1 |                     -1 |                -1 | 18NOV2017:23:22:29 |                 |                   -3 |                   -3 |                  -3 | A                     |                        -1 |               35 |                  -3 | 03DEC2017:00:00:00 | 03DEC2017:00:13:58   | 21NOV2017:00:20:19 |                           |                         |                           |                          |               50029231 |                            |                        |
|     536107 |          50029231 | Licitac?o Marinha do Brasil |                 -1 |                     -1 |                -1 | 01DEC2017:23:42:01 |                 |                   -3 |                   -3 |                  -3 | A                     |                        -1 |               35 |                  -3 | 14JAN2018:00:00:00 | 14JAN2018:00:16:37   | 04DEC2017:00:12:56 |                           |                         |                           |                          |               50029231 |                            |                        |

---

#### 📊 Estatísticas e Tipagem  - `BI_DIM_PLANO_PRECO.csv`

| coluna                   | tipo    |   distintos |   nulos | pct_distintos   | pct_nulos   | cardinalidade   |
|:-------------------------|:--------|------------:|--------:|:----------------|:------------|:----------------|
| DW_PLANO                 | BIGINT  |      293743 |       0 | 100.0%          | 0.0%        | ALTA            |
| COD_PLANO_PRECO          | VARCHAR |       13490 |       0 | 4.59%           | 0.0%        | MEDIA           |
| DSC_PLANO_PRECO          | VARCHAR |       42084 |       0 | 14.33%          | 0.0%        | ALTA            |
| COD_TIPO_CLIENTE         | VARCHAR |           9 |       0 | 0.0%            | 0.0%        | BAIXA           |
| COD_SUB_TIPO_CLIENTE     | VARCHAR |          25 |       0 | 0.01%           | 0.0%        | BAIXA           |
| DW_TIPO_CLIENTE          | BIGINT  |          97 |       0 | 0.03%           | 0.0%        | BAIXA           |
| DAT_EFETIVACAO           | VARCHAR |       10579 |  107047 | 3.6%            | 36.44%      | MEDIA           |
| DAT_EXPIRACAO            | VARCHAR |           2 |  292111 | 0.0%            | 99.44%      | BAIXA           |
| DSC_PLANO_PRECO_BI       | VARCHAR |        2487 |       0 | 0.85%           | 0.0%        | MEDIA           |
| DSC_GRUPO_PLANO_BI       | VARCHAR |          30 |       0 | 0.01%           | 0.0%        | BAIXA           |
| DSC_TIPO_PLANO_BI        | VARCHAR |           9 |       0 | 0.0%            | 0.0%        | BAIXA           |
| IND_AMDOCS_PLAT_PRE      | VARCHAR |           3 |       0 | 0.0%            | 0.0%        | BAIXA           |
| COD_TRATAMENTO_ESPECIAL  | VARCHAR |           4 |       0 | 0.0%            | 0.0%        | BAIXA           |
| COD_SISTEMA_DW           | BIGINT  |          15 |       0 | 0.01%           | 0.0%        | BAIXA           |
| COD_TECNOLOGIA_DW        | VARCHAR |           8 |       0 | 0.0%            | 0.0%        | BAIXA           |
| DAT_EXPIRACAO_DW         | VARCHAR |        1980 |   34169 | 0.67%           | 11.63%      | MEDIA           |
| DAT_ATUALIZACAO_DW       | VARCHAR |        3665 |       0 | 1.25%           | 0.0%        | MEDIA           |
| DAT_CRIACAO_DW           | VARCHAR |        6568 |       0 | 2.24%           | 0.0%        | MEDIA           |
| NUM_FRANQUIA_MINUTOS_BI  | VARCHAR |           0 |  293743 | 0.0%            | 100.0%      | BAIXA           |
| NUM_FRANQUIA_REAIS_BI    | VARCHAR |           0 |  293743 | 0.0%            | 100.0%      | BAIXA           |
| NUM_FRANQUIA_EVENTOS_BI  | VARCHAR |           0 |  293743 | 0.0%            | 100.0%      | BAIXA           |
| NUM_FRANQUIA_VOLUME_BI   | VARCHAR |           0 |  293743 | 0.0%            | 100.0%      | BAIXA           |
| COD_PLANO_COMPONENTE     | BIGINT  |        6259 |  124730 | 2.13%           | 42.46%      | MEDIA           |
| DSC_PLANO_PRECO_UNICO_BI | VARCHAR |         101 |  110147 | 0.03%           | 37.5%       | BAIXA           |
| DSC_MODALIDADE_PLANO     | VARCHAR |           0 |  293743 | 0.0%            | 100.0%      | BAIXA           |

---

#### 📏 Extremos (Min/Max)  - `BI_DIM_PLANO_PRECO.csv`

| coluna               |   minimo |    maximo |
|:---------------------|---------:|----------:|
| DW_PLANO             |       -3 |    712581 |
| DW_TIPO_CLIENTE      |       -3 |       171 |
| COD_SISTEMA_DW       |       -3 |        39 |
| COD_PLANO_COMPONENTE |       -3 | 609552531 |


---



## 📄 Arquivo: `BI_DIM_PLATAFORMA.csv`

#### 📦 Volumetria - `BI_DIM_PLATAFORMA.csv`

| Arquivo | Registros | Colunas |
| :--- | :--- | :--- |
| BI_DIM_PLATAFORMA.csv | 28 | 8 |


---

#### 🔍 Amostra de Dados (Head 5)  - `BI_DIM_PLATAFORMA.csv`

|   COD_PLATAFORMA | DSC_PLATAFORMA   | DAT_EXPIRACAO_DW   | DAT_ATUALIZACAO_DW   | DAT_CRIACAO_DW     | DSC_PLATAFORMA_BI          | COD_GRUPO_PLATAFORMA_BI   | DSC_GRUPO_PLATAFORMA   |
|-----------------:|:-----------------|:-------------------|:---------------------|:-------------------|:---------------------------|:--------------------------|:-----------------------|
|               24 | M2MS             |                    | 06NOV2018:09:05:39   | 06NOV2018:09:05:39 | Machine to Machine Special | POSTL                     | Telemetria             |
|               26 | MVNOD            |                    | 06DEC2021:12:03:25   | 06DEC2021:12:03:25 | Parceiros MVNO DIGITAL     | MVNO                      | MVNO Digital           |
|               12 | POSTL            |                    | 07NOV2012:15:02:14   | 07NOV2012:15:02:14 | Telemetria                 | POSTL                     | Telemetria             |
|               20 | POSDT            |                    | 13DEC2017:15:11:00   | 13DEC2017:15:11:00 | Pós Pago Deutsche Telekom  | POSPG                     | Telemetria             |
|               21 | FLEXD            |                    | 13DEC2017:15:11:00   | 13DEC2017:15:11:00 | Pré Pago Flex Digital      | PREPG                     | Pós Pago               |

---

#### 📊 Estatísticas e Tipagem  - `BI_DIM_PLATAFORMA.csv`

| coluna                  | tipo    |   distintos |   nulos | pct_distintos   | pct_nulos   | cardinalidade   |
|:------------------------|:--------|------------:|--------:|:----------------|:------------|:----------------|
| COD_PLATAFORMA          | BIGINT  |          28 |       0 | 100.0%          | 0.0%        | ALTA            |
| DSC_PLATAFORMA          | VARCHAR |          28 |       0 | 100.0%          | 0.0%        | ALTA            |
| DAT_EXPIRACAO_DW        | VARCHAR |           0 |      28 | 0.0%            | 100.0%      | BAIXA           |
| DAT_ATUALIZACAO_DW      | VARCHAR |          24 |       0 | 85.71%          | 0.0%        | ALTA            |
| DAT_CRIACAO_DW          | VARCHAR |          24 |       0 | 85.71%          | 0.0%        | ALTA            |
| DSC_PLATAFORMA_BI       | VARCHAR |          28 |       0 | 100.0%          | 0.0%        | ALTA            |
| COD_GRUPO_PLATAFORMA_BI | VARCHAR |          13 |       0 | 46.43%          | 0.0%        | ALTA            |
| DSC_GRUPO_PLATAFORMA    | VARCHAR |           6 |       1 | 21.43%          | 3.57%       | ALTA            |

---

#### 📏 Extremos (Min/Max)  - `BI_DIM_PLATAFORMA.csv`

| coluna         |   minimo |   maximo |
|:---------------|---------:|---------:|
| COD_PLATAFORMA |       -3 |       26 |


---



## 📄 Arquivo: `BI_DIM_PROMOCAO_CREDITO.csv`

#### 📦 Volumetria - `BI_DIM_PROMOCAO_CREDITO.csv`

| Arquivo | Registros | Colunas |
| :--- | :--- | :--- |
| BI_DIM_PROMOCAO_CREDITO.csv | 15 | 12 |


---

#### 🔍 Amostra de Dados (Head 5)  - `BI_DIM_PROMOCAO_CREDITO.csv`

|   COD_PROMOCAO | DSC_PROMOCAO                                                                                         | DAT_EXPIRACAO_DW   | DAT_ATUALIZACAO_DW   | DAT_CRIACAO_DW     |   COD_PROM_GRUPO_CARTAO | DSC_NOME_PROMOCAO               | COD_TIPO_PROMOCAO   | DAT_INICIO_VIGENCIA   | DAT_FIM_VIGENCIA   |   VAL_PROMOCAO |   NUM_CONTA_DEDICADA |
|---------------:|:-----------------------------------------------------------------------------------------------------|:-------------------|:---------------------|:-------------------|------------------------:|:--------------------------------|:--------------------|:----------------------|:-------------------|---------------:|---------------------:|
|            317 | Incentivo a adesão ao débito automático para Claro Controle                                          |                    | 14SEP2025:11:05:20   | 11NOV2011:16:31:04 |                       1 | DEBAU_01                        | INCENTIVO_DEBAU     | 07APR2007:00:00:00    | 30APR2010:23:59:59 |             50 |                    2 |
|            318 | Incentivo à recarga, em todas as modalidades, para clientes pré-pago e Claro Controle, em que bônus  |                    | 14SEP2025:11:05:20   | 11NOV2011:16:31:04 |                       2 | Recarga Turbinada               | RECARGA             | 14JUN2007:00:00:00    | 03SEP2007:23:59:59 |              0 |                    0 |
|            319 | Incentivo à recarga em parceria com a VISA para clientes pré-pago e Claro Controle, em que ganham bo |                    | 14SEP2025:11:05:20   | 11NOV2011:16:31:04 |                       3 | Acao Claro Visa                 | RECARGA             | 26NOV2007:00:00:00    | 28JAN2008:23:59:59 |              0 |                    0 |
|            320 | Troca de portfolio com aumento de validade e ajuste nas descricoes de alguns voucher groups de merca |                    | 14SEP2025:11:05:20   | 11NOV2011:16:31:04 |                       4 | Troca de portfolio 19/08/2008   | RECARGA             | 19AUG2008:00:00:00    | 31DEC9999:23:59:59 |              0 |                    0 |
|            321 | Diminui??o de validade nas recargas de 50 e 100 reais                                                | 17JAN2022:00:00:00 | 18JAN2022:12:05:22   | 11NOV2011:16:31:04 |                       5 | Altera??o de validades 50 e 100 | RECARGA             | 10AUG2009:00:00:00    | 31DEC9999:23:59:59 |              0 |                    0 |

---

#### 📊 Estatísticas e Tipagem  - `BI_DIM_PROMOCAO_CREDITO.csv`

| coluna                | tipo    |   distintos |   nulos | pct_distintos   | pct_nulos   | cardinalidade   |
|:----------------------|:--------|------------:|--------:|:----------------|:------------|:----------------|
| COD_PROMOCAO          | BIGINT  |          15 |       0 | 100.0%          | 0.0%        | ALTA            |
| DSC_PROMOCAO          | VARCHAR |          15 |       0 | 100.0%          | 0.0%        | ALTA            |
| DAT_EXPIRACAO_DW      | VARCHAR |           2 |       9 | 13.33%          | 60.0%       | ALTA            |
| DAT_ATUALIZACAO_DW    | VARCHAR |           3 |       0 | 20.0%           | 0.0%        | ALTA            |
| DAT_CRIACAO_DW        | VARCHAR |           6 |       0 | 40.0%           | 0.0%        | ALTA            |
| COD_PROM_GRUPO_CARTAO | BIGINT  |           9 |       0 | 60.0%           | 0.0%        | ALTA            |
| DSC_NOME_PROMOCAO     | VARCHAR |          15 |       0 | 100.0%          | 0.0%        | ALTA            |
| COD_TIPO_PROMOCAO     | VARCHAR |           2 |       0 | 13.33%          | 0.0%        | ALTA            |
| DAT_INICIO_VIGENCIA   | VARCHAR |           9 |       0 | 60.0%           | 0.0%        | ALTA            |
| DAT_FIM_VIGENCIA      | VARCHAR |           5 |       0 | 33.33%          | 0.0%        | ALTA            |
| VAL_PROMOCAO          | DOUBLE  |           2 |       0 | 13.33%          | 0.0%        | ALTA            |
| NUM_CONTA_DEDICADA    | BIGINT  |           3 |       0 | 20.0%           | 0.0%        | ALTA            |

---

#### 📏 Extremos (Min/Max)  - `BI_DIM_PROMOCAO_CREDITO.csv`

| coluna                |   minimo |   maximo |
|:----------------------|---------:|---------:|
| COD_PROMOCAO          |      317 |      379 |
| COD_PROM_GRUPO_CARTAO |        1 |       10 |
| VAL_PROMOCAO          |        0 |       50 |
| NUM_CONTA_DEDICADA    |        0 |       67 |


---



## 📄 Arquivo: `BI_DIM_STATUS_PLATAFORMA.csv`

#### 📦 Volumetria - `BI_DIM_STATUS_PLATAFORMA.csv`

| Arquivo | Registros | Colunas |
| :--- | :--- | :--- |
| BI_DIM_STATUS_PLATAFORMA.csv | 25 | 7 |


---

#### 🔍 Amostra de Dados (Head 5)  - `BI_DIM_STATUS_PLATAFORMA.csv`

| COD_STATUS_PLATAFORMA   | DSC_STATUS_PLATAFORMA   | IND_ATIVO   | DAT_ATUALIZACAO_DW   | DAT_CRIACAO_DW     | COD_STATUS_PLAT_GRP   | IND_STS_PLAT_GRP_ATIVO   |
|:------------------------|:------------------------|:------------|:---------------------|:-------------------|:----------------------|:-------------------------|
| A                       | Ativo                   | S           | 16OCT2006:10:28:44   | 16OCT2006:10:28:44 | A                     | S                        |
| ZB1                     | Expirado 1              | S           | 16OCT2006:10:28:44   | 16OCT2006:10:28:44 | ZB1                   | S                        |
| PRE                     | Pré-Ativo               | N           | 16OCT2006:10:28:56   | 16OCT2006:10:28:56 | PRE                   | N                        |
| ZB2                     | Expirado 2              | N           | 16OCT2006:10:28:56   | 16OCT2006:10:28:56 | ZB2                   | N                        |
| C                       | Desconectado            | N           | 16OCT2006:10:28:56   | 16OCT2006:10:28:56 | C                     | N                        |

---

#### 📊 Estatísticas e Tipagem  - `BI_DIM_STATUS_PLATAFORMA.csv`

| coluna                 | tipo    |   distintos |   nulos | pct_distintos   | pct_nulos   | cardinalidade   |
|:-----------------------|:--------|------------:|--------:|:----------------|:------------|:----------------|
| COD_STATUS_PLATAFORMA  | VARCHAR |          25 |       0 | 100.0%          | 0.0%        | ALTA            |
| DSC_STATUS_PLATAFORMA  | VARCHAR |          24 |       0 | 96.0%           | 0.0%        | ALTA            |
| IND_ATIVO              | VARCHAR |           2 |       0 | 8.0%            | 0.0%        | ALTA            |
| DAT_ATUALIZACAO_DW     | VARCHAR |           7 |       0 | 28.0%           | 0.0%        | ALTA            |
| DAT_CRIACAO_DW         | VARCHAR |           7 |       0 | 28.0%           | 0.0%        | ALTA            |
| COD_STATUS_PLAT_GRP    | VARCHAR |           6 |       0 | 24.0%           | 0.0%        | ALTA            |
| IND_STS_PLAT_GRP_ATIVO | VARCHAR |           2 |       0 | 8.0%            | 0.0%        | ALTA            |

---

#### 📏 Extremos (Min/Max)  - `BI_DIM_STATUS_PLATAFORMA.csv`

> Nenhuma coluna numérica ou de data identificada.


---



## 📄 Arquivo: `BI_DIM_TECNOLOGIA.csv`

#### 📦 Volumetria - `BI_DIM_TECNOLOGIA.csv`

| Arquivo | Registros | Colunas |
| :--- | :--- | :--- |
| BI_DIM_TECNOLOGIA.csv | 10 | 5 |


---

#### 🔍 Amostra de Dados (Head 5)  - `BI_DIM_TECNOLOGIA.csv`

| COD_TECNOLOGIA_DW   | DSC_TECNOLOGIA   | DAT_ATUALIZACAO_DW   | DAT_CRIACAO_DW     | COD_TECNOLOGIA_SVA   |
|:--------------------|:-----------------|:---------------------|:-------------------|:---------------------|
| AMBOS               | 3G/GSM           |                      | 07MAY2010:11:23:38 |                      |
| GSM                 | GSM              | 19NOV2003:16:47:57   | 19NOV2003:16:47:57 |                      |
| NTDMA               | Novo TDMA        | 19NOV2003:16:47:51   | 19NOV2003:16:47:51 |                      |
| TDMA                | TDMA             | 19NOV2003:16:47:44   | 19NOV2003:16:47:44 | T                    |
| -1                  | NA               | 01MAR2004:19:37:55   | 01MAR2004:19:37:55 |                      |

---

#### 📊 Estatísticas e Tipagem  - `BI_DIM_TECNOLOGIA.csv`

| coluna             | tipo    |   distintos |   nulos | pct_distintos   | pct_nulos   | cardinalidade   |
|:-------------------|:--------|------------:|--------:|:----------------|:------------|:----------------|
| COD_TECNOLOGIA_DW  | VARCHAR |          10 |       0 | 100.0%          | 0.0%        | ALTA            |
| DSC_TECNOLOGIA     | VARCHAR |          10 |       0 | 100.0%          | 0.0%        | ALTA            |
| DAT_ATUALIZACAO_DW | VARCHAR |           9 |       1 | 90.0%           | 10.0%       | ALTA            |
| DAT_CRIACAO_DW     | VARCHAR |          10 |       0 | 100.0%          | 0.0%        | ALTA            |
| COD_TECNOLOGIA_SVA | VARCHAR |           3 |       6 | 30.0%           | 60.0%       | ALTA            |

---

#### 📏 Extremos (Min/Max)  - `BI_DIM_TECNOLOGIA.csv`

> Nenhuma coluna numérica ou de data identificada.


---



## 📄 Arquivo: `BI_DIM_TIPO_CREDITO.csv`

#### 📦 Volumetria - `BI_DIM_TIPO_CREDITO.csv`

| Arquivo | Registros | Colunas |
| :--- | :--- | :--- |
| BI_DIM_TIPO_CREDITO.csv | 12 | 5 |


---

#### 🔍 Amostra de Dados (Head 5)  - `BI_DIM_TIPO_CREDITO.csv`

| COD_TIPO_CREDITO   | DSC_TIPO_CREDITO   | DAT_EXPIRACAO_DW   | DAT_ATUALIZACAO_DW   | DAT_CRIACAO_DW     |
|:-------------------|:-------------------|:-------------------|:---------------------|:-------------------|
| PE                 | Online             |                    |                      | 19OCT2011:14:39:55 |
| -1                 | NA                 |                    | 01MAR2004:19:54:06   | 01MAR2004:19:54:06 |
| -2                 | ND                 |                    | 01MAR2004:19:54:08   | 01MAR2004:19:54:08 |
| -3                 | NI                 |                    | 01MAR2004:19:54:09   | 01MAR2004:19:54:09 |
| AU                 | Autocontrole       |                    | 01MAR2004:18:18:22   | 01MAR2004:18:18:22 |

---

#### 📊 Estatísticas e Tipagem  - `BI_DIM_TIPO_CREDITO.csv`

| coluna             | tipo    |   distintos |   nulos | pct_distintos   | pct_nulos   | cardinalidade   |
|:-------------------|:--------|------------:|--------:|:----------------|:------------|:----------------|
| COD_TIPO_CREDITO   | VARCHAR |          12 |       0 | 100.0%          | 0.0%        | ALTA            |
| DSC_TIPO_CREDITO   | VARCHAR |          12 |       0 | 100.0%          | 0.0%        | ALTA            |
| DAT_EXPIRACAO_DW   | VARCHAR |           0 |      12 | 0.0%            | 100.0%      | BAIXA           |
| DAT_ATUALIZACAO_DW | VARCHAR |          11 |       1 | 91.67%          | 8.33%       | ALTA            |
| DAT_CRIACAO_DW     | VARCHAR |          12 |       0 | 100.0%          | 0.0%        | ALTA            |

---

#### 📏 Extremos (Min/Max)  - `BI_DIM_TIPO_CREDITO.csv`

> Nenhuma coluna numérica ou de data identificada.


---



## 📄 Arquivo: `BI_DIM_TIPO_INSERCAO.csv`

#### 📦 Volumetria - `BI_DIM_TIPO_INSERCAO.csv`

| Arquivo | Registros | Colunas |
| :--- | :--- | :--- |
| BI_DIM_TIPO_INSERCAO.csv | 22 | 4 |


---

#### 🔍 Amostra de Dados (Head 5)  - `BI_DIM_TIPO_INSERCAO.csv`

|   DW_TIPO_INSERCAO | DSC_TIPO_INSERCAO   | DAT_EXPIRACAO_DW   | DAT_CRIACAO_DW     |
|-------------------:|:--------------------|:-------------------|:-------------------|
|                 -3 | Não Informado       |                    | 19OCT2011:14:39:56 |
|                 -2 | Não Determinado     |                    | 19OCT2011:14:39:56 |
|                 -1 | Não se Aplica       |                    | 19OCT2011:14:39:56 |
|                  1 | Pag. Cartão Físico  |                    | 19OCT2011:14:39:56 |
|                  2 | Pag. PIN Eletrônico |                    | 19OCT2011:14:39:56 |

---

#### 📊 Estatísticas e Tipagem  - `BI_DIM_TIPO_INSERCAO.csv`

| coluna            | tipo    |   distintos |   nulos | pct_distintos   | pct_nulos   | cardinalidade   |
|:------------------|:--------|------------:|--------:|:----------------|:------------|:----------------|
| DW_TIPO_INSERCAO  | BIGINT  |          22 |       0 | 100.0%          | 0.0%        | ALTA            |
| DSC_TIPO_INSERCAO | VARCHAR |          22 |       0 | 100.0%          | 0.0%        | ALTA            |
| DAT_EXPIRACAO_DW  | VARCHAR |           0 |      22 | 0.0%            | 100.0%      | BAIXA           |
| DAT_CRIACAO_DW    | VARCHAR |           1 |       0 | 4.55%           | 0.0%        | MEDIA           |

---

#### 📏 Extremos (Min/Max)  - `BI_DIM_TIPO_INSERCAO.csv`

| coluna           |   minimo |   maximo |
|:-----------------|---------:|---------:|
| DW_TIPO_INSERCAO |       -3 |       19 |


---



## 📄 Arquivo: `BI_DIM_TIPO_RECARGA.csv`

#### 📦 Volumetria - `BI_DIM_TIPO_RECARGA.csv`

| Arquivo | Registros | Colunas |
| :--- | :--- | :--- |
| BI_DIM_TIPO_RECARGA.csv | 5 | 4 |


---

#### 🔍 Amostra de Dados (Head 5)  - `BI_DIM_TIPO_RECARGA.csv`

|   DW_TIPO_RECARGA | DSC_TIPO_RECARGA            | DAT_EXPIRACAO_DW   | DAT_CRIACAO_DW     |
|------------------:|:----------------------------|:-------------------|:-------------------|
|                -3 | Não Informado               |                    | 19OCT2011:14:39:56 |
|                -2 | Não Determinado             |                    | 19OCT2011:14:39:56 |
|                -1 | Não se Aplica               |                    | 19OCT2011:14:39:56 |
|                 1 | Franquia do Claro Controle  |                    | 19OCT2011:14:39:56 |
|                 2 | Adicional do Claro Controle |                    | 19OCT2011:14:39:56 |

---

#### 📊 Estatísticas e Tipagem  - `BI_DIM_TIPO_RECARGA.csv`

| coluna           | tipo    |   distintos |   nulos | pct_distintos   | pct_nulos   | cardinalidade   |
|:-----------------|:--------|------------:|--------:|:----------------|:------------|:----------------|
| DW_TIPO_RECARGA  | BIGINT  |           5 |       0 | 100.0%          | 0.0%        | ALTA            |
| DSC_TIPO_RECARGA | VARCHAR |           5 |       0 | 100.0%          | 0.0%        | ALTA            |
| DAT_EXPIRACAO_DW | VARCHAR |           0 |       5 | 0.0%            | 100.0%      | BAIXA           |
| DAT_CRIACAO_DW   | VARCHAR |           1 |       0 | 20.0%           | 0.0%        | ALTA            |

---

#### 📏 Extremos (Min/Max)  - `BI_DIM_TIPO_RECARGA.csv`

| coluna          |   minimo |   maximo |
|:----------------|---------:|---------:|
| DW_TIPO_RECARGA |       -3 |        2 |


---

