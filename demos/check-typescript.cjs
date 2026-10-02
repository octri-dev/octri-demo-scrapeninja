const assert = require('node:assert/strict');
const {execFileSync} = require('node:child_process');
const path = require('node:path');
const root = path.resolve(__dirname,'..');
async function check(variant, className) {
 const dir = path.join(root,'sdks',variant,'typescript');
 execFileSync(process.execPath,[path.join(root,'node_modules/typescript/bin/tsc'),'-p',path.join(dir,'tsconfig.json')],{stdio:'inherit'});
 const sdk = require(path.join(dir,'dist/index.js'));
 let seen;
 global.fetch = async (input,init) => {
  const request = new Request(input,init);
  seen={url:request.url,apiroad_header:request.headers.get('X-Apiroad-Key'),rapidapi_header:request.headers.get('X-RapidAPI-Key')};
  const ok = seen.apiroad_header === 'demo-not-a-secret';
  return new Response(JSON.stringify(ok ? {info:{statusCode:200,finalUrl:'https://example.com',headers:[]},body:'<html>mock</html>'} : {message:'Mock APIRoad expects X-Apiroad-Key'}),{status:ok?200:401,headers:{'Content-Type':'application/json'}});
 };
 try {
  const result = await new sdk[className]({baseUrl:'https://scrapeninja.apiroad.net',auth:{apiKeyAuth:'demo-not-a-secret'},retry:{maxAttempts:1},idempotency:{enabled:false}}).scrape.scrape({url:'https://example.com'});
  assert.equal(result.body,'<html>mock</html>'); seen.outcome='accepted by mock';
 } catch(e) { if(variant!=='baseline') throw e; assert.equal(e.status ?? e.statusCode,401); seen.outcome='401 from mock'; }
 assert.match(seen.url,/^https:\/\/scrapeninja.apiroad.net\//);
 assert.equal(seen.apiroad_header,variant==='apiroad'?'demo-not-a-secret':null);
 assert.equal(seen.rapidapi_header,variant==='apiroad'?null:'demo-not-a-secret');
 return seen;
}
(async()=>console.log(JSON.stringify({mode:'offline mock; no live API calls',baseline:await check('baseline','ScrapeNinjaWebScraping'),apiroad:await check('apiroad','ScrapeNinjaAPIRoadUnofficialOctriDemo')},null,2)))().catch(e=>{console.error(e);process.exitCode=1;});
