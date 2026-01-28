# ✅ Política de Qualidade de Dados (Data Quality)

**Objetivo:** Estabelecer os critérios de aceitação, padrões de integridade e o framework de validação para garantir que os dados consumidos pela Squad 3 sejam confiáveis, íntegros e sigam os contratos definidos.

## 1. Framework de Qualidade

A qualidade de dados é aplicada de forma integrada ao pipeline de transformação, utilizando o conceito de **Data Contracts** (Contratos de Dados):

* **Validação de Schema (Pandera):** Atua como o "portão de entrada" na camada inicial. Garante que a estrutura física (nome e quantidade de colunas) esteja correta antes de qualquer processamento, evitando falhas em cascata nas camadas subsequentes.

## 2. Dimensões da Qualidade

| Dimensão | O que validamos | Ferramenta |
| :--- | :--- | :--- |
| **Integridade de Schema** | Nome e quantidade de colunas obrigatórias na origem. | Pandera |
| **Unicidade** | Garantia de registros únicos por chave natural (Grão). | DuckDB (SQL Logic) |
| **Conformidade** | Valores dentro de intervalos lógicos e tipagem forte. | DuckDB (Transform) |
| **Completude** | Monitoramento de nulos e volumetria de carga. | Profiling |
| **Saúde de Safra** | Representatividade volumétrica por período (regra 10%-90%). | Gold Pipeline Audit |
| **Overlap (Riqueza)** | Match de chaves entre camadas para garantir base "ML-Ready". | Gold Pipeline Audit |

## 3. Implementação Prática (Critérios de Garantia)

A qualidade é aplicada através de travas técnicas e auditorias programáticas que garantem a integridade do dado em cada estágio.

### 3.1 Camada Raw (Garantia de Conformidade Estrutural)
O Pandera executa a inspeção física do arquivo antes da ingestão.
* **Garantia de Schema:** Validação mandatória de nomes, tipos básicos e quantidade de colunas.
* **Protocolo Fail-Fast:** A pipeline é abortada imediatamente se a estrutura divergir do contrato, impedindo a poluição do Lake com dados malformados.

---

### 3.2 Transição para Bronze (Garantia de Integridade Técnica)
O DuckDB assegura a estabilidade técnica dos tipos de dados.
* **Tipagem Forte (Casting):** Garantia de que campos de data, hora e valores numéricos foram convertidos com sucesso via `strptime` e casts explícitos.
* **Garantia de Particionamento:** Validação de que todo registro possui uma chave `ano_mes` válida e um timestamp de ingestão (`ingestion_ts`) para auditoria cronológica.

---

### 3.3 Transição para Silver (Garantia de Saneamento e Unicidade)
Nesta fase, o foco é a garantia de que o dado está limpo e é único.
* **Saneamento de Identificadores:** Limpeza ativa de strings vazias, valores 'nan' ou hashes de erro em colunas de grão (CPF, Contrato, Fatura).
* **Garantia de Unicidade (Deduplicação):** Aplicação de lógica de janela para assegurar que cada chave de negócio seja única no dataset, mantendo apenas a versão mais atualizada.
* **Auditoria de Pareamento (Enriquecimento):** Geração de log de qualidade para medir a taxa de encontro de chaves em tabelas de dimensão (descrições), garantindo que o dado não seja "órfão".

---

### 3.4 Transição para Gold (Garantia de Utilidade Estatística)
Auditoria final voltada para a viabilidade do uso do dado em modelos de ML.
* **Auditoria de Overlap:** Garantia de que existe massa crítica de dados (match de chaves) entre as fontes de alvo e as características (features).
* **Health Check de Safra:** Monitoramento da densidade volumétrica por período, garantindo que as safras processadas possuem entre 10% e 90% da volumetria esperada.
* **Garantia de Grão Final:** Verificação de integridade pós-joins para assegurar que não houve multiplicação indevida de registros na agregação final.



## 4. Gestão de Falhas

Quando um teste de qualidade falha, o protocolo de governança define:
1.  **Isolamento:** A `run_id` problemática é identificada e o dado não é promovido para a camada seguinte.
2.  **Trilha de Auditoria:** O erro é registrado nos logs de qualidade para diagnóstico imediato.
3.  **Ação Corretiva:** O motor de Retenção permite o rollback para a última execução estável.

## 5. Evidências e Relatórios

* **Relatórios Pandera (Schema):** [`reports/observability/quality/pandera/`](../../reports/observability/quality/pandera/)
* **Auditoria de Pipeline:** [`reports/observability/quality/pipeline/`](../../reports/observability/quality/pipeline/)

Para auditar uma execução específica, a estrutura no S3 deve ser consultada:
`s3://lake/observability/reports/run_id=YYYYMMDD/`

---

**Observações Finais:** A qualidade não é uma etapa final, mas um processo contínuo integrado ao pipeline de transformação (*Data Quality as Code*).