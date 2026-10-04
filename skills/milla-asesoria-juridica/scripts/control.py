#!/usr/bin/env python3
"""Controles auxiliares de estado y aritmetica; no decide ni autoriza actos juridicos."""
from __future__ import annotations
import argparse
import copy
from datetime import date
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
import json
from pathlib import Path
import re
import sys

SKILL = Path(__file__).resolve().parents[1]
STAGES = {'recepcion', 'admision', 'resumen', 'investigacion', 'asesoria', 'diagnostico', 'contratacion', 'negociacion', 'actuacion', 'seguimiento', 'cierre', 'pausa'}
FACT_STATES = {'DOCUMENTADO', 'MANIFESTADO', 'INFERIDO', 'CONTRADICHO', 'PENDIENTE'}
GATES = {'emitir_diagnostico', 'enviar_propuesta', 'presentar_actuacion'}
CENT = Decimal('0.01')


def load_json(path: Path) -> dict:
    def unique(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError(f'Clave JSON duplicada: {key}')
            result[key] = value
        return result
    obj = json.loads(path.read_text(encoding='utf-8'), object_pairs_hook=unique)
    if not isinstance(obj, dict):
        raise ValueError('Se requiere un objeto JSON, no una lista o un valor suelto.')
    return obj


def new_state(case_id: str, synthetic: bool = False) -> dict:
    if not re.fullmatch(r'[A-Z0-9][A-Z0-9_-]{0,63}', case_id):
        raise ValueError('Usa un ID interno de 1 a 64 caracteres: A-Z, 0-9, _ o -; no el nombre del cliente.')
    obj = copy.deepcopy(load_json(SKILL / 'assets/estado.ejemplo.json'))
    obj.update(case_id=case_id, synthetic=synthetic)
    return obj


def money(value: object) -> Decimal:
    if not isinstance(value, str) or not re.fullmatch(r'\d+(?:\.\d{1,2})?', value):
        raise ValueError('Los importes deben ser textos no negativos con hasta dos decimales, sin simbolos ni comas.')
    return Decimal(value).quantize(CENT)


def phase_totals(phase: dict) -> dict:
    amount = money(phase.get('amount'))
    mode = phase.get('tax_mode')
    if mode not in {'incluido', 'adicional'}:
        raise ValueError('Debes indicar si el impuesto esta incluido o es adicional; no se presume.')
    raw_rate = phase.get('tax_rate')
    if not isinstance(raw_rate, str) or not re.fullmatch(r'\d+(?:\.\d+)?', raw_rate):
        raise ValueError('Indica la tasa aprobada como texto decimal; no existe tasa predeterminada.')
    rate = Decimal(raw_rate)
    if not Decimal('0') <= rate <= Decimal('1'):
        raise ValueError('La tasa debe estar entre 0 y 1.')
    gross = (amount * (Decimal('1') + rate)).quantize(CENT, rounding=ROUND_HALF_UP) if mode == 'adicional' else amount
    credit = money(phase.get('credit_gross', '0.00'))
    if credit > gross:
        raise ValueError('El credito no puede superar el importe bruto de la etapa.')
    total = gross - credit
    payments = phase.get('instalments')
    if not isinstance(payments, list) or not payments:
        raise ValueError('Falta un calendario de importes; no se genera un anticipo por defecto.')
    paid_plan = sum((money(item) for item in payments), Decimal('0.00'))
    if paid_plan != total:
        raise ValueError(f'El calendario suma {paid_plan:.2f} y debe sumar {total:.2f}; diferencia {paid_plan-total:.2f}.')
    return {'gross': f'{gross:.2f}', 'credit_gross': f'{credit:.2f}', 'total': f'{total:.2f}', 'instalments_sum': f'{paid_plan:.2f}'}


def iso_day(value: object) -> bool:
    try:
        return isinstance(value, str) and date.fromisoformat(value).isoformat() == value
    except ValueError:
        return False


def validate(state: dict, gate: str | None = None) -> list[str]:
    """Revisa estructura y evidencia registrada. No autentica documentos ni aprobaciones."""
    errors = []
    if state.get('schema_version') != 1:
        errors.append('schema_version debe ser 1; revisar migracion.')
    if state.get('skill_version') != '0.1.0':
        errors.append('Version distinta; revisar compatibilidad antes de continuar.')
    if not isinstance(state.get('case_id'), str) or not re.fullmatch(r'[A-Z0-9][A-Z0-9_-]{0,63}', state.get('case_id', '')):
        errors.append('Falta ID interno valido.')
    if state.get('stage') not in STAGES:
        errors.append('Etapa desconocida.')
    objects = ('jurisdiction', 'risk', 'reading', 'conflict', 'privacy', 'counsel', 'engagement', 'fees')
    for key in objects:
        if not isinstance(state.get(key), dict):
            errors.append(f'{key} debe ser objeto.')
    for key in ('facts', 'sources', 'deadlines', 'approvals'):
        if not isinstance(state.get(key), list):
            errors.append(f'{key} debe ser lista.')
    if errors:
        return errors
    for fact in state['facts']:
        if not isinstance(fact, dict) or fact.get('status') not in FACT_STATES or not fact.get('id') or not fact.get('source_ref'):
            errors.append('Cada hecho requiere id, estado valido y referencia de origen.')
    for source in state['sources']:
        if not isinstance(source, dict) or source.get('status') not in {'VERIFICADA', 'PARCIAL', 'NO_VERIFICADA'}:
            errors.append('Fuente con estado invalido.')
            continue
        if source['status'] == 'VERIFICADA' and (not source.get('locator') or not source.get('reference') or not iso_day(source.get('checked_on'))):
            errors.append('Fuente marcada verificada sin referencia, localizador o fecha ISO valida.')
    for deadline in state['deadlines']:
        if not isinstance(deadline, dict):
            errors.append('Plazo debe ser objeto.')
            continue
        if deadline.get('verified') is True:
            required = ('legal_source', 'trigger_evidence', 'calendar', 'reviewed_by', 'due_on')
            if not all(deadline.get(key) for key in required) or not iso_day(deadline.get('due_on')):
                errors.append('Plazo marcado verificado sin fundamento, evento, calendario, revisora o fecha valida.')
    phases = state['fees'].get('phases', [])
    if not isinstance(phases, list):
        errors.append('fees.phases debe ser lista.')
    else:
        for number, phase in enumerate(phases, 1):
            try:
                if not isinstance(phase, dict):
                    raise ValueError('Etapa de honorarios debe ser objeto.')
                phase_totals(phase)
            except (ValueError, InvalidOperation) as exc:
                errors.append(f'Honorarios etapa {number}: {exc}')
    if gate is None:
        return errors
    if gate not in GATES:
        return errors + ['Control solicitado no reconocido.']
    jurisdiction = state['jurisdiction']
    if jurisdiction.get('verified') is not True or not all(jurisdiction.get(k) for k in ('country', 'state', 'regime')):
        errors.append('Jurisdiccion/regimen no verificados.')
    risk = state['risk']
    if risk.get('level') != 'ordinario' or not risk.get('reviewed_by') or not risk.get('evidence_ref'):
        errors.append('Riesgo pendiente o urgente: revisar/escalar antes de la ruta ordinaria; no demorar ayuda urgente.')
    reading = state['reading']
    if reading.get('complete') is not True or not isinstance(reading.get('items'), list) or not reading['items']:
        errors.append('Cobertura de lectura insuficientemente documentada.')
    for key in ('privacy', 'conflict'):
        item = state[key]
        if item.get('reviewed') is not True or not item.get('reviewed_by') or not item.get('evidence_ref'):
            errors.append(f'Revision de {key} pendiente o sin referencia.')
    if state['counsel'].get('assigned') is not True or not state['counsel'].get('professional_ref'):
        errors.append('Responsable profesional no acreditado en el estado.')
    if not any(isinstance(s, dict) and s.get('status') == 'VERIFICADA' for s in state['sources']):
        errors.append('No hay fuentes juridicas verificadas registradas; revisar suficiencia material aparte.')
    approvals = [a for a in state['approvals'] if isinstance(a, dict) and a.get('action') == gate]
    if not any(a.get('approved_by') and a.get('evidence_ref') and iso_day(a.get('date')) for a in approvals):
        errors.append('Falta referencia de aprobacion humana para esta accion concreta.')
    if phases and (state['fees'].get('approved') is not True or not state['fees'].get('approval_ref')):
        errors.append('Los honorarios incluidos no constan aprobados.')
    if gate in {'enviar_propuesta', 'presentar_actuacion'}:
        engagement = state['engagement']
        if engagement.get('accepted') is not True or not engagement.get('scope') or not engagement.get('evidence_ref'):
            errors.append('Alcance/mandato para actuar no documentado.')
        if any(d.get('verified') is not True for d in state['deadlines'] if isinstance(d, dict)):
            errors.append('Hay plazos pendientes de revision antes de actuar.')
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    init = sub.add_parser('init', help='Crear estado privado en blanco; no sobrescribe.')
    init.add_argument('--id', required=True)
    init.add_argument('--output', type=Path, required=True)
    init.add_argument('--synthetic', action='store_true')
    check = sub.add_parser('check', help='Comprobar estructura; --gate agrega condiciones registradas.')
    check.add_argument('file', type=Path)
    check.add_argument('--gate', choices=sorted(GATES))
    status = sub.add_parser('status', help='Mostrar etapa y siguiente accion registrada.')
    status.add_argument('file', type=Path)
    fees = sub.add_parser('fees', help='Revisar solo aritmetica de etapas, no procedencia de impuestos.')
    fees.add_argument('file', type=Path)
    args = parser.parse_args()
    try:
        if args.command == 'init':
            target = args.output.resolve()
            if target == SKILL or SKILL in target.parents:
                raise ValueError('No crear expedientes dentro de la carpeta distribuible de la skill.')
            obj = new_state(args.id, synthetic=args.synthetic)
            target.parent.mkdir(parents=True, exist_ok=True)
            with target.open('x', encoding='utf-8') as handle:
                json.dump(obj, handle, ensure_ascii=False, indent=2)
                handle.write('\n')
            print(f'Estado creado en {target}. Conservar privado; no hay autorizacion ni caso validado.')
            return 0
        obj = load_json(args.file)
        if args.command == 'status':
            print(json.dumps({k: obj.get(k) for k in ('case_id', 'skill_version', 'stage', 'next_action')}, ensure_ascii=False, indent=2))
            return 0
        if args.command == 'fees':
            phases = obj.get('fees', {}).get('phases', [])
            if not phases:
                raise ValueError('No hay etapas de honorarios; no se inventara un precio.')
            print(json.dumps([phase_totals(p) for p in phases], indent=2))
            print('Solo aritmetica: revisar impuestos, retenciones, alcance, autorizacion y contrato por separado.')
            return 0
        errors = validate(obj, args.gate)
        if errors:
            print('PENDIENTES / BLOQUEOS REGISTRADOS:\n' + '\n'.join('- ' + e for e in errors))
            return 1
        print('Sin inconsistencias detectadas por estos controles. NO acredita verdad, suficiencia juridica ni autorizacion real.')
        return 0
    except (OSError, ValueError, TypeError, AttributeError, InvalidOperation) as exc:
        print(f'Error: {exc}', file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
