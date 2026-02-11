# 🚀 Guia de Reprodução e Validação - Squad 3

Este guia descreve os passos para configurar o ambiente e reproduzir as métricas de performance apresentadas pela Squad 3, utilizando o modelo serializado e os dados processados na nuvem (OCI/MinIO).

## 🛠️ 1. Configuração do Ambiente (Sandbox)

Recomendamos a criação de um ambiente virtual para isolar as dependências e garantir a compatibilidade das versões (ex: DuckDB 1.4.3 e Scikit-Learn 1.6.1).

### Passo 1: Criar e Ativar o Ambiente Virtual
No terminal, dentro da pasta do projeto:

**Windows:**
```bash
python -m venv venv
.\venv\Scripts\activate
```
**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

---

### Passo 2: Instalar Dependências

Com o ambiente ativo, instale todas as bibliotecas necessárias:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

### Passo 3: Verificar a Estrutura de Pastas
Certifique-se de que a raiz do projeto contém os seguintes itens:
- `.env` e `requirements.txt`
- `models/` (contendo os arquivos .pkl)
- `notebooks/` (com as subpastas eda, modeling e quality)

> ⚠️ **Atenção:** O arquivo `.env` deve permanecer na raiz do projeto. Ele contém as chaves de acesso necessárias para que o DuckDB consuma os dados diretamente do nosso Data Lake.


## 🧪 2. Fluxo de Validação e Artefatos

O projeto utiliza **DuckDB** para processamento em memória e conecta-se via protocolo S3 ao nosso Data Lake externo através das credenciais contidas no arquivo `.env`.

### 2.1 Estudo do Público-Alvo (EDA)
**Arquivo:** `notebooks/eda/01_estudo_publico_alvo_cmv.ipynb`
- Diagnóstico de risco e análise exploratória que fundamentou a estratégia de dados.

---

### 2.2 Reprodução do Modelo e Score
**Arquivo:** `notebooks/modeling/02_modelo_baseline_behavior.ipynb`
- Notebook principal para carregar o artefato `.pkl`, realizar a escoragem das bases no S3 e gerar as métricas de **Gini e KS** (Treino, Teste e OOT).

---

### 2.3 Auditoria de Integridade (Anti-Leakage)
**Arquivo:** `notebooks/quality/00_auditoria_leakage.ipynb`
- Validação técnica que garante o respeito ao **Point-in-Time Join** (sem dados do futuro).

---

### 2.4 Artefatos do Modelo (Outputs)
**Pasta:** `models/`
- `behavior_baseline_woe_v1.pkl`
- `behavior_baseline_simple_v1.pkl`


## 📞 3. Suporte e Considerações Finais

Caso a banca encontre qualquer dificuldade na conectividade com o endpoint do MinIO ou na execução das células, o time da **Squad 3** está à disposição para suporte imediato.

### Checklist de Erros Comuns:
1. **Conexão S3:** Verifique se a sua rede permite conexões externas via protocolo HTTP (porta 9000).
2. **Kernels Jupyter:** Certifique-se de selecionar o kernel do ambiente virtual (`venv`) ao abrir os notebooks no VS Code ou Jupyter Lab.
3. **Versão do Python:** O uso de `python >= 3.10` é recomendado para garantir a compatibilidade total com os binários do DuckDB.
