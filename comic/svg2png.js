const { chromium } = require('playwright');
(async()=>{const [svg,out,w]=process.argv.slice(2);const W=+w||2100;const fs=require('fs');
const s=fs.readFileSync(svg,'utf8');const b=await chromium.launch();const p=await b.newPage({viewport:{width:1400,height:440},deviceScaleFactor:W/1400});
await p.setContent('<html><body style="margin:0">'+s+'</body></html>');await p.waitForTimeout(300);
await (await p.$('svg')).screenshot({path:out});await b.close();})();
