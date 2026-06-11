# AGENTS.md

Instrucoes para agentes e assistentes que forem trabalhar neste repositorio.

## Antes de Fazer Qualquer Alteracao

1. Leia este arquivo inteiro.
2. Leia o `README.md`.
3. Verifique o estado do Git com `git status --short`.
4. Entenda o fluxo atual antes de alterar scripts.

## Regras Obrigatorias

- Respeite o ambiente virtual `.venv`.
- Nao modifique, nao formate, nao mova e nao leia o arquivo `service_account.json`, salvo se o usuario pedir explicitamente.
- Nao exponha, imprima ou versione segredos.
- Preserve o fluxo principal do projeto: buscar odds, salvar historico, resumir odds, gerar palpites e atualizar a planilha.
- Prefira mudancas pequenas, claras e testaveis.
- Nao apague CSVs, historicos ou arquivos gerados sem autorizacao explicita do usuario.
- Se uma etapa depender de uma decisao importante do usuario, credencial, acao externa, consumo relevante de API, alteracao no Google Sheets ou escolha de regra de negocio, crie um gate: pare a execucao, explique a decisao e aguarde confirmacao expressa.
- Execute o roadmap um passo por vez. Ao concluir uma etapa, pare, informe o que foi feito e aguarde o usuario realizar testes manuais e autorizar expressamente o proximo passo.

## Ambiente

O projeto roda em Python com ambiente virtual local:

```powershell
.\.venv\Scripts\Activate.ps1
```

Dependencias:

```powershell
pip install -r requirements.txt
```

Comando principal:

```powershell
python -m src.atualizar_tudo
```

## Segredos e Arquivos Gerados

Antes de qualquer commit, confirme que estes arquivos continuam fora do Git:

```text
.env
service_account.json
.venv/
*.csv
data/*.csv
data/historico_odds/
```

O `.env` contem chaves como:

```env
FOOTBALL_DATA_TOKEN=...
ODDS_API_KEY=...
```

O `service_account.json` contem credencial do Google Cloud e deve ser tratado como segredo.

Os arquivos CSV e a pasta `data/historico_odds/` sao artefatos gerados pelo fluxo local. Eles devem ficar fora do Git por enquanto. Se algum novo segredo ou artefato gerado for criado, atualize o `.gitignore`.

## Fluxo de Trabalho com o Usuario

Este projeto deve evoluir por etapas curtas e validadas manualmente.

Regras do fluxo:

1. Trabalhe somente no passo atual autorizado pelo usuario.
2. Se surgir uma decisao relevante, abra um gate antes de continuar.
3. Ao terminar o passo, rode validacoes compativeis com a mudanca.
4. Informe os arquivos alterados, os comandos executados e qualquer risco restante.
5. Pare e aguarde os testes manuais do usuario.
6. So avance para o proximo passo com ordem expressa do usuario.

Exemplos de gates:

- consumo de creditos de API;
- consulta de fonte externa nova;
- criacao ou alteracao de credenciais;
- alteracao no Google Sheets;
- regra de negocio que muda o palpite;
- automacao agendada no Windows;
- operacao destrutiva ou limpeza de artefatos.

## Fluxo do Projeto

Modulos principais:

```text
src/atualizar_tudo.py
src/apis/football_data.py
src/apis/odds_api.py
src/sheets/google_sheets.py
src/palpites/modelo.py
src/utils/config.py
src/utils/historico.py
```

Nao recrie wrappers na raiz sem motivo forte. A logica principal deve ficar nos modulos dentro de `src/`.

Fluxo executado por `python -m src.atualizar_tudo`:

1. Buscar odds novas.
2. Salvar historico de odds.
3. Resumir odds por jogo.
4. Gerar palpites sugeridos.
5. Atualizar Google Sheets.

## Boas Praticas de Edicao

- Use `README.md` como fonte de contexto do projeto.
- Ao criar ou alterar scripts, mantenha nomes descritivos e coerentes com os scripts existentes.
- Prefira implementar logica nova dentro de `src/` e manter os scripts da raiz como entradas simples.
- Evite refatoracoes grandes sem necessidade.
- Se alterar logica de odds ou palpites, documente a regra no `README.md`.
- Se adicionar nova dependencia Python, atualize `requirements.txt`.
- Se adicionar novo arquivo sensivel ou gerado, atualize `.gitignore`.
- Antes de finalizar, rode pelo menos verificacoes simples compatíveis com a mudanca feita.

## Google Sheets

O projeto atualiza uma planilha chamada `copaDoMundo`.

Abas conhecidas:

- jogos
- odds
- odds_resumo
- previsoes
- palpites_bolao
- apostas_exchange

Nao altere nomes de abas ou URL da planilha sem confirmar com o usuario.

## Git

Antes de sugerir commit ou publicar o projeto:

```powershell
git status --short
```

Confirme que arquivos sensiveis nao aparecem como rastreados ou prontos para commit.
Use a secao "Segredos e Arquivos Gerados" como lista unica do que nao deve ser versionado.

## Artefatos Gerados

Arquivos gerados pelo fluxo devem ficar em `data/`, nao na raiz do projeto.

Estrutura esperada:

```text
data/
  jogos_copa.csv
  odds_copa.csv
  odds_resumo.csv
  palpites_odds.csv
  historico_odds/
```

## Escopo Atual do Modelo

O projeto comecou usando apenas odds `h2h`, mas agora tambem possui suporte local a:

- historico de odds;
- movimento de mercado;
- odds avancadas `totals` e `spreads`;
- Elo local opcional via `data/elo_selecoes.csv`;
- criterios auditaveis de placar sugerido.

Mesmo assim, nao assuma que o sistema ja entende automaticamente:

- lesoes;
- escalacoes;
- contexto esportivo manual;
- BTTS por endpoint geral;
- previsoes premium de Opta, Sportmonks ou Forebet;
- mercado exchange.

Qualquer melhoria nessas direcoes deve ser tratada como nova etapa do roadmap e passar por gate quando envolver fonte externa, custo, scraping ou regra de negocio relevante.
