# Relatório de Profiling: `bronze/score_bureau_movel` - `20251228_155644`

### 📦 Volumetria: `raw/score_bureau_movel`
| diretorio             |   qtd_arquivos | registros   |   colunas |   tamanho_comprimido_mib |   tamanho_descomprimido_mib |
|:----------------------|---------------:|:------------|----------:|-------------------------:|----------------------------:|
| safra_date=2024-10-01 |              1 | 203.828     |        11 |                     2.05 |                        3.45 |
| safra_date=2024-11-01 |              1 | 227.176     |        11 |                     2.28 |                        3.84 |
| safra_date=2024-12-01 |              1 | 227.985     |        11 |                     2.28 |                        3.85 |
| safra_date=2025-01-01 |              1 | 221.002     |        11 |                     2.22 |                        3.74 |
| safra_date=2025-02-01 |              1 | 203.139     |        11 |                     2.04 |                        3.43 |
| safra_date=2025-03-01 |              1 | 207.396     |        11 |                     2.08 |                        3.5  |
| TOTAL                 |              6 | 1.290.526   |        11 |                    12.95 |                       21.82 |

---

### 🧬 Schema: `raw/score_bureau_movel`
| column_name      | column_type              | null   | key   | default   | extra   |
|:-----------------|:-------------------------|:-------|:------|:----------|:--------|
| has_instalacao   | BOOLEAN                  | YES    |       |           |         |
| is_fpd           | BOOLEAN                  | YES    |       |           |         |
| produto          | VARCHAR                  | YES    |       |           |         |
| tipo_migracao    | VARCHAR                  | YES    |       |           |         |
| score_principal  | INTEGER                  | YES    |       |           |         |
| score_secundario | INTEGER                  | YES    |       |           |         |
| cpf_hash         | VARCHAR                  | YES    |       |           |         |
| ingestion_ts     | TIMESTAMP WITH TIME ZONE | YES    |       |           |         |
| source_file      | VARCHAR                  | YES    |       |           |         |
| run_id           | VARCHAR                  | YES    |       |           |         |
| safra_date       | DATE                     | YES    |       |           |         |

---

### 📅 Campos de Data: `raw/score_bureau_movel`
#### ✅ Datas com tipagem (DATE / TIMESTAMP)
**Coluna:** `ingestion_ts`

| min_data                         | max_data                         |
|:---------------------------------|:---------------------------------|
| 2025-12-28 12:56:44.140759-03:00 | 2025-12-28 12:56:44.140759-03:00 |

**Coluna:** `safra_date`

| min_data                   | max_data                   |
|:---------------------------|:---------------------------|
| 2024-10-01T00:00:00.000000 | 2025-03-01T00:00:00.000000 |



---

### 📊 Estatísticas por Coluna: `raw/score_bureau_movel`
| coluna           |   distintos |   nulos |   duplicados | pct_nulos   | pct_duplicados   | cardinalidade   |
|:-----------------|------------:|--------:|-------------:|:------------|:-----------------|:----------------|
| has_instalacao   |           1 |       0 |      1290525 | 0.0%        | 100.0%           | BAIXA           |
| is_fpd           |           2 |       0 |      1290524 | 0.0%        | 100.0%           | BAIXA           |
| produto          |           1 |       0 |      1290525 | 0.0%        | 100.0%           | BAIXA           |
| tipo_migracao    |           1 |       0 |      1290525 | 0.0%        | 100.0%           | BAIXA           |
| score_principal  |         298 |    9439 |      1290228 | 0.73%       | 99.98%           | BAIXA           |
| score_secundario |         585 |     576 |      1289941 | 0.04%       | 99.95%           | BAIXA           |
| cpf_hash         |     1272095 |       0 |        18431 | 0.0%        | 1.43%            | ALTA            |
| ingestion_ts     |           1 |       0 |      1290525 | 0.0%        | 100.0%           | BAIXA           |
| source_file      |           1 |       0 |      1290525 | 0.0%        | 100.0%           | BAIXA           |
| run_id           |           1 |       0 |      1290525 | 0.0%        | 100.0%           | BAIXA           |
| safra_date       |           6 |       0 |      1290520 | 0.0%        | 100.0%           | BAIXA           |

---

### 🔟 Distribuição de Valores (Top 10): `raw/score_bureau_movel`
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

#### Coluna: `cpf_hash`

| valor       |   qtd |
|:------------|------:|
| ZW9TYZXTWTZ |     5 |
| Z9XN9ZZWU7T |     4 |
| ZYWUTZXXTU8 |     4 |
| T87Z88U7U87 |     4 |
| ZZUWWTYWZ8T |     4 |
| Z8NZWZZ7U97 |     4 |
| Z8Y88ZX77ZW |     4 |
| ZUNUNZZNTZY |     4 |
| XUWNXZXN7ZU |     4 |
| TN8Y7XTNZ87 |     4 |

#### Coluna: `ingestion_ts`

| valor                            |     qtd |
|:---------------------------------|--------:|
| 2025-12-28 12:56:44.140759-03:00 | 1290526 |

#### Coluna: `source_file`

| valor                                                                                                |     qtd |
|:-----------------------------------------------------------------------------------------------------|--------:|
| s3://lake/raw/score_bureau_movel/part-00000-b6bf6bdd-9a2d-4bc5-a97c-fa8553906bc9-c000.snappy.parquet | 1290526 |

#### Coluna: `run_id`

|           valor |     qtd |
|----------------:|--------:|
| 20251228_155644 | 1290526 |

#### Coluna: `safra_date`

| valor               |    qtd |
|:--------------------|-------:|
| 2024-12-01 00:00:00 | 227985 |
| 2024-11-01 00:00:00 | 227176 |
| 2025-01-01 00:00:00 | 221002 |
| 2025-03-01 00:00:00 | 207396 |
| 2024-10-01 00:00:00 | 203828 |
| 2025-02-01 00:00:00 | 203139 |



---

### 📏 Comprimento de Strings: `raw/score_bureau_movel`
#### Coluna: `produto`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|         3 |         3 |         3 |

#### Coluna: `tipo_migracao`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|         3 |         3 |         3 |

#### Coluna: `cpf_hash`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|        11 |        11 |        11 |

#### Coluna: `source_file`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|       100 |       100 |       100 |

#### Coluna: `run_id`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|        15 |        15 |        15 |



---

