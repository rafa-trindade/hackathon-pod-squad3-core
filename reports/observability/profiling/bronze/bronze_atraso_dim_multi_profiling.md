# Relatório de Profiling: `bronze/atraso_dim`



## 📄 Arquivo: `tipo_faturamento.parquet`

#### 📦 Volumetria - `tipo_faturamento.parquet`

| Arquivo | Registros | Colunas |
| :--- | :--- | :--- |
| tipo_faturamento.parquet | 72 | 4 |


---

#### 🔍 Amostra de Dados (Head 20)  - `tipo_faturamento.parquet`

|   dw_tipo_faturamento | dsc_tipo_faturamento   | dsc_tipo_faturamento_abrev   | cod_dsc_tipo_faturamento   |
|----------------------:|:-----------------------|:-----------------------------|:---------------------------|
|                 32527 | refund                 | refund                       | r                          |
|                 32528 | credit                 | credit                       | c                          |
|                 32529 | claro                  | service                      | b                          |
|                 32530 | service deposit        | deposit                      | d                          |
|                 32531 | reversal               | reversal                     | rv                         |
|                 32532 | reversed print doc     | revrsprt                     | rp                         |
|                 32533 | encargo de equipamento | equip                        | q                          |
|                 32534 | payment arrangement    | pa                           | pa                         |
|                 32535 | easytone               | easytone                     | 35                         |
|                 32536 | cmbridge               | cmbridge                     | 49                         |
|                 32537 | telcom65               | telcom65                     | 65                         |
|                 32538 | pa easytone            | pa35                         | pe                         |
|                 32539 | pa cambridge           | pa49                         | pc                         |
|                 32540 | pa telecom 65          | pa65                         | pt                         |
|                 32541 | embratel 21            | ebt                          | 21                         |
|                 32542 | telefonica 15          | tlfonica                     | 15                         |
|                 32543 | telemar 31             | telemar                      | 31                         |
|                 32544 | ctbc 12                | ctbc                         | 12                         |
|                 32545 | brt 14                 | brt                          | 14                         |
|                 32546 | intelig 23             | intelig                      | 23                         |

---

#### 📊 Estatísticas e Tipagem  - `tipo_faturamento.parquet`

| coluna                     | tipo    |   distintos |   nulos | pct_distintos   | pct_nulos   | cardinalidade   |
|:---------------------------|:--------|------------:|--------:|:----------------|:------------|:----------------|
| dw_tipo_faturamento        | VARCHAR |          72 |       0 | 100.0%          | 0.0%        | ALTA            |
| dsc_tipo_faturamento       | VARCHAR |          69 |       0 | 95.83%          | 0.0%        | ALTA            |
| dsc_tipo_faturamento_abrev | VARCHAR |          65 |       3 | 90.28%          | 4.17%       | ALTA            |
| cod_dsc_tipo_faturamento   | VARCHAR |          70 |       0 | 97.22%          | 0.0%        | ALTA            |

---

