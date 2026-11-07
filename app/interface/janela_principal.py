# =============================================================================
# Arquivo: app/interface/janela_principal.py
# Descrição: Cria e controla a janela principal fina da aplicação Windows.
#
# Classes e métodos principais:
#   - JanelaPrincipal: representa a janela principal e sua barra de menu.
#   - configurar_janela: configura o tamanho e o comportamento da janela.
#   - criar_menu: cria a barra de menus da aplicação.
#   - executar: inicia o ciclo de eventos da interface.
#
# Autor: Marcio Welb de Aguiar Silveira
# E-mail: marciowelb@outlook.com.br
# Telefone: 55 11 98137-0755
# Data de criação: 2026-11-05
# Última alteração: 2026-11-05
#
# Lista de mudanças:
#   - Criação da janela principal como barra fina de menus.
# =============================================================================

"""Janela principal da aplicação Windows."""

import tkinter as tk

from app.interface.menu_download import MenuDownload


class JanelaPrincipal:
    """
    Representa a janela principal do Radar das Licitações.

    Nesta primeira versão, a janela fornece somente a estrutura visual e o
    menu de download, sem executar operações de rede ou gravação de arquivos.
    """

    # -------------------------------------------------------------------------

    def __init__(self):
        """Inicializa a janela e configura seus componentes visuais."""
        self.janela = tk.Tk()
        self.menu_download = MenuDownload(self.janela)
        self.configurar_janela()
        self.criar_menu()
    # -------------------------------------------------------------------------

    def configurar_janela(self):
        """Define a janela principal como uma barra fina de menus."""

        # ---------------------------------------------------------
        #   TITULO DA APLICACAO COM A VERSÃO
        # ---------------------------------------------------------
        self.janela.title("Radar das Licitações - v:2026-11-07(a) ")
        # ---------------------------------------------------------


        self.janela.geometry("520x55")
        self.janela.minsize(420, 55)
        self.janela.resizable(True, False)

    # -------------------------------------------------------------------------

    def criar_menu(self):
        """Cria a barra de menus e adiciona o menu de download."""
        barra_de_menu = tk.Menu(self.janela)
        self.menu_download.criar_menu(barra_de_menu)
        self.janela.config(menu=barra_de_menu)

    # -------------------------------------------------------------------------

    def executar(self):
        """Inicia o ciclo de eventos da aplicação Windows."""
        self.janela.mainloop()

    # -------------------------------------------------------------------------

# =============================================================================
# Autor: Marcio Welb de Aguiar Silveira
# E-mail: marciowelb@outlook.com.br
# Telefone: 55 11 98137-0755
# =============================================================================
