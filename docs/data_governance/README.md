# 🏛️ Data Governance - Mapeamento Prático do Projeto

Este diretório concentra as **políticas, diretrizes e decisões estruturais** relacionadas à governança de dados da Squad 3. Nosso foco é garantir que o Data Lake seja uma fonte confiável, escalável e de baixo custo operacional.

A governança neste projeto é **pragmática**, orientada a engenharia e aplicada diretamente via código (*Policy as Code*).


## 📌 Escopo e Princípios

A governança atua de forma transversal para garantir:
- **Reprocessabilidade:** Capacidade de reconstruir qualquer estado anterior.
- **Eficiência:** Uso de formatos (Parquet) e partições (ano_mes) que reduzem custo de Cloud.
- **Transparência:** Documentação viva refletindo exatamente o que está implementado nos scripts.



## 📄 Documentos Disponíveis

🏛️ Governança de Dados - Squad 3

Este diretório centraliza as definições políticas e arquiteturais que regem a organização, o ciclo de vida e a qualidade dos dados no Data Lake.



## 📄 Políticas e Documentos Centrais

### 🧹 Política de Retenção de Dados
📄 [`politica_retencao.md`](politica_retencao.md)
**Foco:** Gestão do ciclo de vida e custos.
- Define a estratégia de **Imutabilidade por Execução** (`run_id`).
- Estabelece o protocolo de limpeza *post-write* para evitar perda de dados em falhas.
- **Implementação:** Reforçada pelo utilitário `scripts/transformations/utils/lake_retention.py`.

---

### 🧭 Política de Particionamento
📄 [`politica_particionamento.md`](politica_particionamento.md)
**Foco:** Performance e padronização de consumo.
- Padroniza a partição única `ano_mes=YYYYMM` (BIGINT) para todos os datasets.
- Habilita o *Partition Pruning* no DuckDB/S3 para acelerar consultas em até 90%.
- **Auditoria:** Auditado pelo script `inspect_partition.py`, que garante a conformidade física do particionamento Hive.

---

### ✅ Política de Qualidade de Dados
📄 [`politica_qualidade.md`](politica_qualidade.md)
**Foco:** Contratos de dados e integridade.
- Define as validações estruturais (Raw) e semânticas (Silver).
- Estabelece regras de unicidade e obrigatoriedade de campos.
- **Ferramental:** Integração  com `Pandera` e validações nativas SQL.



## ⚙️ Operação e Troubleshooting

Graças às políticas acima, o projeto herda capacidades operacionais críticas:

1. **Rollback Imediato:** Como mantemos as `MAX_RUNS` anteriores, voltar uma versão de um dataset é apenas uma alteração de ponteiro ou leitura da run anterior.
2. **Isolamento de Erros:** Uma falha na ingestão da `run_id` atual não corrompe os dados já existentes.
3. **Auditoria Simplificada:** Cada partição e cada run carregam consigo o metadado de tempo (`ingestion_ts`), permitindo rastrear a origem de qualquer inconsistência. 
4. **Verificação de Integridade:** O uso da auditoria de partições permite validar, em segundos, se uma carga massiva de dados foi distribuída corretamente nas pastas temporais, evitando "data drift" físico.



## 🏛️ Evidências de Governança (Compliance & Audit)

Para fins de auditoria e conformidade, as evidências de que as políticas acima foram aplicadas estão disponíveis em:

- **Logs de Integridade:** [`reports/observability/partitions/`](../../reports/observability/partitions/) - Comprova o cumprimento da Política de Particionamento.
- **Relatórios de Qualidade:** [`reports/observability/quality/`](../../reports/observability/quality/) - Comprova a aplicação dos Contratos de Dados (Pandera/dbt).


## 🔗 Integração com Outros Domínios

A governança atua como uma camada transversal, garantindo que as definições estratégicas se tornem realidade operacional através da integração com:

- **Data Architecture:** define o desenho físico e lógico do lake
- **Data Lineage:** permite rastreabilidade ponta a ponta
- **Data Quality:** garante confiabilidade semântica
- **Data Observability:** monitora saúde e comportamento dos dados

Governança, neste contexto, **não é um silo**, mas uma camada transversal.

