import pandas as pd
import requests
import sys

from src.utils.config import JOGOS_COPA_CSV, garantir_data_dir, obter_variavel_obrigatoria


COMPETITIONS_URL = "https://api.football-data.org/v4/competitions"
WORLD_CUP_MATCHES_URL = "https://api.football-data.org/v4/competitions/WC/matches"


def obter_token():
    return obter_variavel_obrigatoria(
        "FOOTBALL_DATA_TOKEN",
        "Token nao encontrado. Confira o arquivo .env",
    )


def buscar_dados(url):
    headers = {"X-Auth-Token": obter_token()}
    response = requests.get(url, headers=headers)

    print("Status:", response.status_code)

    dados = response.json()

    if response.status_code != 200:
        print(dados)
        raise SystemExit()

    return dados


def listar_competicoes():
    dados = buscar_dados(COMPETITIONS_URL)
    competicoes = dados.get("competitions", [])

    print("Total de competicoes:", len(competicoes))

    for competicao in competicoes:
        code = competicao.get("code")
        name = competicao.get("name")
        print(code, "-", name)


def buscar_jogos_copa():
    dados = buscar_dados(WORLD_CUP_MATCHES_URL)
    partidas = dados.get("matches", [])

    print("Total de partidas:", len(partidas))

    for partida in partidas[:10]:
        data = partida.get("utcDate")
        fase = partida.get("stage")
        grupo = partida.get("group")
        casa = partida.get("homeTeam", {}).get("name")
        fora = partida.get("awayTeam", {}).get("name")
        status = partida.get("status")

        print(data, "|", fase, "|", grupo, "|", casa, "x", fora, "|", status)


def salvar_jogos_csv(arquivo_saida=JOGOS_COPA_CSV):
    garantir_data_dir()

    dados = buscar_dados(WORLD_CUP_MATCHES_URL)
    partidas = dados.get("matches", [])

    linhas = []

    for partida in partidas:
        linhas.append(
            {
                "id_jogo": partida.get("id"),
                "data_hora_utc": partida.get("utcDate"),
                "fase": partida.get("stage"),
                "grupo": partida.get("group"),
                "time_a": partida.get("homeTeam", {}).get("name"),
                "time_b": partida.get("awayTeam", {}).get("name"),
                "placar_a": partida.get("score", {}).get("fullTime", {}).get("home"),
                "placar_b": partida.get("score", {}).get("fullTime", {}).get("away"),
                "status": partida.get("status"),
                "fonte_jogo": "football-data.org",
            }
        )

    df = pd.DataFrame(linhas)
    df.to_csv(arquivo_saida, index=False, encoding="utf-8-sig")

    print(f"Arquivo {arquivo_saida} criado com sucesso.")
    print("Total de jogos:", len(df))
    print(df.head())


def main():
    comando = sys.argv[1] if len(sys.argv) > 1 else "buscar"

    if comando == "competicoes":
        listar_competicoes()
    elif comando == "buscar":
        buscar_jogos_copa()
    elif comando == "salvar":
        salvar_jogos_csv()
    else:
        raise SystemExit(f"Comando invalido para football_data: {comando}")


if __name__ == "__main__":
    main()
