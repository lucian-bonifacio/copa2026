# VALIDACOES

Registro detalhado de validacoes, execucoes autorizadas e resultados relevantes das etapas do roadmap.

Este arquivo complementa o `ROADMAP.md`. O roadmap deve manter o resumo, status, tarefas, gates e proximos passos. Detalhes maiores de comandos, resultados locais, consumo de creditos e observacoes de validacao devem ficar aqui.

## 2. Consolidar a Automacao Atual

Ajuste no orquestrador:

- `src/atualizar_tudo.py` passou a executar `python -m src.apis.football_data salvar` antes de buscar odds.
- Motivo: a etapa de Google Sheets atualiza a aba `jogos` a partir de `data/jogos_copa.csv`; quando esse arquivo nao existia, o fluxo falhava na etapa final.
- O fluxo principal passou de 5 para 6 etapas.
- Nenhuma chamada externa foi executada durante a validacao deste ajuste.

Validacao feita:

```powershell
.\.venv\Scripts\python.exe -m py_compile src/atualizar_tudo.py
```

## 3. Melhorar Estrutura do Codigo

Validacao feita:

```powershell
.\.venv\Scripts\python.exe -m py_compile ...
```

Resumo:

- Estrutura `src/` validada com compilacao de sintaxe pelo Python da `.venv`.
- Wrappers Python da raiz foram removidos.
- Artefatos gerados foram centralizados em `data/`.

## 4. Criar Historico Mais Inteligente

Validacao feita:

```powershell
.\.venv\Scripts\python.exe -m src.utils.historico
```

Resultado local:

- `data/odds_historico.csv` criado com 2462 linhas na primeira execucao.
- Uma nova foto foi salva em `data/historico_odds/`.
- Como a coleta atual era igual a ultima foto anterior, os movimentos ficaram como `mercado_estavel`.

## 5. Melhorar Score Baseado em Odds e Mercado

Validacao feita:

```powershell
.\.venv\Scripts\python.exe -m src.palpites.modelo resumir
.\.venv\Scripts\python.exe -m src.palpites.modelo gerar
```

Resultado:

- `data/odds_resumo.csv` passou a incluir score de mercado, dispersao, variacao media das odds e movimento agregado.
- `data/palpites_odds.csv` passou a incluir `score_mercado_*`, `confianca_mercado` e `favoritismo_movimento`.
- O criterio dos palpites passou a indicar uso de odds normalizadas e movimento de mercado.

## 6. Expandir The Odds API

### Mapeamento inicial de mercados

Execucao real autorizada e feita:

- Comando executado: `python -m src.apis.odds_api mercados 3`.
- Foram mapeados 3 eventos.
- Custo total observado: 3 creditos, 1 por evento.
- Creditos restantes apos o teste: 481.
- Arquivo gerado: `data/odds_mercados.csv`.
- Resultado: 676 linhas, 38 bookmakers e 58 mercados distintos.
- Mercados uteis encontrados incluem `totals`, `btts`, `spreads`, `team_totals`, `draw_no_bet`, `double_chance` e mercados `lay`.

### Mapeamento ampliado de mercados

Execucao ampliada autorizada e feita:

- Comando executado: `python -m src.apis.odds_api mercados 10`.
- Foram mapeados 10 eventos.
- Custo total observado: 10 creditos, 1 por evento.
- Creditos restantes apos o teste: 471.
- Arquivo atualizado: `data/odds_mercados.csv`.
- Resultado: 2105 linhas, 38 bookmakers e 58 mercados distintos.
- Mercados com melhor cobertura: `h2h`, `h2h_3_way`, `totals`, `btts`, `alternate_totals`, `draw_no_bet`, `double_chance`, `spreads`.

### Odds avancadas

Execucao real de odds avancadas:

- Primeira tentativa com `h2h,totals,btts,spreads` retornou erro `INVALID_MARKET` para `btts` e nao consumiu creditos.
- Coleta ajustada para `h2h,totals,spreads` em regioes `eu,uk`.
- Comando executado: `python -m src.apis.odds_api odds-avancadas`.
- Custo observado: 6 creditos.
- Creditos restantes apos a chamada: 465.
- Arquivo gerado: `data/odds_avancadas.csv`.
- Resultado: 9977 linhas, 72 eventos.
- Mercados retornados: `h2h`, `totals`, `spreads`, `h2h_lay`.
- Comando executado: `python -m src.apis.odds_api resumir-avancadas`.
- Arquivo gerado: `data/odds_avancadas_resumo.csv`.
- Resultado: 1060 linhas resumidas, 72 eventos.

Observacao:

- `btts` apareceu no mapeamento por evento, mas a The Odds API rejeitou esse mercado no endpoint geral `/odds` com erro `INVALID_MARKET`. A chamada nao consumiu creditos.
- BTTS deve ser tratado futuramente via endpoint por evento, se fizer sentido.

## 13. Melhorar Previsibilidade dos Componentes do Bolao

Escopo executado:

- Adicionadas colunas explicitas de previsao por componente em `data/palpites_odds.csv`.
- Mantidas as colunas anteriores de palpite para compatibilidade: `resultado_sugerido`, `placar_sugerido`, `confianca`, `confianca_placar`, `criterio` e `criterio_placar`.
- As previsoes de gols, diferenca e total sao derivadas do `placar_sugerido`.
- As fontes de previsao sao registradas em colunas separadas.
- Nenhuma nova fonte externa foi consultada.
- Nenhuma atualizacao no Google Sheets foi executada nesta etapa.

Colunas adicionadas:

```text
previsao_resultado
previsao_placar
previsao_gols_time_a
previsao_gols_time_b
previsao_gols_vencedor
previsao_gols_perdedor
previsao_diferenca_gols
previsao_total_gols
previsao_tendencia_gols
confianca_resultado
confianca_gols
fonte_previsao_resultado
fonte_previsao_gols
fonte_previsao_placar
```

Validacoes feitas:

```powershell
.\.venv\Scripts\python.exe -m py_compile src/palpites/modelo.py src/palpites/placar.py
```

Validacao com fixture temporario em `/tmp`:

- Entrada temporaria criada com uma linha de `odds_resumo`.
- `src.palpites.modelo.gerar_palpites` executado apontando para arquivos temporarios.
- Saida gerada com 46 colunas.
- Colunas de previsao por componente foram criadas e preenchidas.

Resultado observado no fixture:

```text
previsao_resultado: time_a
previsao_placar: 3x1
previsao_gols_time_a: 3
previsao_gols_time_b: 1
previsao_gols_vencedor: 3
previsao_gols_perdedor: 1
previsao_diferenca_gols: 2
previsao_total_gols: 4
previsao_tendencia_gols: mais_gols
confianca_resultado: alta
confianca_gols: media
fonte_previsao_gols: placar_por_regra+totals+spreads
fonte_previsao_placar: odds_h2h+totals_mais_gols+spread_forte
```

Validacao pendente:

- `python -m src.palpites.modelo gerar` contra os CSVs reais nao foi executado porque `data/odds_resumo.csv` nao existe neste workspace.
