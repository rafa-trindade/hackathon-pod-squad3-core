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
|                 32527 | Refund                 | REFUND                       | R                          |
|                 32528 | Credit                 | CREDIT                       | C                          |
|                 32529 | Claro                  | SERVICE                      | B                          |
|                 32530 | Service Deposit        | DEPOSIT                      | D                          |
|                 32531 | Reversal               | REVERSAL                     | RV                         |
|                 32532 | Reversed Print Doc     | REVRSPRT                     | RP                         |
|                 32533 | ENCARGO DE EQUIPAMENTO | EQUIP                        | Q                          |
|                 32534 | Payment Arrangement    | PA                           | PA                         |
|                 32535 | EASYTONE               | EASYTONE                     | 35                         |
|                 32536 | CMBRIDGE               | CMBRIDGE                     | 49                         |
|                 32537 | TELCOM65               | TELCOM65                     | 65                         |
|                 32538 | PA EASYTONE            | PA35                         | PE                         |
|                 32539 | PA CAMBRIDGE           | PA49                         | PC                         |
|                 32540 | PA TELECOM 65          | PA65                         | PT                         |
|                 32541 | Embratel 21            | EBT                          | 21                         |
|                 32542 | Telefonica 15          | TLFONICA                     | 15                         |
|                 32543 | Telemar 31             | TELEMAR                      | 31                         |
|                 32544 | CTBC 12                | CTBC                         | 12                         |
|                 32545 | BRT 14                 | BRT                          | 14                         |
|                 32546 | Intelig 23             | INTELIG                      | 23                         |

---

#### 📊 Estatísticas e Tipagem  - `tipo_faturamento.parquet`

| coluna                     | tipo    |   distintos |   nulos | pct_distintos   | pct_nulos   | cardinalidade   |
|:---------------------------|:--------|------------:|--------:|:----------------|:------------|:----------------|
| dw_tipo_faturamento        | VARCHAR |          72 |       0 | 100.0%          | 0.0%        | ALTA            |
| dsc_tipo_faturamento       | VARCHAR |          69 |       0 | 95.83%          | 0.0%        | ALTA            |
| dsc_tipo_faturamento_abrev | VARCHAR |          65 |       3 | 90.28%          | 4.17%       | ALTA            |
| cod_dsc_tipo_faturamento   | VARCHAR |          70 |       0 | 97.22%          | 0.0%        | ALTA            |

---

