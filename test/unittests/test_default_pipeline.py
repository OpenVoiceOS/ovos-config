import glob
import unittest
from os.path import dirname, join

from ovos_utils.json_helper import load_commented_json

ROOT = join(dirname(dirname(dirname(__file__))), "ovos_config")
CONF = join(ROOT, "mycroft.conf")


class TestDefaultPipeline(unittest.TestCase):
    def setUp(self):
        self.pipeline = load_commented_json(CONF)["intents"]["pipeline"]

    def test_padatious_medium_present(self):
        self.assertIn("ovos-padatious-pipeline-plugin-medium", self.pipeline)

    def test_padatious_medium_after_high(self):
        self.assertLess(
            self.pipeline.index("ovos-padatious-pipeline-plugin-high"),
            self.pipeline.index("ovos-padatious-pipeline-plugin-medium"))


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
