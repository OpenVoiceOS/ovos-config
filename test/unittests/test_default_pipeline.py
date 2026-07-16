import unittest
from os.path import dirname, join

from ovos_utils.json_helper import load_commented_json

DEFAULT_CONFIG = join(dirname(dirname(dirname(__file__))),
                      "ovos_config", "mycroft.conf")


class TestDefaultPipeline(unittest.TestCase):
    """Validate the intent pipeline shipped in the default mycroft.conf"""

    @classmethod
    def setUpClass(cls):
        config = load_commented_json(DEFAULT_CONFIG)
        cls.pipeline = config["intents"]["pipeline"]

    def test_padacioso_entries_present(self):
        # padacioso ships with ovos-core itself, so the default pipeline must
        # include it or a bare install matches no intents at all
        self.assertIn("ovos-padacioso-pipeline-plugin-high", self.pipeline)
        self.assertIn("ovos-padacioso-pipeline-plugin-medium", self.pipeline)

    def test_padacioso_high_after_padatious_high(self):
        # padatious is the preferred matcher when installed; padacioso acts as
        # its fallback within the same confidence tier
        self.assertLess(
            self.pipeline.index("ovos-padatious-pipeline-plugin-high"),
            self.pipeline.index("ovos-padacioso-pipeline-plugin-high"))

    def test_padacioso_medium_in_medium_tier(self):
        # the medium entry must come after all high-confidence matchers and
        # after the medium-tier adapt matcher, but before the medium fallback
        medium = self.pipeline.index("ovos-padacioso-pipeline-plugin-medium")
        self.assertGreater(
            medium, self.pipeline.index("ovos-padacioso-pipeline-plugin-high"))
        self.assertGreater(
            medium, self.pipeline.index("ovos-adapt-pipeline-plugin-medium"))
        self.assertLess(
            medium, self.pipeline.index("ovos-fallback-pipeline-plugin-medium"))


if __name__ == "__main__":
    unittest.main()
