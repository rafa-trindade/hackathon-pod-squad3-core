# ⚠️ Riscos, Dependências e Estimativa de Custos

Esta seção apresenta a análise de riscos técnicos, as dependências críticas da arquitetura e a viabilidade financeira do projeto, utilizando as boas práticas do PMBOK aplicadas ao cenário de Prova de Conceito (PoC).

---

### 1️⃣ Matriz de Riscos Operacionais e Técnicos

**Escala adotada:**
- **Probabilidade (P):** Baixa (1) | Média (2) | Alta (3)  
- **Impacto (I):** Baixo (1) | Médio (2) | Alto (3)  
- **Nível de Risco:** P × I  

| ID | Risco | Fase Impactada | P | I | Nível | Estratégia de Mitigação |
|:---|:---|:---|:---|:---|:---|:---|
| **R1** | Esgotamento de armazenamento na VPS | Operação | 3 | 3 | **9 (Crítico)** | Implementação da Política de Retenção Ativa e limpeza de `run_id` obsoletas. |
| **R2** | Dados inconsistentes ou ausentes na origem | Qualidade | 3 | 2 | **6 (Alto)** | Validações automatizadas com **Pandera** e monitoramento estatístico via **Profiling**. |
| **R3** | Concorrência de recursos (CPU/RAM) na VPS | Processamento | 2 | 3 | **6 (Alto)** | Limites de memória configurados no **DuckDB** e escalonamento de tarefas via **Airflow**. |
| **R4** | Instabilidade ou indisponibilidade da fonte | Integração | 2 | 3 | **6 (Alto)** | Versionamento dos datasets (imutabilidade) para garantir a reprocessabilidade. |
| **R5** | Corrupção de arquivos em escrita interrompida | Persistência | 1 | 3 | **3 (Médio)** | Estratégia de escrita atômica e isolamento por `run_id`. |
| **R6** | Perda de metadados de experimentos (MLflow) | Data Science | 1 | 2 | **2 (Baixo)** | Backup periódico do volume Docker onde residem os artefatos do MLflow. |
| **R7** | Dependência excessiva de ferramentas ou mudanças de escopo | Arquitetura | 1 | 2 | **2 (Baixo)** | Uso de padrões abertos (S3/Parquet), stack desacoplada e versionamento via Git. |

---

### 2️⃣ Justificativa de Mitigação

A estratégia central de mitigação baseia-se no tripé: **Imutabilidade**, **Idempotência** e **Observabilidade**.

1. **Imutabilidade:** O uso de `run_id` garante que dados antigos nunca sejam corrompidos por processos novos que falharam.
2. **Idempotência:** A arquitetura permite re-executar qualquer tarefa no Airflow sem causar duplicidade, essencial para lidar com instabilidades de fonte.
3. **Observabilidade:** O monitoramento via Profiling e logs do Airflow permite agir proativamente antes que o risco de esgotamento de recursos (R1 e R3) interrompa a operação.

---

### 3️⃣ Estimativa de Custos (Fase PoC)

O projeto foca em **Custo Zero de Licenciamento**, utilizando exclusivamente ferramentas *Open Source* e infraestrutura otimizada.

#### 💰 Custos de Infraestrutura
| Recurso | Tipo | Custo Mensal Estimado |
|:---|:---|:---|
| VPS (Ambiente Docker) | Cloud/Host | R$ 80 - R$ 150 |
| **Total Infraestrutura** | | **~ R$ 100 / mês** |

#### 👨‍💻 Custos de Recursos Humanos
| Papel | Alocação | Horas Estimadas | Custo Estimado |
|:---|:---|:---|:---|
| Squad de Dados | 100% | xxxxh | R$ xxxxxx |

#### 🧰 Custos de Software e Ferramentas
| Ferramenta | Licença | Custo |
|:---|:---|:---|
| DuckDB, PostgreSQL, Airflow, dbt | Open Source | R$ 0 |
| MinIO, MLflow, Streamlit | Open Source | R$ 0 |
| **Total Ferramentas** | | **R$ 0** |

---

### 4️⃣ Justificativa Técnica de Eficiência

A escolha do **DuckDB como motor vetorial in-process** é o principal fator de mitigação de custos e riscos de performance. Ele permite processar volumes de dados de nível Spark sem a necessidade de instâncias de alto custo (High-Memory), tornando a PoC viável em uma VPS modesta. 

A arquitetura foi desenhada para ser altamente elástica:
- **Escalabilidade de Software**: Os componentes (MinIO e Postgres) são modulares e podem ser movidos para serviços gerenciados na nuvem sem qualquer refatoração de código.
- **Escalabilidade de Hardware**: Caso o volume de dados da amostra cresça ou novos modelos de ML exijam mais processamento, a estratégia permite **adicionar recursos diretamente à VPS** (Upscale de CPU/RAM), estendendo a vida útil da PoC antes da necessidade de migração para um ambiente de produção complexo.