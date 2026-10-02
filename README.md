# ScrapeNinja: an unofficial Octri SDK demonstration

**An APIRoad-specific authentication example, with generated Python and TypeScript SDKs and offline reproductions.** Created by Octri for evaluation. Not an official ScrapeNinja SDK, not endorsed by ScrapeNinja, and not published to a package registry.

## The observation

[ScrapeNinja's public OpenAPI document](https://scrapeninja.net/openapi.yaml) lists `https://scrapeninja.apiroad.net` as its first server. Its prose tells APIRoad users to replace `X-RapidAPI-Key` with `X-Apiroad-Key`, but its machine-readable `ApiKeyAuth` scheme still specifies `X-RapidAPI-Key`.

The SDKs generated directly from that spec send `X-RapidAPI-Key` when configured with the spec's APIRoad server. A separate APIRoad-only derivative declares `X-Apiroad-Key`. Regenerating in Octri produces clients that send that header instead, without editing generated source code.

| Client generated from | Header captured in Python and TypeScript | Offline mock result |
|---|---|---|
| Upstream spec | `X-RapidAPI-Key` | 401 |
| APIRoad-specific derivative | `X-Apiroad-Key` | 200; HTML response parsed |

**These statuses come from a mock enforcing the documented APIRoad header requirement. They are not live ScrapeNinja responses.** No real API keys were used; live service behavior, latency, retries, and production readiness are unverified. We do not know whether APIRoad also accepts the alternate header. The concrete finding is the inconsistency between prose and the declared security scheme.

## Try it locally

Requires Python 3.10+ and Node.js 20+.

```sh
git clone https://github.com/octri-dev/octri-demo-scrapeninja.git
cd octri-demo-scrapeninja
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python demos/check-python.py
npm ci --ignore-scripts
npm run check:typescript
```

The TypeScript command compiles both complete generated SDKs, then intercepts their HTTP requests. The Python command injects an `httpx.MockTransport` into each generated client. Both commands make zero live API calls and use the placeholder `demo-not-a-secret`.

Client classes in these builds require the base URL in their constructor config. The examples set it explicitly; do the same when integrating. These are local demos: package metadata retains generator output and must be reviewed and renamed before any registry release.

## What is included

- [`specs/upstream.json`](specs/upstream.json): JSON conversion of the public YAML, captured October 2, 2026.
- [`specs/apiroad-demo.json`](specs/apiroad-demo.json): APIRoad-only derivative. Changes are the security header, server list, and clearly unofficial title/version/description. Endpoint and response schemas are unchanged.
- [`sdks/baseline`](sdks/baseline): unedited Octri Python and TypeScript output from the upstream spec.
- [`sdks/apiroad`](sdks/apiroad): unedited regenerated output from the derivative.
- [`evidence`](evidence): recorded results and source provenance.

The derivative intentionally removes RapidAPI as a server. A long-term upstream solution should model the two authentication variants clearly; changing the header globally would be inappropriate for RapidAPI users.

The public spec also declares only successful responses for these three operations. Ask the team for its actual error contract before adding error schemas; this demo does not invent them.

## A useful conversation with the team

“Your spec has a small inconsistency between the default APIRoad server and its authentication scheme. I prepared an APIRoad-specific Python/TypeScript demo and a before/after test. Is this a real friction point for customers, and would maintaining both gateway variants from one source be useful?”

A good pilot would cover a team-approved auth model, one customer-selected language, one real integration, and regeneration after an API change. The goal is evidence that this saves the team maintenance work.

[Octri](https://octri.dev) · [Public source API](https://scrapeninja.net) · [Provenance](evidence/provenance.json)
