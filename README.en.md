<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/assets/dsh-finops-suite-flow-dark.svg">
  <img src="docs/assets/dsh-finops-suite-flow-light.svg" width="100%" alt="dsh-finops-suite install flow: dsh plugin add → four rows in cordis.patch.yml → four exact pins in package.json → samples/quickstart/run.mjs → 4/4 resolved; error codes E_SUITE_PATCH_MISMATCH / E_SUITE_VERSION_MISMATCH / E_SUITE_MANIFEST_MISSING">
</picture>

# dsh-finops-suite

**Install the four finance-ops packages in one command — then verify every member version resolves.**

An install-only suite for DeepSeek Harness: e-invoicing (`dsh-einvoice`), bank reconciliation (`dsh-bankrec`), three-way match (`dsh-ap-three-way`) and travel reconciliation (`dsh-travel-recon`) pinned to one exact version set and installed together. The suite has no tool surface of its own — it reads no documents, makes no network calls, invokes no model, and keeps input and output local.

[Install](#three-step-setup) · [Configuration](#configuration) · [FAQ](#faq) · [简体中文](README.md) · [English](README.en.md) · [Español](README.es.md) · [Português](README.pt.md) · [हिन्दी](README.hi.md)

[![License](https://img.shields.io/badge/license-Apache--2.0-3366CC?style=flat-square&labelColor=2B3245)](LICENSE)
[![DSH](https://img.shields.io/badge/DSH-%E2%89%A50.2.1--rc.3%20%3C0.3.0-4B67B4?style=flat-square&labelColor=2B3245)](#compatibility)
[![npm](https://img.shields.io/npm/v/dsh-finops-suite?style=flat-square&labelColor=2B3245&color=CB3837)](https://www.npmjs.com/package/dsh-finops-suite)
[![CI](https://img.shields.io/github/actions/workflow/status/PerryLink/dsh-finops-suite/ci.yml?branch=main&label=CI&style=flat-square&labelColor=2B3245)](https://github.com/PerryLink/dsh-finops-suite/actions/workflows/ci.yml)
[![Node](https://img.shields.io/badge/node-%3E%3D24.9.0%20%3C25-339933?style=flat-square&labelColor=2B3245)](#compatibility)

[![Stars](https://img.shields.io/github/stars/PerryLink/dsh-finops-suite?style=flat-square&labelColor=2B3245)](https://github.com/PerryLink/dsh-finops-suite/stargazers)
[![npm downloads](https://img.shields.io/npm/dm/dsh-finops-suite?style=flat-square&labelColor=2B3245&color=CB3837)](https://www.npmjs.com/package/dsh-finops-suite)
[![dshfind](https://dshfind.com/api/badge/PerryLink/dsh-finops-suite?metric=downloads)](https://dshfind.com/plugins/PerryLink/dsh-finops-suite?ref=badge)
[![DSH Market](https://img.shields.io/badge/DSH_Market-listed-4B67B4?style=flat-square&labelColor=2B3245)](https://dsh.market/)
[![Gitee](https://img.shields.io/badge/Gitee-aggregate-C71D23?style=flat-square&labelColor=2B3245&logo=gitee)](https://gitee.com/perrylink/dsh-plugins)

```sh
dsh plugin --profile <profile> add dsh-finops-suite
```

</div>

<sub>Community suite, not affiliated with DeepSeek. Canonical repository: <https://github.com/PerryLink/dsh-finops-suite> (Apache-2.0).</sub>

## What it is

`dsh-finops-suite` installs all four finance-ops packages in one go: e-invoicing (`dsh-einvoice`), bank reconciliation (`dsh-bankrec`), three-way match (`dsh-ap-three-way`) and travel reconciliation (`dsh-travel-recon`). `package.json#dependencies` pins the four members to exact versions, and `cordis.patch.yml` inserts the four member rows into the profile. After install, run the bundled offline sample: the terminal prints each member, its pinned version and how it resolved — 4/4 resolved means the set is complete. The suite is an **install-only bundle**: no tool surface, no configuration keys, no documents read, no model call, no network, no files written. The real invoices, statements, match rows and travel claims are handled by the four members' own tools.

## Best for / not for

- **Best for:** installing e-invoicing, bank reconciliation, three-way match and travel reconciliation into one DSH profile; keeping all four members on one pinned version set; confirming no member row is missing right after install.
- **Not for:** installing only one package (install that member directly); expecting the suite itself to process invoices or bank statements (it has no tool surface — the members do); OCR, live bank feeds, or ERP integration.

## Input & output

**Input**

- The install itself reads no business documents.
- The bundled sample reads only `samples/quickstart/input/profile.json` (synthetic profile dump, < 1 KB), this package's `package.json` and `cordis.patch.yml`. It reads no other directory and no customer data.
- Each member's own input (invoices, bank statements, three-way rows, travel claims) is documented in that member's README; the suite does not change it.

**Output**

- The terminal prints the member list, pinned versions and where each version resolved from; exit code `0` means 4/4 resolve.
- `node samples/quickstart/run.mjs --json` prints the golden JSON stored at `samples/quickstart/expected/result.json`; `--check` compares it field by field.
- No files are written, no model is called, no network is used, nothing is uploaded, and source files are untouched.

## Three-step setup

1. **Install** (pick one channel):

   ```sh
   # npm channel (recommended, published releases)
   dsh plugin --profile <profile> add dsh-finops-suite
   # git channel (latest main)
   dsh plugin --profile <profile> add github:PerryLink/dsh-finops-suite
   # tarball channel: pnpm pack in this repo, then
   dsh plugin --profile <profile> add ./dsh-finops-suite-<version>.tgz
   # 1024 store channel
   npm i -g dsh1024 && dsh1024 plugin --profile <profile> add dsh-finops-suite
   ```

   No build step — pure ESM; `src/` and `samples/` are the shipped content.

2. **Assemble** (already done by default): the bundle applies `cordis.patch.yml`, inserting the four member rows into the profile:

   ```yaml
   - insert:
       - id: dsh-einvoice
         name: dsh-einvoice
       - id: dsh-bankrec
         name: dsh-bankrec
       - id: dsh-ap-three-way
         name: dsh-ap-three-way
       - id: dsh-travel-recon
         name: dsh-travel-recon
   ```

   The suite has no configuration keys; each member's configuration lives in its own README.

3. **Verify it took effect**:

   ```sh
   dsh --profile <profile> --dump-config | grep dsh-finops-suite
   node samples/quickstart/run.mjs
   ```

   Real output (run on 2026-11-05, member-resolution section):

   ```text
   dsh-finops-suite quickstart (offline)
   suite:    dsh-finops-suite 0.1.0-alpha.11
   profile:  finops-demo (synthetic, 4/4 rows enabled)
   members:  4/4 resolved
     dsh-einvoice         0.2.0-alpha.11   [manifest pin]    profile=enabled
     dsh-bankrec          0.1.0-alpha.16   [manifest pin]    profile=enabled
     dsh-ap-three-way     0.1.0-alpha.11   [manifest pin]    profile=enabled
     dsh-travel-recon     0.1.0-alpha.13   [manifest pin]    profile=enabled
   network:  false (no fetch, no registry call)
   ```

   The golden file still records `0.1.0-alpha.9`, so `--check` currently reports a golden mismatch at the end; member resolution itself is 4/4. See "Known limitations".

**Uninstall**: `dsh plugin --profile <profile> remove dsh-finops-suite` (or remove the row from the profile patch). Removing the suite removes only the suite row; the member packages stay installed. Remove them individually if you no longer need them. See [SUITE.md](SUITE.md).

## Core capabilities

- **One command installs the set** — a single `dsh plugin add` installs all four members, so you do not track four package names and versions separately.
- **Versions locked together** — member versions are pinned in `package.json#dependencies`; an installed member at any other version raises `E_SUITE_VERSION_MISMATCH` instead of silently mixing versions. Upgrade the suite, not an individual member.
- **Member-row reconciliation** — `cordis.patch.yml` and `dependencies` are checked in both directions: a missing row, an extra row, a duplicate id, or an `id`/`name` mismatch raises `E_SUITE_PATCH_MISMATCH`; a missing or malformed manifest raises `E_SUITE_MANIFEST_MISSING`.
- **Offline self-check** — `samples/quickstart/run.mjs` reads three files and prints members, pins and resolution sources; `--json` gives machine-readable output, `--check` compares it with the golden file. Zero network, zero writes.
- **No tool surface** — it registers no tools, commands, slots, HTTP routes or service keys, and only inserts four member rows; members stay independent and can be installed or removed on their own.
- **Reproducible evidence** — `ACCEPTANCE.csv` records the public acceptance rows (`counted` marks whether a row counts), `screenshots.json` records the screenshot command, time and SHA-256, and `node scripts/acceptance.mjs` rebuilds the rows.

## Members & versions

The suite only installs these members; it has no tool surface of its own. Versions are pinned in `dependencies`.

| Member | Pinned version |
|---|---:|
| `dsh-einvoice` | `0.2.0-alpha.11` |
| `dsh-bankrec` | `0.1.0-alpha.16` |
| `dsh-ap-three-way` | `0.1.0-alpha.11` |
| `dsh-travel-recon` | `0.1.0-alpha.13` |

Current suite version: `0.1.0-alpha.11` (matches `package.json`).

## Example

Paste this into DSH:

> Install the four finance-ops packages (e-invoicing, bank reconciliation, three-way match and travel reconciliation), confirm all four member packages resolve, and list each version.

Then run the bundled sample from the package directory (offline, no dependency install needed):

```sh
node samples/quickstart/run.mjs
```

The real output is in step 3 of "Three-step setup". The screenshot is the real terminal output of the same command captured on 2026-11-02 (suite version was `0.1.0-alpha.9` then; member versions are the same as now):

![dsh-finops-suite quickstart real terminal output](docs/assets/quickstart.png)

Screenshot metadata (command, time, output SHA-256) is in `screenshots.json`.

## Configuration

The suite is an install-only bundle: **no Config schema and no runtime keys**. Only the assembly surface and the install target are adjustable:

| Adjustable | Where | Current value | Notes |
|---|---|---|---|
| Member set | `cordis.patch.yml` | `dsh-einvoice`, `dsh-bankrec`, `dsh-ap-three-way`, `dsh-travel-recon` | One `id` + `name` row per member; must match `dependencies` exactly |
| Member versions | `package.json#dependencies` | `0.2.0-alpha.11`, `0.1.0-alpha.16`, `0.1.0-alpha.11`, `0.1.0-alpha.13` | Exact pins; upgrading one member raises `E_SUITE_VERSION_MISMATCH` |
| Install target | `dsh plugin --profile <profile>` | your choice | The suite installs into the named profile only |
| Demo metadata | `package.json#dsh.demo` | `sample` / `prompt` / `expect` / `screenshot` | Declares the offline sample, prompt and evidence paths |

Each member's configuration (invoices, statements, three-way rows, travel claims) lives in the member's README; the suite neither reads nor rewrites it, and does not overwrite member config rows.

<details>
<summary>Full assembly file (cordis.patch.yml)</summary>

```yaml
- insert:
    - id: dsh-einvoice
      name: dsh-einvoice
    - id: dsh-bankrec
      name: dsh-bankrec
    - id: dsh-ap-three-way
      name: dsh-ap-three-way
    - id: dsh-travel-recon
      name: dsh-travel-recon
```

</details>

<details>
<summary>Install channels compared</summary>

| Channel | Command | Use when |
|---|---|---|
| npm (recommended) | `dsh plugin --profile <profile> add dsh-finops-suite` | Normal install from a published release |
| git | `dsh plugin --profile <profile> add github:PerryLink/dsh-finops-suite` | Tracking latest main |
| tarball | `pnpm pack`, then `dsh plugin --profile <profile> add ./dsh-finops-suite-<version>.tgz` | Offline or pinned artifact |
| 1024 store | `npm i -g dsh1024`, then `dsh1024 plugin --profile <profile> add dsh-finops-suite` | Installing through the 1024 channel |

</details>

## FAQ

<details>
<summary>The install fails, or a member is missing afterward. What now?</summary>

Run `node samples/quickstart/run.mjs` first. If the two member lists disagree it raises `E_SUITE_PATCH_MISMATCH`; align `cordis.patch.yml` with `dependencies` as described in [TROUBLESHOOTING.md](TROUBLESHOOTING.md), then reinstall. A missing manifest or an incomplete tarball raises `E_SUITE_MANIFEST_MISSING`; rerun from the package root or reinstall.

</details>

<details>
<summary>The version does not match the suite declaration. Why?</summary>

The suite pins exact member versions and promises one fixed set. Upgrading one member alone, or leaving an old version in `node_modules`, raises `E_SUITE_VERSION_MISMATCH`. Remove `node_modules` in that profile and reinstall the suite; if you truly need a newer member, wait for a suite release that pins it — do not upgrade the member alone.

</details>

<details>
<summary>Can the suite process my invoices or bank statements?</summary>

No. The suite only installs members and has no tool surface of its own; e-invoicing, bank reconciliation, three-way match and travel reconciliation run through the member packages' tools. The bundled sample uses a synthetic profile, reads no real documents and produces no business result.

</details>

<details>
<summary>Does uninstalling the suite remove the members?</summary>

No. Removing the suite removes only its row; member packages stay installed until you remove them individually. Members are independent Cordis rows and can also be installed without the suite.

</details>

<details>
<summary>Where is data stored? Does it go online or upload anything?</summary>

The install reads no business documents; the bundled sample reads only three files: `samples/quickstart/input/profile.json`, `cordis.patch.yml` and `package.json`. It writes no files, uses no network, uploads nothing and calls no model. The only network-touching piece is the developer-side `scripts/check.mjs` (it queries the registry to confirm member versions exist), which does not run at install or runtime.

</details>

## Permissions & data

- Read: `samples/quickstart/input/profile.json`, `cordis.patch.yml`, `package.json`; no other directory
- Write: none (R0 — terminal output only; no `$DSH_HOME` writes, source files untouched)
- Network: no
- External systems: none
- The repository contains only public/synthetic fixtures (`samples/quickstart/`); `ACCEPTANCE.csv` records the public checks, with the `counted` column marking whether each row counts (currently only the quickstart golden row is `true`).
- Public/synthetic fixtures only; no customer data and no customer evidence.
- Alpha/partial; not counted, no GA or production-readiness claim.

## Security boundaries

- **Installs only; processes no content.** The suite has no tool surface, no commands, and registers no slot or HTTP route; invoices, statements, match rows and travel claims stay in the member packages and your local environment.
- **Public/synthetic samples.** The repository contains only public or synthetic fixtures; no customer data, customer documents or customer evidence, and no production-readiness claim.
- **Fails closed.** A missing manifest, a patch/dependency mismatch, or member version drift fails loudly with an explicit `E_` code at load/self-check time — never a silent downgrade or a mixed install.
- **Never rewrites member config.** The bundle patch only `insert`s its four rows; it does not overwrite the `config` of built-in or member rows.
- **Least privilege.** The install writes no `$DSH_HOME` and touches no source files; each member tool's permission and data boundaries are documented in its own repository and `ACCEPTANCE`.

## Known limitations

- **Install-only.** The suite has no tool surface of its own; it cannot process invoices, statements, three-way rows or travel claims, and provides no OCR, direct bank feed or ERP integration. Those capabilities (where they exist) belong to the members.
- **Alpha / partial / not counted.** No GA or production-readiness claim; public acceptance rows marked `counted=false` do not count as formal acceptance.
- **Versions are decided by suite releases.** With members pinned, upgrading a member alone fails; changing a member version requires a new suite release.
- **The sample golden still records `0.1.0-alpha.9`.** `samples/quickstart/expected/result.json` was written for an older suite, while the current package is `0.1.0-alpha.11`; `node samples/quickstart/run.mjs --check` and the tests that depend on it report a golden mismatch. `run.mjs --json` still resolves 4/4; regenerating the golden file restores the check. This does not affect installation or member resolution.
- **No configuration keys.** Adjustable member settings live in each member's README; the suite adds no switches.

## Interoperability with other DSH plugins

- **No shared service, port or storage domain.** The suite and its members occupy no shared service, port or storage domain; members are independent Cordis rows.
- **No tool/command/slot/route registration.** The suite registers no tools, commands, client slots or `webServer` prefixes, so there are no name clashes or slot contention.
- **Insert only, never overwrite.** The bundle patch only `insert`s member rows; it does not overwrite the `config` of built-in or member rows.
- **Individually installable.** Members can be installed and removed without the suite; uninstalling the suite does not take them away.
- **Channel-independent.** npm, git, tarball and the 1024 store all produce the same member set and versions.

## Compatibility

| Surface | Status |
|---|---|
| Harness | `dsh >=0.2.1-rc.3 <0.3.0` |
| Node | `>=24.9.0 <25` |
| Platforms | All DSH-capable platforms; local files only |
| Data | No network, no model call, no upload |

## Ecosystem & quality

- [Domain index](https://perrylink.github.io/dsh-plugins/) (package catalog and install entry points)
- [Checker family](https://perrylink.github.io/zh/checkers/) (checker plugin overview)
- [Mainline family](https://github.com/PerryLink/dsh-kit) (install specs and family index)
- [Scenario article](https://perrylink.github.io/dsh-plugins/articles/finops-suite.html) (finance-ops suite walkthrough)
- [Gitee aggregate mirror](https://gitee.com/perrylink/dsh-plugins) (GitHub is canonical)
- [dshfind plugin page](https://dshfind.com/plugins/PerryLink/dsh-finops-suite) (installs and ranking)
- [DSH Market](https://dsh.market/) (listed)
- **1024 store channel**: `npm i -g dsh1024`, then `dsh1024 plugin --profile <profile> add dsh-finops-suite` (counts toward the [deepseek1024.com](https://deepseek1024.com) install ranking)
- **Evidence files**: [`ACCEPTANCE.csv`](ACCEPTANCE.csv) · [`screenshots.json`](screenshots.json) · [`samples/quickstart/expected/result.json`](samples/quickstart/expected/result.json)

## Development

```sh
pnpm quickstart        # node samples/quickstart/run.mjs
pnpm test              # node --test test/suite.test.mjs
pnpm gate              # node scripts/gate.mjs (offline release gate)
pnpm check             # node scripts/check.mjs (registry lookup, CI only)
```

No build step: the shipped content is `src/` + `samples/` + `cordis.patch.yml`.

| Path | Purpose |
|---|---|
| `src/members.mjs` | The only runtime code: reads `package.json` + `cordis.patch.yml`, validates members, resolves versions |
| `samples/quickstart/` | Offline sample: `input/profile.json`, `expected/result.json`, `run.mjs` |
| `test/suite.test.mjs` | `node --test`: manifest, sample, golden, error branches |
| `scripts/gate.mjs` | Release gate: manifest, sample, doc blocks, evidence, golden, tests |
| `scripts/check.mjs` | Registry install smoke (CI only; the one networked script) |
| `scripts/acceptance.mjs` | Rebuilds `ACCEPTANCE.csv` from real local checks |
| `scripts/gen-readme-assets.py` | Generates the README figures (Python + Pillow) |
| `docs/assets/` | Flow diagram and the quickstart screenshot |
| `cordis.patch.yml` | Member assembly surface (four `insert` rows) |

Figures are generated by [`scripts/gen-readme-assets.py`](scripts/gen-readme-assets.py): `python scripts/gen-readme-assets.py` writes `docs/assets/dsh-finops-suite-flow-{light,dark}.svg` (vector, shared by all five languages) and leaves the legacy single-skin `dsh-finops-suite-flow.svg` untouched. The script is safe to re-run.

Five-language READMEs: `README.md` is the Chinese source; `README.en.md`, `README.es.md`, `README.pt.md` and `README.hi.md` follow it.

Current version: `0.1.0-alpha.11` (matches `package.json`). Historical local verification (2026-11-02): `node --test test/suite.test.mjs` passed 8 tests and `node samples/quickstart/run.mjs --check` matched the golden file of that time; the current golden lag is described in "Known limitations".

Topics: `dsh`, `dsh-plugin`, `deepseek-harness`, `deepseek`, `cordis`, `dsh-bundle`, `perrylink`, `suite`, `finance`

## Family & thanks

This project is a member of the [PerryLink](https://github.com/PerryLink) DeepSeek Harness plugin family (all Apache-2.0). If this suite helps you, **give it a star** — it unlocks nothing, but it makes the next person more likely to find it.

- [dsh-einvoice](https://github.com/PerryLink/dsh-einvoice) — the e-invoicing member.
- [dsh-bankrec](https://github.com/PerryLink/dsh-bankrec) — the bank reconciliation member.
- [dsh-ap-three-way](https://github.com/PerryLink/dsh-ap-three-way) — the three-way match member.
- [dsh-travel-recon](https://github.com/PerryLink/dsh-travel-recon) — the travel reconciliation member.
- [@PerryLink](https://github.com/PerryLink) — creator and maintainer: suite contract, version pinning, offline quickstart, acceptance rows and five-language docs.

<details>
<summary>DSH domain plugin family (15 packages + 2 suites)</summary>

| Package | npm |
|---|---|
| **[dsh-einvoice](https://github.com/PerryLink/dsh-einvoice)** | [npm](https://www.npmjs.com/package/dsh-einvoice) |
| **[dsh-docx-redline](https://github.com/PerryLink/dsh-docx-redline)** | [npm](https://www.npmjs.com/package/dsh-docx-redline) |
| **[dsh-policy-ledger](https://github.com/PerryLink/dsh-policy-ledger)** | [npm](https://www.npmjs.com/package/dsh-policy-ledger) |
| **[dsh-ghg](https://github.com/PerryLink/dsh-ghg)** | [npm](https://www.npmjs.com/package/dsh-ghg) |
| **[dsh-bankrec](https://github.com/PerryLink/dsh-bankrec)** | [npm](https://www.npmjs.com/package/dsh-bankrec) |
| **[dsh-ap-three-way](https://github.com/PerryLink/dsh-ap-three-way)** | [npm](https://www.npmjs.com/package/dsh-ap-three-way) |
| **[dsh-ifc-qto](https://github.com/PerryLink/dsh-ifc-qto)** | [npm](https://www.npmjs.com/package/dsh-ifc-qto) |
| **[dsh-qms-capa](https://github.com/PerryLink/dsh-qms-capa)** | [npm](https://www.npmjs.com/package/dsh-qms-capa) |
| **[dsh-legal-intake](https://github.com/PerryLink/dsh-legal-intake)** | [npm](https://www.npmjs.com/package/dsh-legal-intake) |
| **[dsh-legal-clause](https://github.com/PerryLink/dsh-legal-clause)** | [npm](https://www.npmjs.com/package/dsh-legal-clause) |
| **[dsh-freight-audit](https://github.com/PerryLink/dsh-freight-audit)** | [npm](https://www.npmjs.com/package/dsh-freight-audit) |
| **[dsh-hs-candidate](https://github.com/PerryLink/dsh-hs-candidate)** | [npm](https://www.npmjs.com/package/dsh-hs-candidate) |
| **[dsh-travel-recon](https://github.com/PerryLink/dsh-travel-recon)** | [npm](https://www.npmjs.com/package/dsh-travel-recon) |
| **[dsh-pim-lint](https://github.com/PerryLink/dsh-pim-lint)** | [npm](https://www.npmjs.com/package/dsh-pim-lint) |
| **[dsh-eval-pack](https://github.com/PerryLink/dsh-eval-pack)** | [npm](https://www.npmjs.com/package/dsh-eval-pack) |
| **[dsh-finops-suite](https://github.com/PerryLink/dsh-finops-suite)** | [npm](https://www.npmjs.com/package/dsh-finops-suite) |
| **[dsh-contract-suite](https://github.com/PerryLink/dsh-contract-suite)** | [npm](https://www.npmjs.com/package/dsh-contract-suite) |

</details>

<details>
<summary>Mainline family — 87 current install specs</summary>

| Package | npm |
|---|---|
| **[dsh-aqua-input-check](https://github.com/PerryLink/dsh-aqua-input-check)** | [npm](https://www.npmjs.com/package/dsh-aqua-input-check) |
| **[dsh-archive-check](https://github.com/PerryLink/dsh-archive-check)** | [npm](https://www.npmjs.com/package/dsh-archive-check) |
| **[dsh-bid-ca-precheck](https://github.com/PerryLink/dsh-bid-ca-precheck)** | [npm](https://www.npmjs.com/package/dsh-bid-ca-precheck) |
| **[dsh-bid-qual-check](https://github.com/PerryLink/dsh-bid-qual-check)** | [npm](https://www.npmjs.com/package/dsh-bid-qual-check) |
| **[dsh-contract-stance](https://github.com/PerryLink/dsh-contract-stance)** | [npm](https://www.npmjs.com/package/dsh-contract-stance) |
| **[dsh-customs-doc-check](https://github.com/PerryLink/dsh-customs-doc-check)** | [npm](https://www.npmjs.com/package/dsh-customs-doc-check) |
| **[dsh-demurrage-ledger](https://github.com/PerryLink/dsh-demurrage-ledger)** | [npm](https://www.npmjs.com/package/dsh-demurrage-ledger) |
| **[dsh-drill-script-check](https://github.com/PerryLink/dsh-drill-script-check)** | [npm](https://www.npmjs.com/package/dsh-drill-script-check) |
| **[dsh-eia-guide-check](https://github.com/PerryLink/dsh-eia-guide-check)** | [npm](https://www.npmjs.com/package/dsh-eia-guide-check) |
| **[dsh-emergency-plan](https://github.com/PerryLink/dsh-emergency-plan)** | [npm](https://www.npmjs.com/package/dsh-emergency-plan) |
| **[dsh-essay-rubric-check](https://github.com/PerryLink/dsh-essay-rubric-check)** | [npm](https://www.npmjs.com/package/dsh-essay-rubric-check) |
| **[dsh-evidence-check](https://github.com/PerryLink/dsh-evidence-check)** | [npm](https://www.npmjs.com/package/dsh-evidence-check) |
| **[dsh-export-ctl-check](https://github.com/PerryLink/dsh-export-ctl-check)** | [npm](https://www.npmjs.com/package/dsh-export-ctl-check) |
| **[dsh-fmea-table-check](https://github.com/PerryLink/dsh-fmea-table-check)** | [npm](https://www.npmjs.com/package/dsh-fmea-table-check) |
| **[dsh-forecast-penalty](https://github.com/PerryLink/dsh-forecast-penalty)** | [npm](https://www.npmjs.com/package/dsh-forecast-penalty) |
| **[dsh-gongwen-flow-check](https://github.com/PerryLink/dsh-gongwen-flow-check)** | [npm](https://www.npmjs.com/package/dsh-gongwen-flow-check) |
| **[dsh-gongwen-word-check](https://github.com/PerryLink/dsh-gongwen-word-check)** | [npm](https://www.npmjs.com/package/dsh-gongwen-word-check) |
| **[dsh-guard-plan-qc](https://github.com/PerryLink/dsh-guard-plan-qc)** | [npm](https://www.npmjs.com/package/dsh-guard-plan-qc) |
| **[dsh-hazchem-check](https://github.com/PerryLink/dsh-hazchem-check)** | [npm](https://www.npmjs.com/package/dsh-hazchem-check) |
| **[dsh-hazplan-check](https://github.com/PerryLink/dsh-hazplan-check)** | [npm](https://www.npmjs.com/package/dsh-hazplan-check) |
| **[dsh-hidden-risk-map](https://github.com/PerryLink/dsh-hidden-risk-map)** | [npm](https://www.npmjs.com/package/dsh-hidden-risk-map) |
| **[dsh-hs-classify](https://github.com/PerryLink/dsh-hs-classify)** | [npm](https://www.npmjs.com/package/dsh-hs-classify) |
| **[dsh-icd-rule-check](https://github.com/PerryLink/dsh-icd-rule-check)** | [npm](https://www.npmjs.com/package/dsh-icd-rule-check) |
| **[dsh-lawcite-adapter](https://github.com/PerryLink/dsh-lawcite-adapter)** | [npm](https://www.npmjs.com/package/dsh-lawcite-adapter) |
| **[dsh-lc-doc-check](https://github.com/PerryLink/dsh-lc-doc-check)** | [npm](https://www.npmjs.com/package/dsh-lc-doc-check) |
| **[dsh-learning-gap-check](https://github.com/PerryLink/dsh-learning-gap-check)** | [npm](https://www.npmjs.com/package/dsh-learning-gap-check) |
| **[dsh-medrec-qc](https://github.com/PerryLink/dsh-medrec-qc)** | [npm](https://www.npmjs.com/package/dsh-medrec-qc) |
| **[dsh-nsfc-form-check](https://github.com/PerryLink/dsh-nsfc-form-check)** | [npm](https://www.npmjs.com/package/dsh-nsfc-form-check) |
| **[dsh-nurse-record-check](https://github.com/PerryLink/dsh-nurse-record-check)** | [npm](https://www.npmjs.com/package/dsh-nurse-record-check) |
| **[dsh-origin-rvc-check](https://github.com/PerryLink/dsh-origin-rvc-check)** | [npm](https://www.npmjs.com/package/dsh-origin-rvc-check) |
| **[dsh-ota-review-check](https://github.com/PerryLink/dsh-ota-review-check)** | [npm](https://www.npmjs.com/package/dsh-ota-review-check) |
| **[dsh-paper-doc-adapter](https://github.com/PerryLink/dsh-paper-doc-adapter)** | [npm](https://www.npmjs.com/package/dsh-paper-doc-adapter) |
| **[dsh-permit-report-check](https://github.com/PerryLink/dsh-permit-report-check)** | [npm](https://www.npmjs.com/package/dsh-permit-report-check) |
| **[dsh-pipeline-check](https://github.com/PerryLink/dsh-pipeline-check)** | [npm](https://www.npmjs.com/package/dsh-pipeline-check) |
| **[dsh-pleading-draft](https://github.com/PerryLink/dsh-pleading-draft)** | [npm](https://www.npmjs.com/package/dsh-pleading-draft) |
| **[dsh-policy-brief-draft](https://github.com/PerryLink/dsh-policy-brief-draft)** | [npm](https://www.npmjs.com/package/dsh-policy-brief-draft) |
| **[dsh-power-loss-split](https://github.com/PerryLink/dsh-power-loss-split)** | [npm](https://www.npmjs.com/package/dsh-power-loss-split) |
| **[dsh-power-ticket-check](https://github.com/PerryLink/dsh-power-ticket-check)** | [npm](https://www.npmjs.com/package/dsh-power-ticket-check) |
| **[dsh-ppap-check](https://github.com/PerryLink/dsh-ppap-check)** | [npm](https://www.npmjs.com/package/dsh-ppap-check) |
| **[dsh-protest-deadline](https://github.com/PerryLink/dsh-protest-deadline)** | [npm](https://www.npmjs.com/package/dsh-protest-deadline) |
| **[dsh-railway-window](https://github.com/PerryLink/dsh-railway-window)** | [npm](https://www.npmjs.com/package/dsh-railway-window) |
| **[dsh-repair-order-qc](https://github.com/PerryLink/dsh-repair-order-qc)** | [npm](https://www.npmjs.com/package/dsh-repair-order-qc) |
| **[dsh-review-reply-check](https://github.com/PerryLink/dsh-review-reply-check)** | [npm](https://www.npmjs.com/package/dsh-review-reply-check) |
| **[dsh-rulefile-check](https://github.com/PerryLink/dsh-rulefile-check)** | [npm](https://www.npmjs.com/package/dsh-rulefile-check) |
| **[dsh-safety-brief-check](https://github.com/PerryLink/dsh-safety-brief-check)** | [npm](https://www.npmjs.com/package/dsh-safety-brief-check) |
| **[dsh-site-log-check](https://github.com/PerryLink/dsh-site-log-check)** | [npm](https://www.npmjs.com/package/dsh-site-log-check) |
| **[dsh-soe-decision-check](https://github.com/PerryLink/dsh-soe-decision-check)** | [npm](https://www.npmjs.com/package/dsh-soe-decision-check) |
| **[dsh-soilwater-check](https://github.com/PerryLink/dsh-soilwater-check)** | [npm](https://www.npmjs.com/package/dsh-soilwater-check) |
| **[dsh-sop-sync-check](https://github.com/PerryLink/dsh-sop-sync-check)** | [npm](https://www.npmjs.com/package/dsh-sop-sync-check) |
| **[dsh-spc-gbt-adapter](https://github.com/PerryLink/dsh-spc-gbt-adapter)** | [npm](https://www.npmjs.com/package/dsh-spc-gbt-adapter) |
| **[dsh-tender-extract](https://github.com/PerryLink/dsh-tender-extract)** | [npm](https://www.npmjs.com/package/dsh-tender-extract) |
| **[dsh-tender-matrix](https://github.com/PerryLink/dsh-tender-matrix)** | [npm](https://www.npmjs.com/package/dsh-tender-matrix) |
| **[dsh-warranty-calc](https://github.com/PerryLink/dsh-warranty-calc)** | [npm](https://www.npmjs.com/package/dsh-warranty-calc) |
| **[dsh-auto-review](https://github.com/PerryLink/dsh-auto-review)** | [npm](https://www.npmjs.com/package/dsh-auto-review) |
| **[dsh-autotier](https://github.com/PerryLink/dsh-autotier)** | [npm](https://www.npmjs.com/package/dsh-autotier) |
| **[dsh-budget](https://github.com/PerryLink/dsh-budget)** | [npm](https://www.npmjs.com/package/dsh-budget) |
| **[dsh-cert-mcp](https://github.com/PerryLink/dsh-cert-mcp)** | [npm](https://www.npmjs.com/package/dsh-cert-mcp) |
| **[dsh-checkpoint-rewind](https://github.com/PerryLink/dsh-checkpoint-rewind)** | [npm](https://www.npmjs.com/package/dsh-checkpoint-rewind) |
| **[dsh-claude-move](https://github.com/PerryLink/dsh-claude-move)** | [npm](https://www.npmjs.com/package/dsh-claude-move) |
| **[dsh-click](https://github.com/PerryLink/dsh-click)** | [npm](https://www.npmjs.com/package/dsh-click) |
| **[dsh-composer-history](https://github.com/PerryLink/dsh-composer-history)** | [npm](https://www.npmjs.com/package/dsh-composer-history) |
| **[dsh-data-quality](https://github.com/PerryLink/dsh-data-quality)** | [npm](https://www.npmjs.com/package/dsh-data-quality) |
| **[dsh-defend](https://github.com/PerryLink/dsh-defend)** | [npm](https://www.npmjs.com/package/dsh-defend) |
| **[dsh-doublecheck](https://github.com/PerryLink/dsh-doublecheck)** | [npm](https://www.npmjs.com/package/dsh-doublecheck) |
| **[dsh-draw](https://github.com/PerryLink/dsh-draw)** | [npm](https://www.npmjs.com/package/dsh-draw) |
| **[dsh-fast](https://github.com/PerryLink/dsh-fast)** | [npm](https://www.npmjs.com/package/dsh-fast) |
| **[dsh-fund-research](https://github.com/PerryLink/dsh-fund-research)** | [npm](https://www.npmjs.com/package/dsh-fund-research) |
| **[dsh-industry-research](https://github.com/PerryLink/dsh-industry-research)** | [npm](https://www.npmjs.com/package/dsh-industry-research) |
| **[dsh-laya](https://github.com/PerryLink/dsh-laya)** | [npm](https://www.npmjs.com/package/dsh-laya) |
| **[dsh-library](https://github.com/PerryLink/dsh-library)** | [npm](https://www.npmjs.com/package/dsh-library) |
| **[dsh-local-ai](https://github.com/PerryLink/dsh-local-ai)** | [npm](https://www.npmjs.com/package/dsh-local-ai) |
| **[dsh-lsp-actions](https://github.com/PerryLink/dsh-lsp-actions)** | [npm](https://www.npmjs.com/package/dsh-lsp-actions) |
| **[dsh-mask](https://github.com/PerryLink/dsh-mask)** | [npm](https://www.npmjs.com/package/dsh-mask) |
| **[dsh-mcp-panel](https://github.com/PerryLink/dsh-mcp-panel)** | [npm](https://www.npmjs.com/package/dsh-mcp-panel) |
| **[dsh-memento](https://github.com/PerryLink/dsh-memento)** | [npm](https://www.npmjs.com/package/dsh-memento) |
| **[dsh-observe](https://github.com/PerryLink/dsh-observe)** | [npm](https://www.npmjs.com/package/dsh-observe) |
| **[dsh-output-styles](https://github.com/PerryLink/dsh-output-styles)** | [npm](https://www.npmjs.com/package/dsh-output-styles) |
| **[dsh-permission-rules](https://github.com/PerryLink/dsh-permission-rules)** | [npm](https://www.npmjs.com/package/dsh-permission-rules) |
| **[dsh-plugin-guide](https://github.com/PerryLink/dsh-plugin-guide)** | [npm](https://www.npmjs.com/package/dsh-plugin-guide) |
| **[dsh-plugin-upgrade](https://github.com/PerryLink/dsh-plugin-upgrade)** | [npm](https://www.npmjs.com/package/dsh-plugin-upgrade) |
| **[dsh-reach](https://github.com/PerryLink/dsh-reach)** | [npm](https://www.npmjs.com/package/dsh-reach) |
| **[dsh-research-report](https://github.com/PerryLink/dsh-research-report)** | [npm](https://www.npmjs.com/package/dsh-research-report) |
| **[dsh-score](https://github.com/PerryLink/dsh-score)** | [npm](https://www.npmjs.com/package/dsh-score) |
| **[dsh-session-sync](https://github.com/PerryLink/dsh-session-sync)** | [npm](https://www.npmjs.com/package/dsh-session-sync) |
| **[dsh-talk](https://github.com/PerryLink/dsh-talk)** | [npm](https://www.npmjs.com/package/dsh-talk) |
| **[dsh-test-drive](https://github.com/PerryLink/dsh-test-drive)** | [npm](https://www.npmjs.com/package/dsh-test-drive) |
| **[dsh-translate](https://github.com/PerryLink/dsh-translate)** | [npm](https://www.npmjs.com/package/dsh-translate) |

</details>

## License

[LICENSE](LICENSE) (Apache License 2.0) © 2026 dsh-finops-suite contributors

<p align="center"><sub>Apache-2.0 · Community suite, not affiliated with DeepSeek.</sub></p>
