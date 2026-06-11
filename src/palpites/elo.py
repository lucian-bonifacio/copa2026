import pandas as pd

from src.utils.config import ELO_SELECOES_CSV


COLUNAS_ELO = ["selecao", "elo_rank", "elo_pontos", "atualizado_em", "fonte"]


def normalizar_selecao(valor):
    if pd.isna(valor):
        return ""

    return str(valor).strip().casefold()


def carregar_elo(arquivo_elo=ELO_SELECOES_CSV):
    if not arquivo_elo.exists():
        return pd.DataFrame(columns=COLUNAS_ELO + ["selecao_normalizada"])

    elo = pd.read_csv(arquivo_elo)

    for coluna in COLUNAS_ELO:
        if coluna not in elo.columns:
            elo[coluna] = pd.NA

    elo = elo[COLUNAS_ELO].copy()
    elo["selecao_normalizada"] = elo["selecao"].apply(normalizar_selecao)
    elo["elo_rank"] = pd.to_numeric(elo["elo_rank"], errors="coerce")
    elo["elo_pontos"] = pd.to_numeric(elo["elo_pontos"], errors="coerce")

    return elo


def criar_template_elo(selecoes, arquivo_elo=ELO_SELECOES_CSV):
    if arquivo_elo.exists():
        return

    linhas = [{"selecao": selecao, "elo_rank": "", "elo_pontos": "", "atualizado_em": "", "fonte": ""} for selecao in selecoes]
    pd.DataFrame(linhas, columns=COLUNAS_ELO).to_csv(arquivo_elo, index=False, encoding="utf-8-sig")
    print(f"Template de Elo criado em: {arquivo_elo}")


def enriquecer_com_elo(resumo, arquivo_elo=ELO_SELECOES_CSV):
    selecoes = sorted(set(resumo["time_a"]).union(resumo["time_b"]))
    criar_template_elo(selecoes, arquivo_elo)

    elo = carregar_elo(arquivo_elo)

    if elo.empty:
        return adicionar_colunas_elo_vazias(resumo)

    elo_a = elo.rename(
        columns={
            "selecao": "elo_selecao_a",
            "elo_rank": "elo_rank_a",
            "elo_pontos": "elo_pontos_a",
            "atualizado_em": "elo_atualizado_em_a",
            "fonte": "fonte_elo_a",
            "selecao_normalizada": "time_a_normalizado",
        }
    )
    elo_b = elo.rename(
        columns={
            "selecao": "elo_selecao_b",
            "elo_rank": "elo_rank_b",
            "elo_pontos": "elo_pontos_b",
            "atualizado_em": "elo_atualizado_em_b",
            "fonte": "fonte_elo_b",
            "selecao_normalizada": "time_b_normalizado",
        }
    )

    resumo = resumo.copy()
    resumo["time_a_normalizado"] = resumo["time_a"].apply(normalizar_selecao)
    resumo["time_b_normalizado"] = resumo["time_b"].apply(normalizar_selecao)

    resumo = resumo.merge(
        elo_a[
            [
                "time_a_normalizado",
                "elo_rank_a",
                "elo_pontos_a",
                "elo_atualizado_em_a",
                "fonte_elo_a",
            ]
        ],
        on="time_a_normalizado",
        how="left",
    )
    resumo = resumo.merge(
        elo_b[
            [
                "time_b_normalizado",
                "elo_rank_b",
                "elo_pontos_b",
                "elo_atualizado_em_b",
                "fonte_elo_b",
            ]
        ],
        on="time_b_normalizado",
        how="left",
    )

    resumo = resumo.drop(columns=["time_a_normalizado", "time_b_normalizado"])
    resumo["diferenca_elo_pontos"] = resumo["elo_pontos_a"] - resumo["elo_pontos_b"]
    resumo["favorito_elo"] = resumo.apply(classificar_favorito_elo, axis=1)
    resumo["status_elo"] = resumo.apply(classificar_status_elo, axis=1)
    resumo["fonte_elo"] = resumo.apply(consolidar_fonte_elo, axis=1)

    return resumo


def adicionar_colunas_elo_vazias(resumo):
    resumo = resumo.copy()
    for coluna in [
        "elo_rank_a",
        "elo_pontos_a",
        "elo_rank_b",
        "elo_pontos_b",
        "diferenca_elo_pontos",
        "favorito_elo",
        "status_elo",
        "fonte_elo",
    ]:
        resumo[coluna] = pd.NA

    resumo["status_elo"] = "elo_nao_informado"
    return resumo


def classificar_favorito_elo(row):
    diferenca = row.get("diferenca_elo_pontos")

    if pd.isna(diferenca):
        return "sem_elo"
    if abs(diferenca) < 25:
        return "equilibrado"
    if diferenca > 0:
        return "time_a"
    return "time_b"


def classificar_status_elo(row):
    tem_a = pd.notna(row.get("elo_pontos_a"))
    tem_b = pd.notna(row.get("elo_pontos_b"))

    if tem_a and tem_b:
        return "elo_completo"
    if tem_a or tem_b:
        return "elo_parcial"
    return "elo_nao_informado"


def consolidar_fonte_elo(row):
    fontes = []
    for coluna in ["fonte_elo_a", "fonte_elo_b"]:
        valor = row.get(coluna)
        if pd.notna(valor) and str(valor).strip():
            fontes.append(str(valor).strip())

    return " | ".join(sorted(set(fontes)))
