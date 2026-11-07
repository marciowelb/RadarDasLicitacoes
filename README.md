# Radar das Licitações

O **Radar das Licitações** é um projeto de dados abertos para coletar, organizar e analisar preços praticados em compras públicas e processos licitatórios no Brasil. A primeira etapa do projeto consiste na **baixa reproduzível de dados da internet**, preservando os arquivos originais, sua origem e a data da coleta. Em etapas posteriores, os dados serão normalizados em um banco de dados e utilizados em análises estatísticas e modelos de inteligência artificial.

## Aplicação Windows

A aplicação Windows é criada em Python com `tkinter`. A janela principal funciona como uma barra fina de menus; as funcionalidades são abertas em janelas independentes.

### Menu disponível

- **Download > Download dados Compras Governamentais**
- **Download > Download dados de CNPJ** — reservado para uma versão futura.

A opção de Compras Governamentais abre a rotina de download, com log, barra de progresso, cancelamento e gravação dos CSVs em `data/raw/comprasgov`. O download de CNPJ ainda não está implementado.

O período inicial é configurado por `ANO_INICIAL_DADOS = 2025`. Nesta etapa não há processamento dos CSVs nem gravação no Neon.

Para executar a aplicação na raiz do projeto:

```powershell
python main.py
```

No Visual Studio, defina o arquivo `main.py` da raiz como arquivo de inicialização. O arquivo `app/main.py` continua sendo o ponto de entrada interno para execução como módulo.

> O projeto está em fase de levantamento e preparação da ingestão. As estruturas de banco, chaves e regras de negócio ainda devem ser validadas com o perfilamento completo dos arquivos.

## Objetivos

- Baixar dados públicos de compras, itens, propostas, resultados e preços de referência.
- Manter rastreabilidade: fonte, URL, competência, data de download, tamanho, hash e versão do arquivo.
- Integrar dados de compras públicas com catálogos de materiais/serviços e cadastro de fornecedores.
- Criar uma base histórica para comparar preços, identificar outliers e apoiar estimativas de preços.
- Disponibilizar consultas e indicadores para apoiar decisões em licitações, sem substituir a análise técnica ou jurídica.

## Fontes de dados

| Fonte | Uso no projeto |
|---|---|
| [Repositório ComprasGov](https://repositorio.dados.gov.br/seges/comprasgov/) | Downloads históricos em CSV/ZIP de PNCP, propostas, pesquisa de preços, ARP, catálogos e legado. |
| [Portal de dados abertos do Compras.gov.br](https://www.gov.br/compras/pt-br/cidadao/portal-de-dados-abertos/explorador-de-dados) | Catálogo institucional e ponto de entrada para os dados. |
| [Swagger da API Compras.gov.br](https://dadosabertos.compras.gov.br/swagger-ui/index.html) | Consulta de catálogos, contratações, fornecedores, preços e outros módulos. |
| [Contrato OpenAPI](https://dadosabertos.compras.gov.br/v3/api-docs) | Endpoints, parâmetros e esquemas para construir o coletor. |
| [Cadastro Nacional da Pessoa Jurídica](https://dados.gov.br/dados/conjuntos-dados/cadastro-nacional-da-pessoa-juridica---cnpj) | Dados cadastrais e vínculos de fornecedores. |
| [Arquivos públicos da Receita Federal](https://arquivos.receitafederal.gov.br/index.php/s/YggdBLfdninEJX9) | Arquivos mensais do CNPJ para carga cadastral. |

## Documentação do levantamento

- [Estrutura de diretórios e arquitetura](_Documentação/Arquitetura/Estrutura_Diretorios.md)
- [Dados do ComprasGov e layouts](_Documentação/Analise/Documentacao_Dados_ComprasGov.md)
- [Endpoints da API ComprasGov](_Documentação/Analise/Documentacao_API_ComprasGov_Endpoints.md)
- [Arquivos CNPJ, download e modelo de banco](_Documentação/Analise/Documentacao_CNPJ_Download_Layout_BancoDados.md)

## Fluxo inicial de dados

```mermaid
flowchart LR
    F[Fontes oficiais] --> D[Download e descoberta]
    D --> V[Validação de ZIP, CSV, tamanho e hash]
    V --> O[Armazenamento dos originais]
    O --> S[Staging: dados brutos]
    S --> N[Normalização e vínculos]
    N --> B[(Banco analítico)]
    B --> A[Indicadores e modelos de IA]
```

### Princípios da ingestão

1. Descobrir arquivos e registrar a resposta da fonte antes do download.
2. Baixar em partes quando necessário, com retry, checkpoint e promoção atômica.
3. Validar tamanho, integridade do ZIP/CSV e hash antes de carregar.
4. Preservar identificadores, CPF/CNPJ, códigos e zeros à esquerda como texto.
5. Usar `Decimal` para valores monetários e quantidades; não usar `float` em cálculos financeiros.
6. Usar parser CSV com suporte a aspas, delimitador em texto e quebras de linha.
7. Separar dados originais, staging e dados normalizados para permitir reprocessamento.
8. Não impor chaves ou regras de negócio antes do perfilamento completo dos dados.

## Proposta de banco de dados

Uma arquitetura inicial recomendada é:

| Camada | Conteúdo | Tecnologia sugerida |
|---|---|---|
| `raw` | ZIPs/CSV originais, metadados, hashes e logs de download | Object storage, filesystem ou S3 compatível |
| `staging` | Linhas brutas com os tipos ainda próximos da origem | Neon/PostgreSQL ou Parquet/DuckDB |
| `core` | Compras, itens, fornecedores, propostas, resultados, catálogos e snapshots | Neon/PostgreSQL |
| `analytics` | Histórico de preços, agregações, métricas e atributos para modelos | Neon/PostgreSQL, DuckDB ou warehouse |
| `ml` | Features, previsões, versões de modelos e métricas | Neon/PostgreSQL + MLflow |

Entidades iniciais:

- `snapshot` e `arquivo_origem`, para versionamento e rastreabilidade;
- `compra`, `item_compra`, `proposta` e `resultado_item`;
- `fornecedor`, `empresa`, `estabelecimento` e seus vínculos cadastrais;
- `catalogo_material`, `catalogo_servico` e unidades de medida;
- `pesquisa_preco`, `ata_registro_preco` e `contrato`;
- tabelas de domínio e correspondências geográficas.

### Referências para implementação do banco

- [Neon](https://neon.tech/docs) — banco PostgreSQL gerenciado utilizado inicialmente pelo projeto.
- [Console do projeto no Neon](https://console.neon.tech/app/projects/late-dawn-95658203/branches/br-noisy-scene-b66k5mdz/tables) — administração das tabelas e branches.
- [PostgreSQL](https://www.postgresql.org/docs/) — referência da engine relacional utilizada pelo Neon.
- [PostGIS](https://postgis.net/documentation/) — consultas geográficas, se necessárias.
- [DuckDB](https://duckdb.org/docs/) — exploração local de CSV/Parquet e cargas analíticas.
- [Apache Parquet](https://parquet.apache.org/docs/) — formato colunar para dados históricos.
- [MinIO](https://min.io/docs/minio/linux/index.html) — armazenamento de objetos compatível com S3 para ambiente próprio.
- [dbt](https://docs.getdbt.com/) — transformação, documentação e testes das tabelas analíticas.
- [Alembic](https://alembic.sqlalchemy.org/) — versionamento de migrações quando a ingestão for implementada em Python.

### Uso inicial do Neon

O Neon será utilizado inicialmente como a base central do projeto. A conexão deve ser configurada por variável de ambiente, nunca gravada no código ou no README:

```text
DATABASE_URL=postgresql://usuario:senha@host/neondb?sslmode=require
```

Recomendações:

- manter a `DATABASE_URL` em segredo e utilizar o recurso de conexão fornecido pelo Neon;
- habilitar `sslmode=require` nas conexões da aplicação;
- separar ambientes por branches do Neon, como desenvolvimento, homologação e produção;
- criar migrações versionadas para tabelas e índices;
- utilizar pool de conexões para a aplicação e cargas controladas para grandes importações;
- registrar no banco a origem, competência, URL, hash e status de cada arquivo baixado;
- avaliar o uso de [Neon Serverless Driver](https://neon.tech/docs/serverless/serverless-driver) para aplicações serverless.

## Análise de preços com IA

A IA deve ser aplicada sobre dados normalizados, com proveniência e qualidade conhecidas. O objetivo não é gerar um preço sem explicação, mas produzir uma **faixa de referência auditável**, acompanhada das observações usadas, do período, da região, da unidade de medida e da confiança da estimativa.

### Casos de uso previstos

- Comparar preço estimado, homologado e praticado.
- Detectar outliers, duplicidades, alterações de unidade e possíveis erros de cadastro.
- Normalizar descrições de itens e agrupar itens semanticamente semelhantes.
- Estimar uma faixa de preço por item, quantidade, região, período, órgão e características técnicas.
- Recuperar casos históricos semelhantes para explicar a estimativa.
- Monitorar alteração de preços e deterioração da qualidade dos modelos.

### Abordagem recomendada

1. **Qualidade:** validar tipos, unidades, datas, cancelamentos, quantidades e duplicidades.
2. **Normalização:** relacionar itens aos catálogos CATMAT/CATSER e preservar a descrição original.
3. **Features:** criar atributos temporais, geográficos, do órgão, fornecedor, quantidade e categoria.
4. **Baseline:** começar com mediana e intervalos por item/categoria/região/período.
5. **Modelos supervisionados:** comparar modelos como regressão, Random Forest, Gradient Boosting e XGBoost.
6. **Texto e similaridade:** usar embeddings para encontrar descrições semelhantes, sempre com filtros de unidade e categoria.
7. **Validação temporal:** treinar em períodos anteriores e testar em períodos posteriores, evitando vazamento de informação.
8. **Explicabilidade:** armazenar amostra de referência, atributos relevantes, versão do modelo e métricas.

### Referências para IA e MLOps

- [scikit-learn](https://scikit-learn.org/stable/) — preparação, validação e modelos clássicos.
- [XGBoost](https://xgboost.readthedocs.io/) — modelos de gradient boosting para dados tabulares.
- [Sentence Transformers](https://www.sbert.net/) — embeddings e busca semântica de descrições.
- [pgvector](https://github.com/pgvector/pgvector) — armazenamento e busca de vetores no PostgreSQL.
- [MLflow](https://mlflow.org/docs/latest/) — registro de modelos, experimentos e métricas.
- [Evidently](https://docs.evidentlyai.com/) — monitoramento de qualidade, drift e desempenho.
- [OpenAI API](https://platform.openai.com/docs/) — opção para extração/normalização assistida de texto; não deve substituir regras determinísticas e validações financeiras.

## Cuidados, limites e governança

- Os dados publicados podem conter revisões, atrasos, campos ausentes e layouts diferentes entre competências.
- A presença de um registro cadastral não comprova que o fornecedor forneceu determinado item.
- Preço estimado, preço homologado e preço efetivamente praticado são medidas diferentes.
- Valores anômalos não devem ser removidos automaticamente: devem ser marcados e investigados.
- Dados pessoais devem ser minimizados, protegidos e utilizados apenas quando necessários ao objetivo do projeto.
- Toda previsão deve informar data de referência, fonte, população comparável, versão do modelo e limitações.
- A decisão final deve permanecer sob responsabilidade da equipe competente da contratação.

## Próximas etapas

1. Definir o coletor e o manifesto de arquivos por fonte.
2. Implementar download incremental com validação e retomada.
3. Criar tabelas `raw` e `staging` e executar perfilamento das primeiras competências.
4. Definir chaves, regras de deduplicação e correspondências entre ComprasGov, PNCP e CNPJ.
5. Carregar o modelo `core` e publicar consultas de qualidade e rastreabilidade.
6. Criar o baseline estatístico de preços antes de treinar modelos de IA.
7. Medir precisão, cobertura, estabilidade e explicabilidade das previsões.
