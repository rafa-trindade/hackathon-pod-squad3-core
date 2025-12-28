## 🧹 Política de Retenção de Dados no Data Lake

**Objetivo:**  
Definir diretrizes de retenção de dados no Data Lake, equilibrando custo de armazenamento,
capacidade de reprocessamento, governança e confiabilidade operacional.

### 1. Visão Geral

Para evitar crescimento descontrolado de armazenamento e garantir governança operacional, foi definida uma política de retenção baseada em runs nas camadas do Data Lake.

---

#### 1.1 Estratégia de Retenção

- A retenção é aplicada por dataset e por camada
- Cada execução do pipeline gera uma nova pasta lógica identificada por `run_id`
- O `run_id` é um identificador **técnico de execução**, não representando versão de negócio dos dados

*Estrutura padrão:*

`s3://lake/{camada}/{dataset}/`<br>
  └── run_id=YYYYMMDD_HHMMSS/

*Exemplo:*

`s3://lake/bronze/dados_cadastrais/`<br>
  ├── run_id=20251226_091200/  
  ├── run_id=20251227_101530/  
  └── run_id=20251228_175545/

---

#### 1.2 Regra de Retenção (ex: Bronze)

- Quantidade máxima de runs mantidas: configurável via parâmetro
- Padrão atual: manter apenas as N runs mais recentes
- Runs mais antigas são removidas automaticamente após uma execução bem-sucedida

*Exemplo de configuração:*

```python
BRONZE_MAX_RUNS = 3
```

Com essa configuração:
- A run atual nunca é removida
- A run imediatamente anterior é preservada
- Todas as runs mais antigas são excluídas

---

#### 1.3 Momento da Limpeza

A limpeza ocorre somente após a escrita bem-sucedida dos dados.

- Em caso de falha na ingestão ou transformação:
  - Nenhuma run anterior é removida
  - Garante-se capacidade de rollback e reprocessamento

- Essa abordagem garante que:
  - Nenhuma execução válida seja perdida
  - O ambiente permaneça consistente mesmo em falhas intermediárias

*Exemplo de Fluxo:*

`RAW → BRONZE` *(write OK)*<br>
  ↓  
Aplicação da política de retenção

---

#### 1.4 Implementação Técnica

A retenção é implementada via utilitário reutilizável: `scripts/transformations/utils/lake_retention.py`

A função:
  - Lista diretórios run_id=*
  - Ordena por data (mais recentes primeiro)
  - Remove apenas os objetos das runs excedentes
  - Protege explicitamente o run_id da execução atual

---

#### 1.5 Benefícios da Estratégia

- Controle de custos de armazenamento
- Parametrização da retenção por dataset (valores distintos de runs por base)
- Histórico operacional suficiente para auditoria e troubleshooting
- Simplicidade operacional
- Alinhado a padrões modernos de Data Lake

---

#### 1.6 Considerações por Camada

Camada: `RAW`<br>
**Estratégia:** Pode manter histórico maior ou completo, conforme custo e criticidade <br>
*Para este projeto, a retenção na camada RAW não está implementada, devido à característica de ingestão manual dos dados.*

Camada: `BRONZE`<br>
**Estratégia:** Retenção curta baseada em runs técnicas

Camada: `SILVER`<br>  
**Estratégia:** Retenção orientada a negócio e reprocessamento

Camada: `GOLD`<br>
**Estratégia:** Governada por SLA analítico e requisitos de ML

---

#### 1.7 Evoluções Futuras

Esta política foi definida de forma incremental e poderá evoluir conforme a maturidade da plataforma e necessidades do negócio.

Possíveis evoluções previstas:

- Retenção baseada em tempo (ex: dias) combinada com retenção por run
- Integração com métricas de custo e observabilidade do Data Lake

---

### 2. Escopo e Aplicabilidade

Esta política se aplica a:

- Pipelines de ingestão e transformação executados via código
- Camadas do Data Lake que utilizam versionamento técnico por execução (`run_id`)
- Ambientes onde há necessidade de controle de custo e reprocessamento controlado

Não se aplica a:

- Sistemas transacionais de origem
- Camadas analíticas finais com SLA de consumo direto (ex: marts BI expostos)

---

### 3. Responsabilidades

- **Engenharia de Dados**
  - Implementação e manutenção da política
  - Definição de parâmetros de retenção por camada/dataset

- **Arquitetura de Dados**
  - Revisão periódica da política
  - Alinhamento com padrões corporativos e boas práticas

- **Negócio / Analytics**
  - Definição de requisitos de histórico mínimo para consumo e auditoria

---

### 4. Observações Finais

A política de retenção não substitui estratégias de backup, versionamento de código ou controle de qualidade dos dados.

Seu objetivo é exclusivamente garantir equilíbrio entre:
- Governança
- Custo
- Confiabilidade operacional
- Capacidade de reprocessamento
