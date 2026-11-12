# Workflow: implementar funcionalidade

Entrada: projeto/caminho autorizado, objetivo e critérios de aceite observáveis.
Saída: branch com alterações revisáveis (podem estar sem commit), testes e relatório.

## 1. Inspeção e base

Leia instruções do alvo, confirme a raiz e inspecione arquivos não rastreados:

```powershell
git rev-parse --show-toplevel
git status --short --branch
git log -1 --oneline
git diff
```

Registre SHA base com `git rev-parse HEAD`. Se não houver commit, solicite/revise
um commit inicial antes da branch; não invente uma base. Se houver alterações
do usuário, não as reverta nem as inclua silenciosamente. Prefira worktree a
partir de HEAD, deixando claro que alterações não commitadas não são transportadas.

Escolha UMA estratégia; nomes e caminhos abaixo são exemplos a adaptar:

```powershell
# Checkout limpo, mesma pasta
git switch -c devteam/minha-feature
```

```powershell
# Diretório novo e branch nova; não reutilizar destino existente
git worktree add -b devteam/minha-feature ../projeto-minha-feature HEAD
git -C ../projeto-minha-feature status --short --branch
```

Worktrees exigem commit base e escrita nos metadados do repositório principal.
Instale/mescle o kit no alvo conforme README; não assuma que configurações locais
não versionadas foram copiadas. Abra a sessão no diretório escolhido.

## 2. Planejamento e implementação

Registre critérios, arquivos previstos, comandos de teste revisados e escopo.
Delegue ao `developer` passando caminho absoluto, branch, SHA base e contrato.
Aguarde conclusão; não inicie QA sobre um diff ainda em alteração.

## 3. QA e correção

Delegue ao `qa` os critérios e o diff, incluindo arquivos novos. Reexecute testes
pertinentes, distinga defeito do produto de falha de ambiente. Se houver FAIL,
retorne achados ao Developer e repita QA (máximo duas correções). BLOCKED ou
limite atingido exige relatório parcial honesto, nunca aprovação presumida.

## 4. Entrega para aprovação

```powershell
git diff --check
git diff --stat
git diff
git status --short
```

Esses diffs não incluem arquivos novos não rastreados: inspecione-os à parte.
Se houver commits autorizados na tarefa, inclua também `git diff <SHA-base> HEAD`
e mudanças ainda não commitadas. Use o [modelo de relatório](../evaluations/report-template.md).
Pare com alterações preservadas para revisão humana. Commit, merge, push,
publicação e remoção da worktree não são passos automáticos.
