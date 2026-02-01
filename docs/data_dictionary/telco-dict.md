# 📖 Dicionário de Dados Silver: `telco`

Este documento descreve a estrutura técnica e funcional da tabela de **Telco** na camada Silver. Esta entidade consolida atributos de comportamento de rede, consumo de dados e serviços de telecomunicações vinculados ao cliente.

---

## 🛠️ Grão da Tabela (Unicidade)

O grão desta tabela é definido pela combinação das seguintes chaves, garantindo a unicidade do perfil de consumo por safra e produto:
* `num_cpf` + `safra` + `prod`

---

## 🧬 Dicionário de Atributos

### 🔑 Chaves e Identificadores
| Variável | Tipo | Descrição |
| :--- | :--- | :--- |
| `num_cpf` | VARCHAR | **Coluna Mascarada (LGPD):** Identificador único do cliente (Hash/Anonimizado). |
| `safra` | DATE | Data de referência do snapshot de consumo (sempre dia 01 do mês). |
| `prod` | VARCHAR | Código do produto telco associado ao registro (Ex: CMV, NET, DTH). |

---

### 📊 Indicadores e Variáveis de Negócio
| Variável | Tipo | Descrição |
| :--- | :--- | :--- |
| `flag_instalacao` | BOOLEAN | Indicador de ativação ou instalação técnica do serviço concluída. |
| `flag_mig2` | VARCHAR | Tipo de movimentação do cliente na base (Ex: Migração, Nova Venda). |
| `fpd` | BOOLEAN | **Target Potencial:** Indicador de inadimplência no primeiro pagamento (First Payment Default). |

---

### 🔒 Variáveis com Nomes Anonimizados (Feature Set)
*As colunas abaixo representam atributos técnicos de uso, tráfego e rede cujos **nomes originais das colunas foram anonimizados** por questões de governança e segredo de negócio. Os registros internos (valores) são os dados reais de consumo utilizados para o treinamento do modelo.*

| Variável | Tipo | Descrição |
| :--- | :--- | :--- |
| `var_NN` | - | **Nomes Anonimizados:** Conjunto de 68 variáveis (numéricas e categóricas) que detalham volumetria de dados, minutos de voz, frequência de SMS, tipos de tecnologia utilizada e comportamento de rede. |

---

### ⚙️ Metadados de Processamento
| Variável | Tipo | Descrição |
| :--- | :--- | :--- |
| `ingestion_ts` | TIMESTAMP | Data e hora exata do processamento na camada Silver. |
| `run_id` | BIGINT | Identificador único da execução da pipeline de dados. |
| `ano_mes` | BIGINT | Partição física do dado no Data Lake (Formato YYYYMM). |

---

> **Finalidade:** Estes atributos compõem o bloco de variáveis de teleco (`tel_`) na Camada Gold. Eles fornecem sinais granulares de comportamento de uso que possuem alta correlação estatística com a propensão de pagamento e risco de crédito.