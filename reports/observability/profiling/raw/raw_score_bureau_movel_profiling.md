# Relatório de Profiling: `raw/score_bureau_movel`

### 📦 Volumetria: `raw/score_bureau_movel`
|   qtd_arquivos | registros   |   colunas |   tamanho_comprimido_mib |   tamanho_descomprimido_mib |
|---------------:|:------------|----------:|-------------------------:|----------------------------:|
|              1 | 3.795.310   |         8 |                    38.62 |                        65.5 |

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

- `SAFRA`


---

### 📊 Estatísticas por Coluna: `raw/score_bureau_movel`
| coluna          |   distintos |   nulos |   duplicados | pct_nulos   | pct_duplicados   | cardinalidade   |
|:----------------|------------:|--------:|-------------:|:------------|:-----------------|:----------------|
| SAFRA           |           6 |       0 |      3795304 | 0.0%        | 100.0%           | BAIXA           |
| FLAG_INSTALACAO |           2 |       0 |      3795308 | 0.0%        | 100.0%           | BAIXA           |
| FPD             |           2 | 1161410 |      3795308 | 30.6%       | 100.0%           | BAIXA           |
| PROD            |           1 |       0 |      3795309 | 0.0%        | 100.0%           | BAIXA           |
| flag_mig2       |           3 | 1161410 |      3795307 | 30.6%       | 100.0%           | BAIXA           |
| SCORE_01        |         308 |   54035 |      3795002 | 1.42%       | 99.99%           | BAIXA           |
| SCORE_02        |         603 |    1876 |      3794707 | 0.05%       | 99.98%           | BAIXA           |
| NUM_CPF         |     3590459 |       0 |       204851 | 0.0%        | 5.4%             | ALTA            |

---

### 🔟 Distribuição de Valores (Top 10): `raw/score_bureau_movel`
#### Coluna: `SAFRA`

|   valor |    qtd |
|--------:|-------:|
|  202501 | 648554 |
|  202411 | 647199 |
|  202410 | 636951 |
|  202503 | 633518 |
|  202412 | 626744 |
|  202502 | 602344 |

#### Coluna: `FLAG_INSTALACAO`

|   valor |     qtd |
|--------:|--------:|
|       1 | 2633900 |
|       0 | 1161410 |

#### Coluna: `FPD`

|   valor |     qtd |
|--------:|--------:|
|       0 | 2074671 |
|         | 1161410 |
|       1 |  559229 |

#### Coluna: `PROD`

| valor   |     qtd |
|:--------|--------:|
| CMV     | 3795310 |

#### Coluna: `flag_mig2`

| valor     |     qtd |
|:----------|--------:|
| Aquisição | 1338888 |
| PRE       | 1290526 |
|           | 1161410 |
| FLEX      |    4486 |

#### Coluna: `SCORE_01`

|   valor |   qtd |
|--------:|------:|
|     589 | 64373 |
|     601 | 63565 |
|         | 54035 |
|     571 | 53351 |
|     560 | 53313 |
|     582 | 48768 |
|     593 | 48286 |
|     574 | 46425 |
|     531 | 45087 |
|     599 | 43953 |

#### Coluna: `SCORE_02`

|   valor |   qtd |
|--------:|------:|
|       1 | 18855 |
|     574 | 12743 |
|     582 | 12682 |
|     561 | 12680 |
|     577 | 12673 |
|     570 | 12653 |
|     581 | 12627 |
|     576 | 12625 |
|     567 | 12620 |
|     579 | 12613 |

#### Coluna: `NUM_CPF`

| valor       |   qtd |
|:------------|------:|
| Y77ZYUXU8NW |     6 |
| 7X7NZ79YWU9 |     6 |
| ZZZZZZZX7T9 |     6 |
| U8Z9ZZ8N8XZ |     6 |
| 888W78UZYYT |     6 |
| ZNTN78ZW7XX |     5 |
| ZNY9U7TWWUX |     5 |
| ZTZTWZXTYZX |     5 |
| ZUZUZZX7X88 |     5 |
| U79ZXXNY8ZT |     5 |



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
|         3 |      6.05 |         9 |

#### Coluna: `SCORE_01`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|         1 |      2.99 |         3 |

#### Coluna: `SCORE_02`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|         1 |      2.99 |         3 |

#### Coluna: `NUM_CPF`
|   min_len |   avg_len |   max_len |
|----------:|----------:|----------:|
|        11 |        11 |        11 |



---

