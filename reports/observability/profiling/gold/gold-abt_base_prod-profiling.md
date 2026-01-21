# Relatório de Profiling: `gold/abt_base_prod` - `20260120_213851`

## ⚙️ Sumário Técnico do Dataset

- **Volume de Registros (N):** 1.321.168
- **Cardinalidade (CPF):** 1.272.095
- **Grão Definido:** `num_cpf, safra, prod`

### 🔑 Verificação de Chave Técnica
|   pk_distintos |   duplicatas_reais | pct_duplicidade   |
|---------------:|-------------------:|:------------------|
|        1321168 |                  0 | 0.0%              |

## 🔍 Perfil de Missings por Feature (Ordem da Tabela)

| column_name               | column_type              | pct_missing   |
|:--------------------------|:-------------------------|:--------------|
| num_cpf                   | VARCHAR                  | 0.0%          |
| safra                     | DATE                     | 0.0%          |
| prod                      | VARCHAR                  | 0.0%          |
| fpd                       | BOOLEAN                  | 0.0%          |
| rec_qtd_total             | BIGINT                   | 0.0%          |
| rec_vlr_total             | DOUBLE                   | 2.96%         |
| rec_vlr_avg               | DOUBLE                   | 2.96%         |
| rec_vlr_min               | DOUBLE                   | 2.96%         |
| rec_vlr_max               | DOUBLE                   | 2.96%         |
| rec_dat_primeira          | DATE                     | 2.96%         |
| rec_dat_ultima            | DATE                     | 2.96%         |
| rec_qtd_canais_distintos  | BIGINT                   | 0.0%          |
| pag_vlr_total             | DOUBLE                   | 77.74%        |
| pag_vlr_avg               | DOUBLE                   | 77.74%        |
| pag_vlr_min               | DOUBLE                   | 77.74%        |
| pag_vlr_max               | DOUBLE                   | 77.74%        |
| pag_qtd_faturas           | BIGINT                   | 0.0%          |
| pag_qtd_vezes_com_juros   | BIGINT                   | 0.0%          |
| atr_vlr_max_hist          | DOUBLE                   | 74.56%        |
| atr_vlr_acumulado_hist    | DOUBLE                   | 74.56%        |
| atr_qtd_faturas_atrasadas | BIGINT                   | 0.0%          |
| atr_dat_ultima_ref        | DATE                     | 74.56%        |
| cad_cep_3_digitos         | VARCHAR                  | 5.9%          |
| cad_datadenascimento      | DATE                     | 0.15%         |
| cad_flag_mig2             | VARCHAR                  | 0.92%         |
| cad_statusrf              | VARCHAR                  | 0.11%         |
| cad_var_02                | INTEGER                  | 94.42%        |
| cad_var_03                | INTEGER                  | 6.58%         |
| cad_var_04                | INTEGER                  | 0.11%         |
| cad_var_05                | INTEGER                  | 4.24%         |
| cad_var_06                | INTEGER                  | 80.83%        |
| cad_var_07                | DOUBLE                   | 83.3%         |
| cad_var_08                | INTEGER                  | 80.83%        |
| cad_var_09                | INTEGER                  | 53.38%        |
| cad_var_10                | VARCHAR                  | 98.89%        |
| cad_var_11                | DOUBLE                   | 98.95%        |
| cad_var_12                | DATE                     | 38.33%        |
| cad_var_13                | DATE                     | 84.62%        |
| cad_var_14                | INTEGER                  | 92.27%        |
| cad_var_15                | VARCHAR                  | 82.39%        |
| cad_var_16                | INTEGER                  | 82.39%        |
| cad_var_17                | INTEGER                  | 82.39%        |
| cad_var_18                | VARCHAR                  | 80.83%        |
| cad_var_19                | VARCHAR                  | 53.38%        |
| cad_var_20                | VARCHAR                  | 98.71%        |
| cad_var_21                | VARCHAR                  | 38.33%        |
| cad_var_22                | VARCHAR                  | 92.27%        |
| cad_var_23                | VARCHAR                  | 82.39%        |
| cad_var_24                | VARCHAR                  | 38.33%        |
| cad_var_25                | VARCHAR                  | 10.33%        |
| tel_flag_mig2             | VARCHAR                  | 0.92%         |
| tel_var_26                | VARCHAR                  | 0.09%         |
| tel_var_27                | VARCHAR                  | 0.09%         |
| tel_var_28                | DOUBLE                   | 0.09%         |
| tel_var_29                | DOUBLE                   | 0.09%         |
| tel_var_30                | DOUBLE                   | 0.09%         |
| tel_var_31                | DOUBLE                   | 0.09%         |
| tel_var_32                | DOUBLE                   | 0.09%         |
| tel_var_33                | DOUBLE                   | 0.09%         |
| tel_var_34                | DOUBLE                   | 0.09%         |
| tel_var_35                | DOUBLE                   | 0.09%         |
| tel_var_36                | DOUBLE                   | 0.09%         |
| tel_var_37                | DOUBLE                   | 0.09%         |
| tel_var_38                | DOUBLE                   | 0.09%         |
| tel_var_39                | DOUBLE                   | 0.09%         |
| tel_var_40                | DOUBLE                   | 0.09%         |
| tel_var_41                | DOUBLE                   | 0.09%         |
| tel_var_42                | DOUBLE                   | 0.09%         |
| tel_var_43                | DOUBLE                   | 0.09%         |
| tel_var_44                | DOUBLE                   | 0.09%         |
| tel_var_45                | DOUBLE                   | 0.09%         |
| tel_var_46                | DOUBLE                   | 0.09%         |
| tel_var_47                | DOUBLE                   | 0.09%         |
| tel_var_48                | DOUBLE                   | 0.09%         |
| tel_var_49                | DOUBLE                   | 0.09%         |
| tel_var_50                | DOUBLE                   | 0.09%         |
| tel_var_51                | DOUBLE                   | 0.09%         |
| tel_var_52                | DOUBLE                   | 0.09%         |
| tel_var_53                | DOUBLE                   | 0.09%         |
| tel_var_54                | DOUBLE                   | 0.09%         |
| tel_var_55                | DOUBLE                   | 0.09%         |
| tel_var_56                | DOUBLE                   | 0.09%         |
| tel_var_57                | DOUBLE                   | 0.09%         |
| tel_var_58                | DOUBLE                   | 0.09%         |
| tel_var_59                | DOUBLE                   | 0.09%         |
| tel_var_60                | DOUBLE                   | 0.09%         |
| tel_var_61                | DOUBLE                   | 0.09%         |
| tel_var_62                | DOUBLE                   | 0.09%         |
| tel_var_63                | DOUBLE                   | 0.09%         |
| tel_var_64                | VARCHAR                  | 0.09%         |
| tel_var_65                | VARCHAR                  | 0.09%         |
| tel_var_66                | VARCHAR                  | 0.09%         |
| tel_var_67                | VARCHAR                  | 0.09%         |
| tel_var_68                | DOUBLE                   | 0.09%         |
| tel_var_69                | DOUBLE                   | 0.09%         |
| tel_var_70                | DOUBLE                   | 0.09%         |
| tel_var_71                | DOUBLE                   | 0.09%         |
| tel_var_72                | DOUBLE                   | 0.09%         |
| tel_var_73                | VARCHAR                  | 0.09%         |
| tel_var_74                | VARCHAR                  | 0.09%         |
| tel_var_75                | VARCHAR                  | 0.09%         |
| tel_var_76                | VARCHAR                  | 0.09%         |
| tel_var_77                | VARCHAR                  | 0.09%         |
| tel_var_78                | VARCHAR                  | 0.0%          |
| tel_var_79                | VARCHAR                  | 0.0%          |
| tel_var_80                | VARCHAR                  | 0.0%          |
| tel_var_81                | VARCHAR                  | 0.0%          |
| tel_var_82                | DOUBLE                   | 0.0%          |
| tel_var_83                | VARCHAR                  | 0.0%          |
| tel_var_84                | VARCHAR                  | 0.0%          |
| tel_var_85                | VARCHAR                  | 0.0%          |
| tel_var_86                | VARCHAR                  | 0.0%          |
| tel_var_87                | VARCHAR                  | 0.0%          |
| tel_var_88                | VARCHAR                  | 0.0%          |
| tel_var_89                | VARCHAR                  | 0.0%          |
| tel_var_90                | DOUBLE                   | 0.0%          |
| tel_var_91                | VARCHAR                  | 0.0%          |
| tel_var_92                | VARCHAR                  | 0.0%          |
| tel_var_93                | VARCHAR                  | 0.0%          |
| bur_flag_mig2             | VARCHAR                  | 0.92%         |
| bur_score_01              | INTEGER                  | 1.64%         |
| bur_score_02              | INTEGER                  | 0.97%         |
| run_id                    | VARCHAR                  | 0.0%          |
| ingestion_ts              | TIMESTAMP WITH TIME ZONE | 0.0%          |
| ano_mes                   | BIGINT                   | 0.0%          |

## 🚩 Detecção de Anomalias (Outliers)

| Feature                   | Max Value          | Threshold (3σ)   | Status              |
|:--------------------------|:-------------------|:-----------------|:--------------------|
| rec_qtd_total             | 3.384,00           | 131,28           | ⚠️ Outlier Detected |
| rec_vlr_total             | 425.000,00         | 2.970,35         | ⚠️ Outlier Detected |
| rec_vlr_avg               | 11.000,80          | 67,96            | ⚠️ Outlier Detected |
| rec_vlr_min               | 100,00             | 12,01            | ⚠️ Outlier Detected |
| rec_vlr_max               | 25.000,00          | 269,92           | ⚠️ Outlier Detected |
| rec_qtd_canais_distintos  | 38,00              | 11,47            | ⚠️ Outlier Detected |
| pag_vlr_total             | 796.965,27         | 12.338,38        | ⚠️ Outlier Detected |
| pag_vlr_avg               | 42.651,46          | 620,73           | ⚠️ Outlier Detected |
| pag_vlr_min               | 15.599,98          | 196,46           | ⚠️ Outlier Detected |
| pag_vlr_max               | 72.709,30          | 1.295,57         | ⚠️ Outlier Detected |
| pag_qtd_faturas           | 88,00              | 20,51            | ⚠️ Outlier Detected |
| pag_qtd_vezes_com_juros   | 260,00             | 15,85            | ⚠️ Outlier Detected |
| atr_vlr_max_hist          | 509.114,06         | 3.024,04         | ⚠️ Outlier Detected |
| atr_vlr_acumulado_hist    | 55.931.388,30      | 293.518,65       | ⚠️ Outlier Detected |
| atr_qtd_faturas_atrasadas | 250,00             | 20,83            | ⚠️ Outlier Detected |
| cad_var_04                | 5,00               | 1,78             | ⚠️ Outlier Detected |
| cad_var_05                | 10,00              | 4,95             | ⚠️ Outlier Detected |
| cad_var_07                | 32.689.701,00      | 1.059.310,36     | ⚠️ Outlier Detected |
| cad_var_09                | 17,00              | 13,39            | ⚠️ Outlier Detected |
| cad_var_11                | 36.742,89          | 14.896,86        | ⚠️ Outlier Detected |
| cad_var_14                | 77,00              | 2,83             | ⚠️ Outlier Detected |
| cad_var_16                | 2.688,00           | 1.317,45         | ⚠️ Outlier Detected |
| tel_var_90                | 100.560.366.785,53 | 295.054.293,88   | ⚠️ Outlier Detected |
| bur_score_01              | 778,00             | 759,07           | ⚠️ Outlier Detected |
| bur_score_02              | 917,00             | 916,06           | ⚠️ Outlier Detected |

## 📦 Volumetria de Armazenamento e Particionamento

| partition_dir   |   row_count |   compressed_mib |
|:----------------|------------:|-----------------:|
| ano_mes=202410  |     207.953 |            20.26 |
| ano_mes=202411  |     231.824 |            22.92 |
| ano_mes=202412  |     232.984 |            22.43 |
| ano_mes=202501  |     226.446 |            22.74 |
| ano_mes=202502  |     208.731 |            20.71 |
| ano_mes=202503  |     213.23  |            21.22 |

---

