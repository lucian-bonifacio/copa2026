# 005 - Melhorar score baseado em odds e mercado

Status: concluido

## Objetivo

Usar melhor os dados internos de odds, consenso das casas, dispersao e movimento de mercado antes de adicionar fontes externas frageis.

## Escopo

- Criar score de consenso das casas.
- Medir dispersao entre bookmakers.
- Medir movimento de odds por resultado.
- Identificar aumento de favoritismo.
- Criar indicador de confianca baseado em mercado.
- Integrar suporte local a Elo quando preenchido.

## Criterios de Conclusao

- `data/odds_resumo.csv` inclui scores, dispersao e movimento agregado.
- `data/palpites_odds.csv` inclui campos de mercado e movimento.
- Criterio dos palpites indica odds normalizadas e movimento de mercado.
- Elo local integrado sem scraping automatico.

## Resumo da Execucao

Score de mercado, dispersao, movimento agregado e suporte local a Elo foram incorporados aos resumos e palpites.

## Referencias

- `docs/VALIDACOES.md#5-melhorar-score-baseado-em-odds-e-mercado`
