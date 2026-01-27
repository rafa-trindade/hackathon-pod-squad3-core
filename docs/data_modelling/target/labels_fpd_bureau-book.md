# 📖 Book de Variáveis - Camada Gold (`labels_fpd_bureau`)

Este documento descreve as definições de negócio e o grão da tabela âncora baseada no Score de Bureau, servindo como base oficial para o cálculo do Target (FPD) do público CMV.

---

## 🛠️ Metadados e Chaves (Grão)

| Variável | Tipo | Domínio | Descrição |
| :--- | :--- | :--- | :--- |
| `num_cpf` | VARCHAR | Identificador | CPF do cliente (anonimizado/hash). |
| `safra` | DATE | Temporal | Mês de geração do Score no Bureau (sempre dia 01). |
| `prod` | VARCHAR | Produto | Código do produto (Fixo em **CMV** para este público). |
| `fpd` | BOOLEAN | **Target** | Indicador de First Payment Default (1: Inadimplente, 0: Adimplente). |
| `flag_instalacao` | BOOLEAN | Filtro | Indica se houve instalação técnica (Enriquecimento via Telco Silver). |
| `ano_mes` | BIGINT | Partição | Chave física de particionamento (YYYYMM). |

---

## 🎯 Regra de Negócio do Target (Público Bureau CMV)

O **FPD (First Payment Default)** nesta tabela é restrito ao público presente na base `score_bureau_movel`. Esta âncora garante que a modelagem foque exclusivamente no produto CMV, atendendo às diretrizes técnicas de evitar distorções com produtos NET/DTH.

- **Definição:** Cruzamento entre a safra do Bureau e o status de pagamento da primeira fatura gerada após a concessão do score.
- **Valor 1:** Inadimplência confirmada no primeiro ciclo.
- **Valor 0:** Pagamento integral identificado.

---

## 🧪 Notas de Qualidade

1. **Unicidade:** Garantida pela combinação `num_cpf` + `safra` + `prod`.
2. **Fidelidade de Público:** Diferente da `labels_fpd` genérica, esta base passa por uma validação de aderência ao Score Bureau Móvel.
3. **Saneamento:** Registros com `fpd` nulo ou sem correspondência na base de score são descartados para manter a pureza do público-alvo CMV.