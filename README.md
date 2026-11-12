# DevTeam AI · v0.1

Equipe de desenvolvimento local-first e Git-native sobre o Codex CLI.
A sessão principal coordena dois especialistas: Developer implementa; QA revisa
e testa. A entrega é um diff verificável em uma branch, para aprovação humana.

Este MVP é um kit operacional de configuração e workflow, não um servidor.
Arquivos e comandos ficam na máquina; a inferência do Codex pode usar serviços
na nuvem e consumir a franquia da conta. Local-first não significa offline.
Não há MCP próprio, banco de memória, seleção automática pelo registry ou UI.

## Instalação

Pré-requisitos: Git, Codex CLI autenticado e Python 3.11+ para validação offline.
Se o Codex já estiver instalado, reutilize-o. Uma instalação via npm requer
Node.js/npm compatíveis e acesso à rede:

```powershell
npm install -g @openai/codex
codex --version
codex login
git --version
python --version
```

Não copie credenciais para o projeto. A referência local verificada em
10/11/2026 foi `codex-cli 0.167.0-alpha.3.2`; não é uma afirmação de versão
estável mais recente. Consulte [compatibilidade](docs/compatibility.md).

## Primeiro uso

Abra um terminal na pasta `devteam-ai`:

```powershell
python scripts/validate.py
codex --strict-config -s workspace-write -a on-request
```

Revise os arquivos antes de confiar no projeto na interface do Codex. Projetos
não confiáveis podem ignorar a configuração local. Confira as permissões da
sessão e peça que confirme a disponibilidade de `developer` e `qa` antes de editar.
O modelo é herdado da conta/configuração pessoal; nenhum modelo é fixado aqui.

Prompt inicial sugerido:

> Atue como Orquestrador conforme AGENTS.md. Siga workflows/implement-feature.md.
> Objetivo: melhorar a mensagem de erro do validador para JSON inválido.
> Aceite: informar o arquivo e a linha, sair com código 1 e manter os cadastros
> válidos funcionando. Use developer para implementar e qa para revisar e testar.
> Trabalhe em branch de tarefa; apresente o diff sem commit, push ou merge.

Para criar branches em um repositório recém-inicializado, primeiro revise e faça
o commit base manualmente. O bootstrap não cria commits em seu nome:

```powershell
git status --short
git add README.md AGENTS.md .gitignore .codex docs workflows evaluations projects scripts
git diff --cached --check
git diff --cached
git commit -m "chore: bootstrap DevTeam AI v0.1"
git switch -c devteam/validator-errors
```

## Usar em outro projeto

O catálogo é explicado em [projects/README.md](projects/README.md).
Cada projeto mantém seu histórico Git. Não inicie no DevTeam AI e suponha que
`--cd` em outro repositório também carrega estes agentes.

1. Selecione o caminho autorizado e inspecione seu estado Git e instruções.
2. Crie uma branch/worktree conforme o [workflow](workflows/implement-feature.md).
3. No alvo, mescle manualmente `.codex/config.toml` e copie os dois arquivos de
   `.codex/agents/`, somente se não houver colisões. Nunca sobrescreva configurações.
4. Preserve o AGENTS.md existente; acrescente o papel do Orquestrador e as regras
   deste kit compatíveis com o alvo. Copie o workflow para um caminho livre e
   ajuste a referência. Revise e versione a adoção separadamente da funcionalidade.
5. Abra `codex --strict-config -C "<caminho-do-alvo>" -s workspace-write -a on-request`.
   Revise a confiança no alvo/worktree e envie objetivo e critérios de aceite.

Não há instalador que altere outros projetos nesta versão. Não use `--add-dir`
para conceder escrita a todos os repositórios do catálogo.

## Documentação e validação

- [Arquitetura e limites](docs/architecture.md)
- [Segurança e aprovações](docs/security.md)
- [Compatibilidade e fontes](docs/compatibility.md)
- [Roadmap](docs/roadmap.md)
- [Workflow de implementação](workflows/implement-feature.md)
- [Cenários de avaliação](evaluations/scenarios.md)
- [Relatório de validação](docs/validation.md)

`python scripts/validate.py` verifica estrutura, TOML, regras de configuração,
registry de exemplo e links locais. Não chama modelos nem executa comandos do
catálogo. A prova de colaboração entre agentes é um experimento separado,
descrito nos cenários; validação estática não prova qualidade de implementação.
