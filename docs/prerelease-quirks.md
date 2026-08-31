# Pre-release quirks

Behavior changes since the last stable release, newest first. This file is
reset at each stable release; entries that remove or deprecate behavior
become the deprecation ledger for the next semver cycle.

## 2.3.11a3

- **BREAKING**: remote configuration is removed from the merge stack.
  `Configuration.remote` no longer exists (it is a plain `AttributeError`),
  `Configuration.handle_remote_update` is gone, and remote config can no
  longer be re-enabled through `system_constraints`
  (`disable_remote_config`, `protected_keys.remote`). Per owner ruling, no
  compat accessor is provided for `Configuration.remote` -- this is a
  clean break, not a deprecate-then-remove cycle. `RemoteConf` itself stays
  importable as a deprecated class (warns on construction, "removed in
  3.0.0") but is not part of the config stack.
- A new `AssistantConfig` layer (`~/.config/mycroft/runtime.conf`) sits
  between `SystemConfig` and the user config in the merge order
  (`user > assistant > system > distribution > default`). It is the place
  for OVOS components (skills, plugins, e.g. automatic location detection)
  to persist runtime changes without touching the user's own config file.
  Write to it with `update_assistant_config(config, bus)`.
- `MycroftDefaultConfig`, `OvosDistributionConfig`, `MycroftSystemConfig`,
  `MycroftUserConfig` and `MycroftXDGConfig` are renamed to `DefaultConfig`,
  `DistributionConfig`, `SystemConfig`, `UserConfig` (the old names remain
  as deprecated aliases, "removed in 3.0.0"). `read_mycroft_config`,
  `update_mycroft_config`, `load_config_stack` and
  `get_webcache_location`/`find_default_config` are likewise deprecated in
  favor of `Configuration()`, `update_assistant_config`/direct user-config
  writes, and `load_all_configs`, respectively.

## 2.3.9a2

- `Configuration` memoizes the merged config stack instead of re-merging
  the layers on every read (key reads went from ~75µs to ~0.44µs). Every
  mutation path invalidates the memo: `patch`/`__setitem__`/`update`,
  `reload`, the filewatcher on config-file change, `handle_remote_update`,
  bus `configuration.patch*` messages, and direct layer swaps through the
  metaclass (`Configuration.default = ...`, `Configuration.xdg_configs =
  ...`). `Configuration.clear_cache()` is no longer a deprecated no-op:
  it drops the memoized merge and reloads. `load_all_configs()` now
  returns a shallow copy of the memo, so a caller mutating the returned
  top-level dict no longer corrupts the cache for subsequent reads.
  Known nit: memo validity is checked with `is not None`, so a memoized
  empty merge (`{}`) would be served indefinitely instead of triggering a
  rebuild. Unreachable in practice — the baked-in default layer is never
  empty, so `filter_and_merge` cannot produce `{}` — but the sentinel
  should be a private marker rather than `None` if that invariant ever
  weakens.

## 2.3.8a3

- The default `intents.pipeline` list now includes
  `ovos-padatious-pipeline-plugin-medium` (between the stop and adapt medium
  stages). Auto-registered `.entity` files (ovos-workshop 9.5.0a1+) score
  open-slot values below the padatious `conf_high` threshold (identity cap
  0.9 < 0.95), so on a high-only pipeline those utterances matched nothing.
  Behavior change: utterances that previously fell through unmatched on a
  default install can now match at padatious medium confidence
  (`conf_med`, 0.8).
