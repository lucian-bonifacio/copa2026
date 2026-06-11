# Bolao Copa do Mundo + Odds + Google Sheets

Sistema semi-automatico para apoiar palpites em bolao da Copa do Mundo, analise de odds, acompanhamento de mercado e atualizacao de uma planilha Google Sheets.

O projeto nao faz apostas automaticas. Ele apenas coleta dados, organiza informacoes e gera sugestoes para revisao manual.

## Objetivo

O fluxo principal do projeto e:

1. Buscar jogos da Copa
2. Buscar odds da Copa
3. Salvar historico das odds
4. Resumir odds por jogo
5. Gerar palpites sugeridos
6. Atualizar Google Sheets automaticamente

Fluxo atual:

```text
API jogos
  -> data/jogos_copa.csv
API odds
  -> data/odds_copa.csv
  -> data/historico_odds/
  -> data/odds_resumo.csv
  -> data/palpites_odds.csv
  -> Google Sheets
```

## Fontes de Dados

### football-data.org

Usada para buscar jogos da Copa:

- data e hora;
- fase;
- grupo;
- times;
- placar, quando existir;
- status da partida.

Competicao usada:

```text
WC - FIFA World Cup
```

Arquivo gerado:

```text
jogos_copa.csv
```

### The Odds API

Usada para buscar odds da Copa.

Sport key:

```text
soccer_fifa_world_cup
```

Mercado base usado no MVP:

```text
h2h
```

O mercado `h2h` representa:

- vitoria do time A;
- empate;
- vitoria do time B.

Arquivos gerados:

```text
odds_copa.csv
odds_resumo.csv
odds_avancadas.csv
odds_avancadas_resumo.csv
```

O fluxo base usa `h2h`. Tambem ha suporte local para odds avancadas `h2h,totals,spreads`, quando coletadas pela The Odds API.

### Google Sheets

Usado como painel principal do projeto.

Planilha:

```text
copaDoMundo
```

Abas usadas/criadas:

- jogos
- odds
- odds_resumo
- previsoes
- palpites_bolao
- apostas_exchange

A atualizacao e feita com:

- `gspread`
- `google-auth`
- `service_account.json`

## Estrutura Atual

Entrada principal:

```text
src/atualizar_tudo.py
```

Estrutura modular:

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

Arquivos de projeto na raiz:

```text
README.md
ROADMAP.md
AGENTS.md
requirements.txt
.gitignore
```

Documentacao complementar:

```text
docs/VALIDACOES.md
```

Uso dos documentos:

- `README.md`: funcionamento atual e estavel do projeto.
- `ROADMAP.md`: status, tarefas, gates e proximos passos.
- `docs/VALIDACOES.md`: detalhes de validacoes, execucoes autorizadas e resultados locais.

O projeto nao usa wrappers Python na raiz. Os comandos devem chamar os modulos em `src/`.

Arquivos CSV gerados:

```text
data/jogos_copa.csv
data/odds_copa.csv
data/odds_avancadas.csv
data/odds_avancadas_resumo.csv
data/odds_historico.csv
data/odds_resumo.csv
data/palpites_odds.csv
data/elo_selecoes.csv
```

Pasta de historico:

```text
data/historico_odds/
```

## Configuracao

### Ambiente virtual

Use o ambiente virtual local do projeto:

```powershell
.\.venv\Scripts\Activate.ps1
```

Instale as dependencias:

```powershell
pip install -r requirements.txt
```

### Variaveis de ambiente

Crie um arquivo `.env` com:

```env
FOOTBALL_DATA_TOKEN=sua_chave_football_data
ODDS_API_KEY=sua_chave_the_odds_api
```

Nunca envie o `.env` para o GitHub.

### Credencial Google

O arquivo `service_account.json` e a credencial da Service Account do Google Cloud.

Ele permite que o Python atualize a planilha no Google Sheets. A planilha precisa estar compartilhada com o `client_email` dessa Service Account como Editor.

Nunca envie `service_account.json` para o GitHub.

## Comando Principal

Para atualizar todo o fluxo:

```powershell
python -m src.atualizar_tudo
```

Esse comando:

- baixa jogos da Copa;
- baixa odds novas;
- salva historico;
- atualiza o resumo;
- gera palpites;
- atualiza o Google Sheets.

## Scripts

### `src/apis/football_data.py`

Integra com a `football-data.org`.

Comandos uteis:

```powershell
python -m src.apis.football_data competicoes
python -m src.apis.football_data buscar
python -m src.apis.football_data salvar
```

Resultado esperado:

```text
Status: 200
```

### Buscar jogos da Copa

Busca os jogos da Copa em:

```text
https://api.football-data.org/v4/competitions/WC/matches
```

Mostra os primeiros jogos no terminal.

### Salvar jogos em CSV

Busca todos os jogos da Copa e salva em:

```text
data/jogos_copa.csv
```

Colunas principais:

- id_jogo
- data_hora_utc
- fase
- grupo
- time_a
- time_b
- placar_a
- placar_b
- status
- fonte_jogo

### `src/apis/odds_api.py`

Integra com a The Odds API.

Comandos:

```powershell
python -m src.apis.odds_api
python -m src.apis.odds_api odds
python -m src.apis.odds_api odds-avancadas
python -m src.apis.odds_api resumir-avancadas
python -m src.apis.odds_api esportes
python -m src.apis.odds_api eventos
python -m src.apis.odds_api mercados 3
```

Significado:

- `odds`: busca odds `h2h` da Copa e salva `data/odds_copa.csv`.
- `odds-avancadas`: busca `h2h,totals,spreads` e salva `data/odds_avancadas.csv`.
- `resumir-avancadas`: resume `data/odds_avancadas.csv` em `data/odds_avancadas_resumo.csv`.
- `esportes`: lista esportes disponiveis.
- `eventos`: lista eventos da Copa e salva `data/odds_eventos.csv`.
- `mercados 3`: mapeia mercados disponiveis para os 3 primeiros eventos locais e salva `data/odds_mercados.csv`.

Observacao: `eventos`, `mercados` e `odds-avancadas` fazem chamadas externas para The Odds API. Antes de rodar em escala, verificar custo de creditos.

Keys confirmadas:

```text
soccer_fifa_world_cup
soccer_fifa_world_cup_winner
```

### Buscar odds da Copa

Busca odds da Copa no mercado `h2h` e gera:

```text
data/odds_copa.csv
```

Cada linha representa um jogo, uma casa de aposta e as odds daquele mercado.

Colunas principais:

- id_odds_api
- data_hora_utc
- time_a
- time_b
- fonte
- mercado
- odd_a
- odd_empate
- odd_b
- atualizado_em

### `src/utils/historico.py`

Copia o `data/odds_copa.csv` atual para a pasta `data/historico_odds/`.

Comando:

```powershell
python -m src.utils.historico
```

Ele nao busca odds novas. Apenas registra uma foto do arquivo atual para acompanhar mudancas ao longo do tempo.

Tambem atualiza o historico consolidado:

```text
data/odds_historico.csv
```

Esse arquivo registra cada coleta com `coletado_em`, compara odds atuais com odds anteriores e cria colunas como:

- `odd_a_anterior`
- `odd_empate_anterior`
- `odd_b_anterior`
- `odd_a_variacao`
- `odd_empate_variacao`
- `odd_b_variacao`
- `movimento_mercado`
- `odd_subiu`
- `odd_caiu`
- `favoritismo_aumentou`

### `src/palpites/modelo.py`

Le `data/odds_copa.csv` e cria uma visao resumida por jogo em:

```text
data/odds_resumo.csv
```

Comando:

```powershell
python -m src.palpites.modelo resumir
```

Calcula:

- media da odd do time A;
- media da odd do empate;
- media da odd do time B;
- dispersao das odds entre casas;
- probabilidade implicita do time A;
- probabilidade implicita do empate;
- probabilidade implicita do time B;
- score de mercado por resultado;
- confianca de mercado;
- movimento agregado do mercado;
- resultado mais provavel;
- quantidade de casas usadas.

### Gerar palpites

Le `data/odds_resumo.csv` e gera:

```text
data/palpites_odds.csv
```

Comando:

```powershell
python -m src.palpites.modelo gerar
```

Logica atual:

- maior probabilidade define o resultado sugerido;
- favorito muito forte gera `2x0` ou `0x2`;
- favorito normal gera `2x1` ou `1x2`;
- jogo equilibrado gera `1x0`, `0x1` ou `1x1`;
- confianca depende da maior probabilidade;
- confianca de mercado considera probabilidade, vantagem sobre o segundo resultado e dispersao entre casas;
- movimento de mercado usa `data/odds_historico.csv` quando existir.

Colunas adicionais de mercado:

```text
score_mercado_a
score_mercado_empate
score_mercado_b
confianca_mercado
favoritismo_movimento
```

Colunas explicitas de previsao por componente:

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
confianca_placar
fonte_previsao_resultado
fonte_previsao_gols
fonte_previsao_placar
```

Quando `data/elo_selecoes.csv` estiver preenchido, tambem propaga campos Elo:

```text
elo_pontos_a
elo_pontos_b
diferenca_elo_pontos
favorito_elo
status_elo
```

Se o CSV ainda nao tiver dados, `status_elo` fica como `elo_nao_informado`.

### `data/elo_selecoes.csv`

Arquivo local para inserir dados do World Football Elo Ratings de forma controlada, sem scraping automatico.

Estrutura:

```text
selecao,elo_rank,elo_pontos,atualizado_em,fonte
```

O arquivo e criado automaticamente com as selecoes encontradas nos jogos quando o resumo e gerado. Depois disso, pode ser preenchido manualmente ou por importacao controlada.

### `src/sheets/google_sheets.py`

Atualiza o Google Sheets.

Comando:

```powershell
python -m src.sheets.google_sheets
```

Atualiza as abas da planilha:

```text
jogos          <- data/jogos_copa.csv
odds           <- data/odds_copa.csv
odds_resumo    <- data/odds_resumo.csv
palpites_bolao <- data/palpites_odds.csv
```

### `src/atualizar_tudo.py`

Orquestrador principal.

Roda:

1. `python -m src.apis.football_data salvar`
2. `python -m src.apis.odds_api`
3. `python -m src.utils.historico`
4. `python -m src.palpites.modelo resumir`
5. `python -m src.palpites.modelo gerar`
6. `python -m src.sheets.google_sheets`

Comando principal:

```powershell
python -m src.atualizar_tudo
```

## Gates de Decisao

Durante a execucao do roadmap, qualquer etapa que depender de decisao importante do usuario deve parar antes de continuar.

Exemplos de gate:

- consumo relevante de API;
- alteracao no Google Sheets;
- escolha de regra de negocio;
- uso de fonte externa com termos ou formato incerto;
- decisao visual de formatacao;
- risco de sobrescrever dado manual.

Nesses casos, o agente deve explicar a decisao, propor opcoes e aguardar confirmacao expressa.

## Limitacoes Atuais

O sistema ainda depende principalmente de odds e sinais de mercado.

Ele ajuda a entender:

- quem e favorito;
- quem tem maior probabilidade de vencer;
- se o jogo parece equilibrado.

Ja existe suporte local para:

- odds `h2h`;
- historico e movimento de odds;
- odds avancadas `totals` e `spreads`, quando coletadas;
- Elo local opcional via `data/elo_selecoes.csv`.

Ainda nao considera automaticamente:

- ambas marcam;
- estilo das selecoes;
- lesoes;
- escalacoes;
- previsoes premium externas;
- contexto esportivo.

Por isso, os placares sugeridos continuam sendo criterios auditaveis baseados nos sinais disponiveis, nao uma previsao esportiva completa.

## Cuidados de Seguranca

Nunca versionar:

- `.env`
- `service_account.json`
- `.venv/`
- arquivos CSV gerados pelo fluxo local
- `data/historico_odds/`

Antes de enviar para GitHub, confira:

```powershell
git status --short
```

Politica atual de versionamento:

- scripts, documentacao e configuracao do projeto entram no Git;
- credenciais e ambiente virtual ficam fora do Git;
- CSVs e historico de odds ficam em `data/` e fora do Git porque sao dados gerados, podem mudar a cada execucao e podem crescer com o tempo.

## Proximos Passos

Sugestoes de evolucao:

1. Validar manualmente as previsoes por componente em `data/palpites_odds.csv`.
2. Criar uma aba de revisao manual com `palpite_sugerido`, `palpite_final` e `status_revisao`.
3. Criar avaliacao de desempenho do bolao.
4. Avaliar novas fontes somente com gate: Betfair Exchange API, Sportmonks, Opta/Stats Perform ou scraping controlado.
5. Automatizar execucao no Windows com o Agendador de Tarefas depois que o fluxo manual estiver validado.

## Uso Recomendado

Antes da Copa:

- atualizar odds uma vez por dia;
- revisar mudancas relevantes;
- acompanhar favoritos.

Durante a Copa:

- atualizar pela manha;
- atualizar algumas horas antes dos jogos;
- revisar palpites finais manualmente.

Antes de enviar o bolao:

1. Rodar `python -m src.atualizar_tudo`.
2. Revisar `palpites_bolao`.
3. Ajustar manualmente jogos suspeitos.
4. Registrar o palpite final.
