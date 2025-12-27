## 🏗️ squad3-data-engineering

Repositório de desenvolvimento e experimentação de engenharia de dados para o hackathon da Pod Academy - Squad 3 

## 👥 Time de Engenharia

- **Frederico da Costa dos Santos**
- **Rafael Araujo Trindade**
- **Ronaldo Theodoro**

## 🛠️ Arquitetura Local

| Componente | Papel na Arquitetura |
|-----------|----------------------|
| **Apache Airflow** | Orquestração e agendamento dos pipelines |
| **Python + DuckDB (ETL)** | Transformações analíticas in-process via SQL e Python |
| **MinIO (S3)** | Armazenamento de dados nas camadas Raw, Bronze, Silver e Gold |
| **Docker** | Isolamento e deploy dos serviços na VPS |

![Arquitetura Local](docs/data_architecture/arquitetura_local.png)