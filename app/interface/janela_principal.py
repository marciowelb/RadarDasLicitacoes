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
# Última alteração: 2026-11-07
#
# Lista de mudanças:
#   - Criação da janela principal como barra fina de menus.
#   - Adição do botão de download de CNPJ (ainda sem funcionalidade).
# =============================================================================

"""Janela principal da aplicação Windows."""

import tkinter as tk

from app.interface.menu_ajuda import MenuAjuda
from app.interface.menu_download import MenuDownload


class Tooltip:
    """Exibe uma descrição breve ao manter o mouse sobre um controle."""

    def __init__(self, controle, texto):
        self.controle = controle
        self.texto = texto
        self.janela = None
        self.agendamento = None
        controle.bind("<Enter>", self.agendar, add="+")
        controle.bind("<Leave>", self.esconder, add="+")

    def agendar(self, evento=None):
        """Agenda a exibição do tooltip após um breve intervalo."""
        self.esconder()
        self.agendamento = self.controle.after(500, self.exibir)

    def exibir(self):
        """Exibe o texto próximo ao controle."""
        if self.janela or not self.controle.winfo_viewable():
            return
        x = self.controle.winfo_rootx() + self.controle.winfo_width() // 2
        y = self.controle.winfo_rooty() + self.controle.winfo_height() + 6
        self.janela = tk.Toplevel(self.controle)
        self.janela.wm_overrideredirect(True)
        self.janela.geometry(f"+{x}+{y}")
        tk.Label(
            self.janela,
            text=self.texto,
            background="#fff8dc",
            foreground="#202124",
            relief="solid",
            borderwidth=1,
            padx=8,
            pady=4,
        ).pack()

    def esconder(self, evento=None):
        """Cancela ou remove o tooltip atual."""
        if self.agendamento:
            self.controle.after_cancel(self.agendamento)
            self.agendamento = None
        if self.janela:
            self.janela.destroy()
            self.janela = None


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
        self.menu_ajuda = MenuAjuda(self.janela)
        self.configurar_janela()
        self.criar_menu()
        self.criar_barra_ferramentas()
    # -------------------------------------------------------------------------



    # -------------------------------------------------------------------------
    def configurar_janela(self):
        """Define a janela principal como uma barra fina de menus."""

        # ---------------------------------------------------------
        #   TITULO DA APLICACAO COM A VERSÃO
        # ---------------------------------------------------------
        self.janela.title("Radar das Licitações - v:2026-11-07(a) ")
        # ---------------------------------------------------------


        self.janela.geometry("520x50")
        self.janela.minsize(420, 50)
        self.janela.resizable(True, False)
    # -------------------------------------------------------------------------



    # -------------------------------------------------------------------------

    def criar_menu(self):
        """Cria a barra de menus e adiciona o menu de download."""
        barra_de_menu = tk.Menu(self.janela)
        self.menu_download.criar_menu(barra_de_menu)
        self.menu_ajuda.criar_menu(barra_de_menu)
        self.janela.config(menu=barra_de_menu)

    # -------------------------------------------------------------------------

    def criar_barra_ferramentas(self):
        """Cria uma barra compacta de ferramentas no padrão de IDEs modernas."""
        barra = tk.Frame(
            self.janela,
            background="#f3f3f3",
            highlightbackground="#d6d6d6",
            highlightthickness=1,
            padx=6,
            pady=4,
        )
        barra.pack(fill="x")

        self.criar_botao_ferramenta(
            barra,
            "comprasgov",
            "Baixar dados de compras governamentais",
            self.menu_download.exibir_download_compras_governamentais,
        )
        tk.Frame(barra, width=1, height=28, background="#d0d0d0").pack(
            side="left", padx=6
        )
        self.criar_botao_ferramenta(
            barra,
            "cnpj",
            "Baixar dados de CNPJ (em breve)",
            self.menu_download.exibir_download_cnpj,
        )

    def criar_botao_ferramenta(self, barra, tipo, descricao, comando):
        """Cria um botão de ferramenta com ícone vetorial e estado hover."""
        fundo = "#f3f3f3"
        destaque = "#ff69b4"
        cor = "#3b3b3b"
        botao = tk.Frame(barra, width=36, height=34, background=fundo, cursor="hand2")
        botao.pack_propagate(False)
        botao.pack(side="left")
        icone = tk.Canvas(
            botao,
            width=24,
            height=24,
            background=fundo,
            highlightthickness=0,
        )
        icone.place(relx=0.5, rely=0.5, anchor="center")

        if tipo == "comprasgov":
            icone.create_rectangle(5, 15, 19, 20, outline=cor, width=2, tags="contorno")
            icone.create_line(5, 15, 19, 15, fill=cor, width=2, tags="linhas")
            icone.create_line(12, 4, 12, 15, fill=cor, width=2, tags="linhas")
            icone.create_line(8, 11, 12, 15, fill=cor, width=2, tags="linhas")
            icone.create_line(16, 11, 12, 15, fill=cor, width=2, tags="linhas")
        else:
            icone.create_rectangle(6, 3, 17, 21, outline=cor, width=2, tags="contorno")
            icone.create_line(9, 8, 15, 8, fill=cor, width=1, tags="linhas")
            icone.create_line(9, 11, 15, 11, fill=cor, width=1, tags="linhas")
            icone.create_text(
                12,
                16,
                text="C",
                fill=cor,
                font=("Segoe UI", 7, "bold"),
                tags="texto",
            )

        componentes = (botao, icone)
        for componente in componentes:
            componente.bind("<Button-1>", lambda evento: comando(), add="+")
            componente.bind(
                "<Enter>",
                lambda evento: self.alterar_estado_ferramenta(
                    botao, icone, destaque, "#d00000", "#b00020"
                ),
                add="+",
            )
            componente.bind(
                "<Leave>",
                lambda evento: self.alterar_estado_ferramenta(
                    botao, icone, fundo, cor, fundo
                ),
                add="+",
            )
        Tooltip(botao, descricao)

    def alterar_estado_ferramenta(self, botao, icone, fundo, cor_icone, cor_borda):
        """Atualiza fundo, contorno e cor do ícone durante o hover."""
        botao.configure(background=fundo)
        icone.configure(background=fundo)
        botao.configure(
            highlightthickness=1,
            highlightbackground=cor_borda,
            highlightcolor=cor_borda,
        )
        icone.itemconfigure("contorno", outline=cor_icone)
        icone.itemconfigure("linhas", fill=cor_icone)
        icone.itemconfigure("texto", fill=cor_icone)

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
