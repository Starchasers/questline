"""Standard-library package contract tests; DLL fixtures are synthetic, not game tests."""
import hashlib
import importlib.util
import json
import tempfile
import unittest
import zipfile
from pathlib import Path

spec = importlib.util.spec_from_file_location('packager', Path(__file__).with_name('package.py'))
assert spec is not None and spec.loader is not None
packager = importlib.util.module_from_spec(spec)
spec.loader.exec_module(packager)


class PackagingTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / 'LICENSE').write_text('MIT License\nCopyright upstream\n')
        self.core = self.mod('questline', 'questline', 'code', {'game': '1.22.0'})
        self.dll = self.root / 'compiled/questline.dll'
        self.dll.parent.mkdir()
        self.dll.write_bytes(b'MZ synthetic assembly fixture')
        self.assemblies = {'questline': self.dll}
        self.out = self.root / 'Releases'

    def mod(self, folder, modid, kind='content', dependencies=None):
        path = self.root / folder
        path.mkdir(parents=True)
        (path / 'modinfo.json').write_text(json.dumps(dict(type=kind, modid=modid,
            name=modid, version='1.0.0', dependencies=dependencies or {'questline': '1.0.0'})))
        if kind == 'code':
            (path / (path.name + '.csproj')).write_text('<Project Sdk="Microsoft.NET.Sdk"/>')
        assets = path / 'assets/legacy/questline/chapters'
        assets.mkdir(parents=True)
        (assets / 'chapter.json').write_text('{"id":"legacy:chapter"}')
        return path

    def run_package(self):
        return packager.package_repo(self.root, self.out, self.assemblies)

    def test_discovery_determinism_membership_license_checksums_and_preservation(self):
        self.mod('content/vanilla', 'questlinevanilla')
        compat = self.mod('compat/toolsmith', 'questlinetoolsmith', 'code')
        self.assemblies['questlinetoolsmith'] = self.dll.with_name('toolsmith.dll')
        self.assemblies['questlinetoolsmith'].write_bytes(b'MZ synthetic compat fixture')
        (self.core / 'bin').mkdir()
        (self.core / 'bin/VintagestoryAPI.dll').write_bytes(b'game')
        (self.core / 'secrets.txt').write_text('excluded')
        self.out.mkdir()
        (self.out / 'unrelated.zip').write_bytes(b'keep')
        paths = self.run_package()
        self.assertEqual(len(paths), 3)
        before = {p.name: p.read_bytes() for p in paths}
        self.assertEqual(before, {p.name: p.read_bytes() for p in self.run_package()})
        self.assertEqual((self.out / 'unrelated.zip').read_bytes(), b'keep')
        for p in paths:
            with zipfile.ZipFile(p) as z:
                names = z.namelist()
                self.assertEqual(names, sorted(names))
                self.assertIn('LICENSE', names)
                self.assertIn('assets/legacy/questline/chapters/chapter.json', names)
                self.assertNotIn('secrets.txt', names)
                self.assertFalse(any('Vintagestory' in n or '/bin/' in n for n in names))
                self.assertEqual(len([n for n in names if n.endswith('.dll')]), 0 if 'vanilla' in p.name else 1)
                self.assertTrue(all(i.date_time == (1980, 1, 1, 0, 0, 0) for i in z.infolist()))
            self.assertIn(hashlib.sha256(p.read_bytes()).hexdigest() + '  ' + p.name,
                          (self.out / 'SHA256SUMS').read_text())

    def test_repository_inventory_excludes_removed_integrations(self):
        root = Path(__file__).resolve().parents[2]
        expected = {'questline', 'questlinetoolsmith'} | {
            'questline' + key for key in ('vanilla', 'bricklayers', 'butchering', 'efchefstricks',
                'efmealsmodule', 'expandedfoods', 'fromgoldencombs', 'hexsmech',
                'tailorsdelight', 'wool')}
        assemblies = {}
        for modid in ('questline', 'questlinetoolsmith'):
            dll = self.root / (modid + '.dll')
            dll.write_bytes(b'MZ synthetic repository inventory fixture')
            assemblies[modid] = dll
        paths = packager.package_repo(root, self.out, assemblies)
        self.assertEqual(12, len(paths))
        actual = set()
        for path in paths:
            with zipfile.ZipFile(path) as archive:
                info = json.loads(archive.read('modinfo.json'))
                actual.add(info['modid'])
                self.assertIsNone(archive.testzip())
        self.assertEqual(expected, actual)
        self.assertEqual(12, len((self.out / 'SHA256SUMS').read_text().splitlines()))

    def test_content_requires_framework(self):
        self.mod('content/bad', 'bad', dependencies={'game': '1.22.0'})
        with self.assertRaisesRegex(ValueError, 'questline'):
            self.run_package()

    def test_duplicate_modid_rejected(self):
        self.mod('content/duplicate', 'questline')
        with self.assertRaisesRegex(ValueError, 'duplicate'):
            self.run_package()

    def test_missing_assembly_rejected(self):
        self.assemblies.clear()
        with self.assertRaisesRegex(ValueError, 'assembly'):
            self.run_package()

    def test_unsafe_version_rejected(self):
        data = json.loads((self.core / 'modinfo.json').read_text())
        data['version'] = '../escape'
        (self.core / 'modinfo.json').write_text(json.dumps(data))
        with self.assertRaises(ValueError):
            self.run_package()

    def test_invalid_dependency_version_rejected(self):
        self.mod('content/bad', 'bad', dependencies={'questline': '../../evil'})
        with self.assertRaises(ValueError):
            self.run_package()

    def test_unsatisfied_internal_dependency_rejected(self):
        self.mod('content/bad', 'bad', dependencies={'questline': '99.0.0'})
        with self.assertRaisesRegex(ValueError, 'dependency'):
            self.run_package()

    def test_symlink_rejected(self):
        (self.core / 'assets/link').symlink_to(self.dll)
        with self.assertRaisesRegex(ValueError, 'symlink'):
            self.run_package()

    def test_disguised_executable_rejected(self):
        (self.core / 'assets/surprise.png').write_bytes(b'MZnot an image')
        with self.assertRaisesRegex(ValueError, 'executable'):
            self.run_package()

    def test_private_asset_directory_rejected(self):
        (self.core / 'assets/.git').mkdir()
        (self.core / 'assets/.git/config').write_text('private')
        with self.assertRaises(ValueError):
            self.run_package()

    def test_case_colliding_entries_rejected(self):
        (self.core / 'assets/A.png').write_bytes(b'one')
        (self.core / 'assets/a.png').write_bytes(b'two')
        with self.assertRaisesRegex(ValueError, 'collision'):
            self.run_package()

    def test_malformed_asset_json_rejected_before_output(self):
        (self.core / 'assets/bad.json').write_text('{')
        with self.assertRaises(ValueError):
            self.run_package()
        self.assertFalse(self.out.exists())

    def test_undeclared_content_directory_rejected(self):
        (self.root / 'content/unpackaged').mkdir(parents=True)
        with self.assertRaisesRegex(ValueError, 'modinfo'):
            self.run_package()

    def test_utf8_bom_secret_assignment_rejected(self):
        (self.core / 'assets/settings.txt').write_bytes(b'\xef\xbb\xbfAPI_TOKEN=private-value\n')
        with self.assertRaisesRegex(ValueError, 'private'):
            self.run_package()

    def test_secret_material_rejected(self):
        (self.core / 'assets/key.txt').write_text('-----BEGIN PRIVATE KEY-----')
        with self.assertRaisesRegex(ValueError, 'private'):
            self.run_package()

    def test_empty_external_dependency_supported(self):
        self.mod('content/optional', 'optional', dependencies={'questline': '1.0.0', 'external': ''})
        self.assertEqual(len(self.run_package()), 2)

    def test_prerelease_dependency_order(self):
        self.mod('content/optional', 'optional', dependencies={'questline': '1.0.0-rc.2'})
        data = json.loads((self.core / 'modinfo.json').read_text())
        data['version'] = '1.0.0-rc.10'
        (self.core / 'modinfo.json').write_text(json.dumps(data))
        self.assertEqual(len(self.run_package()), 2)

    def test_duplicate_manifest_keys(self):
        (self.core / 'modinfo.json').write_text('{"modid":"questline","modid":"other"}')
        with self.assertRaisesRegex(ValueError, 'duplicate'):
            self.run_package()

    def test_wrong_manifest_type(self):
        data = json.loads((self.core / 'modinfo.json').read_text())
        data['type'] = 123
        (self.core / 'modinfo.json').write_text(json.dumps(data))
        with self.assertRaises(ValueError):
            self.run_package()

    def test_control_character_archive_name(self):
        (self.core / 'assets/bad\nname.txt').write_text('bad')
        with self.assertRaisesRegex(ValueError, 'unsafe'):
            self.run_package()

    def test_missing_license_rejected(self):
        (self.root / 'LICENSE').unlink()
        with self.assertRaisesRegex(ValueError, 'payload'):
            self.run_package()

    def test_output_symlink_rejected(self):
        other = self.root / 'other'
        other.mkdir()
        self.out.symlink_to(other, target_is_directory=True)
        with self.assertRaisesRegex(ValueError, 'symlink'):
            self.run_package()

    def test_archive_permissions(self):
        for path in self.run_package():
            with zipfile.ZipFile(path) as archive:
                self.assertTrue(all(i.external_attr >> 16 == 0o100644 for i in archive.infolist()))

    def test_unowned_assembly_override_rejected(self):
        game = self.dll.with_name('VintagestoryAPI.dll')
        game.write_bytes(b'MZ synthetic game fixture')
        self.assemblies['questline'] = game
        with self.assertRaisesRegex(ValueError, 'owned assembly'):
            self.run_package()

    def test_dotenv_family_rejected_before_output(self):
        for name in ('.env', '.env.local', '.env.production', '.ENV.Production.local'):
            for directory in (False, True):
                with self.subTest(name=name, directory=directory):
                    self.out = self.out.with_name(self.out.name + '-next')
                    path = self.core / 'assets' / name
                    if directory:
                        path.mkdir()
                        target = path / 'settings.txt'
                    else:
                        target = path
                    target.write_text('COLOR=blue\n')
                    try:
                        with self.assertRaisesRegex(ValueError, 'unsafe/private'):
                            self.run_package()
                        self.assertFalse(self.out.exists())
                    finally:
                        target.unlink()
                        if directory:
                            path.rmdir()

    def test_dotenv_secret_assignments_rejected_under_ordinary_names(self):
        path = self.core / 'assets/settings.txt'
        for line in ('TOKEN=private-value', 'export API_TOKEN="private-value"',
                     '  api_key = private-value', 'DB_PASSWORD=private-value',
                     'CLIENT_SECRET=private-value', 'AWS_ACCESS_KEY_ID=private-value'):
            with self.subTest(line=line):
                self.out = self.out.with_name(self.out.name + '-next')
                path.write_text('# settings\n' + line + '\n')
                with self.assertRaisesRegex(ValueError, 'private'):
                    self.run_package()
                self.assertFalse(self.out.exists())

    def test_macho_and_universal_signatures_rejected(self):
        path = self.core / 'assets/disguised.png'
        for magic in ('feedface', 'cefaedfe', 'feedfacf', 'cffaedfe',
                      'cafebabe', 'bebafeca', 'cafebabf', 'bfbafeca'):
            with self.subTest(magic=magic):
                self.out = self.out.with_name(self.out.name + '-next')
                path.write_bytes(bytes.fromhex(magic) + bytes(64))
                with self.assertRaisesRegex(ValueError, 'executable'):
                    self.run_package()
                self.assertFalse(self.out.exists())

    def test_safe_assets_not_confused_with_executable_or_secrets(self):
        assets = self.core / 'assets'
        # Embedded signatures are image content, not executable file headers.
        (assets / 'image.png').write_bytes(b'\x89PNG\r\n\x1a\n' + bytes.fromhex('cffaedfecafebabe'))
        # JPEG's FFD8 header is not little-endian Mach-O's CEFA header.
        (assets / 'image.jpg').write_bytes(bytes.fromhex('ffd8ffe000104a46494600'))
        (assets / '.environment.txt').write_text('COLOR=blue\n')
        (assets / 'help.txt').write_text('Use TOKEN=value in your local environment.\n# TOKEN=example\n')
        (assets / 'game.json').write_text('{"token":"gameplay-item","amount":1e308}')
        self.assertEqual(len(self.run_package()), 1)

    def test_floating_json_overflow_rejected_before_output(self):
        for target in (self.core / 'modinfo.json', self.core / 'assets/overflow.json'):
            original = target.read_bytes() if target.exists() else None
            for number in ('1e999', '-1e999', 'NaN', 'Infinity', '-Infinity'):
                with self.subTest(target=target.name, number=number):
                    self.out = self.out.with_name(self.out.name + '-next')
                    data = json.loads((self.core / 'modinfo.json').read_text()) if target.name == 'modinfo.json' else {}
                    data['nested'] = [{'value': 'OVERFLOW'}]
                    target.write_text(json.dumps(data).replace('"OVERFLOW"', number))
                    try:
                        with self.assertRaisesRegex(ValueError, 'invalid JSON'):
                            self.run_package()
                        self.assertFalse(self.out.exists())
                    finally:
                        if original is not None:
                            target.write_bytes(original)
                        else:
                            target.unlink()

    def test_invalid_semver_prereleases_rejected(self):
        manifest = self.core / 'modinfo.json'
        original = json.loads(manifest.read_text())
        for version in ('1.0.0-.', '1.0.0-rc..1', '1.0.0-01', '1.0.0-rc.01',
                        '1.0.0-.rc', '1.0.0-rc.', '1.0.0-', '01.0.0', '1.0.0-α'):
            for field in ('version', 'dependency'):
                with self.subTest(version=version, field=field):
                    self.out = self.out.with_name(self.out.name + '-next')
                    data = dict(original)
                    if field == 'version':
                        data['version'] = version
                    else:
                        data['dependencies'] = {'game': version}
                    manifest.write_text(json.dumps(data))
                    with self.assertRaisesRegex(ValueError, 'invalid (version|dependency)'):
                        self.run_package()
                    self.assertFalse(self.out.exists())

    def test_valid_semver_prereleases_supported(self):
        manifest = self.core / 'modinfo.json'
        data = json.loads(manifest.read_text())
        for version in ('1.0.0-0', '1.0.0-rc.0', '1.0.0-alpha-beta.1',
                        '1.0.0-01a', '1.0.0--', '1.0.0-RC.123'):
            with self.subTest(version=version):
                data['version'] = version
                data['dependencies'] = {'game': version}
                manifest.write_text(json.dumps(data))
                self.assertEqual(len(self.run_package()), 1)

    def test_content_dll_rejected(self):
        self.mod('content/bad', 'bad')
        (self.root / 'content/bad/assets/stolen.dll').write_bytes(b'fake')
        with self.assertRaises(ValueError):
            self.run_package()


if __name__ == '__main__':
    unittest.main()
