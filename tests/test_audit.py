"""Regresiones sinteticas de la auditoria; no son evaluaciones de modelos de IA."""
import copy
from contextlib import contextmanager
from datetime import date, timedelta
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
import zipfile
from test_control import c, ready_state, checked
from test_package import b


@contextmanager
def source_copy():
    old_root, old_skill = b.ROOT, b.SKILL
    with tempfile.TemporaryDirectory() as folder:
        root = Path(folder)/'repo'
        shutil.copytree(old_root, root, ignore=shutil.ignore_patterns('.git','__pycache__','dist'))
        b.ROOT, b.SKILL = root, root/'skills/milla-asesoria-juridica'
        try: yield root
        finally: b.ROOT, b.SKILL = old_root, old_skill


def write_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False), encoding='utf-8')


class AuditControlTests(unittest.TestCase):
    def test_malformed_top_values_never_crash(self):
        for value in (None, [], {}, True, 1, 1.5, '', 'invalido'):
            for field in ('stage','case_id','schema_version','skill_version','synthetic'):
                if field=='synthetic' and type(value) is bool: continue
                with self.subTest(field=field, value=type(value).__name__):
                    s=c.new_state('TEST'); s[field]=value
                    self.assertTrue(c.validate(s))
    def test_nested_flags_reject_truthy_values(self):
        for key,flag in [('privacy','reviewed'),('engagement','accepted'),('fees','approved'),('reading','complete')]:
            for value in ('true',1,[],{}):
                s=ready_state(); s[key][flag]=value
                self.assertTrue(checked(s,'emitir_diagnostico'))
    def test_lists_reject_non_objects(self):
        for key in ('facts','sources','documents','deadlines','approvals'):
            for value in (None,[],True,''):
                s=c.new_state('TEST'); s[key]=[value]
                self.assertTrue(c.validate(s),(key,value))
    def test_json_nonfinite_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            p=Path(folder)/'s.json'
            for value in ('NaN','Infinity','-Infinity'):
                p.write_text('{"synthetic":'+value+'}')
                with self.assertRaises(ValueError): c.load_json(p)
    def test_json_non_object_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            p=Path(folder)/'s.json'; p.write_text('[]')
            with self.assertRaises(ValueError): c.load_json(p)
    def test_json_deep_rejected_cleanly(self):
        with tempfile.TemporaryDirectory() as folder:
            p=Path(folder)/'s.json'; p.write_text('['*1500+'0'+']'*1500)
            with self.assertRaises(ValueError): c.load_json(p)
    def test_duplicate_ids_rejected(self):
        for key in ('sources','documents'):
            s=ready_state(); s[key].append(copy.deepcopy(s[key][0]))
            self.assertTrue(checked(s,'emitir_diagnostico'))
    def test_future_source_date_rejected(self):
        s=ready_state(); s['sources'][0]['checked_on']=(date.today()+timedelta(days=1)).isoformat()
        self.assertTrue(checked(s,'emitir_diagnostico'))
    def test_future_approval_rejected(self):
        s=ready_state(); s['approvals'][0]['date']=(date.today()+timedelta(days=1)).isoformat()
        self.assertTrue(checked(s,'emitir_diagnostico'))
    def test_document_change_invalidates_approval(self):
        s=ready_state(); s['documents'][0]['sha256']='b'*64
        self.assertTrue(c.validate(s,'emitir_diagnostico','DOC-001','b'*64))
    def test_current_file_mismatch(self):
        self.assertTrue(c.validate(ready_state(),'emitir_diagnostico','DOC-001','b'*64))
    def test_document_version_mismatch(self):
        s=ready_state(); s['documents'][0]['version']='2'
        self.assertTrue(checked(s,'emitir_diagnostico'))
    def test_approval_for_other_document_insufficient(self):
        s=ready_state(); s['approvals'][0]['document_id']='DOC-002'
        self.assertTrue(checked(s,'emitir_diagnostico'))
    def test_sources_bound_to_document(self):
        s=ready_state(); s['sources'].append(dict(id='SRC-002',status='NO_VERIFICADA'))
        s['documents'][0]['source_ids']=['SRC-002']
        self.assertTrue(checked(s,'emitir_diagnostico'))
    def test_nonexistent_source(self):
        s=ready_state(); s['documents'][0]['source_ids']=['SRC-UNKNOWN']
        self.assertTrue(checked(s,'emitir_diagnostico'))
    def test_document_draft_cannot_emit(self):
        s=ready_state(); s['documents'][0]['status']='borrador'
        self.assertTrue(checked(s,'emitir_diagnostico'))
    def test_no_implicit_document(self):
        self.assertTrue(c.validate(ready_state(),'emitir_diagnostico'))
    def test_schema_one_requires_review(self):
        s=ready_state(); s['schema_version']=1
        self.assertTrue(checked(s,'emitir_diagnostico'))
    def test_private_file_cannot_enter_repo(self):
        with self.assertRaises(ValueError): c.private_target(b.ROOT/'otro/estado.json')
    def test_private_file_can_be_outside(self):
        with tempfile.TemporaryDirectory() as folder:
            p=Path(folder)/'state.json'; self.assertEqual(c.private_target(p),p.resolve())
    def test_hash_reads_current_file(self):
        with tempfile.TemporaryDirectory() as folder:
            p=Path(folder)/'doc.txt'; p.write_bytes(b'sintetico')
            self.assertEqual(c.hash_document(p),hashlib.sha256(b'sintetico').hexdigest())
    def test_hash_rejects_symlink(self):
        with tempfile.TemporaryDirectory() as folder:
            p=Path(folder)/'doc.txt'; p.write_bytes(b'sintetico'); link=Path(folder)/'link'; link.symlink_to(p)
            with self.assertRaises(ValueError): c.hash_document(link)
    def test_money_and_rates_limit_nonfinite(self):
        for value in ('NaN','Infinity','0.123456789',[],True):
            with self.assertRaises(ValueError): c.phase_totals(dict(amount='1',tax_mode='incluido',tax_rate=value,instalments=['1']))
    def test_cli_requires_document(self):
        with tempfile.TemporaryDirectory() as folder:
            p=Path(folder)/'s.json'; write_json(p,ready_state())
            cmd=[sys.executable,str(c.SKILL/'scripts/control.py'),'check',str(p),'--gate','emitir_diagnostico']
            result=subprocess.run(cmd,capture_output=True,text=True)
            self.assertEqual(result.returncode,2); self.assertNotIn('Traceback',result.stderr)
    def test_cli_checks_real_document(self):
        with tempfile.TemporaryDirectory() as folder:
            p=Path(folder)/'s.json'; doc=Path(folder)/'d.txt'; doc.write_text('DOCUMENTO SINTETICO')
            s=ready_state(); sha=c.hash_document(doc); s['documents'][0]['sha256']=sha; s['approvals'][0]['document_sha256']=sha; write_json(p,s)
            cmd=[sys.executable,str(c.SKILL/'scripts/control.py'),'check',str(p),'--gate','emitir_diagnostico','--document-id','DOC-001','--document',str(doc)]
            self.assertEqual(subprocess.run(cmd,capture_output=True).returncode,0)
            doc.write_text('CAMBIO SINTETICO')
            self.assertEqual(subprocess.run(cmd,capture_output=True).returncode,1)
    def test_cli_init_never_overwrites(self):
        with tempfile.TemporaryDirectory() as folder:
            p=Path(folder)/'s.json'; p.write_text('ORIGINAL')
            cmd=[sys.executable,str(c.SKILL/'scripts/control.py'),'init','--id','TEST','--synthetic','--output',str(p)]
            self.assertEqual(subprocess.run(cmd,capture_output=True).returncode,2)
            self.assertEqual(p.read_text(),'ORIGINAL')


class AuditPackageTests(unittest.TestCase):
    def test_unapproved_skill_file_rejected(self):
        with source_copy():
            (b.SKILL/'assets/no_aprobado.md').write_text('Solo ejemplo sintetico')
            self.assertTrue(b.validate_package())
    def test_inventory_bad_type(self):
        with source_copy() as root:
            write_json(root/'PUBLIC_FILES.json',[])
            self.assertTrue(b.validate_package())
    def test_inventory_traversal(self):
        with source_copy() as root:
            p=root/'PUBLIC_FILES.json'; v=json.loads(p.read_text()); v['files'].append('../secret.txt'); write_json(p,v)
            self.assertTrue(b.validate_package())
    def test_inventory_duplicates(self):
        with source_copy() as root:
            p=root/'PUBLIC_FILES.json'; v=json.loads(p.read_text()); v['files'].append(v['files'][0]); write_json(p,v)
            self.assertTrue(b.validate_package())
    def test_inventory_requires_license(self):
        with source_copy() as root:
            p=root/'PUBLIC_FILES.json'; v=json.loads(p.read_text()); v['files'].remove('LICENSE'); write_json(p,v)
            self.assertTrue(b.validate_package())
    def test_unknown_tracked_root_file(self):
        with source_copy() as root:
            subprocess.run(['git','init','-q',str(root)],check=True)
            (root/'nota.txt').write_text('Dato sintetico')
            subprocess.run(['git','-C',str(root),'add','nota.txt'],check=True)
            self.assertTrue(b.validate_package())
    def test_untracked_root_file_excluded(self):
        with source_copy() as root, tempfile.TemporaryDirectory() as folder:
            (root/'nota.txt').write_text('Dato sintetico')
            b.build(Path(folder))
            with zipfile.ZipFile(Path(folder)/'MILLA_CODIGO_FUENTE.zip') as archive:
                self.assertNotIn('nota.txt',archive.namelist())
    def test_docs_scanned_and_value_not_logged(self):
        with source_copy() as root:
            token='ghp_'+'x'*32
            with (root/'README.md').open('a') as f: f.write('\n'+token+'\n')
            issues=b.validate_package()
            self.assertTrue(any('posible token' in x for x in issues))
            self.assertTrue(all(token not in x for x in issues))
    def test_all_supported_patterns(self):
        for value in ('ghp_'+'x'*32, '7'*18, '6'*10, '----'+'-BEGIN PRIVATE KEY-----'):
            self.assertTrue(b.scan_text(value,'SINTETICO'))
    def test_symlinks_never_packaged(self):
        with source_copy() as root:
            p=b.SKILL/'assets/enlace.md'; p.symlink_to(root/'README.md')
            self.assertTrue(b.validate_package())
    def test_license_copy_drift(self):
        with source_copy():
            (b.SKILL/'LICENSE').write_text('No es la licencia')
            self.assertTrue(b.validate_package())
    def test_version_drift(self):
        with source_copy():
            p=b.SKILL/'assets/configuracion.ejemplo.json'; v=json.loads(p.read_text()); v['version']='0.0.0'; write_json(p,v)
            self.assertTrue(b.validate_package())
    def test_json_invalid_no_crash(self):
        with source_copy():
            (b.SKILL/'assets/estado.ejemplo.json').write_text('{"bad":NaN}')
            self.assertTrue(b.validate_package())
    def test_output_directory_must_be_empty(self):
        with tempfile.TemporaryDirectory() as folder:
            p=Path(folder)/'keep.txt'; p.write_text('No borrar')
            with self.assertRaises(ValueError): b.build(Path(folder))
            self.assertEqual(p.read_text(),'No borrar')
    def test_manifest_does_not_certify_privacy(self):
        with tempfile.TemporaryDirectory() as folder:
            manifest=b.build(Path(folder))
            self.assertNotIn('contains_client_data',manifest)
            self.assertIs(manifest['privacy']['certifies_absence_of_personal_data'],False)
            self.assertTrue(manifest['privacy']['human_review_required'])
    def test_license_and_notice_in_all_outputs(self):
        with tempfile.TemporaryDirectory() as folder:
            manifest=b.build(Path(folder))
            for name in manifest['products']:
                p=Path(folder)/name
                if p.suffix=='.zip':
                    with zipfile.ZipFile(p) as archive:
                        for required in ('LICENSE','NOTICE'):
                            matches=[n for n in archive.namelist() if Path(n).name==required]
                            self.assertTrue(matches)
                            self.assertTrue(all(archive.read(n)==(b.ROOT/required).read_bytes() for n in matches))
                else:
                    self.assertIn((b.ROOT/'LICENSE').read_text(),p.read_text())
                    self.assertIn((b.ROOT/'NOTICE').read_text(),p.read_text())
    def test_source_manifest_matches_whitelist(self):
        with tempfile.TemporaryDirectory() as folder:
            manifest=b.build(Path(folder))
            allowed={str(p.relative_to(b.ROOT)) for p in b.source_files()}
            self.assertEqual(set(manifest['source_files']),allowed)
            with zipfile.ZipFile(Path(folder)/'MILLA_CODIGO_FUENTE.zip') as archive:
                self.assertEqual(set(archive.namelist()),allowed)
    def test_workflow_does_not_overwrite_source_zip(self):
        text=(b.ROOT/'.github/workflows/validar.yml').read_text()
        self.assertNotIn('git archive',text)
        self.assertIn('contents: read',text)
        self.assertIn('persist-credentials: false',text)


if __name__=='__main__': unittest.main()
