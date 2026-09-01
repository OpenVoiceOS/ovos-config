# Changelog

## [3.2.0a1](https://github.com/OpenVoiceOS/ovos-config/tree/3.2.0a1) (2026-09-01)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/3.1.1a4...3.2.0a1)

**Merged pull requests:**

- feat: GPU STT tier on onnx-asr \(use\_cuda\) + best per-lang models [\#274](https://github.com/OpenVoiceOS/ovos-config/pull/274) ([JarbasAl](https://github.com/JarbasAl))

## [3.1.1a4](https://github.com/OpenVoiceOS/ovos-config/tree/3.1.1a4) (2026-09-01)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/3.1.1a3...3.1.1a4)

**Merged pull requests:**

- chore: raise dependency floors \(ovos-utils, PyYAML, rich-click\) [\#309](https://github.com/OpenVoiceOS/ovos-config/pull/309) ([JarbasAl](https://github.com/JarbasAl))

## [3.1.1a3](https://github.com/OpenVoiceOS/ovos-config/tree/3.1.1a3) (2026-09-01)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/3.1.1a2...3.1.1a3)

**Merged pull requests:**

- Update actions/checkout action to v7 [\#271](https://github.com/OpenVoiceOS/ovos-config/pull/271) ([renovate[bot]](https://github.com/apps/renovate))

## [3.1.1a2](https://github.com/OpenVoiceOS/ovos-config/tree/3.1.1a2) (2026-09-01)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/3.1.1a1...3.1.1a2)

**Merged pull requests:**

- Update actions/setup-python action to v7 [\#277](https://github.com/OpenVoiceOS/ovos-config/pull/277) ([renovate[bot]](https://github.com/apps/renovate))

## [3.1.1a1](https://github.com/OpenVoiceOS/ovos-config/tree/3.1.1a1) (2026-09-01)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/3.1.0a1...3.1.1a1)

**Merged pull requests:**

- fix: CLI config targets swapped, set writes to assistant config [\#305](https://github.com/OpenVoiceOS/ovos-config/pull/305) ([JarbasAl](https://github.com/JarbasAl))

## [3.1.0a1](https://github.com/OpenVoiceOS/ovos-config/tree/3.1.0a1) (2026-09-01)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/3.0.1a1...3.1.0a1)

**Merged pull requests:**

- feat: default m2v intent model per language [\#306](https://github.com/OpenVoiceOS/ovos-config/pull/306) ([JarbasAl](https://github.com/JarbasAl))

## [3.0.1a1](https://github.com/OpenVoiceOS/ovos-config/tree/3.0.1a1) (2026-08-31)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/3.0.0a1...3.0.1a1)

**Merged pull requests:**

- fix: webcache migration, concurrent-write coherence and protected\_keys.assistant [\#303](https://github.com/OpenVoiceOS/ovos-config/pull/303) ([JarbasAl](https://github.com/JarbasAl))

## [3.0.0a1](https://github.com/OpenVoiceOS/ovos-config/tree/3.0.0a1) (2026-08-31)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/2.3.11a2...3.0.0a1)

**Breaking changes:**

- feat!: assistant config; drop remote config from the stack [\#194](https://github.com/OpenVoiceOS/ovos-config/pull/194) ([JarbasAl](https://github.com/JarbasAl))

## [2.3.11a2](https://github.com/OpenVoiceOS/ovos-config/tree/2.3.11a2) (2026-08-31)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/2.3.11a1...2.3.11a2)

**Merged pull requests:**

- docs: add AGENTS.md with the conventions for coding agents [\#300](https://github.com/OpenVoiceOS/ovos-config/pull/300) ([JarbasAl](https://github.com/JarbasAl))

## [2.3.11a1](https://github.com/OpenVoiceOS/ovos-config/tree/2.3.11a1) (2026-08-26)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/2.3.10a2...2.3.11a1)

**Closed issues:**

- A config file that does not exist at boot is never watched, so the first write to it needs a restart [\#297](https://github.com/OpenVoiceOS/ovos-config/issues/297)

**Merged pull requests:**

- fix: watch configuration files that do not exist yet [\#298](https://github.com/OpenVoiceOS/ovos-config/pull/298) ([JarbasAl](https://github.com/JarbasAl))

## [2.3.10a2](https://github.com/OpenVoiceOS/ovos-config/tree/2.3.10a2) (2026-08-23)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/2.3.10a1...2.3.10a2)

**Merged pull requests:**

- docs: prerelease-quirks entry for 2.3.9a2 config memoization [\#294](https://github.com/OpenVoiceOS/ovos-config/pull/294) ([JarbasAl](https://github.com/JarbasAl))

## [2.3.10a1](https://github.com/OpenVoiceOS/ovos-config/tree/2.3.10a1) (2026-08-19)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/2.3.9a2...2.3.10a1)

**Merged pull requests:**

- fix: correct fake\_barge\_in comment [\#291](https://github.com/OpenVoiceOS/ovos-config/pull/291) ([JarbasAl](https://github.com/JarbasAl))

## [2.3.9a2](https://github.com/OpenVoiceOS/ovos-config/tree/2.3.9a2) (2026-08-18)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/2.3.9a1...2.3.9a2)

**Merged pull requests:**

- perf: memoize the merged config stack [\#288](https://github.com/OpenVoiceOS/ovos-config/pull/288) ([goldyfruit](https://github.com/goldyfruit))

## [2.3.9a1](https://github.com/OpenVoiceOS/ovos-config/tree/2.3.9a1) (2026-08-14)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/2.3.8a2...2.3.9a1)

**Merged pull requests:**

- fix: add padatious medium stage to shipped pipelines [\#289](https://github.com/OpenVoiceOS/ovos-config/pull/289) ([JarbasAl](https://github.com/JarbasAl))

## [2.3.8a2](https://github.com/OpenVoiceOS/ovos-config/tree/2.3.8a2) (2026-08-02)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/2.3.7a1...2.3.8a2)

**Merged pull requests:**

- chore: pyproject-only packaging and the shared workflows [\#286](https://github.com/OpenVoiceOS/ovos-config/pull/286) ([JarbasAl](https://github.com/JarbasAl))

## [2.3.7a1](https://github.com/OpenVoiceOS/ovos-config/tree/2.3.7a1) (2026-08-01)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/2.3.6a1...2.3.7a1)

**Merged pull requests:**

- fix: user config must win over /etc/xdg, not lose to it [\#284](https://github.com/OpenVoiceOS/ovos-config/pull/284) ([JarbasAl](https://github.com/JarbasAl))

## [2.3.6a1](https://github.com/OpenVoiceOS/ovos-config/tree/2.3.6a1) (2026-07-26)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/2.3.5a1...2.3.6a1)

**Merged pull requests:**

- fix: reload the distribution config layer in Configuration.reload\(\) [\#281](https://github.com/OpenVoiceOS/ovos-config/pull/281) ([JarbasAl](https://github.com/JarbasAl))

## [2.3.5a1](https://github.com/OpenVoiceOS/ovos-config/tree/2.3.5a1) (2026-07-24)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/2.3.3a1...2.3.5a1)

**Merged pull requests:**

- fix: mark deprecated code for removal [\#253](https://github.com/OpenVoiceOS/ovos-config/pull/253) ([JarbasAl](https://github.com/JarbasAl))

## [2.3.3a1](https://github.com/OpenVoiceOS/ovos-config/tree/2.3.3a1) (2026-07-24)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/2.3.2a2...2.3.3a1)

**Merged pull requests:**

- fix: bind gui\_websocket to loopback by default, matching the messagebus [\#280](https://github.com/OpenVoiceOS/ovos-config/pull/280) ([JarbasAl](https://github.com/JarbasAl))

## [2.3.2a2](https://github.com/OpenVoiceOS/ovos-config/tree/2.3.2a2) (2026-07-16)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/2.3.2a1...2.3.2a2)

**Merged pull requests:**

- revert: restore padatious-only default pipeline [\#276](https://github.com/OpenVoiceOS/ovos-config/pull/276) ([JarbasAl](https://github.com/JarbasAl))

## [2.3.2a1](https://github.com/OpenVoiceOS/ovos-config/tree/2.3.2a1) (2026-07-16)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/2.3.1a1...2.3.2a1)

**Merged pull requests:**

- fix: include padacioso in the default intent pipeline [\#275](https://github.com/OpenVoiceOS/ovos-config/pull/275) ([JarbasAl](https://github.com/JarbasAl))

## [2.3.1a1](https://github.com/OpenVoiceOS/ovos-config/tree/2.3.1a1) (2026-06-23)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/2.3.0a1...2.3.1a1)

**Merged pull requests:**

- fix:pipeline\_config [\#264](https://github.com/OpenVoiceOS/ovos-config/pull/264) ([JarbasAl](https://github.com/JarbasAl))

## [2.3.0a1](https://github.com/OpenVoiceOS/ovos-config/tree/2.3.0a1) (2026-06-23)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/2.2.0a1...2.3.0a1)

**Merged pull requests:**

- feat: onnx-asr offline STT tier \(parakeet + OVOS collection models\) [\#273](https://github.com/OpenVoiceOS/ovos-config/pull/273) ([JarbasAl](https://github.com/JarbasAl))

## [2.2.0a1](https://github.com/OpenVoiceOS/ovos-config/tree/2.2.0a1) (2026-06-23)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/2.1.4a7...2.2.0a1)

**Closed issues:**

- Autoconfig local with gpu offline fails to load whisper model [\#266](https://github.com/OpenVoiceOS/ovos-config/issues/266)

**Merged pull requests:**

- feat: phoonnx as the default offline TTS in autoconfigure recommends [\#272](https://github.com/OpenVoiceOS/ovos-config/pull/272) ([JarbasAl](https://github.com/JarbasAl))

## [2.1.4a7](https://github.com/OpenVoiceOS/ovos-config/tree/2.1.4a7) (2025-12-19)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/2.1.4a6...2.1.4a7)

**Merged pull requests:**

- chore\(deps\): update pilosus/action-pip-license-checker action to v3 [\#263](https://github.com/OpenVoiceOS/ovos-config/pull/263) ([renovate[bot]](https://github.com/apps/renovate))

## [2.1.4a6](https://github.com/OpenVoiceOS/ovos-config/tree/2.1.4a6) (2025-12-19)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/2.1.4a5...2.1.4a6)

**Merged pull requests:**

- chore\(deps\): update dependency python to 3.14 [\#255](https://github.com/OpenVoiceOS/ovos-config/pull/255) ([renovate[bot]](https://github.com/apps/renovate))

## [2.1.4a5](https://github.com/OpenVoiceOS/ovos-config/tree/2.1.4a5) (2025-12-19)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/2.1.4a4...2.1.4a5)

## [2.1.4a4](https://github.com/OpenVoiceOS/ovos-config/tree/2.1.4a4) (2025-12-19)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/2.1.4a3...2.1.4a4)

**Merged pull requests:**

- chore\(deps\): update actions/setup-python action to v6 [\#260](https://github.com/OpenVoiceOS/ovos-config/pull/260) ([renovate[bot]](https://github.com/apps/renovate))
- chore\(deps\): update actions/checkout action to v6 [\#259](https://github.com/OpenVoiceOS/ovos-config/pull/259) ([renovate[bot]](https://github.com/apps/renovate))

## [2.1.4a3](https://github.com/OpenVoiceOS/ovos-config/tree/2.1.4a3) (2025-12-18)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/2.1.4a2...2.1.4a3)

**Merged pull requests:**

- chore: Configure Renovate [\#254](https://github.com/OpenVoiceOS/ovos-config/pull/254) ([renovate[bot]](https://github.com/apps/renovate))

## [2.1.4a2](https://github.com/OpenVoiceOS/ovos-config/tree/2.1.4a2) (2025-11-05)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/2.1.4a1...2.1.4a2)

**Merged pull requests:**

- enable pre-wake-vad by default [\#251](https://github.com/OpenVoiceOS/ovos-config/pull/251) ([JarbasAl](https://github.com/JarbasAl))

## [2.1.4a1](https://github.com/OpenVoiceOS/ovos-config/tree/2.1.4a1) (2025-10-31)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/2.1.3a1...2.1.4a1)

**Merged pull requests:**

- fix: prefer precise onnx [\#249](https://github.com/OpenVoiceOS/ovos-config/pull/249) ([JarbasAl](https://github.com/JarbasAl))

## [2.1.3a1](https://github.com/OpenVoiceOS/ovos-config/tree/2.1.3a1) (2025-10-09)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/2.1.2a5...2.1.3a1)

**Merged pull requests:**

- fix: en-us female voice [\#247](https://github.com/OpenVoiceOS/ovos-config/pull/247) ([JarbasAl](https://github.com/JarbasAl))

## [2.1.2a5](https://github.com/OpenVoiceOS/ovos-config/tree/2.1.2a5) (2025-10-09)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/2.1.2a4...2.1.2a5)

**Merged pull requests:**

- update default voices [\#242](https://github.com/OpenVoiceOS/ovos-config/pull/242) ([JarbasAl](https://github.com/JarbasAl))

## [2.1.2a4](https://github.com/OpenVoiceOS/ovos-config/tree/2.1.2a4) (2025-09-08)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/2.1.2a3...2.1.2a4)

**Merged pull requests:**

- Termux config [\#243](https://github.com/OpenVoiceOS/ovos-config/pull/243) ([JarbasAl](https://github.com/JarbasAl))

## [2.1.2a3](https://github.com/OpenVoiceOS/ovos-config/tree/2.1.2a3) (2025-07-22)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/2.1.2a2...2.1.2a3)

**Merged pull requests:**

- Update pt-pt.conf [\#240](https://github.com/OpenVoiceOS/ovos-config/pull/240) ([JarbasAl](https://github.com/JarbasAl))

## [2.1.2a2](https://github.com/OpenVoiceOS/ovos-config/tree/2.1.2a2) (2025-06-18)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/2.1.2a1...2.1.2a2)

**Merged pull requests:**

- finetune\_lang\_configs [\#236](https://github.com/OpenVoiceOS/ovos-config/pull/236) ([JarbasAl](https://github.com/JarbasAl))

## [2.1.2a1](https://github.com/OpenVoiceOS/ovos-config/tree/2.1.2a1) (2025-06-18)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/2.1.1...2.1.2a1)

**Merged pull requests:**

- fix:default\_pipeline\_recommendations [\#234](https://github.com/OpenVoiceOS/ovos-config/pull/234) ([JarbasAl](https://github.com/JarbasAl))

## [2.1.1](https://github.com/OpenVoiceOS/ovos-config/tree/2.1.1) (2025-06-18)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/2.1.1a1...2.1.1)

## [2.1.1a1](https://github.com/OpenVoiceOS/ovos-config/tree/2.1.1a1) (2025-06-18)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/2.1.0a1...2.1.1a1)

**Merged pull requests:**

- fix: error handling [\#232](https://github.com/OpenVoiceOS/ovos-config/pull/232) ([JarbasAl](https://github.com/JarbasAl))

## [2.1.0a1](https://github.com/OpenVoiceOS/ovos-config/tree/2.1.0a1) (2025-06-18)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/2.0.0...2.1.0a1)

**Merged pull requests:**

- feat:update recommended configs [\#230](https://github.com/OpenVoiceOS/ovos-config/pull/230) ([JarbasAl](https://github.com/JarbasAl))

## [2.0.0](https://github.com/OpenVoiceOS/ovos-config/tree/2.0.0) (2025-06-16)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/2.0.0a1...2.0.0)

**Merged pull requests:**

- Release 2.0.0a1 [\#229](https://github.com/OpenVoiceOS/ovos-config/pull/229) ([github-actions[bot]](https://github.com/apps/github-actions))

## [2.0.0a1](https://github.com/OpenVoiceOS/ovos-config/tree/2.0.0a1) (2025-06-16)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/1.2.2...2.0.0a1)

**Breaking changes:**

- Update mycroft.conf [\#228](https://github.com/OpenVoiceOS/ovos-config/pull/228) ([JarbasAl](https://github.com/JarbasAl))

## [1.2.2](https://github.com/OpenVoiceOS/ovos-config/tree/1.2.2) (2025-05-27)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/1.2.2a1...1.2.2)

**Merged pull requests:**

- Release 1.2.2a1 [\#227](https://github.com/OpenVoiceOS/ovos-config/pull/227) ([github-actions[bot]](https://github.com/apps/github-actions))

## [1.2.2a1](https://github.com/OpenVoiceOS/ovos-config/tree/1.2.2a1) (2025-05-27)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/1.2.1...1.2.2a1)

**Merged pull requests:**

- document intent transformers [\#226](https://github.com/OpenVoiceOS/ovos-config/pull/226) ([JarbasAl](https://github.com/JarbasAl))

## [1.2.1](https://github.com/OpenVoiceOS/ovos-config/tree/1.2.1) (2025-04-27)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/1.2.1a1...1.2.1)

**Merged pull requests:**

- Release 1.2.1a1 [\#225](https://github.com/OpenVoiceOS/ovos-config/pull/225) ([github-actions[bot]](https://github.com/apps/github-actions))

## [1.2.1a1](https://github.com/OpenVoiceOS/ovos-config/tree/1.2.1a1) (2025-04-27)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/1.2.0...1.2.1a1)

**Merged pull requests:**

- Update nl-nl.conf [\#224](https://github.com/OpenVoiceOS/ovos-config/pull/224) ([timonvanhasselt](https://github.com/timonvanhasselt))
- Update nl-nl.conf [\#223](https://github.com/OpenVoiceOS/ovos-config/pull/223) ([timonvanhasselt](https://github.com/timonvanhasselt))
- Update nl-nl.conf [\#222](https://github.com/OpenVoiceOS/ovos-config/pull/222) ([timonvanhasselt](https://github.com/timonvanhasselt))
- Update nl-nl.conf [\#221](https://github.com/OpenVoiceOS/ovos-config/pull/221) ([timonvanhasselt](https://github.com/timonvanhasselt))

## [1.2.0](https://github.com/OpenVoiceOS/ovos-config/tree/1.2.0) (2025-04-11)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/1.2.0a1...1.2.0)

**Merged pull requests:**

- Release 1.2.0a1 [\#220](https://github.com/OpenVoiceOS/ovos-config/pull/220) ([github-actions[bot]](https://github.com/apps/github-actions))

## [1.2.0a1](https://github.com/OpenVoiceOS/ovos-config/tree/1.2.0a1) (2025-04-11)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/1.1.0...1.2.0a1)

**Merged pull requests:**

- feat: ovos-config telemetry [\#219](https://github.com/OpenVoiceOS/ovos-config/pull/219) ([JarbasAl](https://github.com/JarbasAl))

## [1.1.0](https://github.com/OpenVoiceOS/ovos-config/tree/1.1.0) (2025-03-27)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/1.1.0a1...1.1.0)

**Merged pull requests:**

- Release 1.1.0a1 [\#216](https://github.com/OpenVoiceOS/ovos-config/pull/216) ([github-actions[bot]](https://github.com/apps/github-actions))

## [1.1.0a1](https://github.com/OpenVoiceOS/ovos-config/tree/1.1.0a1) (2025-03-27)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/1.0.8...1.1.0a1)

**Merged pull requests:**

- feat:autoconfigure\_hybrid [\#215](https://github.com/OpenVoiceOS/ovos-config/pull/215) ([JarbasAl](https://github.com/JarbasAl))

## [1.0.8](https://github.com/OpenVoiceOS/ovos-config/tree/1.0.8) (2025-03-27)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/1.0.8a1...1.0.8)

**Merged pull requests:**

- Release 1.0.8a1 [\#214](https://github.com/OpenVoiceOS/ovos-config/pull/214) ([github-actions[bot]](https://github.com/apps/github-actions))

## [1.0.8a1](https://github.com/OpenVoiceOS/ovos-config/tree/1.0.8a1) (2025-03-27)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/1.0.7...1.0.8a1)

**Merged pull requests:**

- Update langs autoconfigure [\#213](https://github.com/OpenVoiceOS/ovos-config/pull/213) ([JarbasAl](https://github.com/JarbasAl))

## [1.0.7](https://github.com/OpenVoiceOS/ovos-config/tree/1.0.7) (2025-03-19)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/1.0.7a1...1.0.7)

**Merged pull requests:**

- Release 1.0.7a1 [\#211](https://github.com/OpenVoiceOS/ovos-config/pull/211) ([github-actions[bot]](https://github.com/apps/github-actions))

## [1.0.7a1](https://github.com/OpenVoiceOS/ovos-config/tree/1.0.7a1) (2025-03-19)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/1.0.6...1.0.7a1)

**Merged pull requests:**

- fix: update lang configs [\#210](https://github.com/OpenVoiceOS/ovos-config/pull/210) ([JarbasAl](https://github.com/JarbasAl))

## [1.0.6](https://github.com/OpenVoiceOS/ovos-config/tree/1.0.6) (2025-03-19)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/1.0.6a1...1.0.6)

**Merged pull requests:**

- Release 1.0.6a1 [\#209](https://github.com/OpenVoiceOS/ovos-config/pull/209) ([github-actions[bot]](https://github.com/apps/github-actions))

## [1.0.6a1](https://github.com/OpenVoiceOS/ovos-config/tree/1.0.6a1) (2025-03-19)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/1.0.5...1.0.6a1)

**Merged pull requests:**

- Update lang configs [\#208](https://github.com/OpenVoiceOS/ovos-config/pull/208) ([JarbasAl](https://github.com/JarbasAl))

## [1.0.5](https://github.com/OpenVoiceOS/ovos-config/tree/1.0.5) (2025-03-19)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/1.0.5a1...1.0.5)

**Merged pull requests:**

- Release 1.0.5a1 [\#207](https://github.com/OpenVoiceOS/ovos-config/pull/207) ([github-actions[bot]](https://github.com/apps/github-actions))

## [1.0.5a1](https://github.com/OpenVoiceOS/ovos-config/tree/1.0.5a1) (2025-03-19)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/1.0.4...1.0.5a1)

**Merged pull requests:**

- fix: python version in automations [\#206](https://github.com/OpenVoiceOS/ovos-config/pull/206) ([JarbasAl](https://github.com/JarbasAl))

## [1.0.4](https://github.com/OpenVoiceOS/ovos-config/tree/1.0.4) (2025-03-19)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/1.0.4a3...1.0.4)

**Merged pull requests:**

- Release 1.0.4a2 [\#205](https://github.com/OpenVoiceOS/ovos-config/pull/205) ([github-actions[bot]](https://github.com/apps/github-actions))

## [1.0.4a3](https://github.com/OpenVoiceOS/ovos-config/tree/1.0.4a3) (2025-03-19)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/1.0.4a2...1.0.4a3)

## [1.0.4a2](https://github.com/OpenVoiceOS/ovos-config/tree/1.0.4a2) (2025-03-19)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/1.0.4a1...1.0.4a2)

**Merged pull requests:**

- Bump flake8 from 3.7.9 to 7.1.2 in /requirements [\#199](https://github.com/OpenVoiceOS/ovos-config/pull/199) ([dependabot[bot]](https://github.com/apps/dependabot))

## [1.0.4a1](https://github.com/OpenVoiceOS/ovos-config/tree/1.0.4a1) (2025-03-19)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/1.0.3...1.0.4a1)

**Merged pull requests:**

- Update combo-lock requirement from ~=0.2 to ~=0.3 in /requirements [\#192](https://github.com/OpenVoiceOS/ovos-config/pull/192) ([dependabot[bot]](https://github.com/apps/dependabot))
- Bump pytest-cov from 2.8.1 to 6.0.0 in /requirements [\#189](https://github.com/OpenVoiceOS/ovos-config/pull/189) ([dependabot[bot]](https://github.com/apps/dependabot))

## [1.0.3](https://github.com/OpenVoiceOS/ovos-config/tree/1.0.3) (2025-03-13)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/1.0.3a1...1.0.3)

**Merged pull requests:**

- Release 1.0.3a1 [\#203](https://github.com/OpenVoiceOS/ovos-config/pull/203) ([github-actions[bot]](https://github.com/apps/github-actions))

## [1.0.3a1](https://github.com/OpenVoiceOS/ovos-config/tree/1.0.3a1) (2025-03-13)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/1.0.2...1.0.3a1)

**Merged pull requests:**

- documentation: add opendata servers [\#202](https://github.com/OpenVoiceOS/ovos-config/pull/202) ([JarbasAl](https://github.com/JarbasAl))

## [1.0.2](https://github.com/OpenVoiceOS/ovos-config/tree/1.0.2) (2025-02-28)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/1.0.2a3...1.0.2)

**Merged pull requests:**

- Release 1.0.2a3 [\#201](https://github.com/OpenVoiceOS/ovos-config/pull/201) ([github-actions[bot]](https://github.com/apps/github-actions))

## [1.0.2a3](https://github.com/OpenVoiceOS/ovos-config/tree/1.0.2a3) (2025-02-28)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/1.0.2a2...1.0.2a3)

**Merged pull requests:**

- fix: drop padatious\_medium [\#200](https://github.com/OpenVoiceOS/ovos-config/pull/200) ([JarbasAl](https://github.com/JarbasAl))

## [1.0.2a2](https://github.com/OpenVoiceOS/ovos-config/tree/1.0.2a2) (2025-01-25)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/1.0.2a1...1.0.2a2)

**Merged pull requests:**

- Release 1.0.2a2 [\#198](https://github.com/OpenVoiceOS/ovos-config/pull/198) ([github-actions[bot]](https://github.com/apps/github-actions))
- more padatious config [\#197](https://github.com/OpenVoiceOS/ovos-config/pull/197) ([JarbasAl](https://github.com/JarbasAl))

## [1.0.2a1](https://github.com/OpenVoiceOS/ovos-config/tree/1.0.2a1) (2025-01-25)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/1.0.1...1.0.2a1)

**Merged pull requests:**

- Release 1.0.2a1 [\#196](https://github.com/OpenVoiceOS/ovos-config/pull/196) ([github-actions[bot]](https://github.com/apps/github-actions))
- documentation: new padatious options [\#195](https://github.com/OpenVoiceOS/ovos-config/pull/195) ([JarbasAl](https://github.com/JarbasAl))

## [1.0.1](https://github.com/OpenVoiceOS/ovos-config/tree/1.0.1) (2024-11-23)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/1.0.1a1...1.0.1)

**Merged pull requests:**

- Release 1.0.1a1 [\#187](https://github.com/OpenVoiceOS/ovos-config/pull/187) ([github-actions[bot]](https://github.com/apps/github-actions))

## [1.0.1a1](https://github.com/OpenVoiceOS/ovos-config/tree/1.0.1a1) (2024-11-23)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/1.0.0...1.0.1a1)

## [1.0.0](https://github.com/OpenVoiceOS/ovos-config/tree/1.0.0) (2024-11-19)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/1.0.0a1...1.0.0)

## [1.0.0a1](https://github.com/OpenVoiceOS/ovos-config/tree/1.0.0a1) (2024-11-19)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/0.4.6...1.0.0a1)

## [0.4.6](https://github.com/OpenVoiceOS/ovos-config/tree/0.4.6) (2024-11-19)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/0.4.5...0.4.6)

## [0.4.5](https://github.com/OpenVoiceOS/ovos-config/tree/0.4.5) (2024-10-27)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/0.4.5a1...0.4.5)

## [0.4.5a1](https://github.com/OpenVoiceOS/ovos-config/tree/0.4.5a1) (2024-10-27)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/0.4.4...0.4.5a1)

## [0.4.4](https://github.com/OpenVoiceOS/ovos-config/tree/0.4.4) (2024-10-23)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/0.4.4a1...0.4.4)

## [0.4.4a1](https://github.com/OpenVoiceOS/ovos-config/tree/0.4.4a1) (2024-10-23)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/0.4.3...0.4.4a1)

## [0.4.3](https://github.com/OpenVoiceOS/ovos-config/tree/0.4.3) (2024-10-19)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/0.4.3a1...0.4.3)

## [0.4.3a1](https://github.com/OpenVoiceOS/ovos-config/tree/0.4.3a1) (2024-10-19)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/0.4.2...0.4.3a1)

## [0.4.2](https://github.com/OpenVoiceOS/ovos-config/tree/0.4.2) (2024-10-18)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/0.4.2a1...0.4.2)

## [0.4.2a1](https://github.com/OpenVoiceOS/ovos-config/tree/0.4.2a1) (2024-10-18)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/0.4.1a1...0.4.2a1)

## [0.4.1a1](https://github.com/OpenVoiceOS/ovos-config/tree/0.4.1a1) (2024-10-15)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/0.4.0...0.4.1a1)

## [0.4.0](https://github.com/OpenVoiceOS/ovos-config/tree/0.4.0) (2024-10-09)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/0.4.0a1...0.4.0)

## [0.4.0a1](https://github.com/OpenVoiceOS/ovos-config/tree/0.4.0a1) (2024-10-08)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/0.3.1...0.4.0a1)

## [0.3.1](https://github.com/OpenVoiceOS/ovos-config/tree/0.3.1) (2024-10-06)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/0.3.1a1...0.3.1)

## [0.3.1a1](https://github.com/OpenVoiceOS/ovos-config/tree/0.3.1a1) (2024-10-06)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/0.3.0...0.3.1a1)

## [0.3.0](https://github.com/OpenVoiceOS/ovos-config/tree/0.3.0) (2024-09-25)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/0.3.0a1...0.3.0)

## [0.3.0a1](https://github.com/OpenVoiceOS/ovos-config/tree/0.3.0a1) (2024-09-25)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/0.2.1...0.3.0a1)

## [0.2.1](https://github.com/OpenVoiceOS/ovos-config/tree/0.2.1) (2024-09-15)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/0.2.1a1...0.2.1)

## [0.2.1a1](https://github.com/OpenVoiceOS/ovos-config/tree/0.2.1a1) (2024-09-15)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/0.2.0...0.2.1a1)

## [0.2.0](https://github.com/OpenVoiceOS/ovos-config/tree/0.2.0) (2024-09-11)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/0.2.0a1...0.2.0)

## [0.2.0a1](https://github.com/OpenVoiceOS/ovos-config/tree/0.2.0a1) (2024-09-11)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/0.1.2...0.2.0a1)

## [0.1.2](https://github.com/OpenVoiceOS/ovos-config/tree/0.1.2) (2024-09-11)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/0.1.2a1...0.1.2)

## [0.1.2a1](https://github.com/OpenVoiceOS/ovos-config/tree/0.1.2a1) (2024-09-11)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/0.1.1...0.1.2a1)

## [0.1.1](https://github.com/OpenVoiceOS/ovos-config/tree/0.1.1) (2024-09-10)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/0.1.1a1...0.1.1)

## [0.1.1a1](https://github.com/OpenVoiceOS/ovos-config/tree/0.1.1a1) (2024-09-10)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/0.1.0...0.1.1a1)

## [0.1.0](https://github.com/OpenVoiceOS/ovos-config/tree/0.1.0) (2024-09-10)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/0.1.0a1...0.1.0)

## [0.1.0a1](https://github.com/OpenVoiceOS/ovos-config/tree/0.1.0a1) (2024-09-10)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/V0.1.0...0.1.0a1)

## [V0.1.0](https://github.com/OpenVoiceOS/ovos-config/tree/V0.1.0) (2024-09-03)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/V0.0.13a27...V0.1.0)

## [V0.0.13a27](https://github.com/OpenVoiceOS/ovos-config/tree/V0.0.13a27) (2024-08-16)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/V0.0.13a26...V0.0.13a27)

## [V0.0.13a26](https://github.com/OpenVoiceOS/ovos-config/tree/V0.0.13a26) (2024-08-05)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/V0.0.13a25...V0.0.13a26)

## [V0.0.13a25](https://github.com/OpenVoiceOS/ovos-config/tree/V0.0.13a25) (2024-08-03)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/V0.0.13a24...V0.0.13a25)

## [V0.0.13a24](https://github.com/OpenVoiceOS/ovos-config/tree/V0.0.13a24) (2024-07-17)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/V0.0.13a23...V0.0.13a24)

## [V0.0.13a23](https://github.com/OpenVoiceOS/ovos-config/tree/V0.0.13a23) (2024-07-11)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/V0.0.13a22...V0.0.13a23)

## [V0.0.13a22](https://github.com/OpenVoiceOS/ovos-config/tree/V0.0.13a22) (2024-06-25)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/V0.0.13a21...V0.0.13a22)

## [V0.0.13a21](https://github.com/OpenVoiceOS/ovos-config/tree/V0.0.13a21) (2024-06-22)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/V0.0.13a20...V0.0.13a21)

## [V0.0.13a20](https://github.com/OpenVoiceOS/ovos-config/tree/V0.0.13a20) (2024-06-22)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/V0.0.13a19...V0.0.13a20)

## [V0.0.13a19](https://github.com/OpenVoiceOS/ovos-config/tree/V0.0.13a19) (2024-06-18)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/V0.0.13a18...V0.0.13a19)

## [V0.0.13a18](https://github.com/OpenVoiceOS/ovos-config/tree/V0.0.13a18) (2024-06-11)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/V0.0.13a17...V0.0.13a18)

## [V0.0.13a17](https://github.com/OpenVoiceOS/ovos-config/tree/V0.0.13a17) (2024-06-08)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/V0.0.13a16...V0.0.13a17)

## [V0.0.13a16](https://github.com/OpenVoiceOS/ovos-config/tree/V0.0.13a16) (2024-06-06)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/V0.0.13a15...V0.0.13a16)

## [V0.0.13a15](https://github.com/OpenVoiceOS/ovos-config/tree/V0.0.13a15) (2024-06-06)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/V0.0.13a14...V0.0.13a15)

## [V0.0.13a14](https://github.com/OpenVoiceOS/ovos-config/tree/V0.0.13a14) (2024-06-04)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/V0.0.13a13...V0.0.13a14)

## [V0.0.13a13](https://github.com/OpenVoiceOS/ovos-config/tree/V0.0.13a13) (2024-05-30)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/V0.0.13a12...V0.0.13a13)

## [V0.0.13a12](https://github.com/OpenVoiceOS/ovos-config/tree/V0.0.13a12) (2024-02-26)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/V0.0.13a11...V0.0.13a12)

## [V0.0.13a11](https://github.com/OpenVoiceOS/ovos-config/tree/V0.0.13a11) (2024-02-26)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/V0.0.13a10...V0.0.13a11)

## [V0.0.13a10](https://github.com/OpenVoiceOS/ovos-config/tree/V0.0.13a10) (2024-02-26)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/V0.0.13a9...V0.0.13a10)

## [V0.0.13a9](https://github.com/OpenVoiceOS/ovos-config/tree/V0.0.13a9) (2024-02-26)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/V0.0.13a8...V0.0.13a9)

## [V0.0.13a8](https://github.com/OpenVoiceOS/ovos-config/tree/V0.0.13a8) (2024-02-24)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/V0.0.13a7...V0.0.13a8)

## [V0.0.13a7](https://github.com/OpenVoiceOS/ovos-config/tree/V0.0.13a7) (2024-02-07)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/V0.0.13a6...V0.0.13a7)

## [V0.0.13a6](https://github.com/OpenVoiceOS/ovos-config/tree/V0.0.13a6) (2024-01-23)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/V0.0.13a5...V0.0.13a6)

## [V0.0.13a5](https://github.com/OpenVoiceOS/ovos-config/tree/V0.0.13a5) (2024-01-23)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/V0.0.13a4...V0.0.13a5)

## [V0.0.13a4](https://github.com/OpenVoiceOS/ovos-config/tree/V0.0.13a4) (2024-01-23)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/V0.0.13a3...V0.0.13a4)

## [V0.0.13a3](https://github.com/OpenVoiceOS/ovos-config/tree/V0.0.13a3) (2024-01-23)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/V0.0.13a2...V0.0.13a3)

## [V0.0.13a2](https://github.com/OpenVoiceOS/ovos-config/tree/V0.0.13a2) (2024-01-19)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/V0.0.13a1...V0.0.13a2)

## [V0.0.13a1](https://github.com/OpenVoiceOS/ovos-config/tree/V0.0.13a1) (2023-12-29)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/V0.0.12...V0.0.13a1)

## [V0.0.12](https://github.com/OpenVoiceOS/ovos-config/tree/V0.0.12) (2023-12-28)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/V0.0.12a9...V0.0.12)

## [V0.0.12a9](https://github.com/OpenVoiceOS/ovos-config/tree/V0.0.12a9) (2023-12-28)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/V0.0.12a8...V0.0.12a9)

## [V0.0.12a8](https://github.com/OpenVoiceOS/ovos-config/tree/V0.0.12a8) (2023-12-28)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/V0.0.12a7...V0.0.12a8)

## [V0.0.12a7](https://github.com/OpenVoiceOS/ovos-config/tree/V0.0.12a7) (2023-12-28)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/V0.0.12a6...V0.0.12a7)

## [V0.0.12a6](https://github.com/OpenVoiceOS/ovos-config/tree/V0.0.12a6) (2023-12-27)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/V0.0.12a5...V0.0.12a6)

## [V0.0.12a5](https://github.com/OpenVoiceOS/ovos-config/tree/V0.0.12a5) (2023-12-23)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/V0.0.12a4...V0.0.12a5)

## [V0.0.12a4](https://github.com/OpenVoiceOS/ovos-config/tree/V0.0.12a4) (2023-12-19)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/V0.0.12a3...V0.0.12a4)

## [V0.0.12a3](https://github.com/OpenVoiceOS/ovos-config/tree/V0.0.12a3) (2023-12-07)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/V0.0.12a2...V0.0.12a3)

## [V0.0.12a2](https://github.com/OpenVoiceOS/ovos-config/tree/V0.0.12a2) (2023-12-06)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/V0.0.12a1...V0.0.12a2)

## [V0.0.12a1](https://github.com/OpenVoiceOS/ovos-config/tree/V0.0.12a1) (2023-11-05)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/V0.0.11...V0.0.12a1)

## [V0.0.11](https://github.com/OpenVoiceOS/ovos-config/tree/V0.0.11) (2023-10-25)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/V0.0.11a15...V0.0.11)

## [V0.0.11a15](https://github.com/OpenVoiceOS/ovos-config/tree/V0.0.11a15) (2023-10-24)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/V0.0.11a14...V0.0.11a15)

## [V0.0.11a14](https://github.com/OpenVoiceOS/ovos-config/tree/V0.0.11a14) (2023-10-18)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/V0.0.11a13...V0.0.11a14)

## [V0.0.11a13](https://github.com/OpenVoiceOS/ovos-config/tree/V0.0.11a13) (2023-09-18)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/V0.0.11a12...V0.0.11a13)

## [V0.0.11a12](https://github.com/OpenVoiceOS/ovos-config/tree/V0.0.11a12) (2023-09-17)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/V0.0.11a10...V0.0.11a12)

## [V0.0.11a10](https://github.com/OpenVoiceOS/ovos-config/tree/V0.0.11a10) (2023-08-22)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/V0.0.11a9...V0.0.11a10)

## [V0.0.11a9](https://github.com/OpenVoiceOS/ovos-config/tree/V0.0.11a9) (2023-08-08)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/V0.0.11a8...V0.0.11a9)

## [V0.0.11a8](https://github.com/OpenVoiceOS/ovos-config/tree/V0.0.11a8) (2023-08-08)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/V0.0.11a7...V0.0.11a8)

## [V0.0.11a7](https://github.com/OpenVoiceOS/ovos-config/tree/V0.0.11a7) (2023-08-07)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/V0.0.11a6...V0.0.11a7)

## [V0.0.11a6](https://github.com/OpenVoiceOS/ovos-config/tree/V0.0.11a6) (2023-07-26)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/V0.0.11a5...V0.0.11a6)

## [V0.0.11a5](https://github.com/OpenVoiceOS/ovos-config/tree/V0.0.11a5) (2023-07-21)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/V0.0.11a4...V0.0.11a5)

## [V0.0.11a4](https://github.com/OpenVoiceOS/ovos-config/tree/V0.0.11a4) (2023-07-13)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/V0.0.11a3...V0.0.11a4)

## [V0.0.11a3](https://github.com/OpenVoiceOS/ovos-config/tree/V0.0.11a3) (2023-07-04)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/V0.0.11a2...V0.0.11a3)

## [V0.0.11a2](https://github.com/OpenVoiceOS/ovos-config/tree/V0.0.11a2) (2023-07-04)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/V0.0.11a1...V0.0.11a2)

## [V0.0.11a1](https://github.com/OpenVoiceOS/ovos-config/tree/V0.0.11a1) (2023-07-02)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/V0.0.10...V0.0.11a1)

## [V0.0.10](https://github.com/OpenVoiceOS/ovos-config/tree/V0.0.10) (2023-06-01)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/V0.0.10a3...V0.0.10)

## [V0.0.10a3](https://github.com/OpenVoiceOS/ovos-config/tree/V0.0.10a3) (2023-05-31)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/V0.0.10a2...V0.0.10a3)

## [V0.0.10a2](https://github.com/OpenVoiceOS/ovos-config/tree/V0.0.10a2) (2023-05-31)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/V0.0.10a1...V0.0.10a2)

## [V0.0.10a1](https://github.com/OpenVoiceOS/ovos-config/tree/V0.0.10a1) (2023-05-29)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/V0.0.9...V0.0.10a1)

## [V0.0.9](https://github.com/OpenVoiceOS/ovos-config/tree/V0.0.9) (2023-05-24)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/V0.0.9a6...V0.0.9)

## [V0.0.9a6](https://github.com/OpenVoiceOS/ovos-config/tree/V0.0.9a6) (2023-05-24)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/V0.0.9a5...V0.0.9a6)

## [V0.0.9a5](https://github.com/OpenVoiceOS/ovos-config/tree/V0.0.9a5) (2023-05-24)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/V0.0.9a4...V0.0.9a5)

## [V0.0.9a4](https://github.com/OpenVoiceOS/ovos-config/tree/V0.0.9a4) (2023-05-23)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/V0.0.9a3...V0.0.9a4)

## [V0.0.9a3](https://github.com/OpenVoiceOS/ovos-config/tree/V0.0.9a3) (2023-05-19)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/V0.0.9a2...V0.0.9a3)

## [V0.0.9a2](https://github.com/OpenVoiceOS/ovos-config/tree/V0.0.9a2) (2023-05-07)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/V0.0.9a1...V0.0.9a2)

## [V0.0.9a1](https://github.com/OpenVoiceOS/ovos-config/tree/V0.0.9a1) (2023-05-01)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/V0.0.8...V0.0.9a1)

## [V0.0.8](https://github.com/OpenVoiceOS/ovos-config/tree/V0.0.8) (2023-04-19)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/V0.0.8a5...V0.0.8)

## [V0.0.8a5](https://github.com/OpenVoiceOS/ovos-config/tree/V0.0.8a5) (2023-04-18)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/V0.0.8a4...V0.0.8a5)

## [V0.0.8a4](https://github.com/OpenVoiceOS/ovos-config/tree/V0.0.8a4) (2023-04-14)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/V0.0.8a3...V0.0.8a4)

## [V0.0.8a3](https://github.com/OpenVoiceOS/ovos-config/tree/V0.0.8a3) (2023-04-05)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/V0.0.8a2...V0.0.8a3)

## [V0.0.8a2](https://github.com/OpenVoiceOS/ovos-config/tree/V0.0.8a2) (2023-04-05)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/V0.0.8a1...V0.0.8a2)

## [V0.0.8a1](https://github.com/OpenVoiceOS/ovos-config/tree/V0.0.8a1) (2023-04-04)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/V0.0.7...V0.0.8a1)

## [V0.0.7](https://github.com/OpenVoiceOS/ovos-config/tree/V0.0.7) (2023-03-09)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/V0.0.7a2...V0.0.7)

## [V0.0.7a2](https://github.com/OpenVoiceOS/ovos-config/tree/V0.0.7a2) (2023-03-08)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/V0.0.7a1...V0.0.7a2)

## [V0.0.7a1](https://github.com/OpenVoiceOS/ovos-config/tree/V0.0.7a1) (2023-03-07)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/V0.0.6...V0.0.7a1)

## [V0.0.6](https://github.com/OpenVoiceOS/ovos-config/tree/V0.0.6) (2023-03-06)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/V0.0.6a2...V0.0.6)

## [V0.0.6a2](https://github.com/OpenVoiceOS/ovos-config/tree/V0.0.6a2) (2023-03-06)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/V0.0.6a1...V0.0.6a2)

## [V0.0.6a1](https://github.com/OpenVoiceOS/ovos-config/tree/V0.0.6a1) (2023-03-01)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/V0.0.5...V0.0.6a1)

## [V0.0.5](https://github.com/OpenVoiceOS/ovos-config/tree/V0.0.5) (2022-10-29)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/V0.0.5a6...V0.0.5)

## [V0.0.5a6](https://github.com/OpenVoiceOS/ovos-config/tree/V0.0.5a6) (2022-10-27)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/V0.0.5a5...V0.0.5a6)

## [V0.0.5a5](https://github.com/OpenVoiceOS/ovos-config/tree/V0.0.5a5) (2022-10-04)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/V0.0.5a4...V0.0.5a5)

## [V0.0.5a4](https://github.com/OpenVoiceOS/ovos-config/tree/V0.0.5a4) (2022-09-29)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/V0.0.5a3...V0.0.5a4)

## [V0.0.5a3](https://github.com/OpenVoiceOS/ovos-config/tree/V0.0.5a3) (2022-09-19)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/V0.0.5a2...V0.0.5a3)

## [V0.0.5a2](https://github.com/OpenVoiceOS/ovos-config/tree/V0.0.5a2) (2022-09-06)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/V0.0.5a1...V0.0.5a2)

## [V0.0.5a1](https://github.com/OpenVoiceOS/ovos-config/tree/V0.0.5a1) (2022-07-31)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/V0.0.4...V0.0.5a1)

## [V0.0.4](https://github.com/OpenVoiceOS/ovos-config/tree/V0.0.4) (2022-07-20)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/V0.0.4a5...V0.0.4)

## [V0.0.4a5](https://github.com/OpenVoiceOS/ovos-config/tree/V0.0.4a5) (2022-07-20)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/V0.0.4a4...V0.0.4a5)

## [V0.0.4a4](https://github.com/OpenVoiceOS/ovos-config/tree/V0.0.4a4) (2022-07-18)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/V0.0.4a3...V0.0.4a4)

## [V0.0.4a3](https://github.com/OpenVoiceOS/ovos-config/tree/V0.0.4a3) (2022-07-14)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/V0.0.4a2...V0.0.4a3)

## [V0.0.4a2](https://github.com/OpenVoiceOS/ovos-config/tree/V0.0.4a2) (2022-07-13)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/V0.0.4a1...V0.0.4a2)

## [V0.0.4a1](https://github.com/OpenVoiceOS/ovos-config/tree/V0.0.4a1) (2022-07-07)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/V0.0.3...V0.0.4a1)

## [V0.0.3](https://github.com/OpenVoiceOS/ovos-config/tree/V0.0.3) (2022-07-06)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/V0.0.3a1...V0.0.3)

## [V0.0.3a1](https://github.com/OpenVoiceOS/ovos-config/tree/V0.0.3a1) (2022-07-06)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/V0.0.2...V0.0.3a1)

## [V0.0.2](https://github.com/OpenVoiceOS/ovos-config/tree/V0.0.2) (2022-07-05)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/V0.0.2a4...V0.0.2)

## [V0.0.2a4](https://github.com/OpenVoiceOS/ovos-config/tree/V0.0.2a4) (2022-07-05)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/V0.0.2a3...V0.0.2a4)

## [V0.0.2a3](https://github.com/OpenVoiceOS/ovos-config/tree/V0.0.2a3) (2022-07-05)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/V0.0.2a2...V0.0.2a3)

## [V0.0.2a2](https://github.com/OpenVoiceOS/ovos-config/tree/V0.0.2a2) (2022-07-05)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/V0.0.2a1...V0.0.2a2)

## [V0.0.2a1](https://github.com/OpenVoiceOS/ovos-config/tree/V0.0.2a1) (2022-06-29)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/V0.0.1...V0.0.2a1)

## [V0.0.1](https://github.com/OpenVoiceOS/ovos-config/tree/V0.0.1) (2022-06-25)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/V0.0.1a2...V0.0.1)

## [V0.0.1a2](https://github.com/OpenVoiceOS/ovos-config/tree/V0.0.1a2) (2022-06-25)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-config/compare/5578c76398d3fe143716d52f3f1b1a37f729d133...V0.0.1a2)



\* *This Changelog was automatically generated by [github_changelog_generator](https://github.com/github-changelog-generator/github-changelog-generator)*
