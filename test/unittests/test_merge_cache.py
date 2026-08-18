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
        Configuration.load_all_configs()  # prime
        memo = Configuration._merged()
        self.assertIsNotNone(memo)
        for _ in range(10):
            self.assertEqual(Configuration.load_all_configs(), memo)
            self.assertIs(Configuration._merged(), memo,
                          "clean memo must survive repeat reads")
        cfg = Configuration()
        cfg["lang"]
        self.assertIs(Configuration._merged(), memo,
                      "getitem reads must not rebuild a clean memo")

    def test_public_api_returns_a_safe_copy(self):
        Configuration = _config_cls()
        out = Configuration.load_all_configs()
        memo = Configuration._merged()
        self.assertIsNot(out, memo, "public API must not hand out the memo")
        out["poisoned_key"] = True   # caller mutates the returned dict
        self.assertNotIn("poisoned_key", Configuration.load_all_configs(),
                         "caller mutation must not poison the memo")

    def test_setitem_invalidates_and_wins(self):
        Configuration = _config_cls()
        cfg = Configuration()
        Configuration.load_all_configs()
        before = Configuration._merged()
        cfg["unittest_marker"] = "before"
        Configuration.load_all_configs()
        self.assertIsNot(Configuration._merged(), before,
                         "__setitem__ must invalidate the memo")
        self.assertEqual(cfg["unittest_marker"], "before")
        cfg["unittest_marker"] = "after"
        self.assertEqual(cfg["unittest_marker"], "after")

    def test_update_invalidates(self):
        Configuration = _config_cls()
        cfg = Configuration()
        Configuration.load_all_configs()
        before = Configuration._merged()
        cfg.update({"unittest_marker2": 1})
        Configuration.load_all_configs()
        self.assertIsNot(Configuration._merged(), before)
        self.assertEqual(Configuration()["unittest_marker2"], 1)

    def test_patch_message_invalidates(self):
        Configuration = _config_cls()
        cfg = Configuration()
        Configuration.load_all_configs()
        before = Configuration._merged()

        class Msg:
            data = {"config": {"unittest_marker3": 42}}

        Configuration.patch(Msg())
        Configuration.load_all_configs()
        self.assertIsNot(Configuration._merged(), before)
        self.assertEqual(cfg["unittest_marker3"], 42)

    def test_patch_clear_invalidates(self):
        Configuration = _config_cls()
        cfg = Configuration()
        cfg["unittest_marker4"] = "x"
        self.assertEqual(cfg["unittest_marker4"], "x")
        Configuration.load_all_configs()
        before = Configuration._merged()

        class Msg:
            data = {}

        Configuration.patch_clear(Msg())
        Configuration.load_all_configs()
        self.assertIsNot(Configuration._merged(), before)
        self.assertIsNone(Configuration()["unittest_marker4"])

    def test_layer_swap_invalidates(self):
        """Direct class-attribute layer replacement (the test_locations /
        embedder pattern) must invalidate via the metaclass."""
        Configuration = _config_cls()
        Configuration.load_all_configs()
        before = Configuration._merged()
        old = Configuration.xdg_configs
        try:
            Configuration.xdg_configs = list(old)
            Configuration.load_all_configs()
            self.assertIsNot(Configuration._merged(), before,
                             "layer swap must invalidate the memo")
        finally:
            Configuration.xdg_configs = old

    def test_reload_invalidates(self):
        Configuration = _config_cls()
        Configuration.load_all_configs()
        before = Configuration._merged()
        Configuration.reload()
        Configuration.load_all_configs()
        self.assertIsNot(Configuration._merged(), before)

    def test_clear_cache_invalidates(self):
        Configuration = _config_cls()
        Configuration.load_all_configs()
        before = Configuration._merged()
        Configuration.clear_cache()
        Configuration.load_all_configs()
        self.assertIsNot(Configuration._merged(), before)

    def test_file_change_invalidates(self):
        Configuration = _config_cls()
        Configuration.load_all_configs()
        before = Configuration._merged()
        # simulate the watchdog reporting a change on a real layer: force the
        # hash comparison to differ so the changed-file branch runs
        layer = Configuration.xdg_configs[-1]
        with patch.object(type(layer), "reload"), \
             patch("ovos_config.config.hash", side_effect=[1, 2], create=True):
            Configuration._on_file_change(layer.path)
        Configuration.load_all_configs()
        self.assertIsNot(Configuration._merged(), before,
                         "a changed config file must invalidate the memo")

    def test_unchanged_file_keeps_memo(self):
        Configuration = _config_cls()
        Configuration.load_all_configs()
        before = Configuration._merged()
        layer = Configuration.xdg_configs[-1]
        with patch.object(type(layer), "reload"), \
             patch("ovos_config.config.hash", side_effect=[7, 7], create=True):
            Configuration._on_file_change(layer.path)
        self.assertIs(Configuration._merged(), before,
                      "an unchanged file must not drop the memo")

    def test_custom_constraints_bypass_cache(self):
        Configuration = _config_cls()
        Configuration.load_all_configs()  # prime
        memo = Configuration._merged()
        bypass = Configuration.load_all_configs(
            {"disable_user_config": True, "disable_remote_config": True})
        self.assertIsNot(bypass, memo,
                         "constrained loads must not serve the default memo")
        # and must not poison it either
        self.assertIs(Configuration._merged(), memo)

    def test_partial_reload_failure_still_invalidates(self):
        """reload() must invalidate even when a later layer reload raises
        after an earlier one already succeeded."""
        Configuration = _config_cls()
        Configuration.load_all_configs()
        self.assertIsNotNone(Configuration._merged())
        with patch.object(type(Configuration.system), "reload",
                          side_effect=RuntimeError("disk gone")):
            with self.assertRaises(RuntimeError):
                Configuration.reload()
        self.assertIsNone(Configuration._merged(),
                          "a failed reload must not leave a stale memo")

    def test_stale_inflight_merge_is_not_published(self):
        """A merge that started before an invalidation must not repopulate
        the memo after it (generation guard)."""
        Configuration = _config_cls()
        generation = Configuration._cache_generation
        stale = {"stale": True}
        Configuration._invalidate_cache()          # lands mid-merge
        Configuration._publish_cache(stale, generation)
        self.assertIsNone(Configuration._merged(),
                          "stale in-flight merge must be refused")
        # a merge recorded AFTER the invalidation publishes fine
        generation = Configuration._cache_generation
        fresh = {"fresh": True}
        Configuration._publish_cache(fresh, generation)
        self.assertIs(Configuration._merged(), fresh)


if __name__ == "__main__":
    unittest.main()
