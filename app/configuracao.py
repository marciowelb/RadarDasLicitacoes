# =============================================================================
# Arquivo: app/configuracao.py
# Descrição: Define as configurações da rotina de download do ComprasGov.
#
# Classes e métodos principais:
#   - Não se aplica neste arquivo.
#
# Autor: Marcio Welb de Aguiar Silveira
# E-mail: marciowelb@outlook.com.br
# Telefone: 55 11 98137-0755
# Data de criação: 2026-11-05
# Última alteração: 2026-11-05
#
# Lista de mudanças:
#   - Criação das configurações iniciais do download.
# =============================================================================

from pathlib import Path

# ----------------------------------------------------------
URL_BASE_COMPRASGOV = "https://repositorio.dados.gov.br/seges/comprasgov/"

# Periodo de inicio da baixa dos dados, se necessario, pode ser alterado para um periodo mais antigo.
# deixei fixo essa data pois o volume é grande de dados, dificultado upload no git.
ANO_INICIAL_DADOS = 2026
MES_INICIAL_DADOS = 10
# ----------------------------------------------------------



DIRETORIO_DADOS_BRUTOS = Path("data/raw/comprasgov")
DIRETORIO_DOWNLOAD_TEMPORARIO = Path("data/temporario/downloads")
DIRETORIO_MANIFESTO = DIRETORIO_DADOS_BRUTOS / "manifesto_download.jsonl"
TEMPO_LIMITE_DOWNLOAD = 60.0
TAMANHO_BLOCO_DOWNLOAD = 1024 * 1024
QUANTIDADE_MAXIMA_TENTATIVAS = 3

# =============================================================================
# Autor: Marcio Welb de Aguiar Silveira
# E-mail: marciowelb@outlook.com.br
# Telefone: 55 11 98137-0755
# =============================================================================
