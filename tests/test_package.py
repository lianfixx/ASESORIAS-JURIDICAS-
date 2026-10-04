import hashlib
import importlib.util
import json
from pathlib import Path
import re
import tempfile
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('milla_build', ROOT / 'scripts/build.py')
b = importlib.util.module_from_spec(spec); spec.loader.exec_module(b)


class PackageTests(unittest.TestCase):
    def test_package_structure(self):
        self.assertEqual(b.validate_package(), [])
    def test_reference_links_in_skill(self):
        text = (b.SKILL/'SKILL.md').read_text(encoding='utf-8')
        for target in re.findall(r'\]\(([^)]+)\)', text):
            self.assertTrue((b.SKILL/target).is_file(), target)
    def test_initial_state_has_no_approvals(self):
        s = json.loads((b.SKILL/'assets/estado.ejemplo.json').read_text(encoding='utf-8'))
        self.assertEqual(s['approvals'], [])
        self.assertFalse(s['fees']['approved'])
    def test_eval_ids_unique(self):
        es = json.loads((b.SKILL/'assets/evaluaciones.json').read_text(encoding='utf-8'))['cases']
        self.assertGreaterEqual(len(es), 24)
        self.assertEqual(len({e['id'] for e in es}), len(es))
    def test_source_ids_unique(self):
        ss = json.loads((b.SKILL/'assets/fuentes.json').read_text(encoding='utf-8'))['sources']
        self.assertEqual(len({s['id'] for s in ss}), len(ss))
        self.assertTrue(all(s['url'].startswith('https://') and s['locator'] for s in ss))
    def test_no_binary_case_files(self):
        self.assertTrue(all(p.suffix in {'.md','.json','.py'} or p.name in {'LICENSE','NOTICE'} for p in b.package_files()))
    def test_build_outputs_and_hashes(self):
        with tempfile.TemporaryDirectory() as folder:
            manifest = b.build(Path(folder))
            for name, info in manifest['products'].items():
                self.assertEqual(hashlib.sha256((Path(folder)/name).read_bytes()).hexdigest(), info['sha256'])
    def test_zip_single_top_directory(self):
        with tempfile.TemporaryDirectory() as folder:
            b.build(Path(folder))
            with zipfile.ZipFile(Path(folder)/f'milla-asesoria-juridica-{b.release()["version"]}.zip') as archive:
                self.assertTrue(all(n.startswith('milla-asesoria-juridica/') for n in archive.namelist()))
                self.assertIn('milla-asesoria-juridica/SKILL.md', archive.namelist())
                self.assertFalse(any('..' in Path(n).parts for n in archive.namelist()))
    def test_universal_includes_all_reference_texts(self):
        with tempfile.TemporaryDirectory() as folder:
            b.build(Path(folder)); guide = (Path(folder)/'MILLA_GUIA_UNIVERSAL.md').read_text(encoding='utf-8')
            for ref in (b.SKILL/'references').glob('*.md'):
                self.assertIn(ref.read_text(encoding='utf-8'), guide)
    def test_reproducible_zip(self):
        with tempfile.TemporaryDirectory() as a, tempfile.TemporaryDirectory() as d:
            x = b.build(Path(a)); y = b.build(Path(d))
            self.assertEqual(x['products'], y['products'])
    def test_build_rejects_skill_output(self):
        with self.assertRaises(ValueError): b.build(b.SKILL/'dist')
    def test_durations(self):
        text = (b.SKILL/'references/flujo.md').read_text()
        slots = re.findall(r'\| (\d+)–(\d+) \| (\d+)–(\d+) \|', text)
        self.assertEqual(len(slots), 7)
        for column, total in ((0,30),(2,45)):
            end = 0
            for row in slots:
                start, stop = map(int, row[column:column+2])
                self.assertEqual(start, end); self.assertGreater(stop, start); end = stop
            self.assertEqual(end, total)


if __name__ == '__main__': unittest.main()
