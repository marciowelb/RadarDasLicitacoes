# =============================================================================
# Arquivo: app/download/validador_de_download.py
# Descrição: Valida arquivos temporários antes da gravação definitiva.
#
# Classes e métodos principais:
#   - ValidadorDeDownload: valida existência, tamanho e extensão.
#
# Autor: Marcio Welb de Aguiar Silveira
# E-mail: marciowelb@outlook.com.br
# Telefone: 55 11 98137-0755
# Data de criação: 2026-11-05
# Última alteração: 2026-11-05
#
# Lista de mudanças:
#   - Criação das validações básicas do download.
# =============================================================================

from pathlib import Path


class ValidadorDeDownload:
    """Valida arquivos baixados antes de disponibilizá-los em `data/raw`."""

    # -------------------------------------------------------------------------

    def validar_arquivo(self, caminho_arquivo: Path):
        """Confirma que o arquivo existe e possui conteúdo."""
        if not caminho_arquivo.exists():
            raise FileNotFoundError(f"Arquivo não encontrado: {caminho_arquivo}")
        if caminho_arquivo.stat().st_size == 0:
            raise ValueError(f"Arquivo vazio: {caminho_arquivo}")

    # -------------------------------------------------------------------------

    def validar_extensao(self, caminho_arquivo: Path):
        """Confirma que o arquivo é CSV ou ZIP."""
        extensoes_validas = {".csv", ".zip"}
        if caminho_arquivo.suffix.lower() not in extensoes_validas:
            raise ValueError(f"Extensão não suportada: {caminho_arquivo.suffix}")

    # -------------------------------------------------------------------------

# =============================================================================
# Autor: Marcio Welb de Aguiar Silveira
# E-mail: marciowelb@outlook.com.br
# Telefone: 55 11 98137-0755
# =============================================================================
