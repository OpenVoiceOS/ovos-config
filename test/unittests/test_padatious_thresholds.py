import unittest
from os.path import dirname, join

from ovos_utils.json_helper import load_commented_json

CONF = join(dirname(dirname(dirname(__file__))), "ovos_config", "mycroft.conf")


class TestPadatiousThresholds(unittest.TestCase):
    def test_conf_high_is_hint_identity_boundary(self):
        section = load_commented_json(CONF)["intents"]["ovos-padatious-pipeline-plugin"]
        self.assertEqual(section["conf_high"], 0.9)
        self.assertEqual(section["conf_med"], 0.8)
        self.assertLess(section["conf_med"], section["conf_high"])


if __name__ == "__main__":
    unittest.main()
