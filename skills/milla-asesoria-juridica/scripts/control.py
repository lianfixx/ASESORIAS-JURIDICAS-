#!/usr/bin/env python3
# Copyright 2026 lianfixx and contributors. SPDX-License-Identifier: Apache-2.0
"""Control estructural e integridad registrada; no autentica ni autoriza actos juridicos."""
from __future__ import annotations
import argparse
import copy
from datetime import date
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
import hashlib
import json
from pathlib import Path
import re
import sys

SKILL = Path(__file__).resolve().parents[1]
STAGES = {'recepcion', 'admision', 'resumen', 'investigacion', 'asesoria', 'diagnostico', 'contratacion', 'negociacion', 'actuacion', 'seguimiento', 'cierre', 'pausa'}
FACT_STATES = {'DOCUMENTADO', 'MANIFESTADO', 'INFERIDO', 'CONTRADICHO', 'PENDIENTE'}
GATES = {'emitir_diagnostico', 'enviar_propuesta', 'presentar_actuacion'}
CENT = Decimal('0.01')


def nonempty(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def member(value: object, options: set) -> bool:
    return isinstance(value, str) and value in options


def identifier(value: object) -> bool:
    return isinstance(value, str) and re.fullmatch(r'[A-Z0-9][A-Z0-9_-]{0,63}', value) is not None


def digest(value: object) -> bool:
    return isinstance(value, str) and re.fullmatch(r'[0-9a-f]{64}', value) is not None


def load_json(path: Path) -> dict:
    if path.stat().st_size > 2 * 1024 * 1024:
        raise ValueError('JSON demasiado grande para este control.')
    def unique(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError('Clave JSON duplicada; revisar archivo.')
            result[key] = value
        return result
    def reject(_):
        raise ValueError('Constante JSON no estandar.')
    try:
        obj = json.loads(path.read_text(encoding='utf-8'), object_pairs_hook=unique, parse_constant=reject)
    except RecursionError as exc:
        raise ValueError('JSON demasiado anidado.') from exc
    if not isinstance(obj, dict):
        raise ValueError('Se requiere un objeto JSON.')
    return obj


def new_state(case_id: str, synthetic: bool = False) -> dict:
    if not identifier(case_id) or type(synthetic) is not bool:
        raise ValueError('ID interno de 1–64 caracteres A-Z, 0-9, _ o - y synthetic booleano; no usar nombres.')
    obj = copy.deepcopy(load_json(SKILL/'assets/estado.ejemplo.json'))
    obj.update(case_id=case_id, synthetic=synthetic)
    return obj


def money(value: object) -> Decimal:
    if not isinstance(value, str) or not re.fullmatch(r'[0-9]{1,15}(?:\.[0-9]{1,2})?', value):
        raise ValueError('Importe como texto no negativo: hasta 15 enteros y dos decimales, sin simbolos ni comas.')
    return Decimal(value).quantize(CENT)


def phase_totals(phase: dict) -> dict:
    if not isinstance(phase, dict):
        raise ValueError('Etapa de honorarios debe ser objeto.')
    amount = money(phase.get('amount'))
    mode = phase.get('tax_mode')
    if not member(mode, {'incluido', 'adicional'}):
        raise ValueError('Indicar impuesto incluido o adicional; no se presume.')
    raw_rate = phase.get('tax_rate')
    if not isinstance(raw_rate, str) or not re.fullmatch(r'[01](?:\.[0-9]{1,8})?', raw_rate):
        raise ValueError('Tasa aprobada como texto decimal entre 0 y 1, hasta ocho decimales.')
    rate = Decimal(raw_rate)
    if not Decimal('0') <= rate <= Decimal('1'):
        raise ValueError('Tasa fuera de 0–1.')
    gross = (amount * (Decimal('1') + rate)).quantize(CENT, rounding=ROUND_HALF_UP) if mode == 'adicional' else amount
    credit = money(phase.get('credit_gross', '0.00'))
    if credit > gross:
        raise ValueError('Credito superior al importe bruto.')
    total = gross - credit
    payments = phase.get('instalments')
    if not isinstance(payments, list) or not 1 <= len(payments) <= 1000:
        raise ValueError('Falta calendario de 1–1000 pagos; no se genera anticipo por defecto.')
    planned = sum((money(item) for item in payments), Decimal('0.00'))
    if planned != total:
        raise ValueError(f'Calendario {planned:.2f}; total {total:.2f}; diferencia {planned-total:.2f}.')
    return {'gross': f'{gross:.2f}', 'credit_gross': f'{credit:.2f}', 'total': f'{total:.2f}', 'instalments_sum': f'{planned:.2f}'}


def iso_day(value: object) -> bool:
    try:
        return isinstance(value, str) and date.fromisoformat(value).isoformat() == value
    except ValueError:
        return False


def checked_day(value: object) -> bool:
    return iso_day(value) and date.fromisoformat(value) <= date.today()


def hash_document(path: Path) -> str:
    if any(p.is_symlink() for p in (path.absolute(), *path.absolute().parents)) or not path.is_file() or not 0 < path.stat().st_size <= 25*1024*1024:
        raise ValueError('Documento requerido: archivo regular de 1 byte a 25 MiB, sin enlace simbolico.')
    result = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(65536), b''):
            result.update(block)
    return result.hexdigest()


def validate(state: dict, gate: str | None = None, document_id: str | None = None, document_sha256: str | None = None) -> list[str]:
    """Valida el registro; el llamador aporta la huella del archivo actual, no una firma."""
    errors = []
    if not isinstance(state, dict):
        return ['El estado debe ser objeto.']
    info = load_json(SKILL/'assets/release.json')
    if type(state.get('schema_version')) is not int or state['schema_version'] != info['schema_version']:
        errors.append('Esquema distinto; requiere migracion revisada, no concesion automatica de aprobaciones.')
    if state.get('skill_version') != info['version']:
        errors.append('Version distinta; revisar compatibilidad.')
    if not identifier(state.get('case_id')):
        errors.append('ID interno invalido.')
    if type(state.get('synthetic')) is not bool:
        errors.append('synthetic debe ser booleano.')
    if not member(state.get('stage'), STAGES):
        errors.append('Etapa desconocida o tipo incorrecto.')
    for key in ('jurisdiction', 'risk', 'reading', 'conflict', 'privacy', 'counsel', 'engagement', 'fees'):
        if not isinstance(state.get(key), dict):
            errors.append(f'{key} debe ser objeto.')
    for key in ('facts', 'sources', 'deadlines', 'approvals', 'documents'):
        if not isinstance(state.get(key), list) or len(state[key]) > 10000:
            errors.append(f'{key} debe ser lista de hasta 10000 entradas.')
    if errors:
        return errors
    for key, flag in [('jurisdiction','verified'),('reading','complete'),('conflict','reviewed'),('privacy','reviewed'),('counsel','assigned'),('engagement','accepted'),('fees','approved')]:
        if type(state[key].get(flag)) is not bool:
            errors.append(f'{key}.{flag} debe ser booleano.')
    if not member(state['risk'].get('level'), {'ordinario','urgente','sin_revisar'}):
        errors.append('Nivel de riesgo invalido.')
    items = state['reading'].get('items')
    if not isinstance(items, list) or not all(nonempty(x) for x in items):
        errors.append('Cobertura de lectura: se requieren referencias de texto no vacias.')
    seen = {'facts': set(), 'sources': set(), 'documents': set()}
    for key in seen:
        for record in state[key]:
            if not isinstance(record, dict) or not identifier(record.get('id')):
                errors.append(f'{key}: registro sin ID valido.')
            elif record['id'] in seen[key]:
                errors.append(f'{key}: ID duplicado.')
            else:
                seen[key].add(record['id'])
    for fact in state['facts']:
        if not isinstance(fact, dict) or not member(fact.get('status'), FACT_STATES) or not nonempty(fact.get('source_ref')):
            errors.append('Hecho sin estado valido o referencia de origen.')
    sources = {}
    for source in state['sources']:
        if not isinstance(source, dict) or not member(source.get('status'), {'VERIFICADA','PARCIAL','NO_VERIFICADA'}):
            errors.append('Fuente con estado invalido.')
            continue
        if identifier(source.get('id')):
            sources[source['id']] = source
        if source['status'] == 'VERIFICADA' and (not all(nonempty(source.get(k)) for k in ('reference','locator')) or not checked_day(source.get('checked_on'))):
            errors.append('Fuente verificada sin referencia/localizador/fecha valida, o fechada en el futuro.')
    for deadline in state['deadlines']:
        if not isinstance(deadline, dict) or type(deadline.get('verified')) is not bool:
            errors.append('Plazo sin objeto o indicador booleano.')
        elif deadline['verified'] and (not all(nonempty(deadline.get(k)) for k in ('legal_source','trigger_evidence','calendar','reviewed_by')) or not iso_day(deadline.get('due_on'))):
            errors.append('Plazo verificado sin fundamento, evento, calendario, revisora o fecha valida.')
    for doc in state['documents']:
        if not isinstance(doc, dict):
            continue
        refs = doc.get('source_ids')
        if not nonempty(doc.get('version')) or not digest(doc.get('sha256')) or not member(doc.get('status'), {'borrador','revisado','emitido'}):
            errors.append('Documento sin version, huella SHA-256 o estado valido.')
        if not isinstance(refs, list) or not all(identifier(x) and x in sources for x in refs):
            errors.append('Documento con referencias de fuente inexistentes o mal formadas.')
    for approval in state['approvals']:
        if not isinstance(approval, dict) or not member(approval.get('action'), GATES) or not identifier(approval.get('document_id')) or not nonempty(approval.get('document_version')) or not digest(approval.get('document_sha256')) or not all(nonempty(approval.get(k)) for k in ('approved_by','evidence_ref')) or not checked_day(approval.get('date')):
            errors.append('Aprobacion incompleta o sin version/huella/fecha valida; requiere revision.')
    phases = state['fees'].get('phases')
    if not isinstance(phases, list):
        errors.append('fees.phases debe ser lista.')
    else:
        for index, phase in enumerate(phases, 1):
            try:
                phase_totals(phase)
            except (ValueError, InvalidOperation) as exc:
                errors.append(f'Honorarios etapa {index}: {exc}')
    if gate is None:
        return errors
    if not member(gate, GATES):
        return errors + ['Control no reconocido.']
    if errors:
        return errors
    jurisdiction = state['jurisdiction']
    if jurisdiction['verified'] is not True or not all(nonempty(jurisdiction.get(k)) for k in ('country','state','regime')):
        errors.append('Jurisdiccion/regimen pendientes.')
    risk = state['risk']
    if risk['level'] != 'ordinario' or not all(nonempty(risk.get(k)) for k in ('reviewed_by','evidence_ref')):
        errors.append('Riesgo pendiente/urgente: requiere revision, no ruta ordinaria. Este control NO debe retrasar ayuda urgente.')
    if state['reading']['complete'] is not True or not items:
        errors.append('Lectura incompleta o sin registro.')
    for key in ('privacy','conflict'):
        if state[key]['reviewed'] is not True or not all(nonempty(state[key].get(k)) for k in ('reviewed_by','evidence_ref')):
            errors.append(f'Revision {key} pendiente o sin referencia.')
    if state['counsel']['assigned'] is not True or not nonempty(state['counsel'].get('professional_ref')):
        errors.append('Responsable profesional no acreditado en el estado.')
    docs = [d for d in state['documents'] if d['id'] == document_id]
    if not identifier(document_id) or not digest(document_sha256) or not docs:
        errors.append('Identifica el documento y la huella calculada de su archivo actual.')
    else:
        doc = docs[0]
        if doc['sha256'] != document_sha256 or doc['status'] not in {'revisado','emitido'}:
            errors.append('Archivo distinto del revisado o documento aun en borrador.')
        if not doc['source_ids'] or any(sources[x]['status'] != 'VERIFICADA' for x in doc['source_ids']):
            errors.append('Las fuentes utilizadas por este documento no estan verificadas.')
        approvals = [a for a in state['approvals'] if isinstance(a, dict)]
        if not any(a.get('action') == gate and a.get('document_id') == document_id and a.get('document_version') == doc['version'] and a.get('document_sha256') == document_sha256 and all(nonempty(a.get(k)) for k in ('approved_by','evidence_ref')) and checked_day(a.get('date')) for a in approvals):
            errors.append('Falta aprobacion referenciada para esta accion y esta version/huella exacta.')
    if phases and (state['fees']['approved'] is not True or not nonempty(state['fees'].get('approval_ref'))):
        errors.append('Honorarios incluidos sin aprobacion referenciada.')
    if gate in {'enviar_propuesta','presentar_actuacion'}:
        engagement = state['engagement']
        if engagement['accepted'] is not True or not all(nonempty(engagement.get(k)) for k in ('scope','evidence_ref')):
            errors.append('Alcance/mandato para actuar no documentado.')
        if any(d['verified'] is not True for d in state['deadlines']):
            errors.append('Plazos pendientes de revision antes de actuar.')
    return errors


def private_target(target: Path) -> Path:
    target = target.resolve()
    roots = [SKILL]
    roots += [p for p in SKILL.parents if (p/'PUBLIC_FILES.json').is_file() or (p/'.git').exists()]
    if any(target == root or root in target.parents for root in roots):
        raise ValueError('El estado privado debe quedar fuera de toda la biblioteca publica y de la skill instalada.')
    return target


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    init = sub.add_parser('init'); init.add_argument('--id', required=True); init.add_argument('--output', type=Path, required=True); init.add_argument('--synthetic', action='store_true')
    for name in ('check','status','fees'):
        command = sub.add_parser(name); command.add_argument('file', type=Path)
        if name == 'check':
            command.add_argument('--gate', choices=sorted(GATES)); command.add_argument('--document-id'); command.add_argument('--document', type=Path)
    args = parser.parse_args()
    try:
        if args.command == 'init':
            target = private_target(args.output); obj = new_state(args.id, args.synthetic)
            target.parent.mkdir(parents=True, exist_ok=True)
            with target.open('x', encoding='utf-8') as handle:
                json.dump(obj, handle, ensure_ascii=False, indent=2); handle.write('\n')
            print('Estado creado fuera de la biblioteca. No hay autorizacion ni caso validado.')
            return 0
        obj = load_json(args.file)
        if args.command == 'status':
            print(json.dumps({k: obj.get(k) for k in ('case_id','skill_version','stage','next_action')}, ensure_ascii=False, indent=2)); return 0
        if args.command == 'fees':
            phases = obj.get('fees', {}).get('phases', [])
            if not isinstance(phases, list) or not phases:
                raise ValueError('No hay etapas validas; no se inventara un precio.')
            print(json.dumps([phase_totals(p) for p in phases], indent=2))
            print('Solo aritmetica; revisar impuestos, retenciones, alcance y contrato por separado.'); return 0
        if args.gate and (not args.document_id or not args.document):
            raise ValueError('--gate requiere --document-id y --document para cotejar el archivo real.')
        current_hash = hash_document(args.document) if args.document else None
        errors = validate(obj, args.gate, args.document_id, current_hash)
        if errors:
            print('PENDIENTES:\n'+'\n'.join('- '+e for e in errors)); return 1
        print('Sin inconsistencias detectadas. NO autentica aprobacion, veracidad, suficiencia juridica ni autoridad para actuar.'); return 0
    except (OSError, ValueError, TypeError, AttributeError, InvalidOperation) as exc:
        print(f'Error: {exc}', file=sys.stderr); return 2


if __name__ == '__main__':
    raise SystemExit(main())
