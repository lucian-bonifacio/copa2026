import pandas as pd
import sys

from src.palpites.elo import enriquecer_com_elo
from src.palpites.placar import (
    calcular_confianca_placar,
    enriquecer_com_sinais_placar,
    gerar_criterio_placar,
    gerar_placar,
)
from src.utils.config import (
    ODDS_COPA_CSV,
    ODDS_HISTORICO_CSV,
    ODDS_RESUMO_CSV,
    PALPITES_ODDS_CSV,
    garantir_data_dir,
)


def resultado_mais_provavel(row):
    probs = {
        "time_a": row["prob_a_media"],
        "empate": row["prob_empate_media"],
        "time_b": row["prob_b_media"],
    }
    return max(probs, key=probs.get)


def gerar_resultado(row):
    return resultado_mais_provavel(row)


def calcular_confianca(row):
    maior_prob = max(
        row["prob_a_media"],
        row["prob_empate_media"],
        row["prob_b_media"],
    )

    if maior_prob >= 0.60:
        return "alta"
    if maior_prob >= 0.45:
        return "media"
    return "baixa"


def calcular_confianca_mercado(row):
    maior_score = max(
        row["score_mercado_a"],
        row["score_mercado_empate"],
        row["score_mercado_b"],
    )
    scores = sorted(
        [
            row["score_mercado_a"],
            row["score_mercado_empate"],
            row["score_mercado_b"],
        ],
        reverse=True,
    )
    vantagem = scores[0] - scores[1]
    dispersao_media = row["dispersao_media_mercado"]

    if maior_score >= 0.60 and vantagem >= 0.15 and dispersao_media <= 0.12:
        return "alta"
    if maior_score >= 0.45 and vantagem >= 0.06 and dispersao_media <= 0.20:
        return "media"
    return "baixa"


def carregar_movimento_mercado(arquivo_historico=ODDS_HISTORICO_CSV):
    if not arquivo_historico.exists():
        return pd.DataFrame()

    historico = pd.read_csv(arquivo_historico)

    if historico.empty or "coletado_em" not in historico.columns:
        return pd.DataFrame()

    ultima_coleta = historico["coletado_em"].max()
    historico = historico[historico["coletado_em"] == ultima_coleta].copy()

    colunas_necessarias = {
        "id_odds_api",
        "odd_a_variacao",
        "odd_empate_variacao",
        "odd_b_variacao",
        "movimento_mercado",
        "favoritismo_aumentou",
    }

    if not colunas_necessarias.issubset(historico.columns):
        return pd.DataFrame()

    def contar_movimentos(serie, valor):
        return (serie == valor).sum()

    resumo = (
        historico.groupby("id_odds_api")
        .agg(
            odd_a_variacao_media=("odd_a_variacao", "mean"),
            odd_empate_variacao_media=("odd_empate_variacao", "mean"),
            odd_b_variacao_media=("odd_b_variacao", "mean"),
            casas_favoritismo_time_a=(
                "movimento_mercado",
                lambda serie: contar_movimentos(serie, "favoritismo_time_a_aumentou"),
            ),
            casas_favoritismo_time_b=(
                "movimento_mercado",
                lambda serie: contar_movimentos(serie, "favoritismo_time_b_aumentou"),
            ),
            casas_empate_mais_provavel=(
                "movimento_mercado",
                lambda serie: contar_movimentos(serie, "empate_ficou_mais_provavel"),
            ),
            casas_mercado_estavel=(
                "movimento_mercado",
                lambda serie: contar_movimentos(serie, "mercado_estavel"),
            ),
        )
        .reset_index()
    )

    resumo["favoritismo_movimento"] = resumo.apply(classificar_favoritismo_movimento, axis=1)
    return resumo


def classificar_favoritismo_movimento(row):
    movimentos = {
        "time_a": row["casas_favoritismo_time_a"],
        "empate": row["casas_empate_mais_provavel"],
        "time_b": row["casas_favoritismo_time_b"],
    }
    maior = max(movimentos.values())

    if maior == 0:
        return "sem_movimento_relevante"

    vencedores = [nome for nome, valor in movimentos.items() if valor == maior]
    if len(vencedores) > 1:
        return "movimento_dividido"

    return f"movimento_favorece_{vencedores[0]}"


def resumir_odds(arquivo_entrada=ODDS_COPA_CSV, arquivo_saida=ODDS_RESUMO_CSV):
    garantir_data_dir()

    df = pd.read_csv(arquivo_entrada)

    df = df.dropna(subset=["odd_a", "odd_empate", "odd_b"])

    df["prob_a_bruta"] = 1 / df["odd_a"]
    df["prob_empate_bruta"] = 1 / df["odd_empate"]
    df["prob_b_bruta"] = 1 / df["odd_b"]

    soma = df["prob_a_bruta"] + df["prob_empate_bruta"] + df["prob_b_bruta"]

    df["prob_a"] = df["prob_a_bruta"] / soma
    df["prob_empate"] = df["prob_empate_bruta"] / soma
    df["prob_b"] = df["prob_b_bruta"] / soma

    resumo = (
        df.groupby(["id_odds_api", "data_hora_utc", "time_a", "time_b"], as_index=False)
        .agg(
            qtd_casas=("fonte", "count"),
            odd_a_media=("odd_a", "mean"),
            odd_empate_media=("odd_empate", "mean"),
            odd_b_media=("odd_b", "mean"),
            dispersao_odd_a=("odd_a", "std"),
            dispersao_odd_empate=("odd_empate", "std"),
            dispersao_odd_b=("odd_b", "std"),
            prob_a_media=("prob_a", "mean"),
            prob_empate_media=("prob_empate", "mean"),
            prob_b_media=("prob_b", "mean"),
            atualizado_em_max=("atualizado_em", "max"),
        )
    )

    for coluna in ["dispersao_odd_a", "dispersao_odd_empate", "dispersao_odd_b"]:
        resumo[coluna] = resumo[coluna].fillna(0)

    resumo["dispersao_media_mercado"] = resumo[
        ["dispersao_odd_a", "dispersao_odd_empate", "dispersao_odd_b"]
    ].mean(axis=1)
    resumo["score_mercado_a"] = resumo["prob_a_media"]
    resumo["score_mercado_empate"] = resumo["prob_empate_media"]
    resumo["score_mercado_b"] = resumo["prob_b_media"]
    resumo["confianca_mercado"] = resumo.apply(calcular_confianca_mercado, axis=1)

    movimento = carregar_movimento_mercado()
    if not movimento.empty:
        resumo = resumo.merge(movimento, on="id_odds_api", how="left")
    else:
        resumo["odd_a_variacao_media"] = pd.NA
        resumo["odd_empate_variacao_media"] = pd.NA
        resumo["odd_b_variacao_media"] = pd.NA
        resumo["casas_favoritismo_time_a"] = 0
        resumo["casas_favoritismo_time_b"] = 0
        resumo["casas_empate_mais_provavel"] = 0
        resumo["casas_mercado_estavel"] = 0
        resumo["favoritismo_movimento"] = "sem_historico"

    resumo = enriquecer_com_elo(resumo)
    resumo = enriquecer_com_sinais_placar(resumo)
    resumo["resultado_mais_provavel"] = resumo.apply(resultado_mais_provavel, axis=1)
    resumo.to_csv(arquivo_saida, index=False, encoding="utf-8-sig")

    print(f"Arquivo {arquivo_saida} criado.")
    print("Total de jogos:", len(resumo))
    print(resumo.head(20))


def gerar_palpites(arquivo_entrada=ODDS_RESUMO_CSV, arquivo_saida=PALPITES_ODDS_CSV):
    garantir_data_dir()

    df = pd.read_csv(arquivo_entrada)

    palpites = pd.DataFrame()
    palpites["id_odds_api"] = df["id_odds_api"]
    palpites["data_hora_utc"] = df["data_hora_utc"]
    palpites["time_a"] = df["time_a"]
    palpites["time_b"] = df["time_b"]
    palpites["resultado_sugerido"] = df.apply(gerar_resultado, axis=1)
    palpites["placar_sugerido"] = df.apply(gerar_placar, axis=1)
    palpites["confianca"] = df.apply(calcular_confianca, axis=1)
    palpites["confianca_placar"] = df.apply(calcular_confianca_placar, axis=1)
    palpites["criterio_placar"] = df.apply(gerar_criterio_placar, axis=1)
    palpites["prob_a_media"] = df["prob_a_media"]
    palpites["prob_empate_media"] = df["prob_empate_media"]
    palpites["prob_b_media"] = df["prob_b_media"]
    palpites["score_mercado_a"] = df["score_mercado_a"]
    palpites["score_mercado_empate"] = df["score_mercado_empate"]
    palpites["score_mercado_b"] = df["score_mercado_b"]
    palpites["confianca_mercado"] = df["confianca_mercado"]
    palpites["favoritismo_movimento"] = df["favoritismo_movimento"]
    palpites["elo_pontos_a"] = df["elo_pontos_a"]
    palpites["elo_pontos_b"] = df["elo_pontos_b"]
    palpites["diferenca_elo_pontos"] = df["diferenca_elo_pontos"]
    palpites["favorito_elo"] = df["favorito_elo"]
    palpites["status_elo"] = df["status_elo"]
    palpites["linha_gols_referencia"] = df["linha_gols_referencia"]
    palpites["prob_over_referencia"] = df["prob_over_referencia"]
    palpites["prob_under_referencia"] = df["prob_under_referencia"]
    palpites["tendencia_gols"] = df["tendencia_gols"]
    palpites["time_handicap_favorito"] = df["time_handicap_favorito"]
    palpites["handicap_favorito"] = df["handicap_favorito"]
    palpites["odd_handicap_favorito"] = df["odd_handicap_favorito"]
    palpites["forca_handicap"] = df["forca_handicap"]
    palpites["criterio"] = "odds_h2h_media_normalizada_movimento_mercado"
    palpites["status_revisao"] = "pendente"

    palpites.to_csv(arquivo_saida, index=False, encoding="utf-8-sig")

    print(f"Arquivo {arquivo_saida} criado.")
    print("Total de palpites:", len(palpites))
    print(palpites.head(20))


def main():
    comando = sys.argv[1] if len(sys.argv) > 1 else "gerar"

    if comando == "resumir":
        resumir_odds()
    elif comando == "gerar":
        gerar_palpites()
    else:
        raise SystemExit(f"Comando invalido para modelo de palpites: {comando}")


if __name__ == "__main__":
    main()
