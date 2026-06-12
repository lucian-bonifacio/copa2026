from datetime import timedelta
from zoneinfo import ZoneInfo

import pandas as pd

from src.utils.config import (
    HISTORICO_PREVISOES_CSV,
    JOGOS_COPA_CSV,
    PALPITES_ODDS_CSV,
    garantir_data_dir,
)


FUSO_LOCAL = ZoneInfo("America/Sao_Paulo")
JANELA_CONGELAMENTO_HORAS = 3
FORMATO_DATA_HORA = "%Y-%m-%d %H:%M:%S%z"

COLUNAS_PREVISAO = [
    "id_odds_api",
    "data_hora_utc",
    "data_jogo",
    "time_a",
    "time_b",
    "resultado_sugerido",
    "placar_sugerido",
    "confianca",
    "confianca_placar",
    "criterio_placar",
    "previsao_resultado",
    "previsao_placar",
    "previsao_gols_time_a",
    "previsao_gols_time_b",
    "previsao_gols_vencedor",
    "previsao_gols_perdedor",
    "previsao_diferenca_gols",
    "previsao_total_gols",
    "previsao_tendencia_gols",
    "confianca_resultado",
    "confianca_gols",
    "fonte_previsao_resultado",
    "fonte_previsao_gols",
    "fonte_previsao_placar",
    "prob_a_media",
    "prob_empate_media",
    "prob_b_media",
    "score_mercado_a",
    "score_mercado_empate",
    "score_mercado_b",
    "confianca_mercado",
    "favoritismo_movimento",
    "elo_pontos_a",
    "elo_pontos_b",
    "diferenca_elo_pontos",
    "favorito_elo",
    "status_elo",
    "linha_gols_referencia",
    "prob_over_referencia",
    "prob_under_referencia",
    "tendencia_gols",
    "time_handicap_favorito",
    "handicap_favorito",
    "odd_handicap_favorito",
    "forca_handicap",
    "criterio",
]

COLUNAS_CONTROLE = [
    "id_jogo",
    "registro_atualizado_em",
    "previsao_congelada",
    "janela_congelamento_horas",
]

COLUNAS_RESULTADO = [
    "placar_real_a",
    "placar_real_b",
    "resultado_real",
    "status_jogo",
    "acertou_resultado",
    "acertou_placar",
    "erro_total_gols",
    "erro_diferenca_gols",
]

COLUNAS_HISTORICO = COLUNAS_CONTROLE + COLUNAS_PREVISAO + COLUNAS_RESULTADO


def agora_local():
    return pd.Timestamp.now(tz=FUSO_LOCAL)


def formatar_timestamp(valor):
    if pd.isna(valor):
        return ""
    return pd.Timestamp(valor).strftime(FORMATO_DATA_HORA)


def normalizar_time(valor):
    return str(valor).strip().casefold()


def chave_time_a_time_b(time_a, time_b):
    return (normalizar_time(time_a), normalizar_time(time_b))


def chave_jogo(time_a, time_b, data_hora_utc):
    data = pd.to_datetime(data_hora_utc, errors="coerce", utc=True)
    data_chave = "" if pd.isna(data) else data.strftime("%Y-%m-%dT%H:%M:%SZ")
    return (*chave_time_a_time_b(time_a, time_b), data_chave)


def carregar_csv(caminho):
    if not caminho.exists():
        return pd.DataFrame()
    return pd.read_csv(caminho, dtype=str).fillna("")


def data_jogo_local(data_hora_utc):
    data = pd.to_datetime(data_hora_utc, errors="coerce", utc=True)
    if pd.isna(data):
        return ""
    return data.tz_convert(FUSO_LOCAL).strftime("%d/%m/%Y %H:%M")


def deve_congelar(data_hora_utc, referencia):
    data = pd.to_datetime(data_hora_utc, errors="coerce", utc=True)
    if pd.isna(data):
        return False
    data = data.tz_convert(FUSO_LOCAL)
    limite = data - timedelta(hours=JANELA_CONGELAMENTO_HORAS)
    return referencia >= limite


def montar_indice_jogos(jogos):
    indice_exato = {}
    indice_times = {}

    for _, jogo in jogos.iterrows():
        time_a = jogo.get("time_a", "")
        time_b = jogo.get("time_b", "")
        data_hora_utc = jogo.get("data_hora_utc", "")

        chave_exata_direta = chave_jogo(time_a, time_b, data_hora_utc)
        chave_exata_invertida = chave_jogo(time_b, time_a, data_hora_utc)
        chave_times_direta = chave_time_a_time_b(time_a, time_b)
        chave_times_invertida = chave_time_a_time_b(time_b, time_a)

        indice_exato[chave_exata_direta] = (jogo, False)
        indice_exato[chave_exata_invertida] = (jogo, True)
        indice_times[chave_times_direta] = (jogo, False)
        indice_times[chave_times_invertida] = (jogo, True)

    return {"exato": indice_exato, "times": indice_times}


def buscar_jogo(row, indice_jogos):
    chave_exata = chave_jogo(
        row.get("time_a", ""),
        row.get("time_b", ""),
        row.get("data_hora_utc", ""),
    )
    if chave_exata in indice_jogos["exato"]:
        return indice_jogos["exato"][chave_exata]

    chave_times = chave_time_a_time_b(
        row.get("time_a", ""),
        row.get("time_b", ""),
    )
    return indice_jogos["times"].get(chave_times, (None, False))


def resultado_por_placar(gols_a, gols_b):
    if gols_a == "" or gols_b == "":
        return ""

    gols_a = int(float(gols_a))
    gols_b = int(float(gols_b))

    if gols_a > gols_b:
        return "time_a"
    if gols_b > gols_a:
        return "time_b"
    return "empate"


def gols_do_placar_sugerido(placar):
    partes = str(placar).lower().replace(" ", "").split("x")
    if len(partes) != 2:
        return "", ""

    try:
        return int(partes[0]), int(partes[1])
    except ValueError:
        return "", ""


def calcular_erros(row):
    previsto_a, previsto_b = gols_do_placar_sugerido(row.get("placar_sugerido", ""))
    real_a = row.get("placar_real_a", "")
    real_b = row.get("placar_real_b", "")

    if previsto_a == "" or previsto_b == "" or real_a == "" or real_b == "":
        return "", ""

    real_a = int(float(real_a))
    real_b = int(float(real_b))
    erro_total = abs((previsto_a + previsto_b) - (real_a + real_b))
    erro_diferenca = abs((previsto_a - previsto_b) - (real_a - real_b))
    return erro_total, erro_diferenca


def atualizar_resultado(row, indice_jogos):
    jogo, invertido = buscar_jogo(row, indice_jogos)
    if jogo is None:
        return row

    row["id_jogo"] = jogo.get("id_jogo", row.get("id_jogo", ""))
    row["status_jogo"] = jogo.get("status", row.get("status_jogo", ""))

    placar_a = jogo.get("placar_a", "")
    placar_b = jogo.get("placar_b", "")

    if placar_a != "" and placar_b != "":
        if invertido:
            row["placar_real_a"] = placar_b
            row["placar_real_b"] = placar_a
        else:
            row["placar_real_a"] = placar_a
            row["placar_real_b"] = placar_b

        row["resultado_real"] = resultado_por_placar(
            row["placar_real_a"], row["placar_real_b"]
        )
        row["acertou_resultado"] = str(
            row.get("resultado_sugerido", "") == row["resultado_real"]
        ).lower()
        row["acertou_placar"] = str(
            row.get("placar_sugerido", "")
            == f"{int(float(row['placar_real_a']))}x{int(float(row['placar_real_b']))}"
        ).lower()
        erro_total, erro_diferenca = calcular_erros(row)
        row["erro_total_gols"] = erro_total
        row["erro_diferenca_gols"] = erro_diferenca

    return row


def linha_de_palpite(palpite, existente, referencia, indice_jogos):
    id_odds_api = str(palpite["id_odds_api"])
    congelada = str(existente.get("previsao_congelada", "")).lower() == "sim"
    deve_travar = deve_congelar(palpite.get("data_hora_utc", ""), referencia)
    agora = formatar_timestamp(referencia)

    if congelada:
        row = existente.copy()
        row["registro_atualizado_em"] = agora
        return atualizar_resultado(row, indice_jogos)

    row = existente.copy()
    if not row:
        row = {coluna: "" for coluna in COLUNAS_HISTORICO}
        row["id_odds_api"] = id_odds_api

    for coluna in COLUNAS_PREVISAO:
        if coluna == "data_jogo":
            row[coluna] = data_jogo_local(palpite.get("data_hora_utc", ""))
        else:
            row[coluna] = palpite.get(coluna, "")

    row["registro_atualizado_em"] = agora
    row["janela_congelamento_horas"] = JANELA_CONGELAMENTO_HORAS

    if deve_travar:
        row["previsao_congelada"] = "sim"
    else:
        row["previsao_congelada"] = "nao"

    return atualizar_resultado(row, indice_jogos)


def atualizar_historico_previsoes(
    arquivo_palpites=PALPITES_ODDS_CSV,
    arquivo_jogos=JOGOS_COPA_CSV,
    arquivo_saida=HISTORICO_PREVISOES_CSV,
):
    garantir_data_dir()

    palpites = pd.read_csv(arquivo_palpites).fillna("")
    jogos = pd.read_csv(arquivo_jogos, dtype=str).fillna("")
    historico = carregar_csv(arquivo_saida)
    referencia = agora_local()
    indice_jogos = montar_indice_jogos(jogos)

    existentes = {}
    if not historico.empty:
        for _, row in historico.iterrows():
            existentes[str(row.get("id_odds_api", ""))] = row.to_dict()

    linhas = {}

    for _, palpite in palpites.iterrows():
        id_odds_api = str(palpite["id_odds_api"])
        existente = existentes.pop(id_odds_api, {})
        linhas[id_odds_api] = linha_de_palpite(
            palpite.to_dict(), existente, referencia, indice_jogos
        )

    for id_odds_api, existente in existentes.items():
        linhas[id_odds_api] = atualizar_resultado(existente, indice_jogos)

    saida = pd.DataFrame(linhas.values())
    for coluna in COLUNAS_HISTORICO:
        if coluna not in saida.columns:
            saida[coluna] = ""

    saida = saida[COLUNAS_HISTORICO].fillna("")
    saida.to_csv(arquivo_saida, index=False, encoding="utf-8-sig")

    congeladas = (saida["previsao_congelada"] == "sim").sum()
    print(f"Arquivo {arquivo_saida} atualizado.")
    print(f"Total de previsoes historicas: {len(saida)}")
    print(f"Previsoes congeladas: {congeladas}")


if __name__ == "__main__":
    atualizar_historico_previsoes()
