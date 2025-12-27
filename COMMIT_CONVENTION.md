## PADRÃO DE COMMITS – PROJETO SQUAD3

Este projeto utiliza um padrão de commits inspirado em Conventional Commits,
adaptado para engenharia de dados, pipelines, qualidade e performance.

Objetivos:
- Histórico de commits legível
- Padronização entre scripts, dags e docs
- Facilidade para CI/CD, changelog e manutenção

---

### ESTRUTURA DO COMMIT

`<tipo>(<escopo>): <mensagem>`

Exemplo:
```bash
git commit -m "perf(config): melhorias de performance e configuração"
```

---

### TIPOS DE COMMIT

| Tipo | Descrição |
| :--- | :--- |
| **docs** | Usado exclusivamente para documentação. Não altera código ou comportamento. |
| **perf** | Melhorias de performance sem alterar regra de negócio. |
| **chore** | Tarefas operacionais, organização, limpeza, padronização. |
| **refactor** | Refatoração de código sem mudança de comportamento. |
| **fix** | Correção de bugs. |
| **feat** | Nova funcionalidade ou novo comportamento. |

---

### REGRAS RÁPIDAS

- **Scripts operacionais** -> `chore`
- **Melhoria interna** -> `refactor` ou `perf`
- **Impacta comportamento** -> `feat` ou `fix`
- **Documentação** -> `docs`
- Sempre usar **verbo no presente**.
- Commits **pequenos e objetivos**.

---

### ESCOPOS E EXEMPLOS POR DIRETÓRIO

#### **DOCUMENTAÇÃO** `docs/`
Escopo: `docs`

```bash
git commit -m "docs(docs): atualização da documentação"
```

```bash
git commit -m "docs(docs): adiciona data dictionary"
```

```bash
git commit -m "docs(docs): atualiza documentação de data quality"
```

#### **CONFIGURAÇÃO** `config/`
Escopo: `config`

```bash
git commit -m "perf(config): melhorias de performance e configuração"
```

```bash
git commit -m "fix(config): corrige conexão com MinIO"
```

```bash
git commit -m "refactor(config): reorganiza data_connections"
```


#### **DAGS** `dags/`
Escopo: `dags`

```bash
git commit -m "feat(dags): adiciona dag de profiling"
```

```bash
git commit -m "fix(dags): corrige dependências entre tasks"
```

```bash
git commit -m "perf(dags): otimiza paralelismo das dags"
```

#### **SCRIPTS** `scripts/`
Escopo: `scripts`

```bash
git commit -m "feat(scripts): adiciona ingestão raw"
```

```bash
git commit -m "perf(scripts): reduz custo de agregações"
```

```bash
git commit -m "fix(scripts): corrige teste de completude"
```

```bash
git commit -m "perf(scripts): otimiza joins"
```

```bash
git commit -m "refactor(scripts): organiza camada gold"
```

---


### O QUE NÃO USAR

- Tipos não padronizados: *att, update, misc*
- Commits genéricos: *update, ajustes, fix bug*
- Misturar documentação e código no mesmo commit