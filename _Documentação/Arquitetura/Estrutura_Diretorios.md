# Estrutura de diretórios do Radar das Licitações

## Objetivo

O projeto será uma aplicação Python executada inicialmente no Windows. Sua primeira responsabilidade será baixar dados da internet, validar os arquivos, processá-los e carregá-los no Neon.

A estrutura abaixo é intermediária: mantém o projeto simples para começar, mas separa os principais módulos para evitar que todo o código fique concentrado em poucos arquivos.

## Árvore de diretórios

```text
RadarDasLicitacoes/
├── README.md
├── main.py                       # Inicializador para o Visual Studio
├── pyproject.toml
├── .env.example
├── .gitignore
│
├── app/
│   ├── __init__.py
│   ├── main.py                  # Ponto de entrada da aplicação Windows
│   ├── cli.py                   # Comandos auxiliares de desenvolvimento
│   │
│   ├── interface/
│   │   ├── __init__.py
│   │   ├── janela_principal.py  # Janela principal da aplicação
│   │   └── menu_download.py     # Menu e opções de download
│   │
│   ├── config/
│   │   ├── __init__.py
│   │   └── settings.py          # Variáveis de ambiente e configurações
│   │
│   ├── sources/
│   │   ├── __init__.py
│   │   ├── comprasgov.py        # API e arquivos do ComprasGov
│   │   ├── cnpj.py              # Arquivos da Receita Federal
│   │   ├── pncp.py              # Fonte PNCP, quando aplicável
│   │   └── catalog.py            # Cadastro das fontes e layouts
│   │
│   ├── download/
│   │   ├── __init__.py
│   │   ├── downloader.py        # Download, retry e retomada
│   │   ├── manifest.py          # Controle dos arquivos disponíveis
│   │   ├── checksum.py          # Hash e verificação de integridade
│   │   └── storage.py           # Organização dos arquivos locais
│   │
│   ├── processing/
│   │   ├── __init__.py
│   │   ├── readers.py           # Leitura de CSV, ZIP e arquivos texto
│   │   ├── validators.py        # Validação de layout e conteúdo
│   │   ├── cleaners.py          # Limpeza de campos e valores ausentes
│   │   ├── normalizers.py       # Padronização de datas, códigos e valores
│   │   └── pipeline.py          # Orquestração do processamento
│   │
│   ├── database/
│   │   ├── __init__.py
│   │   ├── connection.py        # Conexão com o Neon
│   │   ├── models.py            # Estruturas das tabelas
│   │   ├── repositories.py      # Gravação e consultas
│   │   ├── migrations.py        # Controle das migrações
│   │   └── loaders.py           # Carga em lotes no banco
│   │
│   ├── analysis/
│   │   ├── __init__.py
│   │   ├── prices.py            # Indicadores e estatísticas de preços
│   │   ├── quality.py           # Métricas de qualidade dos dados
│   │   └── features.py          # Preparação para modelos de IA
│   │
│   └── common/
│       ├── __init__.py
│       ├── logger.py            # Logs da aplicação
│       ├── files.py             # Operações comuns com arquivos
│       ├── dates.py             # Tratamento de datas
│       └── errors.py            # Exceções da aplicação
│
├── data/
│   ├── raw/                     # Arquivos originais baixados
│   ├── staging/                 # Dados temporários durante o processamento
│   ├── processed/               # Arquivos prontos para carga ou consulta
│   ├── error/                   # Arquivos rejeitados
│   ├── manifests/               # Manifestos das execuções
│   └── logs/                    # Logs locais
│
├── database/
│   ├── migrations/              # Migrações versionadas do Neon
│   └── scripts/                 # Scripts de manutenção e diagnóstico
│
├── config/
│   ├── sources/                 # Configurações das fontes externas
│   └── schedules/               # Agendamentos do Windows
│
└── _Documentação/
    ├── Analise/
    └── Arquitetura/
```

## Responsabilidade dos principais módulos

| Módulo | Responsabilidade |
|---|---|
| `sources` | Conhecer cada fonte externa, seus endereços, parâmetros e layouts. |
| `download` | Descobrir, baixar, validar, identificar e armazenar os arquivos originais. |
| `processing` | Ler arquivos, validar colunas, limpar dados e executar a transformação. |
| `database` | Conectar ao Neon, executar migrações e carregar os dados em lotes. |
| `analysis` | Produzir indicadores, métricas e atributos para análise de preços. |
| `common` | Reunir funcionalidades compartilhadas por outros módulos. |
| `config` | Armazenar configurações externas ao código. |
| `interface` | Apresentar a janela Windows, menus, telas e mensagens ao usuário. |
| `cli.py` | Disponibilizar comandos auxiliares de desenvolvimento, sem substituir a aplicação Windows. |

## Fluxo da aplicação

```text
Usuário seleciona uma opção no menu Download
    ↓
Interface Windows
    ↓
app/sources
    ↓
app/download
    ↓
data/raw
    ↓
app/processing
    ↓
data/staging / data/processed
    ↓
app/database
    ↓
Neon
    ↓
app/analysis
```

## Menu da aplicação Windows

O fluxo principal de download será iniciado pela aplicação Windows, por meio do menu:

```text
Download
├── Download dados Compras Governamentais
└── Download dados de CNPJ
```

Cada opção deverá abrir a tela correspondente, permitindo posteriormente selecionar URL, competência, pasta de destino e acompanhar o progresso. Nesta primeira versão, o menu é apenas uma casca visual e não executa downloads.

A janela principal deve permanecer fina, funcionando somente como uma barra de menu. As telas de download devem ser abertas como janelas independentes, sem ocupar o espaço da janela principal.

## Comandos auxiliares

```powershell
python -m app.cli discover
python -m app.cli download
python -m app.cli validate
python -m app.cli process
python -m app.cli import
python -m app.cli status
```

Os comandos auxiliares não substituem o menu da aplicação Windows. A execução normal para o usuário deverá ocorrer pela interface gráfica.

## Configuração do Neon

Criar um arquivo `.env` local, sem versioná-lo:

```text
DATABASE_URL=postgresql://usuario:senha@host/neondb?sslmode=require
DATA_DIR=./data
LOG_LEVEL=INFO
```

O arquivo `.env.example` deve conter somente os nomes das variáveis, sem credenciais reais.

## Dependências iniciais

```text
httpx              # Requisições HTTP
python-dotenv      # Variáveis de ambiente
SQLAlchemy         # Acesso ao PostgreSQL/Neon
psycopg            # Driver PostgreSQL
pandas             # Processamento de dados
tenacity            # Retry de downloads
```

## Regras importantes


- Não versionar arquivos das pastas `data/raw`, `data/staging` e `data/processed`.
- Preservar os arquivos originais antes de processá-los.
- Registrar URL, data, tamanho, competência e hash dos arquivos baixados.
- Usar texto para CNPJ, CPF, códigos e identificadores com zeros à esquerda.
- Usar `Decimal` para valores monetários.
- Processar os arquivos em lotes para evitar consumo excessivo de memória.
- Separar os adaptadores das fontes das regras gerais de download.
- Começar com uma fonte e uma competência de teste antes de realizar cargas maiores.

## Evolução futura

A estrutura permite adicionar uma API, interface web ou serviço Windows sem alterar o núcleo de download e processamento. A análise de preços com IA poderá ser ampliada dentro de `app/analysis` ou, somente quando necessário, transformada em um serviço separado.
