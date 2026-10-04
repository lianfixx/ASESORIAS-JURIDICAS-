#!/usr/bin/env python3
"""Construye paquetes de metodologia; nunca recoge expedientes ni archivos arbitrarios."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import re
import zipfile

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / 'skills/milla-asesoria-juridica'


def package_files() -> list[Path]:
    files = []
    for path in sorted(SKILL.rglob('*')):
        if path.is_symlink():
            raise ValueError(f'No se empaquetan enlaces simbolicos: {path}')
        if path.is_file() and '__pycache__' not in path.parts:
            if path.suffix not in {'.md', '.json', '.py'}:
                raise ValueError(f'Tipo inesperado dentro de skill: {path.name}')
            files.append(path)
    return files


def validate_package() -> list[str]:
    issues = []
    text = (SKILL / 'SKILL.md').read_text(encoding='utf-8')
    if not text.startswith('---\n') or '\n---\n' not in text[4:]:
        return ['SKILL.md no tiene frontmatter delimitado.']
    metadata = text.split('---', 2)[1]
    found = re.search(r'^name:\s*([a-z0-9-]+)\s*$', metadata, re.M)
    if not found or found.group(1) != SKILL.name or '--' in found.group(1):
        issues.append('name invalido o distinto de carpeta.')
    desc = re.search(r'^description:\s*(.+)$', metadata, re.M)
    if not desc or not 1 <= len(desc.group(1)) <= 1024:
        issues.append('description ausente o fuera de longitud.')
    if len(text.splitlines()) >= 500:
        issues.append('SKILL.md debe mantenerse por debajo de 500 lineas.')
    for target in re.findall(r'\]\(([^)]+)\)', text):
        path = SKILL / target
        if not target.startswith(('http:', 'https:', '#')) and not path.is_file():
            issues.append(f'Referencia local ausente: {target}')
    for path in package_files():
        body = path.read_text(encoding='utf-8')
        if path.suffix == '.json':
            try:
                json.loads(body)
            except ValueError as exc:
                issues.append(f'JSON invalido {path.name}: {exc}')
        if re.search(r'(?<!\d)\d{18}(?!\d)', body):
            issues.append(f'Posible numero bancario de 18 digitos en {path.name}: revisar.')
        if re.search(r'(?i)(?:ghp_|github_pat_)[a-z0-9_]{15,}', body):
            issues.append(f'Posible token en {path.name}.')
    return issues


def build(output: Path) -> dict:
    output = output.resolve()
    if output == SKILL or SKILL in output.parents:
        raise ValueError('La salida no debe estar dentro de la skill.')
    issues = validate_package()
    if issues:
        raise ValueError('; '.join(issues))
    output.mkdir(parents=True, exist_ok=True)
    intro = '# MILLA ASESORIAS · GUIA UNIVERSAL · 0.1.0\n\nEdicion 2026-10-04. Metodo supervisado; no expediente, no autorizacion profesional ni actualizacion automatica.\n\nCada bloque identifica su archivo de origen. Las referencias internas estan incluidas mas adelante; no asumir acceso a documentos de clientes.\n\n'
    ordered = [ROOT / 'EMPIEZA_AQUI.md', SKILL / 'SKILL.md']
    ordered += sorted((SKILL / 'references').glob('*.md'))
    ordered += sorted((SKILL / 'assets').glob('*.md'))
    ordered += sorted((SKILL / 'assets').glob('*.json'))
    ordered += [ROOT / 'SECURITY.md', ROOT / 'docs/INSTALACION.md', ROOT / 'docs/RECAPITULACION.md', ROOT / 'docs/MEJORAS_Y_ACTUALIZACION.md']
    parts = [intro]
    for path in ordered:
        parts.append('\n\n---\n\n## ARCHIVO: ' + str(path.relative_to(ROOT)) + '\n\n' + path.read_text(encoding='utf-8'))
    body = ''.join(parts)
    products = []
    for suffix in ('md', 'txt'):
        dest = output / ('MILLA_GUIA_UNIVERSAL.' + suffix)
        dest.write_text(body, encoding='utf-8')
        products.append(dest)
    zip_path = output / 'milla-asesoria-juridica-0.1.0.zip'
    with zipfile.ZipFile(zip_path, 'w', compression=zipfile.ZIP_DEFLATED) as archive:
        for path in package_files():
            info = zipfile.ZipInfo('milla-asesoria-juridica/' + str(path.relative_to(SKILL)), date_time=(2026, 10, 4, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            archive.writestr(info, path.read_bytes())
    products.append(zip_path)
    manifest = {'version': '0.1.0', 'contains_client_data': False, 'warning': 'El escaneo tecnico no garantiza anonimato. Solo empaquetar metodologia revisada.', 'products': {p.name: {'sha256': hashlib.sha256(p.read_bytes()).hexdigest(), 'bytes': p.stat().st_size} for p in products}, 'skill_files': {str(p.relative_to(SKILL)): hashlib.sha256(p.read_bytes()).hexdigest() for p in package_files()}}
    (output / 'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=ROOT / 'dist')
    args = parser.parse_args()
    try:
        result = build(args.output)
    except (OSError, ValueError) as exc:
        parser.exit(1, f'Error: {exc}\n')
    print(json.dumps(result['products'], indent=2))


if __name__ == '__main__':
    main()
