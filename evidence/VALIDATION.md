# Demo validation — October 2, 2026

**Ready for a technical evaluation demo using the current repository files.** Verification used local mocks and synthetic fixtures. No live API calls, real API keys, or production-compatibility claims.

## Complete SDK checks

| Package | Language | SDK tests | Lint | Format | Types | Package creation |
|---|---|---|---|---|---|---|
| scrapeninja-baseline | python | 7 passed; 0 skipped | Pass | Pass | Pass | Pass |
| scrapeninja-baseline | typescript | 12 passed; 0 skipped | Pass | Pass | Pass | Pass |
| scrapeninja-apiroad | python | 7 passed; 0 skipped | Pass | Pass | Pass | Pass |
| scrapeninja-apiroad | typescript | 12 passed; 0 skipped | Pass | Pass | Pass | Pass |

The SDK suite exercised all 3 operations in each language against local HTTP servers. Mock contract probes reported 16 checks across 3 success response modes per contract run. Generated tests include synthetic errors; they do not establish the live service's behavior.

The original targeted demo also passes in Python and TypeScript. Built wheel and npm archives were installed in fresh environments. Each installed client passed import, a high-level call, authentication-header capture, 401 error/request-ID handling, a 429 retry followed by success, and timeout handling. See `installed-python-results.json` and `installed-typescript-results.json`.

The documented verification command also passed from a fresh clone with a new virtual environment and locked npm installs. See `clean-checkout-results.json`.

## Repairs made after the broader test run

- The public JS-scraping response schema requires `info.screenshot` and `info.pageCookies` without defining their types. Generated fixtures omitted both. The demo fixtures now include `null` placeholders, which are permitted for these undeclared property schemas; Python preserves them as extra fields rather than dropping them. Required-field validation remains enabled. This does not establish the live fields' real types.
- The corrected spec's title contains an em dash. The mock server used it directly as a header value and crashed. The mock header now uses percent-encoding.
- Removed a redundant Python import alias flagged by the linter.
- Fetch transport and contract probes now omit a body for GET/HEAD, resolving lint findings and making that constraint explicit.
- Demo setup correction: our ZIP extraction lost executable permissions. The original Octri ZIPs correctly stored `scripts/test` and `scripts/mock` as mode `0755`; this was not a generator defect. Permissions were restored in Git.
- Demo setup correction: installation instructions now use local files and unofficial distribution names. Generated registry-install instructions assume a published package; these demo packages are unpublished. npm packages are private.
- Dependency lockfiles and a repeatable verification command are included. Formatting was applied to changed source and test files.

The timestamp comparator, mock header encoding, fixture synthesis, redundant import alias, and generated lint failures described above are issues in generated output. Executable permissions and unofficial installation/package names are demo setup corrections. These repairs currently live in the demo repositories; the Octri generator implementation was not changed. The original spec snapshots and original ZIP hashes remain in provenance. Regenerating in Octri may require reapplying these repairs until the generator itself incorporates them. **Use the current repository or demo ZIP when sharing; the earlier CDN ZIPs do not contain these repairs.**

## Reproduce the full checks

Requires Node.js 22.12+ and Python 3.10+. Local verification used Node 24.19.0 and Python 3.14.4 on macOS; GitHub Actions uses Python 3.12 and Node 24 on Ubuntu.

From the repository root:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.txt
.venv/bin/python demos/verify.py
```

The verifier installs locked JavaScript development dependencies, runs all SDK checks and the focused demos, and exits unsuccessfully if any check fails. Dependency setup requires registry access; SDK requests go to mocks only. The [GitHub validation workflow](https://github.com/octri-dev/octri-demo-scrapeninja/actions/workflows/demo-validation.yml) repeats this from a clean checkout.

## Scope of confidence

This supports sending a clearly unofficial, runnable demonstration. It does not certify all API combinations, live authentication, service-specific retry/idempotency rules, latency, or production use. A live integration test with credentials provided by the target team is the next validation step.
