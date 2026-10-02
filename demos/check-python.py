"""Exercise the generated APIRoad client with an offline HTTP transport."""
import asyncio
import json
import sys
from pathlib import Path
import httpx

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'sdks/apiroad/python/src'))
from sdk import ScrapeNinjaAPIRoadUnofficialOctriDemo
from sdk.client import ClientConfig, ClientAuthConfig, RetryConfig, IdempotencyConfig

async def main():
    seen = {}
    def handler(request):
        assert request.method == 'POST'
        assert request.headers.get('X-Apiroad-Key') == 'demo-not-a-secret'
        assert request.headers.get('X-RapidAPI-Key') is None
        assert json.loads(request.content)['url'] == 'https://example.com'
        seen.update(url=str(request.url), method=request.method, auth_header='X-Apiroad-Key')
        return httpx.Response(200, json={'info': {'statusCode': 200, 'finalUrl': 'https://example.com', 'headers': []}, 'body': '<html>mock</html>'})
    config = ClientConfig(base_url='https://scrapeninja.apiroad.net', auth=ClientAuthConfig(api_key_auth='demo-not-a-secret'), retry=RetryConfig(max_attempts=1), idempotency=IdempotencyConfig(enabled=False))
    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as http:
        config._client = http
        result = await ScrapeNinjaAPIRoadUnofficialOctriDemo(config).scrape.scrape(url='https://example.com')
        assert result.body == '<html>mock</html>'
    print(json.dumps({'mode': 'offline HTTP mock', 'status': 'passed', 'request': seen, 'response': 'HTML body parsed'}, indent=2))

asyncio.run(main())
