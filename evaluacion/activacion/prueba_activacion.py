#!/usr/bin/env python3
"""Prueba local (no es un test unitario ni corre en CI). Requiere el CLI `claude` autenticado; consume cuota.
Prueba realista de activación: la skill instalada en .claude/skills, consulta tal cual, sin nombrar la skill."""
import json, os, re, shutil, subprocess, sys, tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / 'skills/milla-asesoria-juridica'
evalset = json.load(open(ROOT / 'evaluacion/activacion/consultas.json', encoding='utf-8'))
if len(sys.argv) != 4: sys.exit('Uso: prueba_activacion.py candidatas.json repeticiones salida.json')
cands = json.load(open(sys.argv[1], encoding='utf-8')); runs = int(sys.argv[2]); outp = sys.argv[3]
def with_desc(text, desc):
    return re.sub(r'^description:.*$', 'description: ' + json.dumps(desc, ensure_ascii=False), text, count=1, flags=re.M)
def one(job):
    cname, desc, qi, q, k = job
    d = Path(tempfile.mkdtemp(prefix='trig-'))
    try:
        dst = d/'.claude/skills/milla-asesoria-juridica'; shutil.copytree(SRC, dst)
        s = dst/'SKILL.md'; s.write_text(with_desc(s.read_text(encoding='utf-8'), desc), encoding='utf-8')
        env = {k2: v for k2, v in os.environ.items() if k2 != 'CLAUDECODE'}
        cmd = ['claude','-p',q['query'],'--output-format','stream-json','--verbose','--model','claude-sonnet-5-5',
               '--setting-sources','project','--tools','Skill,Read,Glob,Grep','--allowedTools','Skill,Read,Glob,Grep','--max-turns','3']
        try: r = subprocess.run(cmd, cwd=d, capture_output=True, text=True, timeout=240, env=env); raw = r.stdout
        except subprocess.TimeoutExpired as e: raw = e.stdout or ''
        trig = False
        for line in raw.splitlines():
            try: ev = json.loads(line)
            except Exception: continue
            if ev.get('type') == 'assistant':
                for b in ev['message'].get('content', []):
                    if b.get('type') == 'tool_use' and b['name'] == 'Skill' and 'milla' in str(b['input'].get('skill','')): trig = True
        return cname, qi, trig
    finally: shutil.rmtree(d, ignore_errors=True)
jobs = [(c, desc, i, q, k) for c, desc in cands.items() for i, q in enumerate(evalset) for k in range(runs)]
res = {}
with ThreadPoolExecutor(8) as ex:
    for cname, qi, trig in ex.map(one, jobs): res.setdefault(cname, {}).setdefault(qi, []).append(trig)
summary = {}
for c, byq in res.items():
    tp = sum(sum(v) for i, v in byq.items() if evalset[i]['should_trigger']); np_ = sum(len(v) for i, v in byq.items() if evalset[i]['should_trigger'])
    fp = sum(sum(v) for i, v in byq.items() if not evalset[i]['should_trigger']); nn = sum(len(v) for i, v in byq.items() if not evalset[i]['should_trigger'])
    summary[c] = {'chars': len(cands[c]), 'activa_cuando_debe': f'{tp}/{np_}', 'activa_cuando_no_debe': f'{fp}/{nn}',
                  'por_consulta': {evalset[i]['query'][:60]: v for i, v in byq.items()}}
json.dump(summary, open(outp, 'w'), ensure_ascii=False, indent=1)
for c, s in summary.items(): print(c, s['chars'], 'debe:', s['activa_cuando_debe'], 'no debe:', s['activa_cuando_no_debe'])
