# ROADMAP

## Instrucoes de Uso

Antes de executar qualquer item deste roadmap, leia e siga o `AGENTS.md`.

Este arquivo e o painel de controle operacional e o plano mestre de execucao do projeto. Ele deve responder rapidamente qual e a proxima tarefa, quais tarefas existem, qual o status de cada uma e onde encontrar o detalhamento e o log de execucao.

O detalhamento robusto das tarefas deve ficar em `tasks/`. O log de execucao deve ficar em `logs/`. Enquanto a migracao para `logs/` nao estiver completa, `docs/VALIDACOES.md` permanece como historico legado.

Este documento deve ter sempre estas secoes:

1. `## Instrucoes de Uso`
2. `## Proxima Tarefa`
3. `## Lista de Tarefas`

Status permitidos:

- `pendente`
- `em_execucao`
- `bloqueado`
- `concluido`
- `cancelado`

Cada item da `Lista de Tarefas` deve usar este formato:

```text
N. [ ] Titulo da tarefa
   - Status: pendente | em_execucao | bloqueado | concluido | cancelado
   - Task: `tasks/NNN-nome-da-task.md` ou detalhamento pendente
   - Log: `logs/NNN-nome-da-task.md` ou pendente
```

Regras de preenchimento:

- Toda tarefa planejada ate a conclusao do projeto deve estar representada neste arquivo.
- A secao `## Proxima Tarefa` deve apontar sempre para o proximo item executavel, considerando ordem, dependencias, bloqueios e estado atual.
- Se a proxima tarefa estiver bloqueada, o bloqueio deve ficar explicito.
- Se o usuario pedir algo que ainda nao esta previsto, registre primeiro como novo item de execucao.
- Posicione novos itens em ordem logica, considerando dependencias, prioridade e estado atual da obra.
- Tarefas concluidas devem apontar para um arquivo em `tasks/` e um arquivo em `logs/`.
- Tarefas pendentes podem informar que o detalhamento ainda sera definido pela tarefa de criacao da metodologia de tasks.
- Nao use este arquivo como log de terminal, historico detalhado de execucao ou deposito longo de ideias.
- Atualize este arquivo somente nos momentos definidos no fluxo de trabalho do `AGENTS.md`.

## Proxima Tarefa

ID: 007
Titulo: Criar skill/metodologia de criacao de tasks
Status: pendente
Task: detalhamento inicial a definir nesta propria tarefa
Log: pendente
Bloqueio: nenhum

## Lista de Tarefas

1. [x] Organizar o projeto
   - Status: concluido
   - Task: `tasks/001-organizar-projeto.md`
   - Log: `logs/001-organizar-projeto.md`

2. [x] Consolidar a automacao atual
   - Status: concluido
   - Task: `tasks/002-consolidar-automacao-atual.md`
   - Log: `logs/002-consolidar-automacao-atual.md`

3. [x] Melhorar estrutura do codigo
   - Status: concluido
   - Task: `tasks/003-melhorar-estrutura-codigo.md`
   - Log: `logs/003-melhorar-estrutura-codigo.md`

4. [x] Criar historico mais inteligente
   - Status: concluido
   - Task: `tasks/004-criar-historico-mais-inteligente.md`
   - Log: `logs/004-criar-historico-mais-inteligente.md`

5. [x] Melhorar score baseado em odds e mercado
   - Status: concluido
   - Task: `tasks/005-melhorar-score-odds-mercado.md`
   - Log: `logs/005-melhorar-score-odds-mercado.md`

6. [x] Expandir The Odds API
   - Status: concluido
   - Task: `tasks/006-expandir-the-odds-api.md`
   - Log: `logs/006-expandir-the-odds-api.md`

7. [ ] Criar skill/metodologia de criacao de tasks
   - Status: pendente
   - Task: detalhamento inicial a definir nesta propria tarefa
   - Log: pendente

8. [ ] Conectar e extrair dados de mercado exchange
   - Status: pendente
   - Task: detalhamento pendente; sera definido pela tarefa `Criar skill/metodologia de criacao de tasks`
   - Log: pendente

9. [ ] Avaliar Sportmonks Predictions API
   - Status: pendente
   - Task: detalhamento pendente; sera definido pela tarefa `Criar skill/metodologia de criacao de tasks`
   - Log: pendente

10. [ ] Avaliar Opta/Stats Perform
    - Status: pendente
    - Task: detalhamento pendente; sera definido pela tarefa `Criar skill/metodologia de criacao de tasks`
    - Log: pendente

11. [ ] Avaliar scraping controlado, como Forebet
    - Status: pendente
    - Task: detalhamento pendente; sera definido pela tarefa `Criar skill/metodologia de criacao de tasks`
    - Log: pendente

12. [ ] Melhorar modelo de palpite
    - Status: pendente
    - Task: detalhamento pendente; sera definido pela tarefa `Criar skill/metodologia de criacao de tasks`
    - Log: pendente

13. [ ] Melhorar placar sugerido
    - Status: pendente
    - Task: detalhamento pendente; sera definido pela tarefa `Criar skill/metodologia de criacao de tasks`
    - Log: pendente

14. [ ] Melhorar previsibilidade dos componentes do bolao
    - Status: pendente
    - Task: detalhamento pendente; sera definido pela tarefa `Criar skill/metodologia de criacao de tasks`
    - Log: pendente

15. [ ] Criar historico de previsoes
    - Status: pendente
    - Task: detalhamento pendente; sera definido pela tarefa `Criar skill/metodologia de criacao de tasks`
    - Log: pendente

16. [ ] Formatar Google Sheets automaticamente
    - Status: pendente
    - Task: detalhamento pendente; sera definido pela tarefa `Criar skill/metodologia de criacao de tasks`
    - Log: pendente

17. [ ] Criar avaliacao de desempenho do bolao
    - Status: pendente
    - Task: detalhamento pendente; sera definido pela tarefa `Criar skill/metodologia de criacao de tasks`
    - Log: pendente

18. [ ] Automatizar no Windows
    - Status: pendente
    - Task: detalhamento pendente; sera definido pela tarefa `Criar skill/metodologia de criacao de tasks`
    - Log: pendente
