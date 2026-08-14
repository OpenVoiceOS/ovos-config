"""The memoized config merge.

``load_all_configs`` rebuilds the merged stack on every call, and
``Configuration.__getitem__`` calls it on every key access — ~75us each,
dozens of ``merge_dict`` calls. One ovos-bus-client ``Session`` construction
reads ~13 keys, i.e. ~1 ms of pure re-merging per utterance in every OVOS
process. These tests pin the memo behaviour: a clean memo serves the same
object (identity), and every mutation path (patch/setitem/update, layer
swap, reload, watchdog file change, bus patch messages, clear_cache)
invalidates it (fresh object, fresh values).

NOTE: imports are function-level on purpose — test_locations.py reloads
``ovos_config.config`` mid-suite (``importlib.reload``), so module-level
imports would pin a stale class object.
"""
import unittest
from unittest.mock import patch


def _config_cls():
    from ovos_config.config import Configuration
    return Configuration


class TestMergeCache(unittest.TestCase):
    def setUp(self):
        _config_cls()._invalidate_cache()

    def tearDown(self):
        Configuration = _config_cls()
        Configuration.reset()  # drop any test patches
        Configuration._invalidate_cache()

    def test_repeat_reads_serve_the_memo(self):
        Configuration = _config_cls()
        first = Configuration.load_all_configs()
        for _ in range(10):
            self.assertIs(Configuration.load_all_configs(), first,
                          "clean memo must serve the same object")
        cfg = Configuration()
        cfg["lang"]
        self.assertIs(Configuration.load_all_configs(), first,
                      "getitem reads must not rebuild a clean memo")

    def test_setitem_invalidates_and_wins(self):
        Configuration = _config_cls()
        cfg = Configuration()
        before = Configuration.load_all_configs()
        cfg["unittest_marker"] = "before"
        self.assertIsNot(Configuration.load_all_configs(), before,
                         "__setitem__ must invalidate the memo")
        self.assertEqual(cfg["unittest_marker"], "before")
        cfg["unittest_marker"] = "after"
        self.assertEqual(cfg["unittest_marker"], "after")

    def test_update_invalidates(self):
        Configuration = _config_cls()
        cfg = Configuration()
        before = Configuration.load_all_configs()
        cfg.update({"unittest_marker2": 1})
        self.assertIsNot(Configuration.load_all_configs(), before)
        self.assertEqual(Configuration()["unittest_marker2"], 1)

    def test_patch_message_invalidates(self):
        Configuration = _config_cls()
        cfg = Configuration()
        before = Configuration.load_all_configs()

        class Msg:
            data = {"config": {"unittest_marker3": 42}}

        Configuration.patch(Msg())
        self.assertIsNot(Configuration.load_all_configs(), before)
        self.assertEqual(cfg["unittest_marker3"], 42)

    def test_patch_clear_invalidates(self):
        Configuration = _config_cls()
        cfg = Configuration()
        cfg["unittest_marker4"] = "x"
        self.assertEqual(cfg["unittest_marker4"], "x")
        before = Configuration.load_all_configs()

        class Msg:
            data = {}

        Configuration.patch_clear(Msg())
        self.assertIsNot(Configuration.load_all_configs(), before)
        self.assertIsNone(Configuration()["unittest_marker4"])

    def test_layer_swap_invalidates(self):
        """Direct class-attribute layer replacement (the test_locations /
        embedder pattern) must invalidate via the metaclass."""
        Configuration = _config_cls()
        before = Configuration.load_all_configs()
        old = Configuration.xdg_configs
        try:
            Configuration.xdg_configs = list(old)
            self.assertIsNot(Configuration.load_all_configs(), before,
                             "layer swap must invalidate the memo")
        finally:
            Configuration.xdg_configs = old

    def test_reload_invalidates(self):
        Configuration = _config_cls()
        before = Configuration.load_all_configs()
        Configuration.reload()
        self.assertIsNot(Configuration.load_all_configs(), before)

    def test_clear_cache_invalidates(self):
        Configuration = _config_cls()
        before = Configuration.load_all_configs()
        Configuration.clear_cache()
        self.assertIsNot(Configuration.load_all_configs(), before)

    def test_file_change_invalidates(self):
        Configuration = _config_cls()
        before = Configuration.load_all_configs()
        # simulate the watchdog reporting a change on a real layer: force the
        # hash comparison to differ so the changed-file branch runs
        layer = Configuration.xdg_configs[-1]
        with patch.object(type(layer), "reload"), \
             patch("ovos_config.config.hash", side_effect=[1, 2], create=True):
            Configuration._on_file_change(layer.path)
        self.assertIsNot(Configuration.load_all_configs(), before,
                         "a changed config file must invalidate the memo")

    def test_unchanged_file_keeps_memo(self):
        Configuration = _config_cls()
        before = Configuration.load_all_configs()
        layer = Configuration.xdg_configs[-1]
        with patch.object(type(layer), "reload"), \
             patch("ovos_config.config.hash", side_effect=[7, 7], create=True):
            Configuration._on_file_change(layer.path)
        self.assertIs(Configuration.load_all_configs(), before,
                      "an unchanged file must not drop the memo")

    def test_custom_constraints_bypass_cache(self):
        Configuration = _config_cls()
        cached = Configuration.load_all_configs()  # prime
        bypass = Configuration.load_all_configs(
            {"disable_user_config": True, "disable_remote_config": True})
        self.assertIsNot(bypass, cached,
                         "constrained loads must not serve the default memo")
        # and must not poison it either
        self.assertIs(Configuration.load_all_configs(), cached)


if __name__ == "__main__":
    unittest.main()
