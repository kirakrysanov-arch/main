const { chromium } = require('playwright');const path=require('path');
const [,,src,sel,idx,out]=process.argv;
(async()=>{const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium-1194/chrome-linux/chrome'});
const p=await b.newPage({viewport:{width:1440,height:1000},deviceScaleFactor:2});
await p.goto('file://'+path.resolve(src),{waitUntil:'networkidle'});await p.evaluate(()=>document.fonts.ready);
const els=await p.$$(sel);await els[+idx].screenshot({path:out,type:'jpeg',quality:88});await b.close();})();
