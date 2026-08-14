# Pre-release quirks

Behavior changes since the last stable release, newest first. This file is
reset at each stable release; entries that remove or deprecate behavior
become the deprecation ledger for the next semver cycle.

## 2.3.8a3

- The default `intents.pipeline` list now includes
  `ovos-padatious-pipeline-plugin-medium` (between the stop and adapt medium
  stages). Auto-registered `.entity` files (ovos-workshop 9.5.0a1+) score
  open-slot values below the padatious `conf_high` threshold (identity cap
  0.9 < 0.95), so on a high-only pipeline those utterances matched nothing.
  Behavior change: utterances that previously fell through unmatched on a
  default install can now match at padatious medium confidence
  (`conf_med`, 0.8).
