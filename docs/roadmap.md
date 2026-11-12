# Roadmap

## v0.1 — kit operacional

Configuração nativa, Orquestrador principal, Developer, QA, catálogo manual,
workflow Git e validação offline. Próximo marco: registrar um ciclo real completo
em um projeto de teste, com branch, diff e revisão humana.

## v0.2 — memória e catálogo

Projetar SQLite local com isolamento por projeto, retenção, exclusão e migrações.
Implementar consultas e reconciliar decisões com o código atual. Só considerar
entregue quando testes de persistência e separação de projetos passarem.

## v0.3 — MCP próprio

Implementar servidor com operações mínimas de leitura do catálogo e decisões;
validar entradas, caminhos permitidos e autenticação quando aplicável. Adicionar
testes de protocolo e permissões antes de expor escrita. Nenhum endpoint existe hoje.

## Depois de evidências

Comparar agente único versus equipe em tarefas equivalentes antes de criar
orquestrador TypeScript/Agents SDK, telemetria, dashboard React ou novos papéis.
Exigir ganhos medidos em qualidade/custo/tempo e documentar resultados negativos.
