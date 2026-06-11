import pandas as pd

from src.utils.config import ODDS_AVANCADAS_RESUMO_CSV


COLUNAS_SINAIS_PLACAR = [
    "linha_gols_referencia",
    "prob_over_referencia",
    "prob_under_referencia",
    "tendencia_gols",
    "time_handicap_favorito",
    "handicap_favorito",
    "odd_handicap_favorito",
    "forca_handicap",
]


def carregar_sinais_placar(arquivo_entrada=ODDS_AVANCADAS_RESUMO_CSV):
    if not arquivo_entrada.exists():
        return pd.DataFrame()

    df = pd.read_csv(arquivo_entrada)
    if df.empty:
        return pd.DataFrame()

    sinais_totals = resumir_totals(df)
    sinais_spreads = resumir_spreads(df)

    if sinais_totals.empty and sinais_spreads.empty:
        return pd.DataFrame()
    if sinais_totals.empty:
        return sinais_spreads
    if sinais_spreads.empty:
        return sinais_totals

    return sinais_totals.merge(sinais_spreads, on="id_odds_api", how="outer")


def resumir_totals(df):
    totals = df[df["mercado"] == "totals"].copy()
    if totals.empty:
        return pd.DataFrame()

    totals["outcome_ponto"] = pd.to_numeric(totals["outcome_ponto"], errors="coerce")
    totals = totals.dropna(subset=["outcome_ponto", "odd_media"])

    linhas = []
    for jogo_id, grupo in totals.groupby("id_odds_api"):
        pivot = grupo.pivot_table(
            index="outcome_ponto",
            columns="outcome_nome",
            values=["odd_media", "qtd_casas"],
            aggfunc="mean",
        )

        candidatos = []
        for ponto in pivot.index:
            try:
                odd_over = pivot.loc[ponto, ("odd_media", "Over")]
                odd_under = pivot.loc[ponto, ("odd_media", "Under")]
            except KeyError:
                continue

            if pd.isna(odd_over) or pd.isna(odd_under) or odd_over <= 0 or odd_under <= 0:
                continue

            qtd_over = _valor_pivot(pivot, ponto, "qtd_casas", "Over")
            qtd_under = _valor_pivot(pivot, ponto, "qtd_casas", "Under")
            prob_over_bruta = 1 / odd_over
            prob_under_bruta = 1 / odd_under
            soma = prob_over_bruta + prob_under_bruta

            candidatos.append(
                {
                    "id_odds_api": jogo_id,
                    "linha_gols_referencia": ponto,
                    "prob_over_referencia": prob_over_bruta / soma,
                    "prob_under_referencia": prob_under_bruta / soma,
                    "qtd_casas_total": qtd_over + qtd_under,
                    "distancia_25": abs(ponto - 2.5),
                }
            )

        if not candidatos:
            continue

        escolhido = sorted(
            candidatos,
            key=lambda item: (item["distancia_25"], -item["qtd_casas_total"]),
        )[0]
        escolhido["tendencia_gols"] = classificar_tendencia_gols(escolhido)
        linhas.append(escolhido)

    if not linhas:
        return pd.DataFrame()

    resumo = pd.DataFrame(linhas)
    return resumo.drop(columns=["qtd_casas_total", "distancia_25"])


def resumir_spreads(df):
    spreads = df[df["mercado"] == "spreads"].copy()
    if spreads.empty:
        return pd.DataFrame()

    spreads["outcome_ponto"] = pd.to_numeric(spreads["outcome_ponto"], errors="coerce")
    spreads = spreads.dropna(subset=["outcome_ponto", "odd_media"])

    linhas = []
    for jogo_id, grupo in spreads.groupby("id_odds_api"):
        candidato = grupo[
            (grupo["outcome_ponto"] < 0)
            & (grupo["odd_media"] >= 1.45)
            & (grupo["odd_media"] <= 2.15)
        ].copy()

        if candidato.empty:
            continue

        candidato["forca_linha"] = candidato["outcome_ponto"].abs()
        candidato = candidato.sort_values(
            by=["forca_linha", "qtd_casas", "odd_media"],
            ascending=[False, False, True],
        )
        melhor = candidato.iloc[0]

        linhas.append(
            {
                "id_odds_api": jogo_id,
                "time_handicap_favorito": melhor["outcome_nome"],
                "handicap_favorito": melhor["outcome_ponto"],
                "odd_handicap_favorito": melhor["odd_media"],
                "forca_handicap": classificar_forca_handicap(melhor["outcome_ponto"]),
            }
        )

    return pd.DataFrame(linhas)


def enriquecer_com_sinais_placar(resumo):
    sinais = carregar_sinais_placar()
    if not sinais.empty:
        resumo = resumo.merge(sinais, on="id_odds_api", how="left")

    for coluna in COLUNAS_SINAIS_PLACAR:
        if coluna not in resumo.columns:
            resumo[coluna] = pd.NA

    resumo["tendencia_gols"] = resumo["tendencia_gols"].fillna("sem_totals")
    resumo["forca_handicap"] = resumo["forca_handicap"].fillna("sem_spreads")
    return resumo


def gerar_placar(row):
    resultado = gerar_resultado(row)
    vantagem = calcular_vantagem(row)
    tendencia_gols = row.get("tendencia_gols", "sem_totals")
    forca_handicap = forca_handicap_confirmada(row, resultado)

    if resultado == "empate":
        if tendencia_gols == "mais_gols":
            return "2x2"
        return "1x1"

    favorito_forte = vantagem >= 0.30 or forca_handicap in {"forte", "muito_forte"}
    favorito_normal = vantagem >= 0.15 or forca_handicap == "moderado"

    if resultado == "time_a":
        if tendencia_gols == "menos_gols":
            return "1x0" if not favorito_forte else "2x0"
        if tendencia_gols == "mais_gols":
            return "3x1" if favorito_forte else "2x1"
        if favorito_forte:
            return "2x0"
        if favorito_normal:
            return "2x1"
        return "1x0"

    if resultado == "time_b":
        if tendencia_gols == "menos_gols":
            return "0x1" if not favorito_forte else "0x2"
        if tendencia_gols == "mais_gols":
            return "1x3" if favorito_forte else "1x2"
        if favorito_forte:
            return "0x2"
        if favorito_normal:
            return "1x2"
        return "0x1"

    raise ValueError(f"Resultado inesperado: {resultado}")


def calcular_confianca_placar(row):
    tendencia_gols = row.get("tendencia_gols", "sem_totals")
    resultado = gerar_resultado(row)
    forca_handicap = forca_handicap_confirmada(row, resultado)
    vantagem = calcular_vantagem(row)

    if tendencia_gols != "sem_totals" and forca_handicap in {"forte", "muito_forte"}:
        return "media"
    if tendencia_gols != "sem_totals" and vantagem >= 0.15:
        return "media"
    return "baixa"


def gerar_criterio_placar(row):
    partes = ["odds_h2h"]

    if row.get("tendencia_gols", "sem_totals") != "sem_totals":
        partes.append(f"totals_{row['tendencia_gols']}")
    if row.get("forca_handicap", "sem_spreads") != "sem_spreads":
        resultado = gerar_resultado(row)
        forca = forca_handicap_confirmada(row, resultado)
        if forca == "spread_diverge_resultado":
            partes.append("spread_diverge_resultado")
        elif forca != "sem_spreads":
            partes.append(f"spread_{forca}")

    return "+".join(partes)


def gerar_resultado(row):
    probs = {
        "time_a": row["prob_a_media"],
        "empate": row["prob_empate_media"],
        "time_b": row["prob_b_media"],
    }
    return max(probs, key=probs.get)


def calcular_vantagem(row):
    probs = sorted(
        [row["prob_a_media"], row["prob_empate_media"], row["prob_b_media"]],
        reverse=True,
    )
    return probs[0] - probs[1]


def forca_handicap_confirmada(row, resultado):
    forca_handicap = row.get("forca_handicap", "sem_spreads")
    time_handicap = row.get("time_handicap_favorito")

    if forca_handicap == "sem_spreads" or pd.isna(time_handicap):
        return "sem_spreads"

    if resultado == "time_a" and time_handicap == row.get("time_a"):
        return forca_handicap
    if resultado == "time_b" and time_handicap == row.get("time_b"):
        return forca_handicap
    if resultado == "empate":
        return "sem_spreads"

    return "spread_diverge_resultado"


def classificar_tendencia_gols(row):
    prob_over = row["prob_over_referencia"]
    prob_under = row["prob_under_referencia"]

    if prob_over >= 0.56:
        return "mais_gols"
    if prob_under >= 0.56:
        return "menos_gols"
    return "neutro"


def classificar_forca_handicap(handicap):
    handicap_abs = abs(handicap)
    if handicap_abs >= 1.5:
        return "muito_forte"
    if handicap_abs >= 1.0:
        return "forte"
    if handicap_abs >= 0.5:
        return "moderado"
    return "leve"


def _valor_pivot(pivot, ponto, campo, outcome):
    try:
        valor = pivot.loc[ponto, (campo, outcome)]
    except KeyError:
        return 0

    if pd.isna(valor):
        return 0
    return valor
