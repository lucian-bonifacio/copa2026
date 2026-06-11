import pandas as pd
import requests
import sys
from requests import RequestException

from src.utils.config import (
    ODDS_AVANCADAS_CSV,
    ODDS_AVANCADAS_RESUMO_CSV,
    ODDS_COPA_CSV,
    ODDS_EVENTOS_CSV,
    ODDS_MERCADOS_CSV,
    garantir_data_dir,
    obter_variavel_obrigatoria,
)


SPORTS_URL = "https://api.the-odds-api.com/v4/sports/"
WORLD_CUP_EVENTS_URL = "https://api.the-odds-api.com/v4/sports/soccer_fifa_world_cup/events"
WORLD_CUP_ODDS_URL = "https://api.the-odds-api.com/v4/sports/soccer_fifa_world_cup/odds"
WORLD_CUP_EVENT_MARKETS_URL = "https://api.the-odds-api.com/v4/sports/soccer_fifa_world_cup/events/{event_id}/markets"


def obter_api_key():
    return obter_variavel_obrigatoria(
        "ODDS_API_KEY",
        "ODDS_API_KEY nao encontrada. Confira o arquivo .env",
    )


def imprimir_creditos(response):
    print(f"[ODDS_API] Status: {response.status_code}")
    print(f"[ODDS_API] Creditos restantes: {response.headers.get('x-requests-remaining')}")
    print(f"[ODDS_API] Creditos usados: {response.headers.get('x-requests-used')}")

    custo_ultima_chamada = response.headers.get("x-requests-last")
    if custo_ultima_chamada is not None:
        print(f"[ODDS_API] Custo da ultima chamada: {custo_ultima_chamada}")


def listar_esportes():
    params = {
        "apiKey": obter_api_key(),
        "all": "true",
    }

    response = requests.get(SPORTS_URL, params=params)
    imprimir_creditos(response)

    dados = response.json()

    if response.status_code != 200:
        print(dados)
        raise SystemExit()

    for esporte in dados:
        key = esporte.get("key")
        group = esporte.get("group")
        title = esporte.get("title")
        active = esporte.get("active")
        has_outrights = esporte.get("has_outrights")

        if group == "Soccer":
            print(key, "|", title, "| active:", active, "| outrights:", has_outrights)


def listar_eventos_copa(arquivo_saida=ODDS_EVENTOS_CSV):
    garantir_data_dir()

    params = {
        "apiKey": obter_api_key(),
        "dateFormat": "iso",
    }

    response = requests.get(WORLD_CUP_EVENTS_URL, params=params)
    imprimir_creditos(response)

    dados = response.json()

    if response.status_code != 200:
        print("[ERRO] Falha ao buscar eventos na The Odds API.")
        print(dados)
        raise SystemExit()

    linhas = []
    for evento in dados:
        linhas.append(
            {
                "id_odds_api": evento.get("id"),
                "data_hora_utc": evento.get("commence_time"),
                "time_a": evento.get("home_team"),
                "time_b": evento.get("away_team"),
                "sport_key": evento.get("sport_key"),
                "sport_title": evento.get("sport_title"),
            }
        )

    df = pd.DataFrame(linhas)
    df.to_csv(arquivo_saida, index=False, encoding="utf-8-sig")

    print(f"[OK] Arquivo {arquivo_saida} criado.")
    print("[OK] Total de eventos:", len(df))
    print(df.head(20))


def carregar_eventos_para_mapeamento():
    if ODDS_EVENTOS_CSV.exists():
        eventos = pd.read_csv(ODDS_EVENTOS_CSV)
        if "id_odds_api" in eventos.columns and not eventos.empty:
            return eventos

    if ODDS_COPA_CSV.exists():
        odds = pd.read_csv(ODDS_COPA_CSV)
        colunas = ["id_odds_api", "data_hora_utc", "time_a", "time_b"]
        if set(colunas).issubset(odds.columns):
            return odds[colunas].drop_duplicates()

    raise FileNotFoundError(
        "Nenhum arquivo local com eventos encontrado. Rode primeiro "
        "`python -m src.apis.odds_api eventos` ou busque odds da Copa."
    )


def buscar_mercados_evento(evento_id, regions="eu,uk"):
    params = {
        "apiKey": obter_api_key(),
        "regions": regions,
        "dateFormat": "iso",
    }

    url = WORLD_CUP_EVENT_MARKETS_URL.format(event_id=evento_id)
    try:
        response = requests.get(url, params=params, timeout=30)
    except RequestException as exc:
        print(f"[ERRO] Falha de conexao ao buscar mercados do evento {evento_id}.")
        print(f"[ERRO] Tipo: {type(exc).__name__}")
        raise SystemExit(1) from None
    imprimir_creditos(response)

    dados = response.json()

    if response.status_code != 200:
        print(f"[ERRO] Falha ao buscar mercados do evento {evento_id}.")
        print(dados)
        raise SystemExit()

    return dados


def mapear_mercados_eventos(arquivo_saida=ODDS_MERCADOS_CSV, limite=None, regions="eu,uk"):
    garantir_data_dir()

    eventos = carregar_eventos_para_mapeamento()
    if limite is not None:
        eventos = eventos.head(limite)

    linhas = []

    for _, evento in eventos.iterrows():
        evento_id = evento["id_odds_api"]
        print(f"[INFO] Mapeando mercados do evento: {evento_id}")
        dados = buscar_mercados_evento(evento_id, regions=regions)

        for bookmaker in dados.get("bookmakers", []):
            for mercado in bookmaker.get("markets", []):
                linhas.append(
                    {
                        "id_odds_api": dados.get("id"),
                        "data_hora_utc": dados.get("commence_time"),
                        "time_a": dados.get("home_team"),
                        "time_b": dados.get("away_team"),
                        "bookmaker": bookmaker.get("title"),
                        "bookmaker_key": bookmaker.get("key"),
                        "mercado": mercado.get("key"),
                        "mercado_atualizado_em": mercado.get("last_update"),
                    }
                )

    df = pd.DataFrame(linhas)
    df.to_csv(arquivo_saida, index=False, encoding="utf-8-sig")

    print(f"[OK] Arquivo {arquivo_saida} criado.")
    print("[OK] Total de linhas:", len(df))

    if not df.empty:
        print("[INFO] Mercados encontrados:")
        print(df["mercado"].value_counts())


def buscar_odds_copa(arquivo_saida=ODDS_COPA_CSV):
    garantir_data_dir()

    params = {
        "apiKey": obter_api_key(),
        "regions": "eu,uk",
        "markets": "h2h",
        "oddsFormat": "decimal",
        "dateFormat": "iso",
    }

    response = requests.get(WORLD_CUP_ODDS_URL, params=params)
    imprimir_creditos(response)

    dados = response.json()

    if response.status_code != 200:
        print("[ERRO] Falha ao buscar odds na The Odds API.")
        print(dados)
        raise SystemExit()

    linhas = []

    for jogo in dados:
        jogo_id = jogo.get("id")
        data_hora = jogo.get("commence_time")
        time_casa = jogo.get("home_team")
        time_fora = jogo.get("away_team")

        for casa_aposta in jogo.get("bookmakers", []):
            bookmaker = casa_aposta.get("title")
            atualizado_em = casa_aposta.get("last_update")

            for mercado in casa_aposta.get("markets", []):
                if mercado.get("key") != "h2h":
                    continue

                odds = {
                    "id_odds_api": jogo_id,
                    "data_hora_utc": data_hora,
                    "time_a": time_casa,
                    "time_b": time_fora,
                    "fonte": bookmaker,
                    "mercado": "h2h",
                    "odd_a": None,
                    "odd_empate": None,
                    "odd_b": None,
                    "atualizado_em": atualizado_em,
                }

                for outcome in mercado.get("outcomes", []):
                    nome = outcome.get("name")
                    preco = outcome.get("price")

                    if nome == time_casa:
                        odds["odd_a"] = preco
                    elif nome == time_fora:
                        odds["odd_b"] = preco
                    elif nome == "Draw":
                        odds["odd_empate"] = preco

                linhas.append(odds)

    df = pd.DataFrame(linhas)

    print("[INFO] Mercados encontrados:")
    print(df["mercado"].value_counts())

    df.to_csv(arquivo_saida, index=False, encoding="utf-8-sig")

    print(f"[OK] Arquivo {arquivo_saida} criado.")
    print("[OK] Total de linhas:", len(df))
    print(df.head(20))


def buscar_odds_avancadas(
    arquivo_saida=ODDS_AVANCADAS_CSV,
    markets="h2h,totals,spreads",
    regions="eu,uk",
):
    garantir_data_dir()

    params = {
        "apiKey": obter_api_key(),
        "regions": regions,
        "markets": markets,
        "oddsFormat": "decimal",
        "dateFormat": "iso",
    }

    response = requests.get(WORLD_CUP_ODDS_URL, params=params)
    imprimir_creditos(response)

    dados = response.json()

    if response.status_code != 200:
        print("[ERRO] Falha ao buscar odds avancadas na The Odds API.")
        print(dados)
        raise SystemExit()

    linhas = []

    for jogo in dados:
        for casa_aposta in jogo.get("bookmakers", []):
            bookmaker = casa_aposta.get("title")
            bookmaker_key = casa_aposta.get("key")
            bookmaker_atualizado_em = casa_aposta.get("last_update")

            for mercado in casa_aposta.get("markets", []):
                mercado_key = mercado.get("key")
                mercado_atualizado_em = mercado.get("last_update") or bookmaker_atualizado_em

                for outcome in mercado.get("outcomes", []):
                    linhas.append(
                        {
                            "id_odds_api": jogo.get("id"),
                            "data_hora_utc": jogo.get("commence_time"),
                            "time_a": jogo.get("home_team"),
                            "time_b": jogo.get("away_team"),
                            "fonte": bookmaker,
                            "fonte_key": bookmaker_key,
                            "mercado": mercado_key,
                            "outcome_nome": outcome.get("name"),
                            "outcome_preco": outcome.get("price"),
                            "outcome_ponto": outcome.get("point"),
                            "atualizado_em": mercado_atualizado_em,
                        }
                    )

    df = pd.DataFrame(linhas)
    df.to_csv(arquivo_saida, index=False, encoding="utf-8-sig")

    print(f"[OK] Arquivo {arquivo_saida} criado.")
    print("[OK] Total de linhas:", len(df))

    if not df.empty:
        print("[INFO] Mercados encontrados:")
        print(df["mercado"].value_counts())
        print(df.head(20))


def resumir_odds_avancadas(
    arquivo_entrada=ODDS_AVANCADAS_CSV,
    arquivo_saida=ODDS_AVANCADAS_RESUMO_CSV,
):
    garantir_data_dir()

    df = pd.read_csv(arquivo_entrada)

    if df.empty:
        df.to_csv(arquivo_saida, index=False, encoding="utf-8-sig")
        print(f"[OK] Arquivo {arquivo_saida} criado vazio.")
        return

    resumo = (
        df.groupby(
            [
                "id_odds_api",
                "data_hora_utc",
                "time_a",
                "time_b",
                "mercado",
                "outcome_nome",
                "outcome_ponto",
            ],
            dropna=False,
            as_index=False,
        )
        .agg(
            qtd_casas=("fonte", "count"),
            odd_media=("outcome_preco", "mean"),
            odd_min=("outcome_preco", "min"),
            odd_max=("outcome_preco", "max"),
            atualizado_em_max=("atualizado_em", "max"),
        )
    )

    resumo["prob_implicita_media"] = 1 / resumo["odd_media"]
    resumo.to_csv(arquivo_saida, index=False, encoding="utf-8-sig")

    print(f"[OK] Arquivo {arquivo_saida} criado.")
    print("[OK] Total de linhas:", len(resumo))
    print(resumo.head(20))


def main():
    comando = sys.argv[1] if len(sys.argv) > 1 else "odds"

    if comando == "odds":
        buscar_odds_copa()
    elif comando == "odds-avancadas":
        buscar_odds_avancadas()
    elif comando == "resumir-avancadas":
        resumir_odds_avancadas()
    elif comando == "esportes":
        listar_esportes()
    elif comando == "eventos":
        listar_eventos_copa()
    elif comando == "mercados":
        limite = int(sys.argv[2]) if len(sys.argv) > 2 else None
        mapear_mercados_eventos(limite=limite)
    else:
        raise SystemExit(f"Comando invalido para odds_api: {comando}")


if __name__ == "__main__":
    main()
