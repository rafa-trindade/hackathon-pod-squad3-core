# Relatório de Profiling: `bronze/telco` - `20260108_142134`

### 📦 Volumetria: `bronze/telco`
| diretorio      |   qtd_arquivos | registros   |   colunas |   tamanho_comprimido_mib |   tamanho_descomprimido_mib |
|:---------------|---------------:|:------------|----------:|-------------------------:|----------------------------:|
| ano_mes=202410 |              1 | 219.860     |        77 |                    14.39 |                       20.16 |
| ano_mes=202411 |              1 | 240.520     |        77 |                    16.01 |                       23.29 |
| ano_mes=202412 |              1 | 241.453     |        77 |                    16.14 |                       23.44 |
| ano_mes=202501 |              1 | 233.710     |        77 |                    15.78 |                       22.63 |
| ano_mes=202502 |              1 | 214.665     |        77 |                    14.05 |                       19.75 |
| ano_mes=202503 |              1 | 216.896     |        77 |                    14.49 |                       20.98 |
| TOTAL          |              6 | 1.367.104   |        77 |                    90.85 |                      130.26 |

---

### 🧬 Schema: `bronze/telco`
| column_name     | column_type              | null   | key   | default   | extra   |
|:----------------|:-------------------------|:-------|:------|:----------|:--------|
| safra           | DATE                     | YES    |       |           |         |
| num_cpf         | VARCHAR                  | YES    |       |           |         |
| flag_instalacao | BOOLEAN                  | YES    |       |           |         |
| fpd             | BOOLEAN                  | YES    |       |           |         |
| prod            | VARCHAR                  | YES    |       |           |         |
| flag_mig2       | VARCHAR                  | YES    |       |           |         |
| var_26          | VARCHAR                  | YES    |       |           |         |
| var_27          | VARCHAR                  | YES    |       |           |         |
| var_64          | VARCHAR                  | YES    |       |           |         |
| var_65          | VARCHAR                  | YES    |       |           |         |
| var_66          | VARCHAR                  | YES    |       |           |         |
| var_67          | VARCHAR                  | YES    |       |           |         |
| var_73          | VARCHAR                  | YES    |       |           |         |
| var_74          | VARCHAR                  | YES    |       |           |         |
| var_75          | VARCHAR                  | YES    |       |           |         |
| var_76          | VARCHAR                  | YES    |       |           |         |
| var_77          | VARCHAR                  | YES    |       |           |         |
| var_78          | VARCHAR                  | YES    |       |           |         |
| var_79          | VARCHAR                  | YES    |       |           |         |
| var_80          | VARCHAR                  | YES    |       |           |         |
| var_81          | VARCHAR                  | YES    |       |           |         |
| var_83          | VARCHAR                  | YES    |       |           |         |
| var_84          | VARCHAR                  | YES    |       |           |         |
| var_85          | VARCHAR                  | YES    |       |           |         |
| var_86          | VARCHAR                  | YES    |       |           |         |
| var_87          | VARCHAR                  | YES    |       |           |         |
| var_88          | VARCHAR                  | YES    |       |           |         |
| var_89          | VARCHAR                  | YES    |       |           |         |
| var_91          | VARCHAR                  | YES    |       |           |         |
| var_92          | VARCHAR                  | YES    |       |           |         |
| var_93          | VARCHAR                  | YES    |       |           |         |
| var_28          | DOUBLE                   | YES    |       |           |         |
| var_29          | DOUBLE                   | YES    |       |           |         |
| var_30          | DOUBLE                   | YES    |       |           |         |
| var_31          | DOUBLE                   | YES    |       |           |         |
| var_32          | DOUBLE                   | YES    |       |           |         |
| var_33          | DOUBLE                   | YES    |       |           |         |
| var_34          | DOUBLE                   | YES    |       |           |         |
| var_35          | DOUBLE                   | YES    |       |           |         |
| var_36          | DOUBLE                   | YES    |       |           |         |
| var_37          | DOUBLE                   | YES    |       |           |         |
| var_38          | DOUBLE                   | YES    |       |           |         |
| var_39          | DOUBLE                   | YES    |       |           |         |
| var_40          | DOUBLE                   | YES    |       |           |         |
| var_41          | DOUBLE                   | YES    |       |           |         |
| var_42          | DOUBLE                   | YES    |       |           |         |
| var_43          | DOUBLE                   | YES    |       |           |         |
| var_44          | DOUBLE                   | YES    |       |           |         |
| var_45          | DOUBLE                   | YES    |       |           |         |
| var_46          | DOUBLE                   | YES    |       |           |         |
| var_47          | DOUBLE                   | YES    |       |           |         |
| var_48          | DOUBLE                   | YES    |       |           |         |
| var_49          | DOUBLE                   | YES    |       |           |         |
| var_50          | DOUBLE                   | YES    |       |           |         |
| var_51          | DOUBLE                   | YES    |       |           |         |
| var_52          | DOUBLE                   | YES    |       |           |         |
| var_53          | DOUBLE                   | YES    |       |           |         |
| var_54          | DOUBLE                   | YES    |       |           |         |
| var_55          | DOUBLE                   | YES    |       |           |         |
| var_56          | DOUBLE                   | YES    |       |           |         |
| var_57          | DOUBLE                   | YES    |       |           |         |
| var_58          | DOUBLE                   | YES    |       |           |         |
| var_59          | DOUBLE                   | YES    |       |           |         |
| var_60          | DOUBLE                   | YES    |       |           |         |
| var_61          | DOUBLE                   | YES    |       |           |         |
| var_62          | DOUBLE                   | YES    |       |           |         |
| var_63          | DOUBLE                   | YES    |       |           |         |
| var_68          | DOUBLE                   | YES    |       |           |         |
| var_69          | DOUBLE                   | YES    |       |           |         |
| var_70          | DOUBLE                   | YES    |       |           |         |
| var_71          | DOUBLE                   | YES    |       |           |         |
| var_72          | DOUBLE                   | YES    |       |           |         |
| var_82          | DOUBLE                   | YES    |       |           |         |
| var_90          | DOUBLE                   | YES    |       |           |         |
| ingestion_ts    | TIMESTAMP WITH TIME ZONE | YES    |       |           |         |
| ano_mes         | BIGINT                   | YES    |       |           |         |
| run_id          | VARCHAR                  | YES    |       |           |         |

---

### 📅 Range de Datas: `bronze/telco`
#### Coluna: `safra`
| min                        | max                        |
|:---------------------------|:---------------------------|
| 2024-10-01T00:00:00.000000 | 2025-03-01T00:00:00.000000 |

#### Coluna: `ingestion_ts`
| min                              | max                              |
|:---------------------------------|:---------------------------------|
| 2026-01-08 11:21:34.731530-03:00 | 2026-01-08 11:21:34.731530-03:00 |



---

### 📊 Estatísticas por Coluna: `bronze/telco`
| coluna          |   distintos |   nulos |   duplicados | pct_nulos   | pct_duplicados   | cardinalidade   |
|:----------------|------------:|--------:|-------------:|:------------|:-----------------|:----------------|
| safra           |           6 |       0 |      1367098 | 0.0%        | 100.0%           | BAIXA           |
| num_cpf         |     1272095 |       0 |        95009 | 0.0%        | 6.95%            | ALTA            |
| flag_instalacao |           2 |       0 |      1367102 | 0.0%        | 100.0%           | BAIXA           |
| fpd             |           2 |   45936 |      1367102 | 3.36%       | 100.0%           | BAIXA           |
| prod            |           3 |       0 |      1367101 | 0.0%        | 100.0%           | BAIXA           |
| flag_mig2       |           3 |   58130 |      1367101 | 4.25%       | 100.0%           | BAIXA           |
| var_26          |           8 |    1295 |      1367096 | 0.09%       | 100.0%           | BAIXA           |
| var_27          |           8 |    1295 |      1367096 | 0.09%       | 100.0%           | BAIXA           |
| var_64          |          24 |    1295 |      1367080 | 0.09%       | 100.0%           | BAIXA           |
| var_65          |         297 |    1295 |      1366807 | 0.09%       | 99.98%           | BAIXA           |
| var_66          |          53 |    1295 |      1367051 | 0.09%       | 100.0%           | BAIXA           |
| var_67          |          63 |    1295 |      1367041 | 0.09%       | 100.0%           | BAIXA           |
| var_73          |          12 |    1295 |      1367092 | 0.09%       | 100.0%           | BAIXA           |
| var_74          |          14 |    1295 |      1367090 | 0.09%       | 100.0%           | BAIXA           |
| var_75          |          12 |    1295 |      1367092 | 0.09%       | 100.0%           | BAIXA           |
| var_76          |          12 |    1295 |      1367092 | 0.09%       | 100.0%           | BAIXA           |
| var_77          |           9 |    1295 |      1367095 | 0.09%       | 100.0%           | BAIXA           |
| var_78          |          15 |       0 |      1367089 | 0.0%        | 100.0%           | BAIXA           |
| var_79          |          13 |       0 |      1367091 | 0.0%        | 100.0%           | BAIXA           |
| var_80          |          13 |       0 |      1367091 | 0.0%        | 100.0%           | BAIXA           |
| var_81          |         105 |       0 |      1366999 | 0.0%        | 99.99%           | BAIXA           |
| var_83          |          14 |       0 |      1367090 | 0.0%        | 100.0%           | BAIXA           |
| var_84          |          15 |       0 |      1367089 | 0.0%        | 100.0%           | BAIXA           |
| var_85          |          15 |       0 |      1367089 | 0.0%        | 100.0%           | BAIXA           |
| var_86          |          16 |       0 |      1367088 | 0.0%        | 100.0%           | BAIXA           |
| var_87          |          13 |       0 |      1367091 | 0.0%        | 100.0%           | BAIXA           |
| var_88          |          13 |       0 |      1367091 | 0.0%        | 100.0%           | BAIXA           |
| var_89          |         107 |       0 |      1366997 | 0.0%        | 99.99%           | BAIXA           |
| var_91          |          15 |       0 |      1367089 | 0.0%        | 100.0%           | BAIXA           |
| var_92          |          15 |       0 |      1367089 | 0.0%        | 100.0%           | BAIXA           |
| var_93          |          14 |       0 |      1367090 | 0.0%        | 100.0%           | BAIXA           |
| var_28          |         913 |    1295 |      1366191 | 0.09%       | 99.93%           | BAIXA           |
| var_29          |          79 |    1295 |      1367025 | 0.09%       | 99.99%           | BAIXA           |
| var_30          |         109 |    1295 |      1366995 | 0.09%       | 99.99%           | BAIXA           |
| var_31          |        9777 |    1295 |      1357327 | 0.09%       | 99.28%           | MEDIA           |
| var_32          |       10008 |    1295 |      1357096 | 0.09%       | 99.27%           | MEDIA           |
| var_33          |       10008 |    1295 |      1357096 | 0.09%       | 99.27%           | MEDIA           |
| var_34          |       10008 |    1295 |      1357096 | 0.09%       | 99.27%           | MEDIA           |
| var_35          |       10008 |    1295 |      1357096 | 0.09%       | 99.27%           | MEDIA           |
| var_36          |          97 |    1295 |      1367007 | 0.09%       | 99.99%           | BAIXA           |
| var_37          |          54 |    1295 |      1367050 | 0.09%       | 100.0%           | BAIXA           |
| var_38          |       10006 |    1295 |      1357098 | 0.09%       | 99.27%           | MEDIA           |
| var_39          |       10007 |    1295 |      1357097 | 0.09%       | 99.27%           | MEDIA           |
| var_40          |       10008 |    1295 |      1357096 | 0.09%       | 99.27%           | MEDIA           |
| var_41          |       10008 |    1295 |      1357096 | 0.09%       | 99.27%           | MEDIA           |
| var_42          |         103 |    1295 |      1367001 | 0.09%       | 99.99%           | BAIXA           |
| var_43          |         104 |    1295 |      1367000 | 0.09%       | 99.99%           | BAIXA           |
| var_44          |       10008 |    1295 |      1357096 | 0.09%       | 99.27%           | MEDIA           |
| var_45          |          16 |    1295 |      1367088 | 0.09%       | 100.0%           | BAIXA           |
| var_46          |          46 |    1295 |      1367058 | 0.09%       | 100.0%           | BAIXA           |
| var_47          |        1146 |    1295 |      1365958 | 0.09%       | 99.92%           | BAIXA           |
| var_48          |        3606 |    1295 |      1363498 | 0.09%       | 99.74%           | MEDIA           |
| var_49          |        8098 |    1295 |      1359006 | 0.09%       | 99.41%           | MEDIA           |
| var_50          |        6810 |    1295 |      1360294 | 0.09%       | 99.5%            | MEDIA           |
| var_51          |        1210 |    1295 |      1365894 | 0.09%       | 99.91%           | BAIXA           |
| var_52          |        9878 |    1295 |      1357226 | 0.09%       | 99.28%           | MEDIA           |
| var_53          |          28 |    1295 |      1367076 | 0.09%       | 100.0%           | BAIXA           |
| var_54          |       10008 |    1295 |      1357096 | 0.09%       | 99.27%           | MEDIA           |
| var_55          |          45 |    1295 |      1367059 | 0.09%       | 100.0%           | BAIXA           |
| var_56          |          91 |    1295 |      1367013 | 0.09%       | 99.99%           | BAIXA           |
| var_57          |          20 |    1295 |      1367084 | 0.09%       | 100.0%           | BAIXA           |
| var_58          |         580 |    1295 |      1366524 | 0.09%       | 99.96%           | BAIXA           |
| var_59          |       10008 |    1295 |      1357096 | 0.09%       | 99.27%           | MEDIA           |
| var_60          |       10008 |    1295 |      1357096 | 0.09%       | 99.27%           | MEDIA           |
| var_61          |        4973 |    1295 |      1362131 | 0.09%       | 99.64%           | MEDIA           |
| var_62          |         166 |    1295 |      1366938 | 0.09%       | 99.99%           | BAIXA           |
| var_63          |       10008 |    1295 |      1357096 | 0.09%       | 99.27%           | MEDIA           |
| var_68          |        9577 |    1295 |      1357527 | 0.09%       | 99.3%            | MEDIA           |
| var_69          |        3428 |    1295 |      1363676 | 0.09%       | 99.75%           | MEDIA           |
| var_70          |          20 |    1295 |      1367084 | 0.09%       | 100.0%           | BAIXA           |
| var_71          |          20 |    1295 |      1367084 | 0.09%       | 100.0%           | BAIXA           |
| var_72          |          20 |    1295 |      1367084 | 0.09%       | 100.0%           | BAIXA           |
| var_82          |         803 |       0 |      1366301 | 0.0%        | 99.94%           | BAIXA           |
| var_90          |        1515 |       0 |      1365589 | 0.0%        | 99.89%           | MEDIA           |
| ingestion_ts    |           1 |       0 |      1367103 | 0.0%        | 100.0%           | BAIXA           |
| ano_mes         |           6 |       0 |      1367098 | 0.0%        | 100.0%           | BAIXA           |
| run_id          |           1 |       0 |      1367103 | 0.0%        | 100.0%           | BAIXA           |

---

