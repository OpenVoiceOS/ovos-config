# Pre-release quirks

Behavior changes since the last stable release, newest first. This file is
reset at each stable release; entries that remove or deprecate behavior
become the deprecation ledger for the next semver cycle.

## 2.3.8a3

- The shipped `conf_high` for the padatious pipeline drops from 0.95 to 0.9,
  the entity-hint identity boundary. With ovos-workshop 9.5.0a1+
  auto-registering `.entity` files, out-of-list slot values blend to final
  confidences around 0.94, and at the old threshold their routing flipped
  between high and unmatched per training run. Behavior change: utterances
  scoring 0.9–0.95 now route at the padatious high stage instead of falling
  through to later pipeline stages (or, on the default high-only pipeline,
  to nothing).
