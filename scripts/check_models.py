"""Preflight de modelos nativos; consulta catálogo sem executar inferência."""

import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tomllib

ROOT = Path(__file__).resolve().parents[1]


def read_config(path):
    return tomllib.loads(path.read_text(encoding='utf-8')) if path.exists() else {}


def resolve_models(root, user, override=None):
    project = read_config(root / '.codex/config.toml')
    parent = override or project.get('model') or user.get('model')
    if not isinstance(parent, str) or not parent.strip():
        raise ValueError('Modelo principal não definido; use --model com um slug do catálogo.')
    defaults = {**user.get('agents', {}), **project.get('agents', {})}
    models = {'orchestrator': parent}
    for role in ('developer', 'qa'):
        agent = read_config(root / f'.codex/agents/{role}.toml')
        models[role] = agent.get('model', defaults.get('default_subagent_model', parent))
        if not isinstance(models[role], str) or not models[role].strip():
            raise ValueError(f'Modelo inválido em {role}.')
    return models


def verify_models(models, catalog):
    entries = catalog.get('models')
    if not isinstance(entries, list) or not entries:
        raise ValueError('Catálogo vazio ou formato inesperado; seleção não confirmada.')
    listed = {entry['slug'] for entry in entries if entry.get('visibility') == 'list'}
    missing = [f'{role}={model}' for role, model in models.items() if model not in listed]
    if missing:
        raise ValueError('Modelo não listado para esta sessão: ' + ', '.join(missing)
                         + '. Nenhuma substituição automática foi feita.')
    return listed


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--model', help='Mesmo override principal que será passado a codex --model')
    args = parser.parse_args()
    try:
        home = Path(os.environ.get('CODEX_HOME', str(Path.home() / '.codex')))
        user = read_config(home / 'config.toml')
        models = resolve_models(ROOT, user, args.model)
        # No bundled-catalog fallback: errors are reported and no model is replaced.
        cli = shutil.which('codex')
        if cli is None:
            raise FileNotFoundError('Codex CLI não encontrado no PATH.')
        result = subprocess.run([cli, 'debug', 'models'], cwd=ROOT,
                                capture_output=True, text=True, encoding='utf-8', timeout=45)
        if result.returncode:
            raise ValueError(f'Falha ao consultar catálogo (exit {result.returncode}): {result.stderr.strip()}')
        if result.stderr.strip():
            print(result.stderr.strip(), file=sys.stderr)
        verify_models(models, json.loads(result.stdout))
        for role, model in models.items():
            print(f'{role}: {model}')
        print('PASS: modelos listados. Acesso real depende da execução; nenhum fallback aplicado.')
        print('Escopo: projeto confiável, config pessoal, sem profile ou override de spawn.')
        return 0
    except (OSError, ValueError, subprocess.TimeoutExpired) as error:
        print(f'BLOCKED: {error}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
