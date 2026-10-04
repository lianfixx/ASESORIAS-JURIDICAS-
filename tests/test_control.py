import copy
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('milla_control', ROOT / 'skills/milla-asesoria-juridica/scripts/control.py')
c = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c)


def ready_state(action='emitir_diagnostico'):
    # Datos completamente sinteticos: no sirven como evidencia de aprobacion real.
    s = c.new_state('PRUEBA-001', synthetic=True)
    s['jurisdiction'] = dict(country='MX', state='ENTIDAD SINTETICA', regime='REGIMEN DE PRUEBA', verified=True)
    s['risk'] = dict(level='ordinario', reviewed_by='REVISORA SINTETICA', evidence_ref='DEMO-R01')
    s['reading'] = dict(complete=True, items=['NOTA SINTETICA'])
    for key in ('privacy', 'conflict'):
        s[key] = dict(reviewed=True, reviewed_by='REVISORA SINTETICA', evidence_ref='DEMO-P01')
    s['counsel'] = dict(assigned=True, professional_ref='DEMO-PROF')
    s['sources'] = [dict(id='SRC-001', status='VERIFICADA', reference='FUENTE SINTETICA', locator='APARTADO DEMO', checked_on='2026-10-04')]
    s['documents'] = [dict(id='DOC-001', version='1', sha256='a'*64, status='revisado', source_ids=['SRC-001'])]
    s['approvals'] = [dict(action=action, document_id='DOC-001', document_version='1', document_sha256='a'*64, approved_by='REVISORA SINTETICA', date='2026-10-04', evidence_ref='DEMO-A01')]
    return s


def checked(state, gate=None):
    return c.validate(state, gate, 'DOC-001' if gate else None, 'a'*64 if gate else None)


class ControlTests(unittest.TestCase):
    def test_initial_structure(self):
        self.assertEqual(checked(c.new_state('ABC-001')), [])
    def test_initial_cannot_emit(self):
        self.assertTrue(checked(c.new_state('ABC-001'), 'emitir_diagnostico'))
    def test_id_rejects_name(self):
        with self.assertRaises(ValueError): c.new_state('Nombre Apellido')
    def test_id_rejects_path(self):
        with self.assertRaises(ValueError): c.new_state('../PRIVATE')
    def test_boolean_is_not_money(self):
        with self.assertRaises(ValueError): c.money(True)
    def test_negative_rejected(self):
        with self.assertRaises(ValueError): c.money('-1.00')
    def test_precision_rejected(self):
        with self.assertRaises(ValueError): c.money('1.001')
    def test_money_requires_text(self):
        with self.assertRaises(ValueError): c.money(1000)
    def test_additional_tax(self):
        p = dict(amount='1000.00', tax_mode='adicional', tax_rate='0.16', instalments=['580.00','580.00'])
        self.assertEqual(c.phase_totals(p)['total'], '1160.00')
    def test_tax_included_and_credit(self):
        p = dict(amount='1160.00', tax_mode='incluido', tax_rate='0.16', credit_gross='160.00', instalments=['400.00','600.00'])
        self.assertEqual(c.phase_totals(p)['total'], '1000.00')
    def test_no_default_deposit(self):
        with self.assertRaises(ValueError): c.phase_totals(dict(amount='1000', tax_mode='incluido', tax_rate='0.16'))
    def test_missing_tax_mode(self):
        with self.assertRaises(ValueError): c.phase_totals(dict(amount='1000', tax_rate='0', instalments=['1000']))
    def test_missing_tax_rate(self):
        with self.assertRaises(ValueError): c.phase_totals(dict(amount='1000', tax_mode='incluido', instalments=['1000']))
    def test_plan_mismatch(self):
        with self.assertRaises(ValueError): c.phase_totals(dict(amount='1000', tax_mode='incluido', tax_rate='0', instalments=['400','500']))
    def test_excess_credit(self):
        with self.assertRaises(ValueError): c.phase_totals(dict(amount='1000', tax_mode='incluido', tax_rate='0', credit_gross='1001', instalments=['0']))
    def test_synthetic_recorded_conditions(self):
        self.assertEqual(checked(ready_state(), 'emitir_diagnostico'), [])
    def test_no_approval_no_emission(self):
        s = ready_state(); s['approvals'] = []
        self.assertTrue(checked(s, 'emitir_diagnostico'))
    def test_urgent_not_normal_flow(self):
        s = ready_state(); s['risk']['level'] = 'urgente'
        self.assertTrue(checked(s, 'emitir_diagnostico'))
    def test_reading_must_be_registered(self):
        s = ready_state(); s['reading']['items'] = []
        self.assertTrue(checked(s, 'emitir_diagnostico'))
    def test_counsel_required(self):
        s = ready_state(); s['counsel']['assigned'] = False
        self.assertTrue(checked(s, 'emitir_diagnostico'))
    def test_sending_requires_scope(self):
        s = ready_state('enviar_propuesta')
        self.assertTrue(checked(s, 'enviar_propuesta'))
    def test_sending_recorded_scope(self):
        s = ready_state('enviar_propuesta'); s['engagement'] = dict(accepted=True, scope='ALCANCE SINTETICO', evidence_ref='DEMO-C01')
        self.assertEqual(checked(s, 'enviar_propuesta'), [])
    def test_other_action_approval_insufficient(self):
        self.assertTrue(checked(ready_state(), 'presentar_actuacion'))
    def test_unverified_deadline(self):
        s = ready_state('enviar_propuesta'); s['deadlines'] = [dict(verified=False)]
        self.assertTrue(checked(s, 'enviar_propuesta'))
    def test_verified_deadline_missing_support(self):
        s = c.new_state('A'); s['deadlines'] = [dict(verified=True, due_on='2026-10-04')]
        self.assertTrue(checked(s))
    def test_source_missing_locator(self):
        s = c.new_state('A'); s['sources'] = [dict(id='SRC-001', status='VERIFICADA', reference='DEMO', checked_on='2026-10-04')]
        self.assertTrue(checked(s))
    def test_bad_date(self):
        self.assertFalse(c.iso_day('2026-02-30'))
    def test_bad_nested_type(self):
        s = c.new_state('A'); s['privacy'] = None
        self.assertTrue(checked(s))
    def test_wrong_version(self):
        s = c.new_state('A'); s['skill_version'] = '99'
        self.assertTrue(checked(s))
    def test_unknown_fact(self):
        s = c.new_state('A'); s['facts'] = [dict(id='H1', status='GANADO', source_ref='DEMO')]
        self.assertTrue(checked(s))
    def test_duplicate_json_key(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder)/'state.json'; path.write_text('{"stage":1,"stage":2}', encoding='utf-8')
            with self.assertRaises(ValueError): c.load_json(path)
    def test_synthetic_states_independent(self):
        a = c.new_state('A'); b = c.new_state('B'); a['facts'].append({})
        self.assertEqual(b['facts'], [])


if __name__ == '__main__': unittest.main()
