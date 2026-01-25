# 🏛️ Data Architecture: OCI Cloud Ready Strategy

Este documento detalha a estratégia de arquitetura para a prontidão em nuvem (**Cloud Readiness**) do projeto **Squad 3**. Ele descreve como a solução evolui de um ambiente de desenvolvimento isolado para uma plataforma de dados escalável na **Oracle Cloud Infrastructure (OCI)**.


## 🎯 1. Visão Geral da Estratégia

O objetivo desta arquitetura é demonstrar a portabilidade do pipeline de dados, utilizando serviços gerenciados de nuvem para ganhar escalabilidade, segurança e observabilidade. 

### **Por que a Separação Core vs Ops?**
Para atingir maturidade do projeto, o ecossistema foi dividido em dois repositórios:
1.  **`hackathon-pod-squad3-core`:** Contém a inteligência de processamento. Projetado para ser agnóstico à infraestrutura, foca em lógica de transformação, contratos de dados e qualidade.
2.  **`hackathon-pod-squad3-ops`:** Contém a sustentação técnica. Responsável por "dar vida" à infraestrutura via código (IaC), orquestrar fluxos e gerenciar a movimentação de dados (raw) para a nuvem.

A estratégia de "Cloud Ready" não se limita a mover arquivos; trata-se de garantir que o código seja **portável, resiliente e governado**. 

---

## 🛠️ 2. Fases da Operação em Nuvem

A execução do projeto na OCI é dividida em quatro fases críticas:

### **Fase 1: Provisionamento de Infraestrutura (IaC)**
Utilizando **Terraform**, o ambiente é criado de forma imutável na OCI:
* **Storage:** Bucket `lake-squad3` no Object Storage (S3-Compatible).
* **Compute:** Instância Flex (OCI E4) para hospedagem do Airflow via Docker.
* **IAM & Security:** Configuração de *Dynamic Groups*, permitindo acesso ao storage via identidade nativa.

### **Fase 2: Orquestração e Bootstrap**
O repositório de operações (`-ops`) gerencia o ciclo de vida:
1.  **Task Bootstrap:** O Airflow realiza o `git clone` deste repositório (`-core`) para garantir a execução da versão mais recente.
2.  **Ambiente:** Instalação dinâmica de dependências (DuckDB, Pandera, Boto3).

### **Fase 3: Ingestão "Cloud-Ready" (PoC to Cloud)**
Simulação de ingestão real de um sistema legado:
* O script de ingestão consome dados brutos da camada `RAW` da VPS (MinIO) e replica para o `RAW` do OCI Object Storage.

### **Fase 4: Execução do Pipeline e Qualidade**
Processamento das camadas Bronze, Silver e Gold já em ambiente Oracle, garantindo que o processamento analítico (DuckDB) ocorra com baixa latência e alta performance sobre o Object Storage.

---

## 🛡️ 3. Governança e Observabilidade (Cloud Ready)

A arquitetura transporta os pilares desenvolvidos na Prova de Conceito para a OCI, garantindo que a nuvem opere sob o paradigma de **Policy & Observability as Code**:

- Políticas de qualidade, retenção e particionamento definidas e executadas via código.
- Evidências de observabilidade geradas automaticamente pelo pipeline.
- Logs e relatórios versionados e persistidos no Object Storage.
- Rastreabilidade garantida por execução (`run_id`).
- Comportamento operacional idêntico on-prem e cloud.

---

### 🔗 Ecossistema Squad 3
* **Repositório 1 de 2 (Core):** [hackathon-pod-squad3-core](https://github.com/rafa-trindade/hackathon-pod-squad3-core) — _Engine de processamento, contratos de dados e arquitetura medalhão._
* **Repositório 2 de 2 (Ops):** [hackathon-pod-squad3-ops](https://github.com/rafa-trindade/hackathon-pod-squad3-ops) — _Infraestrutura (IaC), Orquestração e Ingestão de Dados nativa em OCI._