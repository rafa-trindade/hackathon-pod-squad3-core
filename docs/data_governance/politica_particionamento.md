## 🧭 Política de Particionamento no Data Lake

**Objetivo:**  
Documentar o **padrão de particionamento e uso de colunas temporais**
adotado neste projeto, registrando as decisões técnicas aplicadas
na organização dos dados no Data Lake.

---

### 1. Visão Geral

Para garantir organização temporal, previsibilidade de leitura e suporte à modelagem
nas camadas posteriores, foi definido um padrão de particionamento baseado
em colunas de tempo explícitas na camada Bronze.

Neste projeto, todos os datasets da camada **Bronze** possuem
um **eixo temporal definido**, utilizado para:

- Organização física dos dados no Data Lake
- Particionamento eficiente por período
- Base para joins e consolidação na camada Gold

Os dados foram classificados em dois tipos principais:

- **Snapshots mensais**
- **Eventos**

---

#### 1.1 Padrão Adotado - Camada Bronze

| Base               | Tipo            | Coluna de referência  | Coluna técnica | Particionamento   | Exemplo             |
|--------------------|-----------------|-----------------------|----------------|-------------------|---------------------|
| atraso             | Snapshot mensal | DAT_REFERENCIA        | safra          | safra=YYYYMM      | safra=202501        |
| pagamento          | Evento          | DAT_STATUS_FATURA     | data_evento    | ano=YYYY/mes=MM   | ano=2025/mes=01     |
| recarga            | Evento          | DAT_INSERCAO_CREDITO  | data_evento    | ano=YYYY/mes=MM   | ano=2025/mes=03     |
| dados_cadastrais   | Snapshot mensal | SAFRA                 | safra          | safra=YYYYMM      | safra=202501        |
| score_bureau_movel | Snapshot mensal | SAFRA                 | safra          | safra=YYYYMM      | safra=202501        |
| telco              | Snapshot mensal | SAFRA                 | safra          | safra=YYYYMM      | safra=202501        |

---

#### 1.2 Decisões Técnicas

- Snapshots mensais utilizam **SAFRA (YYYYMM)** como referência temporal
- Bases de evento utilizam a **data real de ocorrência**
- A coluna técnica temporal é padronizada para facilitar leitura e reutilização
- O particionamento reflete a **granularidade real do dado**, evitando distorções

Essas decisões facilitam:

- Reprocessamentos por período
- Leitura seletiva de dados
- Consolidação na camada Silver
- Consumo e modelagem na camada Gold

---

### 2. Relação com as Outras Camadas

**Camada: Bronze**  
Dados organizados e particionados por tempo, refletindo a forma como são recebidos das fontes,
sem aplicação de regras de negócio.

**Camada: Silver**  
Consolidação e padronização, mantendo e respeitando
o período de referência definido na Bronze.

**Camada: Gold**  
Camada final voltada à **modelagem para Machine Learning**, com datasets construídos
a partir de períodos de referência explícitos e controlados conforme a necessidade dos modelos.

---

### 3. Observações Finais

Este documento descreve **as decisões adotadas neste projeto específico**
para organização temporal e particionamento dos dados no Data Lake.

O padrão aqui documentado:
- Não é imutável
- Não representa um framework genérico
- Reflete exclusivamente as escolhas técnicas realizadas durante a implementação deste projeto
