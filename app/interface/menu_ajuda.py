# -*- coding: cp1252 -*-
# Autor: Marcio Welb de Aguiar Silveira
# E-mail: marciowelb@outlook.com.br
# Telefone: 55 11 98137-0755
"""Menu Ajuda da aplicação."""

import tkinter as tk

from app.interface.janela_ajuda import JanelaReadme, JanelaSobre


class MenuAjuda:
    """Cria as opções de documentação e informações do sistema."""

    def __init__(self, janela_principal):
        self.janela_principal = janela_principal

    def criar_menu(self, barra_de_menu):
        """Adiciona o menu Ajuda à barra de menus."""
        menu_ajuda = tk.Menu(barra_de_menu, tearoff=False)
        menu_ajuda.add_command(label="README", command=self.exibir_readme)
        menu_ajuda.add_command(label="Sobre", command=self.exibir_sobre)
        barra_de_menu.add_cascade(label="Ajuda", menu=menu_ajuda)
        return menu_ajuda

    def exibir_readme(self):
        """Abre o README.md com Markdown e Mermaid renderizados."""
        JanelaReadme(self.janela_principal)

    def exibir_sobre(self):
        """Abre a janela com o objetivo do sistema e os dados do autor."""
        JanelaSobre(self.janela_principal)
