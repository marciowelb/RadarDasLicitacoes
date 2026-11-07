# =============================================================================
# Arquivo: app/download/baixador_de_arquivos.py
# Descrição: Realiza downloads HTTP em blocos com progresso e cancelamento.
#
# Classes e métodos principais:
#   - BaixadorDeArquivos: baixa arquivos para um caminho temporário.
#   - baixar_arquivo: executa o download de uma URL.
#
# Autor: Marcio Welb de Aguiar Silveira
# E-mail: marciowelb@outlook.com.br
# Telefone: 55 11 98137-0755
# Data de criação: 2026-11-05
# Última alteração: 2026-11-05
#
# Lista de mudanças:
#   - Implementação do download HTTP em blocos.
# =============================================================================

from pathlib import Path
from threading import Event
from typing import Callable, Optional

import httpx

from app.configuracao import TAMANHO_BLOCO_DOWNLOAD, TEMPO_LIMITE_DOWNLOAD


class BaixadorDeArquivos:
    """Realiza downloads HTTP sem alterar o conteúdo recebido da fonte."""

    # -------------------------------------------------------------------------

    def __init__(self, registrador_mensagem: Callable[[str], None]):
        """Inicializa o baixador com a função responsável pelo log da tela."""
        self.registrador_mensagem = registrador_mensagem
        self.cancelamento = Event()

    # -------------------------------------------------------------------------

    def baixar_arquivo(
        self,
        endereco: str,
        caminho_temporario: Path,
        funcao_progresso: Callable[[Optional[int], int, Optional[int]], None],
    ) -> None:
        """
        Baixa um arquivo em blocos para um arquivo temporário.

        Args:
            endereco: URL do arquivo.
            caminho_temporario: Caminho do arquivo temporário `.part`.
            funcao_progresso: Recebe percentual, bytes baixados e tamanho total.

        Raises:
            RuntimeError: Quando o download é cancelado.
            httpx.HTTPError: Quando ocorre erro de comunicação HTTP.
        """
        caminho_temporario.parent.mkdir(parents=True, exist_ok=True)
        self.cancelamento.clear()
        self.registrador_mensagem(f"Iniciando download: {endereco}")

        with httpx.stream(
            "GET",
            endereco,
            follow_redirects=True,
            timeout=TEMPO_LIMITE_DOWNLOAD,
        ) as resposta:
            resposta.raise_for_status()
            tamanho_total = int(resposta.headers.get("content-length", 0)) or None
            quantidade_baixada = 0

            with caminho_temporario.open("wb") as arquivo_temporario:
                for bloco in resposta.iter_bytes(chunk_size=TAMANHO_BLOCO_DOWNLOAD):
                    if self.cancelamento.is_set():
                        raise RuntimeError("Download cancelado pelo usuário.")
                    arquivo_temporario.write(bloco)
                    quantidade_baixada += len(bloco)
                    percentual = self.calcular_percentual(
                        quantidade_baixada,
                        tamanho_total,
                    )
                    funcao_progresso(
                        percentual,
                        quantidade_baixada,
                        tamanho_total,
                    )

        self.registrador_mensagem("Download concluído.")

    # -------------------------------------------------------------------------

    def calcular_percentual(self, quantidade_baixada, tamanho_total):
        """Calcula o percentual ou retorna `None` quando o tamanho é desconhecido."""
        if not tamanho_total:
            return None
        return min(int(quantidade_baixada * 100 / tamanho_total), 100)

    # -------------------------------------------------------------------------

    def cancelar_download(self):
        """Solicita o cancelamento do download em execução."""
        self.cancelamento.set()

    # -------------------------------------------------------------------------

# =============================================================================
# Autor: Marcio Welb de Aguiar Silveira
# E-mail: marciowelb@outlook.com.br
# Telefone: 55 11 98137-0755
# =============================================================================


