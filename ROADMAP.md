# ROADMAP

Plano de evolucao do projeto Bolao Copa do Mundo + Odds + Google Sheets.

Este arquivo organiza o que ja foi feito, o que ainda falta e a ordem recomendada de execucao.

## Status Atual

MVP 1 concluido:

- coleta de odds funcionando;
- historico simples de odds funcionando;
- resumo de odds funcionando;
- geracao inicial de palpites funcionando;
- atualizacao do Google Sheets funcionando;
- comando unico `python -m src.atualizar_tudo` funcionando;
- `README.md` criado;
- `.gitignore` criado;
- `.env` e `service_account.json` protegidos no Git;
- `requirements.txt` criado;
- `AGENTS.md` criado.
- politica inicial de Git definida: CSVs e `data/historico_odds/` ficam fora do Git.

## Ordem Recomendada

1. Organizar e proteger o projeto.
2. Consolidar a automacao atual.
3. Refatorar estrutura dos scripts.
4. Melhorar historico de odds.
5. Melhorar score baseado em odds e movimento de mercado.
6. Expandir The Odds API.
7. Analisar mercado exchange.
8. Avaliar Sportmonks Predictions API.
9. Avaliar Opta/Stats Perform.
10. Avaliar scraping controlado, como Forebet.
11. Melhorar modelo de palpite.
12. Melhorar placar sugerido.
13. Criar revisao manual na planilha.
14. Formatar Google Sheets automaticamente.
15. Criar pontuacao do bolao.
16. Automatizar no Windows.

## 1. Organizar o Projeto

Status: concluido.

Concluido:

- Criar `README.md`.
- Criar `.gitignore`.
- Proteger `.env`.
- Proteger `service_account.json`.
- Criar `requirements.txt`.
- Documentar comando principal:

```powershell
python -m src.atualizar_tudo
```

Politica definida:

- Manter `.env`, `service_account.json` e `.venv/` sempre fora do Git.
- Manter `data/*.csv` e `data/historico_odds/` fora do Git por enquanto.
- Versionar scripts, documentacao e arquivos de configuracao sem segredo.

Pendente para quando o usuario autorizar:

- Fazer primeiro commit local quando a estrutura estiver validada.

## 2. Consolidar a Automacao Atual

Status: concluido.

Objetivo: manter `python -m src.atualizar_tudo` como comando unico e confiavel.

Fluxo atual:

```text
buscar odds
  -> salvar historico
  -> resumir odds
  -> gerar palpites
  -> atualizar Google Sheets
```

Tarefas:

- [x] Manter `src/atualizar_tudo.py` como entrada principal.
- [x] Melhorar logs para mostrar claramente:
  - inicio de cada etapa;
  - fim de cada etapa;
  - erro de cada etapa;
  - tempo de execucao;
  - creditos restantes da Odds API.
- [x] Padronizar mensagens no terminal.
- [x] Garantir que erro em uma etapa pare o fluxo com mensagem clara.

Resultado esperado:

```text
[1/5] Buscando odds...
[OK] Odds atualizadas. Creditos restantes: 123
[2/5] Salvando historico...
[OK] Historico salvo em data/historico_odds/...
...
[OK] Fluxo completo finalizado.
```

Implementado:

- `src/atualizar_tudo.py` agora mostra inicio do fluxo, etapa atual, comando executado, sucesso, erro, codigo de saida e tempo de execucao.
- `src/apis/odds_api.py` agora mostra status da The Odds API e creditos em linhas padronizadas com prefixo `[ODDS_API]`.
- A validacao de sintaxe foi feita com o Python da `.venv`.

## 3. Melhorar Estrutura do Codigo

Status: concluido.

Objetivo: reduzir scripts soltos e organizar o projeto em modulos.

Estrutura desejada:

```text
src/
  apis/
    football_data.py
    odds_api.py
  sheets/
    google_sheets.py
  palpites/
    modelo.py
  utils/
    config.py
    historico.py
  atualizar_tudo.py
```

Possivel estrutura complementar:

```text
data/
  jogos_copa.csv
  odds_copa.csv
  odds_resumo.csv
  palpites_odds.csv
  historico_odds/
```

Tarefas:

- [x] Criar `src/`.
- [x] Mover integracoes com APIs para `src/apis/`.
- [x] Mover integracao com Google Sheets para `src/sheets/`.
- [x] Mover regras de palpite para `src/palpites/`.
- [x] Mover leitura de `.env`, caminhos e funcoes auxiliares para `src/utils/`.
- [x] Manter scripts antigos como comandos simples que chamam os modulos novos.
- [x] Definir `python -m src.atualizar_tudo` como comando principal.

Meta:

- Deixar o projeto menos dependente de varios scripts soltos.
- Facilitar manutencao, testes e evolucao.

Implementado:

- `src/apis/football_data.py`
- `src/apis/odds_api.py`
- `src/sheets/google_sheets.py`
- `src/palpites/modelo.py`
- `src/utils/config.py`
- `src/utils/historico.py`
- `src/atualizar_tudo.py`
- Remocao dos wrappers Python da raiz.
- Centralizacao dos artefatos gerados em `data/`.

Validacao feita:

```powershell
.\.venv\Scripts\python.exe -m py_compile ...
```

## 4. Criar Historico Mais Inteligente

Status: concluido.

Objetivo: alem de salvar fotos das odds, comparar movimento de mercado.

Status atual:

- `data/historico_odds/` guarda copias timestampadas de `data/odds_copa.csv`.

Implementado:

- [x] Manter `data/historico_odds/`.
- [x] Criar um arquivo consolidado:

```text
data/odds_historico.csv
```

- [x] Registrar cada coleta com timestamp.
- [x] Comparar odds atuais contra odds anteriores.
- [x] Criar colunas de movimento de mercado.

Colunas sugeridas:

```text
coletado_em
id_odds_api
time_a
time_b
fonte
odd_a
odd_empate
odd_b
odd_a_anterior
odd_empate_anterior
odd_b_anterior
odd_a_variacao
odd_empate_variacao
odd_b_variacao
movimento_mercado
odd_subiu
odd_caiu
favoritismo_aumentou
```

Exemplos de classificacao:

- `favoritismo_time_a_aumentou`
- `favoritismo_time_b_aumentou`
- `empate_ficou_mais_provavel`
- `mercado_estavel`
- `odds_incompletas`

Validacao feita:

```powershell
.\.venv\Scripts\python.exe -m src.utils.historico
```

Resultado local:

- `data/odds_historico.csv` criado com 2462 linhas na primeira execucao.
- Uma nova foto foi salva em `data/historico_odds/`.
- Como a coleta atual era igual a ultima foto anterior, os movimentos ficaram como `mercado_estavel`.

## 5. Melhorar Score Baseado em Odds e Mercado

Status: concluido.

Objetivo: usar melhor os dados que ja temos antes de adicionar fontes externas frageis.

Ranking FIFA foi removido do plano como fonte prioritaria. Ele e oficial, mas nao e a melhor fonte para prever jogos ou placares neste projeto. A prioridade passa a ser sinal estatistico e sinal de mercado.

Fontes internas atuais:

- odds atuais `h2h`;
- media das odds por jogo;
- probabilidade implicita normalizada;
- quantidade de casas usadas;
- historico de odds;
- movimento de mercado.

Tarefas:

- [x] Criar score de consenso das casas.
- [x] Medir dispersao entre bookmakers.
- [x] Medir movimento de odds por time.
- [x] Identificar aumento de favoritismo.
- [x] Criar um indicador de confianca baseado em mercado.
- [x] Registrar esses campos no resumo e no arquivo de palpites.

Colunas candidatas:

```text
score_mercado_a
score_mercado_empate
score_mercado_b
dispersao_odd_a
dispersao_odd_empate
dispersao_odd_b
movimento_mercado_resumo
favoritismo_movimento
confianca_mercado
```

Implementado:

- `data/odds_resumo.csv` agora inclui score de mercado, dispersao, variacao media das odds e movimento agregado.
- `data/palpites_odds.csv` agora inclui `score_mercado_*`, `confianca_mercado` e `favoritismo_movimento`.
- O criterio dos palpites passou a indicar uso de odds normalizadas e movimento de mercado.

Validacao feita:

```powershell
.\.venv\Scripts\python.exe -m src.palpites.modelo resumir
.\.venv\Scripts\python.exe -m src.palpites.modelo gerar
```

### World Football Elo Ratings

Status: concluido como integracao local.

Usar como fonte complementar de forca das selecoes.

Vantagens:

- Rankings Elo costumam funcionar bem para previsao de partidas.
- Pode complementar o sinal de mercado com forca historica/estatistica.

Implementado:

- Criado suporte local em `data/elo_selecoes.csv`.
- Criado modulo `src/palpites/elo.py`.
- `data/odds_resumo.csv` agora recebe colunas Elo quando os dados estiverem preenchidos.
- `data/palpites_odds.csv` propaga `elo_pontos_a`, `elo_pontos_b`, `diferenca_elo_pontos`, `favorito_elo` e `status_elo`.
- Sem scraping automatico nesta etapa.

Status atual dos dados:

- O template foi criado com as selecoes atuais.
- Como ainda nao ha pontuacoes preenchidas, os jogos ficam com `status_elo = elo_nao_informado`.

## 6. Expandir The Odds API

Status: concluido para o escopo atual.

Objetivo: extrair mais sinal de mercado da fonte que ja esta integrada antes de adicionar dependencias novas.

Possibilidades:

- [x] criar suporte para verificar mercados disponiveis por evento;
- [x] criar comando para coletar `h2h`, `totals` e `spreads`;
- [x] executar coleta real de odds avancadas;
- [ ] coletar odds por evento;
- [x] criar suporte para endpoint de eventos e mapear jogos com mais precisao;
- avaliar historico oficial da The Odds API, se o plano permitir;
- acompanhar custo de creditos por mercado/regiao;
- melhorar comparacao entre casas e dispersao.

Implementado:

- `python -m src.apis.odds_api eventos` salva eventos em `data/odds_eventos.csv`.
- `python -m src.apis.odds_api mercados 3` mapeia mercados para os 3 primeiros eventos locais e salva `data/odds_mercados.csv`.
- O comando `mercados` aceita um limite opcional para controlar custo e volume de chamadas.
- `python -m src.apis.odds_api odds-avancadas` busca `h2h,totals,spreads` e salva `data/odds_avancadas.csv`.
- `python -m src.apis.odds_api resumir-avancadas` resume odds avancadas em `data/odds_avancadas_resumo.csv`.
- `src/palpites/placar.py` usa `totals` e `spreads` ja coletados para melhorar o placar sugerido.

Execucao real autorizada e feita:

- Comando executado: `python -m src.apis.odds_api mercados 3`.
- Foram mapeados 3 eventos.
- Custo total observado: 3 creditos, 1 por evento.
- Creditos restantes apos o teste: 481.
- Arquivo gerado: `data/odds_mercados.csv`.
- Resultado: 676 linhas, 38 bookmakers e 58 mercados distintos.
- Mercados uteis encontrados incluem `totals`, `btts`, `spreads`, `team_totals`, `draw_no_bet`, `double_chance` e mercados `lay`.

Execucao ampliada autorizada e feita:

- Comando executado: `python -m src.apis.odds_api mercados 10`.
- Foram mapeados 10 eventos.
- Custo total observado: 10 creditos, 1 por evento.
- Creditos restantes apos o teste: 471.
- Arquivo atualizado: `data/odds_mercados.csv`.
- Resultado: 2105 linhas, 38 bookmakers e 58 mercados distintos.
- Mercados com melhor cobertura: `h2h`, `h2h_3_way`, `totals`, `btts`, `alternate_totals`, `draw_no_bet`, `double_chance`, `spreads`.

Gate:

- Antes de consultar novos mercados ou historico pago, confirmar consumo de creditos e cobertura do plano.
- Nao executar chamadas de alto custo sem confirmacao expressa do usuario.

Proximo micro-passo recomendado:

```powershell
python -m src.apis.odds_api odds-avancadas
python -m src.apis.odds_api resumir-avancadas
```

Antes de executar, confirmar o custo esperado. Para odds avancadas, o custo tende a depender de mercados e regioes retornados. Com `h2h,totals,spreads` e regioes `eu,uk`, o teto teorico e 6 creditos se os 3 mercados vierem nas 2 regioes.

Observacao: `btts` apareceu no mapeamento por evento, mas a The Odds API rejeitou esse mercado no endpoint geral `/odds` com erro `INVALID_MARKET`. A chamada nao consumiu creditos. BTTS deve ser tratado futuramente via endpoint por evento, se fizer sentido.

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

Uso no modelo:

- `totals` passou a indicar tendencia de gols: `mais_gols`, `menos_gols` ou `neutro`.
- `spreads` passou a indicar forca do favorito: `leve`, `moderado`, `forte` ou `muito_forte`.
- O spread so reforca o placar quando confirma o mesmo favorito apontado pelo `h2h`.
- O arquivo `data/palpites_odds.csv` agora inclui colunas de auditoria para o placar.

## 7. Analisar Mercado Exchange

Objetivo: incorporar sinal de mercado negociado, separado das odds tradicionais de casas.

Fonte candidata principal:

- Betfair Exchange API, se houver conta, app key e permissao de uso.

Dados desejados:

- odds de back;
- odds de lay;
- liquidez;
- spread entre back e lay;
- volume negociado;
- movimento de mercado;
- comparacao exchange x casas.

Sinais possiveis:

```text
exchange_confirma_favorito
exchange_diverge_das_casas
baixa_liquidez
mercado_sem_volume
spread_alto
```

Saidas candidatas:

```text
data/exchange_odds.csv
data/exchange_resumo.csv
```

Planilha:

- atualizar ou preencher a aba `apostas_exchange`.

Gate:

- Exige decisao do usuario sobre fonte, conta, app key, termos de uso e limites de requisicao.
- Nao implementar coleta real sem acesso oficial/API.

## 8. Avaliar Sportmonks Predictions API

Objetivo: adicionar uma fonte de previsoes automatizavel por API.

Potencial:

- probabilidades;
- placar correto;
- over/under;
- BTTS;
- value bets.

Observacoes:

- Predictions API exige add-on pago segundo a documentacao.
- Probabilidades ficam disponiveis ate 21 dias antes do jogo, conforme a documentacao.
- Pode ser uma fonte forte para complementar odds e placar.

Gate:

- Exige conta, token, plano e confirmacao de custo.
- Nao implementar sem chave e confirmacao do usuario.

## 9. Avaliar Opta/Stats Perform

Objetivo: considerar uma fonte premium estatistica para probabilidade, contexto, xG, forca e modelos tipo supercomputer.

Recomendacao:

- Opta/Stats Perform e uma fonte estrategicamente forte.
- Implementar somente se houver acesso oficial/API, contrato ou dados estruturados permitidos.
- Evitar scraping de materias publicas como base principal do modelo.

Gate:

- Confirmar acesso, custo, termos e formato dos dados antes de qualquer implementacao.

## 10. Avaliar Scraping Controlado, como Forebet

Objetivo: avaliar fontes sem API oficial clara somente quando elas forem realmente uteis e com risco aceito.

Fonte candidata:

- Forebet, especialmente para placar provavel.

Riscos:

- layout pode mudar;
- pode haver bloqueio;
- pode haver restricoes de termos de uso;
- scraping pode quebrar silenciosamente.

Gate:

- Nao implementar scraping sem decisao explicita do usuario sobre fonte, frequencia, risco e termos.

### Opta Analyst / Supercomputer

Usar como fonte forte de probabilidade e forca das selecoes.

Vantagens:

- A Opta publica previsoes baseadas em simulacoes/modelos.
- Pode ajudar em probabilidade de avanco, favoritismo e contexto.

Risco:

- Pode exigir scraping ou coleta manual, dependendo da disponibilidade dos dados.

### Nate Silver / PELE

Usar como ranking/modelo estatistico de forca das selecoes.

Vantagens:

- Modelo estatistico conhecido.
- Pode ajudar como referencia independente.

Risco:

- Precisa validar disponibilidade, formato e licenca dos dados publicados.

### Forebet

Usar especialmente para placar provavel, quando disponivel.

Vantagens:

- Pode ajudar onde o `h2h` e fraco: previsao de placar.

Risco:

- Pode exigir scraping.
- Pode ter mudancas de layout.
- Precisa validar termos de uso antes de automatizar coleta.

Ordem sugerida para fontes externas:

1. Expandir The Odds API.
2. Analisar mercado exchange.
3. Avaliar Sportmonks Predictions API.
4. Avaliar Opta/Stats Perform.
5. Avaliar scraping controlado, como Forebet.
6. Manter Elo como complemento local/opcional.

## 11. Melhorar o Modelo de Palpite

Status atual:

```text
odds h2h -> resultado provavel
regra simples -> placar sugerido
```

Modelo desejado:

```text
odds + movimento de mercado + Elo + Opta + Forebet -> score ponderado
```

Peso inicial sugerido:

```text
60% odds/mercado
20% Opta
10% Elo
10% Forebet/contexto
```

Tarefas:

- Criar uma funcao de score por jogo.
- Normalizar fontes diferentes para escala comparavel.
- Registrar o score final no CSV.
- Registrar os componentes do score para auditoria.
- Permitir ajuste manual dos pesos.

Colunas sugeridas:

```text
score_odds
score_movimento_mercado
score_opta
score_elo
score_forebet
score_final_a
score_final_empate
score_final_b
fonte_score
```

Regra importante:

- O modelo deve explicar de onde veio a sugestao.
- Evitar palpite "caixa preta".

## 12. Melhorar Placar Sugerido

Status: primeira versao concluida usando odds avancadas.

Problema original:

- Odds `h2h` ajudam mais no resultado do que no placar.
- Na primeira implementacao, o placar era apenas uma regra simples baseada no favoritismo do `h2h`.

Implementado:

- Criado modulo dedicado `src/palpites/placar.py`.
- Integrado `data/odds_avancadas_resumo.csv` ao resumo de odds.
- Usado `totals` para estimar tendencia de gols.
- Usado `spreads` para estimar forca do favorito.
- Registrada justificativa do placar em `criterio_placar`.
- Registrada confianca especifica do placar em `confianca_placar`.
- Registradas colunas de auditoria:

```text
linha_gols_referencia
prob_over_referencia
prob_under_referencia
tendencia_gols
time_handicap_favorito
handicap_favorito
odd_handicap_favorito
forca_handicap
```

Fontes e criterios futuros para melhorar ainda mais:

- Forebet;
- historico de gols das selecoes;
- forca ofensiva;
- forca defensiva;
- regra conservadora;
- diferenca de favoritismo;
- chance estimada de empate.

Regras iniciais implementadas:

```text
totals com menos gols -> 1x0, 0x1, 2x0 ou 0x2
totals com mais gols -> 2x1, 1x2, 3x1 ou 1x3
spread forte ou muito forte -> aumenta chance de placar com margem maior
equilibrio/empate -> 1x1 ou 2x2, conforme tendencia de gols
```

Tarefas:

- [x] Separar logica de resultado e logica de placar.
- [x] Criar modulo dedicado para placar.
- [x] Registrar justificativa do placar sugerido.
- [x] Criar coluna `criterio_placar`.
- [x] Criar coluna `confianca_placar`.

Colunas implementadas:

```text
resultado_sugerido
placar_sugerido
confianca
confianca_placar
criterio
criterio_placar
```

## 13. Criar Aba de Revisao Manual

Objetivo: deixar claro que o sistema sugere, mas a decisao final e manual.

Na planilha, criar ou ajustar colunas:

```text
palpite_sugerido
palpite_final
status_revisao
observacao_manual
```

Status possiveis:

```text
pendente
revisado
alterado_manual
confirmado
```

Fluxo:

```text
sistema sugere
  -> usuario revisa
  -> usuario ajusta se necessario
  -> usuario confirma palpite final
```

Regra:

- A automacao nao deve sobrescrever `palpite_final` sem confirmacao.
- A automacao pode atualizar `palpite_sugerido`.

## 14. Formatar Google Sheets Automaticamente

Objetivo: aplicar formatacoes visuais e funcionais nas abas atualizadas pelo Python, com definicao manual das regras coluna por coluna junto com o usuario.

Importante:

- Esta etapa nao deve ser implementada sem decisao conjunta sobre a formatacao de cada aba.
- A automacao deve atualizar dados sem destruir formatacoes manuais fora das areas controladas.
- A formatacao deve melhorar leitura e revisao, sem esconder informacoes importantes.

Escopo inicial:

- congelar linha de cabecalho;
- aplicar filtros nas abas principais;
- destacar cabecalhos;
- ajustar largura de colunas;
- aplicar alinhamento e quebra de texto;
- formatar datas e horas de forma legivel;
- decidir se datas e horas devem aparecer em UTC ou horario local;
- formatar odds como numero decimal;
- formatar probabilidades como percentual;
- destacar colunas de confianca;
- destacar colunas de status de revisao;
- preservar campos manuais como `palpite_final` e `observacao_manual`;
- definir regras especificas por aba.

Abas candidatas:

- `jogos`
- `odds`
- `odds_resumo`
- `palpites_bolao`

Exemplos de decisoes que precisam ser feitas com o usuario:

- formato de data e hora: data completa, data curta, horario local ou UTC;
- colunas que devem ficar congeladas;
- cores para cabecalho;
- cores para `confianca`: alta, media, baixa;
- cores para `status_revisao`: pendente, revisado, alterado_manual, confirmado;
- quantidade de casas decimais em odds;
- formato de percentual em probabilidades;
- larguras de colunas principais.

Tarefas:

- Mapear colunas de cada aba.
- Definir formatacao coluna por coluna com o usuario.
- Criar funcoes de formatacao em `src/sheets/google_sheets.py` ou modulo futuro de Sheets.
- Aplicar formatacao apos atualizar os dados.
- Testar em uma aba primeiro antes de aplicar em todas.
- Documentar no `README.md` o que e formatado automaticamente.

## 15. Criar Sistema de Pontuacao do Bolao

Objetivo: medir desempenho dos palpites depois que os jogos comecarem.

Criar aba:

```text
pontuacao_bolao
```

Calcular:

- pontos por placar exato;
- pontos por resultado correto;
- pontos por aproximacao;
- ranking dos palpites;
- taxa de acerto do resultado;
- taxa de placar exato;
- desempenho por fase da Copa;
- desempenho por nivel de confianca.

Tarefas:

- Definir regra de pontuacao do bolao.
- Comparar `palpite_final` com placar real.
- Criar resumo de performance.
- Descobrir quais regras de palpite estao funcionando melhor.

## 16. Automatizar no Windows

Objetivo: rodar a atualizacao automaticamente quando o fluxo estiver estavel.

Ferramenta:

```text
Agendador de Tarefas do Windows
```

Quando fazer:

- Somente depois de validar manualmente por alguns dias.
- Somente depois de melhorar logs e tratamento de erros.

Rotina sugerida:

- Antes da Copa: rodar 1 vez por dia.
- Durante a Copa: rodar pela manha.
- Em dia de jogo: rodar algumas horas antes da partida.

Comando base:

```powershell
python -m src.atualizar_tudo
```

Antes de agendar:

- Confirmar caminho do Python da `.venv`.
- Confirmar diretorio de trabalho do projeto.
- Confirmar que `.env` e `service_account.json` estao disponiveis localmente.
- Confirmar que os logs deixam claro se a execucao falhou.

## Proximo Passo Imediato

Como a organizacao inicial, logs, estrutura `src/`, historico inteligente e score de mercado ja foram feitos, o proximo passo recomendado e:

1. Validar manualmente os novos placares gerados com `totals` e `spreads`.
2. Avaliar Exchange com Betfair API se houver acesso.
3. Avaliar Sportmonks Predictions API se houver interesse em plano pago.
4. Avaliar Opta/Stats Perform se houver acesso oficial/API.
5. Manter Elo como complemento local/opcional.

## Gates de Decisao

Regra operacional:

- Se uma etapa depender de decisao importante do usuario, credencial, acao externa, consumo relevante de API, alteracao no Google Sheets ou escolha de regra de negocio, a execucao deve parar em um gate.
- No gate, o agente deve explicar a decisao, listar as opcoes praticas e aguardar confirmacao expressa antes de continuar.
- Esta regra vale especialmente para fontes externas, formatacao do Google Sheets, alteracoes que possam sobrescrever dados manuais e automacoes agendadas.

## Checklist de Execucao

- [x] Criar `README.md`.
- [x] Criar `.gitignore`.
- [x] Proteger `.env`.
- [x] Proteger `service_account.json`.
- [x] Criar `requirements.txt`.
- [x] Criar `AGENTS.md`.
- [x] Documentar comando principal.
- [x] Decidir politica para CSVs no Git.
- [x] Melhorar logs da automacao.
- [x] Criar estrutura `src/`.
- [x] Consolidar historico em `odds_historico.csv`.
- [x] Comparar odds atuais x anteriores.
- [x] Melhorar score baseado em odds e movimento de mercado.
- [x] Expandir The Odds API.
- [ ] Analisar mercado exchange.
- [ ] Avaliar Sportmonks Predictions API.
- [ ] Avaliar Opta/Stats Perform.
- [ ] Avaliar scraping controlado, como Forebet.
- [x] Adicionar World Football Elo Ratings.
- [ ] Melhorar modelo ponderado de palpite.
- [x] Melhorar placar sugerido.
- [ ] Criar revisao manual na planilha.
- [ ] Formatar Google Sheets automaticamente.
- [ ] Criar pontuacao do bolao.
- [ ] Automatizar no Windows.
