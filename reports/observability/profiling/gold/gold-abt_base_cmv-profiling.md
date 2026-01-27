# Relatório de Profiling: `gold/abt_base_cmv` - `20260127_150607`

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
| rec_qtd_l30d                      | BIGINT                   | 50.3%         |
| rec_qtd_l60d                      | BIGINT                   | 50.3%         |
| rec_qtd_l90d                      | BIGINT                   | 50.3%         |
| rec_qtd_geral                     | BIGINT                   | 50.3%         |
| rec_vlr_total_l30d                | DOUBLE                   | 59.62%        |
| rec_vlr_total_l60d                | DOUBLE                   | 54.28%        |
| rec_vlr_total_l90d                | DOUBLE                   | 52.57%        |
| rec_vlr_total_geral               | DOUBLE                   | 51.76%        |
| rec_vlr_avg_l30d                  | DOUBLE                   | 59.62%        |
| rec_vlr_avg_l60d                  | DOUBLE                   | 54.28%        |
| rec_vlr_avg_l90d                  | DOUBLE                   | 52.57%        |
| rec_vlr_avg_geral                 | DOUBLE                   | 51.76%        |
| rec_vlr_min_l30d                  | DOUBLE                   | 59.62%        |
| rec_vlr_min_l60d                  | DOUBLE                   | 54.28%        |
| rec_vlr_min_l90d                  | DOUBLE                   | 52.57%        |
| rec_vlr_min_geral                 | DOUBLE                   | 51.76%        |
| rec_vlr_max_l30d                  | DOUBLE                   | 59.62%        |
| rec_vlr_max_l60d                  | DOUBLE                   | 54.28%        |
| rec_vlr_max_l90d                  | DOUBLE                   | 52.57%        |
| rec_vlr_max_geral                 | DOUBLE                   | 51.76%        |
| rec_dat_primeira                  | DATE                     | 51.76%        |
| rec_dat_ultima                    | DATE                     | 51.76%        |
| rec_qtd_canais_distintos          | BIGINT                   | 50.3%         |
| rec_dias_desde_ultima             | BIGINT                   | 51.76%        |
| rec_dias_desde_primeira           | BIGINT                   | 51.76%        |
| rec_vlr_std_l30d                  | DOUBLE                   | 70.12%        |
| rec_vlr_std_l60d                  | DOUBLE                   | 59.47%        |
| rec_vlr_std_l90d                  | DOUBLE                   | 55.86%        |
| rec_vlr_std_geral                 | DOUBLE                   | 52.6%         |
| rec_vlr_coef_var_l30d             | DOUBLE                   | 73.57%        |
| rec_vlr_coef_var_l60d             | DOUBLE                   | 64.06%        |
| rec_vlr_coef_var_l90d             | DOUBLE                   | 60.47%        |
| rec_ratio_qtd_l30d_l60d           | DOUBLE                   | 54.28%        |
| rec_ratio_qtd_l60d_l90d           | DOUBLE                   | 52.57%        |
| rec_ratio_vlr_l30d_l60d           | DOUBLE                   | 65.4%         |
| rec_ratio_vlr_l60d_l90d           | DOUBLE                   | 60.43%        |
| rec_flag_sem_recarga_l30d         | INTEGER                  | 50.3%         |
| rec_flag_sem_recarga_l60d         | INTEGER                  | 50.3%         |
| rec_flag_sem_recarga_l90d         | INTEGER                  | 50.3%         |
| pag_vlr_total_l30d                | DOUBLE                   | 92.72%        |
| pag_vlr_total_l60d                | DOUBLE                   | 90.85%        |
| pag_vlr_total_l90d                | DOUBLE                   | 90.18%        |
| pag_vlr_total_geral               | DOUBLE                   | 89.03%        |
| pag_vlr_avg_l30d                  | DOUBLE                   | 92.72%        |
| pag_vlr_avg_l60d                  | DOUBLE                   | 90.85%        |
| pag_vlr_avg_l90d                  | DOUBLE                   | 90.18%        |
| pag_vlr_avg_geral                 | DOUBLE                   | 89.03%        |
| pag_vlr_min_l30d                  | DOUBLE                   | 92.72%        |
| pag_vlr_min_l60d                  | DOUBLE                   | 90.85%        |
| pag_vlr_min_l90d                  | DOUBLE                   | 90.18%        |
| pag_vlr_min_geral                 | DOUBLE                   | 89.03%        |
| pag_vlr_max_l30d                  | DOUBLE                   | 92.72%        |
| pag_vlr_max_l60d                  | DOUBLE                   | 90.85%        |
| pag_vlr_max_l90d                  | DOUBLE                   | 90.18%        |
| pag_vlr_max_geral                 | DOUBLE                   | 89.03%        |
| pag_qtd_faturas_l30d              | BIGINT                   | 50.3%         |
| pag_qtd_faturas_l60d              | BIGINT                   | 50.3%         |
| pag_qtd_faturas_l90d              | BIGINT                   | 50.3%         |
| pag_qtd_faturas_geral             | BIGINT                   | 50.3%         |
| pag_qtd_vezes_com_juros           | BIGINT                   | 50.3%         |
| pag_dias_desde_ultimo_pagamento   | BIGINT                   | 89.03%        |
| pag_ticket_medio_l30d             | DOUBLE                   | 92.72%        |
| pag_ticket_medio_l60d             | DOUBLE                   | 90.85%        |
| pag_ticket_medio_l90d             | DOUBLE                   | 90.18%        |
| pag_ticket_medio_geral            | DOUBLE                   | 89.03%        |
| pag_share_faturas_com_juros_l30d  | DOUBLE                   | 92.72%        |
| pag_share_faturas_com_juros_l60d  | DOUBLE                   | 90.85%        |
| pag_share_faturas_com_juros_l90d  | DOUBLE                   | 90.18%        |
| pag_share_faturas_com_juros_geral | DOUBLE                   | 89.03%        |
| pag_vlr_std_l30d                  | DOUBLE                   | 96.96%        |
| pag_vlr_std_l60d                  | DOUBLE                   | 92.64%        |
| pag_vlr_std_l90d                  | DOUBLE                   | 91.24%        |
| pag_flag_sem_pagamento_l30d       | INTEGER                  | 50.3%         |
| pag_flag_sem_pagamento_l60d       | INTEGER                  | 50.3%         |
| pag_flag_sem_pagamento_l90d       | INTEGER                  | 50.3%         |
| atr_vlr_max_l30d                  | DOUBLE                   | 94.62%        |
| atr_vlr_max_l60d                  | DOUBLE                   | 89.03%        |
| atr_vlr_max_l90d                  | DOUBLE                   | 88.4%         |
| atr_vlr_max_geral                 | DOUBLE                   | 87.45%        |
| atr_vlr_acumulado_l30d            | DOUBLE                   | 94.62%        |
| atr_vlr_acumulado_l60d            | DOUBLE                   | 89.03%        |
| atr_vlr_acumulado_l90d            | DOUBLE                   | 88.4%         |
| atr_vlr_acumulado_geral           | DOUBLE                   | 87.45%        |
| atr_qtd_faturas_atrasadas_l30d    | BIGINT                   | 50.3%         |
| atr_qtd_faturas_atrasadas_l60d    | BIGINT                   | 50.3%         |
| atr_qtd_faturas_atrasadas_l90d    | BIGINT                   | 50.3%         |
| atr_qtd_faturas_atrasadas_geral   | BIGINT                   | 50.3%         |
| atr_dat_ultima_ref                | DATE                     | 87.45%        |
| atr_dias_desde_ultimo_atraso      | BIGINT                   | 87.45%        |
| atr_ticket_medio_l30d             | DOUBLE                   | 94.62%        |
| atr_ticket_medio_l60d             | DOUBLE                   | 89.03%        |
| atr_ticket_medio_l90d             | DOUBLE                   | 88.4%         |
| atr_ticket_medio_geral            | DOUBLE                   | 87.45%        |
| atr_flag_recorrente_l30d          | INTEGER                  | 50.3%         |
| atr_flag_recorrente_l60d          | INTEGER                  | 50.3%         |
| atr_flag_recorrente_l90d          | INTEGER                  | 50.3%         |
| atr_flag_atraso_l30d              | INTEGER                  | 50.3%         |
| atr_flag_atraso_l60d              | INTEGER                  | 50.3%         |
| atr_flag_atraso_l90d              | INTEGER                  | 50.3%         |
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
| run_id                            | VARCHAR                  | 0.0%          |
| ingestion_ts                      | TIMESTAMP WITH TIME ZONE | 0.0%          |
| ano_mes                           | BIGINT                   | 0.0%          |

---

### 🚩 Detecção de Anomalias Financeiras (Outliers > 3σ): `abt_base_cmv`

| Feature                           | Max Value     | Threshold (3σ)   | Status              |
|:----------------------------------|:--------------|:-----------------|:--------------------|
| rec_qtd_l30d                      | 260,00        | 12,22            | ⚠️ Outlier Detected |
| rec_qtd_l60d                      | 511,00        | 22,23            | ⚠️ Outlier Detected |
| rec_qtd_l90d                      | 737,00        | 31,98            | ⚠️ Outlier Detected |
| rec_qtd_geral                     | 3.384,00      | 131,02           | ⚠️ Outlier Detected |
| rec_vlr_total_l30d                | 50.000,00     | 237,20           | ⚠️ Outlier Detected |
| rec_vlr_total_l60d                | 50.060,00     | 360,87           | ⚠️ Outlier Detected |
| rec_vlr_total_l90d                | 75.100,00     | 537,71           | ⚠️ Outlier Detected |
| rec_vlr_total_geral               | 425.000,00    | 2.980,02         | ⚠️ Outlier Detected |
| rec_vlr_avg_l30d                  | 8.338,33      | 58,29            | ⚠️ Outlier Detected |
| rec_vlr_avg_l60d                  | 8.338,33      | 51,81            | ⚠️ Outlier Detected |
| rec_vlr_avg_l90d                  | 8.336,67      | 48,96            | ⚠️ Outlier Detected |
| rec_vlr_avg_geral                 | 11.000,80     | 68,18            | ⚠️ Outlier Detected |
| rec_vlr_min_l30d                  | 109,76        | 32,67            | ⚠️ Outlier Detected |
| rec_vlr_min_l60d                  | 100,00        | 25,21            | ⚠️ Outlier Detected |
| rec_vlr_min_l90d                  | 100,00        | 20,71            | ⚠️ Outlier Detected |
| rec_vlr_min_geral                 | 100,00        | 12,02            | ⚠️ Outlier Detected |
| rec_vlr_max_l30d                  | 25.000,00     | 152,25           | ⚠️ Outlier Detected |
| rec_vlr_max_l60d                  | 25.000,00     | 179,74           | ⚠️ Outlier Detected |
| rec_vlr_max_l90d                  | 25.000,00     | 178,13           | ⚠️ Outlier Detected |
| rec_vlr_max_geral                 | 25.000,00     | 261,68           | ⚠️ Outlier Detected |
| rec_qtd_canais_distintos          | 38,00         | 11,46            | ⚠️ Outlier Detected |
| rec_dias_desde_ultima             | 515,00        | 90,68            | ⚠️ Outlier Detected |
| rec_vlr_std_l30d                  | 14.429,43     | 93,11            | ⚠️ Outlier Detected |
| rec_vlr_std_l60d                  | 12.906,07     | 82,81            | ⚠️ Outlier Detected |
| rec_vlr_std_l90d                  | 12.497,50     | 76,85            | ⚠️ Outlier Detected |
| rec_vlr_std_geral                 | 12.664,85     | 108,11           | ⚠️ Outlier Detected |
| rec_vlr_coef_var_l30d             | 16,12         | 2,85             | ⚠️ Outlier Detected |
| rec_vlr_coef_var_l60d             | 20,54         | 3,00             | ⚠️ Outlier Detected |
| rec_vlr_coef_var_l90d             | 26,12         | 3,13             | ⚠️ Outlier Detected |
| rec_flag_sem_recarga_l60d         | 1,00          | 0,89             | ⚠️ Outlier Detected |
| rec_flag_sem_recarga_l90d         | 1,00          | 0,67             | ⚠️ Outlier Detected |
| pag_vlr_total_l30d                | 139.017,45    | 1.262,72         | ⚠️ Outlier Detected |
| pag_vlr_total_l60d                | 328.986,24    | 2.603,73         | ⚠️ Outlier Detected |
| pag_vlr_total_l90d                | 328.986,24    | 3.142,66         | ⚠️ Outlier Detected |
| pag_vlr_total_geral               | 796.965,27    | 12.546,71        | ⚠️ Outlier Detected |
| pag_vlr_avg_l30d                  | 46.339,15     | 642,82           | ⚠️ Outlier Detected |
| pag_vlr_avg_l60d                  | 54.831,04     | 630,35           | ⚠️ Outlier Detected |
| pag_vlr_avg_l90d                  | 54.831,04     | 639,39           | ⚠️ Outlier Detected |
| pag_vlr_avg_geral                 | 42.651,46     | 625,90           | ⚠️ Outlier Detected |
| pag_vlr_min_l30d                  | 34.646,53     | 565,00           | ⚠️ Outlier Detected |
| pag_vlr_min_l60d                  | 34.646,53     | 511,33           | ⚠️ Outlier Detected |
| pag_vlr_min_l90d                  | 34.646,53     | 499,15           | ⚠️ Outlier Detected |
| pag_vlr_min_geral                 | 15.599,98     | 198,43           | ⚠️ Outlier Detected |
| pag_vlr_max_l30d                  | 52.961,90     | 775,90           | ⚠️ Outlier Detected |
| pag_vlr_max_l60d                  | 89.194,82     | 1.017,54         | ⚠️ Outlier Detected |
| pag_vlr_max_l90d                  | 89.194,82     | 1.105,89         | ⚠️ Outlier Detected |
| pag_vlr_max_geral                 | 89.194,82     | 1.391,93         | ⚠️ Outlier Detected |
| pag_qtd_faturas_l30d              | 25,00         | 1,93             | ⚠️ Outlier Detected |
| pag_qtd_faturas_l60d              | 25,00         | 3,33             | ⚠️ Outlier Detected |
| pag_qtd_faturas_l90d              | 33,00         | 4,77             | ⚠️ Outlier Detected |
| pag_qtd_faturas_geral             | 88,00         | 20,47            | ⚠️ Outlier Detected |
| pag_qtd_vezes_com_juros           | 260,00        | 15,81            | ⚠️ Outlier Detected |
| pag_dias_desde_ultimo_pagamento   | 516,00        | 194,03           | ⚠️ Outlier Detected |
| pag_ticket_medio_l30d             | 46.339,15     | 687,07           | ⚠️ Outlier Detected |
| pag_ticket_medio_l60d             | 54.831,04     | 680,79           | ⚠️ Outlier Detected |
| pag_ticket_medio_l90d             | 54.831,04     | 695,26           | ⚠️ Outlier Detected |
| pag_ticket_medio_geral            | 42.651,46     | 726,39           | ⚠️ Outlier Detected |
| pag_share_faturas_com_juros_l30d  | 6,00          | 2,34             | ⚠️ Outlier Detected |
| pag_share_faturas_com_juros_l60d  | 6,00          | 2,25             | ⚠️ Outlier Detected |
| pag_share_faturas_com_juros_l90d  | 5,33          | 2,18             | ⚠️ Outlier Detected |
| pag_share_faturas_com_juros_geral | 6,43          | 1,96             | ⚠️ Outlier Detected |
| pag_vlr_std_l30d                  | 23.602,64     | 433,33           | ⚠️ Outlier Detected |
| pag_vlr_std_l60d                  | 31.193,86     | 376,94           | ⚠️ Outlier Detected |
| pag_vlr_std_l90d                  | 27.822,78     | 366,86           | ⚠️ Outlier Detected |
| atr_vlr_max_l30d                  | 509.114,06    | 4.251,21         | ⚠️ Outlier Detected |
| atr_vlr_max_l60d                  | 509.114,06    | 3.068,83         | ⚠️ Outlier Detected |
| atr_vlr_max_l90d                  | 509.114,06    | 3.012,88         | ⚠️ Outlier Detected |
| atr_vlr_max_geral                 | 509.114,06    | 3.048,34         | ⚠️ Outlier Detected |
| atr_vlr_acumulado_l30d            | 3.439.561,25  | 27.588,60        | ⚠️ Outlier Detected |
| atr_vlr_acumulado_l60d            | 6.879.122,50  | 38.619,58        | ⚠️ Outlier Detected |
| atr_vlr_acumulado_l90d            | 10.318.683,75 | 56.470,01        | ⚠️ Outlier Detected |
| atr_vlr_acumulado_geral           | 55.931.388,30 | 295.956,86       | ⚠️ Outlier Detected |
| atr_qtd_faturas_atrasadas_l30d    | 57,00         | 2,34             | ⚠️ Outlier Detected |
| atr_qtd_faturas_atrasadas_l60d    | 111,00        | 3,56             | ⚠️ Outlier Detected |
| atr_qtd_faturas_atrasadas_l90d    | 111,00        | 4,67             | ⚠️ Outlier Detected |
| atr_qtd_faturas_atrasadas_geral   | 250,00        | 20,78            | ⚠️ Outlier Detected |
| atr_dias_desde_ultimo_atraso      | 517,00        | 238,66           | ⚠️ Outlier Detected |
| atr_ticket_medio_l30d             | 163.788,63    | 1.429,32         | ⚠️ Outlier Detected |
| atr_ticket_medio_l60d             | 327.577,26    | 1.996,78         | ⚠️ Outlier Detected |
| atr_ticket_medio_l90d             | 491.365,89    | 2.868,27         | ⚠️ Outlier Detected |
| atr_ticket_medio_geral            | 2.663.399,44  | 14.461,44        | ⚠️ Outlier Detected |
| atr_flag_recorrente_l30d          | 1,00          | 0,63             | ⚠️ Outlier Detected |
| atr_flag_recorrente_l60d          | 1,00          | 0,99             | ⚠️ Outlier Detected |

---

### 📦 Volumetria: `abt_base_cmv`
| diretorio      |   qtd_arquivos | registros   |   colunas |   tamanho_comprimido_mib |   tamanho_descomprimido_mib |
|:---------------|---------------:|:------------|----------:|-------------------------:|----------------------------:|
| ano_mes=202410 |              1 | 426.104     |       207 |                    41.64 |                       54.11 |
| ano_mes=202411 |              1 | 454.572     |       207 |                    43.92 |                       56.98 |
| ano_mes=202412 |              1 | 445.154     |       207 |                    45.5  |                       58.9  |
| ano_mes=202501 |              1 | 452.621     |       207 |                    44.39 |                       57.13 |
| ano_mes=202502 |              1 | 419.453     |       207 |                    41.33 |                       53.31 |
| ano_mes=202503 |              1 | 435.996     |       207 |                    44.35 |                       57.19 |
| TOTAL          |              6 | 2.633.900   |       207 |                   261.15 |                      337.62 |

---

