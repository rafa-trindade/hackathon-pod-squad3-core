# ✅ Política de Qualidade de Dados (Data Quality)

**Objetivo:** Estabelecer os critérios de aceitação, padrões de integridade e o framework de validação para garantir que os dados consumidos pela Squad 3 sejam confiáveis, íntegros e sigam os contratos definidos.

## 1. Framework de Qualidade

A qualidade de dados é aplicada de forma integrada ao pipeline de transformação, utilizando o conceito de **Data Contracts** (Contratos de Dados):

* **Validação de Contrato e Semântica (Pandera):** Garante que a estrutura física (schema) e tipagem estejam corretas no momento da persistência no Lake. Atua como o "portão de entrada" para a camada Silver.


## 2. Dimensões da Qualidade

| Dimensão | O que validamos | Ferramenta |
| :--- | :--- | :--- |
| **Integridade de Schema** | Tipagem correta e presença de colunas obrigatórias. | Pandera |
| **Unicidade** | Garantia de registros únicos por chave natural (Grão). | Pandera / DuckDB |
| **Conformidade** | Valores dentro de intervalos lógicos (ex: score 0-1000). | Pandera |
| **Completude** | Monitoramento de nulos e volumetria de carga. | Profiling / Gold Pipeline |
| **Saúde de Safra** | Representatividade volumétrica por período (regra 10%-90%). | Gold Pipeline Audit |
| **Overlap (Riqueza)** | Match de chaves entre camadas para garantir base "ML-Ready". | Gold Pipeline Audit |

## 3. Implementação Prática

### 3.1 Camada Raw -> Bronze (Sanidade)
Nesta fase, o foco é a **estabilidade**. Validamos se o arquivo recebido não sofreu *Schema Drift* (mudança inesperada de colunas).

### 3.2 Camada Bronze -> Silver (Contratos)
É a fase de maior rigor técnico, onde o dado é transformado em informação útil. Utilizamos **Pandera Schemas** para definir e forçar contratos rigorosos diretamente no processamento do Lake:

* **Controle de Nulos:** Definição estrita de quais colunas possuem obrigatoriedade de preenchimento (campo `nullable=False`).
* **Tipagem Forte:** Garantia de que colunas críticas (IDs, Datas, Valores) possuem o tipo primitivo correto para evitar erros em modelos de Machine Learning.

### 3.3 Camada Silver -> Gold (Auditoria de Pipeline)
Nesta fase, o foco é a **qualidade para modelagem**. Diferente das camadas anteriores, a validação aqui é macroscópica e estatística, garantindo que o dataset final seja robusto para treino e teste:

* **Audit de Overlap:** Validação programática do percentual de encontro de chaves (CPFs) entre a tabela âncora (Gold) e as fontes de features (Silver). É o critério que garante que o modelo terá informação suficiente para predizer o target.
* **Health Check de Safra:** Monitoramento da distribuição temporal para evitar safras "vazias" ou "viciadas" que possam enviesar o aprendizado do modelo.
* **Unicidade no Grão Final:** Última trava de segurança para garantir que não houve explosão de linhas nos cruzamentos (Joins).


## 4. Gestão de Falhas

Quando um teste de qualidade falha, o protocolo de governança define:
1.  **Isolamento:** A `run_id` problemática é identificada e não deve ser promovida para consumo final.
2.  **Trilha de Auditoria:** O erro é registrado nos logs de qualidade para diagnóstico rápido.
3.  **Ação Corretiva:** O motor de Retenção permite o rollback para a última `run_id` estável enquanto o erro de qualidade é corrigido no código ou na fonte.


## 5. Evidências e Relatórios

Os resultados das validações de qualidade são exportados e centralizados para transparência total da Squad e Stakeholders:

* **Relatórios Pandera (Schema):** [`reports/observability/quality/pandera/`](../../reports/observability/quality/pandera/)
* **Auditoria de Pipeline (Safra/Overlap):** [`reports/observability/quality/pipeline/`](../../reports/observability/quality/pipeline/)

---

**Observações Finais:** A qualidade não é uma etapa final, mas um processo contínuo integrado ao pipeline de transformação (*Data Quality as Code*).
