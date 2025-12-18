# MeuAT - REST API Agrícola

O **MeuAT** é uma API geoespacial desenvolvida para a consulta de fazendas via coordenadas. Sua funcionalidade principal é buscar dentro de um banco de dados populado com um GeoJSON que contém polígonos das fazendas do estado de São Paulo.

O projeto conta com um sistema de **População Automática (Seed)**: ao iniciar o ambiente pela primeira vez, a API baixa automaticamente o arquivo GeoJSON do Google Drive e os processa em lotes, inserindo o arquivo inteiro parte a parte no banco de dados.

## 🚀 Tecnologias Utilizadas

* **Python 3.14+**
* **FastAPI** (Framework Web)
* **PostgreSQL 16 + PostGIS 3.4**
* **GeoPandas & Pyogrio**
* **Docker & Docker Compose**
* **SQLAlchemy & GeoAlchemy2**
* **gdown** (Download de arquivos via GDrive)

## 🛠️ Como Rodar o Projeto

### Pré-requisitos
* [Docker](https://www.docker.com/get-started) instalado.
* [Docker Compose](https://docs.docker.com/compose/install/) instalado.

### Passo a Passo

1. **Clone o repositório:**
   ```bash
   git clone [https://github.com/juliozambom/meuat-api.git](https://github.com/juliozambom/meuat-api.git)
   cd meuat-api

   
2. Configure as variáveis de ambiente: Crie um arquivo .env na raiz do projeto com base no exemplo abaixo:
```bash
  POSTGRES_DB=meuat
  POSTGRES_USER=root
  POSTGRES_PASSWORD=meuat_database_pwd
  POSTGRES_PORT=5432
  POSTGRES_HOST=postgres
```

Inicie os containers:
  ```bash
  docker-compose up -d
  ```

Após finalizar a orquestração e inicialicação dos containers, a API já estára disponivel para acesso em http://localhost:8000

📖 Documentação da API (Swagger) 


Com a aplicação rodando, você pode acessar a documentação interativa em:

Swagger UI: http://localhost:8000/docs

Redoc: http://localhost:8000/redoc
