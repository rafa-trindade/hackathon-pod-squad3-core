# 🧹 Política de Retenção de Dados no Data Lake

**Objetivo:** Definir diretrizes de retenção de dados no Data Lake, equilibrando custos de armazenamento, governança de dados e resiliência operacional para processos de reprocessamento e rollback.

---

### 1. Visão Geral: Estratégia de Versionamento Técnico

Adotamos uma abordagem de **Imutabilidade por Execução**. Em vez de sobrescrever dados existentes, cada ciclo do pipeline (Job) cria uma nova versão lógica do dataset completo ou particionado, garantindo isolamento total entre execuções.

#### 1.1 O Identificador `run_id`

* **Definição:** O `run_id` é um carimbo de tempo (Timestamp) no formato `YYYYMMDD_HHMMSS`.
* **Função:** Atuar como um contêiner técnico para uma fotografia completa do dataset naquele instante.
* **Estrutura física no S3:** `s3://lake/{camada}/{dataset}/run_id=YYYYMMDD_HHMMSS/`

---

### 2. Regras de Retenção (Purge Policy)

A retenção é gerenciada de forma automatizada pelo utilitário `lake_retention.py`, baseando-se na quantidade de execuções bem-sucedidas.

#### 2.1 Retenção Baseada em Runs (Exemplo: Bronze)

* **Parâmetro:** `MAX_RUNS` (configurável via variável de ambiente ou código).
* **Lógica:** Mantemos as **N** versões mais recentes e removemos fisicamente as versões excedentes.
* **Segurança:** A run atual é explicitamente protegida e nunca é alvo de deleção.

**Exemplo Prático (`MAX_RUNS = 2`):**
1.  **Run T0:** Escrita finalizada (Total: 1 run).
2.  **Run T1:** Escrita finalizada. Política mantem T0 e T1 (Total: 2 runs).
3.  **Run T2:** Escrita finalizada. Política identifica excedente e **remove T0**. Restam T1 e T2.

#### 2.2 Momento da Limpeza (Atomicidade Operacional)

A limpeza **nunca** precede a escrita. O fluxo obedece rigorosamente a seguinte ordem:
1.  **Escrita:** Novos dados são persistidos na nova `run_id`.
2.  **Validação:** O processo de escrita deve retornar código de sucesso.
3.  **Purge:** O utilitário de limpeza é invocado para remover as runs obsoletas.

> 💡 **Benefício:** Se o pipeline falhar no meio da transformação, os dados da run anterior permanecem intactos, garantindo que o consumo nunca fique indisponível.

---

### 3. Considerações por Camada

| Camada | Estratégia de Retenção | Justificativa |
| :--- | :--- | :--- |
| **RAW** | Histórico Longo / Permanente | Garantir a capacidade de reconstruir todo o Lake a partir do dado bruto se necessário. |
| **BRONZE** | Curta (1 a 3 runs) | Camada intermediária de tipagem. Requer histórico apenas para validação imediata e rollback técnico. |
| **SILVER** | Moderada | Dados limpos e padronizados. Retenção maior para suportar análises históricas e reprocessamentos de Gold. |
| **GOLD** | Específica por Modelo | Governança baseada no ciclo de vida dos modelos de ML e requisitos de auditoria. |

---

### 4. Implementação e Governança

A lógica de limpeza é centralizada no módulo `scripts/transformations/utils/lake_retention.py`, utilizando a biblioteca `boto3` para operações atômicas no S3.

**Responsabilidades:**
* **Engenharia de Dados:** Configurar o parâmetro `MAX_RUNS` adequado para a volumetria de cada dataset.
* **Infraestrutura/Cloud:** Monitorar logs de deleção e métricas de custo do S3.

---

### 5. Observações Finais

Esta política foca na **higiene técnica** do Lake. Ela não substitui:
1.  **Backup de Desastre:** Gerenciado por políticas de versionamento e replicação do S3.
2.  **Arquivamento de Longo Prazo:** Dados obsoletos de negócio devem ser movidos para classes de armazenamento de baixo custo (S3 Glacier) conforme legislação vigente (LGPD).