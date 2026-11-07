# =============================================================================
# -*- coding: cp1252 -*-
# Arquivo: app/download/manifesto_de_arquivos.py
# Descrição: Registra o resultado de cada arquivo encontrado no download.
#
# Classes e métodos principais:
#   - ManifestoDeArquivos: grava eventos em formato JSON Lines.
#
# Autor: Marcio Welb de Aguiar Silveira
# E-mail: marciowelb@outlook.com.br
# Telefone: 55 11 98137-0755
# Data de criação: 2026-11-05
# Última alteração: 2026-11-05
#
# Lista de mudanças:
#   - Criação do manifesto de execução dos downloads.
# =============================================================================

import json
from datetime import datetime
from pathlib import Path
from threading import Lock


class ManifestoDeArquivos:
    """Registra status, origem e destino dos arquivos da execução."""

    # -------------------------------------------------------------------------

    def __init__(self, caminho_manifesto: Path):
        """Inicializa o manifesto e garante a existência do diretório."""
        self.caminho_manifesto = caminho_manifesto
        self.caminho_manifesto.parent.mkdir(parents=True, exist_ok=True)
        self.bloqueio = Lock()

    # -------------------------------------------------------------------------

    def registrar(self, endereco, status, caminho_destino=None, mensagem=None):
        """Adiciona um evento de arquivo ao manifesto JSONL."""
        registro = {
            "data_hora": datetime.now().isoformat(timespec="seconds"),
            "endereco": endereco,
            "status": status,
            "caminho_destino": str(caminho_destino) if caminho_destino else None,
            "mensagem": mensagem,
        }
        with self.bloqueio:
            with self.caminho_manifesto.open("a", encoding="utf-8") as arquivo:
                arquivo.write(json.dumps(registro, ensure_ascii=False) + "\n")

    # -------------------------------------------------------------------------

    def foi_concluido(self, endereco):
        """Retorna se o último registro da URL indica conclusão."""
        if not self.caminho_manifesto.exists():
            return False
        ultimo_status = None
        with self.caminho_manifesto.open("r", encoding="utf-8") as arquivo:
            for linha in arquivo:
                try:
                    registro = json.loads(linha)
                except json.JSONDecodeError:
                    continue
                if registro.get("endereco") == endereco:
                    ultimo_status = registro.get("status")
        return ultimo_status == "CONCLUIDO"

    # -------------------------------------------------------------------------

# =============================================================================
# Autor: Marcio Welb de Aguiar Silveira
# E-mail: marciowelb@outlook.com.br
# Telefone: 55 11 98137-0755
# =============================================================================
