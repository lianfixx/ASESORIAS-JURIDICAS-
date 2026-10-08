#!/usr/bin/env python3
# SPDX-License-Identifier: LicenseRef-MILLA-Professional-1.0
"""Empaqueta únicamente los archivos inventariados. No instala ni autoriza el uso."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import re
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

ROOT = Path(__file__).resolve().parents[1]
PREFIX = Path('skills/milla-asesoria-juridica')


def package_files(root: Path = ROOT) -> list[Path]:
    inventory = json.loads((root / 'PUBLIC_FILES.json').read_text(encoding='utf-8'))['files']
    if not isinstance(inventory, list) or not inventory or len(set(inventory)) != len(inventory):
        raise ValueError('Inventario vacío, duplicado o inválido.')
    files = []
    for name in inventory:
        relative = Path(name)
        if relative.is_absolute() or '..' in relative.parts or not relative.is_relative_to(PREFIX):
            raise ValueError('Ruta no permitida en el paquete.')
        path = root / relative
        if any(p.is_symlink() for p in (path, *path.parents)) or not path.is_file():
            raise ValueError(f'Archivo ausente o enlace simbólico: {name}')
        files.append(path)
    actual = {p.relative_to(root).as_posix() for p in (root / PREFIX).rglob('*')
              if p.is_file() and '__pycache__' not in p.parts}
    if actual != set(inventory):
        raise ValueError('Hay archivos de la skill fuera del inventario o faltantes.')
    return sorted(files)


def build(output: Path, root: Path = ROOT) -> list[Path]:
    output = output.resolve()
    if output == (root / PREFIX).resolve() or (root / PREFIX).resolve() in output.parents:
        raise ValueError('El destino no puede estar dentro de la skill.')
    files = package_files(root)
    release = json.loads((root / PREFIX / 'assets/release.json').read_text(encoding='utf-8'))
    version = release['version']
    if not isinstance(version, str) or not re.fullmatch(r'\d+\.\d+\.\d+', version):
        raise ValueError('Versión inválida.')
    output.mkdir(parents=True, exist_ok=True)
    stem = f'milla-asesoria-juridica-{version}'
    archive = output / f'{stem}.zip'
    with ZipFile(archive, 'w', compression=ZIP_DEFLATED, compresslevel=9) as bundle:
        for path in files:
            info = ZipInfo(path.relative_to(root / 'skills').as_posix(), (1980, 1, 1, 0, 0, 0))
            info.compress_type = ZIP_DEFLATED
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            bundle.writestr(info, path.read_bytes())
    alias = output / f'{stem}.skill'
    alias.write_bytes(archive.read_bytes())
    guide = output / f'MILLA_GUIA_UNIVERSAL_{version}.txt'
    ordered = sorted(files, key=lambda p: (p.name != 'SKILL.md', p.as_posix()))
    sections = ['MILLA · GUÍA UNIVERSAL ' + version,
                'Piloto supervisado. Aplicar LICENSE. Este archivo no instala una skill en una cuenta.']
    for path in ordered:
        sections.append('\n===== ' + path.relative_to(root / PREFIX).as_posix() + ' =====\n' + path.read_text(encoding='utf-8'))
    guide.write_text('\n\n'.join(sections) + '\n', encoding='utf-8')
    artifacts = [archive, alias, guide]
    manifest = output / 'SHA256SUMS.txt'
    manifest.write_text(''.join(f'{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.name}\n' for p in artifacts), encoding='utf-8')
    return artifacts + [manifest]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    try:
        for path in build(args.output):
            print(path)
    except (OSError, ValueError, KeyError, TypeError) as exc:
        parser.exit(1, f'Error de empaquetado: {exc}\n')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
