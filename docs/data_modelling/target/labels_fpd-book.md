# 📖 Book de Variáveis - Camada Gold (`labels_fpd`)

Este documento descreve as definições de negócio e o grão da tabela âncora que serve como base para o cálculo do Target (FPD).

---

## 🛠️ Metadados e Chaves (Grão)

| Variável | Tipo | Domínio | Descrição |
| :--- | :--- | :--- | :--- |
| `num_cpf` | VARCHAR | Identificador | CPF do cliente (anonimizado/hash). |
| `safra` | DATE | Temporal | Data de referência da concessão (sempre dia 01). |
| `prod` | VARCHAR | Produto | Código do produto associado à linha/contrato. |
| `fpd` | BOOLEAN | **Target** | Indicador de First Payment Default (1: Inadimplente, 0: Adimplente). |
| `flag_instalacao` | BOOLEAN | Filtro | Indica se houve instalação técnica confirmada (1/0). |
| `ano_mes` | BIGINT | Partição | Chave física de particionamento (YYYYMM). |

---

## 🎯 Regra de Negócio do Target (FPD)

O **FPD (First Payment Default)** é a nossa variável resposta. Ela é definida na camada Silver através do cruzamento entre a base de faturas e o status de pagamento do primeiro mês pós-concessão.
- **Valor 1:** Cliente não efetuou o primeiro pagamento em até X dias após o vencimento.
- **Valor 0:** Cliente efetuou o pagamento integral da primeira fatura.

---

## 🧪 Notas de Qualidade

1. **Unicidade:** Garantida pela combinação `num_cpf` + `safra` + `prod`.
2. **Saneamento:** Registros com `fpd` nulo são removidos durante a promoção para a camada Gold, garantindo uma base limpa para o treino.