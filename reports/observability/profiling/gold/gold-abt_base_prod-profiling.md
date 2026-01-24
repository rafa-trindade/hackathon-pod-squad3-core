# Relatório de Profiling: `gold/abt_base_prod` - `20260124_020926`

### ⚙️ Sumário Técnico do Dataset: `abt_base_prod`

- **Volume de Registros (N):** 1.321.168
- **Cardinalidade (CPF):** 1.272.095
- **Grão Definido:** `num_cpf, safra, prod`

---

### 🎯 Distribuição da Variável Alvo (Target): `abt_base_prod`

| fpd   |   frequencia | percentual   |
|:------|-------------:|:-------------|
| False |      1006838 | 76.21%       |
| True  |       314330 | 23.79%       |

---

### 🔑 Verificação de Chave Técnica: `abt_base_prod`
|   pk_distintos |   duplicatas_reais | pct_duplicidade   |
|---------------:|-------------------:|:------------------|
|        1321168 |                  0 | 0.0%              |

---

### 🔍 Perfil de Missings por Feature: `abt_base_prod`

| column_name                       | column_type              | pct_missing   |
|:----------------------------------|:-------------------------|:--------------|
| num_cpf                           | VARCHAR                  | 0.0%          |
| safra                             | DATE                     | 0.0%          |
| prod                              | VARCHAR                  | 0.0%          |
| fpd                               | BOOLEAN                  | 0.0%          |
| rec_qtd_l30d                      | BIGINT                   | 0.0%          |
| rec_qtd_l60d                      | BIGINT                   | 0.0%          |
| rec_qtd_l90d                      | BIGINT                   | 0.0%          |
| rec_qtd_geral                     | BIGINT                   | 0.0%          |
| rec_vlr_total_l30d                | DOUBLE                   | 18.73%        |
| rec_vlr_total_l60d                | DOUBLE                   | 8.02%         |
| rec_vlr_total_l90d                | DOUBLE                   | 4.59%         |
| rec_vlr_total_geral               | DOUBLE                   | 2.96%         |
| rec_vlr_avg_l30d                  | DOUBLE                   | 18.73%        |
| rec_vlr_avg_l60d                  | DOUBLE                   | 8.02%         |
| rec_vlr_avg_l90d                  | DOUBLE                   | 4.59%         |
| rec_vlr_avg_geral                 | DOUBLE                   | 2.96%         |
| rec_vlr_min_l30d                  | DOUBLE                   | 18.73%        |
| rec_vlr_min_l60d                  | DOUBLE                   | 8.02%         |
| rec_vlr_min_l90d                  | DOUBLE                   | 4.59%         |
| rec_vlr_min_geral                 | DOUBLE                   | 2.96%         |
| rec_vlr_max_l30d                  | DOUBLE                   | 18.73%        |
| rec_vlr_max_l60d                  | DOUBLE                   | 8.02%         |
| rec_vlr_max_l90d                  | DOUBLE                   | 4.59%         |
| rec_vlr_max_geral                 | DOUBLE                   | 2.96%         |
| rec_dat_primeira                  | DATE                     | 2.96%         |
| rec_dat_ultima                    | DATE                     | 2.96%         |
| rec_qtd_canais_distintos          | BIGINT                   | 0.0%          |
| rec_dias_desde_ultima             | BIGINT                   | 2.96%         |
| rec_dias_desde_primeira           | BIGINT                   | 2.96%         |
| rec_vlr_std_l30d                  | DOUBLE                   | 39.83%        |
| rec_vlr_std_l60d                  | DOUBLE                   | 18.42%        |
| rec_vlr_std_l90d                  | DOUBLE                   | 11.17%        |
| rec_vlr_std_geral                 | DOUBLE                   | 4.65%         |
| rec_vlr_coef_var_l30d             | DOUBLE                   | 46.97%        |
| rec_vlr_coef_var_l60d             | DOUBLE                   | 27.82%        |
| rec_vlr_coef_var_l90d             | DOUBLE                   | 20.58%        |
| rec_ratio_qtd_l30d_l60d           | DOUBLE                   | 8.02%         |
| rec_ratio_qtd_l60d_l90d           | DOUBLE                   | 4.59%         |
| rec_ratio_vlr_l30d_l60d           | DOUBLE                   | 30.51%        |
| rec_ratio_vlr_l60d_l90d           | DOUBLE                   | 20.49%        |
| rec_flag_sem_recarga_l30d         | INTEGER                  | 0.0%          |
| rec_flag_sem_recarga_l60d         | INTEGER                  | 0.0%          |
| rec_flag_sem_recarga_l90d         | INTEGER                  | 0.0%          |
| pag_vlr_total_l30d                | DOUBLE                   | 85.19%        |
| pag_vlr_total_l60d                | DOUBLE                   | 81.41%        |
| pag_vlr_total_l90d                | DOUBLE                   | 80.06%        |
| pag_vlr_total_geral               | DOUBLE                   | 77.74%        |
| pag_vlr_avg_l30d                  | DOUBLE                   | 85.19%        |
| pag_vlr_avg_l60d                  | DOUBLE                   | 81.41%        |
| pag_vlr_avg_l90d                  | DOUBLE                   | 80.06%        |
| pag_vlr_avg_geral                 | DOUBLE                   | 77.74%        |
| pag_vlr_min_l30d                  | DOUBLE                   | 85.19%        |
| pag_vlr_min_l60d                  | DOUBLE                   | 81.41%        |
| pag_vlr_min_l90d                  | DOUBLE                   | 80.06%        |
| pag_vlr_min_geral                 | DOUBLE                   | 77.74%        |
| pag_vlr_max_l30d                  | DOUBLE                   | 85.19%        |
| pag_vlr_max_l60d                  | DOUBLE                   | 81.41%        |
| pag_vlr_max_l90d                  | DOUBLE                   | 80.06%        |
| pag_vlr_max_geral                 | DOUBLE                   | 77.74%        |
| pag_qtd_faturas_l30d              | BIGINT                   | 0.0%          |
| pag_qtd_faturas_l60d              | BIGINT                   | 0.0%          |
| pag_qtd_faturas_l90d              | BIGINT                   | 0.0%          |
| pag_qtd_faturas_geral             | BIGINT                   | 0.0%          |
| pag_qtd_vezes_com_juros           | BIGINT                   | 0.0%          |
| pag_dias_desde_ultimo_pagamento   | BIGINT                   | 77.74%        |
| pag_ticket_medio_l30d             | DOUBLE                   | 85.19%        |
| pag_ticket_medio_l60d             | DOUBLE                   | 81.41%        |
| pag_ticket_medio_l90d             | DOUBLE                   | 80.06%        |
| pag_ticket_medio_geral            | DOUBLE                   | 77.74%        |
| pag_share_faturas_com_juros_l30d  | DOUBLE                   | 85.19%        |
| pag_share_faturas_com_juros_l60d  | DOUBLE                   | 81.41%        |
| pag_share_faturas_com_juros_l90d  | DOUBLE                   | 80.06%        |
| pag_share_faturas_com_juros_geral | DOUBLE                   | 77.74%        |
| pag_vlr_std_l30d                  | DOUBLE                   | 93.82%        |
| pag_vlr_std_l60d                  | DOUBLE                   | 85.09%        |
| pag_vlr_std_l90d                  | DOUBLE                   | 82.27%        |
| pag_flag_sem_pagamento_l30d       | INTEGER                  | 0.0%          |
| pag_flag_sem_pagamento_l60d       | INTEGER                  | 0.0%          |
| pag_flag_sem_pagamento_l90d       | INTEGER                  | 0.0%          |
| atr_vlr_max_l30d                  | DOUBLE                   | 89.09%        |
| atr_vlr_max_l60d                  | DOUBLE                   | 77.75%        |
| atr_vlr_max_l90d                  | DOUBLE                   | 76.47%        |
| atr_vlr_max_geral                 | DOUBLE                   | 74.56%        |
| atr_vlr_acumulado_l30d            | DOUBLE                   | 89.09%        |
| atr_vlr_acumulado_l60d            | DOUBLE                   | 77.75%        |
| atr_vlr_acumulado_l90d            | DOUBLE                   | 76.47%        |
| atr_vlr_acumulado_geral           | DOUBLE                   | 74.56%        |
| atr_qtd_faturas_atrasadas_l30d    | BIGINT                   | 0.0%          |
| atr_qtd_faturas_atrasadas_l60d    | BIGINT                   | 0.0%          |
| atr_qtd_faturas_atrasadas_l90d    | BIGINT                   | 0.0%          |
| atr_qtd_faturas_atrasadas_geral   | BIGINT                   | 0.0%          |
| atr_dat_ultima_ref                | DATE                     | 74.56%        |
| atr_dias_desde_ultimo_atraso      | BIGINT                   | 74.56%        |
| atr_ticket_medio_l30d             | DOUBLE                   | 89.09%        |
| atr_ticket_medio_l60d             | DOUBLE                   | 77.75%        |
| atr_ticket_medio_l90d             | DOUBLE                   | 76.47%        |
| atr_ticket_medio_geral            | DOUBLE                   | 74.56%        |
| atr_flag_recorrente_l30d          | INTEGER                  | 0.0%          |
| atr_flag_recorrente_l60d          | INTEGER                  | 0.0%          |
| atr_flag_recorrente_l90d          | INTEGER                  | 0.0%          |
| atr_flag_atraso_l30d              | INTEGER                  | 0.0%          |
| atr_flag_atraso_l60d              | INTEGER                  | 0.0%          |
| atr_flag_atraso_l90d              | INTEGER                  | 0.0%          |
| bur_flag_mig2                     | VARCHAR                  | 0.92%         |
| bur_score_01                      | INTEGER                  | 1.64%         |
| bur_score_02                      | INTEGER                  | 0.97%         |
| cad_cep_3_digitos                 | VARCHAR                  | 5.9%          |
| cad_datadenascimento              | DATE                     | 0.15%         |
| cad_flag_mig2                     | VARCHAR                  | 0.92%         |
| cad_statusrf                      | VARCHAR                  | 0.11%         |
| cad_var_02                        | INTEGER                  | 94.42%        |
| cad_var_03                        | INTEGER                  | 6.58%         |
| cad_var_04                        | INTEGER                  | 0.11%         |
| cad_var_05                        | INTEGER                  | 4.24%         |
| cad_var_06                        | INTEGER                  | 80.83%        |
| cad_var_07                        | DOUBLE                   | 83.3%         |
| cad_var_08                        | INTEGER                  | 80.83%        |
| cad_var_09                        | INTEGER                  | 53.38%        |
| cad_var_10                        | VARCHAR                  | 98.89%        |
| cad_var_11                        | DOUBLE                   | 98.95%        |
| cad_var_12                        | DATE                     | 38.33%        |
| cad_var_13                        | DATE                     | 84.62%        |
| cad_var_14                        | INTEGER                  | 92.27%        |
| cad_var_15                        | VARCHAR                  | 82.39%        |
| cad_var_16                        | INTEGER                  | 82.39%        |
| cad_var_17                        | INTEGER                  | 82.39%        |
| cad_var_18                        | VARCHAR                  | 80.83%        |
| cad_var_19                        | VARCHAR                  | 53.38%        |
| cad_var_20                        | VARCHAR                  | 98.71%        |
| cad_var_21                        | VARCHAR                  | 38.33%        |
| cad_var_22                        | VARCHAR                  | 92.27%        |
| cad_var_23                        | VARCHAR                  | 82.39%        |
| cad_var_24                        | VARCHAR                  | 38.33%        |
| cad_var_25                        | VARCHAR                  | 10.33%        |
| tel_flag_mig2                     | VARCHAR                  | 0.92%         |
| tel_var_26                        | VARCHAR                  | 0.09%         |
| tel_var_27                        | VARCHAR                  | 0.09%         |
| tel_var_28                        | DOUBLE                   | 0.09%         |
| tel_var_29                        | DOUBLE                   | 0.09%         |
| tel_var_30                        | DOUBLE                   | 0.09%         |
| tel_var_31                        | DOUBLE                   | 0.09%         |
| tel_var_32                        | DOUBLE                   | 0.09%         |
| tel_var_33                        | DOUBLE                   | 0.09%         |
| tel_var_34                        | DOUBLE                   | 0.09%         |
| tel_var_35                        | DOUBLE                   | 0.09%         |
| tel_var_36                        | DOUBLE                   | 0.09%         |
| tel_var_37                        | DOUBLE                   | 0.09%         |
| tel_var_38                        | DOUBLE                   | 0.09%         |
| tel_var_39                        | DOUBLE                   | 0.09%         |
| tel_var_40                        | DOUBLE                   | 0.09%         |
| tel_var_41                        | DOUBLE                   | 0.09%         |
| tel_var_42                        | DOUBLE                   | 0.09%         |
| tel_var_43                        | DOUBLE                   | 0.09%         |
| tel_var_44                        | DOUBLE                   | 0.09%         |
| tel_var_45                        | DOUBLE                   | 0.09%         |
| tel_var_46                        | DOUBLE                   | 0.09%         |
| tel_var_47                        | DOUBLE                   | 0.09%         |
| tel_var_48                        | DOUBLE                   | 0.09%         |
| tel_var_49                        | DOUBLE                   | 0.09%         |
| tel_var_50                        | DOUBLE                   | 0.09%         |
| tel_var_51                        | DOUBLE                   | 0.09%         |
| tel_var_52                        | DOUBLE                   | 0.09%         |
| tel_var_53                        | DOUBLE                   | 0.09%         |
| tel_var_54                        | DOUBLE                   | 0.09%         |
| tel_var_55                        | DOUBLE                   | 0.09%         |
| tel_var_56                        | DOUBLE                   | 0.09%         |
| tel_var_57                        | DOUBLE                   | 0.09%         |
| tel_var_58                        | DOUBLE                   | 0.09%         |
| tel_var_59                        | DOUBLE                   | 0.09%         |
| tel_var_60                        | DOUBLE                   | 0.09%         |
| tel_var_61                        | DOUBLE                   | 0.09%         |
| tel_var_62                        | DOUBLE                   | 0.09%         |
| tel_var_63                        | DOUBLE                   | 0.09%         |
| tel_var_64                        | VARCHAR                  | 0.09%         |
| tel_var_65                        | VARCHAR                  | 0.09%         |
| tel_var_66                        | VARCHAR                  | 0.09%         |
| tel_var_67                        | VARCHAR                  | 0.09%         |
| tel_var_68                        | DOUBLE                   | 0.09%         |
| tel_var_69                        | DOUBLE                   | 0.09%         |
| tel_var_70                        | DOUBLE                   | 0.09%         |
| tel_var_71                        | DOUBLE                   | 0.09%         |
| tel_var_72                        | DOUBLE                   | 0.09%         |
| tel_var_73                        | VARCHAR                  | 0.09%         |
| tel_var_74                        | VARCHAR                  | 0.09%         |
| tel_var_75                        | VARCHAR                  | 0.09%         |
| tel_var_76                        | VARCHAR                  | 0.09%         |
| tel_var_77                        | VARCHAR                  | 0.09%         |
| tel_var_78                        | VARCHAR                  | 0.0%          |
| tel_var_79                        | VARCHAR                  | 0.0%          |
| tel_var_80                        | VARCHAR                  | 0.0%          |
| tel_var_81                        | VARCHAR                  | 0.0%          |
| tel_var_82                        | DOUBLE                   | 0.0%          |
| tel_var_83                        | VARCHAR                  | 0.0%          |
| tel_var_84                        | VARCHAR                  | 0.0%          |
| tel_var_85                        | VARCHAR                  | 0.0%          |
| tel_var_86                        | VARCHAR                  | 0.0%          |
| tel_var_87                        | VARCHAR                  | 0.0%          |
| tel_var_88                        | VARCHAR                  | 0.0%          |
| tel_var_89                        | VARCHAR                  | 0.0%          |
| tel_var_90                        | DOUBLE                   | 0.0%          |
| tel_var_91                        | VARCHAR                  | 0.0%          |
| tel_var_92                        | VARCHAR                  | 0.0%          |
| tel_var_93                        | VARCHAR                  | 0.0%          |
| run_id                            | VARCHAR                  | 0.0%          |
| ingestion_ts                      | TIMESTAMP WITH TIME ZONE | 0.0%          |
| ano_mes                           | BIGINT                   | 0.0%          |

---

### 🚩 Detecção de Anomalias Financeiras (Outliers > 3σ): `abt_base_prod`

| Feature                           | Max Value     | Threshold (3σ)   | Status              |
|:----------------------------------|:--------------|:-----------------|:--------------------|
| rec_qtd_l30d                      | 260,00        | 12,21            | ⚠️ Outlier Detected |
| rec_qtd_l60d                      | 511,00        | 22,21            | ⚠️ Outlier Detected |
| rec_qtd_l90d                      | 737,00        | 31,97            | ⚠️ Outlier Detected |
| rec_qtd_geral                     | 3.384,00      | 131,28           | ⚠️ Outlier Detected |
| rec_vlr_total_l30d                | 50.000,00     | 236,36           | ⚠️ Outlier Detected |
| rec_vlr_total_l60d                | 50.060,00     | 359,77           | ⚠️ Outlier Detected |
| rec_vlr_total_l90d                | 75.100,00     | 536,05           | ⚠️ Outlier Detected |
| rec_vlr_total_geral               | 425.010,00    | 2.969,53         | ⚠️ Outlier Detected |
| rec_vlr_avg_l30d                  | 8.338,33      | 58,10            | ⚠️ Outlier Detected |
| rec_vlr_avg_l60d                  | 8.338,33      | 51,65            | ⚠️ Outlier Detected |
| rec_vlr_avg_l90d                  | 8.336,67      | 48,81            | ⚠️ Outlier Detected |
| rec_vlr_avg_geral                 | 11.000,80     | 67,94            | ⚠️ Outlier Detected |
| rec_vlr_min_l30d                  | 109,76        | 32,58            | ⚠️ Outlier Detected |
| rec_vlr_min_l60d                  | 100,00        | 25,14            | ⚠️ Outlier Detected |
| rec_vlr_min_l90d                  | 100,00        | 20,66            | ⚠️ Outlier Detected |
| rec_vlr_min_geral                 | 100,00        | 12,01            | ⚠️ Outlier Detected |
| rec_vlr_max_l30d                  | 25.000,00     | 151,64           | ⚠️ Outlier Detected |
| rec_vlr_max_l60d                  | 25.000,00     | 179,04           | ⚠️ Outlier Detected |
| rec_vlr_max_l90d                  | 25.000,00     | 177,47           | ⚠️ Outlier Detected |
| rec_vlr_max_geral                 | 25.000,00     | 260,67           | ⚠️ Outlier Detected |
| rec_qtd_canais_distintos          | 38,00         | 11,47            | ⚠️ Outlier Detected |
| rec_dias_desde_ultima             | 515,00        | 90,65            | ⚠️ Outlier Detected |
| rec_vlr_std_l30d                  | 14.429,43     | 92,71            | ⚠️ Outlier Detected |
| rec_vlr_std_l60d                  | 12.906,07     | 82,46            | ⚠️ Outlier Detected |
| rec_vlr_std_l90d                  | 12.497,50     | 76,56            | ⚠️ Outlier Detected |
| rec_vlr_std_geral                 | 12.664,85     | 107,68           | ⚠️ Outlier Detected |
| rec_vlr_coef_var_l30d             | 16,12         | 2,86             | ⚠️ Outlier Detected |
| rec_vlr_coef_var_l60d             | 20,54         | 3,01             | ⚠️ Outlier Detected |
| rec_vlr_coef_var_l90d             | 26,12         | 3,13             | ⚠️ Outlier Detected |
| rec_flag_sem_recarga_l60d         | 1,00          | 0,89             | ⚠️ Outlier Detected |
| rec_flag_sem_recarga_l90d         | 1,00          | 0,67             | ⚠️ Outlier Detected |
| pag_vlr_total_l30d                | 139.017,45    | 1.245,77         | ⚠️ Outlier Detected |
| pag_vlr_total_l60d                | 328.986,24    | 2.506,39         | ⚠️ Outlier Detected |
| pag_vlr_total_l90d                | 328.986,24    | 3.059,87         | ⚠️ Outlier Detected |
| pag_vlr_total_geral               | 803.165,27    | 12.409,07        | ⚠️ Outlier Detected |
| pag_vlr_avg_l30d                  | 46.339,15     | 637,89           | ⚠️ Outlier Detected |
| pag_vlr_avg_l60d                  | 54.831,04     | 621,61           | ⚠️ Outlier Detected |
| pag_vlr_avg_l90d                  | 54.831,04     | 633,05           | ⚠️ Outlier Detected |
| pag_vlr_avg_geral                 | 42.651,46     | 622,16           | ⚠️ Outlier Detected |
| pag_vlr_min_l30d                  | 34.646,53     | 561,25           | ⚠️ Outlier Detected |
| pag_vlr_min_l60d                  | 34.646,53     | 508,85           | ⚠️ Outlier Detected |
| pag_vlr_min_l90d                  | 34.646,53     | 496,79           | ⚠️ Outlier Detected |
| pag_vlr_min_geral                 | 15.599,98     | 196,89           | ⚠️ Outlier Detected |
| pag_vlr_max_l30d                  | 52.961,90     | 769,22           | ⚠️ Outlier Detected |
| pag_vlr_max_l60d                  | 64.962,03     | 839,72           | ⚠️ Outlier Detected |
| pag_vlr_max_l90d                  | 64.962,03     | 970,79           | ⚠️ Outlier Detected |
| pag_vlr_max_geral                 | 72.709,30     | 1.296,67         | ⚠️ Outlier Detected |
| pag_qtd_faturas_l30d              | 18,00         | 1,93             | ⚠️ Outlier Detected |
| pag_qtd_faturas_l60d              | 24,00         | 3,34             | ⚠️ Outlier Detected |
| pag_qtd_faturas_l90d              | 33,00         | 4,79             | ⚠️ Outlier Detected |
| pag_qtd_faturas_geral             | 88,00         | 20,51            | ⚠️ Outlier Detected |
| pag_qtd_vezes_com_juros           | 252,00        | 15,84            | ⚠️ Outlier Detected |
| pag_dias_desde_ultimo_pagamento   | 516,00        | 193,18           | ⚠️ Outlier Detected |
| pag_ticket_medio_l30d             | 46.339,15     | 682,03           | ⚠️ Outlier Detected |
| pag_ticket_medio_l60d             | 54.831,04     | 665,19           | ⚠️ Outlier Detected |
| pag_ticket_medio_l90d             | 54.831,04     | 683,88           | ⚠️ Outlier Detected |
| pag_ticket_medio_geral            | 42.651,46     | 720,88           | ⚠️ Outlier Detected |
| pag_share_faturas_com_juros_l30d  | 6,00          | 2,34             | ⚠️ Outlier Detected |
| pag_share_faturas_com_juros_l60d  | 6,00          | 2,25             | ⚠️ Outlier Detected |
| pag_share_faturas_com_juros_l90d  | 5,33          | 2,18             | ⚠️ Outlier Detected |
| pag_share_faturas_com_juros_geral | 6,43          | 1,96             | ⚠️ Outlier Detected |
| pag_vlr_std_l30d                  | 23.602,64     | 429,25           | ⚠️ Outlier Detected |
| pag_vlr_std_l60d                  | 15.872,00     | 304,61           | ⚠️ Outlier Detected |
| pag_vlr_std_l90d                  | 21.713,19     | 323,51           | ⚠️ Outlier Detected |
| atr_vlr_max_l30d                  | 509.114,06    | 4.217,37         | ⚠️ Outlier Detected |
| atr_vlr_max_l60d                  | 509.114,06    | 3.043,15         | ⚠️ Outlier Detected |
| atr_vlr_max_l90d                  | 509.114,06    | 2.988,05         | ⚠️ Outlier Detected |
| atr_vlr_max_geral                 | 509.114,06    | 3.024,04         | ⚠️ Outlier Detected |
| atr_vlr_acumulado_l30d            | 3.439.561,25  | 27.365,30        | ⚠️ Outlier Detected |
| atr_vlr_acumulado_l60d            | 6.879.122,50  | 38.286,95        | ⚠️ Outlier Detected |
| atr_vlr_acumulado_l90d            | 10.318.683,75 | 55.990,50        | ⚠️ Outlier Detected |
| atr_vlr_acumulado_geral           | 55.931.388,30 | 293.518,65       | ⚠️ Outlier Detected |
| atr_qtd_faturas_atrasadas_l30d    | 57,00         | 2,35             | ⚠️ Outlier Detected |
| atr_qtd_faturas_atrasadas_l60d    | 111,00        | 3,57             | ⚠️ Outlier Detected |
| atr_qtd_faturas_atrasadas_l90d    | 111,00        | 4,69             | ⚠️ Outlier Detected |
| atr_qtd_faturas_atrasadas_geral   | 250,00        | 20,83            | ⚠️ Outlier Detected |
| atr_dias_desde_ultimo_atraso      | 517,00        | 237,83           | ⚠️ Outlier Detected |
| atr_ticket_medio_l30d             | 163.788,63    | 1.418,37         | ⚠️ Outlier Detected |
| atr_ticket_medio_l60d             | 327.577,26    | 1.980,23         | ⚠️ Outlier Detected |
| atr_ticket_medio_l90d             | 491.365,89    | 2.844,63         | ⚠️ Outlier Detected |
| atr_ticket_medio_geral            | 2.663.399,44  | 14.343,44        | ⚠️ Outlier Detected |
| atr_flag_recorrente_l30d          | 1,00          | 0,63             | ⚠️ Outlier Detected |
| atr_flag_recorrente_l60d          | 1,00          | 0,99             | ⚠️ Outlier Detected |

---

### 📦 Volumetria: `abt_base_prod`
| diretorio      |   qtd_arquivos | registros   |   colunas |   tamanho_comprimido_mib |   tamanho_descomprimido_mib |
|:---------------|---------------:|:------------|----------:|-------------------------:|----------------------------:|
| ano_mes=202410 |              1 | 207.953     |       206 |                    35.6  |                       45.39 |
| ano_mes=202411 |              1 | 231.824     |       206 |                    38.66 |                       50.47 |
| ano_mes=202412 |              1 | 232.984     |       206 |                    39.11 |                       50.07 |
| ano_mes=202501 |              1 | 226.446     |       206 |                    38.98 |                       50.69 |
| ano_mes=202502 |              1 | 208.731     |       206 |                    35.42 |                       45.46 |
| ano_mes=202503 |              1 | 213.230     |       206 |                    37.72 |                       48.43 |
| TOTAL          |              6 | 1.321.168   |       206 |                   225.49 |                      290.5  |

---

