"""Offline transport reproduction: no API credentials or live API requests."""
import asyncio, importlib, json, sys
from pathlib import Path
import httpx
ROOT = Path(__file__).resolve().parents[1]

async def check(variant, package, class_name):
    sys.path.insert(0, str(ROOT / 'sdks' / variant / 'python' / 'src'))
    pkg = importlib.import_module(package)
    client = importlib.import_module(package + '.client')
    seen = {}
    def handler(req):
        seen.update(url=str(req.url), apiroad_header=req.headers.get('X-Apiroad-Key'), rapidapi_header=req.headers.get('X-RapidAPI-Key'))
        ok = seen['apiroad_header'] == 'demo-not-a-secret'
        return httpx.Response(200 if ok else 401, json={'info': {'statusCode':200,'finalUrl':'https://example.com','headers':[]},'body':'<html>mock</html>'} if ok else {'message':'Mock APIRoad expects X-Apiroad-Key'})
    cfg = client.ClientConfig(base_url='https://scrapeninja.apiroad.net',auth=client.ClientAuthConfig(api_key_auth='demo-not-a-secret'),retry=client.RetryConfig(max_attempts=1),idempotency=client.IdempotencyConfig(enabled=False))
    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as http:
        cfg._client = http
        try:
            result = await getattr(pkg, class_name)(cfg).scrape.scrape(url='https://example.com')
            seen['outcome'] = 'accepted by mock'
            assert result.body == '<html>mock</html>'
        except Exception as exc:
            if variant != 'baseline': raise
            assert getattr(exc, 'status', getattr(exc,'status_code',None)) == 401, repr(exc)
            seen['outcome'] = '401 from mock'
    assert seen['url'].startswith('https://scrapeninja.apiroad.net/')
    assert seen['apiroad_header'] == ('demo-not-a-secret' if variant == 'apiroad' else None)
    assert seen['rapidapi_header'] == (None if variant == 'apiroad' else 'demo-not-a-secret')
    return seen

async def main():
    results = {'mode':'offline mock; no live API calls', 'baseline':await check('baseline','scrapeninja_web_scraping_api','ScrapeNinjaWebScraping'), 'apiroad':await check('apiroad','sdk','ScrapeNinjaAPIRoadUnofficialOctriDemo')}
    print(json.dumps(results,indent=2))
asyncio.run(main())
