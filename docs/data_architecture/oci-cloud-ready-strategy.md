# 🏛️ Data Architecture - Estratégia de Execução Cloud Ready na OCI

Este documento descreve como a arquitetura de dados do projeto, concebida desde sua origem como **cloud ready**, é executada em ambiente de nuvem, utilizando a **Oracle Cloud Infrastructure (OCI)** como plataforma de execução.

## 🎯 1. Visão Geral da Estratégia

A execução da arquitetura em nuvem é orientada por princípios de portabilidade, governança e separação de responsabilidades, permitindo que o mesmo modelo de dados e processamento opere de forma consistente em diferentes ambientes.

Essa abordagem assegura:

- Portabilidade entre ambientes (on-prem e cloud)
- Separação clara de responsabilidades
- Governança e observabilidade aplicadas via código
- Escalabilidade e eficiência operacional em Object Storage

Nesse contexto, a plataforma de execução sustenta a operação da arquitetura de forma consistente e governada.

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

- **Objetivo:** Criar o ambiente de forma imutável na OCI utilizando Terraform.  
- **Storage:** Bucket `lake-squad3` no Object Storage (S3-Compatible).  
- **Compute:** Instância Flex (OCI E4) para hospedagem do Airflow via Docker.  
- **IAM & Security:** Configuração de *Dynamic Groups*, permitindo acesso ao storage via identidade nativa.  

---

### **Fase 2: Orquestração e Bootstrap**

- **Repositório responsável:** `-ops` gerencia o ciclo de vida do pipeline.  
- **Task Bootstrap:** Airflow realiza `git clone` do repositório `-core` para garantir a execução da versão mais recente.  
- **Preparação do ambiente:** Instalação dinâmica de dependências (DuckDB, Pandera, Boto3, etc.)  

---

### **Fase 3: Ingestão Cloud Ready**

- **Objetivo:** Ingestão representativa de dados de origem legada, reproduzindo condições reais de volume, formato e acoplamento.  
- **Execução:** Script consome dados brutos da camada `RAW` da VPS (MinIO) e replica para o `RAW` do OCI Object Storage.  

---

### **Fase 4: Execução do Pipeline**

- **Camadas processadas:** Bronze, Silver e Gold, já em ambiente Oracle.  
- **Transformações:** DuckDB utiliza o acesso S3-compatível para executar SQL vetorizado diretamente sobre o Object Storage.  
- **Benefícios:**  
  - Reduz a necessidade de materialização prévia de dados  
  - Garante execução eficiente com baixa latência


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

> 🔐 O Core define **o que** a arquitetura executa.  
> ⚙️ O Ops define **como e onde** ela é executada.

---

## 📌 Nota de Escopo

> Este documento descreve exclusivamente a **estratégia de execução em nuvem** da arquitetura de dados do projeto, tendo a **Oracle Cloud Infrastructure (OCI)** como plataforma de execução.
>
> Decisões arquiteturais estruturais, modelagem de dados e políticas de governança são definidas no documento principal de arquitetura (`docs/data_architecture/README.md`) e no repositório de operações (`-ops`), quando relacionadas à execução.
>
> A OCI é adotada como ambiente de execução da arquitetura **cloud ready**.  
>
> Variações na adoção de serviços nativos são tratadas como **decisões operacionais**, documentadas e versionadas no repositório (`-ops`), sem alterar o **desenho arquitetural lógico** definido no Core.
