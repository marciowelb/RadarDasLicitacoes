# =============================================================================
# Arquivo: app/interface/janela_download_comprasgov.py
# Descrição: Exibe e executa a janela de download dos dados ComprasGov.
#
# Classes e métodos principais:
#   - JanelaDownloadComprasGov: controla seleção, progresso e log do download.
#
# Autor: Marcio Welb de Aguiar Silveira
# E-mail: marciowelb@outlook.com.br
# Telefone: 55 11 98137-0755
# Data de criação: 2026-11-05
# Última alteração: 2026-11-05
#
# Lista de mudanças:
#   - Criação da janela independente de download ComprasGov.
# =============================================================================

from pathlib import Path
from datetime import date
from threading import Thread
import tkinter as tk
from tkinter import messagebox, ttk

from app.configuracao import (
    DIRETORIO_DADOS_BRUTOS,
    DIRETORIO_DOWNLOAD_TEMPORARIO,
    DIRETORIO_MANIFESTO,
)
from app.download.baixador_de_arquivos import BaixadorDeArquivos
from app.download.extrator_de_csv import ExtratorDeCsv
from app.download.manifesto_de_arquivos import ManifestoDeArquivos
from app.download.validador_de_download import ValidadorDeDownload
from app.fontes.fonte_comprasgov import FonteComprasGov


class JanelaDownloadComprasGov:
    """Executa o download dos arquivos ComprasGov em janela independente."""

    # -------------------------------------------------------------------------

    def __init__(self, janela_principal):
        """Inicializa a janela e seus componentes de download."""
        self.janela_principal = janela_principal
        self.janela = tk.Toplevel(janela_principal)
        self.fonte_comprasgov = FonteComprasGov()
        self.baixador = BaixadorDeArquivos(self.registrar_log)
        self.validador = ValidadorDeDownload()
        self.extrator = ExtratorDeCsv()
        self.manifesto = ManifestoDeArquivos(DIRETORIO_MANIFESTO)
        self.download_em_execucao = False
        hoje = date.today()
        indice_mes = hoje.year * 12 + hoje.month - 1 - 11
        self.ano_inicial_padrao = indice_mes // 12
        self.mes_inicial_padrao = indice_mes % 12 + 1
        self.ano_final_padrao = hoje.year
        self.mes_final_padrao = hoje.month
        self.configurar_janela()
        self.criar_componentes()

    # -------------------------------------------------------------------------

    def configurar_janela(self):
        """Configura tamanho, título e comportamento da janela."""
        self.janela.title("Download dados Compras Governamentais")
        self.janela.geometry("800x620")
        self.janela.minsize(700, 500)

    # -------------------------------------------------------------------------

    def criar_componentes(self):
        """Cria os campos, botões, log e barra de progresso."""
        quadro_selecao = ttk.LabelFrame(self.janela, text="Parâmetros do download")
        quadro_selecao.pack(fill="x", padx=12, pady=12)

        ttk.Label(quadro_selecao, text="Base:").grid(row=0, column=0, padx=8, pady=8)
        self.familia = tk.StringVar(value="todas")
        seletor_familia = ttk.Combobox(
            quadro_selecao,
            textvariable=self.familia,
            values=("todas", "pncp", "propostas", "pesquisa_precos", "arp", "catalogo_cnbs", "compras_legado"),
            state="readonly",
            width=24,
        )
        seletor_familia.grid(row=0, column=1, padx=8, pady=8)

        ttk.Label(quadro_selecao, text="Início (ano/mês):").grid(row=0, column=2, padx=8, pady=8)
        self.ano_inicial = tk.StringVar(value=str(self.ano_inicial_padrao))
        ttk.Entry(quadro_selecao, textvariable=self.ano_inicial, width=8).grid(
            row=0, column=3, padx=2, pady=8
        )
        self.mes_inicial = tk.StringVar(value=f"{self.mes_inicial_padrao:02d}")
        ttk.Entry(quadro_selecao, textvariable=self.mes_inicial, width=5).grid(
            row=0, column=4, padx=2, pady=8
        )

        ttk.Label(quadro_selecao, text="Fim (ano/mês):").grid(row=0, column=5, padx=8, pady=8)
        self.ano_final = tk.StringVar(value=str(self.ano_final_padrao))
        ttk.Entry(quadro_selecao, textvariable=self.ano_final, width=8).grid(
            row=0, column=6, padx=2, pady=8
        )
        self.mes_final = tk.StringVar(value=f"{self.mes_final_padrao:02d}")
        ttk.Entry(quadro_selecao, textvariable=self.mes_final, width=5).grid(
            row=0, column=7, padx=2, pady=8
        )

        quadro_botoes = ttk.Frame(self.janela)
        quadro_botoes.pack(fill="x", padx=12, pady=(0, 8))
        self.botao_iniciar = ttk.Button(
            quadro_botoes,
            text="Iniciar download",
            command=self.iniciar_download,
        )
        self.botao_iniciar.pack(side="left", padx=(0, 8))
        self.botao_cancelar = ttk.Button(
            quadro_botoes,
            text="Cancelar",
            command=self.cancelar_download,
            state="disabled",
        )
        self.botao_cancelar.pack(side="left")

        self.progresso = ttk.Progressbar(self.janela, mode="determinate", maximum=100)
        self.progresso.pack(fill="x", padx=12, pady=8)
        self.status = tk.StringVar(value="Aguardando início.")
        ttk.Label(self.janela, textvariable=self.status).pack(anchor="w", padx=12)

        quadro_log = ttk.LabelFrame(self.janela, text="Log de execução")
        quadro_log.pack(fill="both", expand=True, padx=12, pady=12)
        self.log = tk.Text(
            quadro_log,
            state="disabled",
            wrap="word",
            background="#1e1e1e",
            foreground="#00ff66",
            insertbackground="#ffffff",
            selectbackground="#264f78",
            selectforeground="#ffffff",
        )
        self.log.pack(side="left", fill="both", expand=True)
        barra_rolagem = ttk.Scrollbar(quadro_log, command=self.log.yview)
        barra_rolagem.pack(side="right", fill="y")
        self.log.configure(yscrollcommand=barra_rolagem.set)

    # -------------------------------------------------------------------------

    def registrar_log(self, mensagem):
        """Adiciona uma mensagem ao log de forma segura para a interface."""
        self.janela.after(0, self._adicionar_log, mensagem)

    # -------------------------------------------------------------------------

    def _adicionar_log(self, mensagem):
        """Adiciona uma mensagem no componente visual de log."""
        self.log.configure(state="normal")
        self.log.insert(tk.END, f"{mensagem}\n")
        self.log.see(tk.END)
        self.log.configure(state="disabled")

    # -------------------------------------------------------------------------

    def atualizar_progresso(self, percentual, quantidade_baixada, tamanho_total):
        """Atualiza a barra e o status de progresso na interface."""
        self.janela.after(
            0,
            self._atualizar_barra,
            percentual,
            quantidade_baixada,
            tamanho_total,
        )

    # -------------------------------------------------------------------------

    def _atualizar_barra(self, percentual, quantidade_baixada, tamanho_total):
        """Atualiza os controles visuais da barra no thread da interface."""
        if percentual is None:
            self.progresso.configure(mode="indeterminate")
            self.progresso.start(10)
            self.status.set(f"Baixados {quantidade_baixada} bytes.")
        else:
            self.progresso.stop()
            self.progresso.configure(mode="determinate", value=percentual)
            self.status.set(f"Progresso: {percentual}%.")

    # -------------------------------------------------------------------------

    # -------------------------------------------------------------------------

    def iniciar_download(self):
        """Valida os campos e inicia o download em uma thread."""
        if self.download_em_execucao:
            return
        try:
            ano_inicial = int(self.ano_inicial.get())
            mes_inicial = int(self.mes_inicial.get())
            ano_final = int(self.ano_final.get())
            mes_final = int(self.mes_final.get())
            self.fonte_comprasgov.validar_periodo(
                ano_inicial,
                mes_inicial,
                ano_final,
                mes_final,
            )
        except ValueError as erro:
            messagebox.showerror("Dados inválidos", str(erro), parent=self.janela)
            return

        self.download_em_execucao = True
        self.botao_iniciar.configure(state="disabled")
        self.botao_cancelar.configure(state="normal")
        Thread(
            target=self.executar_download,
            args=(ano_inicial, mes_inicial, ano_final, mes_final, self.familia.get()),
            daemon=True,
        ).start()

    # -------------------------------------------------------------------------

    def executar_download(self, ano_inicial, mes_inicial, ano_final, mes_final, familia):
        """Baixa, valida e grava os arquivos selecionados."""
        quantidade_erros = 0
        try:
            familias = self.fonte_comprasgov.obter_familias() if familia == "todas" else (familia,)
            for familia_atual in familias:
                self.registrar_log(f"Iniciando descoberta da família {familia_atual}.")
                enderecos = self.fonte_comprasgov.listar_arquivos(
                    familia_atual,
                    ano_inicial,
                    self.registrar_log,
                    mes_inicial,
                    ano_final,
                    mes_final,
                )
                self.registrar_log(
                    f"Arquivos encontrados em {familia_atual}: {len(enderecos)}."
                )
                for endereco in enderecos:
                    resultado = self.baixar_arquivo_encontrado(
                        endereco,
                        ano_inicial,
                        mes_inicial,
                        familia_atual,
                    )
                    if resultado is False:
                        quantidade_erros += 1

            self.registrar_log(
                f"Operação concluída. Erros: {quantidade_erros}."
            )
            self.janela.after(0, lambda: self.status.set("Download concluído."))
        except Exception as erro:
            self.registrar_log(f"Erro na descoberta: {erro}")
            self.janela.after(0, lambda: self.status.set("Download finalizado com erro."))
        finally:
            self.janela.after(0, self.finalizar_download)

    # -------------------------------------------------------------------------

    def baixar_arquivo_encontrado(self, endereco, ano, mes, familia):
        """Baixa e grava um arquivo descoberto, retornando sucesso ou falha."""
        nome_arquivo = endereco.rstrip("/").split("/")[-1]
        caminho_destino = DIRETORIO_DADOS_BRUTOS / Path(nome_arquivo).name
        caminho_temporario = DIRETORIO_DOWNLOAD_TEMPORARIO / f"{nome_arquivo}.part"

        if self.manifesto.foi_concluido(endereco):
            self.registrar_log(f"Arquivo já concluído: {endereco}")
            return True

        try:
            self.manifesto.registrar(endereco, "BAIXANDO", caminho_destino)
            self.baixador.baixar_arquivo(
                endereco,
                caminho_temporario,
                self.atualizar_progresso,
            )
            self.validador.validar_arquivo(caminho_temporario)
            self.validador.validar_extensao(Path(nome_arquivo))
            caminho_destino.parent.mkdir(parents=True, exist_ok=True)
            if nome_arquivo.lower().endswith(".zip"):
                arquivos = self.extrator.extrair_csv(
                    caminho_temporario,
                    caminho_destino.parent,
                )
                for arquivo in arquivos:
                    self.registrar_log(f"CSV gravado em: {arquivo}")
            else:
                caminho_temporario.replace(caminho_destino)
                self.registrar_log(f"CSV gravado em: {caminho_destino}")
            caminho_temporario.unlink(missing_ok=True)
            self.manifesto.registrar(endereco, "CONCLUIDO", caminho_destino)
            return True
        except Exception as erro_arquivo:
            quantidade_erro = f"Falha no arquivo {endereco}: {erro_arquivo}"
            self.registrar_log(quantidade_erro)
            self.manifesto.registrar(endereco, "ERRO", caminho_destino, str(erro_arquivo))
            caminho_temporario.unlink(missing_ok=True)
            return False

    # -------------------------------------------------------------------------

    def cancelar_download(self):
        """Solicita o cancelamento do download em execução."""
        if self.download_em_execucao:
            self.baixador.cancelar_download()
            self.registrar_log("Cancelamento solicitado pelo usuário.")

    # -------------------------------------------------------------------------

    def finalizar_download(self):
        """Libera os controles da janela após o término da operação."""
        self.download_em_execucao = False
        self.botao_iniciar.configure(state="normal")
        self.botao_cancelar.configure(state="disabled")
        self.progresso.stop()

    # -------------------------------------------------------------------------

# =============================================================================
# Autor: Marcio Welb de Aguiar Silveira
# E-mail: marciowelb@outlook.com.br
# Telefone: 55 11 98137-0755
# =============================================================================
