# 🏛️ Data Architecture - Estratégia de Execução Cloud Ready na OCI

> 📌 **Escopo do Documento**
>
> Este documento é **complementar** ao documento principal de arquitetura (`docs/data_architecture/README.md`).
>
> Seu objetivo é descrever **como a arquitetura já definida é executada em ambiente de nuvem**, validando sua prontidão para a **Oracle Cloud Infrastructure (OCI)**.
>
> Nenhuma decisão arquitetural estrutural é redefinida aqui - a OCI é tratada como **plataforma de execução** de um desenho previamente preparado para cloud, podendo utilizar serviços e ferramentas nativas quando apropriado.
>
> Eventuais substituições de serviços e ferramentas são documentadas no repositório de operações (`-ops`), no contexto da arquitetura de execução.

O conteúdo a seguir detalha a **estratégia de execução em nuvem** da arquitetura já definida, evidenciando sua aderência prática à **Oracle Cloud Infrastructure (OCI)**.

## 🎯 1. Visão Geral da Estratégia

Esta estratégia tem como objetivo **descrever como o modelo de dados e processamento, já concebido como cloud ready, é executado em ambiente OCI**, assegurando:

- Portabilidade entre ambientes (on-prem e cloud)
- Separação clara de responsabilidades
- Governança e observabilidade aplicadas via código
- Escalabilidade e eficiência operacional em Object Storage

A OCI é utilizada como **plataforma de execução**, **materializando uma arquitetura concebida desde sua origem como Cloud Ready**.


---

### **Por que a Separação Core vs Ops?**
Para atingir maturidade arquitetural e prontidão para nuvem, o ecossistema foi dividido em dois repositórios com responsabilidades bem definidas:
1. **`hackathon-pod-squad3-core`:** Concentra a engine de processamento e a governança de dados, aplicando as políticas de qualidade, modelagem e padronização da arquitetura medalhão. É projetado para ser agnóstico à infraestrutura, garantindo portabilidade entre ambientes on-prem e cloud.
2. **`hackathon-pod-squad3-ops`:** Responsável pela sustentação operacional da plataforma, incluindo infraestrutura como código (IaC), orquestração dos pipelines e ingestão de dados, viabilizando a execução do Core em ambientes de nuvem.

A estratégia de "Cloud Ready" não se limita a mover arquivos; trata-se de garantir que o código seja **portável, resiliente e governado**. 

---

## 🛠️ 2. Fases da Operação em Nuvem

A execução do projeto na OCI é dividida em quatro fases críticas:

### **Fase 1: Provisionamento de Infraestrutura (IaC)**
Utilizando **Terraform**, o ambiente é criado de forma imutável na OCI:
* **Storage:** Bucket `lake-squad3` no Object Storage (S3-Compatible).
* **Compute:** Instância Flex (OCI E4) para hospedagem do Airflow via Docker.
* **IAM & Security:** Configuração de *Dynamic Groups*, permitindo acesso ao storage via identidade nativa.

---

### **Fase 2: Orquestração e Bootstrap**
O repositório de operações (`-ops`) gerencia o ciclo de vida:
1.  **Task Bootstrap:** O Airflow realiza o `git clone` deste repositório (`-core`) para garantir a execução da versão mais recente.
2.  **Ambiente:** Instalação dinâmica de dependências (DuckDB, Pandera, Boto3).

---

### **Fase 3: Ingestão "Cloud-Ready" (PoC to Cloud)**
Simulação de ingestão real de um sistema legado:
* O script de ingestão consome dados brutos da camada `RAW` da VPS (MinIO) e replica para o `RAW` do OCI Object Storage.

---

### **Fase 4: Execução do Pipeline**
Processamento das camadas Bronze, Silver e Gold já em ambiente Oracle, garantindo que o processamento analítico (DuckDB) ocorra com baixa latência e alta performance sobre o Object Storage.


## 🛡️ 3. Governança e Observabilidade (Cloud Ready)

A arquitetura transporta os pilares desenvolvidos na Prova de Conceito para a OCI, garantindo que a nuvem opere sob o paradigma de **Policy & Observability as Code**:

- Políticas de qualidade, retenção e particionamento definidas e executadas via código.
- Evidências de observabilidade geradas automaticamente pelo pipeline.
- Logs e relatórios versionados e persistidos no Object Storage.
- Rastreabilidade garantida por execução (`run_id`).
- Comportamento operacional idêntico on-prem e cloud.

---

### 🔗 Ecossistema Squad 3
* **Repositório 1 de 2 (Core):** [hackathon-pod-squad3-core](https://github.com/rafa-trindade/hackathon-pod-squad3-core) - _Engine de processamento e Governança de Dados (arquitetura medalhão)._
* **Repositório 2 de 2 (Ops):** [hackathon-pod-squad3-ops](https://github.com/rafa-trindade/hackathon-pod-squad3-ops) - _Infraestrutura (IaC), Orquestração e Ingestão de Dados (Cloud Readiness)._