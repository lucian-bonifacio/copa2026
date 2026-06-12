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

## 14. Revisao Manual e Mudanca de Direcao

Escopo executado inicialmente:

- Adicionada rotina para criar/atualizar a aba `revisao_palpites`.
- A aba e montada a partir de `data/palpites_odds.csv`.
- Antes de atualizar a aba, o script le os campos manuais existentes e os reaplica por `id_odds_api`.
- A aba `palpites_bolao` continua sendo uma saida automatica completa.
- A aba `revisao_palpites` passa a ser a area recomendada para revisao manual.

Campos manuais preservados:

```text
palpite_final
placar_final
status_revisao
observacao_manual
```

Validacoes feitas:

```powershell
.\.venv\Scripts\python.exe -m py_compile src\sheets\google_sheets.py
```

Validacao local com `data/palpites_odds.csv`:

- A funcao `montar_revisao_palpites` foi executada com uma linha real do CSV e campos manuais simulados.
- Resultado: `palpite_final`, `placar_final`, `status_revisao` e `observacao_manual` foram preservados corretamente.

Execucao no Google Sheets:

```powershell
.\.venv\Scripts\python.exe -c "from src.sheets.google_sheets import abrir_planilha, atualizar_revisao_palpites; atualizar_revisao_palpites(abrir_planilha())"
```

Resultado:

- A primeira tentativa foi bloqueada pelo sandbox por acesso de rede ao Google.
- A execucao autorizada foi concluida.
- A aba `revisao_palpites` foi atualizada a partir de `data/palpites_odds.csv` preservando campos manuais.

Validacao pendente:

- Usuario conferir visualmente a aba `revisao_palpites` na planilha.

Decisao posterior:

- O usuario decidiu que campos manuais nao sao prioridade para o objetivo atual.
- O foco passa a ser previsao automatica, resultado real e base historica para estudos futuros.
- A rotina `revisao_palpites` foi removida de `src/sheets/google_sheets.py`.
- A coluna `status_revisao` foi removida da geracao de `data/palpites_odds.csv`.
- A aba pode continuar existindo na planilha como resquicio manual, mas nao e mais criada nem atualizada pelo projeto.
- A proxima etapa deve ser planejada com o usuario antes de implementar `historico_previsoes`.

Validacao apos remocao:

```powershell
.\.venv\Scripts\python.exe -m py_compile src\sheets\google_sheets.py src\palpites\modelo.py
.\.venv\Scripts\python.exe -m src.palpites.modelo gerar
```

Resultado:

- `data/palpites_odds.csv` foi regenerado com 71 palpites.
- A saida passou a ter 45 colunas, sem `status_revisao`.

## 15. Formatar Google Sheets Automaticamente

Escopo executado:

- Adicionada preparacao dos dados antes do envio ao Google Sheets.
- Datas e horas das abas automaticas sao convertidas para o fuso `America/Sao_Paulo`.
- Os nomes das colunas sao preservados; o fuso correto fica no valor exibido, nao no nome da coluna.
- Valores decimais sao arredondados para no maximo 4 casas.
- Adicionada formatacao visual basica: primeira linha congelada, filtro, cabecalho destacado, alinhamento no topo, quebra de texto e larguras iniciais.

Abas incluidas:

```text
jogos
odds
odds_resumo
palpites_bolao
```

Validacoes locais:

```powershell
.\.venv\Scripts\python.exe -m py_compile src\sheets\google_sheets.py
```

Exemplo validado com `data/palpites_odds.csv`:

```text
data_hora_utc     prob_a_media  prob_empate_media  prob_b_media
14/06/2026 20:00        0.2678              0.337        0.3952
```

Exemplo validado com `data/odds_copa.csv`:

```text
data_hora_utc: 11/06/2026 23:00
atualizado_em: 11/06/2026 18:25
```

Validacao pendente:

- Conferir visualmente as quatro abas automaticas na planilha.

Execucao no Google Sheets:

```powershell
.\.venv\Scripts\python.exe -c "from src.sheets.google_sheets import ABAS_CSV, abrir_planilha, atualizar_aba; sh = abrir_planilha(); [atualizar_aba(sh, nome, arquivo) for nome, arquivo in ABAS_CSV]"
```

Resultado:

- `jogos` atualizada.
- `odds` atualizada.
- `odds_resumo` atualizada.
- `palpites_bolao` atualizada.

## 14. Criar Historico de Previsoes

Decisoes do usuario:

- Usar apenas uma previsao historica por jogo, sem multiplos snapshots.
- Usar janela padrao de 3 horas antes do jogo.
- Antes da janela, a previsao pode ser atualizada.
- A partir da janela de 3 horas, a previsao fica congelada.
- Depois do jogo comecar, a previsao nao deve ser alterada; apenas resultados reais e metricas podem ser atualizados.
- Salvar em CSV local e Google Sheets.

Implementado:

- Criado `src/palpites/historico_previsoes.py`.
- Criado caminho `HISTORICO_PREVISOES_CSV` em `src/utils/config.py`.
- Adicionada etapa `python -m src.palpites.historico_previsoes` no orquestrador.
- Adicionada aba `historico_previsoes` ao exportador do Google Sheets.
- O exportador passa a criar a aba se ela nao existir.
- Datas de controle do historico tambem sao formatadas no horario local configurado na planilha.
- Removidas as colunas `registro_criado_em` e `congelada_em`; `registro_atualizado_em` e `previsao_congelada` sao suficientes para auditoria operacional.
- A associacao com `jogos_copa.csv` usa times e `data_hora_utc`, com fallback por times.

Validacoes locais:

```powershell
.\.venv\Scripts\python.exe -m py_compile src\palpites\historico_previsoes.py src\atualizar_tudo.py src\sheets\google_sheets.py src\utils\config.py
.\.venv\Scripts\python.exe -m src.palpites.historico_previsoes
```

Resultado local:

- `data/historico_previsoes.csv` atualizado.
- Total de previsoes historicas: 71.
- Previsoes congeladas: 0.
- Resultado esperado no momento da validacao, pois os jogos ainda nao estavam dentro da janela de 3 horas.

Colunas principais verificadas:

```text
id_odds_api
data_jogo
time_a
time_b
resultado_sugerido
placar_sugerido
previsao_congelada
janela_congelamento_horas
resultado_real
```

Validacao pendente:

- Usuario conferir visualmente a aba `historico_previsoes` no Google Sheets.

Execucao no Google Sheets:

```powershell
.\.venv\Scripts\python.exe -c "from src.sheets.google_sheets import abrir_planilha, atualizar_aba; from src.utils.config import HISTORICO_PREVISOES_CSV; atualizar_aba(abrir_planilha(), 'historico_previsoes', HISTORICO_PREVISOES_CSV)"
```

Resultado:

- Aba `historico_previsoes` criada/atualizada a partir de `data/historico_previsoes.csv`.
- Apos ajuste de chave de jogo, o CSV foi regenerado e a aba foi atualizada novamente.
- Ajustado exportador para enviar `id_jogo` como identificador textual, evitando exibicao como `537352.0` na planilha.
- Ajustados nomes das colunas para nao usar sufixo de fuso; o horario local configurado continua aplicado aos valores exibidos.
- `data/historico_previsoes.csv` foi regenerado sem `registro_criado_em`, `congelada_em` e `data_jogo_brasilia`.
- A aba `historico_previsoes` foi atualizada novamente com os nomes finais das colunas.
