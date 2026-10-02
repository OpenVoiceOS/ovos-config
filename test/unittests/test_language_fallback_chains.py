import json
import re
import unittest
from collections import Counter
from os.path import dirname, join

from ovos_utils.json_helper import load_commented_json

CONF = join(dirname(dirname(dirname(__file__))), "ovos_config", "mycroft.conf")

# Every plugin name the `language` section may name, under the distribution that
# publishes it. A plugin is an entry point, not a distribution: each name below
# is declared in the `opm.lang.detect`, `opm.lang.translate` or legacy
# `neon.plugin.lang.detect` group of a published package, and most of them are
# not PyPI project names at all. A change to a chain needs this set changed too.
PUBLISHED_PLUGINS = {
    # ovos-translate-server-plugin
    "ovos-lang-detector-plugin-server",
    "ovos-translate-plugin-server",
    # ovos-google-translate-plugin
    "ovos-google-lang-detector-plugin",
    "ovos-google-translate-plugin",
    # ovos-lang-detector-classics-plugin
    "ovos-lang-detector-plugin-cld3",
    "ovos-lang-detector-plugin-cld2",
    "ovos-lang-detector-plugin-langdetect",
    "ovos-lang-detector-plugin-fastlang",
    "ovos-lang-detector-plugin-voter",
    # ovos-lang-detector-fasttext-plugin
    "ovos-lang-detector-fasttext-plugin",
    # ovos-classifiers
    "ovos-lang-detect-ngram-lm",
    # lingua-podre
    "ovos-lang-detector-plugin-lingua-podre",
}

DETECTOR_CHAIN = [
    "ovos-lang-detector-plugin-server",
    "ovos-google-lang-detector-plugin",
    "ovos-lang-detector-plugin-cld3",
    "ovos-lang-detector-plugin-cld2",
    "ovos-lang-detector-plugin-langdetect",
    "ovos-lang-detector-plugin-fastlang",
    "ovos-lang-detect-ngram-lm",
]
TRANSLATOR_CHAIN = [
    "ovos-translate-plugin-server",
    "ovos-google-translate-plugin",
]


class TestLanguageFallbackChains(unittest.TestCase):
    """The `language` chains, as a reader traces them and as a loader reads them.

    A factory reads `fallback_module` out of the block of the module it failed
    to build, then tries that module instead. A name that no distribution
    publishes can never load, so it only makes the walk longer and the failure
    harder to read. A block written twice under one JSON name loses its first
    copy without a word, so the file then says one thing and means another.
    """

    def setUp(self):
        self.language = load_commented_json(CONF)["language"]

    def _chain(self, first):
        """Walk `fallback_module` from `first`, stopping on a repeat."""
        chain = []
        module = first
        while module and module not in chain:
            chain.append(module)
            module = (self.language.get(module) or {}).get("fallback_module")
        return chain

    def test_the_detector_chain_is_the_one_written(self):
        self.assertEqual(self._chain(self.language["detection_module"]),
                         DETECTOR_CHAIN)

    def test_the_translator_chain_is_the_one_written(self):
        self.assertEqual(self._chain(self.language["translation_module"]),
                         TRANSLATOR_CHAIN)

    def test_every_module_of_a_chain_is_published(self):
        for first in (self.language["detection_module"],
                      self.language["translation_module"]):
            for module in self._chain(first):
                self.assertIn(module, PUBLISHED_PLUGINS,
                              f"no published distribution declares {module}")

    def test_no_key_of_the_language_section_is_written_twice(self):
        """Keep the pairs the loader collapses, and count the names."""
        with open(CONF) as f:
            text = re.sub(r"^\s*//.*$", "", f.read(), flags=re.MULTILINE)
        pairs = dict(json.loads(text, object_pairs_hook=lambda p: p))
        names = Counter(name for name, _ in pairs["language"])
        self.assertEqual([name for name, count in names.items() if count > 1],
                         [])
