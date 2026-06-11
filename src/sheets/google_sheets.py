import gspread
import pandas as pd

from src.utils.config import (
    JOGOS_COPA_CSV,
    ODDS_COPA_CSV,
    ODDS_RESUMO_CSV,
    PALPITES_ODDS_CSV,
    SERVICE_ACCOUNT_FILE,
    SPREADSHEET_URL,
)


ABAS_CSV = [
    ("jogos", JOGOS_COPA_CSV),
    ("odds", ODDS_COPA_CSV),
    ("odds_resumo", ODDS_RESUMO_CSV),
    ("palpites_bolao", PALPITES_ODDS_CSV),
]


def abrir_planilha():
    gc = gspread.service_account(filename=SERVICE_ACCOUNT_FILE)
    return gc.open_by_url(SPREADSHEET_URL)


def atualizar_aba(sh, nome_aba, arquivo_csv):
    df = pd.read_csv(arquivo_csv)
    df = df.fillna("")

    valores = [df.columns.tolist()] + df.values.tolist()

    aba = sh.worksheet(nome_aba)
    aba.clear()
    aba.update(range_name="A1", values=valores)

    print(f"Aba atualizada: {nome_aba} <- {arquivo_csv}")


def atualizar_planilha():
    sh = abrir_planilha()

    for nome_aba, arquivo_csv in ABAS_CSV:
        atualizar_aba(sh, nome_aba, arquivo_csv)

    print("Planilha atualizada com sucesso.")


def testar_conexao():
    sh = abrir_planilha()
    aba = sh.worksheet("palpites_bolao")
    aba.update("A1", [["teste_google_sheets_ok"]])
    print("Conexao com Google Sheets funcionando.")


if __name__ == "__main__":
    atualizar_planilha()
