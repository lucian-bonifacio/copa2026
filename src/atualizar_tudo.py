import subprocess
import sys
from time import perf_counter


ETAPAS = [
    ("Salvar jogos", ["-m", "src.apis.football_data", "salvar"]),
    ("Buscar odds", ["-m", "src.apis.odds_api"]),
    ("Salvar historico", ["-m", "src.utils.historico"]),
    ("Resumir odds", ["-m", "src.palpites.modelo", "resumir"]),
    ("Gerar palpites", ["-m", "src.palpites.modelo", "gerar"]),
    ("Atualizar historico de previsoes", ["-m", "src.palpites.historico_previsoes"]),
    ("Atualizar Google Sheets", ["-m", "src.sheets.google_sheets"]),
]


def formatar_tempo(segundos):
    return f"{segundos:.1f}s"


def main():
    tempo_total_inicio = perf_counter()
    total_etapas = len(ETAPAS)

    print("[INICIO] Fluxo completo iniciado.")

    for indice, (nome, comando) in enumerate(ETAPAS, start=1):
        inicio = perf_counter()
        print(f"\n[{indice}/{total_etapas}] {nome}...")
        print(f"[INFO] Executando: python {' '.join(comando)}")

        resultado = subprocess.run([sys.executable, *comando])
        duracao = perf_counter() - inicio

        if resultado.returncode != 0:
            print(f"[ERRO] Etapa falhou: {nome}")
            print(f"[ERRO] Comando: python {' '.join(comando)}")
            print(f"[ERRO] Codigo de saida: {resultado.returncode}")
            print(f"[ERRO] Tempo ate falhar: {formatar_tempo(duracao)}")
            raise SystemExit(resultado.returncode)

        print(f"[OK] Etapa concluida: {nome} ({formatar_tempo(duracao)})")

    tempo_total = perf_counter() - tempo_total_inicio

    print(f"\n[OK] Fluxo completo finalizado em {formatar_tempo(tempo_total)}.")


if __name__ == "__main__":
    main()
