# =============================================================================
# Arquivo: app/download/extrator_de_csv.py
# Descrição: Extrai arquivos CSV de pacotes ZIP do ComprasGov.
#
# Classes e métodos principais:
#   - ExtratorDeCsv: localiza e extrai CSVs sem alterar seu conteúdo.
#
# Autor: Marcio Welb de Aguiar Silveira
# E-mail: marciowelb@outlook.com.br
# Telefone: 55 11 98137-0755
# Data de criação: 2026-11-05
# Última alteração: 2026-11-05
#
# Lista de mudanças:
#   - Criação do extrator seguro de CSV.
# =============================================================================

from pathlib import Path
from zipfile import ZipFile


class ExtratorDeCsv:
    """Extrai CSVs de ZIPs para o diretório final dos dados brutos."""

    # -------------------------------------------------------------------------

    def extrair_csv(self, caminho_zip: Path, diretorio_destino: Path):
        """
        Extrai todos os CSVs encontrados no ZIP.

        Args:
            caminho_zip: Caminho do arquivo ZIP baixado.
            diretorio_destino: Diretório final dos CSVs.

        Returns:
            list[Path]: Arquivos CSV extraídos.
        """
        diretorio_destino.mkdir(parents=True, exist_ok=True)
        arquivos_extraidos = []

        with ZipFile(caminho_zip) as arquivo_zip:
            nomes_csv = [
                nome for nome in arquivo_zip.namelist()
                if nome.lower().endswith(".csv")
            ]
            if not nomes_csv:
                raise ValueError(f"Nenhum CSV encontrado em {caminho_zip.name}.")

            for nome_csv in nomes_csv:
                caminho_saida = diretorio_destino / Path(nome_csv).name
                with arquivo_zip.open(nome_csv) as origem:
                    with caminho_saida.open("wb") as destino:
                        destino.write(origem.read())
                arquivos_extraidos.append(caminho_saida)

        return arquivos_extraidos

    # -------------------------------------------------------------------------

# =============================================================================
# Autor: Marcio Welb de Aguiar Silveira
# E-mail: marciowelb@outlook.com.br
# Telefone: 55 11 98137-0755
# =============================================================================
