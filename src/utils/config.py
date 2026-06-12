import os
from pathlib import Path

from dotenv import load_dotenv


SPREADSHEET_URL = "https://docs.google.com/spreadsheets/d/1XBKDm8hgNvC_gZqRKNTH1XfwSBiuViGqZLHjyvhDncU/edit"
SERVICE_ACCOUNT_FILE = "service_account.json"

DATA_DIR = Path("data")
JOGOS_COPA_CSV = DATA_DIR / "jogos_copa.csv"
ODDS_COPA_CSV = DATA_DIR / "odds_copa.csv"
ODDS_AVANCADAS_CSV = DATA_DIR / "odds_avancadas.csv"
ODDS_AVANCADAS_RESUMO_CSV = DATA_DIR / "odds_avancadas_resumo.csv"
ODDS_EVENTOS_CSV = DATA_DIR / "odds_eventos.csv"
ODDS_MERCADOS_CSV = DATA_DIR / "odds_mercados.csv"
ODDS_HISTORICO_CSV = DATA_DIR / "odds_historico.csv"
ODDS_RESUMO_CSV = DATA_DIR / "odds_resumo.csv"
PALPITES_ODDS_CSV = DATA_DIR / "palpites_odds.csv"
HISTORICO_PREVISOES_CSV = DATA_DIR / "historico_previsoes.csv"
ELO_SELECOES_CSV = DATA_DIR / "elo_selecoes.csv"
HISTORICO_ODDS_DIR = DATA_DIR / "historico_odds"


def garantir_data_dir():
    DATA_DIR.mkdir(exist_ok=True)


def carregar_env():
    load_dotenv()


def obter_variavel_obrigatoria(nome, mensagem_erro):
    carregar_env()
    valor = os.getenv(nome)

    if not valor:
        raise ValueError(mensagem_erro)

    return valor
