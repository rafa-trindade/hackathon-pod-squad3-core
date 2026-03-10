# 📚 Book de Variáveis - `abt_model_features`
> Pipeline: Gold ABT - Fusão Performance + Inteligência  
> Última atualização: 02/2026  
> Total de variáveis documentadas: 80

---

## Índice

1. [Chaves e Metadados](#1-chaves-e-metadados)
2. [Bureau de Crédito](#2-bureau-de-crédito)
3. [Dados Cadastrais](#3-dados-cadastrais)
4. [Telco (Comportamento de Uso)](#4-telco-comportamento-de-uso)
5. [Recarga](#5-recarga)
6. [Pagamento](#6-pagamento)
7. [Atraso](#7-atraso)
8. [Glossário de Sufixos e Convenções](#8-glossário-de-sufixos-e-convenções)

---

## 1. Chaves e Metadados

> Identificadores do registro. Não devem ser usados como features em modelos preditivos.

| Variável | Tipo | Descrição | Valores Esperados | Observações |
|---|---|---|---|---|
| `num_cpf` | STRING | CPF do cliente (anonimizado ou hasheado) | Identificador único | Chave primária do cliente |
| `safra` | DATE | Data de referência da observação (ponto de corte) | `YYYY-MM-DD` | Define a janela temporal de todas as agregações |
| `prod` | STRING | Produto/segmento ao qual o cliente pertence | Ex: `CONTROLE`, `PRE` | Usado como chave de join nas tabelas silver |
| `fpd` | INTEGER / FLOAT | First Payment Default - target do modelo (label) | `0` ou `1` | Variável resposta; não usar como feature |
| `flag_instalacao` | INTEGER | Indica se o cliente possui instalação ativa | `0` ou `1` | Proveniente da anchor de labels |
| `ano_mes` | STRING | Partição de armazenamento no lake | `YYYYMM` | Usada para particionamento físico do parquet no S3 |

---

## 2. Bureau de Crédito

> Scores externos provenientes de bureaus de crédito. Fonte: `silver/score_bureau_movel`.

| Variável | Tipo | Descrição | Faixa Esperada | Observações |
|---|---|---|---|---|
| `bur_score_01` | FLOAT | Score primário do bureau de crédito externo | `0` – `1000` | Score bruto; quanto maior, melhor o perfil de crédito |
| `bur_score_02` | FLOAT | Score secundário do bureau (variante do modelo de crédito externo) | `0` – `1000` | Utilizado como base para o cálculo de `cad_bureau_x_estabilidade`; correlacionado com `bur_score_01` |

---

## 3. Dados Cadastrais

> Variáveis derivadas dos dados cadastrais do cliente. Fonte: `silver/dados_cadastrais` e processamento inline no pipeline.

| Variável | Tipo | Descrição | Faixa / Valores | Observações |
|---|---|---|---|---|
| `cad_datadenascimento` | DATE | Data de nascimento do cliente | Data válida | Usada para derivar `idade`; não usar diretamente em modelos |
| `idade` | INTEGER | Idade do cliente em anos completos na data da safra | `18` – `100` | Calculada como `DATE_DIFF('year', cad_datadenascimento, safra)` |
| `tempo_conta_dias` | INTEGER | Tempo de relacionamento do cliente com a empresa, em dias | `0` – `~7300` | Calculado como `DATE_DIFF('day', cad_var_12, safra)`; proxy de maturidade do cliente |
| `cad_cep_3_digitos` | STRING | Primeiros 3 dígitos do CEP do cliente | Ex: `010`, `304` | Proxy geográfico de nível regional; útil para segmentação por microrregião |
| `cad_var_05` | STRING / CATEGORICAL | Variável cadastral 05 (atributo demográfico ou socioeconômico) | Categórico | Definição exata dependente do dicionário de dados da camada silver |
| `cad_var_16` | STRING / CATEGORICAL | Variável cadastral 16 (atributo de perfil do cliente) | Categórico | Definição exata dependente do dicionário de dados da camada silver |
| `cad_bureau_x_estabilidade` | FLOAT | Score de bureau ponderado pela estabilidade de renda declarada | `0` – `~1150` | Calculado como `bur_score_02 × (1 + estabilidade × 0.15)`, onde estabilidade considera flags de funcionário privado e aposentado; combina inteligência externa com cadastral |

---

## 4. Telco (Comportamento de Uso)

> Variáveis de comportamento de uso da linha telefônica. Fonte: `silver/telco`. Os nomes reais das colunas são preservados com prefixo `tel_`.

| Variável | Tipo | Descrição | Faixa / Valores | Observações |
|---|---|---|---|---|
| `tel_var_28` | FLOAT | Variável telco 28 - métrica de comportamento de uso | Contínua | Definição exata no dicionário da camada silver telco |
| `tel_var_30` | FLOAT | Variável telco 30 - métrica de comportamento de uso | Contínua | Definição exata no dicionário da camada silver telco |
| `tel_var_31` | FLOAT | Variável telco 31 - métrica de comportamento de uso | Contínua | Definição exata no dicionário da camada silver telco |
| `tel_var_33` | FLOAT | Variável telco 33 - métrica de comportamento de uso | Contínua | Definição exata no dicionário da camada silver telco |
| `tel_var_34` | FLOAT | Variável telco 34 - métrica de comportamento de uso | Contínua | Definição exata no dicionário da camada silver telco |
| `tel_var_41` | FLOAT | Variável telco 41 - métrica de comportamento de uso | Contínua | Definição exata no dicionário da camada silver telco |
| `tel_var_48` | FLOAT | Variável telco 48 - métrica de comportamento de uso | Contínua | Definição exata no dicionário da camada silver telco |
| `tel_var_50` | FLOAT | Variável telco 50 - métrica de comportamento de uso | Contínua | Definição exata no dicionário da camada silver telco |
| `tel_var_82` | FLOAT | Variável telco 82 - métrica de comportamento de uso | Contínua | Definição exata no dicionário da camada silver telco |

---

## 5. Recarga

> Comportamento transacional de recarga de crédito. Fonte: `silver/recarga`. Todas as agregações consideram apenas recargas com `dat_insercao_credito < safra`.

### 5.1 Volume e Quantidade

| Variável | Tipo | Descrição | Faixa / Valores | Observações |
|---|---|---|---|---|
| `rec_qtd_geral` | INTEGER | Total de recargas realizadas pelo cliente em toda a série histórica | `0` – `N` | Inclui todos os registros anteriores à safra |
| `rec_qtd_l30d` | INTEGER | Total de recargas nos últimos 30 dias antes da safra | `0` – `N` | Janela curta; proxy de atividade recente |
| `rec_qtd_l90d` | INTEGER | Total de recargas nos últimos 90 dias antes da safra | `0` – `N` | Janela padrão de análise comportamental |
| `rec_vlr_total_geral` | FLOAT | Valor total em reais de todas as recargas históricas | `0.0` – `N` | Soma de `val_credito_inserido` |
| `rec_vlr_total_l30d` | FLOAT | Valor total de recargas nos últimos 30 dias | `0.0` – `N` | Comparado com `rec_vlr_total_l90d` para detectar tendência |
| `rec_vlr_total_l60d` | FLOAT | Valor total de recargas nos últimos 60 dias | `0.0` – `N` | Janela intermediária |
| `rec_vlr_total_l90d` | FLOAT | Valor total de recargas nos últimos 90 dias | `0.0` – `N` | Janela padrão de análise comportamental |

### 5.2 Tendência e Atividade

| Variável | Tipo | Descrição | Faixa / Valores | Observações |
|---|---|---|---|---|
| `rec_tendencia_vlr_l30_l90` | FLOAT | Razão entre o valor de recarga nos últimos 30 dias e a média mensal dos últimos 90 dias | `0.0` – `N` | `vlr_l30d / (vlr_l90d / 3)`. Valores > 1 indicam aceleração; < 1 indicam desaceleração |
| `rec_dias_desde_ultima` | INTEGER | Número de dias entre a última recarga e a data da safra | `0` – `~365+` | Alta recência (valor baixo) indica cliente ativo; `NULL` se nunca recarregou |
| `rec_vlr_std_l90d` | FLOAT | Desvio padrão dos valores de recarga nos últimos 90 dias | `0.0` – `N` | Mede irregularidade do valor de recarga no período recente |

### 5.3 SOS (Necessidade Financeira Emergencial)

| Variável | Tipo | Descrição | Faixa / Valores | Observações |
|---|---|---|---|---|
| `rec_qtd_sos_geral` | INTEGER | Quantidade de recargas classificadas como SOS (flag de necessidade financeira) em toda a série histórica | `0` – `N` | `flag_sos = true`; indica episódios de liquidez muito baixa |
| `rec_vlr_sos_l90d` | FLOAT | Valor total de recargas SOS nos últimos 90 dias | `0.0` – `N` | Combinado com `rec_vlr_total_l90d` para calcular `rec_dependencia_sos` |
| `rec_dependencia_sos` | FLOAT | Proporção do valor de recarga oriundo de SOS nos últimos 90 dias | `0.0` – `1.0` | `rec_vlr_sos_l90d / rec_vlr_total_l90d`; quanto maior, maior a fragilidade financeira |

### 5.4 Canal e Perfil de Pagamento

| Variável | Tipo | Descrição | Faixa / Valores | Observações |
|---|---|---|---|---|
| `rec_qtd_canais_digitais_geral` | INTEGER | Quantidade de recargas via canais digitais (PIX, Mercado Pago) em toda a série | `0` – `N` | Canais detectados por `LIKE '%pix%'` ou `LIKE '%mercado pago%'` |
| `rec_share_digital` | FLOAT | Proporção de recargas via canais digitais nos últimos 90 dias | `0.0` – `1.0` | `rec_qtd_canais_digitais_l90d / rec_qtd_l90d`; proxy de maturidade digital do cliente |
| `rec_qtd_plano_controle_geral` | INTEGER | Quantidade de recargas associadas a planos do tipo "controle" | `0` – `N` | Detectado por `LIKE '%controle%'` no campo de plano de tarifação |
| `rec_share_status_ativo` | FLOAT | Proporção de recargas com status de plataforma ativo (`cod_status_plataforma = 'A'`) | `0.0` – `1.0` | Indica consistência de uso ativo da plataforma |
| `rec_qtd_plat_autoc` | INTEGER | Quantidade de recargas na plataforma AUTOC | `0` – `N` | `cod_plataforma_atu = 'AUTOC'` |
| `rec_taxa_cartao_online` | FLOAT | Proporção de recargas via cartão online (`dsc_grupo_cartao_wpp = 'Rec.Online'`) | `0.0` – `1.0` | Indica preferência por pagamento recorrente via cartão |

### 5.5 Bônus

| Variável | Tipo | Descrição | Faixa / Valores | Observações |
|---|---|---|---|---|
| `rec_vlr_bonus_geral` | FLOAT | Valor total de bônus recebidos em toda a série histórica | `0.0` – `N` | Soma de `val_bonus`; proxy de engajamento com promoções |
| `rec_vlr_bonus_l90d` | FLOAT | Valor total de bônus recebidos nos últimos 90 dias | `0.0` – `N` | Janela padrão para `rec_share_bonus` |
| `rec_share_bonus` | FLOAT | Proporção do valor de bônus em relação ao total de recargas nos últimos 90 dias | `0.0` – `1.0` | `rec_vlr_bonus_l90d / rec_vlr_total_l90d`; alto share pode indicar dependência de promoções |

### 5.6 Risco e Volatilidade

| Variável | Tipo | Descrição | Faixa / Valores | Observações |
|---|---|---|---|---|
| `rec_volatilidade_ticket` | FLOAT | Coeficiente de variação do valor de recarga (desvio padrão / média) | `0.0` – `N` | Quanto maior, mais irregular o padrão de recarga do cliente |
| `rec_indice_concentracao` | FLOAT | Razão entre a maior recarga única e o total histórico | `0.0` – `1.0` | Valor próximo a 1 indica dependência de poucos eventos grandes |
| `rec_indice_estresse_financeiro` | FLOAT | Score composto de estresse financeiro baseado em múltiplos sinais de recarga | `0` – `100` | Combina: share de plataformas de risco (30pts), status bloqueio (25pts), proporção SOS (20pts), volatilidade (15pts), concentração (10pts). Escalonado para `[0, 100]` |

---

## 6. Pagamento

> Comportamento de pagamento de faturas. Fonte: `silver/pagamento`. Todas as agregações consideram apenas faturas com `dat_status_fatura < safra`.

### 6.1 Volume e Frequência

| Variável | Tipo | Descrição | Faixa / Valores | Observações |
|---|---|---|---|---|
| `pag_vlr_total_geral` | FLOAT | Valor total de faturas pagas em toda a série histórica | `0.0` – `N` | Soma de `val_pagamento_fatura` |
| `pag_ticket_medio_geral` | FLOAT | Valor médio por fatura paga em toda a série histórica | `0.0` – `N` | `pag_vlr_total_geral / pag_qtd_faturas_geral` |
| `pag_qtd_faturas_geral` | INTEGER | Quantidade total de faturas distintas na série histórica | `0` – `N` | Conta `seq_fatura` distintos |
| `pag_qtd_faturas_l90d` | INTEGER | Quantidade de faturas distintas nos últimos 90 dias | `0` – `N` | Janela padrão de análise |
| `pag_qtd_debito_direto_geral` | INTEGER | Quantidade de pagamentos realizados via débito direto (`DD`, `D`) | `0` – `N` | Proxy de comprometimento e regularidade financeira |
| `pag_dias_desde_ultimo_pagamento` | INTEGER | Número de dias entre o último pagamento de fatura e a safra | `0` – `~365+` | Recência de pagamento; alto valor indica inatividade |
| `pag_taxa_fatura_aberta` | FLOAT | Proporção de faturas com status aberto (`ind_status_fatura = 'O'`) | `0.0` – `1.0` | Faturas abertas = não liquidadas; alto valor é sinal de risco |

### 6.2 Atraso e Inadimplência

| Variável | Tipo | Descrição | Faixa / Valores | Observações |
|---|---|---|---|---|
| `pag_media_dias_atraso_l90d` | FLOAT | Média de dias de atraso (pagamentos após vencimento) nos últimos 90 dias | `0.0` – `~90` | Considera apenas registros onde `dat_atividade_credito > dat_vencimento_credito` |
| `pag_share_faturas_com_juros_geral` | FLOAT | Proporção de faturas que geraram juros/multas em toda a série | `0.0` – `1.0` | `COUNT(val_juros_multas_item > 0) / COUNT(seq_fatura)` |

### 6.3 Risco e Saúde Financeira

| Variável | Tipo | Descrição | Faixa / Valores | Observações |
|---|---|---|---|---|
| `pag_instabilidade_pagamento` | FLOAT | Coeficiente de variação do valor pago por fatura (desvio padrão / média) geral | `0.0` – `N` | Quanto maior, mais irregular o volume de pagamento do cliente |
| `pag_esforco` | FLOAT | Razão entre o valor total em atraso (últimos 90 dias) e o valor pago (últimos 90 dias) | `0.0` – `N` | `atr_vlr_acumulado_l90d / pag_vlr_total_l90d`; alto valor indica que o cliente paga pouco frente ao que está em aberto |
| `pag_taxa_falha` | FLOAT | Proporção de faturas atrasadas sobre o total (atrasadas + pagas) nos últimos 90 dias | `0.0` – `1.0` | `atr_qtd_l90d / (atr_qtd_l90d + pag_qtd_l90d)` |
| `pag_vs_recarga_total` | FLOAT | Razão entre o valor total histórico de recargas e o valor total histórico de pagamentos | `0.0` – `N` | `rec_vlr_total_geral / pag_vlr_total_geral`; desequilíbrio pode indicar comportamento atípico |
| `pag_severidade_juros` | FLOAT | Produto entre a taxa de faturas com juros (últimos 90d) e a média de dias de atraso (últimos 90d) | `0.0` – `N` | Combina frequência e gravidade dos atrasos recentes; quanto maior, mais severo o comportamento |
| `atr_vlr_acumulado_geral` | FLOAT | Valor total acumulado de faturas em atraso em toda a série histórica | `0.0` – `N` | Incluída no bloco de pagamento por ser usada nas features derivadas de pagamento |

---

## 7. Atraso

> Exposição histórica a inadimplência. Fonte: `silver/atraso`. Todas as agregações consideram apenas registros com `dat_referencia < safra`.

### 7.1 Exposição e Volume

| Variável | Tipo | Descrição | Faixa / Valores | Observações |
|---|---|---|---|---|
| `atr_vlr_max_geral` | FLOAT | Maior valor de fatura em atraso registrado em toda a série histórica | `0.0` – `N` | `MAX(val_fat_aberto)`; indica pico de exposição ao risco |
| `atr_qtd_faturas_atrasadas_geral` | INTEGER | Quantidade total de faturas distintas com atraso registrado na série histórica | `0` – `N` | Conta `num_fatura_hash` distintos |
| `atr_dias_desde_ultimo_atraso` | INTEGER | Número de dias entre o último evento de atraso registrado e a safra | `0` – `~365+` | Recência do comportamento de inadimplência; `NULL` se nunca atrasou |

### 7.2 Gravidade (Aging)

| Variável | Tipo | Descrição | Faixa / Valores | Observações |
|---|---|---|---|---|
| `atr_max_aging_divida_geral` | INTEGER | Faixa máxima de aging de dívida atingida em toda a série histórica | `0` – `N` | Baseado em `dw_faixa_aging_divida` (convertido para INTEGER); quanto maior, mais grave o histórico |
| `atr_max_aging_divida_l90d` | INTEGER | Faixa máxima de aging de dívida nos últimos 90 dias | `0` – `N` | Versão recente do aging; útil para capturar deterioração recente |
| `atr_fator_cronico` | FLOAT | Razão entre o aging máximo e o aging médio histórico | `0.0` – `N` | `MAX(aging) / AVG(aging)`; valores muito altos indicam eventos pontuais extremos; valores próximos a 1 indicam cronicidade |

### 7.3 Severidade (PDD, Write-off, Fraude)

| Variável | Tipo | Descrição | Faixa / Valores | Observações |
|---|---|---|---|---|
| `atr_intensidade` | FLOAT | Razão entre o valor acumulado em atraso (últimos 90d) e o ticket médio de pagamento (últimos 90d) | `0.0` – `N` | `atr_vlr_acumulado_l90d / pag_ticket_medio_l90d`; normaliza o atraso pelo porte financeiro do cliente |
| `atr_indice_gravidade_historica` | FLOAT | Score composto de gravidade do histórico de atraso | `0` – `100` | Combina: proporção de write-off (35pts), proporção de PDD (25pts), proporção de fraude (20pts), proporção de aging alto > faixa 2 (20pts). Escalonado para `[0, 100]` |

---

## 8. Glossário de Sufixos e Convenções

### Sufixos de Janela Temporal

| Sufixo | Significado |
|---|---|
| `_geral` | Toda a série histórica disponível anterior à safra |
| `_l30d` | Últimos 30 dias antes da safra |
| `_l60d` | Últimos 60 dias antes da safra |
| `_l90d` | Últimos 90 dias antes da safra |

### Prefixos por Domínio

| Prefixo | Domínio | Fonte Silver |
|---|---|---|
| `bur_` | Bureau de Crédito Externo | `silver/score_bureau_movel` |
| `cad_` | Dados Cadastrais | `silver/dados_cadastrais` |
| `tel_` | Comportamento Telco | `silver/telco` |
| `rec_` | Histórico de Recarga | `silver/recarga` |
| `pag_` | Histórico de Pagamento | `silver/pagamento` |
| `atr_` | Histórico de Atraso | `silver/atraso` |

### Convenções Gerais

| Convenção | Descrição |
|---|---|
| `NULLIF(..., 0)` | Divisões protegidas contra divisão por zero; resultado é `NULL` quando denominador é 0 |
| `COALESCE(..., 0)` | Valores nulos substituídos por 0 em somas e contagens |
| `LEAST(100, GREATEST(0, ...))` | Scores compostos escalonados para o intervalo `[0, 100]` |
| `flag_*` | Variáveis binárias `0/1` derivadas de condições categóricas |
| `share_*` | Proporções no intervalo `[0.0, 1.0]` |
| `taxa_*` | Proporções no intervalo `[0.0, 1.0]` |
| `indice_*` | Scores compostos normalizados ou escalonados |
| `tendencia_*` | Razões temporais comparando janelas distintas |
