import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sqlite3
import json
import re
from datetime import datetime, date, timedelta
from faker import Faker


BANCO = "tarefas.db"

fake = Faker("pt_BR")


# ============================================================
# PALETA
# ============================================================

FUNDO = "#F6F3EF"
CREME = "#FBF9F6"
BRANCO = "#FFFFFF"

VINHO = "#542536"
VINHO_ESCURO = "#351722"
VINHO_CLARO = "#7A4056"

DOURADO = "#DCB376"
DOURADO_CLARO = "#E8D7B8"

# Tons usados somente nas fitas decorativas
DOURADO_FITA = "#C99745"
DOURADO_FITA_CLARO = "#F0D18E"
DOURADO_FITA_LUZ = "#F8E2AE"
DOURADO_FITA_SOMBRA = "#8E642E"

TEXTO = "#29242A"
TEXTO_SECUNDARIO = "#81767D"
BORDA = "#E7E0DA"

VERDE = "#43866A"
VERDE_CLARO = "#E8F3ED"

VERMELHO = "#A84D59"
VERMELHO_CLARO = "#F8E8EB"

LARANJA = "#B5793D"
LARANJA_CLARO = "#FAEEDB"

ROXO = "#76658A"
ROXO_CLARO = "#EEE9F2"


# ============================================================
# BANCO DE DADOS
# ============================================================

def conectar():
    return sqlite3.connect(BANCO)


def criar_banco():
    con = conectar()
    cur = con.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS tarefas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            texto_original TEXT NOT NULL,
            titulo TEXT NOT NULL,
            responsavel TEXT NOT NULL,
            prazo TEXT NOT NULL,
            prioridade TEXT NOT NULL,
            categoria TEXT NOT NULL,
            status TEXT NOT NULL,
            criada_em TEXT NOT NULL
        )
    """)

    con.commit()
    con.close()


# ============================================================
# IDENTIFICAÇÃO DO RESPONSÁVEL
# ============================================================

def identificar_responsavel(texto):

    texto = " ".join(texto.split())

    padroes = [
        r"\brespons[aá]vel\s*(?:é|e|:|-)?\s*(?:o|a)?\s*([A-Za-zÀ-ÿ]+)",
        r"\bpreciso\s+que\s+(?:o|a)?\s*([A-Za-zÀ-ÿ]+)\s+(?:faça|faca|fazer)\b",
        r"\bquero\s+que\s+(?:o|a)?\s*([A-Za-zÀ-ÿ]+)\s+(?:faça|faca|fazer)\b",
        r"\b(?:o|a)\s+([A-Za-zÀ-ÿ]+)\s+(?:precisa|deve|vai|irá|ira|fica|ficará|ficara)\b",
        r"\b([A-Za-zÀ-ÿ]+)\s+(?:precisa|deve|vai|irá|ira|fica|ficará|ficara)\b",
        r"\btarefa\s+para\s+(?:o|a)?\s*([A-Za-zÀ-ÿ]+)",
        r"\bpara\s*:\s*([A-Za-zÀ-ÿ]+)",
        r"\bé\s+para\s+(?:o|a)?\s*([A-Za-zÀ-ÿ]+)"
    ]

    proibidas = {
        "fazer", "faça", "faca", "precisa", "deve", "vai",
        "entregar", "enviar", "realizar", "preparar", "criar",
        "organizar", "finalizar", "relatório", "relatorio",
        "documento", "planilha", "arquivo", "projeto", "tarefa",
        "cliente", "reunião", "reuniao", "pagamento", "sistema",
        "código", "codigo", "hoje", "amanhã", "amanha", "sexta",
        "segunda", "terça", "terca", "quarta", "quinta", "sábado",
        "sabado", "domingo", "urgente", "importante", "até", "ate",
        "para", "com", "de", "do", "da"
    }

    for padrao in padroes:

        resultado = re.search(
            padrao,
            texto,
            re.IGNORECASE
        )

        if resultado:

            nome = resultado.group(1).strip()

            if nome.lower() not in proibidas:
                return nome.title()

    return "Não definido"


# ============================================================
# IDENTIFICAÇÃO DO PRAZO
# ============================================================

def identificar_prazo(texto):

    texto = texto.lower()
    hoje = date.today()

    if re.search(r"\bhoje\b", texto):
        return hoje.strftime("%d/%m/%Y")

    if re.search(r"\bamanh[ãa]\b", texto):
        return (
            hoje + timedelta(days=1)
        ).strftime("%d/%m/%Y")

    resultado = re.search(
        r"\b(\d{1,2})[/-](\d{1,2})[/-](\d{4})\b",
        texto
    )

    if resultado:

        try:

            data = date(
                int(resultado.group(3)),
                int(resultado.group(2)),
                int(resultado.group(1))
            )

            return data.strftime("%d/%m/%Y")

        except ValueError:

            return "Data inválida"

    resultado = re.search(
        r"\b(\d{1,2})[/-](\d{1,2})\b",
        texto
    )

    if resultado:

        dia = int(resultado.group(1))
        mes = int(resultado.group(2))

        try:

            data = date(
                hoje.year,
                mes,
                dia
            )

            if data < hoje:

                data = date(
                    hoje.year + 1,
                    mes,
                    dia
                )

            return data.strftime("%d/%m/%Y")

        except ValueError:

            return "Data inválida"

    resultado = re.search(
        r"\b(?:até|ate)\s+(?:o\s+)?dia\s+(\d{1,2})",
        texto
    )

    if resultado:

        dia = int(resultado.group(1))

        try:

            data = date(
                hoje.year,
                hoje.month,
                dia
            )

            if data < hoje:

                if hoje.month == 12:

                    data = date(
                        hoje.year + 1,
                        1,
                        dia
                    )

                else:

                    data = date(
                        hoje.year,
                        hoje.month + 1,
                        dia
                    )

            return data.strftime("%d/%m/%Y")

        except ValueError:

            return "Data inválida"

    dias = {

        "segunda": 0,
        "terça": 1,
        "terca": 1,
        "quarta": 2,
        "quinta": 3,
        "sexta": 4,
        "sábado": 5,
        "sabado": 5,
        "domingo": 6

    }

    for nome, numero in dias.items():

        if re.search(

            r"\b(?:até|ate|na|no|para|nesta|neste|"
            r"próxima|proxima|próximo|proximo)?\s*" +
            re.escape(nome),

            texto

        ):

            diferenca = (
                numero - hoje.weekday()
            ) % 7

            if diferenca == 0:
                diferenca = 7

            data = hoje + timedelta(
                days=diferenca
            )

            return data.strftime("%d/%m/%Y")

    meses = {

        "janeiro": 1,
        "fevereiro": 2,
        "março": 3,
        "marco": 3,
        "abril": 4,
        "maio": 5,
        "junho": 6,
        "julho": 7,
        "agosto": 8,
        "setembro": 9,
        "outubro": 10,
        "novembro": 11,
        "dezembro": 12

    }

    for nome, numero in meses.items():

        resultado = re.search(

            rf"\b(?:dia\s+)?(\d{{1,2}})\s+de\s+{nome}\b",

            texto

        )

        if resultado:

            try:

                dia = int(resultado.group(1))

                data = date(
                    hoje.year,
                    numero,
                    dia
                )

                if data < hoje:

                    data = date(
                        hoje.year + 1,
                        numero,
                        dia
                    )

                return data.strftime("%d/%m/%Y")

            except ValueError:

                return "Data inválida"

    return "Não definido"


# ============================================================
# PRIORIDADE
# ============================================================

def identificar_prioridade(texto):

    texto = texto.lower()

    alta = [
        "urgente",
        "urgência",
        "urgencia",
        "imediato",
        "imediatamente",
        "agora",
        "crítico",
        "critico",
        "pra ontem",
        "o quanto antes"
    ]

    media = [
        "importante",
        "prioridade",
        "atenção",
        "atencao"
    ]

    if any(p in texto for p in alta):
        return "ALTA"

    if any(p in texto for p in media):
        return "MÉDIA"

    return "BAIXA"


# ============================================================
# CATEGORIA
# ============================================================

def identificar_categoria(texto):

    texto = texto.lower()

    if any(p in texto for p in [
        "relatório",
        "relatorio",
        "documento",
        "planilha",
        "arquivo",
        "pdf"
    ]):

        return "DOCUMENTOS"

    if any(p in texto for p in [
        "reunião",
        "reuniao",
        "call",
        "meeting",
        "encontro"
    ]):

        return "REUNIÃO"

    if any(p in texto for p in [
        "cliente",
        "venda",
        "vendas",
        "proposta"
    ]):

        return "CLIENTE / VENDAS"

    if any(p in texto for p in [
        "pagamento",
        "cobrança",
        "cobranca",
        "financeiro",
        "dinheiro"
    ]):

        return "FINANCEIRO"

    if any(p in texto for p in [
        "programar",
        "programação",
        "programacao",
        "código",
        "codigo",
        "sistema",
        "software",
        "computador"
    ]):

        return "TECNOLOGIA"

    return "GERAL"


# ============================================================
# TÍTULO
# ============================================================

def criar_titulo(texto):

    titulo = texto.strip()

    for inicio in [
        "preciso que",
        "precisamos que",
        "por favor",
        "favor",
        "quero que"
    ]:

        if titulo.lower().startswith(inicio):

            titulo = titulo[
                len(inicio):
            ].strip()

    titulo = titulo.rstrip(".!?")

    if len(titulo) > 75:
        titulo = titulo[:75] + "..."

    return titulo


# ============================================================
# INTERPRETAR
# ============================================================

def interpretar(texto):

    return {

        "texto_original": texto,

        "titulo": criar_titulo(texto),

        "responsavel": identificar_responsavel(texto),

        "prazo": identificar_prazo(texto),

        "prioridade": identificar_prioridade(texto),

        "categoria": identificar_categoria(texto),

        "status": "PENDENTE",

        "criada_em":
            datetime.now().strftime(
                "%d/%m/%Y %H:%M"
            )

    }


# ============================================================
# INSERIR
# ============================================================

def inserir(tarefa):

    con = conectar()
    cur = con.cursor()

    cur.execute("""

        INSERT INTO tarefas
        (
            texto_original,
            titulo,
            responsavel,
            prazo,
            prioridade,
            categoria,
            status,
            criada_em
        )

        VALUES (?, ?, ?, ?, ?, ?, ?, ?)

    """, (

        tarefa["texto_original"],
        tarefa["titulo"],
        tarefa["responsavel"],
        tarefa["prazo"],
        tarefa["prioridade"],
        tarefa["categoria"],
        tarefa["status"],
        tarefa["criada_em"]

    ))

    con.commit()
    con.close()


# ============================================================
# BUSCAR
# ============================================================

def buscar():

    con = conectar()
    cur = con.cursor()

    cur.execute("""

        SELECT
            id,
            titulo,
            responsavel,
            prazo,
            prioridade,
            categoria,
            status,
            criada_em

        FROM tarefas

        ORDER BY id DESC

    """)

    dados = cur.fetchall()

    con.close()

    return dados


# ============================================================
# ESTATÍSTICAS
# ============================================================

def estatisticas():

    con = conectar()
    cur = con.cursor()

    cur.execute(
        "SELECT COUNT(*) FROM tarefas"
    )

    total = cur.fetchone()[0]

    cur.execute("""

        SELECT COUNT(*)
        FROM tarefas
        WHERE status = 'PENDENTE'

    """)

    pendentes = cur.fetchone()[0]

    cur.execute("""

        SELECT COUNT(*)
        FROM tarefas
        WHERE status = 'CONCLUÍDA'

    """)

    concluidas = cur.fetchone()[0]

    cur.execute("""

        SELECT COUNT(*)
        FROM tarefas
        WHERE prioridade = 'ALTA'

    """)

    urgentes = cur.fetchone()[0]

    con.close()

    return (
        total,
        pendentes,
        concluidas,
        urgentes
    )


# ============================================================
# APLICAÇÃO
# ============================================================

class Aplicativo(tk.Tk):

    def __init__(self):

        super().__init__()

        self.title(
            "Caixa de Entrada → Ação"
        )

        self.geometry("1360x820")

        self.minsize(
            1100,
            700
        )

        self.configure(
            bg=FUNDO
        )

        self.pagina_atual = None

        self.configurar_estilo()

        self.criar_interface()

        self.atualizar_tudo()


    # ========================================================
    # FITAS DOURADAS CURVAS
    # ========================================================

    def criar_fitas_curvas(
        self,
        pai,
        bg=VINHO_ESCURO,
        largura=255,
        altura=125
    ):

        canvas = tk.Canvas(
            pai,
            width=largura,
            height=altura,
            bg=bg,
            highlightthickness=0,
            bd=0
        )

        canvas.pack(
            fill="both",
            expand=True
        )

        # ----------------------------------------------------
        # SOMBRA DA FITA
        # ----------------------------------------------------

        canvas.create_line(
            -35, 88,
            15, 78,
            55, 81,
            92, 96,
            126, 113,
            157, 119,
            188, 112,
            218, 94,
            252, 71,
            285, 59,
            315, 62,
            350, 78,
            385, 102,
            425, 120,
            465, 123,
            510, 111,
            550, 89,
            590, 70,
            fill=DOURADO_FITA_SOMBRA,
            width=6,
            smooth=True
        )

        # ----------------------------------------------------
        # FITA PRINCIPAL
        # ----------------------------------------------------

        canvas.create_line(
            -35, 82,
            15, 72,
            55, 75,
            92, 90,
            126, 107,
            157, 113,
            188, 106,
            218, 88,
            252, 65,
            285, 53,
            315, 56,
            350, 72,
            385, 96,
            425, 114,
            465, 117,
            510, 105,
            550, 83,
            590, 64,
            fill=DOURADO_FITA,
            width=5,
            smooth=True
        )

        # ----------------------------------------------------
        # BRILHO DA FITA
        # ----------------------------------------------------

        canvas.create_line(
            -30, 79,
            15, 69,
            55, 72,
            91, 87,
            126, 104,
            157, 110,
            188, 103,
            218, 85,
            252, 62,
            285, 50,
            315, 53,
            350, 69,
            385, 93,
            425, 111,
            465, 114,
            510, 102,
            550, 80,
            590, 61,
            fill=DOURADO_FITA_CLARO,
            width=2,
            smooth=True
        )

        # ----------------------------------------------------
        # SEGUNDA FITA, MAIS FINA
        # ----------------------------------------------------

        canvas.create_line(
            -30, 103,
            20, 93,
            58, 96,
            95, 109,
            128, 121,
            158, 124,
            190, 118,
            220, 102,
            253, 81,
            285, 70,
            316, 73,
            350, 88,
            385, 108,
            424, 123,
            466, 126,
            510, 116,
            552, 96,
            592, 79,
            fill=DOURADO_FITA_CLARO,
            width=2,
            smooth=True
        )

        # ----------------------------------------------------
        # PEQUENOS REFLEXOS
        # ----------------------------------------------------

        canvas.create_line(
            224, 85,
            253, 65,
            285, 54,
            fill=DOURADO_FITA_LUZ,
            width=1,
            smooth=True
        )

        return canvas


    def fita_dourada(
        self,
        pai,
        lado="top",
        margem=0,
        espessura=1,
        cor=DOURADO
    ):

        fita = tk.Frame(
            pai,
            bg=cor,
            height=espessura
        )

        if lado == "top":

            fita.pack(
                side="top",
                fill="x",
                padx=margem
            )

        elif lado == "bottom":

            fita.pack(
                side="bottom",
                fill="x",
                padx=margem
            )

        return fita


    def ornamento_dourado(
        self,
        pai,
        bg,
        largura=70
    ):

        area = tk.Frame(
            pai,
            bg=bg,
            height=8
        )

        area.pack_propagate(False)

        canvas = tk.Canvas(
            area,
            width=largura,
            height=8,
            bg=bg,
            highlightthickness=0,
            bd=0
        )

        canvas.pack()

        centro = largura // 2

        canvas.create_line(
            0,
            4,
            centro - 7,
            4,
            fill=DOURADO,
            width=1
        )

        canvas.create_oval(
            centro - 3,
            1,
            centro + 3,
            7,
            outline=DOURADO,
            width=1
        )

        canvas.create_line(
            centro + 7,
            4,
            largura,
            4,
            fill=DOURADO,
            width=1
        )

        return area


    # ========================================================
    # ESTILO
    # ========================================================

    def configurar_estilo(self):

        style = ttk.Style()

        style.theme_use("clam")

        style.configure(
            "Treeview",
            background=BRANCO,
            fieldbackground=BRANCO,
            foreground=TEXTO,
            rowheight=44,
            borderwidth=0,
            font=("Segoe UI", 10)
        )

        style.configure(
            "Treeview.Heading",
            background=CREME,
            foreground=TEXTO_SECUNDARIO,
            font=(
                "Segoe UI",
                9,
                "bold"
            ),
            relief="flat"
        )

        style.map(
            "Treeview",
            background=[
                ("selected", "#EFE7EB")
            ],
            foreground=[
                ("selected", TEXTO)
            ]
        )


    # ========================================================
    # INTERFACE
    # ========================================================

    def criar_interface(self):

        self.sidebar = tk.Frame(
            self,
            bg=VINHO_ESCURO,
            width=255
        )

        self.sidebar.pack(
            side="left",
            fill="y"
        )

        self.sidebar.pack_propagate(False)


        # ----------------------------------------------------
        # FILETE DOURADO SUPERIOR
        # ----------------------------------------------------

        self.fita_dourada(
            self.sidebar,
            "top",
            0,
            2
        )


        logo_area = tk.Frame(
            self.sidebar,
            bg=VINHO_ESCURO
        )

        logo_area.pack(
            fill="x",
            padx=28,
            pady=(35, 40)
        )


        tk.Label(
            logo_area,
            text="B",
            font=(
                "Edwardian Script ITC",
                34,
                "bold"
            ),
            fg=DOURADO,
            bg=VINHO_ESCURO
        ).pack(
            anchor="w"
        )


        tk.Label(
            logo_area,
            text="CAIXA DE ENTRADA",
            font=(
                "Segoe UI",
                10,
                "bold"
            ),
            fg=BRANCO,
            bg=VINHO_ESCURO
        ).pack(
            anchor="w",
            pady=(5, 0)
        )


        tk.Label(
            logo_area,
            text="AÇÃO",
            font=(
                "Georgia",
                9
            ),
            fg=DOURADO,
            bg=VINHO_ESCURO
        ).pack(
            anchor="w"
        )


        self.ornamento_dourado(
            logo_area,
            VINHO_ESCURO,
            105
        ).pack(
            anchor="w",
            pady=(12, 0)
        )


        self.criar_menu(
            "⌂   VISÃO GERAL",
            self.mostrar_dashboard
        )

        self.criar_menu(
            "＋   NOVA SOLICITAÇÃO",
            self.mostrar_nova
        )

        self.criar_menu(
            "☷   MINHAS TAREFAS",
            self.mostrar_tarefas
        )

        self.criar_menu(
            "⇅   DADOS ",
            self.mostrar_dados
        )


        # ----------------------------------------------------
        # ÁREA DAS FITAS CURVAS
        # ----------------------------------------------------

        decoracao = tk.Frame(
            self.sidebar,
            bg=VINHO_ESCURO,
            height=125
        )

        decoracao.pack(
            side="bottom",
            fill="x"
        )

        decoracao.pack_propagate(False)

        self.criar_fitas_curvas(
            decoracao,
            VINHO_ESCURO,
            255,
            125
        )


        # ----------------------------------------------------
        # RODAPÉ
        # ----------------------------------------------------

        rodape = tk.Frame(
            self.sidebar,
            bg=VINHO_ESCURO
        )

        rodape.pack(
            side="bottom",
            fill="x",
            padx=25,
            pady=20
        )


        self.fita_dourada(
            rodape,
            "top",
            0,
            1
        )


        self.fita_dourada(
            rodape,
            "top",
            0,
            1
        ).pack(
            fill="x",
            pady=(3, 14)
        )


        tk.Label(
            rodape,
            text="AUTOMAÇÃO INTELIGENTE",
            font=(
                "Segoe UI",
                8,
                "bold"
            ),
            fg=DOURADO,
            bg=VINHO_ESCURO
        ).pack(
            anchor="w"
        )


        tk.Label(
            rodape,
        
            font=(
                "Segoe UI",
                8
            ),
            fg="#B8AAB0",
            bg=VINHO_ESCURO,
            justify="left"
        ).pack(
            anchor="w",
            pady=(5, 0)
        )


        self.conteudo = tk.Frame(
            self,
            bg=FUNDO
        )

        self.conteudo.pack(
            side="left",
            fill="both",
            expand=True
        )


        self.criar_cabecalho()


        self.container = tk.Frame(
            self.conteudo,
            bg=FUNDO
        )

        self.container.pack(
            fill="both",
            expand=True
        )


        self.mostrar_dashboard()


    # ========================================================
    # MENU
    # ========================================================

    def criar_menu(
        self,
        texto,
        comando
    ):

        botao = tk.Button(
            self.sidebar,
            text=texto,
            command=comando,
            font=(
                "Segoe UI",
                9,
                "bold"
            ),
            fg="#CFC3C8",
            bg=VINHO_ESCURO,
            activebackground=VINHO,
            activeforeground=BRANCO,
            relief="flat",
            bd=0,
            anchor="w",
            padx=28,
            pady=15,
            cursor="hand2"
        )

        botao.pack(
            fill="x",
            padx=12,
            pady=2
        )

        return botao


    # ========================================================
    # CABEÇALHO
    # ========================================================

    def criar_cabecalho(self):

        topo = tk.Frame(
            self.conteudo,
            bg=FUNDO
        )

        topo.pack(
            fill="x",
            padx=42,
            pady=(35, 15)
        )


        esquerda = tk.Frame(
            topo,
            bg=FUNDO
        )

        esquerda.pack(
            side="left"
        )


        self.titulo = tk.Label(
            esquerda,
            text="Visão geral",
            font=(
                "Georgia",
                26,
                "bold"
            ),
            fg=TEXTO,
            bg=FUNDO
        )

        self.titulo.pack(
            anchor="w"
        )


        self.subtitulo = tk.Label(
            esquerda,
            text=(
                "Seu espaço para transformar "
                "solicitações em ação."
            ),
            font=(
                "Segoe UI",
                10
            ),
            fg=TEXTO_SECUNDARIO,
            bg=FUNDO
        )

        self.subtitulo.pack(
            anchor="w",
            pady=(5, 0)
        )


        self.fita_dourada(
            esquerda,
            "top",
            0,
            1
        ).pack(
            fill="x",
            pady=(12, 0)
        )


        direita = tk.Frame(
            topo,
            bg=FUNDO
        )

        direita.pack(
            side="right"
        )


        hoje = datetime.now().strftime(
            "%d de %B de %Y"
        ).replace(
            "September",
            "setembro"
        )


        tk.Label(
            direita,
            text="HOJE",
            font=(
                "Segoe UI",
                8,
                "bold"
            ),
            fg=DOURADO,
            bg=FUNDO
        ).pack(
            anchor="e"
        )


        tk.Label(
            direita,
            text=hoje,
            font=(
                "Segoe UI",
                10
            ),
            fg=TEXTO_SECUNDARIO,
            bg=FUNDO
        ).pack(
            anchor="e"
        )


    # ========================================================
    # LIMPAR
    # ========================================================

    def limpar_container(self):

        for widget in self.container.winfo_children():
            widget.destroy()


    # ========================================================
    # DASHBOARD
    # ========================================================

    def mostrar_dashboard(self):

        self.pagina_atual = "dashboard"

        self.limpar_container()

        self.titulo.config(
            text="Visão geral"
        )

        self.subtitulo.config(
            text=(
                "Seu espaço para transformar "
                "solicitações em ação."
            )
        )


        total, pendentes, concluidas, urgentes = estatisticas()


        cards = tk.Frame(
            self.container,
            bg=FUNDO
        )

        cards.pack(
            fill="x",
            padx=42
        )


        self.criar_stat_card(
            cards,
            "TAREFAS",
            total,
            "Total cadastradas",
            DOURADO
        )


        self.criar_stat_card(
            cards,
            "PENDENTES",
            pendentes,
            "Aguardando ação",
            VINHO_CLARO
        )


        self.criar_stat_card(
            cards,
            "CONCLUÍDAS",
            concluidas,
            "Finalizadas",
            VERDE
        )


        self.criar_stat_card(
            cards,
            "URGENTES",
            urgentes,
            "Alta prioridade",
            VERMELHO
        )


        inferior = tk.Frame(
            self.container,
            bg=FUNDO
        )

        inferior.pack(
            fill="both",
            expand=True,
            padx=42,
            pady=25
        )


        # ====================================================
        # CARD VINHO
        # ====================================================

        card_entrada = tk.Frame(
            inferior,
            bg=VINHO_ESCURO
        )

        card_entrada.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(0, 12)
        )


        self.fita_dourada(
            card_entrada,
            "top",
            0,
            3
        )


        self.fita_dourada(
            card_entrada,
            "top",
            18,
            1
        )


        tk.Label(
            card_entrada,
            text="NOVA SOLICITAÇÃO",
            font=(
                "Segoe UI",
                8,
                "bold"
            ),
            fg=DOURADO,
            bg=VINHO_ESCURO
        ).pack(
            anchor="w",
            padx=28,
            pady=(28, 5)
        )


        tk.Label(
            card_entrada,
            text=(
                "Transforme uma frase\n"
                "em uma tarefa organizada."
            ),
            font=(
                "Georgia",
                21,
                "bold"
            ),
            fg=BRANCO,
            bg=VINHO_ESCURO,
            justify="left"
        ).pack(
            anchor="w",
            padx=28
        )


        tk.Label(
            card_entrada,
            text=(
                "Escreva do seu jeito. O sistema identifica "
                "automaticamente as informações importantes."
            ),
            font=(
                "Segoe UI",
                9
            ),
            fg="#C9BBC1",
            bg=VINHO_ESCURO,
            wraplength=420,
            justify="left"
        ).pack(
            anchor="w",
            padx=28,
            pady=(12, 18)
        )


        self.dashboard_texto = tk.Text(
            card_entrada,
            height=5,
            font=(
                "Segoe UI",
                10
            ),
            bg="#4A2534",
            fg=BRANCO,
            insertbackground=BRANCO,
            relief="flat",
            bd=0,
            wrap="word",
            padx=15,
            pady=12
        )

        self.dashboard_texto.pack(
            fill="x",
            padx=28
        )


        campo_linha = tk.Frame(
            card_entrada,
            bg=DOURADO,
            height=1
        )

        campo_linha.pack(
            fill="x",
            padx=28
        )


        self.dashboard_texto.insert(
            "1.0",
            " A Beatriz precisa enviar a proposta ao cliente até sexta. É urgente."
        )


        tk.Button(
            card_entrada,
            text="ANALISAR E CRIAR  →",
            command=self.criar_pelo_dashboard,
            bg=DOURADO,
            fg=VINHO_ESCURO,
            activebackground="#D0B27E",
            relief="flat",
            bd=0,
            font=(
                "Segoe UI",
                9,
                "bold"
            ),
            cursor="hand2",
            padx=20,
            pady=11
        ).pack(
            anchor="w",
            padx=28,
            pady=20
        )


        # ====================================================
        # CARD ATIVIDADE
        # ====================================================

        card_lista = tk.Frame(
            inferior,
            bg=BRANCO,
            highlightbackground=BORDA,
            highlightthickness=1
        )

        card_lista.pack(
            side="right",
            fill="both",
            expand=True,
            padx=(12, 0)
        )


        self.fita_dourada(
            card_lista,
            "top",
            0,
            2
        )


        tk.Label(
            card_lista,
            text="ATIVIDADE RECENTE",
            font=(
                "Segoe UI",
                8,
                "bold"
            ),
            fg=DOURADO,
            bg=BRANCO
        ).pack(
            anchor="w",
            padx=25,
            pady=(25, 3)
        )


        tk.Label(
            card_lista,
            text="Últimas tarefas",
            font=(
                "Georgia",
                18,
                "bold"
            ),
            fg=TEXTO,
            bg=BRANCO
        ).pack(
            anchor="w",
            padx=25
        )


        self.ornamento_dourado(
            card_lista,
            BRANCO,
            80
        ).pack(
            anchor="w",
            padx=25,
            pady=(8, 5)
        )


        tarefas = buscar()[:5]


        if not tarefas:

            tk.Label(
                card_lista,
                text="Nenhuma tarefa cadastrada ainda.",
                font=(
                    "Segoe UI",
                    10
                ),
                fg=TEXTO_SECUNDARIO,
                bg=BRANCO
            ).pack(
                pady=45
            )

        else:

            for tarefa in tarefas:

                linha = tk.Frame(
                    card_lista,
                    bg=BRANCO
                )

                linha.pack(
                    fill="x",
                    padx=25,
                    pady=9
                )


                tk.Frame(
                    linha,
                    bg=(
                        VERMELHO
                        if tarefa[4] == "ALTA"
                        else DOURADO
                        if tarefa[4] == "MÉDIA"
                        else VERDE
                    ),
                    width=4
                ).pack(
                    side="left",
                    fill="y",
                    padx=(0, 12)
                )


                info = tk.Frame(
                    linha,
                    bg=BRANCO
                )

                info.pack(
                    side="left",
                    fill="x",
                    expand=True
                )


                tk.Label(
                    info,
                    text=tarefa[1],
                    font=(
                        "Segoe UI",
                        9,
                        "bold"
                    ),
                    fg=TEXTO,
                    bg=BRANCO,
                    anchor="w"
                ).pack(
                    fill="x"
                )


                tk.Label(
                    info,
                    text=f"{tarefa[2]}  •  {tarefa[3]}",
                    font=(
                        "Segoe UI",
                        8
                    ),
                    fg=TEXTO_SECUNDARIO,
                    bg=BRANCO,
                    anchor="w"
                ).pack(
                    fill="x",
                    pady=(3, 0)
                )


        tk.Button(
            card_lista,
            text="VER TODAS AS TAREFAS  →",
            command=self.mostrar_tarefas,
            bg=BRANCO,
            fg=VINHO,
            activebackground=CREME,
            relief="flat",
            bd=0,
            font=(
                "Segoe UI",
                8,
                "bold"
            ),
            cursor="hand2"
        ).pack(
            anchor="w",
            padx=25,
            pady=15
        )


    # ========================================================
    # CARDS DE ESTATÍSTICA
    # ========================================================

    def criar_stat_card(
        self,
        pai,
        titulo,
        valor,
        descricao,
        detalhe
    ):

        card = tk.Frame(
            pai,
            bg=BRANCO,
            highlightbackground=BORDA,
            highlightthickness=1
        )

        card.pack(
            side="left",
            fill="both",
            expand=True,
            padx=5
        )


        tk.Frame(
            card,
            bg=detalhe,
            width=5
        ).pack(
            side="left",
            fill="y"
        )


        self.fita_dourada(
            card,
            "top",
            0,
            2
        )


        corpo = tk.Frame(
            card,
            bg=BRANCO
        )

        corpo.pack(
            fill="both",
            expand=True,
            padx=18,
            pady=17
        )


        tk.Label(
            corpo,
            text=titulo,
            font=(
                "Segoe UI",
                8,
                "bold"
            ),
            fg=TEXTO_SECUNDARIO,
            bg=BRANCO
        ).pack(
            anchor="w"
        )


        tk.Label(
            corpo,
            text=str(valor),
            font=(
                "Georgia",
                25,
                "bold"
            ),
            fg=TEXTO,
            bg=BRANCO
        ).pack(
            anchor="w",
            pady=(3, 0)
        )


        tk.Label(
            corpo,
            text=descricao,
            font=(
                "Segoe UI",
                8
            ),
            fg=TEXTO_SECUNDARIO,
            bg=BRANCO
        ).pack(
            anchor="w"
        )


    # ========================================================
    # NOVA SOLICITAÇÃO
    # ========================================================

    def mostrar_nova(self):

        self.pagina_atual = "nova"

        self.limpar_container()

        self.titulo.config(
            text="Nova solicitação"
        )

        self.subtitulo.config(
            text="Descreva o que precisa ser feito."
        )


        card = tk.Frame(
            self.container,
            bg=BRANCO,
            highlightbackground=BORDA,
            highlightthickness=1
        )

        card.pack(
            fill="both",
            expand=True,
            padx=42,
            pady=10
        )


        self.fita_dourada(
            card,
            "top",
            0,
            2
        )


        self.fita_dourada(
            card,
            "top",
            30,
            1
        )


        tk.Label(
            card,
            text="DESCREVA A TAREFA",
            font=(
                "Segoe UI",
                8,
                "bold"
            ),
            fg=DOURADO,
            bg=BRANCO
        ).pack(
            anchor="w",
            padx=35,
            pady=(35, 5)
        )


        tk.Label(
            card,
            text="O que precisa acontecer?",
            font=(
                "Georgia",
                23,
                "bold"
            ),
            fg=TEXTO,
            bg=BRANCO
        ).pack(
            anchor="w",
            padx=35
        )


        tk.Label(
            card,
            text=(
                "Não precisa preencher vários campos. "
                "Escreva uma frase normalmente."
            ),
            font=(
                "Segoe UI",
                10
            ),
            fg=TEXTO_SECUNDARIO,
            bg=BRANCO
        ).pack(
            anchor="w",
            padx=35,
            pady=(5, 20)
        )


        self.campo_nova = tk.Text(
            card,
            height=9,
            font=(
                "Segoe UI",
                12
            ),
            bg=CREME,
            fg=TEXTO,
            insertbackground=TEXTO,
            relief="flat",
            bd=0,
            wrap="word",
            padx=18,
            pady=15
        )

        self.campo_nova.pack(
            fill="x",
            padx=35
        )


        self.fita_dourada(
            card,
            "top",
            35,
            1
        )


        self.campo_nova.insert(
            "1.0",
            "O Ivan precisa preparar o relatório para o cliente até sexta. É urgente."
        )


        exemplo = tk.Frame(
            card,
            bg=CREME
        )

        exemplo.pack(
            fill="x",
            padx=35,
            pady=20
        )


        tk.Label(
            exemplo,
            text="DICA",
            font=(
                "Segoe UI",
                8,
                "bold"
            ),
            fg=DOURADO,
            bg=CREME
        ).pack(
            side="left",
            padx=15,
            pady=13
        )


        tk.Label(
            exemplo,
            text=(
                "Você pode escrever o nome, prazo "
                "e prioridade na mesma frase."
            ),
            font=(
                "Segoe UI",
                9
            ),
            fg=TEXTO_SECUNDARIO,
            bg=CREME
        ).pack(
            side="left"
        )


        tk.Button(
            card,
            text="CRIAR TAREFA  →",
            command=self.criar_tarefa_nova,
            bg=VINHO,
            fg=BRANCO,
            activebackground=VINHO_CLARO,
            relief="flat",
            bd=0,
            font=(
                "Segoe UI",
                9,
                "bold"
            ),
            cursor="hand2",
            padx=25,
            pady=13
        ).pack(
            anchor="w",
            padx=35
        )


    # ========================================================
    # CRIAR TAREFA NOVA
    # ========================================================

    def criar_tarefa_nova(self):

        texto = self.campo_nova.get(
            "1.0",
            tk.END
        ).strip()

        if not texto:

            messagebox.showwarning(
                "Atenção",
                "Digite uma solicitação."
            )

            return

        tarefa = interpretar(texto)

        inserir(tarefa)

        self.mostrar_confirmacao(tarefa)


    # ========================================================
    # CRIAR PELO DASHBOARD
    # ========================================================

    def criar_pelo_dashboard(self):

        texto = self.dashboard_texto.get(
            "1.0",
            tk.END
        ).strip()

        if not texto:

            messagebox.showwarning(
                "Atenção",
                "Digite uma solicitação."
            )

            return

        tarefa = interpretar(texto)

        inserir(tarefa)

        self.mostrar_confirmacao(tarefa)


    # ========================================================
    # CONFIRMAÇÃO
    # ========================================================

    def mostrar_confirmacao(self, tarefa):

        janela = tk.Toplevel(self)

        janela.title("Tarefa criada")

        janela.geometry("520x520")

        janela.configure(
            bg=BRANCO
        )

        janela.resizable(
            False,
            False
        )


        self.fita_dourada(
            janela,
            "top",
            0,
            3
        )


        tk.Label(
            janela,
            text="✓",
            font=(
                "Georgia",
                42,
                "bold"
            ),
            fg=DOURADO,
            bg=BRANCO
        ).pack(
            pady=(25, 0)
        )


        tk.Label(
            janela,
            text="Tudo organizado.",
            font=(
                "Georgia",
                22,
                "bold"
            ),
            fg=TEXTO,
            bg=BRANCO
        ).pack()


        tk.Label(
            janela,
            text=(
                "A solicitação foi transformada "
                "em uma tarefa."
            ),
            font=(
                "Segoe UI",
                9
            ),
            fg=TEXTO_SECUNDARIO,
            bg=BRANCO
        ).pack(
            pady=(5, 20)
        )


        self.ornamento_dourado(
            janela,
            BRANCO,
            100
        ).pack(
            pady=(0, 8)
        )


        dados = [
            (
                "RESPONSÁVEL",
                tarefa["responsavel"]
            ),
            (
                "PRAZO",
                tarefa["prazo"]
            ),
            (
                "PRIORIDADE",
                tarefa["prioridade"]
            ),
            (
                "CATEGORIA",
                tarefa["categoria"]
            )
        ]


        for nome, valor in dados:

            linha = tk.Frame(
                janela,
                bg=CREME
            )

            linha.pack(
                fill="x",
                padx=45,
                pady=4
            )


            tk.Label(
                linha,
                text=nome,
                font=(
                    "Segoe UI",
                    8,
                    "bold"
                ),
                fg=TEXTO_SECUNDARIO,
                bg=CREME
            ).pack(
                side="left",
                padx=15,
                pady=12
            )


            tk.Label(
                linha,
                text=valor,
                font=(
                    "Segoe UI",
                    9,
                    "bold"
                ),
                fg=(
                    VERMELHO
                    if valor == "ALTA"
                    else TEXTO
                ),
                bg=CREME
            ).pack(
                side="right",
                padx=15
            )


        tk.Button(
            janela,
            text="FECHAR",
            command=lambda: (
                janela.destroy(),
                self.atualizar_tudo()
            ),
            bg=VINHO,
            fg=BRANCO,
            activebackground=VINHO_CLARO,
            relief="flat",
            bd=0,
            font=(
                "Segoe UI",
                9,
                "bold"
            ),
            cursor="hand2",
            padx=30,
            pady=11
        ).pack(
            pady=25
        )


    # ========================================================
    # MINHAS TAREFAS
    # ========================================================

    def mostrar_tarefas(self):

        self.pagina_atual = "tarefas"

        self.limpar_container()

        self.titulo.config(
            text="Minhas tarefas"
        )

        self.subtitulo.config(
            text="Gerencie tudo o que precisa ser feito."
        )


        topo = tk.Frame(
            self.container,
            bg=FUNDO
        )

        topo.pack(
            fill="x",
            padx=42,
            pady=(0, 15)
        )


        self.busca = tk.Entry(
            topo,
            font=(
                "Segoe UI",
                10
            ),
            bg=BRANCO,
            fg=TEXTO,
            relief="flat",
            bd=0
        )

        self.busca.pack(
            side="left",
            fill="x",
            expand=True,
            ipady=11,
            padx=(0, 10)
        )


        self.busca.bind(
            "<KeyRelease>",
            lambda e:
                self.atualizar_tabela()
        )


        tk.Button(
            topo,
            text="+  NOVA TAREFA",
            command=self.mostrar_nova,
            bg=VINHO,
            fg=BRANCO,
            activebackground=VINHO_CLARO,
            relief="flat",
            bd=0,
            font=(
                "Segoe UI",
                9,
                "bold"
            ),
            cursor="hand2",
            padx=18,
            pady=10
        ).pack(
            side="right"
        )


        card = tk.Frame(
            self.container,
            bg=BRANCO,
            highlightbackground=BORDA,
            highlightthickness=1
        )

        card.pack(
            fill="both",
            expand=True,
            padx=42
        )


        self.fita_dourada(
            card,
            "top",
            0,
            2
        )


        colunas = (
            "ID",
            "TÍTULO",
            "RESPONSÁVEL",
            "PRAZO",
            "PRIORIDADE",
            "CATEGORIA",
            "STATUS",
            "CRIADA EM"
        )


        self.tabela = ttk.Treeview(
            card,
            columns=colunas,
            show="headings",
            selectmode="browse"
        )


        larguras = [
            45,
            290,
            130,
            110,
            105,
            150,
            105,
            130
        ]


        for coluna, largura in zip(
            colunas,
            larguras
        ):

            self.tabela.heading(
                coluna,
                text=coluna
            )

            self.tabela.column(
                coluna,
                width=largura,
                anchor="center"
            )


        scroll = ttk.Scrollbar(
            card,
            orient="vertical",
            command=self.tabela.yview
        )


        self.tabela.configure(
            yscrollcommand=scroll.set
        )


        scroll.pack(
            side="right",
            fill="y"
        )


        self.tabela.pack(
            side="left",
            fill="both",
            expand=True,
            padx=8,
            pady=8
        )


        acoes = tk.Frame(
            self.container,
            bg=FUNDO
        )

        acoes.pack(
            fill="x",
            padx=42,
            pady=15
        )


        self.botao_acao(
            acoes,
            "✓  CONCLUIR",
            self.concluir,
            VERDE_CLARO,
            VERDE
        ).pack(
            side="left",
            padx=(0, 7)
        )


        self.botao_acao(
            acoes,
            "×  EXCLUIR",
            self.excluir,
            VERMELHO_CLARO,
            VERMELHO
        ).pack(
            side="left",
            padx=7
        )


        self.botao_acao(
            acoes,
            "↓  EXPORTAR JSON",
            self.exportar,
            ROXO_CLARO,
            ROXO
        ).pack(
            side="right"
        )


        self.atualizar_tabela()


    # ========================================================
    # BOTÕES DE AÇÃO
    # ========================================================

    def botao_acao(
        self,
        pai,
        texto,
        comando,
        fundo,
        cor
    ):

        return tk.Button(
            pai,
            text=texto,
            command=comando,
            bg=fundo,
            fg=cor,
            activebackground=fundo,
            relief="flat",
            bd=0,
            font=(
                "Segoe UI",
                8,
                "bold"
            ),
            cursor="hand2",
            padx=15,
            pady=9
        )


    # ========================================================
    # ATUALIZAR TABELA
    # ========================================================

    def atualizar_tabela(self):

        if not hasattr(
            self,
            "tabela"
        ):

            return


        for item in self.tabela.get_children():

            self.tabela.delete(item)


        termo = ""


        if hasattr(
            self,
            "busca"
        ):

            termo = self.busca.get().lower()


        for tarefa in buscar():

            texto = " ".join(
                str(x)
                for x in tarefa
            ).lower()


            if termo and termo not in texto:
                continue


            tag = (
                "alta"
                if tarefa[4] == "ALTA"
                else "media"
                if tarefa[4] == "MÉDIA"
                else "concluida"
                if tarefa[6] == "CONCLUÍDA"
                else "baixa"
            )


            self.tabela.insert(
                "",
                "end",
                values=tarefa,
                tags=(tag,)
            )


        self.tabela.tag_configure(
            "alta",
            foreground=VERMELHO
        )

        self.tabela.tag_configure(
            "media",
            foreground=LARANJA
        )

        self.tabela.tag_configure(
            "baixa",
            foreground=VERDE
        )

        self.tabela.tag_configure(
            "concluida",
            foreground=VERDE
        )


    # ========================================================
    # CONCLUIR
    # ========================================================

    def concluir(self):

        selecionado = self.tabela.selection()

        if not selecionado:

            messagebox.showwarning(
                "Atenção",
                "Selecione uma tarefa."
            )

            return


        item = self.tabela.item(
            selecionado[0]
        )


        id_tarefa = item["values"][0]


        con = conectar()
        cur = con.cursor()


        cur.execute("""

            UPDATE tarefas

            SET status = 'CONCLUÍDA'

            WHERE id = ?

        """, (
            id_tarefa,
        ))


        con.commit()

        con.close()


        self.atualizar_tabela()


    # ========================================================
    # EXCLUIR
    # ========================================================

    def excluir(self):

        selecionado = self.tabela.selection()

        if not selecionado:

            messagebox.showwarning(
                "Atenção",
                "Selecione uma tarefa."
            )

            return


        item = self.tabela.item(
            selecionado[0]
        )


        id_tarefa = item["values"][0]


        if not messagebox.askyesno(
            "Excluir tarefa",
            "Deseja realmente excluir esta tarefa?"
        ):

            return


        con = conectar()
        cur = con.cursor()


        cur.execute(
            "DELETE FROM tarefas WHERE id = ?",
            (
                id_tarefa,
            )
        )


        con.commit()

        con.close()


        self.atualizar_tabela()


    # ========================================================
    # DADOS
    # ========================================================

    def mostrar_dados(self):

        self.pagina_atual = "dados"

        self.limpar_container()

        self.titulo.config(
            text="Dados & automação"
        )

        self.subtitulo.config(
            text="Importe, exporte e gere dados de teste."
        )


        area = tk.Frame(
            self.container,
            bg=FUNDO
        )

        area.pack(
            fill="both",
            expand=True,
            padx=42
        )


        self.criar_card_dado(
            area,
            "EXPORTAR",
            "Salvar tarefas",
            "Exporte suas tarefas para um arquivo JSON.",
            "↓  EXPORTAR JSON",
            self.exportar
        )


        self.criar_card_dado(
            area,
            "IMPORTAR",
            "Restaurar tarefas",
            "Carregue tarefas salvas anteriormente.",
            "↑  IMPORTAR JSON",
            self.importar
        )


        self.criar_card_dado(
            area,
            "FAKER",
            "Dados de teste",
            "Crie automaticamente cinco tarefas.",
            "✦  GERAR TESTES",
            self.gerar_faker
        )


    # ========================================================
    # CARDS DE DADOS
    # ========================================================

    def criar_card_dado(
        self,
        pai,
        etiqueta,
        titulo,
        descricao,
        botao,
        comando
    ):

        card = tk.Frame(
            pai,
            bg=BRANCO,
            highlightbackground=BORDA,
            highlightthickness=1
        )

        card.pack(
            fill="x",
            pady=7
        )


        self.fita_dourada(
            card,
            "top",
            0,
            2
        )


        conteudo = tk.Frame(
            card,
            bg=BRANCO
        )

        conteudo.pack(
            side="left",
            padx=25,
            pady=22
        )


        tk.Label(
            conteudo,
            text=etiqueta,
            font=(
                "Segoe UI",
                8,
                "bold"
            ),
            fg=DOURADO,
            bg=BRANCO
        ).pack(
            anchor="w"
        )


        tk.Label(
            conteudo,
            text=titulo,
            font=(
                "Georgia",
                17,
                "bold"
            ),
            fg=TEXTO,
            bg=BRANCO
        ).pack(
            anchor="w"
        )


        tk.Label(
            conteudo,
            text=descricao,
            font=(
                "Segoe UI",
                9
            ),
            fg=TEXTO_SECUNDARIO,
            bg=BRANCO
        ).pack(
            anchor="w",
            pady=(3, 0)
        )


        tk.Button(
            card,
            text=botao,
            command=comando,
            bg=CREME,
            fg=VINHO,
            activebackground=DOURADO_CLARO,
            relief="flat",
            bd=0,
            font=(
                "Segoe UI",
                8,
                "bold"
            ),
            cursor="hand2",
            padx=18,
            pady=10
        ).pack(
            side="right",
            padx=25
        )


    # ========================================================
    # EXPORTAR
    # ========================================================

    def exportar(self):

        dados = []


        for tarefa in buscar():

            dados.append({

                "id": tarefa[0],
                "titulo": tarefa[1],
                "responsavel": tarefa[2],
                "prazo": tarefa[3],
                "prioridade": tarefa[4],
                "categoria": tarefa[5],
                "status": tarefa[6],
                "criada_em": tarefa[7]

            })


        arquivo = filedialog.asksaveasfilename(

            title="Exportar tarefas",

            defaultextension=".json",

            initialfile="tarefas.json",

            filetypes=[
                (
                    "Arquivo JSON",
                    "*.json"
                )
            ]

        )


        if not arquivo:
            return


        with open(
            arquivo,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                dados,
                f,
                ensure_ascii=False,
                indent=4
            )


        messagebox.showinfo(
            "Exportação",
            "Tarefas exportadas com sucesso."
        )


    # ========================================================
    # IMPORTAR
    # ========================================================

    def importar(self):

        arquivo = filedialog.askopenfilename(

            title="Importar tarefas",

            filetypes=[
                (
                    "Arquivo JSON",
                    "*.json"
                )
            ]

        )


        if not arquivo:
            return


        try:

            with open(
                arquivo,
                "r",
                encoding="utf-8"
            ) as f:

                dados = json.load(f)


            quantidade = 0


            for tarefa in dados:

                nova = {

                    "texto_original": tarefa.get(
                        "texto_original",
                        tarefa.get(
                            "titulo",
                            "Tarefa importada"
                        )
                    ),

                    "titulo": tarefa.get(
                        "titulo",
                        "Tarefa importada"
                    ),

                    "responsavel": tarefa.get(
                        "responsavel",
                        "Não definido"
                    ),

                    "prazo": tarefa.get(
                        "prazo",
                        "Não definido"
                    ),

                    "prioridade": tarefa.get(
                        "prioridade",
                        "BAIXA"
                    ),

                    "categoria": tarefa.get(
                        "categoria",
                        "GERAL"
                    ),

                    "status": tarefa.get(
                        "status",
                        "PENDENTE"
                    ),

                    "criada_em": tarefa.get(
                        "criada_em",
                        datetime.now().strftime(
                            "%d/%m/%Y %H:%M"
                        )
                    )

                }


                inserir(nova)

                quantidade += 1


            self.atualizar_tudo()


            messagebox.showinfo(
                "Importação",
                f"{quantidade} tarefa(s) importada(s)."
            )


        except Exception as erro:

            messagebox.showerror(
                "Erro",
                f"Não foi possível importar:\n{erro}"
            )


    # ========================================================
    # FAKER
    # ========================================================

    def gerar_faker(self):

        atividades = [

            "entregar o relatório",
            "organizar o documento",
            "preparar a planilha",
            "enviar a proposta para o cliente",
            "finalizar o projeto"

        ]


        for atividade in atividades:

            nome = fake.first_name()


            data = fake.date_between(
                start_date="+1d",
                end_date="+30d"
            )


            texto = (
                f"{nome} precisa {atividade} "
                f"até {data.strftime('%d/%m/%Y')}."
            )


            inserir(
                interpretar(texto)
            )


        self.atualizar_tudo()


        messagebox.showinfo(
            "Faker",
            "5 tarefas foram criadas."
        )


    # ========================================================
    # ATUALIZAR TUDO
    # ========================================================

    def atualizar_tudo(self):

        if self.pagina_atual == "dashboard":

            self.mostrar_dashboard()

        elif self.pagina_atual == "tarefas":

            self.atualizar_tabela()

        elif self.pagina_atual == "nova":

            pass

        elif self.pagina_atual == "dados":

            pass


# ============================================================
# INICIAR
# ============================================================

criar_banco()

app = Aplicativo()

app.mainloop()