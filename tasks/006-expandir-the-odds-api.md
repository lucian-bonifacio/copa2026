# 006 - Expandir The Odds API

Status: concluido

## Objetivo

Extrair mais sinal de mercado da The Odds API usando eventos, mercados disponiveis e odds avancadas.

## Escopo

- Criar comandos para eventos e mercados.
- Mapear mercados disponiveis por evento com limite controlado.
- Coletar odds avancadas `h2h`, `totals` e `spreads`.
- Resumir odds avancadas.
- Usar `totals` e `spreads` como sinais para placar sugerido.

## Criterios de Conclusao

- Eventos salvos em `data/odds_eventos.csv`.
- Mercados salvos em `data/odds_mercados.csv`.
- Odds avancadas salvas em `data/odds_avancadas.csv`.
- Resumo salvo em `data/odds_avancadas_resumo.csv`.
- Modelo usa sinais de gols e handicap quando disponiveis.

## Resumo da Execucao

The Odds API foi expandida para eventos, mapeamento de mercados e odds avancadas, com uso local de `totals` e `spreads` no placar sugerido.

## Referencias

- `docs/VALIDACOES.md#6-expandir-the-odds-api`
