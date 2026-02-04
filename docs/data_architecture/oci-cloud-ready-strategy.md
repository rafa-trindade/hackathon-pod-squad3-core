# 🏛️ Data Architecture - Estratégia de Cloud Readiness (OCI Execution)

Este documento detalha a implementação da arquitetura de dados do Squad 3, concebida sob o paradigma **Cloud Ready**. Aqui, a infraestrutura da **Oracle Cloud Infrastructure (OCI)** atua como a plataforma de execução para o motor de governança e processamento.

---

## 🎯 1. Visão Geral da Estratégia: Core & Ops

Para atingir a máxima maturidade arquitetural, separamos a **Inteligência** da **Sustentação**. Essa separação permite que o motor de dados seja agnóstico, enquanto a operação é otimizada para a nuvem através de pilares de **Cloud Readiness**.

* **🧠 Core (The Engine):** Responsável pela lógica de negócio e transformação. Atua como o **Worker** que executa a arquitetura Medallion e garante a integridade dos dados através de processamento vetorial (DuckDB). É o motor de execução agnóstico à infraestrutura, onde residem os contratos de dados e as regras de qualidade.
* **🏗️ Ops (The Platform):** Responsável pelo **Provisionamento (IaC)** via Terraform, **Orquestração** via Airflow e **Ingestão Híbrida**. É o que viabiliza a execução do Core com segurança e escalabilidade.


> 💡 **Decisão Estratégia de Não-Lock-in:** Optamos pelo deploy via **Docker Compose dentro de OCI Compute**. Isso garante portabilidade total: podemos migrar todo o ecossistema para qualquer nuvem ou ambiente local apenas alterando o arquivo de composição.

---

## 🛠️ 2. Fases do Ciclo de Vida Operacional

A execução na OCI foi estruturada em um pipeline de 4 fases automatizadas:

### **Fase 1: Provisionamento Imutável (Terraform)**
Toda a infraestrutura é erguida via código, garantindo reprodutibilidade:
- **Networking:** VCN isolada com Subnets e Security Lists (Portas 22/8080).
- **Identity (IAM):** RBAC via grupos e políticas nativas.
- **Storage:** Bucket `lake-squad3` configurado com acesso S3-Compatible.

### **Fase 2: Bootstrap & Integração (Cloud-Init + Docker)**
No momento do boot da instância, o script `cloud-init.sh` prepara o ambiente:
- Instalação automatizada da stack Docker.
- Criação dos caminhos de persistência (`/home/opc/app/`).
- O **Core é montado como um volume persistente** dentro dos containers do Airflow, fundindo a lógica de negócio à capacidade de escala da nuvem.

### **Fase 3: Ingestão Híbrida (The Data Bridge)**
A **`dag_ingestion_bridge`** executa o script de migração que conecta o legado à nuvem:
- **Fluxo:** MinIO (VPS) ➔ OCI Object Storage (Raw).
- **Eficiência:** Transferência via streaming (`upload_fileobj`), otimizando memória e I/O da instância.

### **Fase 4: Orquestração do Core Pipeline**
Com os dados na nuvem, o Airflow aciona as DAGs de processamento:
- **`dag_core_bootstrap`:** Sincroniza o repositório Core, instala dependências e injeta variáveis de ambiente (`.env`) dinamicamente.
- **`dag_core_pipeline`:** Dispara o motor DuckDB para transformar as camadas Bronze, Silver e Gold diretamente sobre o Object Storage.

---

## 🛡️ 3. Governança e Observabilidade (Policy as Code)

A arquitetura transporta os pilares de **Cloud Readiness** para a nuvem de forma nativa:

- **Rastreabilidade:** Cada execução gera um `run_id` único, persistido em logs no Object Storage.
- **Lifecycle & Retenção:** Implementação de políticas de retenção automatizadas para as camadas Medallion, garantindo a limpeza de dados temporários e a conformidade com o ciclo de vida definido via código.
- **Identidade:** Uso de *Instance Principals* para que a VM acesse o Storage sem a necessidade de chaves fixas no código (Segurança nativa OCI).
- **Versionamento Dinâmico:** Garantia de que a plataforma de execução (Ops) sempre utiliza a versão estável mais recente do motor de processamento (Core) via Bootstrap automatizado.

---

## 🛠️ Stack & Estratégia de Hardware (Sandbox vs Prod)

Atualmente, a infraestrutura de **Sandbox** está **100% consolidada** via código (IaC). Toda a camada de governança, segurança e rede já foi provisionada com sucesso. O deploy da instância de computação encontra-se aguardando disponibilidade de slots de hardware ARM no pool **Always Free** da Oracle na região `sa-saopaulo-1`.

---

### **Fase 1: Sandbox & Testes (Atual)**
* **Shape:** `VM.Standard.A1.Flex` (ARM Ampere)
* **Recursos:** 4 OCPUs | 24GB RAM
* **Custo:** Always Free Tier (OCI)

---

| Recurso | Status | Descrição |
| :--- | :---: | :--- |
| **Identity (IAM)** | 🟢 | Usuários e grupos do Squad 3 com políticas RBAC ativas. |
| **Networking** | 🟢 | VCN e Subnets configuradas para isolamento de tráfego. |
| **Object Storage** | 🟢 | Bucket `lake-squad3` operacional (Camadas Medallion). |
| **Compute Instance**| 🟡 | Aguardando disponibilidade ARM (A1.Flex) no Free Tier OCI. |
| **Data Bridge** | 🟢 | Script de ingestão Raw (MinIO → OCI) finalizado e testado. |

---

### **Fase 2: Produção Oficial (Patrocinado)**
* **Shape:** `VM.Standard.E4.Flex` (AMD EPYC™)
* **Recursos:** 8 OCPUs | 64GB RAM (Escalável)
* **Objetivo:** Alta performance para o motor DuckDB e paralelismo total de DAGs.

---

## 📂 Organização Cloud Path (VM OCI)

Para garantir a separação de responsabilidades no sistema de arquivos da VM:

- **⚙️ Camada Ops:** `/home/opc/app/hackathon-pod-squad3-ops/` (Docker, DAGs, IaC).
- **🔐 Camada Core:** `/home/opc/app/hackathon-pod-squad3-core/` (DuckDB, Regras de Negócio).
- **⚡ Temp Path:** `/mnt/nvme/duckdb_temp` (Processamento vetorizado de alta performance).

---

> 🔗 **Ecossistema:** [Core Repo](https://github.com/rafa-trindade/hackathon-pod-squad3-core) | [Ops Repo](https://github.com/rafa-trindade/hackathon-pod-squad3-ops)