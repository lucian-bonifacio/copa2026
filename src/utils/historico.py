from datetime import datetime
from pathlib import Path
import shutil

import pandas as pd

from src.utils.config import HISTORICO_ODDS_DIR, ODDS_COPA_CSV, ODDS_HISTORICO_CSV


CHAVES_COMPARACAO = ["id_odds_api", "fonte", "mercado"]
COLUNAS_ODDS = ["odd_a", "odd_empate", "odd_b"]


def carregar_historico_anterior(arquivo_historico=ODDS_HISTORICO_CSV, pasta_snapshots=HISTORICO_ODDS_DIR):
    arquivo_historico = Path(arquivo_historico)
    pasta_snapshots = Path(pasta_snapshots)

    if arquivo_historico.exists():
        historico = pd.read_csv(arquivo_historico)
        if not historico.empty and "coletado_em" in historico.columns:
            ultima_coleta = historico["coletado_em"].max()
            return historico[historico["coletado_em"] == ultima_coleta].copy()

    if pasta_snapshots.exists():
        snapshots = sorted(pasta_snapshots.glob("odds_copa_*.csv"))
        if snapshots:
            return pd.read_csv(snapshots[-1])

    return pd.DataFrame()


def listar_colunas_alteradas(row, operador):
    colunas = []

    for coluna in COLUNAS_ODDS:
        variacao = row.get(f"{coluna}_variacao")
        if pd.notna(variacao) and operador(variacao):
            colunas.append(coluna)

    return ",".join(colunas)


def classificar_movimento(row):
    if any(pd.isna(row.get(f"{coluna}_anterior")) for coluna in COLUNAS_ODDS):
        return "sem_historico"

    if any(pd.isna(row.get(coluna)) for coluna in COLUNAS_ODDS):
        return "odds_incompletas"

    variacoes = {coluna: row.get(f"{coluna}_variacao", 0) for coluna in COLUNAS_ODDS}

    if all(abs(valor) < 0.01 for valor in variacoes.values()):
        return "mercado_estavel"

    quedas = {coluna: abs(valor) for coluna, valor in variacoes.items() if valor < -0.01}

    if not quedas:
        return "odds_subiram"

    principal = max(quedas, key=quedas.get)

    if principal == "odd_a":
        return "favoritismo_time_a_aumentou"
    if principal == "odd_b":
        return "favoritismo_time_b_aumentou"
    if principal == "odd_empate":
        return "empate_ficou_mais_provavel"

    return "mercado_alterado"


def preparar_registro_historico(df_atual, df_anterior, coletado_em):
    atual = df_atual.copy()
    atual["coletado_em"] = coletado_em

    colunas_anteriores = CHAVES_COMPARACAO + COLUNAS_ODDS
    if df_anterior.empty or not set(colunas_anteriores).issubset(df_anterior.columns):
        for coluna in COLUNAS_ODDS:
            atual[f"{coluna}_anterior"] = pd.NA
    else:
        anterior = df_anterior[colunas_anteriores].copy()
        anterior = anterior.rename(columns={coluna: f"{coluna}_anterior" for coluna in COLUNAS_ODDS})
        atual = atual.merge(anterior, on=CHAVES_COMPARACAO, how="left")

    for coluna in COLUNAS_ODDS:
        atual[f"{coluna}_variacao"] = atual[coluna] - atual[f"{coluna}_anterior"]

    atual["movimento_mercado"] = atual.apply(classificar_movimento, axis=1)
    atual["odd_subiu"] = atual.apply(lambda row: listar_colunas_alteradas(row, lambda valor: valor > 0.01), axis=1)
    atual["odd_caiu"] = atual.apply(lambda row: listar_colunas_alteradas(row, lambda valor: valor < -0.01), axis=1)
    atual["favoritismo_aumentou"] = atual["movimento_mercado"].where(
        atual["movimento_mercado"].isin(
            [
                "favoritismo_time_a_aumentou",
                "favoritismo_time_b_aumentou",
                "empate_ficou_mais_provavel",
            ]
        ),
        "",
    )

    colunas_base = ["coletado_em"] + [coluna for coluna in atual.columns if coluna != "coletado_em"]
    return atual[colunas_base]


def atualizar_historico_consolidado(
    arquivo_origem=ODDS_COPA_CSV,
    arquivo_historico=ODDS_HISTORICO_CSV,
    pasta_snapshots=HISTORICO_ODDS_DIR,
    coletado_em=None,
):
    arquivo_origem = Path(arquivo_origem)
    arquivo_historico = Path(arquivo_historico)

    if not arquivo_origem.exists():
        raise FileNotFoundError(f"Arquivo {arquivo_origem} nao encontrado.")

    coletado_em = coletado_em or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    df_atual = pd.read_csv(arquivo_origem)
    df_anterior = carregar_historico_anterior(arquivo_historico, pasta_snapshots)
    registro = preparar_registro_historico(df_atual, df_anterior, coletado_em)

    if arquivo_historico.exists():
        historico = pd.read_csv(arquivo_historico)
        historico = pd.concat([historico, registro], ignore_index=True)
    else:
        historico = registro

    historico.to_csv(arquivo_historico, index=False, encoding="utf-8-sig")

    print(f"Historico consolidado atualizado em: {arquivo_historico}")
    print("Linhas adicionadas:", len(registro))
    print("Movimentos encontrados:")
    print(registro["movimento_mercado"].value_counts())


def salvar_historico_odds(arquivo_origem=ODDS_COPA_CSV, pasta_destino=HISTORICO_ODDS_DIR):
    origem = Path(arquivo_origem)

    if not origem.exists():
        raise FileNotFoundError(f"Arquivo {arquivo_origem} nao encontrado.")

    pasta = Path(pasta_destino)
    pasta.mkdir(exist_ok=True)

    agora = datetime.now().strftime("%Y%m%d_%H%M%S")
    destino = pasta / f"odds_copa_{agora}.csv"

    atualizar_historico_consolidado(
        arquivo_origem=origem,
        arquivo_historico=ODDS_HISTORICO_CSV,
        pasta_snapshots=pasta,
        coletado_em=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    )

    shutil.copy(origem, destino)

    print(f"Historico salvo em: {destino}")


if __name__ == "__main__":
    salvar_historico_odds()
