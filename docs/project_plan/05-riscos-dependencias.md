# ⚠️ Riscos, Dependências e Estimativa de Custos

Esta seção apresenta a análise de riscos integrados, as dependências críticas da arquitetura e a viabilidade financeira do projeto, utilizando as boas práticas do PMBOK aplicadas ao cenário de Prova de Conceito (PoC).


## 1️⃣ Matriz de Riscos Integrada (Engenharia & Ciência de Dados)

**Escala adotada:**
- **Probabilidade (P):** Baixa (1) | Média (2) | Alta (3)  
- **Impacto (I):** Baixo (1) | Médio (2) | Alto (3)  
- **Nível de Risco:** P × I  

| ID | Risco | Categoria | P | I | Nível | Estratégia de Mitigação |
|:---|:---|:---|:---|:---|:---|:---|
| **R1** | Esgotamento de armazenamento na VPS | Infra | 3 | 3 | **9** | Implementação da **Política de Retenção Ativa** e limpeza de `run_id` obsoletas. |
| **R2** | Dados inconsistentes ou ausentes na origem | Qualidade | 3 | 2 | **6** | Validações automatizadas com **Pandera** e monitoramento estatístico via **Profiling**. |
| **R3** | Concorrência de recursos (CPU/RAM) na VPS | Processamento | 2 | 3 | **6** | Limites de memória no **DuckDB** e escalonamento de tarefas via **Airflow**. |
| **R4** | Instabilidade ou indisponibilidade da fonte | Integração | 2 | 3 | **6** | Versionamento dos datasets (imutabilidade) para garantir a reprocessabilidade. |
| **R5** | **Target Ambíguo** | Modelagem | 2 | 3 | **6** | Definição formal registrada + validações por safra. |
| **R6** | **Vazamento Temporal (*Leakage*)** | Modelagem | 2 | 3 | **6** | Split temporal + features anteriores ao target + checklist DS obrigatório. |
| **R7** | **Inconsistência de chaves/temporalidade** | Engenharia | 2 | 3 | **6** | Testes de unicidade/cobertura + contrato explícito da ABT. |
| **R8** | **Books pouco interpretáveis** | Analytics | 2 | 2 | **4** | Cada variável/grupo com definição, janela, regra, interpretação e racional. |
| **R9** | Corrupção de arquivos em escrita interrompida | Persistência | 1 | 3 | **3** | Estratégia de escrita atômica e isolamento por `run_id`. |
| **R10** | Perda de metadados de experimentos (MLflow) | Modelagem | 1 | 2 | **2** | Backup periódico do volume Docker onde residem os artefatos do MLflow. |
| **R11** | Mudanças de escopo ou ferramentas | Arquitetura | 1 | 2 | **2** | Uso de padrões abertos (S3/Parquet), stack desacoplada e versionamento via Git. |


## 2️⃣ Justificativa de Mitigação

A estratégia central de mitigação baseia-se no tripé: **Imutabilidade**, **Rigor Temporal** e **Observabilidade**.

1. **Imutabilidade e Idempotência:** O uso de `run_id` garante que dados antigos nunca sejam corrompidos por processos novos que falharam, permitindo re-execuções sem duplicidade.
2. **Rigor de Modelagem:** O controle rigoroso das janelas de observação e performance (R6) associado a contratos explícitos de ABT (R7) evita o desperdício de esforço em modelos sem validade estatística.
3. **Observabilidade:** O monitoramento via **Profiling** e logs do Airflow permite agir proativamente antes que limites físicos da VPS ou anomalias de dados interrompam a operação.


## 3️⃣ Estimativa de Custos (Fase PoC)

O projeto foca em **Custo Zero de Licenciamento**, utilizando exclusivamente ferramentas *Open Source*.

### 💰 Custos de Infraestrutura e Software
| Recurso | Tipo | Custo Mensal Estimado |
|:---|:---|:---|
| VPS (Ambiente Docker) | Hospedagem | ~ R$ 100,00 |
| DuckDB, PostgreSQL, Airflow, dbt | Licença | R$ 0,00 |
| MinIO, MLflow, Streamlit | Licença | R$ 0,00 |
| **Total Estimado** | | **~ R$ 100,00 / mês** |

---

### 👥 Recursos Humanos (Squad de Dados)
A PoC foi executada por uma Squad multidisciplinar de 10 especialistas, operando em regime de dedicação exclusiva durante as Sprints do projeto.


## 4️⃣ Justificativa Técnica de Eficiência

A escolha do **DuckDB como motor vetorial in-process** é o principal fator de mitigação de custos e riscos de performance. Ele permite processar volumes de dados de nível Spark sem a necessidade de instâncias de alto custo (High-Memory), tornando a PoC viável em uma VPS modesta. 

A arquitetura foi desenhada para ser altamente elástica:
- **Escalabilidade de Software**: Os componentes são modulares e podem ser movidos para nuvens públicas sem refatoração de código.
- **Escalabilidade de Hardware**: Permite **Upscale direto de CPU/RAM na VPS**, estendendo a vida útil da PoC conforme o crescimento da volumetria ou complexidade dos modelos de ML.