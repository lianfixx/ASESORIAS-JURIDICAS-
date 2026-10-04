#!/usr/bin/env python3
# Copyright 2026 lianfixx and contributors. SPDX-License-Identifier: Apache-2.0
"""Empaqueta exclusivamente archivos publicos inventariados; no certifica anonimato."""
from __future__ import annotations
import argparse
from datetime import date
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import subprocess
import zipfile

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / 'skills/milla-asesoria-juridica'
MAX_FILE_BYTES = 512 * 1024
ALLOWED_SUFFIXES = {'.md', '.json', '.py', '.yml', '.txt'}
SPECIAL_NAMES = {'LICENSE', 'NOTICE', '.gitignore', 'CODEOWNERS'}
SENSITIVE = {
    'posible token': r'(?i)(?:ghp_|github_pat_)[a-z0-9_]{15,}',
    'posible cuenta de 18 digitos': r'(?<!\w)\d{18}(?!\w)',
    'posible telefono de 10 digitos': r'(?<!\w)\d{10}(?!\w)',
    'posible CURP': r'\b[A-Z][AEIOUX][A-Z]{2}\d{6}[HM][A-Z]{5}[0-9A-Z]\d\b',
    'posible RFC': r'\b[A-ZÑ&]{3,4}\d{6}[A-Z0-9]{3}\b',
    'posible clave privada': r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----',
}


def strict_json(path: Path):
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
        return json.loads(path.read_text(encoding='utf-8'), object_pairs_hook=unique, parse_constant=reject)
    except RecursionError as exc:
        raise ValueError('JSON demasiado anidado.') from exc


def release() -> dict:
    info = strict_json(SKILL / 'assets/release.json')
    if not isinstance(info, dict) or not re.fullmatch(r'\d+\.\d+\.\d+', str(info.get('version', ''))):
        raise ValueError('Version de release invalida.')
    if info.get('license') != 'Apache-2.0' or type(info.get('schema_version')) is not int:
        raise ValueError('Licencia o esquema de release invalido.')
    if date.fromisoformat(info['released_on']).isoformat() != info['released_on']:
        raise ValueError('Fecha de release invalida.')
    return info


def source_files() -> list[Path]:
    catalog = strict_json(ROOT / 'PUBLIC_FILES.json')
    names = catalog.get('files') if isinstance(catalog, dict) else None
    if not isinstance(catalog, dict) or catalog.get('purpose') != 'public-methodology-only' or not isinstance(names, list) or not names:
        raise ValueError('Falta inventario explicito de archivos publicos.')
    if not all(isinstance(n, str) for n in names) or len(names) != len(set(names)):
        raise ValueError('Inventario duplicado o mal formado.')
    files = []
    for name in sorted(names):
        rel = PurePosixPath(name)
        if rel.is_absolute() or '..' in rel.parts or '\\' in name or str(rel) != name:
            raise ValueError('Ruta no segura en inventario publico.')
        path = ROOT / name
        if path.name not in SPECIAL_NAMES and path.suffix not in ALLOWED_SUFFIXES:
            raise ValueError(f'Tipo no permitido: {name}')
        if any(p.is_symlink() for p in (path, *path.parents) if p == ROOT or ROOT in p.parents):
            raise ValueError(f'Enlace simbolico no permitido: {name}')
        if not path.is_file() or path.stat().st_size > MAX_FILE_BYTES:
            raise ValueError(f'Archivo ausente o demasiado grande: {name}')
        path.read_text(encoding='utf-8')
        files.append(path)
    required = {'PUBLIC_FILES.json','LICENSE','NOTICE','USO_Y_LICENCIA.md',
        'skills/milla-asesoria-juridica/LICENSE','skills/milla-asesoria-juridica/NOTICE',
        'skills/milla-asesoria-juridica/SKILL.md','skills/milla-asesoria-juridica/assets/release.json',
        'skills/milla-asesoria-juridica/assets/estado.ejemplo.json',
        'skills/milla-asesoria-juridica/assets/configuracion.ejemplo.json'}
    if not required.issubset(names):
        raise ValueError('Inventario sin archivos esenciales o sin incluirse a si mismo.')
    allowed = set(files)
    for path in SKILL.rglob('*'):
        if '__pycache__' in path.parts:
            continue
        if path.is_symlink() or (path.is_file() and path not in allowed):
            raise ValueError(f'Archivo no aprobado en skill: {path.relative_to(ROOT)}')
    return files


def package_files() -> list[Path]:
    return [p for p in source_files() if SKILL in p.parents]


def scan_text(body: str, label: str) -> list[str]:
    issues = []
    for number, line in enumerate(body.splitlines(), 1):
        for kind, pattern in SENSITIVE.items():
            if re.search(pattern, line):
                issues.append(f'{label}:{number}: {kind}; revisar sin exponer el valor en logs.')
    return issues


def validate_package() -> list[str]:
    issues = []
    try:
        files = source_files()
        info = release()
    except (OSError, ValueError, TypeError, AttributeError, KeyError) as exc:
        return [str(exc)]
    for path in files:
        body = path.read_text(encoding='utf-8')
        issues.extend(scan_text(body, str(path.relative_to(ROOT))))
        if path.suffix == '.json':
            try:
                strict_json(path)
            except ValueError:
                issues.append(f'JSON invalido: {path.relative_to(ROOT)}')
        if path.suffix == '.md':
            for target in re.findall(r'\]\(([^)\s]+)\)', body):
                if target.startswith(('http:', 'https:', '#', 'mailto:')):
                    continue
                target = target.split('#')[0]
                if target and not (path.parent / target).is_file():
                    issues.append(f'Referencia local ausente: {path.relative_to(ROOT)} -> {target}')
    text = (SKILL / 'SKILL.md').read_text(encoding='utf-8')
    if not text.startswith('---\n') or '\n---\n' not in text[4:]:
        issues.append('Frontmatter ausente.')
    else:
        metadata = text.split('---', 2)[1]
        found = re.search(r'^name:\s*([a-z0-9-]+)\s*$', metadata, re.M)
        desc = re.search(r'^description:\s*(.+)$', metadata, re.M)
        if not found or found.group(1) != SKILL.name or '--' in found.group(1):
            issues.append('Nombre de skill invalido.')
        if not desc or not 1 <= len(desc.group(1)) <= 1024:
            issues.append('Descripcion invalida.')
        if f'version: "{info["version"]}"' not in metadata or 'license: Apache-2.0' not in metadata:
            issues.append('Version/licencia de skill incoherente.')
    if len(text.splitlines()) >= 500:
        issues.append('Skill demasiado extensa.')
    for filename in ('LICENSE', 'NOTICE'):
        if (ROOT / filename).read_bytes() != (SKILL / filename).read_bytes():
            issues.append(f'{filename} de skill distinto del canonico.')
    try:
        state = strict_json(SKILL / 'assets/estado.ejemplo.json')
        config = strict_json(SKILL / 'assets/configuracion.ejemplo.json')
        if not isinstance(state, dict) or not isinstance(config, dict):
            raise ValueError('Estado y configuracion deben ser objetos.')
    except (ValueError, OSError) as exc:
        return issues + [str(exc)]
    if state.get('skill_version') != info['version'] or state.get('schema_version') != info['schema_version']:
        issues.append('Estado de ejemplo de otra version/esquema.')
    if config.get('version') != info['version'] or config.get('distribution_license') != info['license']:
        issues.append('Configuracion con version/licencia incoherente.')
    if (ROOT / '.git').exists():
        result = subprocess.run(['git', '-C', str(ROOT), 'ls-files', '-z'], capture_output=True, check=True)
        tracked = set(result.stdout.decode().split('\0')) - {''}
        approved = {str(p.relative_to(ROOT)) for p in files}
        for name in sorted(tracked - approved):
            issues.append(f'Archivo versionado fuera del inventario publico: {name}')
    return issues


def write_zip(path: Path, entries: dict[str, bytes], released_on: str) -> None:
    day = date.fromisoformat(released_on)
    stamp = (day.year, day.month, day.day, 0, 0, 0)
    with zipfile.ZipFile(path, 'w') as archive:
        for name, data in sorted(entries.items()):
            item = zipfile.ZipInfo(name, date_time=stamp)
            item.create_system = 3
            item.compress_type = zipfile.ZIP_DEFLATED
            item.external_attr = 0o100644 << 16
            archive.writestr(item, data)


def build(output: Path) -> dict:
    output = output.resolve()
    if output == ROOT or output == SKILL or SKILL in output.parents:
        raise ValueError('No escribir el paquete sobre la fuente o dentro de la skill.')
    if output.exists() and (not output.is_dir() or any(output.iterdir())):
        raise ValueError('La salida debe ser una carpeta vacia; evita mezclar versiones o sobrescribir datos.')
    issues = validate_package()
    if issues:
        raise ValueError('; '.join(issues))
    info = release()
    files = source_files()
    output.mkdir(parents=True, exist_ok=True)
    version = info['version']
    parts = [f'# MILLA ASESORIAS · GUIA UNIVERSAL · {version}\n\nEdicion {info["released_on"]}. Apache-2.0. Piloto supervisado; no expediente ni aprobacion juridica.\n\n']
    ordered = [ROOT/'NOTICE', ROOT/'USO_Y_LICENCIA.md', ROOT/'EMPIEZA_AQUI.md', SKILL/'SKILL.md']
    ordered += sorted((SKILL/'references').glob('*.md'))
    ordered += sorted((SKILL/'assets').glob('*.md')) + sorted((SKILL/'assets').glob('*.json'))
    ordered += [ROOT/'SECURITY.md', ROOT/'docs/INSTALACION.md', ROOT/'docs/RECAPITULACION.md', ROOT/'docs/MEJORAS_Y_ACTUALIZACION.md', ROOT/'LICENSE']
    for path in ordered:
        if path not in files:
            raise ValueError('La guia intenta incorporar un archivo no aprobado.')
        parts.append('\n\n---\n\n## ARCHIVO: '+str(path.relative_to(ROOT))+'\n\n'+path.read_text(encoding='utf-8'))
    products = []
    for ext in ('md', 'txt'):
        dest = output / f'MILLA_GUIA_UNIVERSAL.{ext}'
        dest.write_text(''.join(parts), encoding='utf-8')
        products.append(dest)
    dest = output / f'milla-asesoria-juridica-{version}.zip'
    write_zip(dest, {f'{SKILL.name}/{p.relative_to(SKILL)}': p.read_bytes() for p in package_files()}, info['released_on'])
    products.append(dest)
    dest = output / 'MILLA_CODIGO_FUENTE.zip'
    write_zip(dest, {str(p.relative_to(ROOT)): p.read_bytes() for p in files}, info['released_on'])
    products.append(dest)
    manifest = {
        'version': version, 'license': info['license'], 'schema_version': info['schema_version'],
        'privacy': {'scan_scope': 'inventario publico completo', 'human_review_required': True,
                    'certifies_absence_of_personal_data': False, 'warning': 'Patrones limitados; posibles falsos positivos y negativos.'},
        'products': {p.name: {'sha256': hashlib.sha256(p.read_bytes()).hexdigest(), 'bytes': p.stat().st_size} for p in products},
        'source_files': {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in files},
    }
    (output/'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=ROOT/'dist')
    args = parser.parse_args()
    try:
        result = build(args.output)
    except (OSError, ValueError, TypeError, KeyError, subprocess.SubprocessError) as exc:
        parser.exit(1, f'Error: {exc}\n')
    print(json.dumps(result['products'], indent=2))


if __name__ == '__main__':
    main()
