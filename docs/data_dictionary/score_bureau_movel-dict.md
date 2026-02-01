# 📖 Dicionário de Dados Silver: `score_bureau_movel`

Este documento descreve a estrutura técnica e funcional da tabela de **Bureau** na camada Silver. Esta entidade centraliza os indicadores oficiais de risco de crédito externos capturados para a base de clientes.

---

## 🛠️ Grão da Tabela (Unicidade)

O grão desta tabela é definido pela combinação das seguintes chaves, garantindo a unicidade do score por cliente, período de safra e produto:
* `num_cpf` + `safra` + `prod`

---

## 🧬 Dicionário de Atributos

### 🔑 Chaves e Identificadores
| Variável | Tipo | Descrição |
| :--- | :--- | :--- |
| `num_cpf` | VARCHAR | **Coluna Mascarada (LGPD):** Identificador único do cliente (Hash). |
| `safra` | DATE | Data de referência do snapshot do score (sempre dia 01). |
| `prod` | VARCHAR | Código do produto associado à consulta de bureau (Ex: CMV). |

---

### 📈 Indicadores de Crédito (Scores Oficiais)
| Variável | Tipo | Descrição |
| :--- | :--- | :--- |
| `score_01` | INTEGER | Primeiro indicador numérico de propensão de risco/crédito do parceiro externo. |
| `score_02` | INTEGER | Segundo indicador numérico de propensão de risco/crédito do parceiro externo. |

---

### 📊 Indicadores e Status de Negócio
| Variável | Tipo | Descrição |
| :--- | :--- | :--- |
| `fpd` | BOOLEAN | **Target Potencial:** Indicador de inadimplência no primeiro pagamento (First Payment Default). |
| `flag_instalacao` | BOOLEAN | Indicador de conclusão de instalação técnica do serviço. |
| `flag_mig2` | VARCHAR | Tipo de entrada/migração do cliente no portfólio (Ex: Aquisição, Pré). |

---

### ⚙️ Metadados de Processamento
| Variável | Tipo | Descrição |
| :--- | :--- | :--- |
| `ingestion_ts` | TIMESTAMP | Data e hora exata do processamento na camada Silver. |
| `run_id` | BIGINT | Identificador único da execução da pipeline. |
| `ano_mes` | BIGINT | Partição física do dado no Data Lake (YYYYMM). |

---

> **Finalidade:** Estes atributos compõem o bloco de variáveis de bureau (`bur_`) na Camada Gold, sendo cruciais para calibrar o motor de decisão de crédito com dados externos de mercado.