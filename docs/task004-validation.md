# TASK-004 — validação

Execução de 18/11/2026 na branch `task/004-model-management`, base `55f1974`.
CLI: `0.169.0-alpha.11.1`. Configuração global preservada. Sem commit adicional,
merge, publicação, agentes novos ou E02.

## Modelos

`codex debug models` retornou exit 0. O catálogo lista GPT-6.2 Astra e Sol;
GPT-5.5 não aparece. A referência antiga foi identificada no campo `model` da
configuração pessoal. O kit agora usa preferência local editável e preflight
explícito, sem alterar esse arquivo pessoal.

Sol aceitou a chamada de inferência do E01. Astra foi confirmado no catálogo,
sem chamada adicional para reduzir consumo. A disponibilidade futura deve ser
revalidada. As instruções textuais de Developer e QA foram preservadas.

## Checks

- `python scripts/validate.py`: PASS, exit 0.
- `python -m unittest discover -s tests -v`: 5 testes aprovados.
- Preflight padrão: Astra nos três papéis; override Sol: Sol nos três.
- Modelo fictício: exit 1, BLOCKED explícito, nenhuma substituição.
- CLI `app-server --strict-config --print-startup-config`: exit 0 com cópia
  da configuração em CODEX_HOME isolado. Não testa carregamento por confiança.
- `git diff --check`: sem erros de whitespace.

## E01 — BLOCKED

Uma única execução de inferência, com modelo `gpt-6.2-sol`, esforço low e
sandbox read-only. Identificador da sessão omitido.
O processo terminou com exit 0, mas o resultado funcional é BLOCKED.

O CLI avisou que ignorou a configuração local por falta de confiança, apesar
do override de `projects` passado na invocação. Seu `--trust` persiste confiança
e não foi executado para respeitar a restrição sobre configurações globais.
A sessão reportou que `collaboration.spawn_agent` não expunha `agent_type`.
Não houve chamada de spawn, ID de filho ou resultado de Developer/QA; portanto
reconhecimento, delegação e herança em execução continuam NÃO CONFIRMADOS.

A leitura do cenário funcionou, mas tentativas subsequentes do executor falharam:
`registered Core launch requires an installed app`.
O runtime também emitiu aviso de depreciação de `features.multi_agent` herdado.
Nenhum desses problemas foi contornado mudando arquitetura ou desativando proteções.

A cópia descartável recebeu um snapshot das alterações TASK-004 existentes no
início do teste sobre o commit base. Hashes SHA-256 e status Git antes/depois
permaneceram idênticos; a verificação externa confirmou preservação dos arquivos.
As últimas edições de documentação não fizeram parte desse snapshot E01.

Uso reportado pelo runtime: 94.649 tokens de entrada, 76.288 em cache,
357 de saída, 15 de raciocínio. Custo financeiro não reportado.

Evidências locais ignoradas em `evaluations/runs/task004-2026-11-18/`:
`models.json`, `prompt.txt`, `invocation.json`, `events.jsonl`, `stderr.txt`,
`result.md`, `strict-config.txt`, `integrity.json` e `unavailable.txt`.

Próximo passo: resolver confiança e instalação do executor com uma decisão
explícita sobre mudanças persistentes, verificar o suporte a papéis personalizados
no runtime e repetir E01. Não avançar a E02 enquanto a delegação não for comprovada.
