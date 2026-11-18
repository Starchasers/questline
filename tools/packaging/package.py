#!/usr/bin/env python3
"""Build owned code and package discovered mods using only Python's standard library."""
import argparse
import hashlib
import json
import math
import os
from pathlib import Path
import re
import subprocess
import tempfile
import zipfile
import xml.etree.ElementTree as ET

MODID = re.compile(r'[a-z][a-z0-9]*\Z')
PRERELEASE_ID = r'(?:0|[1-9][0-9]*|[0-9A-Za-z-]*[A-Za-z-][0-9A-Za-z-]*)'
VERSION = re.compile(r'(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)'
                     rf'(?:-{PRERELEASE_ID}(?:\.{PRERELEASE_ID})*)?\Z')
PRIVATE = {'.git', '.env', '__pycache__', 'bin', 'obj', 'tests', 'node_modules'}
BINARY = {'.dll', '.exe', '.pdb', '.so', '.dylib'}
EXECUTABLE_MAGIC = (b'MZ', b'\x7fELF') + tuple(bytes.fromhex(magic) for magic in (
    'feedface', 'cefaedfe', 'feedfacf', 'cffaedfe',  # Mach-O, 32/64-bit, both byte orders
    'cafebabe', 'bebafeca', 'cafebabf', 'bfbafeca',  # universal, 32/64-bit, both byte orders
))
# CAFEBABE also identifies Java class files, which are likewise unowned executable
# payloads. Match headers only: arbitrary image bytes may contain these sequences.
SECRET_ASSIGNMENT = re.compile(
    rb'(?im)^[ \t]*(?:export[ \t]+)?[A-Z0-9_]*(?:TOKEN|PASSWORD|SECRET|API_KEY|ACCESS_KEY)[A-Z0-9_]*[ \t]*=')


def load_json(path):
    def finite_float(value):
        result = float(value)
        if not math.isfinite(result):
            raise ValueError(f'non-finite JSON number: {value}')
        return result

    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                raise ValueError(f'duplicate JSON key {key}: {path}')
            result[key] = value
        return result
    try:
        return json.loads(path.read_text(encoding='utf-8-sig'), object_pairs_hook=pairs,
                          parse_float=finite_float,
                          parse_constant=lambda value: (_ for _ in ()).throw(ValueError(value)))
    except (ValueError, UnicodeError) as exc:
        raise ValueError(f'invalid JSON {path}: {exc}') from exc


def safe_path(path):
    if path.is_symlink():
        raise ValueError(f'symlink not allowed: {path}')


def discover(root):
    folders = [root / 'questline']
    for group in ('content', 'compat'):
        parent = root / group
        safe_path(parent)
        if parent.exists():
            for folder in sorted(parent.iterdir()):
                safe_path(folder)
                if folder.is_dir():
                    folders.append(folder)
    mods = []
    ids = set()
    for folder in folders:
        safe_path(folder)
        manifest = folder / 'modinfo.json'
        safe_path(manifest)
        if not manifest.is_file():
            raise ValueError(f'missing modinfo.json: {folder}')
        info = load_json(manifest)
        if not isinstance(info, dict):
            raise ValueError(f'manifest must be an object: {folder}')
        modid, version = info.get('modid', ''), info.get('version', '')
        if not isinstance(modid, str) or not MODID.fullmatch(modid):
            raise ValueError(f'invalid modid: {folder}')
        if not isinstance(version, str) or not VERSION.fullmatch(version):
            raise ValueError(f'invalid version: {folder}')
        if modid in ids:
            raise ValueError(f'duplicate modid: {modid}')
        ids.add(modid)
        expected = 'content' if folder.parent.name == 'content' else 'code'
        if not isinstance(info.get('type'), str) or info['type'].lower() != expected:
            raise ValueError(f'{folder} must have type {expected}')
        if folder == root / 'questline' and modid != 'questline':
            raise ValueError('framework identity must be questline')
        deps = info.get('dependencies')
        if not isinstance(deps, dict) or not deps:
            raise ValueError(f'missing dependencies: {modid}')
        for dep, minimum in deps.items():
            if not MODID.fullmatch(dep) or not isinstance(minimum, str) or (minimum != '' and not VERSION.fullmatch(minimum)):
                raise ValueError(f'invalid dependency {dep}: {modid}')
            if dep == modid:
                raise ValueError(f'self dependency: {modid}')
        if modid != 'questline' and 'questline' not in deps:
            raise ValueError(f'{modid} must depend on questline')
        if expected == 'code':
            projects = list(folder.glob('*.csproj'))
            if len(projects) != 1:
                raise ValueError(f'expected one code project: {folder}')
            safe_path(projects[0])
        mods.append((folder, info))
    versions = {info['modid']: info['version'] for _, info in mods}
    for _, info in mods:
        for dep, minimum in info['dependencies'].items():
            if dep in versions and minimum:
                # Vintage Story dependencies are minimum versions, not exact pins.
                def key(v):
                    main, _, pre = v.partition('-')
                    prerelease = tuple((0, int(part)) if part.isdigit() else (1, part)
                                       for part in pre.split('.')) if pre else ()
                    return tuple(map(int, main.split('.'))) + (not bool(pre), prerelease)
                if key(versions[dep]) < key(minimum):
                    raise ValueError(f'unsatisfied internal dependency {dep}: {info["modid"]}')
    return mods


def payload(folder, info, license_path, assemblies):
    entries = {}
    folded = set()

    def add(name, source, assembly=False):
        safe_path(source)
        parts = name.split('/')
        if (name.startswith('/') or any(p in ('', '.', '..') or p.lower() in PRIVATE
                                       or p.lower().startswith('.env.') for p in parts)
                or '\\' in name or ':' in name or any(ord(c) < 32 for c in name)):
            raise ValueError(f'unsafe/private archive name: {name}')
        if name.casefold() in folded:
            raise ValueError(f'archive name collision: {name}')
        if not source.is_file():
            raise ValueError(f'missing payload: {source}')
        data = source.read_bytes()
        if not assembly:
            if source.suffix.lower() in BINARY or data.startswith(EXECUTABLE_MAGIC):
                raise ValueError(f'unowned executable payload: {source}')
            if (b'PRIVATE KEY-----' in data or SECRET_ASSIGNMENT.search(data.removeprefix(b'\xef\xbb\xbf'))
                    or re.search(rb'/(?:home|Users)/[A-Za-z0-9_.-]+/', data)):
                raise ValueError(f'private material in payload: {source}')
            if source.suffix.lower() == '.json':
                load_json(source)
        folded.add(name.casefold())
        entries[name] = data

    add('LICENSE', license_path)
    add('modinfo.json', folder / 'modinfo.json')
    icon = folder / 'modicon.png'
    if icon.exists() or icon.is_symlink():
        add('modicon.png', icon)
    assets = folder / 'assets'
    safe_path(assets)
    if assets.exists():
        for path in sorted(assets.rglob('*')):
            safe_path(path)
            if path.is_file():
                add(path.relative_to(folder).as_posix(), path)
    if info['type'].lower() == 'code':
        assembly = assemblies.get(info['modid'])
        if assembly is None:
            raise ValueError(f'missing assembly for {info["modid"]}')
        project = next(folder.glob('*.csproj'))
        try:
            project_xml = ET.parse(project)
            declared_names = [element.text.strip() for element in project_xml.iter()
                              if element.tag.rsplit('}', 1)[-1] == 'AssemblyName' and element.text]
        except ET.ParseError as exc:
            raise ValueError(f'invalid project XML: {project}') from exc
        allowed_names = {name + '.dll' for name in declared_names} or {project.stem + '.dll'}
        if assembly.name not in allowed_names:
            raise ValueError(f'expected owned assembly {sorted(allowed_names)}, got {assembly.name}')
        add(assembly.name, assembly, assembly=True)
    return entries


def atomic_bytes(path, data):
    fd, temporary = tempfile.mkstemp(prefix='.' + path.name, dir=path.parent)
    try:
        with os.fdopen(fd, 'wb') as stream:
            stream.write(data)
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def package_repo(root, output, assemblies):
    root, output = Path(root), Path(output)
    # Validate every mod before creating/replacing any output.
    planned = []
    for folder, info in discover(root):
        planned.append((f'{info["modid"]}_{info["version"]}.zip',
                        payload(folder, info, root / 'LICENSE', assemblies)))
    safe_path(output)
    output.mkdir(parents=True, exist_ok=True)
    artifacts = []
    for name, entries in planned:
        target = output / name
        fd, temporary = tempfile.mkstemp(prefix='.' + name, dir=output)
        os.close(fd)
        try:
            with zipfile.ZipFile(temporary, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
                for entry, data in sorted(entries.items()):
                    meta = zipfile.ZipInfo(entry, (1980, 1, 1, 0, 0, 0))
                    meta.create_system = 3
                    meta.external_attr = 0o100644 << 16
                    meta.compress_type = zipfile.ZIP_DEFLATED
                    archive.writestr(meta, data, compresslevel=9)
            with zipfile.ZipFile(temporary) as archive:
                if archive.namelist() != sorted(entries) or archive.testzip() is not None:
                    raise ValueError(f'archive membership/CRC verification failed: {name}')
                for entry, data in entries.items():
                    if archive.read(entry) != data:
                        raise ValueError(f'archive byte verification failed: {entry}')
            os.replace(temporary, target)
            artifacts.append(target)
        finally:
            if os.path.exists(temporary):
                os.unlink(temporary)
    checksums = ''.join(f'{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.name}\n' for p in sorted(artifacts))
    atomic_bytes(output / 'SHA256SUMS', checksums.encode('ascii'))
    return artifacts


def build(root, mods, configuration, dotnet):
    game = os.environ.get('VINTAGE_STORY')
    if not game:
        raise ValueError('set VINTAGE_STORY to the external game SDK directory')
    required = ('VintagestoryAPI.dll', 'Mods/VSSurvivalMod.dll', 'Mods/VSEssentials.dll',
                'Lib/0Harmony.dll', 'Lib/Newtonsoft.Json.dll', 'Lib/protobuf-net.dll', 'Lib/cairo-sharp.dll')
    for relative in required:
        if not (Path(game) / relative).is_file():
            raise ValueError(f'missing external SDK assembly: {relative}')
    assemblies = {}
    # Core is always first; compat projects use their own actual ProjectReference/HintPath.
    for folder, info in mods:
        if info['type'].lower() != 'code':
            continue
        project = next(folder.glob('*.csproj'))
        subprocess.run([dotnet, 'build', str(project), '-c', configuration, '--nologo',
                        '-p:Deterministic=true', '-p:ContinuousIntegrationBuild=true'], cwd=root, check=True)
        result = subprocess.run([dotnet, 'msbuild', str(project), '-nologo',
                                 f'-p:Configuration={configuration}', '-getProperty:TargetPath'],
                                cwd=root, check=True, text=True, capture_output=True)
        assembly = Path(result.stdout.strip())
        if not assembly.is_absolute():
            assembly = folder / assembly
        if assembly.suffix.lower() != '.dll' or not assembly.is_file():
            raise ValueError(f'build did not produce owned assembly: {assembly}')
        assemblies[info['modid']] = assembly
    return assemblies


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument('--output', type=Path)
    parser.add_argument('--configuration', choices=('Release', 'Debug'), default='Release')
    parser.add_argument('--dotnet', default=os.environ.get('DOTNET', 'dotnet'))
    parser.add_argument('--package-only', action='store_true', help='skip build; requires explicit code assemblies')
    parser.add_argument('--assembly', action='append', default=[], metavar='MODID=PATH')
    args = parser.parse_args()
    root = args.root.resolve()
    try:
        mods = discover(root)
        assemblies = {}
        if args.package_only:
            for assignment in args.assembly:
                modid, separator, path = assignment.partition('=')
                if not separator or modid in assemblies:
                    raise ValueError('use one --assembly MODID=PATH per code mod')
                assemblies[modid] = Path(path).resolve()
            code_ids = {info['modid'] for _, info in mods if info['type'].lower() == 'code'}
            if set(assemblies) != code_ids:
                raise ValueError(f'assembly membership must equal code mods: {sorted(code_ids)}')
        else:
            if args.assembly:
                raise ValueError('--assembly requires --package-only')
            assemblies = build(root, mods, args.configuration, args.dotnet)
        for artifact in package_repo(root, args.output or root / 'Releases', assemblies):
            print(artifact)
        return 0
    except (ValueError, OSError, subprocess.CalledProcessError) as exc:
        parser.exit(1, f'packaging failed: {exc}\n')


if __name__ == '__main__':
    raise SystemExit(main())
