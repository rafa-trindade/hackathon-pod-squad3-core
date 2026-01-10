# Relatório de Profiling: `silver/score_bureau_movel` - `20260110_052433`

### 🔑 Garantia de Unicidade: `silver/score_bureau_movel`
- **Chave Técnica:** `num_cpf, safra, fpd`
- **Tipo:** `COMPOSTA`

| coluna        |   distintos |   nulos |   duplicados | pct_nulos   | pct_duplicados   | cardinalidade   |
|:--------------|------------:|--------:|-------------:|:------------|:-----------------|:----------------|
| CHAVE_TECNICA |     1290526 |       0 |            0 | 0.0%        | 0.0%             | MÁXIMA          |

### 🚩 Diagnóstico e Observações Técnicas
* ✅ **Sucesso:** Unicidade Garantida. O grão da tabela está preservado.


---

### 📊 Schema e Estatísticas: `silver/score_bureau_movel`
| column_name     | column_type              |   distintos |   nulos |   duplicados | pct_nulos   | pct_duplicados   | cardinalidade   |
|:----------------|:-------------------------|------------:|--------:|-------------:|:------------|:-----------------|:----------------|
| num_cpf         | VARCHAR                  |     1187719 |       0 |       102807 | 0.0%        | 7.97%            | ALTA            |
| safra           | VARCHAR                  |           6 |       0 |      1290520 | 0.0%        | 100.0%           | BAIXA           |
| fpd             | VARCHAR                  |           2 |       0 |      1290524 | 0.0%        | 100.0%           | BAIXA           |
| flag_instalacao | BOOLEAN                  |           1 |       0 |      1290525 | 0.0%        | 100.0%           | BAIXA           |
| flag_mig2       | VARCHAR                  |           1 |       0 |      1290525 | 0.0%        | 100.0%           | BAIXA           |
| prod            | VARCHAR                  |           1 |       0 |      1290525 | 0.0%        | 100.0%           | BAIXA           |
| score_01        | INTEGER                  |         330 |    9439 |      1290196 | 0.73%       | 99.97%           | BAIXA           |
| score_02        | INTEGER                  |         598 |     576 |      1289928 | 0.04%       | 99.95%           | BAIXA           |
| ingestion_ts    | TIMESTAMP WITH TIME ZONE |           1 |       0 |      1290525 | 0.0%        | 100.0%           | BAIXA           |
| run_id          | VARCHAR                  |           1 |       0 |      1290525 | 0.0%        | 100.0%           | BAIXA           |
| ano_mes         | BIGINT                   |           6 |       0 |      1290520 | 0.0%        | 100.0%           | BAIXA           |

---

### 📦 Volumetria: `silver/score_bureau_movel`
| diretorio      |   qtd_arquivos | registros   |   colunas |   tamanho_comprimido_mib |   tamanho_descomprimido_mib |
|:---------------|---------------:|:------------|----------:|-------------------------:|----------------------------:|
| ano_mes=202410 |              1 | 203.828     |        11 |                     2.06 |                        3.47 |
| ano_mes=202411 |              1 | 227.176     |        11 |                     2.3  |                        3.87 |
| ano_mes=202412 |              1 | 227.985     |        11 |                     2.3  |                        3.88 |
| ano_mes=202501 |              1 | 221.002     |        11 |                     2.23 |                        3.77 |
| ano_mes=202502 |              1 | 203.139     |        11 |                     2.05 |                        3.46 |
| ano_mes=202503 |              1 | 207.396     |        11 |                     2.1  |                        3.53 |
| TOTAL          |              6 | 1.290.526   |        11 |                    13.04 |                       21.98 |

---

### 📅 Range de Datas: `silver/score_bureau_movel`
#### Coluna: `ingestion_ts`
| min                              | max                              |
|:---------------------------------|:---------------------------------|
| 2026-01-08 17:47:37.193060-03:00 | 2026-01-08 17:47:37.193060-03:00 |



---

### 🔢 Range de Valores Numéricos: `silver/score_bureau_movel`

#### Coluna: `score_01`
|   min |   max |   media |
|------:|------:|--------:|
|     0 |   778 |   586.9 |

#### Coluna: `score_02`
|   min |   max |   media |
|------:|------:|--------:|
|     1 |   917 |  627.55 |



---

### 🔟 Distribuição de Valores (Top 10): `silver/score_bureau_movel`
#### Coluna: `num_cpf`

| valor       |   qtd |
|:------------|------:|
| ZW9TYZXTWTZ |     5 |
| XUWNXZXN7ZU |     4 |
| TN8Y7XTNZ87 |     4 |
| Z9XN9ZZWU7T |     4 |
| 8Z7UTZ9XZ9X |     4 |
| ZUNUNZZNTZY |     4 |
| ZYWUTZXXTU8 |     4 |
| 78X9UYXZTWU |     4 |
| XWYWZZZNNNN |     4 |
| T87Z88U7U87 |     4 |

#### Coluna: `safra`

| valor      |    qtd |
|:-----------|-------:|
| 2024-12-01 | 227985 |
| 2024-11-01 | 227176 |
| 2025-01-01 | 221002 |
| 2025-03-01 | 207396 |
| 2024-10-01 | 203828 |
| 2025-02-01 | 203139 |

#### Coluna: `fpd`

| valor   |    qtd |
|:--------|-------:|
| false   | 986330 |
| true    | 304196 |

#### Coluna: `flag_instalacao`

| valor   |     qtd |
|:--------|--------:|
| true    | 1290526 |

#### Coluna: `flag_mig2`

| valor   |     qtd |
|:--------|--------:|
| PRE     | 1290526 |

#### Coluna: `prod`

| valor   |     qtd |
|:--------|--------:|
| CMV     | 1290526 |

#### Coluna: `score_01`

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

#### Coluna: `score_02`

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

#### Coluna: `ingestion_ts`

| valor                        |     qtd |
|:-----------------------------|--------:|
| 2026-01-08 17:47:37.19306-03 | 1290526 |

#### Coluna: `run_id`

|           valor |     qtd |
|----------------:|--------:|
| 20260110_052433 | 1290526 |

#### Coluna: `ano_mes`

|   valor |    qtd |
|--------:|-------:|
|  202412 | 227985 |
|  202411 | 227176 |
|  202501 | 221002 |
|  202503 | 207396 |
|  202410 | 203828 |
|  202502 | 203139 |



---

