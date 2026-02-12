# Relatório de Profiling: `gold/labels_fpd_bureau` - `20260212`

### 🔑 Garantia de Unicidade: `gold/labels_fpd_bureau`
- **Chave Técnica:** `num_cpf, safra, prod`
- **Tipo:** `COMPOSTA`

| coluna        |   distintos |   nulos |   duplicados | pct_nulos   | pct_duplicados   | cardinalidade   |
|:--------------|------------:|--------:|-------------:|:------------|:-----------------|:----------------|
| CHAVE_TECNICA |     2633900 |       0 |            0 | 0.0%        | 0.0%             | MÁXIMA          |

### 🚩 Diagnóstico e Observações Técnicas
* ✅ **Sucesso:** Unicidade Garantida. O grão da tabela está preservado.


---

### 📊 Schema e Estatísticas: `gold/labels_fpd_bureau`
| column_name     | column_type              |   distintos |   nulos |   duplicados | pct_nulos   | pct_duplicados   | cardinalidade   |
|:----------------|:-------------------------|------------:|--------:|-------------:|:------------|:-----------------|:----------------|
| num_cpf         | VARCHAR                  |     2341772 |       0 |       292128 | 0.0%        | 11.09%           | ALTA            |
| safra           | DATE                     |           6 |       0 |      2633894 | 0.0%        | 100.0%           | BAIXA           |
| prod            | VARCHAR                  |           1 |       0 |      2633899 | 0.0%        | 100.0%           | BAIXA           |
| fpd             | BOOLEAN                  |           2 |       0 |      2633898 | 0.0%        | 100.0%           | BAIXA           |
| flag_instalacao | BOOLEAN                  |           1 |       0 |      2633899 | 0.0%        | 100.0%           | BAIXA           |
| run_id          | BIGINT                   |           1 |       0 |      2633899 | 0.0%        | 100.0%           | BAIXA           |
| ingestion_ts    | TIMESTAMP WITH TIME ZONE |           1 |       0 |      2633899 | 0.0%        | 100.0%           | BAIXA           |
| ano_mes         | BIGINT                   |           6 |       0 |      2633894 | 0.0%        | 100.0%           | BAIXA           |

---

### 📦 Volumetria: `gold/labels_fpd_bureau`
| diretorio      |   qtd_arquivos | registros   |   colunas |   tamanho_comprimido_mib |   tamanho_descomprimido_mib |
|:---------------|---------------:|:------------|----------:|-------------------------:|----------------------------:|
| ano_mes=202410 |              1 | 426.104     |         8 |                     3.8  |                        6.2  |
| ano_mes=202411 |              1 | 454.572     |         8 |                     4.05 |                        6.61 |
| ano_mes=202412 |              1 | 445.154     |         8 |                     3.97 |                        6.48 |
| ano_mes=202501 |              1 | 452.621     |         8 |                     4.03 |                        6.58 |
| ano_mes=202502 |              1 | 419.453     |         8 |                     3.75 |                        6.1  |
| ano_mes=202503 |              1 | 435.996     |         8 |                     3.89 |                        6.34 |
| TOTAL          |              6 | 2.633.900   |         8 |                    23.5  |                       38.31 |

---

### 📅 Range de Datas: `gold/labels_fpd_bureau`
#### Coluna: `safra`
| min                        | max                        |
|:---------------------------|:---------------------------|
| 2024-10-01T00:00:00.000000 | 2025-03-01T00:00:00.000000 |

#### Coluna: `ingestion_ts`
| min                              | max                              |
|:---------------------------------|:---------------------------------|
| 2026-02-12 01:29:41.180523-03:00 | 2026-02-12 01:29:41.180523-03:00 |



---

### 🔢 Range de Valores Numéricos: `gold/labels_fpd_bureau`

> ⚠️ Nenhuma coluna numérica relevante encontrada.



---

### 🔟 Distribuição de Valores (Top 10): `gold/labels_fpd_bureau`
#### Coluna: `num_cpf`

| valor       |   qtd |
|:------------|------:|
| ZZZZZZZX7T9 |     6 |
| 7X7NZ79YWU9 |     6 |
| ZW9TYZXTWTZ |     5 |
| XYUZ8ZXUUZ9 |     5 |
| ZTZTWZXTYZX |     5 |
| XYTY9ZX879Z |     5 |
| ZZTZ799U79T |     5 |
| Y97YZZX88TY |     5 |
| ZZTU7ZZZY78 |     5 |
| YY8U879X87Z |     5 |

#### Coluna: `safra`

| valor      |    qtd |
|:-----------|-------:|
| 2024-11-01 | 454572 |
| 2025-01-01 | 452621 |
| 2024-12-01 | 445154 |
| 2025-03-01 | 435996 |
| 2024-10-01 | 426104 |
| 2025-02-01 | 419453 |

#### Coluna: `prod`

| valor   |     qtd |
|:--------|--------:|
| CMV     | 2633900 |

#### Coluna: `fpd`

| valor   |     qtd |
|:--------|--------:|
| false   | 2074671 |
| true    |  559229 |

#### Coluna: `flag_instalacao`

| valor   |     qtd |
|:--------|--------:|
| true    | 2633900 |

#### Coluna: `run_id`

|    valor |     qtd |
|---------:|--------:|
| 20260212 | 2633900 |

#### Coluna: `ingestion_ts`

| valor                         |     qtd |
|:------------------------------|--------:|
| 2026-02-12 01:29:41.180523-03 | 2633900 |

#### Coluna: `ano_mes`

|   valor |    qtd |
|--------:|-------:|
|  202411 | 454572 |
|  202501 | 452621 |
|  202412 | 445154 |
|  202503 | 435996 |
|  202410 | 426104 |
|  202502 | 419453 |



---

