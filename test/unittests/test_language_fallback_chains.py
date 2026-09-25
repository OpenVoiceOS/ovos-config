import json
import re
import unittest
from collections import Counter
from os.path import dirname, join

from ovos_utils.json_helper import load_commented_json

ROOT = join(dirname(dirname(dirname(__file__))), "ovos_config")
CONF = join(ROOT, "mycroft.conf")

# Every plugin name the `language` chains may name, with the distribution that
# publishes the entry point. A plugin is an entry point, not a distribution: a
# name here is checked against what some published package declares in the
# `opm.lang.detect` / `opm.lang.translate` group, never against a PyPI project
# of the same name.
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
    # ovos-classifiers. Declared under the legacy `neon.plugin.lang.detect`
    # group, which OPM maps to `opm.lang.detect`
    # (ovos_plugin_manager/utils/__init__.py), so it loads like any other.
    "ovos-lang-detect-ngram-lm",
}


class TestLanguageFallbackChains(unittest.TestCase):
    """The `language` fallback chains must name plugins that exist.

    A factory walks `fallback_module` from one link to the next. A link whose
    plugin no distribution publishes can never load, so it only makes the walk
    longer and the failure harder to read.
    """

    def setUp(self):
        self.language = load_commented_json(CONF)["language"]

    def _chain(self, first):
        """Walk the chain from `first`, stopping on a repeat."""
        chain = []
        module = first
        while module and module not in chain:
            chain.append(module)
            module = (self.language.get(module) or {}).get("fallback_module")
        return chain

    def test_every_detector_in_the_chain_is_published(self):
        chain = self._chain(self.language["detection_module"])
        self.assertGreater(len(chain), 1)
        for module in chain:
            self.assertIn(module, PUBLISHED_PLUGINS, f"{module} is not published")

    def test_every_translator_in_the_chain_is_published(self):
        chain = self._chain(self.language["translation_module"])
        self.assertGreater(len(chain), 1)
        for module in chain:
            self.assertIn(module, PUBLISHED_PLUGINS, f"{module} is not published")

    def _effective_chain(self, first):
        """Walk the chain the way OPM does, which is not the way it reads.

        `OVOSLangDetectionFactory.create` follows a fallback only when the
        fallback's own name is a key of this block:

            if fallback in config and fallback != lang_module

        (ovos_plugin_manager/language.py). A `fallback_module` naming a plugin
        that has no key here is written but never reached, so the chain a reader
        traces and the chain that runs can differ by a hop.
        """
        chain = []
        module = first
        while module and module not in chain:
            chain.append(module)
            nxt = (self.language.get(module) or {}).get("fallback_module")
            module = nxt if nxt in self.language and nxt != module else None
        return chain

    def test_the_effective_detector_chain_reaches_every_keyed_link(self):
        """The hop this file exists to protect.

        A change that deletes a key deletes the hop INTO it, not only the dead
        tail after it. Removing the `fastlang` key shortened the effective chain
        from `langdetect -> fastlang` to `langdetect` while the written map still
        read as though nothing had changed, and nothing here noticed.
        """
        effective = self._effective_chain(self.language["detection_module"])
        self.assertGreater(len(effective), 1)
        self.assertEqual(effective[-1], "ovos-lang-detector-plugin-fastlang",
                         "the effective chain no longer ends where it did; a "
                         "key was added or removed, which moves a hop")
        for module in effective:
            self.assertIn(module, PUBLISHED_PLUGINS,
                          f"{module} is reached and is not published")

    def test_a_written_fallback_without_a_key_is_never_reached(self):
        """The written chain runs one link past the effective one, on purpose.

        `ovos-lang-detect-ngram-lm` is published and is named as the tail, but it
        has no key of its own, so OPM stops before it. That is the documented
        reason the chain ends, and it is not that the plugin is missing: give it
        a key and the chain extends.
        """
        written = self._chain(self.language["detection_module"])
        effective = self._effective_chain(self.language["detection_module"])
        self.assertIn("ovos-lang-detect-ngram-lm", written)
        self.assertNotIn("ovos-lang-detect-ngram-lm", effective)
        self.assertEqual(written[:len(effective)], effective)
        self.assertNotIn("ovos-lang-detect-ngram-lm", self.language)

    def test_no_duplicate_key_in_the_language_section(self):
        """A repeated JSON key is silently dropped by the parser.

        `load_commented_json` keeps the last value, so a duplicated block reads
        as valid while one of the two chains it describes is dead text.
        """
        text = open(CONF, encoding="utf-8").read()
        text = re.sub(r"^\s*//.*$", "", text, flags=re.M)
        raw = json.loads(text, object_pairs_hook=lambda pairs: pairs)

        def _section(pairs, name):
            for key, value in pairs:
                if key == name:
                    return value
            raise AssertionError(f"no {name} section")

        keys = [key for key, _ in _section(raw, "language")]
        repeats = [key for key, count in Counter(keys).items() if count > 1]
        self.assertEqual(repeats, [])


if __name__ == "__main__":
    unittest.main()
