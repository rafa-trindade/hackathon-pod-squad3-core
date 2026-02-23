# Relatório de Profiling: `gold/abt_base_cmv` - `20260223`

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
| rec_qtd_geral                     | BIGINT                   | 0.0%          |
| rec_qtd_l30d                      | BIGINT                   | 0.0%          |
| rec_qtd_l90d                      | BIGINT                   | 0.0%          |
| rec_vlr_total_geral               | DOUBLE                   | 28.17%        |
| rec_vlr_total_l30d                | DOUBLE                   | 41.68%        |
| rec_vlr_total_l90d                | DOUBLE                   | 31.11%        |
| rec_tendencia_vlr_l30_l90         | DOUBLE                   | 57.65%        |
| rec_qtd_sos_geral                 | BIGINT                   | 0.0%          |
| rec_qtd_sos_l90d                  | BIGINT                   | 0.0%          |
| rec_vlr_sos_l90d                  | DOUBLE                   | 82.68%        |
| rec_qtd_canais_digitais_geral     | BIGINT                   | 0.0%          |
| rec_dias_desde_ultima             | BIGINT                   | 28.17%        |
| rec_vlr_std_l90d                  | DOUBLE                   | 35.94%        |
| rec_vlr_bonus_geral               | DOUBLE                   | 28.17%        |
| rec_qtd_plano_controle_geral      | BIGINT                   | 0.0%          |
| pag_vlr_total_geral               | DOUBLE                   | 70.16%        |
| pag_vlr_total_l90d                | DOUBLE                   | 72.26%        |
| pag_ticket_medio_geral            | DOUBLE                   | 70.16%        |
| pag_qtd_faturas_geral             | BIGINT                   | 0.0%          |
| pag_media_dias_atraso_geral       | DOUBLE                   | 73.7%         |
| pag_max_dias_atraso_geral         | BIGINT                   | 73.7%         |
| pag_qtd_debito_direto_geral       | BIGINT                   | 0.0%          |
| pag_share_faturas_com_juros_geral | DOUBLE                   | 70.16%        |
| pag_vlr_std_l90d                  | DOUBLE                   | 74.11%        |
| pag_dias_desde_ultimo_pagamento   | BIGINT                   | 70.16%        |
| atr_vlr_acumulado_geral           | DOUBLE                   | 68.15%        |
| atr_vlr_max_geral                 | DOUBLE                   | 68.15%        |
| atr_qtd_faturas_atrasadas_geral   | BIGINT                   | 0.0%          |
| atr_dias_desde_ultimo_atraso      | BIGINT                   | 68.15%        |
| atr_max_aging_divida_geral        | INTEGER                  | 68.15%        |
| atr_qtd_pdd_geral                 | BIGINT                   | 0.0%          |
| atr_qtd_wo_geral                  | BIGINT                   | 0.0%          |
| atr_qtd_fraude_geral              | BIGINT                   | 0.0%          |
| bur_flag_mig2                     | VARCHAR                  | 0.0%          |
| bur_score_01                      | INTEGER                  | 0.67%         |
| bur_score_02                      | INTEGER                  | 0.07%         |
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
| idade                             | BIGINT                   | 0.23%         |
| tempo_conta_dias                  | BIGINT                   | 35.4%         |
| flag_auxilio_emergencial          | INTEGER                  | 0.0%          |
| flag_bolsa_familia                | INTEGER                  | 0.0%          |
| flag_aposentado                   | INTEGER                  | 0.0%          |
| flag_funcionario_privado          | INTEGER                  | 0.0%          |
| cad_flag_statusrf_irregular       | INTEGER                  | 0.0%          |
| run_id                            | BIGINT                   | 0.0%          |
| ingestion_ts                      | TIMESTAMP WITH TIME ZONE | 0.0%          |
| ano_mes                           | BIGINT                   | 0.0%          |

---

### 🚩 Detecção de Anomalias Financeiras (Outliers > 3σ): `abt_base_cmv`

| Feature                           | Max Value     | Threshold (3σ)   | Status              |
|:----------------------------------|:--------------|:-----------------|:--------------------|
| rec_qtd_geral                     | 3.387,00      | 106,89           | ⚠️ Outlier Detected |
| rec_qtd_l30d                      | 260,00        | 9,83             | ⚠️ Outlier Detected |
| rec_qtd_l90d                      | 738,00        | 26,00            | ⚠️ Outlier Detected |
| rec_vlr_total_geral               | 425.000,00    | 3.079,36         | ⚠️ Outlier Detected |
| rec_vlr_total_l30d                | 50.000,00     | 242,92           | ⚠️ Outlier Detected |
| rec_vlr_total_l90d                | 75.164,70     | 588,25           | ⚠️ Outlier Detected |
| rec_qtd_sos_geral                 | 321,00        | 12,38            | ⚠️ Outlier Detected |
| rec_qtd_sos_l90d                  | 57,00         | 3,13             | ⚠️ Outlier Detected |
| rec_vlr_sos_l90d                  | 1.040,00      | 66,51            | ⚠️ Outlier Detected |
| rec_qtd_canais_digitais_geral     | 167,00        | 8,94             | ⚠️ Outlier Detected |
| rec_dias_desde_ultima             | 517,00        | 139,36           | ⚠️ Outlier Detected |
| rec_vlr_std_l90d                  | 13.693,06     | 87,93            | ⚠️ Outlier Detected |
| rec_vlr_bonus_geral               | 20.904.231,55 | 1.535.574,35     | ⚠️ Outlier Detected |
| rec_qtd_plano_controle_geral      | 333,00        | 34,52            | ⚠️ Outlier Detected |
| pag_vlr_total_geral               | 2.537.770,97  | 23.318,89        | ⚠️ Outlier Detected |
| pag_vlr_total_l90d                | 979.673,73    | 7.149,32         | ⚠️ Outlier Detected |
| pag_ticket_medio_geral            | 181.269,35    | 1.408,01         | ⚠️ Outlier Detected |
| pag_qtd_faturas_geral             | 110,00        | 24,66            | ⚠️ Outlier Detected |
| pag_media_dias_atraso_geral       | 4.853,00      | 125,39           | ⚠️ Outlier Detected |
| pag_max_dias_atraso_geral         | 4.853,00      | 213,81           | ⚠️ Outlier Detected |
| pag_qtd_debito_direto_geral       | 195,00        | 9,10             | ⚠️ Outlier Detected |
| pag_share_faturas_com_juros_geral | 7,80          | 2,16             | ⚠️ Outlier Detected |
| pag_vlr_std_l90d                  | 208.314,08    | 950,68           | ⚠️ Outlier Detected |
| pag_dias_desde_ultimo_pagamento   | 516,00        | 166,07           | ⚠️ Outlier Detected |
| atr_vlr_acumulado_geral           | 55.931.388,30 | 206.947,05       | ⚠️ Outlier Detected |
| atr_vlr_max_geral                 | 3.406.523,69  | 11.804,53        | ⚠️ Outlier Detected |
| atr_qtd_faturas_atrasadas_geral   | 319,00        | 25,17            | ⚠️ Outlier Detected |
| atr_dias_desde_ultimo_atraso      | 517,00        | 263,62           | ⚠️ Outlier Detected |
| atr_max_aging_divida_geral        | 276,00        | 269,88           | ⚠️ Outlier Detected |
| atr_qtd_pdd_geral                 | 2.316,00      | 18,03            | ⚠️ Outlier Detected |
| atr_qtd_wo_geral                  | 1.271,00      | 12,51            | ⚠️ Outlier Detected |
| atr_qtd_fraude_geral              | 28,00         | 0,46             | ⚠️ Outlier Detected |

---

### 📦 Volumetria: `abt_base_cmv`
| diretorio      |   qtd_arquivos | registros   |   colunas |   tamanho_comprimido_mib |   tamanho_descomprimido_mib |
|:---------------|---------------:|:------------|----------:|-------------------------:|----------------------------:|
| ano_mes=202410 |              1 | 426.104     |       148 |                    35.4  |                       47.62 |
| ano_mes=202411 |              1 | 454.572     |       148 |                    38.4  |                       51.81 |
| ano_mes=202412 |              1 | 445.154     |       148 |                    37.84 |                       50.91 |
| ano_mes=202501 |              1 | 452.621     |       148 |                    38.39 |                       51.61 |
| ano_mes=202502 |              1 | 419.453     |       148 |                    35.81 |                       48.32 |
| ano_mes=202503 |              1 | 435.996     |       148 |                    37.56 |                       50.72 |
| TOTAL          |              6 | 2.633.900   |       148 |                   223.4  |                      300.99 |

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
| rec_      |             15 | 22.24%              | 77.76%            |
| pag_      |             10 | 57.44%              | 42.56%            |
| atr_      |              8 | 34.08%              | 65.92%            |
| bur_      |              3 | 0.25%               | 99.75%            |
| tel_      |             69 | 50.34%              | 49.66%            |
| cad_      |             29 | 54.16%              | 45.84%            |
| outros    |             11 | 3.24%               | 96.76%            |

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
| atr_max_aging_divida_geral      |    0.145128  |
| pag_qtd_faturas_geral           |   -0.104181  |
| cad_var_05                      |   -0.103676  |
| tel_var_28                      |    0.0992972 |
| pag_dias_desde_ultimo_pagamento |    0.0992828 |
| flag_bolsa_familia              |    0.099142  |
| tel_var_31                      |    0.087449  |
| cad_var_02                      |    0.0859616 |
| flag_auxilio_emergencial        |    0.0822269 |
| rec_qtd_sos_geral               |    0.081496  |
| pag_max_dias_atraso_geral       |    0.0790687 |
| pag_media_dias_atraso_geral     |    0.0789047 |
| tel_var_30                      |    0.0766779 |

---

### 📊 Sumário Estatístico dos Scores de Bureau
> Análise de quartis e dispersão para validação da saúde dos scores de entrada.

| feature      |   min |   p25 |   median |     avg |   p75 |   max |      std |
|:-------------|------:|------:|---------:|--------:|------:|------:|---------:|
| bur_score_01 |     0 |   558 |      593 | 590.948 |   626 |   778 |  56.3142 |
| bur_score_02 |     1 |   575 |      653 | 651.013 |   730 |   926 | 101.717  |

---

