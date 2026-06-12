import gspread
import pandas as pd
from gspread.exceptions import WorksheetNotFound
from zoneinfo import ZoneInfo

from src.utils.config import (
    HISTORICO_PREVISOES_CSV,
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
    ("historico_previsoes", HISTORICO_PREVISOES_CSV),
]

FUSO_LOCAL = ZoneInfo("America/Sao_Paulo")
FORMATO_DATA_HORA = "%d/%m/%Y %H:%M"
COLUNAS_DATA_HORA = [
    "data_hora_utc",
    "atualizado_em",
    "atualizado_em_max",
    "registro_atualizado_em",
]


def abrir_planilha():
    gc = gspread.service_account(filename=SERVICE_ACCOUNT_FILE)
    return gc.open_by_url(SPREADSHEET_URL)


def obter_ou_criar_aba(sh, nome_aba):
    try:
        return sh.worksheet(nome_aba)
    except WorksheetNotFound:
        return sh.add_worksheet(title=nome_aba, rows=1000, cols=80)


def formatar_data_hora_local(serie):
    datas = pd.to_datetime(serie, errors="coerce", utc=True)
    datas = datas.dt.tz_convert(FUSO_LOCAL)
    formatadas = datas.dt.strftime(FORMATO_DATA_HORA)
    return formatadas.fillna(serie)


def preparar_dataframe_para_planilha(df):
    df = df.copy()

    for coluna in df.select_dtypes(include=["float"]).columns:
        df[coluna] = df[coluna].round(4)

    if "id_jogo" in df.columns:
        df["id_jogo"] = df["id_jogo"].apply(formatar_identificador)

    for coluna in COLUNAS_DATA_HORA:
        if coluna in df.columns:
            df[coluna] = formatar_data_hora_local(df[coluna])

    return df.fillna("")


def formatar_identificador(valor):
    if pd.isna(valor):
        return ""
    texto = str(valor)
    try:
        numero = float(texto)
    except ValueError:
        return texto

    if numero.is_integer():
        return str(int(numero))
    return texto


def indice_coluna(colunas, nome_coluna):
    try:
        return colunas.index(nome_coluna)
    except ValueError:
        return None


def request_largura_colunas(sheet_id, inicio, fim, largura):
    return {
        "updateDimensionProperties": {
            "range": {
                "sheetId": sheet_id,
                "dimension": "COLUMNS",
                "startIndex": inicio,
                "endIndex": fim,
            },
            "properties": {"pixelSize": largura},
            "fields": "pixelSize",
        }
    }


def aplicar_formatacao_basica(sh, aba, df):
    total_linhas = len(df) + 1
    total_colunas = len(df.columns)
    sheet_id = aba.id

    requests = [
        {
            "updateSheetProperties": {
                "properties": {
                    "sheetId": sheet_id,
                    "gridProperties": {"frozenRowCount": 1},
                },
                "fields": "gridProperties.frozenRowCount",
            }
        },
        {
            "setBasicFilter": {
                "filter": {
                    "range": {
                        "sheetId": sheet_id,
                        "startRowIndex": 0,
                        "endRowIndex": total_linhas,
                        "startColumnIndex": 0,
                        "endColumnIndex": total_colunas,
                    }
                }
            }
        },
        {
            "repeatCell": {
                "range": {
                    "sheetId": sheet_id,
                    "startRowIndex": 0,
                    "endRowIndex": 1,
                    "startColumnIndex": 0,
                    "endColumnIndex": total_colunas,
                },
                "cell": {
                    "userEnteredFormat": {
                        "backgroundColor": {"red": 0.12, "green": 0.18, "blue": 0.28},
                        "horizontalAlignment": "CENTER",
                        "textFormat": {
                            "foregroundColor": {
                                "red": 1.0,
                                "green": 1.0,
                                "blue": 1.0,
                            },
                            "bold": True,
                        },
                    }
                },
                "fields": (
                    "userEnteredFormat(backgroundColor,"
                    "horizontalAlignment,textFormat)"
                ),
            }
        },
        {
            "repeatCell": {
                "range": {
                    "sheetId": sheet_id,
                    "startRowIndex": 1,
                    "endRowIndex": total_linhas,
                    "startColumnIndex": 0,
                    "endColumnIndex": total_colunas,
                },
                "cell": {
                    "userEnteredFormat": {
                        "verticalAlignment": "TOP",
                        "wrapStrategy": "WRAP",
                    }
                },
                "fields": "userEnteredFormat(verticalAlignment,wrapStrategy)",
            }
        },
        request_largura_colunas(sheet_id, 0, total_colunas, 130),
    ]

    for coluna in df.columns:
        indice = indice_coluna(df.columns.tolist(), coluna)
        if indice is None:
            continue
        if "data_hora" in coluna or "atualizado_em" in coluna:
            requests.append(request_largura_colunas(sheet_id, indice, indice + 1, 155))
        elif coluna in {"time_a", "time_b", "fonte", "criterio_placar"}:
            requests.append(request_largura_colunas(sheet_id, indice, indice + 1, 170))
        elif coluna.startswith("prob_") or coluna.startswith("odd_"):
            requests.append(request_largura_colunas(sheet_id, indice, indice + 1, 95))

    sh.batch_update({"requests": requests})


def atualizar_aba(sh, nome_aba, arquivo_csv):
    df = pd.read_csv(arquivo_csv)
    df = preparar_dataframe_para_planilha(df)

    valores = [df.columns.tolist()] + df.values.tolist()

    aba = obter_ou_criar_aba(sh, nome_aba)
    aba.clear()
    aba.update(range_name="A1", values=valores)
    aplicar_formatacao_basica(sh, aba, df)

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
