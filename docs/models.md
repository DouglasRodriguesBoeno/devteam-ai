# Seleção de modelos

O Orquestrador continua sendo a sessão principal. Use `model` no início de
`.codex/config.toml`, antes de qualquer tabela, ou `codex --model <slug>`.
A preferência local desta entrega é `gpt-6.2-astra` para trabalho complexo.
Para tarefas simples e E01, use `gpt-6.2-sol`. Esses nomes são configurações
editáveis, não constantes de código nem garantia de acesso futuro.

Cada especialista aceita `model = "<slug>"` no início do seu TOML em
`.codex/agents/`, fora do texto `developer_instructions`. Remova ou comente
essa chave para herdar. O kit não define `agents.default_subagent_model`.
Se uma configuração pessoal definir esse padrão, ele também afeta a herança;
o preflight abaixo mostra a seleção resultante. Instruções dos papéis não mudam.

## Procedimento

```powershell
python scripts/validate.py
python scripts/check_models.py --model gpt-6.2-sol
if ($LASTEXITCODE -eq 0) { codex --strict-config --model gpt-6.2-sol }
```

Para Astra, substitua o slug nos dois comandos. Para usar o modelo do arquivo
local, omita `--model` em ambos. Confie somente no projeto revisado no Codex;
um projeto não confiável pode ter sua configuração ignorada.
Na execução TASK-004, o override de confiança via `-c projects=...` não habilitou
a configuração local. O CLI indicou `--trust`, que salva confiança persistente.
Essa opção não foi usada devido à restrição de não modificar configurações globais.

O preflight consulta `codex debug models`, resolve a escolha principal e dos dois
TOML e termina com exit 1 se houver modelo ausente. Não chama modelos, troca
slugs, altera configurações ou inicia agentes. O validador offline não consulta
disponibilidade. O catálogo pode vir de cache do CLI; aparecer nele não prova
que uma chamada será aceita. Erros de autenticação, quota ou disponibilidade
na execução devem ser reportados como BLOCKED, sem escolher outro modelo.

Este preflight cobre o layout deste kit, a configuração pessoal e `--model`.
Não resolve profiles, políticas gerenciadas, configurações de diretórios ancestrais
ou escolhas explícitas feitas ao delegar. Se usar essas opções, confira também
a configuração efetiva no Codex. Iniciar o CLI diretamente pula esse preflight.
`--strict-config` valida campos, não disponibilidade de modelos.

## Evidência de 18/11/2026

CLI `0.169.0-alpha.11.1`: catálogo atualizado sem `--bundled` listou
`gpt-6.2-astra` e `gpt-6.2-sol`. A configuração pessoal ainda selecionava
`gpt-5.5`, ausente desse catálogo. Ela foi preservada; a escolha local ou `--model`
evita herdar essa referência. A comprovação por inferência está no relatório E01.

## Mecanismos oficiais

O campo `model` do especialista prevalece sobre a escolha de spawn, os padrões
de `[agents]` e o pai. Sem escolhas específicas, modelo e esforço vêm do pai.
Se necessário, configure também `model_reasoning_effort` no TOML do papel e
confira os níveis suportados no catálogo. [Subagentes](https://learn.chatgpt.com/docs/agent-configuration/subagents).

Configuração nativa e opções são documentadas na
[referência do Codex](https://learn.chatgpt.com/docs/config-file/config-reference).
