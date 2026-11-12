"""Offline checks for the DevTeam AI kit; never execute registry commands."""

import argparse
import json
from pathlib import Path, PurePosixPath, PureWindowsPath
import re
import sys
import tomllib

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = (
    'README.md', 'AGENTS.md', '.gitignore', '.codex/config.toml',
    '.codex/agents/developer.toml', '.codex/agents/qa.toml',
    'docs/architecture.md', 'docs/roadmap.md', 'docs/security.md',
    'docs/compatibility.md', 'docs/validation.md',
    'workflows/implement-feature.md', 'evaluations/scenarios.md',
    'evaluations/report-template.md', 'projects/README.md',
    'projects/registry.example.json',
)


def check_registry(path):
    data = json.loads(path.read_text(encoding='utf-8'))
    if not isinstance(data, dict) or type(data.get('schema_version')) is not int or data['schema_version'] != 1:
        raise ValueError('registry: schema_version deve ser 1')
    projects = data.get('projects')
    if not isinstance(projects, list) or not projects:
        raise ValueError('registry: projects deve ser uma lista não vazia')
    seen = set()
    for project in projects:
        if not isinstance(project, dict):
            raise ValueError('registry: cada projeto deve ser um objeto')
        for key in ('id', 'path', 'description', 'default_branch', 'notes'):
            if not isinstance(project.get(key), str) or not project[key].strip():
                raise ValueError(f'registry: campo inválido {key}')
        if project['id'] in seen:
            raise ValueError(f'registry: ID duplicado {project["id"]}')
        seen.add(project['id'])
        path_value = project['path']
        if not (PureWindowsPath(path_value).is_absolute() or PurePosixPath(path_value).is_absolute()):
            raise ValueError(f'registry: caminho deve ser absoluto ({project["id"]})')
        commands = project.get('test_commands')
        if not isinstance(commands, list) or not commands or any(
            not isinstance(command, str) or not command.strip() for command in commands
        ):
            raise ValueError('registry: test_commands deve conter strings não vazias')


def validate(root, registry):
    for relative in REQUIRED:
        path = root / relative
        if not path.is_file() or not path.read_text(encoding='utf-8').strip():
            raise ValueError(f'arquivo ausente ou vazio: {relative}')
    config = tomllib.loads((root / '.codex/config.toml').read_text(encoding='utf-8'))
    if config.get('sandbox_mode') != 'workspace-write' or config.get('approval_policy') != 'on-request':
        raise ValueError('política do kit deve ser workspace-write/on-request')
    if config.get('agents') != {'enabled': True, 'max_concurrent_threads_per_session': 2}:
        raise ValueError('configuração de agents divergente do contrato v0.1')
    for name in ('developer', 'qa'):
        agent = tomllib.loads((root / f'.codex/agents/{name}.toml').read_text(encoding='utf-8'))
        if set(agent) != {'name', 'description', 'developer_instructions'} or agent['name'] != name:
            raise ValueError(f'contrato de agente inválido: {name}')
        if any(not isinstance(value, str) or not value.strip() for value in agent.values()):
            raise ValueError(f'campos de agente vazios: {name}')
    check_registry(registry)
    for relative in REQUIRED:
        source = root / relative
        if source.suffix != '.md':
            continue
        for target in re.findall(r'\[[^\]]+\]\(([^)]+)\)', source.read_text(encoding='utf-8')):
            if '://' in target or target.startswith('#'):
                continue
            target = target.split('#', 1)[0]
            if not (source.parent / target).is_file():
                raise ValueError(f'link local quebrado em {relative}: {target}')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--registry', type=Path, default=ROOT / 'projects/registry.example.json')
    args = parser.parse_args()
    try:
        validate(ROOT, args.registry)
    except (OSError, ValueError) as error:
        print(f'FAIL: {error}', file=sys.stderr)
        return 1
    print(f'PASS: {len(REQUIRED)} arquivos; TOML, agentes, registry e links locais válidos.')
    print('Não executa modelos, comandos cadastrados ou testes de projetos externos.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
