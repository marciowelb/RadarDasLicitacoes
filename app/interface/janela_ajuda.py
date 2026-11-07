# -*- coding: cp1252 -*-
# Autor: Marcio Welb de Aguiar Silveira
# E-mail: marciowelb@outlook.com.br
# Telefone: 55 11 98137-0755
"""Janelas de ajuda, README e informações do sistema."""

import json
import tempfile
import webbrowser
from pathlib import Path
import tkinter as tk
from tkinter import messagebox, ttk


class JanelaReadme:
    """Lê o README e abre uma visualização Markdown com diagramas Mermaid."""

    def __init__(self, janela_pai):
        self.janela_pai = janela_pai
        self.caminho_readme = Path(__file__).resolve().parents[2] / "README.md"
        self.abrir_readme()

    def abrir_readme(self):
        """Gera uma página temporária e abre o README no navegador padrão."""
        try:
            conteudo = self.caminho_readme.read_text(encoding="utf-8")
        except OSError as erro:
            messagebox.showerror(
                "README",
                f"Não foi possível ler o arquivo README.md.\n\n{erro}",
                parent=self.janela_pai,
            )
            return

        conteudo_json = json.dumps(conteudo, ensure_ascii=False)
        html = f"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<title>Radar das Licitações - README</title>
<script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
<style>
body {{ max-width: 1200px; margin: 32px auto; padding: 0 24px; font-family: Segoe UI, Arial, sans-serif; line-height: 1.55; color: #202124; }}
pre {{ background: #f3f4f6; padding: 14px; overflow-x: auto; border-radius: 6px; }}
code {{ font-family: Consolas, monospace; }}
table {{ border-collapse: collapse; width: 100%; }}
th, td {{ border: 1px solid #d0d7de; padding: 8px; text-align: left; }}
th {{ background: #f6f8fa; }}
.mermaid {{ text-align: center; margin: 24px 0; }}
</style>
</head>
<body>
<main id="conteudo"></main>
<script>
const markdown = {conteudo_json};
const html = marked.parse(markdown);
document.getElementById("conteudo").innerHTML = html;
for (const bloco of document.querySelectorAll("pre code.language-mermaid")) {{
    const diagrama = document.createElement("div");
    diagrama.className = "mermaid";
    diagrama.textContent = bloco.textContent;
    bloco.parentElement.replaceWith(diagrama);
}}
mermaid.initialize({{ startOnLoad: true, securityLevel: "loose" }});
mermaid.run();
</script>
</body>
</html>"""
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            suffix=".html",
            prefix="radar_readme_",
            delete=False,
        ) as arquivo:
            arquivo.write(html)
            webbrowser.open(Path(arquivo.name).as_uri())


class JanelaSobre:
    """Exibe o objetivo do sistema e os dados do autor."""

    def __init__(self, janela_pai):
        self.janela = tk.Toplevel(janela_pai)
        self.janela.title("Sobre o Radar das Licitações")
        self.janela.geometry("620x360")
        self.janela.resizable(False, False)
        self.janela.transient(janela_pai)

        quadro = ttk.Frame(self.janela, padding=20)
        quadro.pack(fill="both", expand=True)
        ttk.Label(
            quadro,
            text="Radar das Licitações",
            font=("Segoe UI", 18, "bold"),
        ).pack(anchor="w", pady=(0, 12))
        texto = (
            "Sistema para descoberta, download e rastreabilidade de dados públicos "
            "de compras governamentais. O objetivo é preservar os arquivos de origem, "
            "registrar sua procedência e preparar uma base confiável para análises "
            "de preços, fornecedores e processos licitatórios.\n\n"
            "Autor e responsável técnico:\n"
            "Marcio Welb de Aguiar Silveira\n\n"
            "Senior Software Engineer | Digital Banking, Credit Platforms & "
            "E-Government | Clean Architecture, DDD, SAGA, Event-Driven | "
            "AI-First | .NET & Python | Aikido Sensei\n\n"
            "marciowelb@outlook.com.br\n"
            "55 (11) 98137-0755"
        )
        ttk.Label(quadro, text=texto, justify="left", wraplength=570).pack(anchor="w")
        ttk.Button(quadro, text="Fechar", command=self.janela.destroy).pack(
            anchor="e", pady=(20, 0)
        )
