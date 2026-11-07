# =============================================================================
# Arquivo: app/fontes/fonte_comprasgov.py
# Descrição: Monta endereços de arquivos publicados no repositório ComprasGov.
#
# Classes e métodos principais:
#   - FonteComprasGov: identifica arquivos conhecidos da fonte.
#   - obter_enderecos_pncp: monta os arquivos mensais conhecidos do PNCP.
#
# Autor: Marcio Welb de Aguiar Silveira
# E-mail: marciowelb@outlook.com.br
# Telefone: 55 11 98137-0755
# Data de criação: 2026-11-05
# Última alteração: 2026-11-05
#
# Lista de mudanças:
#   - Criação do adaptador inicial do repositório ComprasGov.
# =============================================================================

from html.parser import HTMLParser
from pathlib import PurePosixPath
from urllib.parse import urljoin, urlparse

import httpx

from app.configuracao import ANO_INICIAL_DADOS, URL_BASE_COMPRASGOV


class ExtratorDeLinks(HTMLParser):
    """Extrai links de páginas de listagem do servidor web."""

    # -------------------------------------------------------------------------

    def __init__(self):
        """Inicializa a lista de links encontrados."""
        super().__init__()
        self.links = []

    # -------------------------------------------------------------------------

    def handle_starttag(self, tag, atributos):
        """Armazena links encontrados em elementos HTML `a`."""
        if tag.lower() != "a":
            return
        for nome, valor in atributos:
            if nome.lower() == "href" and valor:
                self.links.append(valor)

    # -------------------------------------------------------------------------


class FonteComprasGov:
    """Monta URLs de arquivos disponíveis no repositório do ComprasGov."""

    # -------------------------------------------------------------------------

    def __init__(self, url_base=URL_BASE_COMPRASGOV):
        """Inicializa a fonte com a URL base oficial."""
        self.url_base = url_base.rstrip("/") + "/"

    # -------------------------------------------------------------------------

    def obter_enderecos_pncp(self, ano, mes):
        """
        Retorna os arquivos mensais conhecidos do PNCP.

        Args:
            ano: Ano da competência.
            mes: Mês da competência.

        Returns:
            list[str]: URLs dos arquivos PNCP.
        """
        mes_formatado = f"{mes:02d}"
        caminho = f"pncp/{ano}/{mes_formatado}/"
        nomes_arquivos = (
            f"compra_{ano}_{mes_formatado}.csv.zip",
            f"compra_item_{ano}_{mes_formatado}.csv.zip",
            f"item_resultado_{ano}_{mes_formatado}.csv.zip",
        )
        return [self.url_base + caminho + nome for nome in nomes_arquivos]

    # -------------------------------------------------------------------------

    def obter_familias(self):
        """Retorna todas as famílias documentadas do ComprasGov."""
        return (
            "pncp",
            "propostas",
            "pesquisa_precos",
            "arp",
            "catalogo_cnbs",
            "compras_legado",
        )

    # -------------------------------------------------------------------------

    def validar_periodo(self, ano_inicial, mes_inicial, ano_final=None, mes_final=None):
        """Valida o período antes de iniciar uma operação de download."""
        if ano_final is None:
            ano_final = ano_inicial
        if mes_final is None:
            mes_final = mes_inicial
        if ano_inicial < 2025 or ano_final < 2025:
            raise ValueError("O ano deve ser igual ou superior a 2025.")
        if mes_inicial < 1 or mes_inicial > 12 or mes_final < 1 or mes_final > 12:
            raise ValueError("O mês deve estar entre 1 e 12.")
        if (ano_inicial, mes_inicial) > (ano_final, mes_final):
            raise ValueError("O período inicial deve ser anterior ou igual ao período final.")

    # -------------------------------------------------------------------------

    def listar_arquivos(
        self,
        familia,
        ano_inicial=ANO_INICIAL_DADOS,
        registrador=None,
        mes_inicial=1,
        ano_final=None,
        mes_final=12,
    ):
        """
        Percorre a família e retorna todos os CSVs e ZIPs disponíveis.

        A listagem é feita a partir dos índices publicados pelo repositório,
        sem presumir nomes de arquivos. Pastas e arquivos anteriores ao ano
        configurado são ignorados quando o caminho contém um ano identificável.

        Args:
            familia: Diretório da família no repositório.
            ano_inicial: Primeiro ano permitido para download.
            registrador: Função opcional para registrar o andamento.

        Returns:
            list[str]: URLs únicas de arquivos encontrados.
        """
        if ano_final is None:
            ano_final = ano_inicial
        arquivos = set()
        with httpx.Client(follow_redirects=True, timeout=30.0) as cliente:
            if familia == "catalogo_cnbs":
                arquivos.update(
                    self._listar_arquivos_diretorio(
                        cliente,
                        self.url_base + "catalogo_cnbs/",
                        registrador,
                    )
                )
            elif familia == "compras_legado":
                arquivos.update(
                    self._listar_arquivos_legado(
                        cliente,
                        ano_inicial,
                        ano_final,
                        registrador,
                    )
                )
            elif familia == "arp":
                arquivos.update(
                    self._listar_arquivos_arp(
                        cliente,
                        ano_inicial,
                        ano_final,
                        registrador,
                    )
                )
            else:
                arquivos.update(
                    self._listar_arquivos_anuais_mensais(
                        cliente,
                        familia,
                        ano_inicial,
                        mes_inicial,
                        ano_final,
                        mes_final,
                        registrador,
                    )
                )
        return sorted(arquivos)

    # -------------------------------------------------------------------------

    def _diretorio_deve_ser_visitado(self, endereco, ano_inicial, familia):
        """Decide se um subdiretório pode conter dados do período desejado."""
        partes = PurePosixPath(endereco.rstrip("/")).parts
        anos = [int(parte) for parte in partes if parte.isdigit() and len(parte) == 4]
        if anos and max(anos) < ano_inicial:
            return False
        return True

    # -------------------------------------------------------------------------

    def _arquivo_deve_ser_baixado(self, endereco, ano_inicial, familia, ano_final=None):
        """Filtra arquivos CSV/ZIP respeitando a competência inicial."""
        if ano_final is None:
            ano_final = ano_inicial
        nome = endereco.lower().split("?")[0]
        if not (nome.endswith(".csv") or nome.endswith(".zip")):
            return False
        partes = PurePosixPath(nome).parts
        anos = [int(parte) for parte in partes if parte.isdigit() and len(parte) == 4]
        if anos:
            return ano_inicial <= max(anos) <= ano_final
        if familia == "catalogo_cnbs":
            return True
        nome_sem_extensao = PurePosixPath(nome).stem
        anos_no_nome = [
            int(parte) for parte in nome_sem_extensao.replace("-", "_").split("_")
            if parte.isdigit() and len(parte) == 4
        ]
        return not anos_no_nome or max(anos_no_nome) >= ano_inicial

    # -------------------------------------------------------------------------

    def _listar_links(self, cliente, endereco_diretorio, registrador):
        """Lê uma página de índice e retorna seus links absolutos."""
        if registrador:
            registrador(f"Analisando diretório: {endereco_diretorio}")
        resposta = cliente.get(endereco_diretorio)
        resposta.raise_for_status()
        parser = ExtratorDeLinks()
        parser.feed(resposta.text)
        return [
            urljoin(endereco_diretorio, link)
            for link in parser.links
            if link not in ("../", "./") and not link.startswith("?")
        ]

    # -------------------------------------------------------------------------

    def _listar_arquivos_diretorio(self, cliente, endereco_diretorio, registrador):
        """Retorna arquivos CSV e ZIP de um diretório sem entrar nos filhos."""
        return [
            endereco for endereco in self._listar_links(
                cliente,
                endereco_diretorio,
                registrador,
            )
            if not endereco.endswith("/")
            and endereco.lower().split("?")[0].endswith((".csv", ".zip"))
        ]

    # -------------------------------------------------------------------------

    def _listar_arquivos_anuais_mensais(
        self,
        cliente,
        familia,
        ano_inicial,
        mes_inicial,
        ano_final,
        mes_final,
        registrador,
    ):
        """Lista arquivos de famílias particionadas por ano e mês."""
        arquivos = []
        endereco_familia = self.url_base + f"{familia}/"
        anos = self._listar_links(cliente, endereco_familia, registrador)
        for endereco_ano in anos:
            nome_ano = PurePosixPath(endereco_ano.rstrip("/")).name
            if not (endereco_ano.endswith("/") and nome_ano.isdigit()):
                continue
            ano = int(nome_ano)
            if ano < ano_inicial or ano > ano_final:
                continue
            meses = self._listar_links(cliente, endereco_ano, registrador)
            for endereco_mes in meses:
                if not endereco_mes.endswith("/"):
                    continue
                nome_mes = PurePosixPath(endereco_mes.rstrip("/")).name
                if not nome_mes.isdigit():
                    continue
                mes = int(nome_mes)
                if (ano, mes) < (ano_inicial, mes_inicial) or (ano, mes) > (ano_final, mes_final):
                    continue
                arquivos.extend(
                    self._listar_arquivos_diretorio(
                        cliente,
                        endereco_mes,
                        registrador,
                    )
                )
        return arquivos

    # -------------------------------------------------------------------------

    def _listar_arquivos_arp(self, cliente, ano_inicial, ano_final, registrador):
        """Lista arquivos de ARP da raiz e das pastas de anos permitidos."""
        arquivos = []
        endereco_familia = self.url_base + "arp/"
        links = self._listar_links(cliente, endereco_familia, registrador)
        for endereco in links:
            nome = PurePosixPath(endereco.rstrip("/")).name
            if endereco.endswith("/") and nome.isdigit() and ano_inicial <= int(nome) <= ano_final:
                arquivos.extend(
                    self._listar_arquivos_diretorio(cliente, endereco, registrador)
                )
            elif not endereco.endswith("/") and self._arquivo_deve_ser_baixado(
                endereco,
                ano_inicial,
                "arp",
                ano_final,
            ):
                arquivos.append(endereco)
        return arquivos

    # -------------------------------------------------------------------------

    def _listar_arquivos_legado(self, cliente, ano_inicial, ano_final, registrador):
        """Lista arquivos de cada modalidade do legado a partir do ano inicial."""
        arquivos = []
        endereco_familia = self.url_base + "compras_legado/"
        modalidades = self._listar_links(cliente, endereco_familia, registrador)
        for endereco_modalidade in modalidades:
            if not endereco_modalidade.endswith("/"):
                continue
            anos = self._listar_links(cliente, endereco_modalidade, registrador)
            for endereco_ano in anos:
                nome_ano = PurePosixPath(endereco_ano.rstrip("/")).name
                if not (endereco_ano.endswith("/") and nome_ano.isdigit()):
                    continue
                if int(nome_ano) < ano_inicial or int(nome_ano) > ano_final:
                    continue
                arquivos.extend(
                    self._listar_arquivos_diretorio(
                        cliente,
                        endereco_ano,
                        registrador,
                    )
                )
        return arquivos

    # -------------------------------------------------------------------------

    def obter_caminho_relativo(self, endereco, familia):
        """Retorna a estrutura relativa publicada para um arquivo."""
        caminho = PurePosixPath(urlparse(endereco).path)
        partes = list(caminho.parts)
        try:
            indice_familia = partes.index(familia)
        except ValueError:
            return PurePosixPath(caminho.name)
        partes_relativas = partes[indice_familia + 1:]
        return PurePosixPath(*partes_relativas)

    # -------------------------------------------------------------------------

# =============================================================================
# Autor: Marcio Welb de Aguiar Silveira
# E-mail: marciowelb@outlook.com.br
# Telefone: 55 11 98137-0755
# =============================================================================
