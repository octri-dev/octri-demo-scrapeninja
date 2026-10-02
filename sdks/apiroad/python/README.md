# ScrapeNinja APIRoad — unofficial Octri demo Python SDK

> **Unofficial Octri evaluation demo.** Not endorsed by ScrapeNinja. Use the local files in this repository; this demo is not published on npm or PyPI. [Runnable offline examples](../../../README.md) · [Validation and local repairs](../../../evidence/VALIDATION.md).


Unofficial Octri demonstration. APIRoad-specific derivative of https://scrapeninja.net/openapi.yaml. Authentication header corrected to X-Apiroad-Key; API behavior and response schemas remain unchanged. Not endorsed by ScrapeNinja. This is a high-performance web scraping API with smart retries and proxy rotation, with multiple proxy geos, and with two scraping engines under the hood: high performance engine with Chrome browser TLS fingerprint, but without JavaScript execution and real browser overhead; and real Chrome browser engine, with JS and CSS evaluation and screenshots, when high performance engine features are not enough.

ScrapeNinja API is available on two marketplace platforms: RapidAPI and APIRoad.
To get your API key, go to https://rapidapi.com/restyler/api/scrapeninja or https://apiroad.net/marketplace/apis/scrapeninja
If you prefer to use APIRoad, you will need to replace API key name from `X-RapidAPI-Key` to `X-Apiroad-Key`.

> Package `octri-demo-scrapeninja-apiroad` · Version `1.0.0` · 3 operations

## Installation

From this SDK directory, with a Python virtual environment active:

```sh
python -m pip install .
```

## Quickstart

Every generated operation requires input. Start from the typed signature for the operation you need; required path and body values are intentionally not replaced with unsafe placeholders here.

## Authentication

Keep credentials outside source control. The quickstart reads them from the environment and the client applies them to every request.

| Scheme | ClientAuthConfig field | Sent as |
| --- | --- | --- |
| ApiKeyAuth | `api_key_auth` | `X-Apiroad-Key` in header |

## Client behavior

- Base URL: `https://scrapeninja.apiroad.net`.
- Transport: httpx.
- Timeout: 30,000 ms per attempt.
- Retries: up to 3 attempts for status codes `408`, `425`, `429`, `500`, `502`, `503`, `504`, with 500–8,000 ms backoff.
- Idempotency: enabled for `POST`, `PATCH` using `Idempotency-Key`.
- Error telemetry: off. This build has no reporting endpoint and sends no error reports.

High-level operation methods return the typed response body directly. The low-level request layer returns an `SdkResponse<T>` envelope containing data, status, headers, request ID, latency, and attempt count.

## Errors and response metadata

All failure paths use a small, predictable hierarchy:

| Error | Meaning |
| --- | --- |
| `SdkValidationError` | A request argument failed an OpenAPI constraint before network I/O. |
| `SdkHttpError` | The server returned a non-2xx response. |
| `SdkNetworkError` | DNS, connection, TLS, or socket failure. |
| `SdkTimeoutError` | The configured per-attempt timeout elapsed. |

HTTP errors expose `status_code`, the response body and headers, plus `request_id` when the server supplies one. Preserve the request ID in support logs; it is the fastest way to correlate a failed SDK call with server-side traces.

Common statuses are reported as a subclass of `SdkHttpError`, so a handler can catch only the one it handles: `SdkBadRequestError` (400), `SdkUnauthorizedError` (401), `SdkPermissionDeniedError` (403), `SdkNotFoundError` (404), `SdkConflictError` (409), `SdkUnprocessableEntityError` (422), `SdkRateLimitError` (429), `SdkInternalServerError` (any 5xx). Any other status is reported as `SdkHttpError` itself.

When the API declares a model for an error response, `error.decode_body(ErrorModel)` decodes the body into it, where `ErrorModel` is that model. The raw body stays available on the error.

An operation that declares error models also defines `<Operation>Error` beside it, the union of those models. `error.decode_body(<Operation>Error)` returns whichever model the body fits; narrow it with `isinstance`.

## Project layout and API discovery

- Operation implementations are grouped under `src/sdk/methods/`.
- 4 component models are split by API domain under `src/sdk/types/<domain>.py` or `types/<tag path>/models.py`, re-exported by `sdk.types`.
- Component schemas can choose a nested model folder with `x-octri-sdk-tags: ["Billing/Invoices"]`; the first tag owns the model and `/` creates nesting.
- [`sdk-manifest.json`](sdk-manifest.json) is the language-neutral public API index: operations, request/response modes, model properties, enum values, and generation settings.
- Public barrel/module exports are the compatibility boundary. Import public model names from those exports; internal domain filenames may evolve without changing model names.

<!-- sdk-studio-mock-tests -->
## Local mock-server tests

Generated SDK includes schema-derived, zero-dependency mock server and network
contract suite. Node.js 22.12+ required. Contract probes use authored response
examples only; schema-synthesized routes remain available to the local server.

`./scripts/mock --port 4010` starts server. `./scripts/test` runs the mock contract suite, then native SDK tests. A zero-authored-example contract run succeeds with an explicit zero-test
summary; mismatches in authored examples still fail.
