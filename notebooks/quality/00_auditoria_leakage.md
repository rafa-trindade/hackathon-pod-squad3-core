# Auditoria de Vazamento (Target Leakage)

Data: Fevereiro/2026  
Artefato: T1.2 – Auditoria de Vazamento e Validação AS-OF  
Responsável: Squad DS

---

## 1. Objetivo

Este documento tem como objetivo validar que a base analítica utilizada para o desenvolvimento do modelo de comportamento (Behavior Score) não apresenta **vazamento de informação do target (FPD)**, garantindo aderência ao princípio **AS-OF**, fundamental em projetos de Credit Scoring.

De acordo com a literatura clássica de Credit Scoring, uma variável é considerada válida apenas se puder ser observada **no momento da decisão**, isto é, antes do início do evento de risco associado ao target. Variáveis que utilizam, direta ou indiretamente, informações posteriores ao evento invalidam a capacidade preditiva real do modelo e geram performance artificial.

Esta auditoria é um pré-requisito para:
- Estudo de Público-Alvo
- Construção do Modelo Baseline de Behavior
- Simulações de política (swap-in)
- Governança e validação do modelo perante a banca

---

## 2. Base Analisada

- Tabela: `gold/abt_base_cmv`
- Origem: Camada Gold do Data Lake
- Grão: `num_cpf + safra + prod`
- Target: `FPD` (First Payment Default)
- Safras analisadas: 2024-10 a 2025-03
- Volume total: 1.321.168 registros
- Produtos: 3
- Taxa média de FPD: 23,79%

O grão adotado reflete corretamente o contexto de negócio, no qual um mesmo CPF pode estar associado a múltiplos produtos em uma mesma safra, com riscos distintos.

---

## 3. Metodologia de Auditoria

A auditoria foi conduzida seguindo práticas consagradas em Credit Scoring e Model Risk Management, estruturada em três frentes complementares.

### 3.1 Validação Temporal (Princípio AS-OF)

Foi verificado se alguma variável de data ou timestamp apresentava valores posteriores ou coincidentes ao início da safra, o que indicaria uso de informação futura.

Procedimento:
- Identificação de todas as colunas do tipo data ou timestamp.
- Cálculo do percentual de registros em que `feature_date >= safra`.

Resultado:
- Nenhuma variável operacional apresentou ocorrência relevante de datas posteriores à safra.
- A única exceção foi um campo cadastral esparso (`cad_var_13`), com baixa cobertura e sem impacto estrutural no modelo.
- Variáveis como datas de recarga, pagamento e atraso foram corretamente limitadas a eventos anteriores à safra.

Conclusão:
- Não foi identificado vazamento temporal estrutural.
- O princípio AS-OF é respeitado na construção da ABT.

---

### 3.2 Auditoria Semântica por Domínio de Variáveis

As variáveis foram analisadas por domínio funcional, considerando seu significado de negócio e momento de disponibilidade:

- `bur_*`: Bureau de crédito
- `cad_*`: Dados cadastrais
- `tel_*`: Variáveis operacionais de telecom
- `rec_*`: Histórico de recargas
- `pag_*`: Histórico de pagamentos
- `atr_*`: Histórico de atrasos

Para cada domínio, avaliou-se se as variáveis representam:
- Estado histórico do cliente anterior à decisão
- Informação estática ou cadastral
- Métrica agregada de comportamento passado

Resultado:
- Não foram identificadas variáveis semanticamente dependentes do evento de FPD.
- Variáveis operacionais de telecom apresentaram baixo poder individual e comportamento consistente com histórico pré-evento.
- Variáveis comportamentais (recarga, pagamento, atraso) refletem comportamento passado e são compatíveis com modelos de behavior.

Conclusão:
- Não foram identificadas variáveis semanticamente incompatíveis com o momento da decisão.
- Todas as variáveis avaliadas são elegíveis do ponto de vista conceitual.

---

### 3.3 Detector Estatístico de Vazamento (AUC Univariada)

Como boa prática adicional, foi aplicado um detector estatístico baseado na **AUC univariada**, amplamente utilizado em projetos de Credit Scoring para identificar proxies diretos do target.

#### Racional
Na literatura de Credit Scoring, espera-se que variáveis individuais apresentem poder discriminatório limitado. Modelos robustos derivam performance da combinação de múltiplos sinais fracos e complementares. Variáveis isoladas com poder excessivo frequentemente indicam:
- Vazamento de informação futura
- Proxy direto do target
- Variável construída com informação pós-evento

#### Procedimento
- Cálculo da AUC ROC individual para cada variável numérica em relação ao target FPD.
- Exclusão de chaves, identificadores e colunas técnicas.
- Análise dos maiores valores de AUC univariada.

#### Critérios de referência (heurística de mercado)
- AUC ~0.50: ausência de sinal
- AUC entre 0.52 e 0.65: sinal esperado
- AUC > 0.70: sinal forte, requer revisão
- AUC > 0.80: alta suspeita de vazamento

#### Resultados
- Nenhuma variável apresentou AUC univariada superior a 0.60.
- As variáveis com maior poder individual situam-se entre 0.52 e 0.58.
- Não foi identificada variável com poder discriminatório excessivo.

Conclusão:
- Não há evidência estatística de vazamento ou proxy direto do target.
- O comportamento observado é consistente com bases saudáveis de Credit Scoring.

---

## 4. Consolidação dos Achados

### 4.1 Features Aprovadas (Whitelist)

- Todas as variáveis da ABT foram consideradas elegíveis para uso no modelo baseline.
- As variáveis respeitam o princípio AS-OF, não apresentam vazamento temporal ou semântico e possuem poder individual compatível com boas práticas de scoring.

### 4.2 Features Bloqueadas (Blacklist)

- Nenhuma variável foi bloqueada nesta etapa.
- Não foram identificados riscos que justifiquem exclusão preventiva.

---

## 5. Implicações para o Modelo e para o Negócio

- A ausência de vazamento garante que a performance futura do modelo seja consistente com a performance observada em validação.
- O modelo baseline deverá extrair poder preditivo da combinação de sinais comportamentais, e não de variáveis artificiais.
- Reduz-se significativamente o risco de overfitting e de degradação em produção.
- A base está adequada para análises de público, construção de score e simulações de política.

---

## 6. Próximos Passos

Com a auditoria de vazamento concluída, o projeto avança para:
1. Estudo de Público-Alvo e segmentação comportamental.
2. Construção do Modelo Baseline de Behavior com split temporal por safra.
3. Definição e simulação de políticas de decisão (swap-in).
4. Consolidação dos Books de Variáveis por domínio.

Esta auditoria encerra formalmente a etapa de validação de integridade da base analítica para modelagem.

---
