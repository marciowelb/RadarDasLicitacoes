# =============================================================================
# Arquivo: app/interface/menu_download.py
# Descrição: Cria o menu Download e abre as janelas das opções disponíveis.
#
# Classes e métodos principais:
#   - MenuDownload: administra o menu e as janelas de download.
#   - criar_menu: cria as opções do menu Download.
#   - exibir_download_compras_governamentais: abre a janela de ComprasGov.
#
# Autor: Marcio Welb de Aguiar Silveira
# E-mail: marciowelb@outlook.com.br
# Telefone: 55 11 98137-0755
# Data de criação: 2026-11-05
# Última alteração: 2026-11-05
#
# Lista de mudanças:
#   - Criação do menu de download.
#   - Inclusão das janelas independentes para Compras Governamentais e CNPJ.
# =============================================================================

"""Menu e opções de download da aplicação."""

import tkinter as tk
from tkinter import messagebox

from app.interface.janela_download_comprasgov import JanelaDownloadComprasGov


class MenuDownload:
    """
    Cria o menu de download da aplicação Windows.

    A opção Compras Governamentais abre a rotina de download. O CNPJ permanece
    apenas como opção futura nesta primeira etapa.
    """

    # -------------------------------------------------------------------------

    def __init__(self, janela_principal):
        """Inicializa o menu usando a janela principal como referência."""
        self.janela_principal = janela_principal

    # -------------------------------------------------------------------------

    def criar_menu(self, barra_de_menu):
        """
        Cria o menu Download e suas opções.

        Args:
            barra_de_menu: Barra de menus da janela principal.

        Returns:
            tk.Menu: Menu de download criado.
        """
        menu_download = tk.Menu(barra_de_menu, tearoff=False)
        menu_download.add_command(
            label="Download dados Compras Governamentais",
            command=self.exibir_download_compras_governamentais,
        )
        menu_download.add_command(
            label="Download dados de CNPJ",
            command=self.exibir_download_cnpj,
        )
        barra_de_menu.add_cascade(label="Download", menu=menu_download)
        return menu_download

    # -------------------------------------------------------------------------

    def exibir_download_compras_governamentais(self):
        """Abre a janela independente de dados governamentais."""
        JanelaDownloadComprasGov(self.janela_principal)

    # -------------------------------------------------------------------------

    def exibir_download_cnpj(self):
        """Informa que o download de CNPJ será implementado posteriormente."""
        messagebox.showinfo(
            "Download de CNPJ",
            "O download de CNPJ será implementado em uma próxima versão.",
            parent=self.janela_principal,
        )

# =============================================================================
# Autor: Marcio Welb de Aguiar Silveira
# E-mail: marciowelb@outlook.com.br
# Telefone: 55 11 98137-0755
# =============================================================================
