# Relatório de Profiling: `bronze/score_bureau_movel` - `20260108_074222`

### 📦 Volumetria: `bronze/score_bureau_movel`
| diretorio      |   qtd_arquivos | registros   |   colunas |   tamanho_comprimido_mib |   tamanho_descomprimido_mib |
|:---------------|---------------:|:------------|----------:|-------------------------:|----------------------------:|
| ano_mes=202410 |              1 | 203.828     |        10 |                     2.05 |                        3.45 |
| ano_mes=202411 |              1 | 227.176     |        10 |                     2.28 |                        3.84 |
| ano_mes=202412 |              1 | 227.985     |        10 |                     2.28 |                        3.85 |
| ano_mes=202501 |              1 | 221.002     |        10 |                     2.22 |                        3.74 |
| ano_mes=202502 |              1 | 203.139     |        10 |                     2.04 |                        3.43 |
| ano_mes=202503 |              1 | 207.396     |        10 |                     2.08 |                        3.5  |
| TOTAL          |              6 | 1.290.526   |        10 |                    12.94 |                       21.81 |

---

### 🧬 Schema: `bronze/score_bureau_movel`
| column_name      | column_type   | null   | key   | default   | extra   |
|:-----------------|:--------------|:-------|:------|:----------|:--------|
| safra            | DATE          | YES    |       |           |         |
| cpf_hash         | VARCHAR       | YES    |       |           |         |
| has_instalacao   | BOOLEAN       | YES    |       |           |         |
| is_fpd           | BOOLEAN       | YES    |       |           |         |
| produto          | VARCHAR       | YES    |       |           |         |
| tipo_migracao    | VARCHAR       | YES    |       |           |         |
| score_principal  | INTEGER       | YES    |       |           |         |
| score_secundario | INTEGER       | YES    |       |           |         |
| ano_mes          | BIGINT        | YES    |       |           |         |
| run_id           | VARCHAR       | YES    |       |           |         |

---

### 📅 Range de Datas: `bronze/score_bureau_movel`
#### Coluna: `safra`
| min                        | max                        |
|:---------------------------|:---------------------------|
| 2024-10-01T00:00:00.000000 | 2025-03-01T00:00:00.000000 |



---

### 📊 Estatísticas por Coluna: `bronze/score_bureau_movel`
| coluna           |   distintos |   nulos |   duplicados | pct_nulos   | pct_duplicados   | cardinalidade   |
|:-----------------|------------:|--------:|-------------:|:------------|:-----------------|:----------------|
| safra            |           6 |       0 |      1290520 | 0.0%        | 100.0%           | BAIXA           |
| cpf_hash         |     1272095 |       0 |        18431 | 0.0%        | 1.43%            | ALTA            |
| has_instalacao   |           1 |       0 |      1290525 | 0.0%        | 100.0%           | BAIXA           |
| is_fpd           |           2 |       0 |      1290524 | 0.0%        | 100.0%           | BAIXA           |
| produto          |           1 |       0 |      1290525 | 0.0%        | 100.0%           | BAIXA           |
| tipo_migracao    |           1 |       0 |      1290525 | 0.0%        | 100.0%           | BAIXA           |
| score_principal  |         298 |    9439 |      1290228 | 0.73%       | 99.98%           | BAIXA           |
| score_secundario |         585 |     576 |      1289941 | 0.04%       | 99.95%           | BAIXA           |
| ano_mes          |           6 |       0 |      1290520 | 0.0%        | 100.0%           | BAIXA           |
| run_id           |           1 |       0 |      1290525 | 0.0%        | 100.0%           | BAIXA           |

---

### 🔟 Distribuição de Valores (Top 10): `bronze/score_bureau_movel`
#### Coluna: `safra`

| valor               |    qtd |
|:--------------------|-------:|
| 2024-12-01 00:00:00 | 227985 |
| 2024-11-01 00:00:00 | 227176 |
| 2025-01-01 00:00:00 | 221002 |
| 2025-03-01 00:00:00 | 207396 |
| 2024-10-01 00:00:00 | 203828 |
| 2025-02-01 00:00:00 | 203139 |

#### Coluna: `cpf_hash`

| valor       |   qtd |
|:------------|------:|
| ZW9TYZXTWTZ |     5 |
| ZZUWWTYWZ8T |     4 |
| Z9XN9ZZWU7T |     4 |
| Z8NZWZZ7U97 |     4 |
| T87Z88U7U87 |     4 |
| ZTU8UZXYWWW |     4 |
| XWYWZZZNNNN |     4 |
| 8Z7UTZ9XZ9X |     4 |
| XUWNXZXN7ZU |     4 |
| 78X9UYXZTWU |     4 |

#### Coluna: `has_instalacao`

| valor   |     qtd |
|:--------|--------:|
| True    | 1290526 |

#### Coluna: `is_fpd`

| valor   |    qtd |
|:--------|-------:|
| False   | 986330 |
| True    | 304196 |

#### Coluna: `produto`

| valor   |     qtd |
|:--------|--------:|
| CMV     | 1290526 |

#### Coluna: `tipo_migracao`

| valor   |     qtd |
|:--------|--------:|
| PRE     | 1290526 |

#### Coluna: `score_principal`

|   valor |   qtd |
|--------:|------:|
|     601 | 18537 |
|     589 | 18512 |
|     560 | 16329 |
|     571 | 16315 |
|     582 | 15515 |
|     593 | 15307 |
|     574 | 14650 |
|     585 | 14167 |
|     599 | 13404 |
|     553 | 12672 |

#### Coluna: `score_secundario`

|   valor |   qtd |
|--------:|------:|
|     593 |  5178 |
|     582 |  5177 |
|     598 |  5166 |
|     594 |  5149 |
|     591 |  5143 |
|     578 |  5137 |
|     595 |  5132 |
|     574 |  5121 |
|     596 |  5119 |
|     605 |  5114 |

#### Coluna: `ano_mes`

|   valor |    qtd |
|--------:|-------:|
|  202412 | 227985 |
|  202411 | 227176 |
|  202501 | 221002 |
|  202503 | 207396 |
|  202410 | 203828 |
|  202502 | 203139 |

#### Coluna: `run_id`

|           valor |     qtd |
|----------------:|--------:|
| 20260108_074222 | 1290526 |



---

