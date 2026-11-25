"""Regression checks for the validator's registry CLI."""

import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]


class RegistryValidationTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.registry_dir = Path(temp.name)

    def run_validator(self, registry):
        return subprocess.run(
            [sys.executable, str(ROOT / 'scripts/validate.py'), '--registry', str(registry)],
            cwd=ROOT,
            env=dict(os.environ, PYTHONIOENCODING='utf-8'),
            capture_output=True,
            encoding='utf-8',
            timeout=15,
        )

    def test_truncated_registry_reports_path_and_line(self):
        registry = self.registry_dir / 'truncated registry.json'
        registry.write_text('{\n  "schema_version": 1,\n  "projects": [', encoding='utf-8')

        result = self.run_validator(registry)

        self.assertEqual(result.returncode, 1)
        self.assertIn(str(registry), result.stderr)
        self.assertRegex(result.stderr, r'\blinha 3\b')

    def test_valid_registry_copy_passes(self):
        registry = self.registry_dir / 'valid registry.json'
        shutil.copyfile(ROOT / 'projects/registry.example.json', registry)

        result = self.run_validator(registry)

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('PASS:', result.stdout)
