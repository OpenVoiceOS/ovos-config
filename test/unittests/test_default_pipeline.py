import glob
import unittest
from os.path import dirname, join

from ovos_utils.json_helper import load_commented_json

ROOT = join(dirname(dirname(dirname(__file__))), "ovos_config")
CONF = join(ROOT, "mycroft.conf")


class TestDefaultPipeline(unittest.TestCase):
    """New installs match intents with model2vec; padatious is opt-in."""

    def setUp(self):
        self.pipeline = load_commented_json(CONF)["intents"]["pipeline"]

    def test_no_padatious_stage(self):
        padatious = [p for p in self.pipeline if "padatious" in p]
        self.assertEqual(padatious, [])

    def test_m2v_high_before_adapt_high(self):
        self.assertLess(self.pipeline.index("ovos-m2v-pipeline-high"),
                        self.pipeline.index("ovos-adapt-pipeline-plugin-high"))

    def test_m2v_medium_before_adapt_medium(self):
        self.assertLess(
            self.pipeline.index("ovos-m2v-pipeline-medium"),
            self.pipeline.index("ovos-adapt-pipeline-plugin-medium"))

    def test_full_order(self):
        self.assertEqual(self.pipeline, [
            "ovos-stop-pipeline-plugin-high",
            "ovos-converse-pipeline-plugin",
            "ovos-ocp-pipeline-plugin-high",
            "ovos-m2v-pipeline-high",
            "ovos-adapt-pipeline-plugin-high",
            "ovos-ocp-pipeline-plugin-medium",
            "ovos-fallback-pipeline-plugin-high",
            "ovos-stop-pipeline-plugin-medium",
            "ovos-m2v-pipeline-medium",
            "ovos-adapt-pipeline-plugin-medium",
            "ovos-fallback-pipeline-plugin-medium",
            "ovos-fallback-pipeline-plugin-low",
        ])


class TestPlatformPipelines(unittest.TestCase):
    """Platform confs replace the whole pipeline list, so each one that
    carries a padatious high stage must carry the medium stage too — the
    open-slot rescue must not vanish on autoconfigured installs."""

    def test_platform_confs_carry_padatious_medium(self):
        for conf in glob.glob(join(ROOT, "recommends", "platform", "*.conf")):
            pipeline = load_commented_json(conf).get(
                "intents", {}).get("pipeline")
            if not pipeline:
                continue
            if "ovos-padatious-pipeline-plugin-high" in pipeline:
                self.assertIn("ovos-padatious-pipeline-plugin-medium",
                              pipeline, conf)
                self.assertLess(
                    pipeline.index("ovos-padatious-pipeline-plugin-high"),
                    pipeline.index("ovos-padatious-pipeline-plugin-medium"),
                    conf)


if __name__ == "__main__":
    unittest.main()
