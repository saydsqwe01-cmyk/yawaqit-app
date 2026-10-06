const CACHE='yawaqit-media-v8';
const MEDIA=/\/(assets|favicon|manifest)\//;
self.addEventListener('install',event=>{self.skipWaiting()});
self.addEventListener('activate',event=>{event.waitUntil(caches.keys().then(keys=>Promise.all(keys.filter(k=>k!==CACHE).map(k=>caches.delete(k)))).then(()=>self.clients.claim()))});
self.addEventListener('fetch',event=>{
  const req=event.request;
  if(req.method!=='GET') return;
  const url=new URL(req.url);
  if(url.origin!==self.location.origin) return;
  if(!MEDIA.test(url.pathname)) return;
  if(req.headers.has('range')) return;
  event.respondWith(caches.open(CACHE).then(async cache=>{
    const hit=await cache.match(req);
    if(hit) return hit;
    try{
      const response=await fetch(req);
      if(response.ok) cache.put(req,response.clone());
      return response;
    }catch(err){
      const fallback=await cache.match(req);
      if(fallback) return fallback;
      throw err;
    }
  }));
});
self.addEventListener('notificationclick',event=>{
  event.notification.close();
  event.waitUntil(self.clients.matchAll({type:'window',includeUncontrolled:true}).then(clients=>{
    const client=clients.find(c=>c.url.startsWith(self.location.origin));
    return client?client.focus():self.clients.openWindow('/');
  }));
});
