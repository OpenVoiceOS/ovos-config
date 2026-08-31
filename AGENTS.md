# AGENTS.md

Conventions for AI coding agents (internal and community) working in this
repository.

## What this repo is

`ovos-config` loads and merges OVOS configuration. It defines the shipped
default `mycroft.conf`, the layered load order (default → remote → system →
user), and the `recommends/` platform/locale overlay files that other OVOS
tooling applies on top of the defaults.

`ovos-core`, `ovos-workshop`, and `ovos_bus_client` all depend on it for
reading configuration and locale settings. Unlike its sibling packages it
is still packaged with `setup.py` and a `requirements/` directory rather
than a fully declarative `pyproject.toml`.

## Ground rules

- Work on a feature branch. Never push to `dev` or `master` directly.
- Open pull requests against `dev` as **drafts** until CI is green and the
  change is ready for review.
- One commit per PR. Squash before pushing if history accumulates.

- Use conventional commit prefixes (`fix:`, `feat:`, `refactor:`, `docs:`,
  `test:`, `chore:`). Reserve `feat:` for changes a user or downstream
  consumer can actually observe.
- Never hand-edit `ovos_config/version.py`'s `VERSION_MAJOR`/`MINOR`/`BUILD`/
  `ALPHA` block by hand for a version bump. CI computes and bumps the version
  from conventional commit history.

- Every PR description and issue you write or edit carries an AI-authorship
  disclosure at the top, naming the exact model used, and states the text is
  not human-reviewed.

## Dependencies

- Use `uv`, never `pip`, for installing and resolving dependencies.

- Pin floors only, and always allow prereleases: `>=X.Y.Za1`. The runtime
  list in `pyproject.toml` still carries `~=` compatible-release pins
  (`combo_lock~=0.3`, `python-dateutil~=2.9`, `rich-click~=1.6`) and a plain
  floor on `ovos-utils`. When you touch one of those lines, move it to an
  explicit `>=X.Y.Za1` floor rather than leaving a `~=` pin that blocks
  prereleases.

- All dependency and metadata declarations live in `pyproject.toml`
  (`dependencies` for runtime, `[project.optional-dependencies].test` for
  the test extra). Nothing dependency-related belongs in CI workflow files.
- Never install a dependency from a git URL. Publish an alpha to PyPI and
  depend on that.

## Testing

```bash
uv venv .venv
source .venv/bin/activate
uv pip install -e ".[test]"
pytest test/unittests
```

A regression test for a bug must be shown to fail against the code before the
fix and pass after it. A test that passes against unfixed code proves
nothing and does not satisfy this gate.

## Docs discipline

Any change that touches observable behavior updates `README.md` in the same
PR. Also add a version-stamped entry at the top of `docs/prerelease-quirks.md`
describing the change (create the file and the `docs/` directory if neither
exists yet), newest entry first.

## Repo-specific notes

- The values shipped in `ovos_config/mycroft.conf` (units, listener wake
  word, default TTS/STT engine choices, pipeline order, and similar) are
  ecosystem-wide decisions, not bugs. Do not change a shipped default inside
  a `fix:` PR because it doesn't match your preference or a downstream
  project's needs. That is a `feat:`/discussion-worthy change with
  ecosystem-wide impact, and it needs explicit sign-off, not a quiet default
  swap.

- `ovos_config/recommends/` holds per-platform and per-locale overlay files
  (for example `recommends/base/en-us.conf` and `recommends/platform/*.conf`).
  `ovos-config` applies them with a recursive, key-by-key dictionary merge on
  top of the shipped defaults (`do_merge` in `ovos_config/__main__.py` →
  `LocalConf.merge` → `ovos_utils.json_helper.merge_dict`), so an overlay
  only needs the keys it changes.

  Never copy a whole section from `mycroft.conf` into an overlay. That
  duplicates defaults that then drift.

- `test/unittests` is the real test path, with further subdirectories
  (`test/unittests/mycroft`, `test/unittests/test_config`,
  `test/unittests/config_stack`). It is not a flat `test/` directory.
