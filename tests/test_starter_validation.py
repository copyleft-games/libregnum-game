"""Skill schema, recursive resources and engine evidence regressions."""
import hashlib
import importlib.util
from pathlib import Path
import sys
import tempfile
import unittest

TOOLS = Path(__file__).resolve().parents[1] / "tools"
sys.path.insert(0, str(TOOLS))
from starter_validation import bundle_errors, check_links, parse_metadata, section_errors, validate_skill

SPEC = importlib.util.spec_from_file_location("contracts", TOOLS / "check-engine-contracts.py")
contracts = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(contracts)


class MetadataTests(unittest.TestCase):
    def test_supported_strings_and_order(self):
        for scalar in ('Use for game rules.', '"Use for game: rules."', "'Use for game: rules.'", '>\n  Use for\n  game rules.', '|\n  Use for\n  game rules.'):
            text = f'---\ndescription: {scalar}\nname: libregnum-example\n---\n'
            result = parse_metadata(text)
            self.assertEqual(result['name'], 'libregnum-example')
            self.assertIn('Use for', result['description'])

    def test_reject_invalid_frontmatter(self):
        for text in ('\n---\nname: x\n---', '---\nname: x',
                     '---\nname: x\nname: y\ndescription: z\n---',
                     '---\nname: x\ndescription: null\n---',
                     '---\nname: x\ndescription: 123\n---',
                     '---\nname: x\ndescription: [a, b]\n---',
                     '---\nname: x\ndescription: !tag hi\n---',
                     '---\nname: x\ndescription: bad: scalar\n---',
                     '---\nname: x\ndescription: bad:\n---',
                     '---\nname: x\ndescription: - item\n---',
                     '---\nname: x\ndescription: >\n---',
                     '---\nname: x\ndescription: "unterminated\n---'):
            with self.subTest(text=text), self.assertRaises(ValueError):
                parse_metadata(text)

    def test_empty_required_section(self):
        self.assertEqual(section_errors('## Examples\n\n## Constraints\nText', ('Examples',)),
                         ['missing or empty section: Examples'])


class BundleTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        self.folder = self.root / '.agents/skills/libregnum-example'
        self.folder.mkdir(parents=True)
        self.skill = self.folder / 'SKILL.md'
        self.skill.write_text('---\nname: libregnum-example\ndescription: Test rules.\n---\n' +
                             ''.join(f'## {name}\n\nText.\n\n' for name in ('When to Use', 'Prerequisites', 'Instructions', 'Output Format', 'Examples', 'Constraints')) +
                             '**Input:** Test a move.\n**Result:** Move is rejected.\n')

    def test_name_must_match_directory(self):
        self.assertEqual(validate_skill(self.skill), [])
        self.skill.write_text(self.skill.read_text().replace('name: libregnum-example', 'name: skill-example'))
        self.assertTrue(any('libregnum-' in e for e in validate_skill(self.skill)))
        self.assertTrue(any('directory' in e for e in validate_skill(self.skill)))

    def test_concrete_example_markers_required(self):
        self.skill.write_text(self.skill.read_text().replace('**Result:**', 'Outcome'))
        self.assertIn('example must include concrete Input and Result', validate_skill(self.skill))

    def test_recursive_reference_and_orphan(self):
        refs = self.folder / 'references'
        refs.mkdir()
        (refs / 'first.md').write_text('[Second](second.md)')
        (refs / 'second.md').write_text('Details')
        self.skill.write_text(self.skill.read_text() + '[Read](references/first.md)')
        self.assertEqual(bundle_errors(self.folder), [])
        (refs / 'unused.md').write_text('Unused')
        self.assertEqual(bundle_errors(self.folder), ['unlinked bundle resource: references/unused.md'])
        (refs / 'second.md').write_text('[Cycle](first.md)')
        self.assertEqual(len(bundle_errors(self.folder)), 1)

    def test_broken_nested_link(self):
        self.skill.write_text(self.skill.read_text() + '[Missing](references/missing.md)')
        errors, skipped = check_links(self.root, self.skill)
        self.assertEqual(skipped, 0)
        self.assertTrue(any('broken' in e for e in errors))

    def test_engine_missing_is_explicit_skip(self):
        self.skill.write_text(self.skill.read_text() + '[Engine](../../../deps/libregnum/src/example.h)')
        self.assertEqual(check_links(self.root, self.skill), ([], 1))
        engine = self.root / 'engine'
        engine.mkdir()
        self.assertTrue(check_links(self.root, self.skill, engine)[0])
        (engine / 'src').mkdir()
        (engine / 'src/example.h').write_text('header')
        self.assertEqual(check_links(self.root, self.skill, engine), ([], 0))

    def test_source_drift_fails_even_if_symbol_survives(self):
        engine = self.root / 'engine'
        engine.mkdir()
        data = b'void example(void);'
        (engine / 'example.h').write_bytes(data)
        refs = self.folder / 'references'
        refs.mkdir()
        (refs / 'engine-recipe.md').write_text('Recipe')
        manifest = {'version': 1, 'records': [{'skill': 'libregnum-example', 'path': 'example.h',
                    'symbols': ['example'], 'sha256': hashlib.sha256(data).hexdigest()}]}
        self.assertEqual(contracts.validate_records(self.root, engine, manifest), [])
        (engine / 'example.h').write_bytes(data + b' /* changed semantics */')
        self.assertTrue(any('source changed' in e for e in contracts.validate_records(self.root, engine, manifest)))
        manifest['records'][0]['path'] = '../escape'
        self.assertTrue(any('unsafe' in e for e in contracts.validate_records(self.root, engine, manifest)))


if __name__ == '__main__':
    unittest.main()
