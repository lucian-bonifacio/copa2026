# 002 - Consolidar a automacao atual

Status: concluido

## Objetivo

Manter `python -m src.atualizar_tudo` como comando unico e confiavel para atualizar o fluxo principal.

## Escopo

- Gerar `data/jogos_copa.csv` antes de atualizar o Google Sheets.
- Padronizar logs de inicio, fim, erro e tempo de execucao.
- Mostrar creditos restantes da Odds API.
- Garantir que erro em etapa interrompa o fluxo com mensagem clara.

## Criterios de Conclusao

- `src/atualizar_tudo.py` executa as etapas principais em ordem.
- Logs padronizados mostram comando, status, erro e duracao.
- Odds API informa status e creditos em linhas padronizadas.
- Sintaxe validada com Python da `.venv`.

## Resumo da Execucao

Fluxo consolidado com execucao unica, logs padronizados e parada clara em caso de erro.

## Referencias

- `docs/VALIDACOES.md#2-consolidar-a-automacao-atual`
