const ITEMS=await (await fetch(BASE+'dl_items.json')).json();
const its=ITEMS[location.host]||[];if(!its.length)return 'NOITEMS '+location.host;
const T=new Uint32Array(256);for(let n=0;n<256;n++){let c=n;for(let k=0;k<8;k++)c=c&1?0xEDB88320^(c>>>1):c>>>1;T[n]=c>>>0}
const crc=b=>{let c=0xFFFFFFFF;for(let i=0;i<b.length;i++)c=T[(c^b[i])&255]^(c>>>8);return (c^0xFFFFFFFF)>>>0};
const enc=new TextEncoder();const parts=[];const cd=[];let off=0;const ok=[],bad=[];let total=0;
for(const [name,u] of its){try{
 const r=await fetch(u,{credentials:'include'});const b=new Uint8Array(await r.arrayBuffer());
 if(!r.ok){bad.push(name.slice(-4)+':s'+r.status);continue}
 if(b.length>60e6||total+b.length>180e6){bad.push(name.slice(-4)+':big');continue}
 const h4=String.fromCharCode(...b.slice(0,4));const ext=h4==='%PDF'?'.pdf':(h4.startsWith('PK')?'.docx':'.html');
 const fn=enc.encode(name+ext);const c=crc(b);
 const lh=new DataView(new ArrayBuffer(30));lh.setUint32(0,0x04034b50,true);lh.setUint16(4,20,true);lh.setUint16(8,0,true);lh.setUint32(14,c,true);lh.setUint32(18,b.length,true);lh.setUint32(22,b.length,true);lh.setUint16(26,fn.length,true);
 parts.push(new Uint8Array(lh.buffer),fn,b);
 const ch=new DataView(new ArrayBuffer(46));ch.setUint32(0,0x02014b50,true);ch.setUint16(4,20,true);ch.setUint16(6,20,true);ch.setUint32(16,c,true);ch.setUint32(20,b.length,true);ch.setUint32(24,b.length,true);ch.setUint16(28,fn.length,true);ch.setUint32(42,off,true);
 cd.push(new Uint8Array(ch.buffer),fn);off+=30+fn.length+b.length;total+=b.length;ok.push(name.slice(-4));
}catch(e){bad.push(name.slice(-4)+':E')}}
if(!ok.length)return 'NONE '+location.host+' bad '+bad.join(',');
const cdSize=cd.reduce((s,x)=>s+x.length,0);const e=new DataView(new ArrayBuffer(22));e.setUint32(0,0x06054b50,true);e.setUint16(8,ok.length,true);e.setUint16(10,ok.length,true);e.setUint32(12,cdSize,true);e.setUint32(16,off,true);
const blob=new Blob([...parts,...cd,new Uint8Array(e.buffer)],{type:'application/zip'});
const a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download='agc_'+location.host.replace(/[^a-z0-9.-]/gi,'_')+'.zip';document.body.appendChild(a);a.click();a.remove();
return 'OK '+location.host+' files '+ok.length+' bytes '+total+(bad.length?' bad '+bad.join(','):'');
