# Data Quality - `silver/clientes`

## Regras
- cpf → NOT NULL
- cpf → 11 caracteres
- data_nascimento → <= data_atual
- sexo → {M, F, OUTRO}

## SLAs (Service Level Agreement)
- Percentual de CPF nulo ≤ 0,1%
- Atraso máximo de ingestão ≤ 1 hora
