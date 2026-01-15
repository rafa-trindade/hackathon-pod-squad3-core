# Relatório de Profiling: `gold/labels_fpd` - `20260115_140241`

### 🔑 Garantia de Unicidade: `gold/labels_fpd`
- **Chave Técnica:** `num_cpf, safra, prod`
- **Tipo:** `COMPOSTA`

| coluna        |   distintos |   nulos |   duplicados | pct_nulos   | pct_duplicados   | cardinalidade   |
|:--------------|------------:|--------:|-------------:|:------------|:-----------------|:----------------|
| CHAVE_TECNICA |     1321168 |       0 |            0 | 0.0%        | 0.0%             | MÁXIMA          |

### 🚩 Diagnóstico e Observações Técnicas
* ✅ **Sucesso:** Unicidade Garantida. O grão da tabela está preservado.


---

### 📊 Schema e Estatísticas: `gold/labels_fpd`
| column_name               | column_type              |   distintos |   nulos |   duplicados | pct_nulos   | pct_duplicados   | cardinalidade   |
|:--------------------------|:-------------------------|------------:|--------:|-------------:|:------------|:-----------------|:----------------|
| num_cpf                   | VARCHAR                  |     1187719 |       0 |       133449 | 0.0%        | 10.1%            | ALTA            |
| safra                     | DATE                     |           6 |       0 |      1321162 | 0.0%        | 100.0%           | BAIXA           |
| prod                      | VARCHAR                  |           3 |       0 |      1321165 | 0.0%        | 100.0%           | BAIXA           |
| fpd                       | INTEGER                  |           2 |       0 |      1321166 | 0.0%        | 100.0%           | BAIXA           |
| flag_instalacao_resolvida | BOOLEAN                  |           1 |       0 |      1321167 | 0.0%        | 100.0%           | BAIXA           |
| run_id                    | VARCHAR                  |           1 |       0 |      1321167 | 0.0%        | 100.0%           | BAIXA           |
| ingestion_ts              | TIMESTAMP WITH TIME ZONE |           1 |       0 |      1321167 | 0.0%        | 100.0%           | BAIXA           |
| ano_mes                   | BIGINT                   |           6 |       0 |      1321162 | 0.0%        | 100.0%           | BAIXA           |

---

### 📦 Volumetria: `gold/labels_fpd`
| diretorio      |   qtd_arquivos | registros   |   colunas |   tamanho_comprimido_mib |   tamanho_descomprimido_mib |
|:---------------|---------------:|:------------|----------:|-------------------------:|----------------------------:|
| ano_mes=202410 |              1 | 207.953     |         8 |                     1.88 |                        3.09 |
| ano_mes=202411 |              1 | 231.824     |         8 |                     2.09 |                        3.44 |
| ano_mes=202412 |              1 | 232.984     |         8 |                     2.1  |                        3.46 |
| ano_mes=202501 |              1 | 226.446     |         8 |                     2.05 |                        3.36 |
| ano_mes=202502 |              1 | 208.731     |         8 |                     1.89 |                        3.1  |
| ano_mes=202503 |              1 | 213.230     |         8 |                     1.93 |                        3.17 |
| TOTAL          |              6 | 1.321.168   |         8 |                    11.93 |                       19.62 |

---

### 📅 Range de Datas: `gold/labels_fpd`
#### Coluna: `safra`
| min                        | max                        |
|:---------------------------|:---------------------------|
| 2024-10-01T00:00:00.000000 | 2025-03-01T00:00:00.000000 |

#### Coluna: `ingestion_ts`
| min                              | max                              |
|:---------------------------------|:---------------------------------|
| 2026-01-15 11:02:41.369506-03:00 | 2026-01-15 11:02:41.369506-03:00 |



---

### 🔢 Range de Valores Numéricos: `gold/labels_fpd`

#### Coluna: `fpd`
|   min |   max |   media |
|------:|------:|--------:|
|     0 |     1 |    0.24 |



---

### 🔟 Distribuição de Valores (Top 10): `gold/labels_fpd`
#### Coluna: `num_cpf`

| valor       |   qtd |
|:------------|------:|
| ZTZTWZXTYZX |     5 |
| ZWZT9ZZUZU8 |     5 |
| XYTY9ZX879Z |     5 |
| T9ZYTXZ7WYZ |     5 |
| Y97YZZX88TY |     5 |
| ZW9TYZXTWTZ |     5 |
| YTWN99NY8ZU |     5 |
| XYUZ8ZXUUZ9 |     5 |
| XXWXUNN8UTT |     4 |
| U89WNW7TWWU |     4 |

#### Coluna: `safra`

| valor      |    qtd |
|:-----------|-------:|
| 2024-12-01 | 232984 |
| 2024-11-01 | 231824 |
| 2025-01-01 | 226446 |
| 2025-03-01 | 213230 |
| 2025-02-01 | 208731 |
| 2024-10-01 | 207953 |

#### Coluna: `prod`

| valor   |     qtd |
|:--------|--------:|
| CMV     | 1308974 |
| NET     |   10043 |
| DTH     |    2151 |

#### Coluna: `fpd`

|   valor |     qtd |
|--------:|--------:|
|       0 | 1006838 |
|       1 |  314330 |

#### Coluna: `flag_instalacao_resolvida`

| valor   |     qtd |
|:--------|--------:|
| true    | 1321168 |

#### Coluna: `run_id`

|           valor |     qtd |
|----------------:|--------:|
| 20260115_140241 | 1321168 |

#### Coluna: `ingestion_ts`

| valor                         |     qtd |
|:------------------------------|--------:|
| 2026-01-15 11:02:41.369506-03 | 1321168 |

#### Coluna: `ano_mes`

|   valor |    qtd |
|--------:|-------:|
|  202412 | 232984 |
|  202411 | 231824 |
|  202501 | 226446 |
|  202503 | 213230 |
|  202502 | 208731 |
|  202410 | 207953 |



---

