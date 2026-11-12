# Catálogo manual

Copie `registry.example.json` para `registry.local.json` nesta pasta e edite
os caminhos absolutos, IDs únicos, branch padrão e comandos reais. O arquivo
local é ignorado pelo Git; os caminhos de exemplo não precisam existir.

`schema_version` é 1. `projects` contém objetos com `id`, `path`, `description`,
`default_branch`, `test_commands` (lista de strings) e `notes`.
Não coloque tokens, senhas ou URLs autenticadas. O Codex não descobre este
formato automaticamente: peça ao orquestrador que leia a entrada escolhida.
Nenhum comando é executado pelo validador. O cadastro não concede permissões.

Validação opcional do cadastro real, a partir da raiz DevTeam AI:

```powershell
python scripts/validate.py --registry projects/registry.local.json
```

O validador confere o formato e caminhos absolutos Windows/POSIX, não a existência
dos projetos. Antes do uso, confira `git -C <caminho> rev-parse --show-toplevel`
e `git -C <caminho> status --short --branch`.
