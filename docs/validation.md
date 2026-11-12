# Validação do bootstrap

Data: 10/11/2026. Ambiente: Windows, Python 3.13, Git 2.45.1,
Codex CLI 0.167.0-alpha.3.2.

| Verificação | Resultado |
| --- | --- |
| Estrutura | 17 arquivos de entrega presentes, incluindo arquivos ocultos |
| `python scripts/validate.py` | PASS; 16 arquivos obrigatórios, TOML, agentes, JSON e links |
| Registry com ID duplicado | Rejeitado, exit 1 |
| Registry com caminho relativo | Rejeitado, exit 1 |
| JSON truncado | Rejeitado, exit 1 |
| CLI `app-server --strict-config --print-startup-config` | Exit 0, configuração aceita |
| Chave desconhecida na cópia de configuração | Rejeitada pelo modo estrito |
| `git check-ignore` | Registry local, .env e relatórios privados ignorados |
| Git | Inicializado em main, sem commits ou remote |

A checagem do CLI usou cópia da configuração em um CODEX_HOME isolado em
`.local/validation-home`, sem autenticação ou alteração das preferências globais.
Ela valida a configuração de inicialização; não comprova descoberta dos agentes
no projeto confiável, execução dos papéis ou acesso ao modelo. Os TOML dos
especialistas foram verificados pelo parser Python e contrato documentado.

Limitações observadas: a pasta temporária padrão negou escrita; as verificações
foram refeitas na pasta local ignorada. `codex features` não aceita
`--strict-config`; usou-se o comando de validação de inicialização acima.
Não houve chamada de inferência, instalação de pacotes ou edição de outro projeto.

Pendentes: smoke test E01 e tarefa E02 com login, confiança do projeto e modelo
disponível. Não se afirma que a colaboração ponta a ponta foi validada.

O validador verifica o contrato deste kit, não todo o schema do Codex.
A aceitação pelo CLI e a execução real de subagentes são verificações distintas.
