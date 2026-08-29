# E-Commerce Data Lakehouse & Executive Analytics

![Python](https://img.shields.io/badge/Python-3.14+-3776ab?style=flat-square&logo=python&logoColor=white)
![Poetry](https://img.shields.io/badge/Poetry-60A5FA?style=flat-square&logo=poetry&logoColor=white)
![Azure Blob Storage](https://img.shields.io/badge/Azure%20Storage-0089D6?style=flat-square&logo=microsoft-azure&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-336791?style=flat-square&logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat-square&logo=docker&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)
![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen?style=flat-square)

---

## 📋 Contextualização

No cenário competitivo do e-commerce, painéis estáticos e relatórios descritivos não acompanham o ritmo das decisões operacionais. Este projeto implementa uma **arquitetura end-to-end** de pipeline ETL contínuo acoplado a um dashboard analítico que transforma dados brutos em **inteligência de negócio preditiva e prescritiva**.

### Problemas de Negócio Resolvidos

**🚨 Ruptura de Estoque (Out-of-Stock)**
- O motor de análise cruza volume de vendas em tempo real com níveis de inventário, gerando alertas automáticos quando os produtos caem abaixo de 15 unidades. Isto reduz perda de vendas e melhora fill rate operacional.

**📉 Erosão de Margem Bruta**
- Identifica automaticamente produtos com alto faturamento operando em margens insustentáveis (< 15%), permitindo intervenção imediata na precificação ou negociação com fornecedores antes do prejuízo.

**⚠️ Anomalias de Churn (Cancelamentos/Devoluções)**
- Monitora a taxa de cancelamento e sinaliza quando ultrapassa o threshold tolerável (acima de 15%), indicando problemas potenciais no fulfilment ou na qualidade do produto.

### Valor da Engenharia

O sistema foi construído com **separação rigorosa de responsabilidades** (Clean Architecture), que garante resiliência mesmo sob falhas. Se as camadas transacionais (Bronze/Silver) falharem, o painel isola o erro e continua entregando os KPIs consolidados da camada Gold por meio de um sistema de proteção automática. Ou seja, o painel nunca fica fora do ar e você continua acompanhando todos os seus números sem nenhuma interrupção**.

---

## 🏗️ Arquitetura da Solução

```mermaid
graph TD
    subgraph Ingestion["🔄 1. Ingestão & Orquestração"]
        S1["Motor de Ingestão<br/>(main.py - Python)"]
        Gen["Generators<br/>(Produtos, Clientes, Pedidos)"]
    end

    subgraph Cloud["☁️ 2. Data Lakehouse - Azure"]
        Bronze["Bronze Container<br/>(Raw Data - JSON)"]
        Silver["Silver Container<br/>(Validated Data)"]
        Gold["Gold Container<br/>(Aggregated - Parquet)"]
    end

    subgraph RDBMS["🗄️ 3. Serving Layer"]
        PG["PostgreSQL 15<br/>(OLTP Analítico)"]
    end

    subgraph Analytics["📊 4. Consumo & Analytics"]
        ST["Streamlit Dashboard<br/>(Dark Mode + Plotly)"]
    end

    subgraph Monitoring["🎯 5. Business Intelligence"]
        Insights["Business Insights Engine<br/>(Alerts & Anomalies)"]
    end

    Gen -->|Gera Massa de Dados| S1
    S1 -->|Extração & Validação| Bronze
    Bronze -->|Transformação Silver| Silver
    Silver -->|Agregação Gold| Gold
    Gold -->|Persistência Analítica| PG
    PG -->|Consultas Otimizadas via SQLAlchemy| ST
    ST -->|Dados Filtrados| Insights
    Insights -->|KPIs & Alertas| ST

    classDef source fill:#38bdf8,stroke:#0f172a,stroke-width:2px,color:#ffffff,font-weight:bold
    classDef cloud fill:#0284c7,stroke:#bae6fd,stroke-width:2px,color:#ffffff,font-weight:bold
    classDef db fill:#10b981,stroke:#d1fae5,stroke-width:2px,color:#0b0f19,font-weight:bold
    classDef app fill:#f59e0b,stroke:#fef3c7,stroke-width:2px,color:#0b0f19,font-weight:bold
    classDef monitor fill:#ec4899,stroke:#fbcfe8,stroke-width:2px,color:#ffffff,font-weight:bold

    class S1,Gen source
    class Bronze,Silver,Gold cloud
    class PG db
    class ST app
    class Insights monitor
```

**Fluxo de Dados:**
1. **Ingestão**: Generators criam massa de dados mockada (produtos, clientes, pedidos).
2. **Bronze (Raw)**: Dados extraídos em formato JSON bruto, sem transformação.
3. **Silver (Clean)**: Validação, limpeza e enriquecimento usando Pydantic e regras de negócio.
4. **Gold (Aggregated)**: Camada de agregação — sumários financeiros, margens, lucros (formato Parquet otimizado).
5. **Serving (PostgreSQL)**: Persistência em RDBMS para consultas analíticas de baixa latência.
6. **Dashboard (Streamlit)**: Interface interativa com filtros, gráficos Plotly e insights automáticos.
7. **Insights**: Motor de anomalias que dispara alertas baseado em regras preditivas.

---

## ⚙️ Tecnologias Envolvidadas

### 🔧 Orquestração & Processamento
- **Python 3.14+** — Linguagem principal; tipagem forte com type hints.
- **Poetry** — Gerenciamento determinístico de dependências (sem dependency hell).
- **Pydantic v2** — Validação de dados com schemas fortemente tipados.
- **Pandas** — Processamento e transformação de dados tabulares.

### ☁️ Data Lake (Azure)
- **Azure Blob Storage (ADLS Gen2)** — Arquitetura Medallion: Bronze → Silver → Gold.
- **JSON & Parquet** — Formatos otimizados por camada (JSON para ingestão, Parquet para analytics).

### 🗄️ Banco de Dados (RDBMS)
- **PostgreSQL 15 (Alpine)** — Instância otimizada em container para ambiente local/staging.
- **SQLAlchemy 2.0** — ORM declarativo com suporte a async queries.

### 📊 Visualização & Frontend
- **Streamlit** — Framework interativo para dashboards sem necessidade de JavaScript/CSS complexo.
- **Plotly** — Gráficos interativos, responsive e publication-ready.
- **CSS Customizado** — Tema Dark Mode integrado.

### 🐳 Ambiente & DevOps
- **Docker & Docker Compose** — Orquestração local de múltiplos serviços (PostgreSQL + Streamlit + Pipeline).
- **Alpine Linux** — Imagens otimizadas em tamanho.

---

## 📂 Estrutura do Repositório

```
projeto-dados/
├── src/
│   ├── config.py                     # Configuração centralizada (env vars, DB_URL, Azure credentials)
│   │
│   ├── pipeline/                     # Orquestração e transição entre camadas
│   │   └── (regras de transição Bronze → Silver → Gold)
│   │
│   ├── transformers/                 # Lógica de transformação e regras de negócio
│   │   ├── silver_transformer.py    # Limpeza e validação
│   │   └── gold_transformer.py      # Agregação financeira (receita, lucro, margem)
│   │
│   ├── loaders/                      # Conectores de escrita
│   │   ├── azure_loader.py          # Upload para Azure Blob Storage
│   │   └── db_loader.py             # Gravação em PostgreSQL via SQLAlchemy
│   │
│   ├── readers/                      # Conectores de leitura agnósticos a formato
│   │   ├── base_reader.py           # Interface base (contrato)
│   │   ├── json_reader.py           # Parser JSON com Pydantic validation
│   │   └── parquet_reader.py        # Leitor de Parquet (se necessário)
│   │
│   ├── generators/                   # Geração de massa de dados mockada
│   │   ├── customer_generator.py    # Faker: clientes com email, cidade, estado
│   │   ├── product_generator.py     # Faker: produtos com SKU, preço, categoria
│   │   ├── order_generator.py       # Faker: pedidos com status, desconto, shipping
│   │   └── data_quality_injector.py # Injetor de anomalias (teste de resiliência)
│   │
│   ├── models/                       # Schemas Pydantic (tipagem e validação)
│   │   └── models.py                # Customer, Product, Order (com field_validator)
│   │
│   ├── dashboard/                    # Camada de apresentação (Streamlit)
│   │   ├── app.py                   # Entrypoint do dashboard
│   │   ├── components.py            # Componentes reutilizáveis (KPIs, cards)
│   │   ├── insights.py              # Motor de business insights (alertas)
│   │   └── styles.css               # Customização visual (Dark Mode)
│   │
│   └── logger.py                     # Configuração de logging centralizada
│
├── tests/                            # Suíte de testes unitários (pytest)
│   ├── test_transformers.py         # Testes de transformação e agregação
│   ├── test_readers.py              # Testes de validação de leitura
│   ├── test_loaders.py              # Testes de persistência
│   └── test_models.py               # Testes de validação de modelos
│
├── data/                             # Diretório local para fallback/cache
│   ├── bronze/                      # Cópia local de dados brutos (backup)
│   ├── silver/                      # Staging local (opcional)
│   └── gold/                        # Resultados locais de processamento
│
├── main.py                           # Orquestrador principal (Entrypoint do ETL)
├── compose.yaml                      # Definição de infraestrutura (Docker Compose)
├── Dockerfile                        # Imagem Docker da aplicação
├── .dockerignore                     # Exclusões para build Docker
├── .gitignore                        # Exclusões Git
├── .env.example                      # Template de variáveis de ambiente
├── pyproject.toml                    # Manifesto Poetry (dependências, Python version)
├── poetry.lock                       # Lock file (versões exatas reproduzíveis)
└── README.md                         # Este arquivo
```

**Princípios de Design:**
- **Clean Architecture**: Separação entre domínio (models), casos de uso (transformers), infraestrutura (loaders/readers).
- **Dependency Injection**: Loaders e readers recebem configuração via parâmetros.
- **Type Safety**: Uso agressivo de type hints e Pydantic para validação em tempo de execução.
- **DRY (Don't Repeat Yourself)**: Componentes reutilizáveis no dashboard, logging centralizado. (Um Shout Out para Luciano Vasconcelos por me ensinar esse)

---

## 🚀 Guia de Execução (How to Run)

Este guia leva você do zero ao full stack em poucos minutos. Cada passo foi testado em ambiente Linux/macOS/Windows (WSL2).

### **Passo 1: Pré-requisitos**

Certifique-se de ter instalado:

- **Git** — Controle de versão
- **Docker & Docker Compose** — Orquestração de containers
  - [Instalar Docker](https://docs.docker.com/get-docker/)
  - [Instalar Docker Compose](https://docs.docker.com/compose/install/) (geralmente bundled)
- **Python 3.14+** — Linguagem principal
  - [Instalar Python](https://www.python.org/downloads/)
- **Poetry** — Gerenciador de dependências
  ```bash
  curl -sSL https://install.python-poetry.org | python3 -
  ```
  Após instalar, adicione Poetry ao PATH se necessário:
  ```bash
  export PATH="$HOME/.local/bin:$PATH"
  ```
- **Conta no Azure** (opcional, para uso em produção)
  - Uma Storage Account com containers: `bronze`, `silver`, `gold`
  - Connection String (obtida no portal Azure)

**Verificar Instalação:**
```bash
git --version
docker --version
docker compose --version
python3 --version
poetry --version
```

---

### **Passo 2: Clonagem e Instalação de Dependências**

Clone o repositório e configure o ambiente isolado:

```bash
# Clonar repositório
git clone https://github.com/Xurisco/projeto-dados.git
cd projeto-dados

# Instalar dependências via Poetry (cria virtual env automaticamente)
poetry install

# Ativar o ambiente virtual (opcional, Poetry gerencia automaticamente)
poetry shell
```

**O que Poetry faz:**
- Lê `pyproject.toml` e `poetry.lock`.
- Cria um virtual environment isolado.
- Instala todas as dependências com versões exatas (reproduzibilidade garantida).
- Dependências incluem: Pydantic, Pandas, SQLAlchemy, Faker, Azure SDK, Streamlit, Plotly.

---

### **Passo 3: Configuração de Variáveis de Ambiente**

Crie um arquivo `.env` na raiz do projeto com as credenciais:

```env
# .env

# ===== PostgreSQL =====
POSTGRES_USER=user
POSTGRES_PASSWORD=senha_super_segura_aqui
POSTGRES_DB=ecommerce

# ===== Database URL (CRÍTICO para Docker Compose) =====
# Use 'db' como hostname quando rodando via Docker
# Use 'localhost' quando executar main.py do terminal da máquina host
DATABASE_URL=postgresql://user:senha_super_segura_aqui@db:5432/ecommerce

# ===== Azure Blob Storage (Optional - para produção) =====
# Se não tiver conta Azure, deixe em branco (sistema roda em fallback local)
AZURE_STORAGE_CONNECTION_STRING=DefaultEndpointsProtocol=https;AccountName=YOUR_ACCOUNT;AccountKey=YOUR_KEY;EndpointSuffix=core.windows.net
```

**⚠️ Nota Crítica sobre DATABASE_URL:**
- **No Docker Compose**: Use `@db:5432` (hostname do serviço interno).
- **Rodando main.py localmente**: Mude temporariamente para `@localhost:5432`.

Exemplo com comentários:
```env
# Variáveis para o container do dashboard
DATABASE_URL=postgresql://user:senha@db:5432/ecommerce

# Se for rodar main.py do terminal (fora do Docker):
# DATABASE_URL=postgresql://user:senha@localhost:5432/ecommerce
```

---

### **Passo 4: Subindo a Infraestrutura (PostgreSQL + Streamlit)**

Inicie os containers do banco de dados e do dashboard:

```bash
# Build e start dos serviços em background
docker compose up --build -d

# Verificar status dos containers
docker compose ps

# Ver logs em tempo real (opcional)
docker compose logs -f dashboard
docker compose logs -f db
```

**O que acontece:**
1. Container `db` (PostgreSQL 15 Alpine) é iniciado e expõe porta 5432.
2. Container `dashboard` (Streamlit) é construído e rodado, expondo porta 8501.
3. Ambos compartilham a mesma rede Docker interna (hostname `db` é resolvível).

**Verificar conectividade:**
```bash
# Conectar ao PostgreSQL do container
docker compose exec db psql -U user -d ecommerce -c "SELECT 1;"
```

Se tudo OK, você verá: `?column? \n ----------- \n 1`

---

### **Passo 5: Executando o Pipeline ETL (Primeira Carga)**

O `main.py` orquestra a extração, validação e agregação. **Ele roda fora do Docker** (do seu terminal), para que você veja os logs em tempo real.

**IMPORTANTE**: Ajuste temporariamente o `DATABASE_URL` para apontar para `localhost`:

```bash
# Abra um novo terminal e execute:
export DATABASE_URL="postgresql://user:senha_super_segura_aqui@localhost:5432/ecommerce"

# Ou, em um comando só:
DATABASE_URL="postgresql://user:senha_super_segura_aqui@localhost:5432/ecommerce" poetry run python main.py
```

**O que o pipeline faz (a cada 15 segundos):**
1. Gera 20 produtos mockados (1ª vez apenas).
2. Gera 50 clientes mockados (1ª vez apenas).
3. Gera 10 pedidos novos a cada ciclo.
4. Valida pedidos usando Pydantic.
5. Transforma em DataFrame Pandas.
6. Agrega por `product_id` (receita, lucro, margem).
7. Envia para Azure Blob Storage (Bronze → Silver → Gold) se configurado.
8. Grava tabela `sales_summary` no PostgreSQL (sobrescreve).
9. Aguarda 15 segundos e repete.

**Logs esperados:**
```
INFO: Iniciando orquestrador de ingestão contínua com Azure Data Lake.
INFO: --- Novo ciclo de ingestão de dados ---
INFO: Arquivo 'orders.json' enviado com sucesso para o container 'bronze' (Azure).
INFO: Tabela 'sales_summary' atualizada no PostgreSQL com sucesso.
INFO: Ciclo concluído. Aguardando 15 segundos...
```

**Deixe rodando por 1-2 minutos** para popular o banco. Você verá vários ciclos. Depois:

```bash
# Parar o pipeline (Ctrl+C)
# Mas DEIXE os containers rodando:
docker compose ps  # Ainda deve mostrar db e dashboard online
```

---

### **Passo 6: Acessando o Dashboard**

Com os dados carregados, acesse a interface no navegador:

```
👉 http://localhost:8501
```

**O que você verá:**
--------COLOCAR AS PRINTS DO DASHBOARD----------


---

## 🛠️ Troubleshooting (Solução de Problemas Comuns)

### **Erro 1: `psycopg2.OperationalError: connection to server at "localhost", port 5432 failed`**

**Sintoma**: Ao executar `poetry run python main.py`, recebe erro de conexão recusada.

**Causa**: O PostgreSQL não está rodando em `localhost:5432` ou o container não foi iniciado.

**Solução**:
```bash
# 1. Verificar se containers estão rodando
docker compose ps

# Se db não aparecer ou status ≠ Up:
docker compose up -d db

# 2. Aguarde alguns segundos para o PostgreSQL inicializar
sleep 5

# 3. Teste a conexão
docker compose exec db psql -U user -d ecommerce -c "SELECT 1;"

# 4. Se a porta 5432 já está em uso localmente (conflito com PostgreSQL instalado):
# a. Parar PostgreSQL local: sudo systemctl stop postgresql
# b. Ou usar porta diferente no docker-compose.yaml: "5433:5432"

# 5. Tente rodar o pipeline novamente
DATABASE_URL="postgresql://user:senha@localhost:5432/ecommerce" poetry run python main.py
```

---

### **Erro 2: `⏳ Aguardando o primeiro ciclo do pipeline para carregar os dados...`**

**Sintoma**: Dashboard abre mas mostra aviso amarelo e nenhum dado aparece.

**Causa**: O `main.py` ainda não completou o primeiro ciclo, ou a URL do banco no `.env` está incorreta.

**Solução**:
```bash
# 1. Verificar se main.py está rodando
ps aux | grep "python main.py"

# 2. Se não vir o processo, inicie novamente
DATABASE_URL="postgresql://user:senha@localhost:5432/ecommerce" poetry run python main.py &

# 3. Verificar se dados foram gravados no PostgreSQL
docker compose exec db psql -U user -d ecommerce -c "SELECT COUNT(*) FROM sales_summary;"

# 4. Se tabela não existe, main.py não rodou. Volte ao Passo 5 e deixe rodar 1-2 min

# 5. No Streamlit, clique no botão "🔄 Atualizar Painel" para forçar recarga
```

---

### **Erro 3: Database URL Mismatch (Dados No PostgreSQL Mas Dashboard Vazio)**

**Sintoma**: Você rodou `main.py` e vê logs de gravação, mas dashboard continua vazio.

**Causa**: O `.env` contém `@db:5432` (correto para Docker), mas o `main.py` rodou com `@localhost:5432`. Houve dois bancos diferentes.

**Solução**:
```bash
# Verificar qual DATABASE_URL está ativo no container dashboard
docker compose exec dashboard env | grep DATABASE_URL

# Se estiver errado, edite .env e reinicie
# Correto para Docker: @db:5432
# Correto para main.py fora do Docker: @localhost:5432

# Reiniciar dashboard
docker compose restart dashboard

# Aguarde 5-10 segundos e recarregue o navegador
```

---

### **Erro 4: Azure Connection Error**

**Sintoma**: Logs mostram `AZURE_STORAGE_CONNECTION_STRING não configurada` ou `Connection refused` ao Azure.

**Causa**: Variável de ambiente não setada ou credencial inválida.

**Solução**:
```bash
# 1. Sistema roda sem Azure (fallback local). Dados ficam em data/bronze, data/silver, data/gold
# 2. Se quer usar Azure:
#    - Obtenha a connection string no portal Azure (Storage Account > Access Keys)
#    - Adicione ao .env: AZURE_STORAGE_CONNECTION_STRING="DefaultEndpointsProtocol=..."
#    - Reinicie: docker compose restart projeto-dados

# 3. Testar conectividade
poetry run python -c "from azure.storage.blob import BlobServiceClient; print('OK')"
```

---

### **Erro 5: `ModuleNotFoundError: No module named 'src'`**

**Sintoma**: Ao rodar `python main.py`, Python não encontra o módulo `src`.

**Causa**: Você executou direto sem usar Poetry, ou o PYTHONPATH não está configurado.

**Solução**:
```bash
# Sempre use Poetry para rodar scripts
poetry run python main.py

# Ou entre no shell Poetry
poetry shell
python main.py
```

---

### **Erro 6: Docker Image Build Fails**

**Sintoma**: `docker compose up --build` falha com erro de build.

**Causa**: Geralmente, `poetry.lock` corrompido ou dependência incompatível com Python 3.14.

**Solução**:
```bash
# 1. Forçar rebuild sem cache
docker compose down
docker system prune -a  # CUIDADO: remove todas as imagens não usadas

# 2. Regenerar lock file localmente
poetry lock --no-update

# 3. Rebuild Docker
docker compose up --build -d
```

---

## 🧪 Testes e Qualidade de Dados

A confiabilidade dos dados é crítica. O projeto inclui uma suíte de testes robusta:

### **Executar Testes**

```bash
# Rodar todos os testes
poetry run pytest tests/ -v

# Rodar com cobertura
poetry run pytest tests/ --cov=src --cov-report=html

# Rodar teste específico
poetry run pytest tests/test_transformers.py::test_create_sales_summary -v
```

### **O que é Testado**

1. **Validação de Modelos** (`test_models.py`):
   - Pydantic validates Customer, Product, Order.
   - Rejeita dados inválidos (email malformado, preço negativo, etc.).

2. **Transformação & Agregação** (`test_transformers.py`):
   - Cálculos de receita, lucro, margem.
   - Tratamento de pedidos vazios ou incompletos.

3. **Leitura & Serialização** (`test_readers.py`):
   - JSONReader valida e deserializa corretamente.
   - Falha gracefully com arquivos corrompidos.

4. **Persistência** (`test_loaders.py`):
   - db_loader insere dados no PostgreSQL.
   - azure_loader envia blobs com retry logic.

### **Data Quality Injector**

Módulo `src/generators/data_quality_injector.py` simula anomalias em ambiente de desenvolvimento:
- Valores nulos não esperados.
- SKUs corrompidos.
- Preços negativos.
- Quantidades zeradas.

O pipeline Silver/Gold isola automaticamente essas anomalias e as sanitiza antes da camada analítica, garantindo que o dashboard exiba apenas dados confiáveis.

---

## 📈 Próximos Passos (Roadmap)

Melhorias arquiteturais mapeadas:

- [ ] **Modern Data Stack Orchestration**: Migração da orquestração nativa (`main.py`) para **Apache Airflow** ou **Prefect**, aprimorando observabilidade, retentativas (retries) e SLA tracking.

- [ ] **Transformação via DBT**: Refatoração das regras da camada Gold (agregadores SQL) para modelos **DBT**, incluindo DAGs de linhagem, data tests e documentação automatizada.

- [ ] **Observabilidade & Monitoring**: Integração com **Prometheus** + **Grafana** para rastreamento de métricas do pipeline (latência, taxa de erro, volume processado).

---

## 👨‍💻 Autor

**Arthur Klein**

Estudante de Ciência e Engenharia de Dados e Inteligência Artificial 

- 📧 Email: [arthurklein777.ak@gmail.com](mailto:arthurklein777.ak@gmail.com)
- 💼 LinkedIn: [linkedin.com/in/arthurklein](https://linkedin.com/in/arthurklein)
- 🐙 GitHub: [@Xurisco](https://github.com/Xurisco)
