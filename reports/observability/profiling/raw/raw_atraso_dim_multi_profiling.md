# Relatório de Profiling: `raw/atraso_dim`



## 📄 Arquivo: `BI_DIM_TIPO_FATURAMENTO.csv`

#### 📦 Volumetria - `BI_DIM_TIPO_FATURAMENTO.csv`

| Arquivo | Registros | Colunas |
| :--- | :--- | :--- |
| BI_DIM_TIPO_FATURAMENTO.csv | 72 | 6 |


---

#### 🔍 Amostra de Dados (Head 5)  - `BI_DIM_TIPO_FATURAMENTO.csv`

|   DW_TIPO_FATURAMENTO | DSC_TIPO_FATURAMENTO   | COD_TIPO_FATURAMENTO   | DAT_EXPIRACAO_DW   | DAT_CRIACAO_DW     | DSC_TIPO_FATURAMENTO_ABREV   |
|----------------------:|:-----------------------|:-----------------------|:-------------------|:-------------------|:-----------------------------|
|                 32527 | Refund                 | R                      |                    | 28MAR2017:08:00:40 | REFUND                       |
|                 32528 | Credit                 | C                      |                    | 28MAR2017:08:00:40 | CREDIT                       |
|                 32529 | Claro                  | B                      |                    | 28MAR2017:08:00:40 | SERVICE                      |
|                 32530 | Service Deposit        | D                      |                    | 28MAR2017:08:00:40 | DEPOSIT                      |
|                 32531 | Reversal               | RV                     |                    | 28MAR2017:08:00:40 | REVERSAL                     |

---

#### 📊 Estatísticas e Tipagem  - `BI_DIM_TIPO_FATURAMENTO.csv`

| coluna                     | tipo    |   distintos |   nulos | pct_distintos   | pct_nulos   | cardinalidade   |
|:---------------------------|:--------|------------:|--------:|:----------------|:------------|:----------------|
| DW_TIPO_FATURAMENTO        | BIGINT  |          72 |       0 | 100.0%          | 0.0%        | ALTA            |
| DSC_TIPO_FATURAMENTO       | VARCHAR |          69 |       0 | 95.83%          | 0.0%        | ALTA            |
| COD_TIPO_FATURAMENTO       | VARCHAR |          70 |       0 | 97.22%          | 0.0%        | ALTA            |
| DAT_EXPIRACAO_DW           | VARCHAR |           2 |      70 | 2.78%           | 97.22%      | MEDIA           |
| DAT_CRIACAO_DW             | VARCHAR |          10 |       0 | 13.89%          | 0.0%        | ALTA            |
| DSC_TIPO_FATURAMENTO_ABREV | VARCHAR |          65 |       3 | 90.28%          | 4.17%       | ALTA            |

---

#### 📏 Extremos (Min/Max)  - `BI_DIM_TIPO_FATURAMENTO.csv`

| coluna              |   minimo |   maximo |
|:--------------------|---------:|---------:|
| DW_TIPO_FATURAMENTO |       -3 |    33543 |


---

