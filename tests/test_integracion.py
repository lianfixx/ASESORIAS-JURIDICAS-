# SPDX-License-Identifier: LicenseRef-MILLA-Professional-1.0
"""Controles de integración 0.3.1; no evalúan corrección jurídica ni activación en IA."""
from __future__ import annotations
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import tempfile
import unittest
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / 'skills/milla-asesoria-juridica'


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    loaded = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(loaded)
    return loaded


CONTROL = module('control', SKILL / 'scripts/control.py')
BUILD = module('build', ROOT / 'scripts/build.py')


class Integracion(unittest.TestCase):
    def test_01_frontmatter(self):
        text = (SKILL / 'SKILL.md').read_text(encoding='utf-8')
        self.assertTrue(text.startswith('---\n'))
        self.assertIn('\n---\n', text[4:])
        self.assertIn('name: milla-asesoria-juridica', text)
        self.assertIn('license: LicenseRef-MILLA-Professional-1.0', text)

    def test_02_descripcion(self):
        desc = re.search(r'^description: (.+)$', (SKILL / 'SKILL.md').read_text(encoding='utf-8'), re.M).group(1)
        self.assertEqual(len(desc), 200)
        self.assertNotIn(': ', desc)

    def test_03_versiones(self):
        for filename, key in [('release.json', 'version'), ('estado.ejemplo.json', 'skill_version'),
                              ('configuracion.ejemplo.json', 'version'), ('evaluaciones.json', 'version')]:
            with self.subTest(filename=filename):
                self.assertEqual(CONTROL.load_json(SKILL / 'assets' / filename)[key], '0.3.1')
        self.assertIn('version: "0.3.1"', (SKILL / 'SKILL.md').read_text(encoding='utf-8'))

    def test_04_licencia_conservada(self):
        self.assertEqual((ROOT / 'LICENSE').read_bytes(), (SKILL / 'LICENSE').read_bytes())
        self.assertEqual((ROOT / 'USO_Y_LICENCIA.md').read_bytes(), (SKILL / 'references/uso-licencia.md').read_bytes())
        self.assertEqual(hashlib.sha1(b'blob ' + str(len((ROOT/'LICENSE').read_bytes())).encode() + b'\0' + (ROOT/'LICENSE').read_bytes()).hexdigest(), 'dbf85e5cbd7ab6c72265305870188c04ebec0580')

    def test_05_avisos_historicos(self):
        self.assertTrue((SKILL / 'LICENSES/Apache-2.0.txt').is_file())
        self.assertIn('componentes', (SKILL / 'NOTICE').read_text(encoding='utf-8'))
        self.assertIn('SPDX-License-Identifier: Apache-2.0', (SKILL / 'scripts/control.py').read_text(encoding='utf-8'))

    def test_06_enlaces_locales(self):
        for path in SKILL.rglob('*.md'):
            for link in re.findall(r'\]\(([^\s)]+)\)', path.read_text(encoding='utf-8')):
                if '://' not in link and not link.startswith(('#', 'mailto:')):
                    self.assertTrue((path.parent / link.split('#')[0]).exists(), f'{path}: {link}')

    def test_07_json_valido(self):
        for path in SKILL.rglob('*.json'):
            with self.subTest(path=path):
                self.assertIsInstance(CONTROL.load_json(path), dict)

    def test_08_escenarios(self):
        cases = CONTROL.load_json(SKILL / 'assets/evaluaciones.json')['cases']
        self.assertEqual([c['id'] for c in cases], [f'E{i:02d}' for i in range(1, 36)])
        for case in cases:
            self.assertTrue(case['input'] and case['expected'] and case['critical_failure'])

    def test_09_privacidad_configuracion(self):
        config = CONTROL.load_json(SKILL / 'assets/configuracion.ejemplo.json')
        self.assertIsNone(config['responsible_professional'])
        self.assertIsNone(config['approved_fee_policy_ref'])
        self.assertTrue(config['external_actions_require_specific_authorization'])
        self.assertEqual(config['distribution_license'], 'LicenseRef-MILLA-Professional-1.0')

    def test_10_estado_sintetico(self):
        state = CONTROL.new_state('PRUEBA-001', synthetic=True)
        self.assertEqual(CONTROL.validate(state), [])
        self.assertTrue(state['synthetic'])
        self.assertEqual(state['approvals'], [])

    def test_11_sin_autorizacion(self):
        state = CONTROL.new_state('PRUEBA-001', synthetic=True)
        for gate in CONTROL.GATES:
            self.assertTrue(CONTROL.validate(state, gate=gate))

    def test_12_id_invalido(self):
        for identifier in ('nombre cliente', '../PRIVADO', '', 'A'*65):
            with self.subTest(identifier=identifier), self.assertRaises(ValueError):
                CONTROL.new_state(identifier)

    def test_13_prohibir_estado_en_repo(self):
        with self.assertRaises(ValueError):
            CONTROL.private_target(ROOT / 'estado-cliente.json')

    def test_14_version_antigua(self):
        state = CONTROL.new_state('PRUEBA-001', synthetic=True)
        state['skill_version'] = '0.2.2'
        self.assertTrue(CONTROL.validate(state))

    def test_15_importes_invalidos(self):
        for amount in ('-1', 'NaN', '1e3', '1,000.00', '$20', '1.999'):
            with self.subTest(amount=amount), self.assertRaises(ValueError):
                CONTROL.money(amount)

    def test_16_suma_honorarios(self):
        phase = dict(amount='1000.00', tax_mode='incluido', tax_rate='0', credit_gross='100.00', instalments=['400.00', '500.00'])
        self.assertEqual(CONTROL.phase_totals(phase)['total'], '900.00')
        phase['instalments'] = ['899.99']
        with self.assertRaises(ValueError):
            CONTROL.phase_totals(phase)

    def test_17_claves_duplicadas(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'duplicado.json'
            path.write_text('{"id": 1, "id": 2}', encoding='utf-8')
            with self.assertRaises(ValueError):
                CONTROL.load_json(path)

    def test_18_paquete_inventariado(self):
        self.assertEqual(len(BUILD.package_files()), 22)
        with tempfile.TemporaryDirectory() as tmp:
            paths = BUILD.build(Path(tmp))
            with ZipFile(paths[0]) as archive:
                self.assertEqual(len(archive.namelist()), 22)
                self.assertTrue(all(p.startswith('milla-asesoria-juridica/') for p in archive.namelist()))
                self.assertIsNone(archive.testzip())
                self.assertFalse(any('/evaluacion/' in p or '/tests/' in p for p in archive.namelist()))
            self.assertEqual(paths[0].read_bytes(), paths[1].read_bytes())

    def test_19_build_reproducible(self):
        with tempfile.TemporaryDirectory() as a, tempfile.TemporaryDirectory() as b:
            left, right = BUILD.build(Path(a)), BUILD.build(Path(b))
            self.assertEqual([p.read_bytes() for p in left], [p.read_bytes() for p in right])

    def test_20_destino_seguro(self):
        with self.assertRaises(ValueError):
            BUILD.build(SKILL / 'salida')

    def test_21_sin_falsa_aprobacion(self):
        release = CONTROL.load_json(SKILL / 'assets/release.json')
        self.assertEqual(release['status'], 'piloto_supervisado')
        self.assertEqual(release['legal_review'], 'pendiente')

    def test_22_huella_documental(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'sintetico.txt'
            path.write_bytes(b'PRUEBA SINTETICA')
            self.assertEqual(CONTROL.hash_document(path), hashlib.sha256(path.read_bytes()).hexdigest())


if __name__ == '__main__':
    unittest.main()
