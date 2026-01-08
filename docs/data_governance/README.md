# 🏛️ Data Governance - Mapeamento Prático do Projeto

Este diretório concentra as **políticas, diretrizes e decisões estruturais**
relacionadas à governança de dados do projeto.

O objetivo da governança é garantir que os dados sejam:
- Confiáveis
- Reprocessáveis
- Auditáveis
- Sustentáveis em custo
- Alinhados às necessidades do negócio

A governança neste projeto é **pragmática**, orientada a engenharia e operação,
evitando complexidade desnecessária.

---

## 📌 Escopo da Governança

A governança de dados neste projeto cobre:

- Organização lógica do Data Lake
- Estratégias de retenção e descarte
- Separação clara entre camadas técnicas e semânticas
- Regras de reprocessamento
- Definição de contratos de qualidade
- Suporte à observabilidade e auditoria
- Políticas regulatórias externas já são aplicadas na origem (LGPD, etc.)

---

## 📄 Documentos Disponíveis

### 🧹 Política de Retenção de Dados
📄 [`data_governance/politica_retencao.md`](politica_retencao.md)

Define:
- Estratégia de retenção baseada em runs
- Estrutura de pastas por execução (`run_id`)
- Quantidade máxima de histórico por camada
- Momento seguro de limpeza
- Garantias de rollback e reprocessamento

---

### 🧭 Política de Particionamento Temporal no Data Lake
📄 [`data_governance/politica_particionamento_temporal.md`](politica_particionamento_temporal.md)

Define:
- Padrão de uso de colunas temporais na camada Bronze
- Estratégia de particionamento por tipo de dado (snapshot vs evento)
- Convenções técnicas para colunas de tempo
- Relação entre a organização temporal e modelagem nas camadas Silver e Gold

Este documento registra **as decisões arquiteturais adotadas neste projeto**
para a organização temporal dos dados no Data Lake.

---

### ✅ Política de Qualidade de Dados
📄 [`data_governance/politica_qualidade.md`](politica_qualidade.md)


Define:
- Princípios gerais de qualidade de dados do projeto
- Separação entre validações estruturais e semânticas
- Responsabilidade de cada camada (RAW, BRONZE, SILVER, GOLD)
- Regras de unicidade, obrigatoriedade e consistência
- Diretrizes para criação de contratos de dados
- Integração com validações automatizadas (Pandera)

Essa política estabelece **o contrato geral de qualidade**, enquanto
as regras específicas por dataset são documentadas no domínio de
`data_quality/`.

---

## 🔗 Integração com Outros Domínios

A governança atua de forma integrada com:

- **Data Architecture:** define o desenho físico e lógico do lake
- **Data Lineage:** permite rastreabilidade ponta a ponta
- **Data Quality:** garante confiabilidade semântica
- **Data Observability:** monitora saúde e comportamento dos dados

Governança, neste contexto, **não é um silo**, mas uma camada transversal.

---

## 🎯 Princípios Norteadores

- Simplicidade operacional
- Transparência técnica
- Custos controlados
- Reprocessamento como regra, não exceção
- Governança aplicada via código e automação
