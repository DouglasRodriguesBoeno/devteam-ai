# Compatibilidade

Referência inspecionada em 10/11/2026: Codex CLI `0.167.0-alpha.3.2` no Windows.
A configuração usa agentes TOML autônomos com `name`, `description` e
`developer_instructions`. Não usa o antigo registro `agents.<role>.config_file`.
As permissões ficam no pai; os agentes herdam o modelo e o ambiente.

Fontes oficiais consultadas:
- [Subagentes e formato atual](https://learn.chatgpt.com/docs/agent-configuration/subagents)
- [Referência de configuração](https://learn.chatgpt.com/docs/config-file/config-reference)

Na instalação local, `codex --help` confirmou `--strict-config`, `-C`, `-s`,
`-a` e `--worktree`. `codex features list` apresentou `multi_agent` estável/ativo.
Este kit usa `[agents] enabled` e `max_concurrent_threads_per_session`, sem
depender do sinalizador legado. Não fixa versão mínima não testada.

Após atualizar o CLI, execute a validação offline e um smoke test de delegação.
Se agentes não aparecerem, confira confiança do projeto, arquivos TOML e versão.
Não traduza uma falha em execução monolítica silenciosa.
Use o CLI para este procedimento; a configuração do app não é pressuposta.

TASK-004 (18/11/2026): CLI `0.169.0-alpha.11.1`. A preferência principal passou
a ser local; campos opcionais `model` e `model_reasoning_effort` dos agentes são
aceitos pelo validador. Nenhum slug é fixado no código de validação.
Consulte [modelos](models.md) e [evidências TASK-004](task004-validation.md).
