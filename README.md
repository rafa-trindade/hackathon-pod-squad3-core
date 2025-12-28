## 🏗️ squad3-data-engineering

Repositório de desenvolvimento e experimentação de engenharia de dados para o hackathon da Pod Academy - Squad 3 

## 👥 Time de Engenharia

- **Frederico da Costa dos Santos**
- **Rafael Araujo Trindade**
- **Ronaldo Theodoro**

## 🛠️ Arquitetura Local

![Arquitetura Local](docs/data_architecture/arquitetura_local.png)

| Componente          | Papel na Arquitetura                              | Responsabilidades Técnicas                                                                                           | Diferencial Estratégico                                                                         |
| :------------------ | :------------------------------------------------ | :------------------------------------------------------------------------------------------------------------------- | :---------------------------------------------------------------------------------------------- |
| **MinIO (S3)**      | **Data Lakehouse Storage**                        | Armazenamento de dados nas camadas Raw, Bronze, Silver e Gold.                                                       | Compatibilidade total com S3 API, permitindo portabilidade para nuvem (AWS) sem alterar código. |
| **DuckDB + Python** | **Engine Analítica (ETL)**                        | Processamento SQL vetorizado, transformações complexas e escrita de arquivos Parquet.                                | Execução in-process eficiente para workloads de médio volume.                                   |
| **Pandera**         | **Validação e Qualidade de Dados (Raw & Silver)** | Validação de schema, tipagem e regras de negócio logo após ingestão (Raw) e após transformações (Silver). | Detecção precoce de problemas de dados e garantia de contratos entre camadas do lakehouse.      |
| **Apache Airflow**  | **Orquestração de Workflows**                     | Gestão de DAGs, controle de dependências, agendamento e alertas de falha.                                            | Centralização do controle operacional e garantia de linhagem (lineage) básica do pipeline.      |
| **Docker**          | **Isolamento de Infra**                           | Empacotamento de serviços, controle de versões de imagem e deploy reprodutível.                                      | Facilidade de escalar e mover a stack inteira entre diferentes provedores de infraestrutura.    |

