# Relatório de Profiling: `raw/score_bureau_movel`

### 📦 Volume Físico Parquet: `raw/score_bureau_movel`
|   qtd_arquivos |   tamanho_comprimido_mb |   tamanho_comprimido_gb |   tamanho_descomprimido_mb |   tamanho_descomprimido_gb |
|---------------:|------------------------:|------------------------:|---------------------------:|---------------------------:|
|              1 |                    12.9 |                    0.01 |                      21.59 |                       0.02 |

---

### 🔢 Volume Lógico: `raw/score_bureau_movel`
- **Total de linhas:** 1290526
- **Total de colunas:** 8

---

### 🧬 Schema: `raw/score_bureau_movel`
| column_name     | column_type   | null   | key   | default   | extra   |
|:----------------|:--------------|:-------|:------|:----------|:--------|
| SAFRA           | VARCHAR       | YES    |       |           |         |
| FLAG_INSTALACAO | VARCHAR       | YES    |       |           |         |
| FPD             | VARCHAR       | YES    |       |           |         |
| PROD            | VARCHAR       | YES    |       |           |         |
| flag_mig2       | VARCHAR       | YES    |       |           |         |
| SCORE_01        | VARCHAR       | YES    |       |           |         |
| SCORE_02        | VARCHAR       | YES    |       |           |         |
| NUM_CPF         | VARCHAR       | YES    |       |           |         |

---

### 📅 Campos de Data: `raw/score_bureau_movel`
#### ✅ Datas com tipagem (DATE / TIMESTAMP)
> ⚠️ Nenhuma coluna DATE ou TIMESTAMP encontrada.

#### ⚠️ Possíveis campos de data/hora sem tipagem (inferido pelo nome)

> Nenhuma coluna com nome sugestivo de data encontrada.

---

### 📊 Estatísticas por Coluna: `raw/score_bureau_movel`
| coluna          |   distintos |   nulos |   duplicados | pct_nulos   | pct_duplicados   | cardinalidade   |
|:----------------|------------:|--------:|-------------:|:------------|:-----------------|:----------------|
| SAFRA           |           6 |       0 |      1290520 | 0.0%        | 100.0%           | BAIXA           |
| FLAG_INSTALACAO |           1 |       0 |      1290525 | 0.0%        | 100.0%           | BAIXA           |
| FPD             |           2 |       0 |      1290524 | 0.0%        | 100.0%           | BAIXA           |
| PROD            |           1 |       0 |      1290525 | 0.0%        | 100.0%           | BAIXA           |
| flag_mig2       |           1 |       0 |      1290525 | 0.0%        | 100.0%           | BAIXA           |
| SCORE_01        |         298 |    9439 |      1290228 | 0.73%       | 99.98%           | BAIXA           |
| SCORE_02        |         585 |     576 |      1289941 | 0.04%       | 99.95%           | BAIXA           |
| NUM_CPF         |     1272095 |       0 |        18431 | 0.0%        | 1.43%            | ALTA            |

---

### 🔟 Distribuição de Valores (Top 10): `raw/score_bureau_movel`
#### Coluna: `SAFRA`

|   valor |    qtd |
|--------:|-------:|
|  202412 | 227985 |
|  202411 | 227176 |
|  202501 | 221002 |
|  202503 | 207396 |
|  202410 | 203828 |
|  202502 | 203139 |

#### Coluna: `FLAG_INSTALACAO`

|   valor |     qtd |
|--------:|--------:|
|       1 | 1290526 |

#### Coluna: `FPD`

|   valor |    qtd |
|--------:|-------:|
|       0 | 986330 |
|       1 | 304196 |

#### Coluna: `PROD`

| valor   |     qtd |
|:--------|--------:|
| CMV     | 1290526 |

#### Coluna: `flag_mig2`

| valor   |     qtd |
|:--------|--------:|
| PRE     | 1290526 |

#### Coluna: `SCORE_01`

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

#### Coluna: `SCORE_02`

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

#### Coluna: `NUM_CPF`

| valor       |   qtd |
|:------------|------:|
| ZW9TYZXTWTZ |     5 |
| 78X9UYXZTWU |     4 |
| TN8Y7XTNZ87 |     4 |
| ZZUWWTYWZ8T |     4 |
| ZW7UTZZYYW7 |     4 |
| XUWNXZXN7ZU |     4 |
| ZUNUNZZNTZY |     4 |
| 8Z7UTZ9XZ9X |     4 |
| Z8Y88ZX77ZW |     4 |
| ZTU8UZXYWWW |     4 |



---

### 📏 Comprimento de Strings: `raw/score_bureau_movel`
#### Coluna: `SAFRA`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|         6 |         6 |         6 |

#### Coluna: `FLAG_INSTALACAO`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|         1 |         1 |         1 |

#### Coluna: `FPD`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|         1 |         1 |         1 |

#### Coluna: `PROD`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|         3 |         3 |         3 |

#### Coluna: `flag_mig2`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|         3 |         3 |         3 |

#### Coluna: `SCORE_01`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|         1 |         3 |         3 |

#### Coluna: `SCORE_02`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|         1 |         3 |         3 |

#### Coluna: `NUM_CPF`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|        11 |        11 |        11 |



---

