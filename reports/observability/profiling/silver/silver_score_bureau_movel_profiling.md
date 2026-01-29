# Relatório de Profiling: `silver/score_bureau_movel` - `20260129`

### 🔑 Garantia de Unicidade: `silver/score_bureau_movel`
- **Chave Técnica:** `num_cpf, safra, prod`
- **Tipo:** `COMPOSTA`

| coluna        |   distintos |   nulos |   duplicados | pct_nulos   | pct_duplicados   | cardinalidade   |
|:--------------|------------:|--------:|-------------:|:------------|:-----------------|:----------------|
| CHAVE_TECNICA |     3795310 |       0 |            0 | 0.0%        | 0.0%             | MÁXIMA          |

### 🚩 Diagnóstico e Observações Técnicas
* ✅ **Sucesso:** Unicidade Garantida. O grão da tabela está preservado.


---

### 📊 Schema e Estatísticas: `silver/score_bureau_movel`
| column_name     | column_type              |   distintos |   nulos |   duplicados | pct_nulos   | pct_duplicados   | cardinalidade   |
|:----------------|:-------------------------|------------:|--------:|-------------:|:------------|:-----------------|:----------------|
| num_cpf         | VARCHAR                  |     3034069 |       0 |       761241 | 0.0%        | 20.06%           | ALTA            |
| safra           | DATE                     |           6 |       0 |      3795304 | 0.0%        | 100.0%           | BAIXA           |
| prod            | VARCHAR                  |           1 |       0 |      3795309 | 0.0%        | 100.0%           | BAIXA           |
| flag_instalacao | BOOLEAN                  |           2 |       0 |      3795308 | 0.0%        | 100.0%           | BAIXA           |
| flag_mig2       | VARCHAR                  |           3 | 1161410 |      3795307 | 30.6%       | 100.0%           | BAIXA           |
| fpd             | BOOLEAN                  |           2 | 1161410 |      3795308 | 30.6%       | 100.0%           | BAIXA           |
| score_01        | INTEGER                  |         355 |   54035 |      3794955 | 1.42%       | 99.99%           | BAIXA           |
| score_02        | INTEGER                  |         598 |    1876 |      3794712 | 0.05%       | 99.98%           | BAIXA           |
| ingestion_ts    | TIMESTAMP WITH TIME ZONE |           1 |       0 |      3795309 | 0.0%        | 100.0%           | BAIXA           |
| run_id          | BIGINT                   |           1 |       0 |      3795309 | 0.0%        | 100.0%           | BAIXA           |
| ano_mes         | BIGINT                   |           6 |       0 |      3795304 | 0.0%        | 100.0%           | BAIXA           |

---

### 📦 Volumetria: `silver/score_bureau_movel`
| diretorio      |   qtd_arquivos | registros   |   colunas |   tamanho_comprimido_mib |   tamanho_descomprimido_mib |
|:---------------|---------------:|:------------|----------:|-------------------------:|----------------------------:|
| ano_mes=202410 |              1 | 636.951     |        11 |                     6.48 |                       11.01 |
| ano_mes=202411 |              1 | 647.199     |        11 |                     6.59 |                       11.2  |
| ano_mes=202412 |              1 | 626.744     |        11 |                     6.39 |                       10.85 |
| ano_mes=202501 |              1 | 648.554     |        11 |                     6.6  |                       11.23 |
| ano_mes=202502 |              1 | 602.344     |        11 |                     6.15 |                       10.42 |
| ano_mes=202503 |              1 | 633.518     |        11 |                     6.45 |                       10.95 |
| TOTAL          |              6 | 3.795.310   |        11 |                    38.64 |                       65.66 |

---

### 📅 Range de Datas: `silver/score_bureau_movel`
#### Coluna: `safra`
| min                        | max                        |
|:---------------------------|:---------------------------|
| 2024-10-01T00:00:00.000000 | 2025-03-01T00:00:00.000000 |

#### Coluna: `ingestion_ts`
| min                              | max                              |
|:---------------------------------|:---------------------------------|
| 2026-01-29 01:47:56.641739-03:00 | 2026-01-29 01:47:56.641739-03:00 |



---

### 🔢 Range de Valores Numéricos: `silver/score_bureau_movel`

#### Coluna: `score_01`
|   min |   max |   media |
|------:|------:|--------:|
|     0 |   778 |  578.99 |

#### Coluna: `score_02`
|   min |   max |   media |
|------:|------:|--------:|
|     1 |   926 |  628.51 |



---

### 🔟 Distribuição de Valores (Top 10): `silver/score_bureau_movel`
#### Coluna: `num_cpf`

| valor       |   qtd |
|:------------|------:|
| Y77ZYUXU8NW |     6 |
| U8Z9ZZ8N8XZ |     6 |
| ZZZZZZZX7T9 |     6 |
| 7X7NZ79YWU9 |     6 |
| 888W78UZYYT |     6 |
| 9TUZT8Y8XU9 |     5 |
| ZNTN78ZW7XX |     5 |
| 7ZNUZYNWN8Y |     5 |
| ZY9NYT7NXWW |     5 |
| U79ZXXNY8ZT |     5 |

#### Coluna: `safra`

| valor      |    qtd |
|:-----------|-------:|
| 2025-01-01 | 648554 |
| 2024-11-01 | 647199 |
| 2024-10-01 | 636951 |
| 2025-03-01 | 633518 |
| 2024-12-01 | 626744 |
| 2025-02-01 | 602344 |

#### Coluna: `prod`

| valor   |     qtd |
|:--------|--------:|
| CMV     | 3795310 |

#### Coluna: `flag_instalacao`

| valor   |     qtd |
|:--------|--------:|
| true    | 2633900 |
| false   | 1161410 |

#### Coluna: `flag_mig2`

| valor     |     qtd |
|:----------|--------:|
| Aquisição | 1338888 |
| PRE       | 1290526 |
| NULL      | 1161410 |
| FLEX      |    4486 |

#### Coluna: `fpd`

| valor   |     qtd |
|:--------|--------:|
| false   | 2074671 |
| NULL    | 1161410 |
| true    |  559229 |

#### Coluna: `score_01`

| valor   |   qtd |
|:--------|------:|
| 589     | 64373 |
| 601     | 63565 |
| NULL    | 54035 |
| 571     | 53351 |
| 560     | 53313 |
| 582     | 48768 |
| 593     | 48286 |
| 574     | 46425 |
| 531     | 45087 |
| 599     | 43953 |

#### Coluna: `score_02`

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

#### Coluna: `ingestion_ts`

| valor                         |     qtd |
|:------------------------------|--------:|
| 2026-01-29 01:47:56.641739-03 | 3795310 |

#### Coluna: `run_id`

|    valor |     qtd |
|---------:|--------:|
| 20260129 | 3795310 |

#### Coluna: `ano_mes`

|   valor |    qtd |
|--------:|-------:|
|  202501 | 648554 |
|  202411 | 647199 |
|  202410 | 636951 |
|  202503 | 633518 |
|  202412 | 626744 |
|  202502 | 602344 |



---

