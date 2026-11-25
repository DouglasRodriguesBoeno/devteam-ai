"""Regression checks for inheritance, selection and unavailable models."""
import importlib.util
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / 'scripts/check_models.py'
spec = importlib.util.spec_from_file_location('check_models', SCRIPT)
models = importlib.util.module_from_spec(spec)
spec.loader.exec_module(models)


class ModelSelectionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / '.codex/agents').mkdir(parents=True)
        (self.root / '.codex/config.toml').write_text('model = "parent"\n')

    def test_inheritance_and_session_override(self):
        self.assertEqual(models.resolve_models(self.root, {'model': 'old'}),
                         dict.fromkeys(('orchestrator', 'developer', 'qa'), 'parent'))
        self.assertEqual(models.resolve_models(self.root, {}, 'session'),
                         dict.fromkeys(('orchestrator', 'developer', 'qa'), 'session'))

    def test_agent_override_preserves_other_inheritance(self):
        (self.root / '.codex/agents/developer.toml').write_text('model = "specific"\n')
        self.assertEqual(models.resolve_models(self.root, {}, 'session'),
                         {'orchestrator': 'session', 'developer': 'specific', 'qa': 'session'})

    def test_personal_subagent_default_is_reported(self):
        result = models.resolve_models(self.root, {'agents': {'default_subagent_model': 'personal'}})
        self.assertEqual(result['qa'], 'personal')

    def test_unavailable_and_hidden_models_fail_without_replacement(self):
        selection = {'qa': 'missing'}
        with self.assertRaisesRegex(ValueError, 'Nenhuma substituição'):
            models.verify_models(selection, {'models': [{'slug': 'missing', 'visibility': 'hide'}]})
        self.assertEqual(selection, {'qa': 'missing'})

    def test_new_slug_needs_no_code_change(self):
        self.assertEqual(models.verify_models({'qa': 'future-model'},
                         {'models': [{'slug': 'future-model', 'visibility': 'list'}]}), {'future-model'})

    @unittest.skipUnless(os.name == 'nt', 'Windows npm launcher')
    def test_preflight_with_only_cmd_launcher(self):
        bin_dir = self.root / 'npm bin'
        bin_dir.mkdir()
        (bin_dir / 'codex.cmd').write_text(
            '@echo off\nif not "%*"=="debug models" exit /b 2\n'
            'echo {"models":[{"slug":"sample","visibility":"list"}]}\n',
            encoding='ascii')
        env = dict(os.environ, PATH=str(bin_dir), PATHEXT='.EXE;.CMD',
                   CODEX_HOME=str(self.root), PYTHONIOENCODING='utf-8')
        result = subprocess.run([sys.executable, str(SCRIPT), '--model', 'sample'],
                                cwd=self.root, env=env, capture_output=True,
                                encoding='utf-8', timeout=15)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('orchestrator: sample', result.stdout)


if __name__ == '__main__':
    unittest.main()
