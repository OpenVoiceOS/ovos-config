import unittest
from os.path import dirname, join

from ovos_utils.json_helper import load_commented_json

ROOT = join(dirname(dirname(dirname(__file__))), "ovos_config")
CONF = join(ROOT, "mycroft.conf")


class TestM2VPipelineDefaultModels(unittest.TestCase):
    """`mycroft.conf` ships no active `intents.ovos_m2v_pipeline` config:
    the pipeline's own built-in default (ovos-m2v-pipeline#86) already
    resolves to `OpenVoiceOS/ovos-m2v-intents-multilingual` for every
    language, so there is nothing to configure. This only guards against
    that block coming back with an `en`-model override installed by
    default -- the smaller `OpenVoiceOS/ovos-m2v-intents-en` model ranks
    paraphrases worse in prototype mode and must stay opt-in.
    """

    def setUp(self):
        self.intents = load_commented_json(CONF)["intents"]

    def test_no_active_m2v_pipeline_config_block(self):
        self.assertNotIn("ovos_m2v_pipeline", self.intents)

    def test_config_does_not_default_english_to_the_en_model(self):
        m2v_config = self.intents.get("ovos_m2v_pipeline") or {}
        models = m2v_config.get("models") or {}
        self.assertNotEqual(models.get("en"), "OpenVoiceOS/ovos-m2v-intents-en")

    def test_config_does_not_reference_the_deprecated_jarbas_model(self):
        m2v_config = self.intents.get("ovos_m2v_pipeline") or {}
        self.assertNotIn("Jarbas", str(m2v_config))


if __name__ == "__main__":
    unittest.main()
