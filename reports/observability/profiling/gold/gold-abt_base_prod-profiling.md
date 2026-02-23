# Relatório de Profiling: `gold/abt_base_prod` - `20260221`

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
| flag_instalacao                   | BOOLEAN                  | 0.0%          |
| rec_qtd_geral                     | BIGINT                   | 0.0%          |
| rec_qtd_l30d                      | BIGINT                   | 0.0%          |
| rec_qtd_l90d                      | BIGINT                   | 0.0%          |
| rec_vlr_total_geral               | DOUBLE                   | 2.96%         |
| rec_vlr_total_l30d                | DOUBLE                   | 18.73%        |
| rec_vlr_total_l90d                | DOUBLE                   | 4.59%         |
| rec_tendencia_vlr_l30_l90         | DOUBLE                   | 28.55%        |
| rec_qtd_sos_geral                 | BIGINT                   | 0.0%          |
| rec_qtd_sos_l90d                  | BIGINT                   | 0.0%          |
| rec_vlr_sos_l90d                  | DOUBLE                   | 68.79%        |
| rec_qtd_canais_digitais_geral     | BIGINT                   | 0.0%          |
| rec_dias_desde_ultima             | BIGINT                   | 2.96%         |
| rec_vlr_std_l90d                  | DOUBLE                   | 11.17%        |
| rec_vlr_bonus_geral               | DOUBLE                   | 2.96%         |
| rec_qtd_plano_controle_geral      | BIGINT                   | 0.0%          |
| pag_vlr_total_geral               | DOUBLE                   | 77.74%        |
| pag_vlr_total_l90d                | DOUBLE                   | 80.05%        |
| pag_ticket_medio_geral            | DOUBLE                   | 77.74%        |
| pag_qtd_faturas_geral             | BIGINT                   | 0.0%          |
| pag_media_dias_atraso_geral       | DOUBLE                   | 80.46%        |
| pag_max_dias_atraso_geral         | BIGINT                   | 80.46%        |
| pag_qtd_debito_direto_geral       | BIGINT                   | 0.0%          |
| pag_share_faturas_com_juros_geral | DOUBLE                   | 77.74%        |
| pag_vlr_std_l90d                  | DOUBLE                   | 82.24%        |
| pag_dias_desde_ultimo_pagamento   | BIGINT                   | 77.74%        |
| atr_vlr_acumulado_geral           | DOUBLE                   | 74.56%        |
| atr_vlr_max_geral                 | DOUBLE                   | 74.56%        |
| atr_qtd_faturas_atrasadas_geral   | BIGINT                   | 0.0%          |
| atr_dias_desde_ultimo_atraso      | BIGINT                   | 74.56%        |
| atr_max_aging_divida_geral        | INTEGER                  | 74.56%        |
| atr_qtd_pdd_geral                 | BIGINT                   | 0.0%          |
| atr_qtd_wo_geral                  | BIGINT                   | 0.0%          |
| atr_qtd_fraude_geral              | BIGINT                   | 0.0%          |
| bur_flag_mig2                     | VARCHAR                  | 0.92%         |
| bur_score_01                      | INTEGER                  | 1.64%         |
| bur_score_02                      | INTEGER                  | 0.97%         |
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
| idade                             | BIGINT                   | 0.15%         |
| tempo_conta_dias                  | BIGINT                   | 38.33%        |
| flag_auxilio_emergencial          | INTEGER                  | 0.0%          |
| flag_bolsa_familia                | INTEGER                  | 0.0%          |
| flag_aposentado                   | INTEGER                  | 0.0%          |
| flag_funcionario_privado          | INTEGER                  | 0.0%          |
| cad_flag_statusrf_irregular       | INTEGER                  | 0.0%          |
| run_id                            | BIGINT                   | 0.0%          |
| ingestion_ts                      | TIMESTAMP WITH TIME ZONE | 0.0%          |
| ano_mes                           | BIGINT                   | 0.0%          |

---

### 🚩 Detecção de Anomalias Financeiras (Outliers > 3σ): `abt_base_prod`

| Feature                           | Max Value     | Threshold (3σ)   | Status              |
|:----------------------------------|:--------------|:-----------------|:--------------------|
| rec_qtd_geral                     | 3.387,00      | 131,36           | ⚠️ Outlier Detected |
| rec_qtd_l30d                      | 260,00        | 12,22            | ⚠️ Outlier Detected |
| rec_qtd_l90d                      | 738,00        | 31,98            | ⚠️ Outlier Detected |
| rec_vlr_total_geral               | 425.000,00    | 2.970,43         | ⚠️ Outlier Detected |
| rec_vlr_total_l30d                | 50.000,00     | 236,37           | ⚠️ Outlier Detected |
| rec_vlr_total_l90d                | 75.100,00     | 536,07           | ⚠️ Outlier Detected |
| rec_qtd_sos_geral                 | 321,00        | 16,27            | ⚠️ Outlier Detected |
| rec_qtd_sos_l90d                  | 57,00         | 4,16             | ⚠️ Outlier Detected |
| rec_vlr_sos_l90d                  | 1.040,00      | 66,05            | ⚠️ Outlier Detected |
| rec_qtd_canais_digitais_geral     | 140,00        | 11,77            | ⚠️ Outlier Detected |
| rec_dias_desde_ultima             | 515,00        | 90,65            | ⚠️ Outlier Detected |
| rec_vlr_std_l90d                  | 12.497,50     | 76,55            | ⚠️ Outlier Detected |
| rec_vlr_bonus_geral               | 20.904.231,55 | 1.709.319,15     | ⚠️ Outlier Detected |
| rec_qtd_plano_controle_geral      | 236,00        | 30,92            | ⚠️ Outlier Detected |
| pag_vlr_total_geral               | 869.165,45    | 13.645,57        | ⚠️ Outlier Detected |
| pag_vlr_total_l90d                | 328.986,24    | 3.436,23         | ⚠️ Outlier Detected |
| pag_ticket_medio_geral            | 47.706,70     | 790,98           | ⚠️ Outlier Detected |
| pag_qtd_faturas_geral             | 88,00         | 20,52            | ⚠️ Outlier Detected |
| pag_media_dias_atraso_geral       | 2.717,00      | 136,82           | ⚠️ Outlier Detected |
| pag_max_dias_atraso_geral         | 3.739,00      | 227,80           | ⚠️ Outlier Detected |
| pag_qtd_debito_direto_geral       | 117,00        | 5,89             | ⚠️ Outlier Detected |
| pag_share_faturas_com_juros_geral | 6,43          | 2,01             | ⚠️ Outlier Detected |
| pag_vlr_std_l90d                  | 33.218,60     | 390,14           | ⚠️ Outlier Detected |
| pag_dias_desde_ultimo_pagamento   | 516,00        | 192,92           | ⚠️ Outlier Detected |
| atr_vlr_acumulado_geral           | 55.931.388,30 | 293.518,65       | ⚠️ Outlier Detected |
| atr_vlr_max_geral                 | 509.114,06    | 3.024,04         | ⚠️ Outlier Detected |
| atr_qtd_faturas_atrasadas_geral   | 250,00        | 20,83            | ⚠️ Outlier Detected |
| atr_dias_desde_ultimo_atraso      | 517,00        | 237,83           | ⚠️ Outlier Detected |
| atr_max_aging_divida_geral        | 276,00        | 270,60           | ⚠️ Outlier Detected |
| atr_qtd_pdd_geral                 | 1.636,00      | 16,06            | ⚠️ Outlier Detected |
| atr_qtd_wo_geral                  | 736,00        | 11,60            | ⚠️ Outlier Detected |
| atr_qtd_fraude_geral              | 24,00         | 0,43             | ⚠️ Outlier Detected |

---

### 📦 Volumetria: `abt_base_prod`
| diretorio      |   qtd_arquivos | registros   |   colunas |   tamanho_comprimido_mib |   tamanho_descomprimido_mib |
|:---------------|---------------:|:------------|----------:|-------------------------:|----------------------------:|
| ano_mes=202410 |              1 | 207.953     |       120 |                    21.04 |                       28.48 |
| ano_mes=202411 |              1 | 231.824     |       120 |                    23.52 |                       32.79 |
| ano_mes=202412 |              1 | 232.984     |       120 |                    23.32 |                       31.65 |
| ano_mes=202501 |              1 | 226.446     |       120 |                    23.52 |                       32.39 |
| ano_mes=202502 |              1 | 208.731     |       120 |                    21.36 |                       29.18 |
| ano_mes=202503 |              1 | 213.230     |       120 |                    21.87 |                       29.81 |
| TOTAL          |              6 | 1.321.168   |       120 |                   134.64 |                      184.3  |

---

### 📅 Estabilidade de Safras (Volumetria Mensal)

| safra               |   qtd_registros | representatividade   |
|:--------------------|----------------:|:---------------------|
| 2024-10-01 00:00:00 |          207953 | 15.74%               |
| 2024-11-01 00:00:00 |          231824 | 17.55%               |
| 2024-12-01 00:00:00 |          232984 | 17.63%               |
| 2025-01-01 00:00:00 |          226446 | 17.14%               |
| 2025-02-01 00:00:00 |          208731 | 15.8%                |
| 2025-03-01 00:00:00 |          213230 | 16.14%               |

---

### 📶 Densidade de Sinal (Percentual de nulos médio por Prefixo)
> Mede o percentual médio de preenchimento das variáveis agrupadas por origem.

| prefixo   |   qtd_features | pct_missing_medio   | densidade_sinal   |
|:----------|---------------:|:--------------------|:------------------|
| rec_      |             15 | 9.38%               | 90.62%            |
| pag_      |             10 | 63.42%              | 36.58%            |
| atr_      |              8 | 37.28%              | 62.72%            |
| bur_      |              3 | 1.18%               | 98.82%            |
| tel_      |             69 | 0.08%               | 99.92%            |
| cad_      |              1 | 0.0%                | 100.0%            |
| outros    |             11 | 3.5%                | 96.5%             |

---

### 💳 Perfil de Risco (Taxa de FPD por Produto)

| prod   |   total_cpfs |   qtd_bad | fpd_rate   |
|:-------|-------------:|----------:|:-----------|
| CMV    |      1308974 |    310555 | 23.73%     |
| NET    |        10043 |      2626 | 26.15%     |
| DTH    |         2151 |      1149 | 53.42%     |

---

### 📈 Top 15 Variáveis com Maior Correlação (Pearson) com Target
> Identifica a força da relação linear entre as features e o evento de FPD.

| feature                         |   correlacao |
|:--------------------------------|-------------:|
| bur_score_02                    |   -0.292252  |
| bur_score_01                    |   -0.2177    |
| atr_max_aging_divida_geral      |    0.135113  |
| tel_var_28                      |    0.0998143 |
| pag_qtd_faturas_geral           |   -0.09079   |
| pag_dias_desde_ultimo_pagamento |    0.0897205 |
| tel_var_31                      |    0.0879407 |
| flag_bolsa_familia              |    0.085265  |
| atr_dias_desde_ultimo_atraso    |   -0.0805903 |
| tel_var_30                      |    0.0770578 |
| rec_vlr_bonus_geral             |   -0.0766015 |
| tel_var_50                      |    0.0749363 |
| pag_media_dias_atraso_geral     |    0.0747362 |
| tel_var_48                      |    0.0741826 |
| tel_var_45                      |    0.0735332 |

---

### 📊 Sumário Estatístico dos Scores de Bureau
> Análise de quartis e dispersão para validação da saúde dos scores de entrada.

| feature      |   min |   p25 |   median |     avg |   p75 |   max |     std |
|:-------------|------:|------:|---------:|--------:|------:|------:|--------:|
| bur_score_01 |     0 |   554 |      587 | 586.877 |   621 |   778 | 57.3987 |
| bur_score_02 |     1 |   557 |      622 | 627.528 |   697 |   917 | 96.1777 |

---

