const { chromium } = require('playwright');
const path=require('path');
const [,,src,out,mode,png]=process.argv;
(async()=>{
 const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium-1194/chrome-linux/chrome'});
 const p=await b.newPage({viewport:{width:mode==='long'?1440:794,height:1000},deviceScaleFactor:2});
 await p.goto('file://'+path.resolve(src),{waitUntil:'networkidle'});
 await p.evaluate(()=>document.fonts.ready);
 if(mode==='long'){
   const h=await p.evaluate(()=>document.documentElement.scrollHeight);
   if(png) await p.screenshot({path:png,fullPage:true});
   await p.pdf({path:out,width:'1440px',height:(h+2)+'px',printBackground:true,pageRanges:'1'});
   console.log('height',h);
 } else {
   await p.pdf({path:out,format:'A4',printBackground:true,preferCSSPageSize:true});
   if(png) await p.screenshot({path:png,fullPage:true});
 }
 await b.close();
})();
