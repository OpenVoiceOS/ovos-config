import json
import os
import shutil
import subprocess
import sys
import tempfile
from os.path import join
from unittest import TestCase


# ovos_config.__main__ builds a Configuration() singleton (and a file
# watcher) at import time. Running the CLI in a subprocess with its own
# isolated XDG_CONFIG_HOME keeps that singleton out of the test process, so
# it can't race with other test modules that assume they're the first to
# import ovos_config (see test_configuration.py's setUpClass).
_RUN_CLI = """
import sys
from ovos_config.__main__ import config
sys.exit(config.main(sys.argv[1:], standalone_mode=False))
"""


class TestCliConfigTargets(TestCase):
    """Regression tests: CONFIGS used to be indexed by position, which
    silently swapped the Assistant and User configurations once the
    Assistant entry was inserted at index 2 of the list. `show --user` used
    to display the Assistant config, `show --assistant` used to display the
    User config, and `set` wrote every change to the Assistant config file
    instead of the User config file.
    """

    def setUp(self):
        self.test_dir = tempfile.mkdtemp(prefix="ovos-config-cli-test-")
        self.addCleanup(shutil.rmtree, self.test_dir, ignore_errors=True)
        os.makedirs(join(self.test_dir, "mycroft"), exist_ok=True)
        self.user_conf = join(self.test_dir, "mycroft", "mycroft.conf")
        self.assistant_conf = join(self.test_dir, "mycroft", "runtime.conf")
        with open(self.user_conf, "w") as f:
            json.dump({"marker": "user"}, f)
        with open(self.assistant_conf, "w") as f:
            json.dump({"marker": "assistant"}, f)

    def _run(self, *args):
        env = dict(os.environ)
        env["XDG_CONFIG_HOME"] = self.test_dir
        return subprocess.run(
            [sys.executable, "-c", _RUN_CLI, *args],
            env=env, capture_output=True, text=True, timeout=30)

    def test_show_user_uses_user_config(self):
        result = self._run("show", "--user")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("marker", result.stdout)
        self.assertIn("user", result.stdout)
        self.assertNotIn("Configuration: Assistant", result.stdout)

    def test_show_assistant_uses_assistant_config(self):
        result = self._run("show", "--assistant")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("marker", result.stdout)
        self.assertIn("assistant", result.stdout)
        self.assertNotIn("Configuration: User", result.stdout)

    def test_set_writes_user_config_not_assistant(self):
        result = self._run("set", "-k", "marker", "-v", "touched")
        self.assertEqual(result.returncode, 0, result.stderr)

        with open(self.user_conf) as f:
            user_data = json.load(f)
        with open(self.assistant_conf) as f:
            assistant_data = json.load(f)

        self.assertEqual(user_data.get("marker"), "touched")
        self.assertEqual(assistant_data.get("marker"), "assistant")


class TestAutoconfigureOfflineVoices(TestCase):
    """Regression tests: grant-funded phoonnx voices exist for Asturian,
    Aragonese, Occitan and Frisian, but `autoconfigure` had no
    offline_male/offline_female recommendation file for them, so it printed
    "not available" instead of setting up the voice.
    """

    def setUp(self):
        self.test_dir = tempfile.mkdtemp(prefix="ovos-config-cli-test-")
        self.addCleanup(shutil.rmtree, self.test_dir, ignore_errors=True)

    def _run(self, *args):
        env = dict(os.environ)
        env["XDG_CONFIG_HOME"] = self.test_dir
        return subprocess.run(
            [sys.executable, "-c", _RUN_CLI, *args],
            env=env, capture_output=True, text=True, timeout=30)

    def test_ast_es_male_voice_recommended(self):
        result = self._run("autoconfigure", "--lang", "ast-ES", "--offline", "--male")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertNotIn("offline_male not available", result.stdout)
        self.assertIn("OpenVoiceOS/phoonnx_ast_miro_unicode", result.stdout)

    def test_an_es_female_voice_recommended(self):
        result = self._run("autoconfigure", "--lang", "an-ES", "--offline", "--female")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertNotIn("offline_female not available", result.stdout)
        self.assertIn("OpenVoiceOS/phoonnx_an_dii_unicode", result.stdout)

    def test_oc_fr_male_voice_recommended(self):
        result = self._run("autoconfigure", "--lang", "oc-FR", "--offline", "--male")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertNotIn("offline_male not available", result.stdout)
        self.assertIn("OpenVoiceOS/phoonnx_oc_miro_unicode", result.stdout)

    def test_fy_nl_female_voice_recommended(self):
        result = self._run("autoconfigure", "--lang", "fy-NL", "--offline", "--female")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertNotIn("offline_female not available", result.stdout)
        self.assertIn("OpenVoiceOS/phoonnx_fy-NL_dii_unicode", result.stdout)
