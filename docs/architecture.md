# Arquitetura v0.1

```text
Usuário: objetivo + critérios + revisão final
  -> Codex CLI / sessão principal: Orquestrador (AGENTS.md)
      -> developer: implementação + testes
      -> qa: revisão independente + verificações
  <- diff + evidências + riscos + decisão pendente
```

O runtime é o Codex; o kit fornece instruções, agentes e procedimento. O workflow
Markdown é seguido pelo modelo, não interpretado por uma máquina de estados.
Transições: inspeção -> plano -> implementação -> revisão -> até duas correções
-> entrega; falhas de ambiente levam a BLOCKED com evidências e próximo passo.

Uma sessão opera em um repositório alvo. O catálogo central é consultado
manualmente. Branches isolam históricos; worktrees isolam diretórios, mas
compartilham metadados Git. Nenhum deles substitui sandbox ou permissões.
Developer e QA trabalham sequencialmente no mesmo checkout. O QA não altera
fontes por instrução; herda permissões do pai e pode produzir artefatos de testes.

Contratos de delegação: objetivo, caminho absoluto, branch/base, critérios,
arquivos permitidos e comandos revisados entram; diff, testes com exit code,
achados e limitações saem. O Orquestrador integra evidências, não presume sucesso.
O limite de dois subagentes é capacidade, não instrução para paralelizar edições.

Documentação versionada preserva decisões explícitas. Relatórios privados podem
ficar em `evaluations/runs/`, ignorado no Git. Não há recuperação automática,
memória semântica, persistência própria de sessões ou tracing próprio.

Decisões: TOML nativo reduz dependências; JSON para catálogo permite validação
com biblioteca padrão; modelo herdado evita exigir acesso a um modelo específico.
A portabilidade depende de testar o CLI instalado e ferramentas do alvo.
