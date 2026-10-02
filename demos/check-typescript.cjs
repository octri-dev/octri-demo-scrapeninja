const assert = require('node:assert/strict');
const {execFileSync} = require('node:child_process');
const path = require('node:path');
const root = path.resolve(__dirname, '..');
const dir = path.join(root, 'sdks/apiroad/typescript');
execFileSync(process.execPath, [path.join(root, 'node_modules/typescript/bin/tsc'), '-p', path.join(dir, 'tsconfig.json')], {stdio: 'inherit'});
const {ScrapeNinjaAPIRoadUnofficialOctriDemo} = require(path.join(dir, 'dist/index.js'));
let seen;
global.fetch = async (input, init) => {
  const request = new Request(input, init);
  assert.equal(request.method, 'POST');
  assert.equal(request.headers.get('X-Apiroad-Key'), 'demo-not-a-secret');
  assert.equal(request.headers.get('X-RapidAPI-Key'), null);
  assert.equal((await request.json()).url, 'https://example.com');
  seen = {url: request.url, method: request.method, auth_header: 'X-Apiroad-Key'};
  return new Response(JSON.stringify({info: {statusCode: 200, finalUrl: 'https://example.com', headers: []}, body: '<html>mock</html>'}), {status: 200, headers: {'Content-Type': 'application/json'}});
};
(async () => {
  const client = new ScrapeNinjaAPIRoadUnofficialOctriDemo({baseUrl: 'https://scrapeninja.apiroad.net', auth: {apiKeyAuth: 'demo-not-a-secret'}, retry: {maxAttempts: 1}, idempotency: {enabled: false}});
  const result = await client.scrape.scrape({url: 'https://example.com'});
  assert.equal(result.body, '<html>mock</html>');
  console.log(JSON.stringify({mode: 'offline HTTP mock', status: 'passed', request: seen, response: 'HTML body parsed'}, null, 2));
})().catch(error => {console.error(error); process.exitCode = 1;});
