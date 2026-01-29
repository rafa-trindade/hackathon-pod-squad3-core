# Relatório de Profiling: `gold/abt_base_cmv` - `20260129`

### ⚙️ Sumário Técnico do Dataset: `abt_base_cmv`

- **Volume de Registros (N):** 2.633.900
- **Cardinalidade (CPF):** 2.565.985
- **Grão Definido:** `num_cpf, safra, prod`

---

### 🎯 Distribuição da Variável Alvo (Target): `abt_base_cmv`

| fpd   |   frequencia | percentual   |
|:------|-------------:|:-------------|
| False |      2074671 | 78.77%       |
| True  |       559229 | 21.23%       |

---

### 🔑 Verificação de Chave Técnica: `abt_base_cmv`
|   pk_distintos |   duplicatas_reais | pct_duplicidade   |
|---------------:|-------------------:|:------------------|
|        2633900 |                  0 | 0.0%              |

---

### 🔍 Perfil de Missings por Feature: `abt_base_cmv`

| column_name                       | column_type              | pct_missing   |
|:----------------------------------|:-------------------------|:--------------|
| num_cpf                           | VARCHAR                  | 0.0%          |
| safra                             | DATE                     | 0.0%          |
| prod                              | VARCHAR                  | 0.0%          |
| fpd                               | BOOLEAN                  | 0.0%          |
| flag_instalacao                   | BOOLEAN                  | 0.0%          |
| rec_qtd_l30d                      | BIGINT                   | 0.0%          |
| rec_qtd_l60d                      | BIGINT                   | 0.0%          |
| rec_qtd_l90d                      | BIGINT                   | 0.0%          |
| rec_qtd_geral                     | BIGINT                   | 0.0%          |
| rec_vlr_total_l30d                | DOUBLE                   | 41.68%        |
| rec_vlr_total_l60d                | DOUBLE                   | 33.85%        |
| rec_vlr_total_l90d                | DOUBLE                   | 31.11%        |
| rec_vlr_total_geral               | DOUBLE                   | 28.17%        |
| rec_vlr_avg_l30d                  | DOUBLE                   | 41.68%        |
| rec_vlr_avg_l60d                  | DOUBLE                   | 33.85%        |
| rec_vlr_avg_l90d                  | DOUBLE                   | 31.11%        |
| rec_vlr_avg_geral                 | DOUBLE                   | 28.17%        |
| rec_vlr_min_l30d                  | DOUBLE                   | 41.68%        |
| rec_vlr_min_l60d                  | DOUBLE                   | 33.85%        |
| rec_vlr_min_l90d                  | DOUBLE                   | 31.11%        |
| rec_vlr_min_geral                 | DOUBLE                   | 28.17%        |
| rec_vlr_max_l30d                  | DOUBLE                   | 41.68%        |
| rec_vlr_max_l60d                  | DOUBLE                   | 33.85%        |
| rec_vlr_max_l90d                  | DOUBLE                   | 31.11%        |
| rec_vlr_max_geral                 | DOUBLE                   | 28.17%        |
| rec_dat_primeira                  | DATE                     | 28.17%        |
| rec_dat_ultima                    | DATE                     | 28.17%        |
| rec_qtd_canais_distintos          | BIGINT                   | 0.0%          |
| rec_dias_desde_ultima             | BIGINT                   | 28.17%        |
| rec_dias_desde_primeira           | BIGINT                   | 28.17%        |
| rec_vlr_std_l30d                  | DOUBLE                   | 60.46%        |
| rec_vlr_std_l60d                  | DOUBLE                   | 41.28%        |
| rec_vlr_std_l90d                  | DOUBLE                   | 35.94%        |
| rec_vlr_std_geral                 | DOUBLE                   | 29.6%         |
| rec_vlr_coef_var_l30d             | DOUBLE                   | 69.59%        |
| rec_vlr_coef_var_l60d             | DOUBLE                   | 57.5%         |
| rec_vlr_coef_var_l90d             | DOUBLE                   | 52.79%        |
| rec_ratio_qtd_l30d_l60d           | DOUBLE                   | 33.85%        |
| rec_ratio_qtd_l60d_l90d           | DOUBLE                   | 31.11%        |
| rec_ratio_vlr_l30d_l60d           | DOUBLE                   | 59.01%        |
| rec_ratio_vlr_l60d_l90d           | DOUBLE                   | 52.7%         |
| rec_flag_sem_recarga_l30d         | INTEGER                  | 0.0%          |
| rec_flag_sem_recarga_l60d         | INTEGER                  | 0.0%          |
| rec_flag_sem_recarga_l90d         | INTEGER                  | 0.0%          |
| pag_vlr_total_l30d                | DOUBLE                   | 77.59%        |
| pag_vlr_total_l60d                | DOUBLE                   | 73.43%        |
| pag_vlr_total_l90d                | DOUBLE                   | 72.26%        |
| pag_vlr_total_geral               | DOUBLE                   | 70.16%        |
| pag_vlr_avg_l30d                  | DOUBLE                   | 77.59%        |
| pag_vlr_avg_l60d                  | DOUBLE                   | 73.43%        |
| pag_vlr_avg_l90d                  | DOUBLE                   | 72.26%        |
| pag_vlr_avg_geral                 | DOUBLE                   | 70.16%        |
| pag_vlr_min_l30d                  | DOUBLE                   | 77.59%        |
| pag_vlr_min_l60d                  | DOUBLE                   | 73.43%        |
| pag_vlr_min_l90d                  | DOUBLE                   | 72.26%        |
| pag_vlr_min_geral                 | DOUBLE                   | 70.16%        |
| pag_vlr_max_l30d                  | DOUBLE                   | 77.59%        |
| pag_vlr_max_l60d                  | DOUBLE                   | 73.43%        |
| pag_vlr_max_l90d                  | DOUBLE                   | 72.26%        |
| pag_vlr_max_geral                 | DOUBLE                   | 70.16%        |
| pag_qtd_faturas_l30d              | BIGINT                   | 0.0%          |
| pag_qtd_faturas_l60d              | BIGINT                   | 0.0%          |
| pag_qtd_faturas_l90d              | BIGINT                   | 0.0%          |
| pag_qtd_faturas_geral             | BIGINT                   | 0.0%          |
| pag_qtd_vezes_com_juros           | BIGINT                   | 0.0%          |
| pag_dias_desde_ultimo_pagamento   | BIGINT                   | 70.16%        |
| pag_ticket_medio_l30d             | DOUBLE                   | 77.59%        |
| pag_ticket_medio_l60d             | DOUBLE                   | 73.43%        |
| pag_ticket_medio_l90d             | DOUBLE                   | 72.26%        |
| pag_ticket_medio_geral            | DOUBLE                   | 70.16%        |
| pag_share_faturas_com_juros_l30d  | DOUBLE                   | 77.59%        |
| pag_share_faturas_com_juros_l60d  | DOUBLE                   | 73.43%        |
| pag_share_faturas_com_juros_l90d  | DOUBLE                   | 72.26%        |
| pag_share_faturas_com_juros_geral | DOUBLE                   | 70.16%        |
| pag_vlr_std_l30d                  | DOUBLE                   | 88.55%        |
| pag_vlr_std_l60d                  | DOUBLE                   | 76.99%        |
| pag_vlr_std_l90d                  | DOUBLE                   | 74.11%        |
| pag_flag_sem_pagamento_l30d       | INTEGER                  | 0.0%          |
| pag_flag_sem_pagamento_l60d       | INTEGER                  | 0.0%          |
| pag_flag_sem_pagamento_l90d       | INTEGER                  | 0.0%          |
| atr_vlr_max_l30d                  | DOUBLE                   | 86.47%        |
| atr_vlr_max_l60d                  | DOUBLE                   | 72.23%        |
| atr_vlr_max_l90d                  | DOUBLE                   | 70.78%        |
| atr_vlr_max_geral                 | DOUBLE                   | 68.15%        |
| atr_vlr_acumulado_l30d            | DOUBLE                   | 86.47%        |
| atr_vlr_acumulado_l60d            | DOUBLE                   | 72.23%        |
| atr_vlr_acumulado_l90d            | DOUBLE                   | 70.78%        |
| atr_vlr_acumulado_geral           | DOUBLE                   | 68.15%        |
| atr_qtd_faturas_atrasadas_l30d    | BIGINT                   | 0.0%          |
| atr_qtd_faturas_atrasadas_l60d    | BIGINT                   | 0.0%          |
| atr_qtd_faturas_atrasadas_l90d    | BIGINT                   | 0.0%          |
| atr_qtd_faturas_atrasadas_geral   | BIGINT                   | 0.0%          |
| atr_dat_ultima_ref                | DATE                     | 68.15%        |
| atr_dias_desde_ultimo_atraso      | BIGINT                   | 68.15%        |
| atr_ticket_medio_l30d             | DOUBLE                   | 86.47%        |
| atr_ticket_medio_l60d             | DOUBLE                   | 72.23%        |
| atr_ticket_medio_l90d             | DOUBLE                   | 70.78%        |
| atr_ticket_medio_geral            | DOUBLE                   | 68.15%        |
| atr_flag_recorrente_l30d          | INTEGER                  | 0.0%          |
| atr_flag_recorrente_l60d          | INTEGER                  | 0.0%          |
| atr_flag_recorrente_l90d          | INTEGER                  | 0.0%          |
| atr_flag_atraso_l30d              | INTEGER                  | 0.0%          |
| atr_flag_atraso_l60d              | INTEGER                  | 0.0%          |
| atr_flag_atraso_l90d              | INTEGER                  | 0.0%          |
| bur_flag_mig2                     | VARCHAR                  | 0.0%          |
| bur_score_01                      | INTEGER                  | 0.67%         |
| bur_score_02                      | INTEGER                  | 0.07%         |
| cad_cep_3_digitos                 | VARCHAR                  | 5.49%         |
| cad_datadenascimento              | DATE                     | 0.23%         |
| cad_flag_mig2                     | VARCHAR                  | 0.0%          |
| cad_statusrf                      | VARCHAR                  | 0.2%          |
| cad_var_02                        | INTEGER                  | 94.22%        |
| cad_var_03                        | INTEGER                  | 6.82%         |
| cad_var_04                        | INTEGER                  | 0.2%          |
| cad_var_05                        | INTEGER                  | 3.56%         |
| cad_var_06                        | INTEGER                  | 79.39%        |
| cad_var_07                        | DOUBLE                   | 81.85%        |
| cad_var_08                        | INTEGER                  | 79.4%         |
| cad_var_09                        | INTEGER                  | 59.2%         |
| cad_var_10                        | VARCHAR                  | 98.19%        |
| cad_var_11                        | DOUBLE                   | 98.32%        |
| cad_var_12                        | DATE                     | 35.4%         |
| cad_var_13                        | DATE                     | 85.0%         |
| cad_var_14                        | INTEGER                  | 89.31%        |
| cad_var_15                        | VARCHAR                  | 86.86%        |
| cad_var_16                        | INTEGER                  | 86.86%        |
| cad_var_17                        | INTEGER                  | 86.86%        |
| cad_var_18                        | VARCHAR                  | 79.39%        |
| cad_var_19                        | VARCHAR                  | 59.2%         |
| cad_var_20                        | VARCHAR                  | 97.88%        |
| cad_var_21                        | VARCHAR                  | 35.4%         |
| cad_var_22                        | VARCHAR                  | 89.31%        |
| cad_var_23                        | VARCHAR                  | 86.86%        |
| cad_var_24                        | VARCHAR                  | 35.4%         |
| cad_var_25                        | VARCHAR                  | 9.96%         |
| tel_flag_mig2                     | VARCHAR                  | 50.3%         |
| tel_var_26                        | VARCHAR                  | 50.35%        |
| tel_var_27                        | VARCHAR                  | 50.35%        |
| tel_var_28                        | DOUBLE                   | 50.35%        |
| tel_var_29                        | DOUBLE                   | 50.35%        |
| tel_var_30                        | DOUBLE                   | 50.35%        |
| tel_var_31                        | DOUBLE                   | 50.35%        |
| tel_var_32                        | DOUBLE                   | 50.35%        |
| tel_var_33                        | DOUBLE                   | 50.35%        |
| tel_var_34                        | DOUBLE                   | 50.35%        |
| tel_var_35                        | DOUBLE                   | 50.35%        |
| tel_var_36                        | DOUBLE                   | 50.35%        |
| tel_var_37                        | DOUBLE                   | 50.35%        |
| tel_var_38                        | DOUBLE                   | 50.35%        |
| tel_var_39                        | DOUBLE                   | 50.35%        |
| tel_var_40                        | DOUBLE                   | 50.35%        |
| tel_var_41                        | DOUBLE                   | 50.35%        |
| tel_var_42                        | DOUBLE                   | 50.35%        |
| tel_var_43                        | DOUBLE                   | 50.35%        |
| tel_var_44                        | DOUBLE                   | 50.35%        |
| tel_var_45                        | DOUBLE                   | 50.35%        |
| tel_var_46                        | DOUBLE                   | 50.35%        |
| tel_var_47                        | DOUBLE                   | 50.35%        |
| tel_var_48                        | DOUBLE                   | 50.35%        |
| tel_var_49                        | DOUBLE                   | 50.35%        |
| tel_var_50                        | DOUBLE                   | 50.35%        |
| tel_var_51                        | DOUBLE                   | 50.35%        |
| tel_var_52                        | DOUBLE                   | 50.35%        |
| tel_var_53                        | DOUBLE                   | 50.35%        |
| tel_var_54                        | DOUBLE                   | 50.35%        |
| tel_var_55                        | DOUBLE                   | 50.35%        |
| tel_var_56                        | DOUBLE                   | 50.35%        |
| tel_var_57                        | DOUBLE                   | 50.35%        |
| tel_var_58                        | DOUBLE                   | 50.35%        |
| tel_var_59                        | DOUBLE                   | 50.35%        |
| tel_var_60                        | DOUBLE                   | 50.35%        |
| tel_var_61                        | DOUBLE                   | 50.35%        |
| tel_var_62                        | DOUBLE                   | 50.35%        |
| tel_var_63                        | DOUBLE                   | 50.35%        |
| tel_var_64                        | VARCHAR                  | 50.35%        |
| tel_var_65                        | VARCHAR                  | 50.35%        |
| tel_var_66                        | VARCHAR                  | 50.35%        |
| tel_var_67                        | VARCHAR                  | 50.35%        |
| tel_var_68                        | DOUBLE                   | 50.35%        |
| tel_var_69                        | DOUBLE                   | 50.35%        |
| tel_var_70                        | DOUBLE                   | 50.35%        |
| tel_var_71                        | DOUBLE                   | 50.35%        |
| tel_var_72                        | DOUBLE                   | 50.35%        |
| tel_var_73                        | VARCHAR                  | 50.35%        |
| tel_var_74                        | VARCHAR                  | 50.35%        |
| tel_var_75                        | VARCHAR                  | 50.35%        |
| tel_var_76                        | VARCHAR                  | 50.35%        |
| tel_var_77                        | VARCHAR                  | 50.35%        |
| tel_var_78                        | VARCHAR                  | 50.3%         |
| tel_var_79                        | VARCHAR                  | 50.3%         |
| tel_var_80                        | VARCHAR                  | 50.3%         |
| tel_var_81                        | VARCHAR                  | 50.3%         |
| tel_var_82                        | DOUBLE                   | 50.3%         |
| tel_var_83                        | VARCHAR                  | 50.3%         |
| tel_var_84                        | VARCHAR                  | 50.3%         |
| tel_var_85                        | VARCHAR                  | 50.3%         |
| tel_var_86                        | VARCHAR                  | 50.3%         |
| tel_var_87                        | VARCHAR                  | 50.3%         |
| tel_var_88                        | VARCHAR                  | 50.3%         |
| tel_var_89                        | VARCHAR                  | 50.3%         |
| tel_var_90                        | DOUBLE                   | 50.3%         |
| tel_var_91                        | VARCHAR                  | 50.3%         |
| tel_var_92                        | VARCHAR                  | 50.3%         |
| tel_var_93                        | VARCHAR                  | 50.3%         |
| run_id                            | BIGINT                   | 0.0%          |
| ingestion_ts                      | TIMESTAMP WITH TIME ZONE | 0.0%          |
| ano_mes                           | BIGINT                   | 0.0%          |

---

### 🚩 Detecção de Anomalias Financeiras (Outliers > 3σ): `abt_base_cmv`

| Feature                           | Max Value     | Threshold (3σ)   | Status              |
|:----------------------------------|:--------------|:-----------------|:--------------------|
| rec_qtd_l30d                      | 260,00        | 9,83             | ⚠️ Outlier Detected |
| rec_qtd_l60d                      | 511,00        | 18,02            | ⚠️ Outlier Detected |
| rec_qtd_l90d                      | 738,00        | 26,00            | ⚠️ Outlier Detected |
| rec_qtd_geral                     | 3.387,00      | 106,89           | ⚠️ Outlier Detected |
| rec_vlr_total_l30d                | 50.000,00     | 242,92           | ⚠️ Outlier Detected |
| rec_vlr_total_l60d                | 50.109,80     | 399,18           | ⚠️ Outlier Detected |
| rec_vlr_total_l90d                | 75.164,70     | 588,25           | ⚠️ Outlier Detected |
| rec_vlr_total_geral               | 425.000,00    | 3.079,35         | ⚠️ Outlier Detected |
| rec_vlr_avg_l30d                  | 12.500,00     | 70,02            | ⚠️ Outlier Detected |
| rec_vlr_avg_l60d                  | 12.500,00     | 65,13            | ⚠️ Outlier Detected |
| rec_vlr_avg_l90d                  | 12.500,00     | 63,02            | ⚠️ Outlier Detected |
| rec_vlr_avg_geral                 | 12.500,00     | 80,36            | ⚠️ Outlier Detected |
| rec_vlr_min_l30d                  | 109,84        | 36,45            | ⚠️ Outlier Detected |
| rec_vlr_min_l60d                  | 109,84        | 30,93            | ⚠️ Outlier Detected |
| rec_vlr_min_l90d                  | 109,84        | 27,48            | ⚠️ Outlier Detected |
| rec_vlr_min_geral                 | 100,00        | 19,92            | ⚠️ Outlier Detected |
| rec_vlr_max_l30d                  | 25.000,00     | 183,82           | ⚠️ Outlier Detected |
| rec_vlr_max_l60d                  | 25.000,00     | 195,52           | ⚠️ Outlier Detected |
| rec_vlr_max_l90d                  | 25.000,00     | 193,27           | ⚠️ Outlier Detected |
| rec_vlr_max_geral                 | 25.000,00     | 267,00           | ⚠️ Outlier Detected |
| rec_qtd_canais_distintos          | 38,00         | 10,82            | ⚠️ Outlier Detected |
| rec_dias_desde_ultima             | 517,00        | 139,36           | ⚠️ Outlier Detected |
| rec_vlr_std_l30d                  | 17.677,67     | 118,75           | ⚠️ Outlier Detected |
| rec_vlr_std_l60d                  | 14.433,76     | 94,37            | ⚠️ Outlier Detected |
| rec_vlr_std_l90d                  | 13.693,06     | 87,93            | ⚠️ Outlier Detected |
| rec_vlr_std_geral                 | 12.729,38     | 113,47           | ⚠️ Outlier Detected |
| rec_vlr_coef_var_l30d             | 16,12         | 2,89             | ⚠️ Outlier Detected |
| rec_vlr_coef_var_l60d             | 20,54         | 3,10             | ⚠️ Outlier Detected |
| rec_vlr_coef_var_l90d             | 26,12         | 3,25             | ⚠️ Outlier Detected |
| pag_vlr_total_l30d                | 438.467,35    | 2.608,05         | ⚠️ Outlier Detected |
| pag_vlr_total_l60d                | 979.673,73    | 5.207,82         | ⚠️ Outlier Detected |
| pag_vlr_total_l90d                | 979.673,73    | 7.149,32         | ⚠️ Outlier Detected |
| pag_vlr_total_geral               | 2.537.770,97  | 23.318,89        | ⚠️ Outlier Detected |
| pag_vlr_avg_l30d                  | 438.467,35    | 1.916,59         | ⚠️ Outlier Detected |
| pag_vlr_avg_l60d                  | 122.459,22    | 879,43           | ⚠️ Outlier Detected |
| pag_vlr_avg_l90d                  | 122.459,22    | 895,04           | ⚠️ Outlier Detected |
| pag_vlr_avg_geral                 | 48.105,38     | 763,23           | ⚠️ Outlier Detected |
| pag_vlr_min_l30d                  | 438.467,35    | 1.853,37         | ⚠️ Outlier Detected |
| pag_vlr_min_l60d                  | 55.261,99     | 565,24           | ⚠️ Outlier Detected |
| pag_vlr_min_l90d                  | 55.261,99     | 530,79           | ⚠️ Outlier Detected |
| pag_vlr_min_geral                 | 16.874,46     | 224,74           | ⚠️ Outlier Detected |
| pag_vlr_max_l30d                  | 438.467,35    | 2.190,67         | ⚠️ Outlier Detected |
| pag_vlr_max_l60d                  | 480.478,67    | 2.215,40         | ⚠️ Outlier Detected |
| pag_vlr_max_l90d                  | 480.478,67    | 2.255,87         | ⚠️ Outlier Detected |
| pag_vlr_max_geral                 | 1.028.185,94  | 4.634,40         | ⚠️ Outlier Detected |
| pag_qtd_faturas_l30d              | 30,00         | 2,37             | ⚠️ Outlier Detected |
| pag_qtd_faturas_l60d              | 30,00         | 4,08             | ⚠️ Outlier Detected |
| pag_qtd_faturas_l90d              | 40,00         | 5,82             | ⚠️ Outlier Detected |
| pag_qtd_faturas_geral             | 110,00        | 24,66            | ⚠️ Outlier Detected |
| pag_qtd_vezes_com_juros           | 268,00        | 20,08            | ⚠️ Outlier Detected |
| pag_dias_desde_ultimo_pagamento   | 516,00        | 166,07           | ⚠️ Outlier Detected |
| pag_ticket_medio_l30d             | 438.467,35    | 2.083,42         | ⚠️ Outlier Detected |
| pag_ticket_medio_l60d             | 122.459,22    | 1.221,23         | ⚠️ Outlier Detected |
| pag_ticket_medio_l90d             | 122.459,22    | 1.225,07         | ⚠️ Outlier Detected |
| pag_ticket_medio_geral            | 181.269,36    | 1.408,01         | ⚠️ Outlier Detected |
| pag_share_faturas_com_juros_l30d  | 8,00          | 2,49             | ⚠️ Outlier Detected |
| pag_share_faturas_com_juros_l60d  | 7,00          | 2,41             | ⚠️ Outlier Detected |
| pag_share_faturas_com_juros_l90d  | 7,33          | 2,33             | ⚠️ Outlier Detected |
| pag_share_faturas_com_juros_geral | 7,80          | 2,16             | ⚠️ Outlier Detected |
| pag_vlr_std_l30d                  | 52.576,08     | 802,48           | ⚠️ Outlier Detected |
| pag_vlr_std_l60d                  | 208.314,08    | 989,12           | ⚠️ Outlier Detected |
| pag_vlr_std_l90d                  | 208.314,08    | 950,68           | ⚠️ Outlier Detected |
| atr_vlr_max_l30d                  | 509.114,06    | 3.064,48         | ⚠️ Outlier Detected |
| atr_vlr_max_l60d                  | 3.406.523,69  | 12.414,23        | ⚠️ Outlier Detected |
| atr_vlr_max_l90d                  | 3.406.523,69  | 12.120,22        | ⚠️ Outlier Detected |
| atr_vlr_max_geral                 | 3.406.523,69  | 11.804,53        | ⚠️ Outlier Detected |
| atr_vlr_acumulado_l30d            | 3.439.561,25  | 19.090,87        | ⚠️ Outlier Detected |
| atr_vlr_acumulado_l60d            | 6.879.122,50  | 31.724,27        | ⚠️ Outlier Detected |
| atr_vlr_acumulado_l90d            | 10.318.683,75 | 46.142,49        | ⚠️ Outlier Detected |
| atr_vlr_acumulado_geral           | 55.931.388,30 | 206.947,05       | ⚠️ Outlier Detected |
| atr_qtd_faturas_atrasadas_l30d    | 102,00        | 2,54             | ⚠️ Outlier Detected |
| atr_qtd_faturas_atrasadas_l60d    | 111,00        | 3,91             | ⚠️ Outlier Detected |
| atr_qtd_faturas_atrasadas_l90d    | 111,00        | 5,36             | ⚠️ Outlier Detected |
| atr_qtd_faturas_atrasadas_geral   | 319,00        | 25,17            | ⚠️ Outlier Detected |
| atr_dias_desde_ultimo_atraso      | 517,00        | 263,62           | ⚠️ Outlier Detected |
| atr_ticket_medio_l30d             | 163.788,63    | 1.177,58         | ⚠️ Outlier Detected |
| atr_ticket_medio_l60d             | 1.792.397,31  | 6.568,26         | ⚠️ Outlier Detected |
| atr_ticket_medio_l90d             | 1.849.738,64  | 6.809,65         | ⚠️ Outlier Detected |
| atr_ticket_medio_geral            | 2.663.399,44  | 10.326,31        | ⚠️ Outlier Detected |
| atr_flag_recorrente_l30d          | 1,00          | 0,69             | ⚠️ Outlier Detected |

---

### 📦 Volumetria: `abt_base_cmv`
| diretorio      |   qtd_arquivos | registros   |   colunas |   tamanho_comprimido_mib |   tamanho_descomprimido_mib |
|:---------------|---------------:|:------------|----------:|-------------------------:|----------------------------:|
| ano_mes=202410 |              1 | 426.104     |       207 |                    59.31 |                       76.43 |
| ano_mes=202411 |              1 | 454.572     |       207 |                    61.99 |                       79.54 |
| ano_mes=202412 |              1 | 445.154     |       207 |                    63.44 |                       81.22 |
| ano_mes=202501 |              1 | 452.621     |       207 |                    62.88 |                       80.25 |
| ano_mes=202502 |              1 | 419.453     |       207 |                    58.58 |                       74.99 |
| ano_mes=202503 |              1 | 435.996     |       207 |                    64.26 |                       82.21 |
| TOTAL          |              6 | 2.633.900   |       207 |                   370.46 |                      474.64 |

---

### 📅 Estabilidade de Safras (Volumetria Mensal)

| safra               |   qtd_registros | representatividade   |
|:--------------------|----------------:|:---------------------|
| 2024-10-01 00:00:00 |          426104 | 16.18%               |
| 2024-11-01 00:00:00 |          454572 | 17.26%               |
| 2024-12-01 00:00:00 |          445154 | 16.9%                |
| 2025-01-01 00:00:00 |          452621 | 17.18%               |
| 2025-02-01 00:00:00 |          419453 | 15.93%               |
| 2025-03-01 00:00:00 |          435996 | 16.55%               |

---

### 📶 Densidade de Sinal (Percentual de nulos médio por Prefixo)
> Mede o percentual médio de preenchimento das variáveis agrupadas por origem.

| prefixo   |   qtd_features | pct_missing_medio   | densidade_sinal   |
|:----------|---------------:|:--------------------|:------------------|
| rec_      |             39 | 30.15%              | 69.85%            |
| pag_      |             36 | 57.51%              | 42.49%            |
| atr_      |             24 | 42.88%              | 57.12%            |
| bur_      |              3 | 0.25%               | 99.75%            |
| tel_      |             69 | 50.34%              | 49.66%            |
| cad_      |             28 | 56.1%               | 43.9%             |
| outros    |              5 | 0.0%                | 100.0%            |

---

### 💳 Perfil de Risco (Taxa de FPD por Produto)

| prod   |   total_cpfs |   qtd_bad | fpd_rate   |
|:-------|-------------:|----------:|:-----------|
| CMV    |      2633900 |    559229 | 21.23%     |

---

### 📈 Top 15 Variáveis com Maior Correlação (Pearson) com Target
> Identifica a força da relação linear entre as features e o evento de FPD.

| feature                         |   correlacao |
|:--------------------------------|-------------:|
| bur_score_02                    |   -0.305193  |
| bur_score_01                    |   -0.224621  |
| pag_qtd_faturas_geral           |   -0.104181  |
| cad_var_05                      |   -0.103676  |
| pag_flag_sem_pagamento_l30d     |    0.0993391 |
| tel_var_28                      |    0.0992972 |
| pag_dias_desde_ultimo_pagamento |    0.0992828 |
| pag_flag_sem_pagamento_l60d     |    0.0957088 |
| pag_qtd_faturas_l90d            |   -0.0934844 |
| pag_flag_sem_pagamento_l90d     |    0.0919605 |
| pag_qtd_faturas_l60d            |   -0.0882341 |
| tel_var_31                      |    0.087449  |
| cad_var_02                      |    0.0859616 |
| tel_var_30                      |    0.0766779 |
| atr_qtd_faturas_atrasadas_geral |   -0.0757858 |

---

### 📊 Sumário Estatístico dos Scores de Bureau
> Análise de quartis e dispersão para validação da saúde dos scores de entrada.

| feature      |   min |   p25 |   median |     avg |   p75 |   max |      std |
|:-------------|------:|------:|---------:|--------:|------:|------:|---------:|
| bur_score_01 |     0 |   558 |      593 | 590.948 |   626 |   778 |  56.3142 |
| bur_score_02 |     1 |   575 |      653 | 651.013 |   731 |   926 | 101.717  |

---

