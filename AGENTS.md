# AGENTS.md

Instrucoes para agentes e assistentes que forem trabalhar neste repositorio.

Este arquivo define o modo de trabalho do agente neste projeto. Ele deve ser tratado como a regra operacional principal para decidir o que ler, quando planejar, quando implementar, quando parar e como atualizar a documentacao.

Ao iniciar trabalho neste repositorio pela primeira vez na sessao, o agente deve:

1. Ler este `AGENTS.md` inteiro.
2. Ler o `README.md`.
3. Ler o `ROADMAP.md` para saber onde o projeto parou, qual e o proximo passo previsto e quais etapas devem orientar a continuidade do trabalho.

## Regras Obrigatorias

Estas regras acionam gate de excecao. Se a implementacao exigir descumprir qualquer uma delas, o agente deve parar imediatamente e pedir autorizacao expressa do usuario antes de continuar.

- Respeite o ambiente virtual `.venv`.
- Nao modifique, nao formate, nao mova e nao leia arquivos de segredo, como `.env` e `service_account.json`, salvo se o usuario pedir explicitamente.
- Nao exponha, imprima, copie para logs ou versione segredos, tokens, chaves de API ou credenciais.
- Nao execute comando destrutivo ou de limpeza, como `git reset`, `git clean`, exclusao recursiva, limpeza de volumes ou remocao em massa, sem autorizacao explicita.
- Nao apague CSVs, historicos, arquivos gerados ou abas da planilha sem autorizacao explicita do usuario.
- Nao faca chamada externa com custo, API paga ou consumo relevante de creditos sem que isso esteja previsto no plano aprovado.
- Nao altere Google Sheets fora das abas, intervalos ou comportamento previstos no plano aprovado.
- Nao avance para o proximo item do `ROADMAP.md` sem homologacao pratica do usuario.
- Nao saia do plano aprovado sem abrir novo gate quando a mudanca envolver acao sensivel ou alterar o comportamento combinado.


## Boas Praticas

Estas praticas orientam a execucao normal, a manutencao e a qualidade do trabalho. 

- Verifique o estado do Git com `git status --short` antes de qualquer alteracao.
- Entenda o contexto e o fluxo afetado antes de alterar scripts, regras de negocio, planilhas ou arquivos gerados.
- Rode validacoes compativeis com a mudanca feita antes de finalizar a implementacao.
- Durante uma implementacao ja autorizada, execute com autonomia o que estiver dentro do plano aprovado.
- Prefira mudancas pequenas, claras e testaveis.
- Preserve a estrutura modular existente e implemente logica nova dentro de `src/` quando aplicavel.
- Atualize a documentacao correspondente quando alterar comportamento, regras de negocio, odds, previsoes, historico, congelamento ou metricas.
- Mantenha o `ROADMAP.md` como resumo do estado da obra e use `docs/VALIDACOES.md` para detalhes de execucao.


## Fluxo de Trabalho

Este fluxo pode ser iniciado por uma das duas hipoteses abaixo.

**A. Identifique o item de execucao atual no `ROADMAP.md`**

- Siga diretamente para o item 1.

**B. Solicitacao do usuario ainda nao prevista no `ROADMAP.md`**

- Registre a solicitacao como novo item de execucao no `ROADMAP.md`.
- Posicione o item em ordem logica, considerando dependencias, prioridade e estado atual da obra.
- Nao implemente nada durante esse ajuste.
- Retorne a hipotese **A. Identifique o item de execucao atual no `ROADMAP.md`**.

1. Leia o item de execucao atual no `ROADMAP.md`, verifique o contexto atual do projeto e identifique silenciosamente restricoes, dependencias ou riscos relevantes antes de propor qualquer acao.

2. Apresente um **Plano Curtissimo** antes de implementar, com o seguinte formato obrigatorio:

   - **Objetivo:** ate 2 ou 3 frases curtas.
   - **Plano tecnico:** 3 a 5 acoes tecnicas objetivas.
   - **Operacoes sensiveis:** comandos, alteracoes destrutivas ou operacoes sensiveis. Se nao houver, escreva `Nenhuma`.

   Ao final, pergunte exatamente: **"Aprova este plano (S/N) ou tem alguma duvida tecnica?"**

3. Interprete a resposta do usuario ao gate do plano.

   - Se o usuario aprovar explicitamente com **"S"** ou equivalente claro, execute o plano e siga o fluxo.

   - Se houver duvida, pedido de ajuste ou ausencia de aprovacao clara (**Sub-fluxo de Esclarecimento/Ajuste**):
     - **nao implemente**;
     - responda de forma objetiva e curta, sem implementar;
     - mantenha o dialogo ate o usuario declarar que a duvida foi resolvida ou autorizar a continuidade;
     - entao apresente um **Novo Plano Curtissimo**;
     - re-valide: **"Podemos seguir com o plano (S/N)?"**

4. Execute o plano aprovado em modo continuo e autonomo e, durante a codificacao, verifique silenciosamente as **Regras Obrigatorias**.

5. Se a implementacao exigir descumprir qualquer **Regra Obrigatoria**, pare imediatamente e peca autorizacao expressa do usuario antes de continuar.

6. Ao concluir a implementacao, informe o usuario e aguarde a homologacao pratica.

   - Se o usuario aprovar a implementacao, siga para o item 7.

   - Se o usuario reportar erro ou pedir ajuste:
     - **nao atualize o `ROADMAP.md` como concluido**;
     - retorne ao **Sub-fluxo de Esclarecimento/Ajuste** do item 3.

7. Apos a homologacao aprovada pelo usuario, atualize o `ROADMAP.md` como concluido e reinicie este fluxo no item 1 para o proximo item de execucao.

   A atualizacao do `ROADMAP.md` deve seguir este formato minimo:

   - **Status do item:** marcar como concluido.
   - **Resumo da execucao:** registrar em 1 ou 2 frases o que foi implementado.
   - **Proximo item:** indicar qual sera o proximo item de execucao previsto.


## ROADMAP.md Como Estado da Obra

O `ROADMAP.md` e a fonte de verdade da execucao do projeto.

Ele deve representar o estado da obra: onde o projeto parou, o que ja foi concluido, o que esta pendente, o que esta bloqueado e qual e o proximo item de execucao.

Regras:

- Toda tarefa planejada ate a conclusao do projeto deve estar representada no `ROADMAP.md`.
- Se o usuario pedir algo que ainda nao esta previsto no `ROADMAP.md`, registre primeiro como novo item de execucao no roadmap.
- Posicione novos itens em ordem logica, considerando dependencias, prioridade e estado atual da obra.
- Nao use o `ROADMAP.md` como log completo de terminal, historico repetitivo ou registro longo de detalhes operacionais.
- Atualize o `ROADMAP.md` somente nos momentos definidos no fluxo de trabalho.

## Documento de Log da Execucao

Use `docs/VALIDACOES.md` como documento de log da execucao.

Ele deve registrar detalhes que nao devem sobrecarregar o `ROADMAP.md`, como:

- comandos executados;
- validacoes realizadas;
- resultados locais;
- decisoes relevantes;
- observacoes tecnicas;
- consumo de creditos de API;
- execucoes autorizadas;
- erros encontrados e correcoes aplicadas.

O `ROADMAP.md` deve conter o resumo e, quando necessario, apontar para a secao correspondente em `docs/VALIDACOES.md`.

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

## Fluxo do Projeto

Modulos principais:

```text
src/atualizar_tudo.py
src/apis/football_data.py
src/apis/odds_api.py
src/sheets/google_sheets.py
src/palpites/modelo.py
src/palpites/historico_previsoes.py
src/utils/config.py
src/utils/historico.py
```

Nao recrie wrappers na raiz sem motivo forte. A logica principal deve ficar nos modulos dentro de `src/`.

O fluxo operacional atual executado por `python -m src.atualizar_tudo` esta documentado no `README.md` e deve ser tratado como contexto tecnico atual, nao como regra imutavel.

## Boas Praticas de Edicao

- Use `README.md` como fonte de contexto do funcionamento atual e estavel do projeto.
- Use `ROADMAP.md` como fonte de verdade da execucao e do proximo passo.
- Use `docs/VALIDACOES.md` como log detalhado de execucao, validacoes e decisoes.
- Ao criar ou alterar scripts, mantenha nomes descritivos e coerentes com os scripts existentes.
- Prefira implementar logica nova dentro de `src/`.
- Evite refatoracoes grandes sem necessidade.
- Se alterar logica de odds, previsoes, historico de previsoes, congelamento ou metricas, documente a regra no `README.md` e no `ROADMAP.md`.
- Se adicionar nova dependencia Python, atualize `requirements.txt`.
- Se adicionar novo arquivo sensivel ou gerado, atualize `.gitignore`.
- Antes de finalizar, rode pelo menos verificacoes simples compativeis com a mudanca feita.

## Google Sheets

O projeto atualiza uma planilha chamada `copaDoMundo`.

Abas conhecidas:

- jogos
- odds
- odds_resumo
- previsoes
- palpites_bolao
- historico_previsoes
- apostas_exchange

Nao altere nomes de abas, URL da planilha, estrutura de abas existentes ou comportamento de atualizacao sem que isso esteja previsto no plano aprovado.

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
  historico_previsoes.csv
  historico_odds/
```

## Escopo Atual do Modelo

O projeto comecou usando apenas odds `h2h`, mas agora tambem possui suporte local a:

- historico de odds;
- movimento de mercado;
- odds avancadas `totals` e `spreads`;
- Elo local opcional via `data/elo_selecoes.csv`;
- criterios auditaveis de placar sugerido;
- historico de previsoes com congelamento pre-jogo.

Mesmo assim, nao assuma que o sistema ja entende automaticamente:

- lesoes;
- escalacoes;
- contexto esportivo manual;
- BTTS por endpoint geral;
- previsoes premium de Opta, Sportmonks ou Forebet;
- mercado exchange.

Qualquer melhoria nessas direcoes deve ser tratada como novo item no `ROADMAP.md` e seguir o Fluxo de Trabalho deste arquivo.
