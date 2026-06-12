# 003 - Melhorar estrutura do codigo

Status: concluido

## Objetivo

Reduzir scripts soltos e organizar a logica principal em modulos dentro de `src/`.

## Escopo

- Criar estrutura modular em `src/`.
- Mover integracoes com APIs para `src/apis/`.
- Mover integracao com Google Sheets para `src/sheets/`.
- Mover regras de palpite para `src/palpites/`.
- Centralizar configuracoes e historico em `src/utils/`.
- Manter `python -m src.atualizar_tudo` como entrada principal.

## Criterios de Conclusao

- Modulos principais criados em `src/`.
- Wrappers Python da raiz removidos.
- Artefatos gerados centralizados em `data/`.
- Sintaxe validada com Python da `.venv`.

## Resumo da Execucao

Codigo reorganizado em estrutura modular, com entrada principal preservada e artefatos gerados centralizados em `data/`.

## Referencias

- `docs/VALIDACOES.md#3-melhorar-estrutura-do-codigo`
