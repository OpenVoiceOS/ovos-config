import glob
import unittest
from os.path import dirname, join

from ovos_utils.json_helper import load_commented_json

ROOT = join(dirname(dirname(dirname(__file__))), "ovos_config")
CONF = join(ROOT, "mycroft.conf")
M2V_TIERS = ["ovos-m2v-pipeline-high", "ovos-m2v-pipeline-medium",
             "ovos-m2v-pipeline-low"]


def _assert_m2v_default(case, pipeline, where):
    """The m2v tiers are present, in order, and padatious is not listed.

    -high and -medium run the trained model, -low runs prototype mode on the
    loaded skills' templates; padatious stays installable and selectable, so
    a deployment lists its stages itself.
    """
    for tier in M2V_TIERS:
        case.assertIn(tier, pipeline, where)
    case.assertEqual([t for t in pipeline if t in M2V_TIERS], M2V_TIERS, where)
    case.assertFalse([t for t in pipeline if "padatious" in t], where)
    # the medium rescue sits after the high tiers of the other matchers
    case.assertLess(pipeline.index("ovos-adapt-pipeline-plugin-high"),
                    pipeline.index("ovos-m2v-pipeline-medium"), where)


class TestDefaultPipeline(unittest.TestCase):
    def setUp(self):
        self.pipeline = load_commented_json(CONF)["intents"]["pipeline"]

    def test_m2v_is_the_default_matcher(self):
        _assert_m2v_default(self, self.pipeline, CONF)

    def test_m2v_high_leads_adapt_high(self):
        self.assertLess(self.pipeline.index("ovos-m2v-pipeline-high"),
                        self.pipeline.index("ovos-adapt-pipeline-plugin-high"))


class TestPlatformPipelines(unittest.TestCase):
    """Platform confs replace the whole pipeline list, so each one that
    carries a list must carry the same three m2v tiers in order, and must not
    override the plugin's model under the key OPM reads
    (``intents["ovos-m2v-pipeline"]``): the plugin's own default is the
    published model."""

    def test_platform_confs_follow_the_default(self):
        seen = 0
        for conf in glob.glob(join(ROOT, "recommends", "platform", "*.conf")):
            intents = load_commented_json(conf).get("intents", {})
            pipeline = intents.get("pipeline")
            if not pipeline:
                continue
            seen += 1
            _assert_m2v_default(self, pipeline, conf)
            self.assertNotIn("ovos-m2v-pipeline", intents, conf)
        self.assertGreaterEqual(seen, 5)


if __name__ == "__main__":
    unittest.main()
