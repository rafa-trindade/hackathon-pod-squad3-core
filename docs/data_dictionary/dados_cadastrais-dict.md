# 📖 Dicionário de Dados Silver: `dados_cadastrais`

Este documento descreve a estrutura técnica e funcional da tabela de **Dados Cadastrais** na camada Silver. Esta entidade centraliza o perfil demográfico e os atributos estáticos dos clientes por período de observação.

---

## 🛠️ Grão da Tabela (Unicidade)

O grão desta tabela é definido pela combinação das seguintes chaves, garantindo a unicidade do perfil do cliente por safra e produto:
* `num_cpf` + `safra` + `prod`

---

## 🧬 Dicionário de Atributos

### 🔑 Chaves e Identificadores
| Variável | Tipo | Descrição |
| :--- | :--- | :--- |
| `num_cpf` | VARCHAR | **Coluna Mascarada (LGPD):** Identificador único do cliente (Hash). |
| `safra` | DATE | Data de referência do snapshot cadastral (sempre dia 01). |
| `prod` | VARCHAR | Código do produto associado ao registro (Ex: CMV, NET, DTH). |

---

### 👤 Perfil Demográfico e Indicadores de Negócio
| Variável | Tipo | Descrição |
| :--- | :--- | :--- |
| `datadenascimento` | DATE | Data de nascimento do cliente. |
| `cep_3_digitos` | VARCHAR | **Coluna Mascarada (LGPD):** Truncamento do CEP para análise regional. |
| `statusrf` | VARCHAR | Situação cadastral do CPF perante a Receita Federal. |
| `flag_instalacao` | BOOLEAN | Indicador de conclusão de instalação técnica do produto. |
| `flag_mig2` | VARCHAR | Indicador do tipo de entrada ou migração do cliente. |
| `fpd` | BOOLEAN | **Target Potencial:** Indicador de inadimplência no primeiro pagamento. |

---

### 🔒 Variáveis com Nomes Anonimizados (Feature Set)
*As colunas abaixo representam atributos de negócio cujos **nomes originais foram anonimizados** por questões de governança e segredo de negócio. Os registros contidos nestas colunas são dados reais utilizados para o treinamento do modelo.*

| Variável | Tipo | Descrição |
| :--- | :--- | :--- |
| `var_NN` | - | **Nomes Anonimizados:** Conjunto de variáveis (numéricas, datas e categóricas) representando perfis ocupacionais, faixas de renda, pontuações e indicadores de risco. |

---

### ⚙️ Metadados de Processamento
| Variável | Tipo | Descrição |
| :--- | :--- | :--- |
| `ingestion_ts` | TIMESTAMP | Data e hora exata do processamento na camada Silver. |
| `run_id` | BIGINT | Identificador único da execução da pipeline. |
| `ano_mes` | BIGINT | Partição física do dado no Data Lake (YYYYMM). |

---

> **Finalidade:** Estes atributos compõem o bloco de variáveis de cadastro (`cad_`) na Camada Gold, fundamentais para a segmentação de risco e análise de aderência de perfil para o produto CMV.